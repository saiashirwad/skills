# Skills

A collection of agent skills installable via the [`skills`](https://github.com/vercel-labs/skills) CLI.

## Available Skills

### [effect-policy-extraction](./effect-policy-extraction/SKILL.md)

Refactor complex Effect-based orchestrators and workers into the "Functional Core, Imperative Shell" pattern using pure policy ADTs. Separates business logic from I/O, making domain logic 100% unit-testable without mocking.

### [refactor-radar](./refactor-radar/SKILL.md)

Scans the codebase using parallel subagents to identify files that are prime candidates for a specific refactoring pattern or skill.

## Installation

```bash
npx skills add saiashirwad/skills
```

Or install a specific skill:

```bash
npx skills add saiashirwad/skills --skill effect-policy-extraction
```
