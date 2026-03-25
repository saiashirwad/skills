---
name: refactor-radar
description: Scans the codebase using parallel subagents to identify files that are prime candidates for a specific refactoring pattern or skill. Use when asked to "find where we can apply X skill", "scan for X pattern", or "find refactoring targets".
---

# Guide: Refactor Radar (Skill Applicability Scanner)

This skill scans a codebase to find files that perfectly match the "Anti-Pattern" of a target skill, proposing how that specific skill could fix them.

## Execution Strategy

Follow these exact steps:

### 1. Analyze the Target Skill

Use the `read` tool to load the target skill's `SKILL.md` file (e.g., `effect-policy-extraction`).
Extract the following into your context:

- **The Anti-Pattern (What to look for):** Code smells, specific imports, or mixed logic.
- **Exclusion Criteria (When NOT to apply):** Explicit warnings in the skill about when to avoid the pattern (e.g., "fewer than 2 branching outcomes").
- **Target State (What it becomes):** The desired architectural components.

### 2. Smart Pre-Filtering (The Hunting Ground)

Do not pass every file in the codebase to subagents. Use `bash` (`rg` or `find`) to identify candidate files based on keywords related to the Anti-Pattern (e.g., `rg -l "Effect.gen" src/`). Filter out tests, configs, and files that already match the target state.

### 3. Determine Subagent JSON Schema

Based on the target skill's architecture, invent 2 custom JSON keys the subagents must output to prove they understand the required refactor.
_(Example for Effect Policy: `proposed_adt` and `io_split`. Example for a UI skill: `proposed_component_split` and `css_state`)_.

### 4. Spawn Parallel Subagents

Chunk the surviving candidate files into groups of 3 to 5. Call the `subagent` tool concurrently for each chunk to maximize speed and isolate context. Pass this exact, dynamically-filled instruction to each subagent:

> "Read the following files: [INSERT_FILE_PATHS].
> Evaluate if they are prime candidates for the '[INSERT SKILL NAME]' refactoring pattern.
>
> **The Anti-Pattern (What to look for):**
> [INSERT EXTRACTED ANTI-PATTERN]
>
> **Exclusion Criteria (What to ignore):**
> [INSERT EXTRACTED EXCLUSION CRITERIA]
>
> If a file is a strong candidate, output a JSON object containing:
>
> 1. `file_path`
> 2. `anti_pattern_evidence`: Quote or describe the specific logic that violates the pattern.
> 3. `[INSERT CUSTOM JSON KEY 1]`: [DESCRIPTION]
> 4. `[INSERT CUSTOM JSON KEY 2]`: [DESCRIPTION]
>
> Ignore files that hit the exclusion criteria or do not strongly exhibit the anti-pattern."

### 5. Synthesize and Report

Collect the JSON outputs from all subagents. Present a final, prioritized markdown report detailing the top 3 to 5 best candidates for this exact refactoring, including the proposed architecture sketches for each.
