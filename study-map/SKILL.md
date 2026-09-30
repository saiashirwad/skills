---
name: study-map
description: Study a subject as an open-ended map of drill, learn and mock tickets on a study repo's GitHub issues, with Claude-graded attempts and scheduled reviews. Use when the user wants to start or continue a study map.
disable-model-invocation: true
---

Study runs as a **map** on the study repo's GitHub issues: map → topic issues → tickets, as nested sub-issues. The map is an open-ended epic ("Crack Google DSA interview"). It starts vague and grows with the user's progress. Depth beats count: one hard problem explored fully is worth more than five skimmed. The user solves; Claude never writes the user's attempt.

In anything the user reads, refer to an issue by its linked title, never a bare number. Scripts are in `~/.agents/skills/study-map/scripts/` and default to the current repo; `scripts/x` below means that folder.

## The map

Labelled `study:map`; topics are sub-issues labelled `study:topic`, tickets hang under topics.

```markdown
## Goal
<the epic, one line>

## Notes
<language, pass bar (e.g. unaided, optimal, ≤25 min per medium), standing preferences>

## Not yet specified
<topics the user wants but that aren't sharp enough to ticket>
```

## Tickets

Labelled `study:<type>`:

- **drill** (the default): one hard original problem plus its related variants, explored until the user owns the pattern. Never LeetCode or links to problem sites. Files live in `drills/<topic>/<slug>/`: `problem.md`, public tests, the user's attempts (committed, never deleted) and Claude's `review.md`.
- **learn**: only when the user asks to be taught. Teach one coherent piece live (500–1000 words, citing primary sources). Don't quiz mid-reading. Answer the user's questions as one second pass, then the user reconstructs it without notes and Claude points at the hole.
- **mock**: a timed interview with Claude as interviewer. Ask whether the problem is familiar. Freeze the question and its rubric first. Grade framing, reasoning, implementation, validation and communication as poor / borderline / solid / outstanding, citing what was said and written. Call it Google-informed practice, never a hiring prediction.

**Help during an attempt:** weakest hint first; a small counterexample instead of a correction. Hand over syntax, stdlib and vocabulary freely. "Just tell me" gets a clean answer, recorded as help.

## Writing a drill

Delegate it (`delegate` skill, `--rift drill/<slug>`) so the answer never shows in this session: "Write an original drill for <pattern> at <level> in <language> under `drills/<topic>/<slug>/`: `problem.md`, public tests that import only the learner's file, and an empty typed stub. Write a reference solution with explanation outside the repo, make it pass the tests, then `~/.agents/skills/study-map/scripts/seal <drill-dir> <reference-dir>` and delete the plaintext. Use neutral filenames. Commit only public files and `reference.tar.age`. Report readiness and test status, never the approach." Merge it without a verifier.

## A session

1. `scripts/due` lists reviews; clear the DUE ones first (`gh issue reopen`). A review is a cold attempt at a fresh variant of the same pattern, not a reread. A revealed answer can't be unseen.
2. Take the named ticket, or the first from `scripts/frontier <map>`, and claim it (`gh issue edit <n> --add-assignee @me`).
3. When the user submits or gives up, `scripts/reveal <drill-dir>` and compare reasoning, not source text. Grade against the pass bar and classify each miss: **recognition** (didn't see the approach) or **execution** (saw it, couldn't build it).
4. Close with a comment: verdict and why, help given, the miss types, and a line `review: YYYY-MM-DD`. Pick the date by judgement along 1/3/7/14/30/60 days: move up a rung on a clean pass, stay or drop on a shaky one, restart on a fail.
5. Propose 1–3 next tickets from what was missed or what's adjacent. Create only what the user approves, as sub-issues of the right topic. The user may also add topics.

## Start a map

Use `grilling` for the goal, language, pass bar and first topics. Create the map, the topics and one or two first tickets.
