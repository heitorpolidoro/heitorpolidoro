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
    if not re.search(rf"<!-- {section}: starts -->.*<!-- {section}: ends -->", readme_content, flags=re.DOTALL):
        logging.warning(
            f"Section {section} no found in README.md\n<!-- {section}: starts -->\n<!-- {section}: ends -->")
    return re.sub(rf"<!-- {section}: starts -->.*<!-- {section}: ends -->",
                  f"<!-- {section}: starts -->\n{content}\n<!-- {section}: ends -->", readme_content, flags=re.DOTALL)


def get_last_working_repositories(last=1, days=30):
    repos = list(user.get_repos(sort="pushed"))
    resp = []
    for repo in repos:
        if repo.name == "heitorpolidoro":
            continue
        if repo.pushed_at.date() <= now - datetime.timedelta(days=days):
            continue
        resp.append(repo)
        if len(resp) >= last:
            break

    return resp


def build_working_on_section(last=5, days=30):
    def _scape(text):
        return text.replace("_", "__").replace("-", "--").replace(" ", "_")

    repos = get_last_working_repositories(last=last, days=days)

    current_working_on_template = f"""
<div align="center">

### 🔭 I’m currently working on:
$projects 
</div>
"""
    projects = [
        f"![{repo.name.title()}](https://img.shields.io/badge/{_scape(repo.name)}-{_scape(repo.description or 'No description')}-lightgreen)"
        for repo in repos]
    return Template(current_working_on_template).safe_substitute(projects="<br>\n".join(projects))


def build_activity_section(last=10):
    events_to_ignore = {
        "pullrequestreview",
        "watch",
    }

    events = []
    seen_events = set()
    count = 0
    user_events = iter(user.get_events())
    while count < last:
        template = (
            "- <img src='$icon' width='12'> $event_title in <a href='http://github.com/$repo'>$repo</a>"
        )
        event = next(user_events)
        event_type = event.type.replace("Event", "").lower()
        if event_type in events_to_ignore:
            continue

        match event_type:
            case "create" | "delete":
                event_type = f"{event_type}_{event.payload['ref_type']}"
            case "pullrequestreviewcomment":
                event_type = "comment"
            case "issues":
                event_type = f"issue_{event.payload['action']}"
                template = (
                    "- <img src='$icon' width='12'> Issue $payload_action in <a href='http://github.com/$repo'>"
                    "$repo</a> -> <a href='http://github.com/$payload_issue_number'>$payload_issue_title</a>"
                )
            case "pullrequest":
                event_type = f"pull_request_{event.payload['action']}"
                if event.payload['action'] == "closed":
                    if not event.payload['pull_request']['merged']:
                        event_type += "_not"
                    else:
                        event_type = event_type.replace("_closed", "")
                    event_type += "_merged"

        event_key = f"{event_type}_{event.repo.name}"
        if event_key in seen_events:
            continue
        seen_events.add(event_key)
        count += 1
        attrs = set(re.findall(r"\$([\w.]+)", template))
        info = {}
        for attr in attrs:
            match attr:
                case "icon":
                    try:
                        info[attr] = f"icons/{event_type}.svg"
                    except KeyError:
                        raise ValueError(f"Missing icon for {event_type}")
                case "event_title":
                    info[attr] = event_type.replace("_", " ").title()
                case "repo":
                    info[attr] = event.repo.name
                case _:
                    aux = event
                    for a in attr.split("_"):
                        if isinstance(aux, dict):
                            aux = aux.get(a)
                        else:
                            aux = getattr(aux, a, None)
                        if aux is None:
                            break
                    info[attr] = aux or ""

        events.append(Template(template).safe_substitute(**info))

    return "\n".join(events)


if __name__ == "__main__":
    readme = root / "README.md"
    readme_content = readme.open().read()
    readme_content = replace_section(readme_content, "working_on", build_working_on_section())
    # readme_content = replace_section(readme_content, "activity", build_activity_section())
    readme.open("w").write(readme_content)
