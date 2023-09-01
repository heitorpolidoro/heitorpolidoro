set -e

wget https://raw.githubusercontent.com/heitorpolidoro/projects-actions-health/master/README-template.md
repo=$(pwd | sed -e "s;^$HOME;~;" | sed -e "s;^~/workspace/;;")
sed -i "s;\$repo;$repo;" README-template.md
mkdir .github/workflows -p
cd .github
wget https://raw.githubusercontent.com/heitorpolidoro/projects-actions-health/master/CODEOWNERS
wget https://raw.githubusercontent.com/heitorpolidoro/projects-actions-health/master/FUNDING.yml
cd workflows
wget https://raw.githubusercontent.com/heitorpolidoro/projects-actions-health/master/ci_cd.yml
wget https://raw.githubusercontent.com/heitorpolidoro/projects-actions-health/master/create.yml
wget https://raw.githubusercontent.com/heitorpolidoro/projects-actions-health/master/release.yml
