set -e

mkdir .github/workflows -p
cd .github
wget https://raw.githubusercontent.com/heitorpolidoro/projects-actions-health/master/CODEOWNERS
wget https://raw.githubusercontent.com/heitorpolidoro/projects-actions-health/master/FUNDING.yml
cd workflows
wget https://raw.githubusercontent.com/heitorpolidoro/projects-actions-health/master/ci_cd.yml
wget https://raw.githubusercontent.com/heitorpolidoro/projects-actions-health/master/create.yml
wget https://raw.githubusercontent.com/heitorpolidoro/projects-actions-health/master/release.yml
