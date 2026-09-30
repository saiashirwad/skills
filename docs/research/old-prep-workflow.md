# The old `~/code/prep` study workflow

Research for [ticket #15](https://github.com/saiashirwad/skills/issues/15), in [map #1](https://github.com/saiashirwad/skills/issues/1). Inspected 2026-09-30. **History, not a proposed specification.**

## Answer

`prep` was a local, agent-assisted interview-preparation workspace: the agent supplied question ladders, problem scaffolds and tests; the user derived ideas and wrote solutions; the agent maintained a dictated evidence ledger and a spaced-rebuild queue. Its durable principle was **retrieval rather than apparent understanding**. Its documented failure was leaving routine variations and scheduled rebuilds undone after the interesting insight. Later work added annotated architecture reading, and an uncommitted September rewrite separated Derive, Teach, Check, Rep and Interview modes. These were successive protocols, not one consistent system. [S1–S8]

The new study family should borrow learner-owned attempts, minimal hints, assistant-written evidence, session-start reviews, and reconstruction after teaching. It should **not** inherit fixed review intervals, disposable attempts, six-problem batches, or the old prohibition on grading/timing as universal rules: those conflict with the explicit September 30 study decisions. [S2–S6, S12]

## Evidence boundary

- The inspected repository is `/Users/texoport/code/prep`; local `main` was `1a3f7569d78e5414838bbcb9e2f1bef679e96d23` (2026-08-31). `origin` is `git@github.com:saiashirwad/prep.git`. GitHub links below identify commits/files, but remote accessibility was not verified. Local Git objects are the evidence. [S1]
- The checkout was **dirty**: `.claude/problem-setup.md`, `.claude/session-start.sh`, and `.claude/settings.json` were deleted locally; `CLAUDE.md`, `GOALS.md`, `LOG.md`, and `TODO.md` were modified; `MEMORY.md` was untracked. `AGENTS.md` is a tracked symlink to `CLAUDE.md`, not an independent contract. September material below is explicitly working-tree evidence, not committed history. Nothing in `prep` was changed for this research. [S1, S8]
- Statements about learning success are the repository's recorded observations, not independently measured outcomes. In particular, one July ledger entry explicitly says it was reconstructed from files rather than observed; August annotated-reading notes explicitly say retention had not yet been tested. [S4, S7]

## Structure and day-to-day mechanics

| Area | What it did |
|---|---|
| `src/1`, `src/2`, `src/tree`, `src/backtracking`, `src/graph`, `src/dp` | TypeScript attempts and embedded cases. Early sets were numbered by session; later folders were topics. Tree problems shared `src/tree/tree.ts`. [S1, S3] |
| `problems.md`, `session2.md` | Early six-problem session sheets: warm-up/core/stretch blocks, about two hours, cold attempts, written approach, rebuild and spoken narration. These retained rules later superseded by the setup prompt. [S2] |
| `SETUP-PROMPT.md` | Reusable paste-in installer: interview the learner about language, background, review preference, failure modes, time/complexity bounds and goals; generate workspace; install tutor rules; confirm before producing problems. [S3] |
| `CLAUDE.md` / `AGENTS.md` | Startup contract: user solves; agent derives with questions, provides conventions immediately, and records evidence. September expanded this into explicit modes. [S6, S8] |
| `LOG.md` | Assistant-written ledger and dated standing patterns; entries distinguish Derived, Hints, Pattern, Next rep. No user forms, no “solved alone” score column. [S4] |
| `REPS.md` | Manual spaced re-derivation queue: thing, first derived, next due, attempts, what broke. Blank file/no notes/10-minute cap, then delete attempt and advance date by +3/+10/+30 days. [S5] |
| `CARDS.md` | On-request, topic-grouped hub questions: self-contained fronts, short answers in the user's words, connected ideas rather than isolated facts. Not an observed automated flashcard scheduler. [S6] |
| `GOALS.md`, `TODO.md` | Longer tracks and immediate next steps. Current local version prioritizes Google L4/Python, leaves existing TS files intact, and parks reconciler/backprop/Kyoot work behind due reps. [S8] |
| `annotated-reading.md`, `kyoot.md` | August evidence and proposed protocol for complete architecture explanations, batched annotations, a coherent second pass and later no-notes reconstruction. [S7] |
| `MEMORY.md` | Untracked September living learner model: per-topic stable/shaky knowledge, dated evidence, stale claims to reverify; agent writes it, user does not fill it in. [S8] |
| `scratch/`, `node_modules/` | Present locally and ignored by Git. Temporary work therefore cannot be reconstructed from committed history alone. [S1] |

### Problems, help and code ownership

The later setup convention chose **shapes before volume** and plain-language titles, supplied a prose statement, edge-case examples, one decision question without algorithm vocabulary, then an empty typed body and test harness. The prescribed harness printed **got | expected**, with no automatic green tick or summary: comparing output was itself a practice target. The agent was forbidden to write solution bodies or modify an existing `src/` file. Shared topic helpers were encouraged. [S3]

This was a target convention, not a uniform migration. The existing palindrome file still has an explicit complexity target, a “two indices” hint and bare `console.log`s; the newer stairs file has a decision paragraph and named two-column cases. Thus copying all old files would copy contradictory generations of pedagogy. [S9]

Help was a weakest-hint ladder, with the smallest counterexample instead of a correction. Syntax, stdlib and vocabulary were handed over rather than turned into riddles. “Just tell me” allowed a clean answer, followed by diagnosis and a queued rep. Code shown to the agent did not automatically request review: verification, review, hint and acknowledgment were distinct intents. [S3, S6, S8]

### Reviews, notes and actual follow-through

Reviews meant **rebuilding**, not rereading: start the next sitting with due reps, diagnose what failed, and distinguish recognition from execution and insight from implementation mechanics. The ledger recorded supplied help without making it a debit. The queue contains concrete failures—for example, tree diameter confused the value returned upward with the answer recorded separately; Path Sum III mixed helper meanings and stopped too early on a match. [S4–S5]

Follow-through was limited in the surviving evidence. `REPS.md` still has three zero-attempt `due` rows (permutations, Kahn's topo, DFS topo) and dated July/August reviews. July's ledger recorded 13 unstarted versus 15 finished problems and named “abandons a set once the aha is spent.” The September memory explicitly calls the evidence stale and says there is not yet a study streak under the new protocol. This supports **lapsed recorded repetition**, not a claim that no off-repo practice occurred. [S4–S5, S8]

August added a different activity: requested complete explanations of existing systems, reading aloud with Clipboard Annotator, then batched questions about unstable connections. The September contract calls the tool SendPoint and permits 500–1000-word Teach passes, a connected second pass and a no-notes reconstruction; Derive remains the default for interview material. “Long explanations are now allowed” did **not** mean “derivation was abandoned.” [S7–S8]

## Tooling, prompts and guardrails

- `package.json` declares Node >=24, ESM, TypeScript and Node types; `pnpm-lock.yaml` is committed. Scripts are `start: node src/index.ts` and `typecheck: tsc --noEmit`. `src/index.ts` was deleted in July, so the surviving start script targets a missing file. This is a collection of individually runnable attempts rather than a maintained central exercise runner; no new dependency installation or execution of learner code was needed for this investigation. [S1, S10]
- Committed Claude configuration used a `PreToolUse` hook for `Edit|Write|NotebookEdit` to reject existing `src/` paths, plus a `SessionStart` re-entry shell script. The script heuristically counted code lines to list unstarted TS files and pointed to `REPS.md`. It did **not** implement calendar-aware scheduling: its `due` grep result was unused. The setup prompt explicitly rejected end-of-session form-filling hooks. [S3, S10]
- `.pi/extensions/prep.ts` ported the edit/write guard and re-entry card, injected the card into the agent prompt, and exposed `/prep`. `.codex/hooks.json` contains the Claude-style configuration and still references `$CLAUDE_PROJECT_DIR/.claude/session-start.sh`. Configuration files demonstrate intended integration, not proof those versions of the agents loaded them correctly. [S10]
- Current local `.claude/` deletions leave the Pi re-entry path missing (the extension returns an empty card in that case) and the Codex script reference stale. The Pi edit/write guard is independent of that script. These are partial tool guards, not a security boundary against shell writes or every possible editing tool. [S1, S10]
- A repo-local Hermes skill, `.hermes/skills/derive-dont-explain/`, was added August 23 with `how-he-learns.md` and `derived-so-far.md` references, then explicitly removed August 30. It added prediction-before-running, re-posing unfinished ladder questions after detours, and learner-specific tracking. Committed `CLAUDE.md` still named that skill after its removal, so committed startup instructions were stale. The current local rewrite no longer relies on that skill name. [S6, S8, S11]

## What Git suggests was kept, changed or abandoned

These are local `main` commits, not inferred activity dates from prose. Most commit messages are just `eh`, so file changes carry more evidence than their titles. Two July 30 T3 checkpoint snapshots appear under `git log --all`; they are not extra commits on the seven-commit `main` history. [S1]

| Date / commit | Evidence and cautious reading |
|---|---|
| Jul 25 / `bd6cbfa` | Initial TS project plus `problems.md`: timed, target-bearing session plan. [S1–S2] |
| Jul 28 / `0b340be` | Topic attempts, second session sheet and notes/output added; starter index/greet removed. Both completed and empty attempts survived. This was the main exercise accumulation. [S1, S9] |
| Jul 31 / `f48bc8c` | Setup prompt, Claude/Pi guards, AGENTS symlink, ledger/cards/reps/goals/TODO and two DP files added. The workflow became an explicit agent-managed learning protocol. [S1, S3–S6, S10] |
| Aug 23 / `5476078` | Hermes skill and references, Codex hooks, rep update and BST code added. Strong evidence of trying multiple agent hosts, not proof of abandoning the underlying method. [S1, S11] |
| Aug 30 / `26a1ee9` | Deletes all three Hermes skill files. Clear removal of that integration; insufficient evidence to explain the user's reasons or retire Socratic derivation generally. [S11] |
| Aug 31 / `8c8add6`, `1a3f756` | Add annotated-reading/Kyoot material and extend the ledger with architecture-oriented sessions. The last commits prioritize prose/model learning over new coding exercises. [S1, S7] |
| Sep 15 / uncommitted text | Local protocol rewrite retains Derive, adds explicit Teach/Check/Rep/Interview, Google/Python goals and living memory. Claude helper files are locally deleted, but Git does not date those deletions or establish intentional retirement. [S1, S8] |

**Kept:** learner ownership, weak hints, conventions immediately, assistant-written evidence, due reps before novel material, reconstruction as the bar. **Changed:** timed/prose-heavy early sheets → lower-friction spoken/dictated work → later separate timed Interview mode; explanation prohibition → requested full teaching plus reconstruction. **Explicitly removed:** Hermes skill files. **Lapsed or incomplete:** several rep rows, routine variations, and currently disconnected re-entry hooks. Do not label the whole repository or derivation method abandoned merely because its last commit is August 31. [S1–S11]

## Comparison with the new study decisions

The authority here is [#2's resolution](https://github.com/saiashirwad/skills/issues/2#issuecomment-5911131277), read alongside map #1—not the old workspace. [S12]

| New decision | Old precedent / conflict | What to borrow (recommendation, not a new decision) |
|---|---|---|
| Open-ended map → topic issues → drill/learn/mock tickets | Old state lived in Markdown queues and files, not an issue hierarchy. [S4–S5, S8] | Transfer evidence into ticket comments and committed review notes; avoid duplicating scheduling state in a second `REPS.md`. |
| One hard original core drill explored through variants; never LeetCode | Old setup prescribed warm-up/core/stretch sets of six and contains familiar stock interview problems. Originality or provenance of every old problem cannot be established. [S2–S3, S9] | Borrow decision-centered, technique-neutral statements and targeted variants, not the old exercise catalog or batch size. |
| Reference solution hidden until done; attempts committed under `drills/<topic>/` | Old agent generally wrote no solution, permitted “just tell me,” and told the user to delete rebuild attempts. [S3, S5] | Keep learner-owned attempts; replace deletion with committed evidence. Define the answer-request/reveal transition explicitly rather than silently importing the old escape hatch. |
| Claude grades against a bar in map Notes | Old workflow resisted optimality verdicts, clocks in normal tutoring, unsolicited review and “solved alone” columns. September Interview mode already introduced a quiet timed attempt. [S3, S6, S8] | Separate supportive hints during practice from an explicit final grading step; record assistance accurately without moralizing it. The new grading decision wins. |
| Claude chooses `review: YYYY-MM-DD`; `study-due` reopens the same issue | Old fixed +3/+10/+30 intervals and manual rows, with no demonstrated due-date automation. [S5, S10] | Keep reviews first and diagnose what broke; use the new adaptive issue schedule, not the old timing table. |
| `study:learn`: teach live with primary sources, then Socratic check | Later annotated teaching/reconstruction is a close fit; old ladder-only setup conflicts if treated as universal. [S3, S7–S8] | Preserve complete reading passes and ask for reconstruction afterward, not interleaved micro-quizzes. Retain the new primary-source requirement. |
| Session: clear due reviews → one new ticket → propose 1–3 next tickets for approval | Old “reps before keystones” directly fits, but automatic sets/unstarted-file counts are not topic progress or approved next work. [S3, S10] | Borrow low-maintenance re-entry summaries and no user forms; generate them from actual ticket state. |

Two especially useful reusable details are (1) **assistant-written learner evidence with dates and stale-knowledge warnings**, and (2) **classifying misses as recognition vs execution**, so a review can target the actual failure rather than merely repeat the whole lesson. Both should stay lightweight; the historical cost was not lack of documentation, but missing repetitions. [S4–S5, S8]

## Unconfirmed / limitations

No remote fetch, external agent-session reconstruction, runtime hook validation, test execution, or inspection of ignored scratch work was performed. Local history cannot establish every session, whether flashcards were actually reviewed, whether Python mocks happened elsewhere, or why helper files were deleted. The “0% written forms / 100% dictated” claim is the ledger's own account, not audited telemetry. The hidden-reference mechanism remains unspecified by the map and is not solved by the old `src/` editing guard. [S1, S4, S8, S12]

## Primary-source index

Paths labeled **WT** mean the local working tree as inspected on 2026-09-30; these are deliberately not presented as committed remote content. To reproduce history, run `git -C ~/code/prep show <commit>:<path>`; to inspect the local changes, use `git -C ~/code/prep diff` and `git status --short`.

- **S1 — Repository metadata/history:** local `git status --short --branch`, `git remote -v`, `git log main --date=short --format='%H %ad %s'`, `git log --all --stat --oneline`, `git ls-files -s AGENTS.md CLAUDE.md`; `.gitignore` lines 1–2 and directory listings. [HEAD tree](https://github.com/saiashirwad/prep/tree/1a3f7569d78e5414838bbcb9e2f1bef679e96d23).
- **S2 — Early session sheets:** [problems.md](https://github.com/saiashirwad/prep/blob/1a3f7569d78e5414838bbcb9e2f1bef679e96d23/problems.md), especially lines 1–43; [session2.md](https://github.com/saiashirwad/prep/blob/1a3f7569d78e5414838bbcb9e2f1bef679e96d23/session2.md), lines 1–28.
- **S3 — Installer and teaching contract:** [SETUP-PROMPT.md](https://github.com/saiashirwad/prep/blob/1a3f7569d78e5414838bbcb9e2f1bef679e96d23/SETUP-PROMPT.md), lines 14–43 (interview), 82–155 (problems), 157–216 (reviews/hooks), 220–349 (tutoring).
- **S4 — Ledger:** [committed LOG.md](https://github.com/saiashirwad/prep/blob/1a3f7569d78e5414838bbcb9e2f1bef679e96d23/LOG.md); WT `/Users/texoport/code/prep/LOG.md` lines 1–100 and 249–330 (September additions at 25–29, updated standing entry at 65).
- **S5 — Review queue:** [REPS.md](https://github.com/saiashirwad/prep/blob/1a3f7569d78e5414838bbcb9e2f1bef679e96d23/REPS.md), lines 1–25.
- **S6 — Committed startup/cards:** [CLAUDE.md](https://github.com/saiashirwad/prep/blob/1a3f7569d78e5414838bbcb9e2f1bef679e96d23/CLAUDE.md); [CARDS.md](https://github.com/saiashirwad/prep/blob/1a3f7569d78e5414838bbcb9e2f1bef679e96d23/CARDS.md), especially lines 1–16.
- **S7 — Annotated reading:** [annotated-reading.md](https://github.com/saiashirwad/prep/blob/1a3f7569d78e5414838bbcb9e2f1bef679e96d23/annotated-reading.md), especially lines 7–83 and 136–144; LOG entries dated Aug 30–31 [S4]; commit `8c8add6` adds this file and `kyoot.md`.
- **S8 — September local rewrite (WT only):** `/Users/texoport/code/prep/CLAUDE.md` lines 9–97 (modes/memory), 101–140 (rules/track); `MEMORY.md` lines 1–34, 38–124; `GOALS.md` lines 1–84; `TODO.md` lines 1–25; `git diff --stat`. `MEMORY.md:6` dates the rewrite September 15 and says it was not a study session.
- **S9 — Contrasting actual problems:** [palindrome](https://github.com/saiashirwad/prep/blob/1a3f7569d78e5414838bbcb9e2f1bef679e96d23/src/2/01-palindromeignoringpunctuation.ts), lines 9–18; [stairs](https://github.com/saiashirwad/prep/blob/1a3f7569d78e5414838bbcb9e2f1bef679e96d23/src/dp/01-waystoclimbstairs.ts), lines 13–43.
- **S10 — Tool source:** [package.json](https://github.com/saiashirwad/prep/blob/1a3f7569d78e5414838bbcb9e2f1bef679e96d23/package.json); [.claude/session-start.sh](https://github.com/saiashirwad/prep/blob/1a3f7569d78e5414838bbcb9e2f1bef679e96d23/.claude/session-start.sh); [.pi/extensions/prep.ts](https://github.com/saiashirwad/prep/blob/1a3f7569d78e5414838bbcb9e2f1bef679e96d23/.pi/extensions/prep.ts), lines 18–38, 40–84; [.codex/hooks.json](https://github.com/saiashirwad/prep/blob/1a3f7569d78e5414838bbcb9e2f1bef679e96d23/.codex/hooks.json).
- **S11 — Removed Hermes integration:** [skill at addition commit](https://github.com/saiashirwad/prep/blob/5476078b4426dde4b370d330f7857066765758d6/.hermes/skills/derive-dont-explain/SKILL.md); [removal commit](https://github.com/saiashirwad/prep/commit/26a1ee94f47b02318db2b0da119313bf0a87d1e1). Verified with `git show 5476078:.hermes/skills/derive-dont-explain/SKILL.md` and history stats.
- **S12 — Current decisions:** [map #1](https://github.com/saiashirwad/skills/issues/1), Destination/Notes/Decisions/Not yet specified; [study #2 resolution](https://github.com/saiashirwad/skills/issues/2#issuecomment-5911131277), retrieved via `gh issue view` before comparison.
