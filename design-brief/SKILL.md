---
name: design-brief
description: Write a scoped design brief before building or reshaping a web UI. Use when a visual direction needs turning into an implementation brief; use prototype for throwaway variants.
license: Apache-2.0; see LICENSE.txt
---

# Design brief

Claude reads the map/ticket and [reference.md](reference.md), then writes a self-contained brief: fixed constraints first, the open question and allowed variation, real content/assets (mark missing items), and required proof. The brief beats generic taste; do not reopen settled brand choices or invent product claims.

Review the plan against the brief, then use `delegate` to have OpenCode build it in a Rift. Use `prototype` for experiments rather than create another prototype workflow. Workers return evidence and unresolved choices, not decisions on the user's behalf.

Require a run command, URLs, known defects, and inspected full-page captures via `python3 <skill-dir>/scripts/capture.py --help` (project Python with Playwright and Chromium installed). Show actual previews before visual choices; production work still needs the user's request.
