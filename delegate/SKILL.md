---
name: delegate
description: Delegate independent lookups, research, reviews, prototypes and chores to Pi in Herdr.
---

Keep planning, judgment, requested code and quick checks; delegate the rest. Requires `HERDR_ENV=1`; otherwise do small lookups inline and ask before larger work.

Use `~/.agents/skills/delegate/scripts/`:

1. Write a standalone brief: task, sources, acceptance criteria.
2. `spawn <name> <brief.md> [--rift <branch>] [--model <tier>] [--cwd <dir>]`. Any repo writes require a Rift (copies uncommitted work too). Default: GPT 6.1 Sol medium; `light`: low for lookups; `hard`: high for verification or when default cannot cope. See `models`.
3. `await <name|job-dir> [minutes=60]`. Prints TL;DR; read `result.md` only for needed detail. In Claude Code: run each `await` with Bash `run_in_background`, one per job, and return to the user; you're woken on exit. Otherwise: poll; keep monitoring until resolved or user input is needed.
4. Exit `0`: inspect actual work. `2`: show the user the blocker; never approve for them. `3/4/5`: stalled/timeout/possibly hung—read `herdr agent read <name> --source visible` before retrying or interrupting.
5. Continue: `followup <job> "message"`, then await again.
6. Writes: `land <job>` imports the committed branch, **without merging**. Before merging anything beyond small docs, spawn a `hard` adversarial verifier; relay substantiated findings. After merge/push/discard, run `finish <job>`.

Always `finish <job>` when no follow-up remains (including read-only jobs): closes Pi and its tab, removes any Rift, retains branches/reports/sessions. Never finish blocked or unresolved work.

`jobs` recovers state after compaction; resume unfinished watchers. Agents work alone, report TL;DR (≤8 lines) then details/citations, create `DONE` last, or write `BLOCKED` for human input. Pi runs in its tab, not a detached service; idle alone is not completion.

Brief contracts:
- Lookup: `light`; answer with `file:line` or URLs.
- Research: `research/<slug>` Rift; follow `research`, commit `docs/research/<slug>.md`, push.
- Review: specify diff/branch; findings give `file:line`, what breaks and how; verify.
- Prototype: `prototype/<slug>` Rift; follow `prototype`, push, give run instructions.
- Chore: `chore/<slug>` Rift; commit.
