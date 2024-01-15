import datetime
import logging
import os
import pathlib
import re
from string import Template

from github import Github

root = pathlib.Path(__file__).parent.resolve()
now = datetime.datetime.utcnow().date()
user = Github(os.getenv("GITHUB_TOKEN")).get_user("heitorpolidoro")


def replace_section(readme_content, section, content):
    if not re.search(
        rf"<!-- {section}: starts -->.*<!-- {section}: ends -->",
        readme_content,
        flags=re.DOTALL,
    ):
        logging.warning(
            f"Section {section} no found in README.md\n<!-- {section}: starts -->\n<!-- {section}: ends -->"
        )
    return re.sub(
        rf"<!-- {section}: starts -->.*<!-- {section}: ends -->",
        f"<!-- {section}: starts -->\n{content}\n<!-- {section}: ends -->",
        readme_content,
        flags=re.DOTALL,
    )


def get_last_working_repositories(last=1, days=30):
    repos = list(user.get_repos(sort="pushed"))
    resp = []
    for repo in repos:
        hide_repos = ["heitorpolidoro", ".github"]
        if repo.name in hide_repos:
            continue
        if repo.pushed_at.date() <= now - datetime.timedelta(days=days):
            continue
        resp.append(repo)
        if len(resp) >= last:
            break

    return resp


def build_working_on_section(last=2, days=30):
    def _scape(text):
        return text.replace("_", "__").replace("-", "--").replace(" ", "_")

    repos = get_last_working_repositories(last=last, days=days)

    current_working_on_template = """
<div align="center">

### 🔭 I’m currently working on:
$projects 
</div>
"""
    projects = [
        f"[![{repo.name.title()}](https://img.shields.io/badge/{_scape(repo.name)}-{_scape(repo.description or 'No description')}-lightgreen)]({repo.html_url})"
        for repo in repos
    ]
    return Template(current_working_on_template).safe_substitute(
        projects="<br>\n".join(projects)
    )


if __name__ == "__main__":
    readme = root / "README.md"
    readme_content = readme.open().read()
    readme_content = replace_section(
        readme_content, "working_on", build_working_on_section()
    )
    readme.open("w").write(readme_content)
