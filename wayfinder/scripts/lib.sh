# shellcheck shell=bash
# Sourced by the wayfinder scripts. Works on the repo of the current directory.
set -euo pipefail

die () { echo "$(basename "$0"): $*" >&2; exit 1; }

R=repos/$(gh repo view --json nameWithOwner --jq .nameWithOwner) ||
  die 'not in a GitHub repo'

# num <n|url>: the issue number.
num () { echo "${1##*/}"; }

# id <n|url>: the issue's database id, for the sub-issue and dependency APIs.
id () { gh api "$R/issues/$(num "$1")" --jq .id; }

# link <n>: the issue as a Markdown link with its title.
link () { gh api "$R/issues/$(num "$1")" --jq '"[\(.title)](\(.html_url))"'; }

label () { gh label create "$1" --color "${2:-c5def5}" &>/dev/null || true; }
