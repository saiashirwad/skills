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

# status <dir>: finished, done, blocked, running or stopped.
status() {
  if [ -f "$1/finished" ]; then echo finished
  elif [ -f "$1/DONE" ]; then echo done
  elif [ -f "$1/BLOCKED" ]; then echo blocked
  elif opencode api get /api/session/active 2>/dev/null | grep -q "\"$(cat "$1/session")\""; then echo running
  else echo stopped
  fi
}

# tldr <dir>: the TL;DR section of result.md.
tldr() {
  [ -f "$1/result.md" ] || return 0
  awk '/^## TL;DR/{on=1; next} on && /^#/{exit} on && NF' "$1/result.md" | head -8
}
