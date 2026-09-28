---
name: zoom-out
description: Tell the agent to zoom out and give broader context or a higher-level
  perspective on a section of code you're unfamiliar with. Use only when explicitly invoked by the user.
disable-model-invocation: true
---

Produce a map of this area of the codebase — an orienting overview of how the
code you're unfamiliar with fits into the bigger picture. Keep it short enough
to read in one pass.

1. Find the entry points — the public APIs, exports, command handlers, or
   endpoints that lead into this area.
   Done when: you can name every way in, and each name comes from having read
   the code, not from guessing.

2. Trace modules and callers. Open each module you intend to mention and find
   who calls it and what it depends on.
   Done when: every module on the map has been opened, and you can state its
   callers and dependencies from evidence.

3. Mark the boundaries — which layer each piece belongs to and where its
   ownership lives.
   Done when: every module on the map is assigned to a layer, and you can say
   who owns it.

4. Present the map: a one-paragraph overview, then the call graph and data
   flow. Use the project's own vocabulary; if no glossary exists, say so in
   one line and use plain naming.
   Done when: a reader unfamiliar with the code can say who calls what and who
   owns it, without asking a follow-up.
