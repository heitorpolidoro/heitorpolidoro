import datetime
import logging
import pathlib
import re
from string import Template

from github import Github

root = pathlib.Path(__file__).parent.resolve()
now = datetime.datetime.utcnow().date()


def replace_section(readme_content, section, content):
    if not re.search(rf"<!-- {section}: starts -->.*<!-- {section}: ends -->", readme_content, flags=re.DOTALL):
        logging.warning(f"Section {section} no found in README.md\n<!-- {section}: starts -->\n<!-- {section}: ends -->")
    return re.sub(rf"<!-- {section}: starts -->.*<!-- {section}: ends -->",
                  f"<!-- {section}: starts -->\n{content}\n<!-- {section}: ends -->", readme_content, flags=re.DOTALL)


def get_last_working_repositories(last=1, days=30):
    repos = list(Github().get_user("heitorpolidoro").get_repos())
    return [r for r in repos[:last] if r.pushed_at.date() > now - datetime.timedelta(days=days) and r.name != "heitorpolidoro"]


def build_working_on_section(last=1, days=30):
    def _scape(text):
        return text.replace("_", "__").replace("-", "--").replace(" ", "_")
    repos = get_last_working_repositories(last=last, days=days)

    current_working_on_template = f"""
<div align="center">

### 🔭 I’m currently working on:
$projects 
</div>
"""
    projects = [f"![{repo.name.title()}](https://img.shields.io/badge/{_scape(repo.name)}-{_scape(repo.description or 'No description')}-lightgreen)" for repo in repos]
    return Template(current_working_on_template).safe_substitute(projects="<br>\n".join(projects))


def build_badges_section(sub_sections):
    badges_template = f"""
<div align="center">

$badges 
</div>
"""
    badges = []
    for sub_section, info in sub_sections.items():
        badges = [

        ]
        info["url"] = f"https://img.shields.io/badge/{sub_section}-{info['value']}-{info['color']}"


if __name__ == "__main__":
    readme = root / "README.md"
    readme_content = readme.open().read()
    readme_content = replace_section(readme_content, "working_on", build_working_on_section())
    # from simpleicons.all import icons
    #
    # Get a specific icon by its slug as:
    # print(icons.get('python').__dict__)
    # readme_content += "\n\n---" + icons.get("python").svg
    readme.open("w").write(readme_content)

