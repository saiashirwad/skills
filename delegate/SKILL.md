---
name: delegate
description: Delegate independent lookups, research, reviews, prototypes and chores to Pi in Herdr.
---

- Delegate lookups, research, reviews, prototypes, chores; keep planning, judgment, requested code, quick checks
  - Outside Herdr (`HERDR_ENV` ≠ 1): do small lookups inline, ask before bigger work
- Scripts live in `~/.agents/skills/delegate/scripts/`
- Write a standalone brief: task, sources, acceptance criteria
  - Lookup: `--model light`; answer with `file:line` or URLs
  - Research: `--rift research/<slug>`; follow `research`; commit `docs/research/<slug>.md`, push
  - Review: name the diff/branch; findings give `file:line`, what breaks and how
  - Prototype: `--rift prototype/<slug>`; follow `prototype`; push; give run instructions
  - Chore: `--rift chore/<slug>`; commit
- `spawn <name> <brief.md> [--rift <branch>] [--model light|hard] [--cwd <dir>]`
  - Any repo write needs `--rift` (isolated copy, uncommitted work included)
  - `hard` for verification or when the default can't cope; tiers in `models`
- `await <job> [minutes=60]` prints the TL;DR and what to do next
  - In Claude Code: one Bash `run_in_background` per job, then return to the user; you're woken on exit
  - Otherwise: poll until resolved or the user is needed
  - Done: inspect the actual work; read `result.md` only for detail you need
- `followup <job> "message"`, then await again
- Writes: `land <job>` copies the branch into the source repo, unmerged
  - Before merging more than small docs: spawn a `hard` adversarial verifier; relay substantiated findings
- `finish <job>` once nothing is left, read-only jobs too: closes the tab, removes the Rift, keeps branches and reports
  - Never on blocked or unresolved work
- After compaction: `jobs` shows state; restart watchers for unfinished jobs
