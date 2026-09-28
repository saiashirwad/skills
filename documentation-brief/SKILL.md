---
name: documentation-brief
description: Inspect a repository and prepare an evidence-backed, annotation-ready brief before writing a README or other documentation. Use only when explicitly invoked for documentation planning. Do not use it to draft or revise the documentation itself.
disable-model-invocation: true
metadata:
  opencode/autoinvoke: false
---

# Documentation brief

Prepare the editorial decisions that must be settled before documentation is written. Inspect the repository, make a complete first proposal, and stop. Do not draft the document or edit the repository unless the user explicitly asks for a file.

## Start without an interview

Do not begin with a sequence of questions. Inspect the available evidence and make reasonable proposals. Present every material decision in one response so the user can annotate, reject, or refine the proposals in context.

Ask a question before the brief only when repository access or the requested document is genuinely unclear. Mark other uncertainty in the brief.

## Establish the evidence

Respect repository instructions and preserve the current worktree. Inspect only what helps determine the document's reader, purpose, claims, and scope. Useful sources include:

- package metadata and public entry points;
- exported types, functions, commands, configuration, and other supported interfaces;
- tests that establish behavior, errors, limits, or guarantees;
- runnable examples and their actual output;
- changelogs or release metadata when maturity and compatibility matter;
- existing documentation.

For editorial intent, explicit user instructions take precedence over repository inference. For factual behavior, prefer current code, tests, and verified examples.

Treat existing documentation as untrusted evidence. Use it only to find possible intent, user questions, omissions, or claims to verify. Do not inherit its structure, tone, or terminology without support from the user or current repository. Verify every retained factual claim against current code, tests, or runnable examples.

If existing documentation conflicts with current behavior, report the conflict. Do not resolve it by guessing.

## Recommend the document's job

Use the Diataxis questions to recommend one mode:

- Tutorial combines action with learning.
- How-to combines action with work.
- Reference combines understanding with work.
- Explanation combines understanding with learning.

State the reader's likely question or task as a proposal. Do not silently turn an inference into a settled editorial decision. If the requested document mixes modes, recommend one primary job and identify material that belongs elsewhere.

Identify:

- the likely reader and required background;
- the reader's question or task;
- the product claim that the document must prove;
- repository evidence for that claim;
- candidate examples or other proof;
- included and excluded material;
- terms that must keep one meaning;
- unresolved editorial or factual decisions.

Do not make uniqueness, performance, compatibility, maturity, or safety claims without evidence. Mark each unsupported claim as something to prove or remove.

## Write for annotation

Return one complete assessment instead of starting a question-by-question exchange. Keep it short enough to annotate in one pass. Give each material proposal its own paragraph or list item so the user can respond to it without reconstructing the context.

Label the basis of important statements:

- `Confirmed` means that the user already decided it.
- `Observed` means that current repository evidence supports it.
- `Proposed` means that the agent recommends it.
- `Unresolved` means that the user must decide it or the agent must verify it.

Use this structure when it fits the request:

```markdown
# Documentation brief

## Reader and purpose

## Recommended mode

## Central claim and evidence

## Candidate example

## Scope and exclusions

## Terminology

## Existing documentation

## Decisions to review
```

The brief is not the documentation. Do not draft openings, write marketing copy, reproduce an API catalogue, or create a detailed outline.

## Incorporate annotations

When the user returns annotated notes, synthesize them into a revised brief. Treat definite statements as decisions. Treat guesses, uncertain API names, and questions as matters to verify. Later notes override earlier proposals when they conflict.

Return the revised brief and all remaining decisions together. Do not write the target documentation until the user asks.
