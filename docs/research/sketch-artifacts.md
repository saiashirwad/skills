# Cheap, co-editable artifacts for hands-on sketch tickets

Resolves [ticket #13](https://github.com/saiashirwad/skills/issues/13) in [map #1](https://github.com/saiashirwad/skills/issues/1). Researched 2026-09-30 from primary documentation. Recommendations below are synthesis, not measured usability results.

## Answer

Use **one executable model plus examples**, **one small Mermaid view when relationships need explaining**, and **a short Markdown decision record only for a consequential choice**. Choose the model in the target project's existing language/toolchain: TypeScript types for internal shapes, Zod or Effect Schema for runtime boundaries, SQL DDL for relational persistence. Do not require every sketch to produce all of these.

This fits the map's hands-on design goal: the user can change a field, constraint, example, or transition themselves; Claude can run a tight check and discuss its consequences. Keep the GitHub ticket as the question and conversation, repository files as the editable evidence, and the map as a pointer to the result—not three copies of the design.

## Capability and cost comparison

“Renders” distinguishes a visual diagram or formatted prose from merely displaying source. GitHub displays code; that does not mean GitHub executes its checks. Its documented native diagram formats include Mermaid, but not D2. [1]

| Artifact | Best question to answer together | GitHub presentation | Checkable evidence | Cost / limitation |
| --- | --- | --- | --- | --- |
| TypeScript types/interfaces + example values | What entities, variants, inputs and outputs exist? | Source or fenced code, not a model diagram | `tsc --noEmit --strict` checks assignability and use of the model without emitting JS. [2][3] | Lowest incremental cost in a TS repo. Types are erased; no validation of untrusted runtime data. [2] |
| Zod schema + valid/invalid fixtures | Which payloads should the boundary accept or reject? | TS source or fenced code | Type-check consumers; run `.parse` / `.safeParse` against fixtures; derive types with `z.infer`. [4] | Adds a library if absent. A schema definition alone does not run validation. Input/output types may differ after transformations. [4] |
| Effect Schema + fixtures | How do encoded data, decoded domain values and validation requirements relate? | TS source or fenced code | Type-check inferred types; execute decoding/encoding; optionally derive test arbitraries and JSON Schema. [5] | Prefer where Effect already exists. Its `Type`, `Encoded`, and `Requirements` concepts add material to discuss; pin the project's major version. [5] |
| SQL DDL + insertion/deletion scenarios | What identity, cardinality, uniqueness, nullability and deletion policy does storage enforce? | SQL source or fenced code, not an ER diagram | Apply to an isolated database of the target engine/version, then exercise success and expected-failure cases. PostgreSQL enforces declared constraints when data is written. [6] | Requires a database harness; SQL dialect semantics matter. Creating tables alone does not test the intended invariant. |
| Mermaid in Markdown | How do components communicate or entities relate? | **Native diagram** in Markdown files, issues, PRs, discussions and wikis. [1] | Render with Mermaid CLI; it also transforms Markdown Mermaid blocks into linked SVGs. [7] | Lowest publishing overhead on GitHub. Successful rendering does not establish correctness of architecture or code conformance. |
| D2 source + generated image | Would a richer, separately rendered architecture view make this clearer? | No native D2 renderer documented; embed generated SVG/PNG instead. [1][8] | Compile/render with D2; `--watch` gives a live-reloading local preview. Parser and formatter support are documented. [8] | Extra CLI and generated-output maintenance. Good opt-in, not the default solely for GitHub discussion. |
| Markdown ADR | Why this choice rather than the alternative, and what does it cost? | Formatted prose; Nygard explicitly describes GitHub Markdown rendering. [9] | Human review of reasoning; optionally lint structure/links. No type checker proves a prose decision correct. | Cheap if limited to one significant decision: context, decision, status, consequences. Preserve superseded decisions. [9] |

## Selection rules

These are proposed defaults for a future `sketch` workflow, not changes implemented by this research.

1. **Start from the disputed question, not a document checklist.** If names and states are unsettled, use a small typed model with concrete examples. If the project is not TypeScript, use its native types rather than introducing TS just to sketch.
2. **Stay in the existing stack.** Plain types are enough for internal compile-time contracts. Use the project's existing Zod or Effect Schema for external input/output. Do not introduce both to describe the same boundary. Infer domain types from runtime schemas rather than manually maintaining matching interfaces. Zod and Effect both expose type extraction. [4][5]
3. **Use the database to settle database rules.** Add DDL when uniqueness, optional relationships, referential integrity, or delete behavior is the question. A TS `string` ID or an arrow in an ER diagram cannot substitute for a database foreign key. PostgreSQL documents the actual constraint behavior. [6]
4. **Use Mermaid first for shared GitHub views.** Keep diagram labels tied to actual model/component names. Use D2 only when its local authoring/layout workflow earns the extra render step. GitHub's Mermaid version can lag a local installation: its docs show an `info` diagram for checking the deployed version. [1][8]
5. **Record rationale only when it matters.** Keep a choice proposed until the user agrees; then capture one significant decision and its trade-offs. Nygard's format explicitly supports proposed, accepted and superseded statuses. [9]
6. **Do not create a shadow implementation.** Promote accepted types/schemas into the production location or explicitly label and later remove the disposable sketch. Derive views where cheap; otherwise designate the authoritative artifact and check the small diagram manually after edits.

## A small hands-on loop

Recommended session structure:

1. Put one question and two competing examples in the ticket: e.g. “Can an order exist without a customer?”
2. Link a small editable source file and its check command. The user can write the variant or constraint; Claude can prepare fixtures or run the check. User authorship is optional, not a homework gate.
3. Run the check after each meaningful edit. Add a valid example, an invalid example and a boundary case. Distinguish “this parsed/compiled” from “this rule matches what we want.”
4. For a behavioral dispute, add a tiny function or test: a union of states does not alone enforce legal transitions between them. For a persistence dispute, exercise writes/deletes against the target DB. For a topology dispute, walk one request and one failure path through a diagram.
5. End with the chosen artifact, the observed check result, what remains unproven, and any agreed decision. Split implementation or operational validation into follow-up tickets rather than pretending the sketch proves them.

### Illustrative minimal TypeScript sketch

```ts
type Order =
  | { state: "draft"; customerId: string | null }
  | { state: "submitted"; customerId: string };

const draft: Order = { state: "draft", customerId: null };
const submitted: Order = { state: "submitted", customerId: "customer-1" };

// @ts-expect-error A submitted order requires a customer.
const invalid: Order = { state: "submitted", customerId: null };
```

Suggested check in a TypeScript-equipped project: `tsc --noEmit --strict sketch.ts`. The union makes the design question tangible, but runtime JSON still needs validation and transitions still need behavior tests. Static checking and type erasure are documented in the TypeScript handbook. [2][3] This snippet is illustrative and was not executed during this research.

For a Zod variant, have the user edit the schema and keep explicit test assertions that the good fixture succeeds and the bad fixture fails through `safeParse`. Derive `Order` with `z.infer`; do not duplicate its fields in a handwritten interface. [4] For an Effect variant, likewise distinguish encoded and decoded fixtures and test any chosen round-trip property. Effect documents the encode/decode distinction and round-trip rule. [5]

### SQL pitfalls worth making visible during sketching

PostgreSQL's documentation gives several productive counterexamples: [6]

- `CHECK (price > 0)` does **not** forbid null; add `NOT NULL` if required.
- A nullable foreign-key column can avoid the relationship check; decide whether absence is meaningful.
- Ordinary unique constraints permit multiple nulls by default; null treatment is not portable across engines.
- `ON DELETE CASCADE`, `RESTRICT` and `NO ACTION` encode different policies; ask what should happen to the dependent object.
- Cross-row invariants cannot generally be enforced by a row `CHECK`; use suitable database constraints or explicitly designed transactional behavior.

Run these scenarios only in a disposable database, never against user production data. Tests must assert expected failures rather than accepting any SQL error as success.

### Diagram validation recipes

With the relevant tools already installed and version-pinned:

- Mermaid source: `mmdc -i sketch.mmd -o sketch.svg`. For a Markdown source containing Mermaid blocks, the CLI also documents Markdown-to-Markdown transformation with generated images; write to a separate output path rather than overwriting the source. [7]
- D2 source: `d2 --watch sketch.d2 sketch.svg` for local co-editing preview. Commit or publish the generated image alongside its source when GitHub readers need to see it, and regenerate after edits. [8]

These establish renderability, not that deployed services match the diagram. Keep the render command in the ticket or repository script if the artifact will survive the session.

## Confidence and unconfirmed points

- This is documentation research, not a benchmark or usability study. “Cheap” means few new tools, small text edits, and a short feedback loop; actual co-editing speed was not measured.
- No compiler, schema tests, database instance, or diagram renderer was installed or executed for this ticket. Commands are documented/proposed recipes, not reported test passes.
- GitHub's exact deployed Mermaid version was not checked. Use its documented `info` block and preview before relying on newer syntax. [1]
- D2's lack of native GitHub rendering is inferred from GitHub's documented supported formats, not an exhaustive test of every GitHub surface or extension. [1]
- Effect's fetched introduction resolves to **v3** documentation and shows v4 as release candidate; use the target repository's pinned major, not copied API examples from a different major. [5]
- Tooling can check shapes, encoded constraints and rendering. Domain correctness, concurrency safety, migration safety, performance and architectural suitability require additional tests or human judgment; none is established by this research.

## Primary sources

All accessed 2026-09-30; web documentation and default-branch READMEs may change.

1. GitHub Docs, [Creating diagrams](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams): supported formats/surfaces, Mermaid fences, deployed-version check.
2. TypeScript Handbook, [The Basics](https://www.typescriptlang.org/docs/handbook/2/basic-types.html): static checks, compiler, strictness, erased types.
3. TypeScript TSConfig, [noEmit](https://www.typescriptlang.org/tsconfig/noEmit.html): type-check without output files.
4. Zod, [Basic usage](https://zod.dev/basics): schemas, parse/safeParse, asynchronous variants, inferred input/output types.
5. Effect, [Introduction to Effect Schema (v3)](https://effect.website/docs/v3/schema/introduction): schema parameters, requirements, decoding/encoding, derived operations, type extraction and round-trip rule.
6. PostgreSQL 18, [Constraints](https://www.postgresql.org/docs/18/ddl-constraints.html): checks, nullability, uniqueness, keys, referential actions and caveats.
7. Mermaid project, [mermaid-cli README](https://github.com/mermaid-js/mermaid-cli/blob/master/README.md): rendering commands, output formats and Markdown transformation.
8. D2 project, [README](https://github.com/d2lang/d2/blob/master/README.md): text syntax, watch preview, export formats, parser/formatter and tooling.
9. Michael Nygard, [Documenting Architecture Decisions](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions): original lightweight ADR format, scope and lifecycle.
