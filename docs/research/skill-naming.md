# Skill naming and discovery: Claude Code and OpenCode V2

Research for [ticket #14](https://github.com/saiashirwad/skills/issues/14), in [the swe/study map](https://github.com/saiashirwad/skills/issues/1). Checked 2026-09-30 against current official documentation; OpenCode findings are **V2**, not V1.

## Decision summary

Use unique lowercase kebab-case directory names, with identical frontmatter `name`: `swe-…` and `study-…` only for activity-specific skills; shared skills stay unprefixed. Keep canonical files in `~/.agents/skills` and expose individual skill directories through `~/.claude/skills` symlinks. Rename directories **and** names, symlinks, invocation references, and path references together. OpenCode V2 derives identity from the path, not frontmatter. Claude plugin namespacing prevents a direct full-name collision with `engineering`, but not overlapping model-trigger descriptions. These recommendations follow the discovery/name rules below and the map's agreed family policy. [1][2][3][4]

## 1. Names: portable convention versus runtime behavior

| Question | Claude Code | OpenCode V2 |
| --- | --- | --- |
| What identifies a skill? | Directory name by default; frontmatter `name` sets the displayed/typed command unless already occupied. The directory name also invokes it. Plugin names retain the plugin prefix. | **Path-derived ID**. `<source>/swe-design/SKILL.md` has ID `swe-design`; frontmatter `name` is merely a display label. |
| Nested folders create namespaces? | Nested project skill directories can receive directory-qualified commands when names clash, e.g. `/apps/web:deploy`. | No: `<source>/teams/release/SKILL.md` still has ID `release`, not `teams/release`. |
| Enforcement to rely on? | Current Code docs make frontmatter optional; don't confuse permissive Code loading with portable packaging validation. Reserved local names include `synced` (case-insensitive folder name) and `anthropic-skills`/`anthropic-skills:…`. | IDs are exact and case-sensitive. V2 does not currently enforce the recommended name pattern, length, directory/name match, or description maximum. |

Sources: Claude Code name/frontmatter/reserved-name sections [2]; OpenCode IDs/frontmatter [1].

**Repository convention:** use ASCII `^[a-z0-9]+(-[a-z0-9]+)*$`, 1–64 characters, and make `name` equal the parent directory. Include a nonempty description of at most 1,024 characters. These satisfy the Agent Skills standard (no leading/trailing/consecutive hyphens, matching directory/name) and OpenCode's portability recommendation. Prefixes are an ordinary naming convention, not special syntax or isolated namespaces. [1][3]

For example:

```text
~/.agents/skills/swe-design/SKILL.md
```

```yaml
---
name: swe-design
description: Work with the user on data models and architecture for a software-building GitHub issue map. Use for its design tickets, not study exercises or a general architecture review.
---
```

This is an illustrative description, not a decision to create that particular skill.

## 2. Discovery and duplicate precedence

### Claude Code

Documented filesystem locations are personal `~/.claude/skills/<name>/SKILL.md`, project `.claude/skills/<name>/SKILL.md`, enterprise skills under the managed settings directory, and enabled plugin `skills/` directories. **The official discovery table does not list `~/.agents/skills` or project `.agents/skills`**; use the `.claude` symlink exposure rather than assuming direct discovery. Individual skill-folder symlinks are supported, and multiple links to the same target load it once. [2, “Choose where skills load”]

Project discovery runs from the starting directory upward to the repository root. Skills below the starting directory load when Claude first reads/edits files there (or via `/add-dir`); linked worktrees stop at their own root, with a documented main-checkout fallback in recent versions. `--add-dir`/`/add-dir` also load the added directory's `.claude/skills`; a filesystem permission alone does not. [2, “Load skills in monorepos and subdirectories”, “Load skills from a directory outside the project”]

For equal local directory/file names: **enterprise > personal > project**. A skill beats an old `.claude/commands` file. Project-root and nested skills can coexist using qualified commands; plugin skills coexist because of their plugin prefix. Thus do not assume a project skill overrides a personal skill in Claude Code. [2, “Resolve skills that share a name”]

### OpenCode V2

Automatic global roots: `~/.config/opencode/skills`, `~/.claude/skills`, `~/.agents/skills`. Automatic project roots: `.opencode/skills`, `.claude/skills`, `.agents/skills`, searched from the current directory through the project root. A source accepts root-level `*.md` or files named exactly `SKILL.md` at any depth. Extra directories and HTTP catalogs can be added via the `skills` configuration array; relative configured paths resolve from the active working directory, not the config file. [1, “Discovery”, “Sources”]

Equal IDs use **last registered source wins**, in this low-to-high order: [1, “Precedence”]

1. Built-ins.
2. `.claude/skills`: global, then farthest project ancestor toward current directory.
3. `.agents/skills`: global, then farthest project ancestor toward current directory.
4. `~/.config/opencode/skills`.
5. Project `.opencode/skills`: project root toward current directory.
6. Explicit `skills` config entries in config priority and array order.

The same skill exposed under both `.claude` and `.agents` is therefore not two independent names: its equal ID resolves to the later source. Avoid divergent copies and deliberate same-ID overrides across these two tools, whose precedence differs. [1][2]

### Local installation observation

Read-only filesystem inspection on 2026-09-30 found that `~/.claude/skills` is a real directory containing **individual absolute symlinks**, not one symlink of the entire directory. For example, `~/.claude/skills/wayfinder -> /Users/texoport/.agents/skills/wayfinder`; `delegate`, `research`, and other repo skills follow the same layout. A `synced` directory is also present. This is machine-local evidence, not a claim about default installation behavior. Reproduce with `ls -ld ~/.claude/skills ~/.agents/skills` and `ls -l ~/.claude/skills`.

**Rename implication:** moving only `wayfinder/` in this repo leaves that existing absolute symlink pointing at a missing path. Update the link name and target when deploying a rename; editing an isolated Rift alone does not change the installed canonical directory. This follows directly from the observed symlink target.

## 3. Plugins and the installed engineering overlap

Claude Code plugins namespace skills as `/plugin-name:skill-name`, so `/engineering:architecture` and a local `/swe-design` can coexist. Current docs also permit a plugin skill's bare name when no other command occupies it; use the **fully qualified** name when targeting a plugin. Frontmatter can change the last segment, not remove the plugin prefix. [2, “How a skill gets its command name”][4]

Local primary-source inspection found an `engineering` plugin manifest declaring version `1.2.0` and author `Anthropic`, at `~/.claude/plugins/synced/<account-specific-directory>/engineering/.claude-plugin/plugin.json`. Its `skills/architecture/SKILL.md` has `name: architecture` and describes ADRs, technology choices, design proposal review, and component design; `skills/system-design/SKILL.md` has `name: system-design` and triggers on architecture, APIs, data modeling, and service boundaries. These files establish disk content, **not that a particular session enabled or loaded it**. Reproduce by locating `engineering/.claude-plugin/plugin.json` and reading those two skill frontmatters.

Therefore prefixing local skills prevents ambiguous explicit names, but descriptions must still separate the local **map-guided, hands-on design workflow** from the plugin's broad architecture advice. Namespace isolation is not semantic trigger isolation: both products present descriptions to the model. [1][2][4; inference]

Do not transfer Claude's namespace behavior to OpenCode. V2's plugin API registers skills with explicit IDs (its example registers `review`), and supports updating/removing those entries. The official V2 skill discovery page does not list `~/.claude/plugins`, and the plugin guide does not promise automatic Claude-plugin import or a `plugin:skill` namespace. If someone exposes an engineering plugin's `skills/` directory as an explicit OpenCode source, ordinary path-derived IDs such as `architecture` will apply. [1][5]

## 4. Descriptions and automatic selection

- **Both tools:** metadata tells the model what is available; full instructions load on invocation, with supporting resources read only as needed. A description is a model-selection hint, not a deterministic router. Put the activity, concrete task, and boundary first; the delegate's explicit if/else routing can then request an exact skill. [1][2; routing recommendation]
- **Claude Code:** `description` states what/when; absent it, Code uses the first nonempty body line. `when_to_use` is appended. The combined listing text defaults to a 1,536-character cap, and the total listing budget can drop less-used descriptions. Keep descriptions short and distinguish overlapping workflows. [2, “Frontmatter reference”, “Claude doesn't see all my skills”]
- **OpenCode V2:** each model step lists permitted skills with a description unless `metadata.opencode/autoinvoke` is false. No description means not advertised. Loading uses the exact ID and checks the agent's skill permission. [1, “Frontmatter”, “Loading”, “Permissions”]

Invocation controls are **not equivalent**: [1][2, “Control who invokes a skill”]

| Intent | Claude Code | OpenCode V2 |
| --- | --- | --- |
| Manual-only / omit auto-discovery | `disable-model-invocation: true` blocks model invocation, not just advertising. | `metadata: { opencode/autoinvoke: false }` hides advertising, but explicit ID loads still work. |
| Hide interactive entry | `user-invocable: false` hides menu and disallows typed invocation, while model invocation remains. | `slash: false` (or `metadata.opencode/slash`) hides interactive command catalogs. |

Do not rely on a description saying “only when explicitly invoked” as a hard permission boundary. Nor assume Claude-specific frontmatter enforces the same behavior in OpenCode: use each tool's documented controls where required. [1][2; recommendation]

## 5. Referring to other skills and sharing scripts

**Cross-skill references:** a skill body can instruct the agent to load another available skill by its exact ID/name, subject to invocation permissions. This is a practical composition pattern inferred from documented instruction bodies and model skill loading, **not a documented dependency/import system**. Neither cited product guide defines dependency resolution, automatic installation, ordering, or cycle handling between skills. Keep references explicit, update them on renames, and do not use a Markdown link as if it automatically activated the linked skill. [1, “Loading”][2, “Types of skill content”, “Control who invokes a skill”][3, “Body content”]

**Supporting files are directly supported:** keep scripts/references alongside `SKILL.md`, reference them from the body, and execute scripts only when needed. OpenCode describes paths as relative to the skill's base directory and supplies that base directory on loading; this is not a guarantee that a shell starts there. Claude Code offers `${CLAUDE_SKILL_DIR}` to reference bundled scripts independently of working directory. Plugin skills can use `${CLAUDE_PLUGIN_ROOT}` for resources shared across skills in that plugin. These Claude substitutions are not a documented OpenCode V2 feature. [1, “Create”, “Loading”][2, “Available string substitutions”, “Add supporting files”][3]

**Recommended shared-mechanics pattern for this repo:** have one unprefixed shared skill own its helper scripts and tell callers to load it, then resolve helpers from that owning skill's supplied base directory. This avoids duplicating mechanics and hardcoding sibling installation paths. A repo-level shared script directory can also work in this controlled installation if paths and distribution are explicitly maintained, but neither guide guarantees it is bundled with each standalone skill. Treat this as a repository design choice, not a portable dependency feature. [1][2][3; recommendation]

## 6. Rename checklist and remaining uncertainty

1. Choose unique `swe-…` / `study-…` IDs; retain unprefixed shared skills. Keep name and directory identical and under the portable limits.
2. Search all skill bodies, scripts, docs, permission rules, and routing logic for old names and absolute/relative paths; change intentional references together.
3. Deploy canonical directory moves and recreate the corresponding `.claude/skills` links; do not leave old names as accidental aliases.
4. Check actual loaded listings in each tool, explicit invocation, one intended trigger, one near-miss, and one shared-helper call. In Claude, check plugin-qualified names and `/skills`; in OpenCode check exact IDs and later source overrides.
5. Do not rename or edit the installed engineering plugin to solve local workflow overlap; distinguish local descriptions or choose its fully qualified command deliberately.

These are proposed acceptance checks, **not tests performed in this research**. No skills, settings, symlinks, or plugin files were changed. The researched sources establish documented behavior, not the installed clients' exact version-dependent behavior. I did not verify live auto-trigger quality, plugin activation, custom OpenCode transforms, same-priority duplicate ordering inside one source, or automatic skill-to-skill chaining. Current official Claude docs include recent version-specific behavior; check the installed version before relying on those refinements. [1][2][5]

## Primary sources

1. [OpenCode V2 — Skills](https://opencode.ai/v2/docs/skills): discovery, sources, frontmatter, IDs, precedence, loading, permissions.
2. [Claude Code — Extend Claude with skills](https://code.claude.com/docs/en/skills): locations, symlinks, collision precedence, names, invocation, resources, troubleshooting.
3. [Agent Skills specification](https://agentskills.io/specification): portable names, descriptions, layout and file references.
4. [Claude Code — Plugins overview](https://code.claude.com/docs/en/plugins/overview): plugin identity, namespaced commands, enabled-plugin context cost.
5. [OpenCode V2 — Plugins, Skills API](https://opencode.ai/v2/docs/build/plugins#skills): skill registration and transforms.
6. Local installation files and symlink listing described above: inspected read-only on 2026-09-30; machine-local, not portable/public citations.
