---
name: research
description: Investigate a question against primary sources and write cited findings to one Markdown file. Use when a decision needs facts from docs, APIs or source code.
---

Claude doesn't research; it hands the question off with the `delegate` skill (Research brief). The OpenCode session doing it:

1. Uses primary sources (official docs, source code, specs, first-party APIs) and traces every claim to the source that owns it.
2. Writes one Markdown file that cites each claim and says what it couldn't confirm.
3. Saves it where the brief says, otherwise `docs/research/<slug>.md`.
