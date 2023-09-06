set -e
download() {
  target=$1
  echo "Downloading ${target}"
  curl -s -o ".${target}" "https://raw.githubusercontent.com/heitorpolidoro/heitorpolidoro/master/${target}"
}

download README-template.md
echo "Replacing in README-template.md"
repo=$(pwd | sed -e "s;^$HOME;~;" | sed -e "s;^~/workspace/;;")
sed -i '' -e "s/\$repo/${repo}/g" .README-template.md
mv .README-template.md README.md
mkdir -p .github/workflows
download github/CODEOWNERS
download github/FUNDING.yml
download github/workflows/ci_cd.yml
download github/workflows/create.yml
download github/workflows/release.yml
