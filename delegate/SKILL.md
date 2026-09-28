---
name: delegate
description: Hand work to an OpenCode session in a Herdr tab instead of a Claude subagent. Use for any lookup, research, review, prototype build or chore that doesn't need the user in the loop.
---

Claude keeps planning, judgment, code the user asked Claude to write, and quick commands with short output (a lint or typecheck after an edit); everything else is delegated. Needs `HERDR_ENV=1`; without it, do small lookups inline and ask before anything bigger.

Scripts are in `~/.agents/skills/delegate/scripts/`; they take a job name. Use them rather than typing the git, Rift or API steps yourself.

1. Write a brief to your scratchpad. It stands alone: the job, what to read, what done looks like. `spawn` appends the report contract (TL;DR first, then `DONE`).
2. `spawn <name> <brief> [--rift <branch>] [--model <tier>]`
   - `--rift <branch>` for any job that writes: it works in a Rift (an instant copy of the checkout, uncommitted work included) on that branch. Read-only jobs run in the checkout.
   - Tiers are in `../models`: `light` for small reading jobs (lookups, finding a doc or API fact), `hard` only when the default failed or clearly can't cope, the default for everything else.
3. Run `await <name>` with Bash `run_in_background`, one per job. It prints only the TL;DR; open `result.md` only when a decision needs the detail.
4. On exit **0** (done), check the work where it landed, not the report. **2** (blocked): show the user what it needs; never answer an approval yourself. **3** (stalled), **4** (timed out) or **5** (hung: running with no new tokens for 15 minutes; `await` prints how to interrupt it): read its tab (`herdr agent read <name> --source visible`), then `followup` or tell the user.
5. More to do in the same context? `followup <name> "<message>"`, then `await` again.
6. Writing jobs: `land <name>` copies the branch into the source repo, unmerged. Before the user merges anything beyond a small docs change, spawn a `--model hard` verifier that tries to disprove it, and relay only what survives. Once it's merged, pushed or discarded, run `finish <name>` (removes the Rift; the tab stays).

`jobs` lists every job with its status, which helps after a context compaction.

## Briefs

- **Lookup** (`--model light`): the question. Answer with `file:line` references or source URLs.
- **Research**: `--rift research/<slug>`. Follow the `research` skill, commit to `docs/research/<slug>.md`, push the branch.
- **Review**: the diff or branch. Each finding gives `file:line`, what breaks, and how; then verify as in step 6.
- **Prototype**: `--rift prototype/<slug>`. Follow the `prototype` skill, push the branch, say how to run it.
- **Chore** (long checks, docs, packaging): `--rift chore/<slug>`, commit.
