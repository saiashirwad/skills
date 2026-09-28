---
name: delegate
description: Hand work to an OpenCode session in a Herdr tab instead of a Claude subagent. Use for any lookup, research, review, prototype build or chore that doesn't need the user in the loop.
---

Never use the Agent tool or Workflows; delegate. Claude keeps planning, judgment, code the user asked Claude to write, and quick commands with short output (a lint or typecheck after an edit). Needs `HERDR_ENV=1`; without it, do small lookups inline and ask before anything bigger.

1. Write a brief to your scratchpad. It stands alone: the job, what to read, what done looks like. `spawn` appends the report contract.
2. `~/.agents/skills/delegate/scripts/spawn <name> <brief> [--rift <branch>] [--model <tier>]` prints a job dir.
   - `--rift <branch>` for any job that writes: it works in a Rift (an instant copy of the checkout, uncommitted work included) on that branch. Read-only jobs run in the checkout.
   - Tiers are in `~/.agents/skills/delegate/models`. Use the default unless it failed or the job clearly needs `hard`.
3. Run `~/.agents/skills/delegate/scripts/await <job> [minutes]` with Bash `run_in_background`. Fan out by spawning several.
4. On exit **0** (done), check the work where it landed, not the report. **2** (blocked): show the user what it needs; never answer an approval yourself. **3** (stalled) or **4** (timed out): read its tab (`herdr agent read <name> --source visible`), then re-brief or tell the user. Leave tabs open.

## Briefs

- **Lookup**: the question. Answer with `file:line` references.
- **Research**: `--rift research/<slug>`. Follow the `research` skill, commit to `docs/research/<slug>.md`, push the branch.
- **Review**: the diff or branch. Each finding gives `file:line`, what breaks, and how. Then spawn a `--model hard` verifier that tries to disprove each finding from the code; relay only what survives.
- **Prototype**: `--rift prototype/<slug>`. Follow the `prototype` skill, push the branch, say how to run it.
- **Chore** (long checks, docs, packaging): `--rift chore/<slug>`, commit. Bring it back with `git fetch <rift> <branch>` (`head -1 <job>/rift` is the Rift path) and show the user the diff; they merge.

Once a Rift's branch is pushed or merged, run `rift remove <path>`.
