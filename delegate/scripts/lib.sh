# shellcheck shell=bash
# Sourced by the delegate scripts.
jobs_root=${TMPDIR:-/tmp}
jobs_root=${jobs_root%/}

# job <name|dir>: print the job dir (the newest one for a name).
job() {
  if [ -d "$1" ]; then echo "${1%/}"; return; fi
  local d
  d=$(ls -dt "$jobs_root"/delegate."$1".* 2>/dev/null | head -1)
  [ -n "$d" ] || { echo "no job named $1" >&2; return 1; }
  echo "$d"
}

# Live Herdr state; unknown on lookup failure.
agent_state() {
  herdr agent get "$(cat "$1/pane" 2>/dev/null || cat "$1/name")" 2>/dev/null |
    python3 -c 'import json,sys; print(json.load(sys.stdin)["result"]["agent"]["agent_status"])' 2>/dev/null || echo unknown
}

# status <dir>: finished, done, blocked, running, stopped or unknown.
status() {
  if [ -f "$1/finished" ]; then echo finished
  elif [ -f "$1/DONE" ]; then echo 'done'
  elif [ -f "$1/BLOCKED" ]; then echo blocked
  else
    local state
    state=$(agent_state "$1")
    case "$state" in
      working) echo running ;;
      blocked) echo blocked ;;
      idle|done) echo stopped ;;
      *) echo unknown ;;
    esac
  fi
}

# tldr <dir>: the TL;DR section of result.md.
tldr() {
  [ -f "$1/result.md" ] || return 0
  awk '/^## TL;DR/{on=1; next} on && /^#/{exit} on && NF' "$1/result.md" | head -8
}
