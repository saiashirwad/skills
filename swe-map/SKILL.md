---
name: swe-map
description: Plan software work too big for one session as a map of decision tickets on GitHub issues, resolving one ticket per session until the way to the destination is clear.
disable-model-invocation: true
---

A loose idea has arrived, too big for one session, and the way to its **destination** isn't visible yet. swe-map charts that way as a **map** on the repo's GitHub issues, then resolves its **tickets** (questions whose answer is a decision) one per session. It plans; it doesn't build. When you feel the pull to just do the work, you've reached the edge of the map, so hand off. A map's Notes may override this.

In anything the user reads, refer to an issue by its linked title, never a bare number.

## The map

A GitHub issue labelled `swe:map`, with tickets as its sub-issues. It's an index: each decision lives only in its ticket, and open tickets aren't listed (query them).

```markdown
## Destination
<what done looks like: a spec, a locked decision, or a change. One or two lines.>

## Notes
<domain; skills every session should use; standing preferences>

## Decisions so far
- [<closed ticket title>](url): <one-line gist>

## Not yet specified
<fog: in-scope questions not yet sharp enough to ticket>

## Out of scope
- [<closed ticket title>](url): <gist, and why it's out>
```

## Tickets

A sub-issue whose body is `## Question` plus what it needs, sized to one session and labelled `swe:<type>`:

- **research** (AFK): facts from outside the repo. Delegate it with the brief below.
- **prototype** (HITL): a cheap artifact to react to, when the question is how something should look or behave. Delegate the build (`prototype` skill), then settle it with the user.
- **grilling** (HITL, the default): a conversation using `grilling` and `domain-modeling`. Never answer the user's side yourself.
- **task**: work that must happen before a decision (sign up, provision, move data). Delegate what an agent can do alone; give the user a checklist for the rest.

A ticket's **frontier** is open, unblocked and unassigned; `~/.agents/skills/swe-map/scripts/frontier <map>` lists it. Ticket or fog? Ticket it if you can state the question sharply now, even if it's blocked; otherwise it stays in Not yet specified. Work past the destination is out of scope: close its ticket and add a line under Out of scope. It never returns to this map.

With `R=repos/{owner}/{repo}` and `id(n)` = `gh api $R/issues/<n> --jq .id`:

- Claim: `gh issue edit <n> --add-assignee @me`, before any work.
- Add to map: `gh api $R/issues/<map>/sub_issues -F sub_issue_id=<id(n)>`
- Block: `gh api $R/issues/<n>/dependencies/blocked_by -F issue_id=<id(blocker)>`

## Chart a map (the user brings an idea)

1. Pin the destination with `grilling` and `domain-modeling`.
2. Grill breadth-first for the open decisions. If there's no fog, you don't need a map; ask the user how to proceed.
3. Create the map, then the tickets you can state, then wire blocking in a second pass.
4. Delegate every research ticket, then stop. Charting resolves nothing.

## Work the map (the user brings a map)

1. Read the map body, not every ticket.
2. Take the named ticket, or the first on the frontier, and claim it.
3. Resolve it, zooming into related tickets as needed and using the skills Notes names.
4. Record the answer as a resolution comment, close the ticket, and add one line to Decisions so far.
5. Create and wire tickets that are now sharp, clear the fog they came from, close anything now out of scope, and fix tickets the decision invalidated.

Resolve one ticket per session; research tickets may fan out. Other sessions may be editing the map at the same time.

## Research brief

`--rift research/<slug>`: "Resolve ticket <url> of map <url> using `gh`. Claim it, research it per the `research` skill, commit findings to `docs/research/<slug>.md` and push the branch, comment a summary linking the file, close the ticket, and end your report with `- [<title>](<url>): <gist>`; don't edit the map." When it's done, confirm the ticket is closed, then add that line to Decisions so far yourself (parallel jobs editing the map body overwrite each other).
