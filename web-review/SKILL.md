---
name: web-review
description: Audit web UI code and rendered behavior against pinned accessibility, interaction, performance, and copy rules. Use for a read-only web interface review, not a redesign or implementation request.
license: MIT; see LICENSE.txt
---

# Web review

Use the `delegate` skill with `--model design` for a read-only audit with the target files/URLs, brief constraints, and [reference.md](reference.md). Do not fix files, install dependencies, or add framework libraries during the audit.

Report each finding as `file:line | rule | evidence | likely impact | proposed fix`, grouped by file and ordered by impact. Distinguish observed behavior from source inference; use browser evidence for keyboard focus, reduced motion, and other behavior source alone cannot prove. Include reproduction steps and capture paths, or mark the check untested. Never infer accessibility compliance from screenshots.

Use sentence case, straight quotes, and complete short sentences in both copy recommendations and the report. These override the upstream title-case, curly-quote, and grammar-sacrificing rules. Apply framework-specific guidance only where relevant: native buttons already support keyboards; Astro/HTML does not need React handlers or URL-state libraries.

Claude synthesizes the findings and returns proposed fixes to the user; an audit is not permission to implement them.
