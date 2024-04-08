from string import Template

TEMPLATE = """## $project_name

$github_actions_badges
<br>
$github_repository_badges

$sonar_badges
<br>
$deepsource_badges
"""
GITHUB_ACTION_BADGE_TEMPLATE = "[![$action_name](https://github.com/$repository/actions/workflows/$action_file/badge.svg)](https://github.com/$repository/actions/workflows/$action_file)"

GITHUB_REPOSITORY_BADGES_TEMPLATE = """[![Latest Version](https://img.shields.io/github/v/release/$repository?label=Latest%20Version)](https://github.com/$repository/releases/latest)
![GitHub Release Date](https://img.shields.io/github/release-date/$repository)
![GitHub commits since latest release (by SemVer including pre-releases)](https://img.shields.io/github/commits-since/$repository/latest)
![GitHub last commit](https://img.shields.io/github/last-commit/$repository)
<br>
[![GitHub issues](https://img.shields.io/github/issues/$repository)](https://github.com/$repository/issues)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/$repository)](https://github.com/$repository/pulls)
"""

SONAR_BADGES_TEMPLATE = """[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=$project_slug&metric=coverage)](https://sonarcloud.io/summary/new_code?id=$project_slug)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=$project_slug&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=$project_slug)
<br>
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=$project_slug&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=$project_slug)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=$project_slug&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=$project_slug)
[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=$project_slug&metric=reliability_rating)](https://sonarcloud.io/summary/new_code?id=$project_slug)
<br>
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=$project_slug&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=$project_slug)
[![Duplicated Lines (%)](https://sonarcloud.io/api/project_badges/measure?project=$project_slug&metric=duplicated_lines_density)](https://sonarcloud.io/summary/new_code?id=$project_slug)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=$project_slug&metric=vulnerabilities)](https://sonarcloud.io/summary/new_code?id=$project_slug)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=$project_slug&metric=bugs)](https://sonarcloud.io/summary/new_code?id=$project_slug)
[![Technical Debt](https://sonarcloud.io/api/project_badges/measure?project=$project_slug&metric=sqale_index)](https://sonarcloud.io/summary/new_code?id=$project_slug)"""

DEEPSOURCE_BADGE_TEMPLATE = "[![DeepSource](https://app.deepsource.com/gh/$repository.svg/?label=active+issues&show_trend=true&token=hZuHoQ-gd4kIPgNuSX0X_QT2)](https://app.deepsource.com/gh/$repository/)"
VERCEL_BADGE_TEMPLATE = "![Vercel](https://vercelbadge.vercel.app/api/$repository)"

PYPI_BADGE_TEMPLATE = (
    "![PyPI](https://img.shields.io/pypi/v/$package?label=pypi%20package)"
)

CHECKLY_BADGE_TEMPLATE = "![](https://api.checklyhq.com/v1/badges/checks/$checkly_id?style=flat&theme=default)"

PYPI_PROJECTS = ["github-app-handler"]
VERCEL_PROJECTS = ["bartholomew-smith"]
CHECKLY_PROJECTS = {"bartholomew-smith": "b7690d9e-b7e7-4637-b601-c6611d06b848"}

GITHUB_ACTIONS = {
    "github-app-handler": {
        "Code Quality": "code_quality.yml",
        "PyPi Package": "pypi-publish.yml",
    },
    "bartholomew-smith": {
        "Code Quality": "code_quality.yml",
        "CodeQL": "github-code-scanning/codeql",
    },
}

PROJECTS = {
    "Github App Handler": "github-app-handler",
    "Bartholomew Smith": "bartholomew-smith",
}


def fix_repository(repository: str) -> str:
    if "/" not in repository:
        repository = "heitorpolidoro/" + repository
    return repository


def generate_badge(template: str, **values: str) -> str:
    template = Template(template)
    return template.safe_substitute(**values)


def generate_github_actions_badges(repository: str) -> str:
    badges = []
    for name, file in GITHUB_ACTIONS.get(repository, {}).items():
        badges.append(
            generate_badge(
                GITHUB_ACTION_BADGE_TEMPLATE,
                action_name=name,
                action_file=file,
                repository=fix_repository(repository),
            )
        )
    return "\n".join(badges)


def generate_file():
    with open("project-health-check.md", "w") as readme:
        for project_name, repository in PROJECTS.items():
            fixed_repository = fix_repository(repository)
            project_health_check = Template(TEMPLATE).safe_substitute(
                project_name=project_name,
                github_actions_badges=generate_github_actions_badges(repository),
                github_repository_badges=generate_badge(
                    GITHUB_REPOSITORY_BADGES_TEMPLATE,
                    repository=fixed_repository,
                ),
                sonar_badges=generate_badge(
                    SONAR_BADGES_TEMPLATE,
                    project_slug=fixed_repository.replace("/", "_"),
                ),
                deepsource_badges=generate_badge(
                    DEEPSOURCE_BADGE_TEMPLATE,
                    repository=fixed_repository,
                ),
            )
            readme.write(project_health_check)
            if repository in PYPI_PROJECTS:
                readme.write(
                    "<br>\n"
                    + generate_badge(PYPI_BADGE_TEMPLATE, package=repository)
                    + "\n"
                )
            if repository in VERCEL_PROJECTS:
                readme.write(
                    "<br>\n"
                    + generate_badge(VERCEL_BADGE_TEMPLATE, repository=fixed_repository)
                    + "\n"
                )


if __name__ == "__main__":
    generate_file()
