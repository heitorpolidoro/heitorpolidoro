import datetime
import json
import os
import pathlib
import re
import subprocess

from github import Github

root = pathlib.Path(__file__).parent.resolve()
now = datetime.datetime.utcnow().date()


def replace_section(readme_content, section, content):
    return re.sub(rf"<!-- {section} starts -->.*<!-- {section} ends -->",
                  f"<!-- {section} starts -->\n{content}\n<!-- {section} ends -->", readme_content, flags=re.DOTALL)


def get_last_working_repositories(last=4, days=30):
    return [r.name for r in Github(os.getenv("GITHUB_TOKEN")).get_user("heitorpolidoro").get_repos()[:last] if
            r.pushed_at.date() > now - datetime.timedelta(days=days)]


def build_working_on_section():
    current_working_on = """
### 🔭 I’m currently working on:

"""

    for repo in get_last_working_repositories():
        current_working_on += f"[![Profile](https://github-readme-stats.vercel.app/api/pin/?username=heitorpolidoro&repo={repo}&theme=dark)](https://github.com/heitorpolidoro/{repo})\n"

    return current_working_on


if __name__ == "__main__":
    readme = root / "README.md"
    readme_content = readme.open().read()
    readme_content = replace_section(readme_content, "working_on", build_working_on_section())
    readme.open("w").write(readme_content)
