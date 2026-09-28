---
name: handoff
description: Compact the current conversation into a handoff document for another agent to pick up. Use only when explicitly invoked.
disable-model-invocation: true
metadata:
  opencode/autoinvoke: false
---

Write a handoff document summarising the current conversation so a fresh agent can continue the work. Save to the temporary directory of the user's OS - not the current workspace. If the user passed arguments, treat them as a description of what the next session will focus on and tailor the doc accordingly.
