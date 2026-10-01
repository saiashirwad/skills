# Can Paseo replace Herdr + OpenCode as the delegate backend?

Research for [ticket #16](https://github.com/saiashirwad/skills/issues/16), under [map #1](https://github.com/saiashirwad/skills/issues/1). Inspected 2026-10-01. **Recommendation: yes, as a backend migration with explicit behavioral changes, not a drop-in replacement.** Paseo supplies agent creation, follow-ups, lifecycle notifications, provider settings, and managed Git workspaces; the existing delegate scripts still supply the task/report contract that should survive. [Paseo MCP reference][mcp], [current spawn contract][spawn]

## Evidence boundary

Primary sources only: deployed Paseo documentation, upstream source pinned to `e0a0cf990d27f9a40cb1ef2fc490a1d2d7a7e4ef`, installed CLI help/source, live MCP discovery, and the user's own skills/scripts. The local untracked `paseo*/SKILL.md` files were read from `/Users/texoport/.agents/skills`, including the reference, advisor, committee, handoff, help, and plugin skills. The useful local orchestration rules agree with the public docs: discover profiles, materialize their settings, create an isolated workspace explicitly, and favor finish notifications. The handoff skill returns immediately, so it cannot itself replace delegate's await/report workflow. [Local Paseo reference](/Users/texoport/.agents/skills/paseo/SKILL.md), [local handoff](/Users/texoport/.agents/skills/paseo-handoff/SKILL.md), [MCP reference][mcp], [orchestration][orchestration]

### Live evidence

These are compact records of read-only calls made during this research, rather than claims about every Paseo installation:

| Probe | Observed result |
| --- | --- |
| `paseo --version`; `paseo daemon status --json` | CLI `0.4.0`; desktop-managed daemon `0.10.2`; local daemon reachable at `127.0.0.1:6767`; home `/Users/texoport/.paseo`. |
| MCP `list_profiles({})` | `profiles: []`. No saved tier profiles to reuse. |
| MCP `list_providers({})` | Codex and Claude available; OpenCode unavailable/disabled on this daemon. |
| MCP `list_models({provider:"codex"})` | Includes `gpt-6.1-sol`, `gpt-6-astra`, and `gpt-6-luna`. Sol and Astra offer medium/high; Luna offers high. |
| MCP `inspect_provider({provider:"codex/gpt-6.1-sol",settings:{thinkingOptionId:"medium"}})` | Selected model `gpt-6.1-sol`; modes `auto`, `auto-review`, `full-access`; only feature returned was `plan_mode`. |
| `paseo run/send/wait/logs/inspect/workspace create/provider models/permit --help` | The flags and commands in the examples below are present. |

The Sol model response has a discrepancy: `defaultThinkingOptionId` is `medium`, but its metadata says `defaultReasoningEffort: low`. Set thinking explicitly. The CLI/daemon versions also differ; upstream source findings below describe that pinned revision, with locally inspected CLI code corroborating the run/send/wait behavior. These observations do not prove a new worker will complete a job. [Recorded probes](#live-evidence), [installed run source](/Users/texoport/.local/share/mise/installs/node/24.18.0/lib/node_modules/@getpaseo/cli/dist/commands/agent/run.js)

## Start, brief, await, and read

### MCP

First call `list_profiles` and read its notes; materialize the selected profile's `provider/model`, `modeId`, `thinkingOptionId`, and `featureValues` into `create_agent`. There is no `profile` parameter. With no matching profiles, discover through `list_providers`, `list_models`, and `inspect_provider`; use model/mode IDs returned by that host. Our host has no profiles, so the following launch settings are a proposed fallback using observed IDs. [MCP profiles/discovery][mcp], [recorded probes](#live-evidence)

For a writing job, call these in order; these are illustrative requests, not an executed smoke test. `workspaceId` below means the ID returned by the first call. [Workspace tool schema][tools-workspaces], [agent tool implementation][tools-create]

```json
// create_workspace
{
  "path": "/Users/texoport/.agents/skills",
  "isolation": "worktree",
  "mode": "branch-off",
  "branchName": "research/example",
  "baseBranch": "refs/heads/main",
  "worktreeSlug": "research-example"
}
// create_agent
{
  "title": "Research example",
  "provider": "codex/gpt-6.1-sol",
  "workspaceId": "<returned workspaceId>",
  "initialPrompt": "<complete brief plus report contract>",
  "notifyOnFinish": true,
  "settings": {
    "modeId": "full-access",
    "thinkingOptionId": "medium"
  }
}
```

An agent-scoped call creates a child, even when placed in another workspace. Creation returns its `agentId` and placement/status metadata immediately; finish notification defaults to true. A top-level caller has different defaults and can wait synchronously. Tool injection is off by default, but shell-based CLI orchestration does not require it. [MCP ownership][mcp], [create source][tools-create], [orchestration setup][orchestration]

Brief the worker with the task, source paths, constraints, acceptance criteria, exact output path, and commit/push instructions. Retain `result.md` with an at-most-eight-line TL;DR, `DONE` written last, and `BLOCKED` for required human input. These are the existing delegate protocol; Paseo does not create those application-specific files for us. Use a report path accessible to the daemon/worker host. [Current spawn][spawn], [Paseo host execution model][orchestration]

Await the automatic notification while doing other work. Notifications cover finished, error, permission, and closure; the implementation labels a run-to-idle transition as finished and includes the latest assistant message, truncated at 4,000 characters. Read the report artifact for complete results; `get_agent_activity({agentId,limit})` supplies a curated timeline and `get_agent_status({agentId})` supplies lifecycle and permissions for targeted diagnosis. Follow up with `send_agent_prompt({agentId,prompt,background:true,notifyOnFinish:true})`; synchronous calls can return `lastMessage`. [Notification implementation][notify], [prompt implementation][tools-send], [activity implementation][tools-activity], [MCP tool catalog][mcp]

### CLI

The same job can use this command sequence. Substitute an actual source checkout, brief, and agent ID; `paseo run` takes the initial prompt as a positional argument, while `send` accepts `--prompt-file`. `--thinking high` selects high instead of medium. [CLI reference][cli], [run source][run], [send source][send], [local help evidence](#live-evidence)

```bash
paseo provider models codex --thinking --json
paseo run --background --json \
  --provider codex/gpt-6.1-sol --thinking medium --mode full-access \
  --cwd /Users/texoport/.agents/skills \
  --new-workspace worktree --worktree-mode branch-off \
  --new-branch research/example --base refs/heads/main \
  --title research-example "$(cat /absolute/path/brief.md)"

# Store the agentId and cwd from run's JSON; use that ID below.
paseo wait <agent-id> --timeout 3600 --json
paseo logs <agent-id> --tail 20
paseo inspect <agent-id> --json
paseo send <agent-id> --no-wait --prompt-file /absolute/path/followup.md
paseo wait <agent-id> --timeout 3600 --json
```

Foreground `run` waits by default, with no limit unless `--wait-timeout` is set. Its ordinary output is job metadata, not the complete final answer; use logs or the report file. `wait` returns a JSON status of `idle`, `permission`, `error`, or `timeout`, with a small recent-activity preview for idle/timeout. Parse that status; do not map shell exit zero directly to delegate's `DONE`. The installed and pinned `send` implementation has a ten-minute blocking wait, so `--no-wait` followed by an explicit `wait` avoids mistaking a long follow-up for failure. [Run source][run], [wait source][wait], [send source][send], [installed send](/Users/texoport/.local/share/mise/installs/node/24.18.0/lib/node_modules/@getpaseo/cli/dist/commands/agent/send.js)

## Isolation, Git delivery, and cleanup

Paseo supports a branch per job through worktree `branch-off`, plus existing-branch and PR checkout modes. Specify the base ref deliberately: `refs/heads/main` means local main; `origin/main` means the remote-tracking ref. Worktrees are separate working directories built with `git worktree add`, sharing the repository's Git common directory and refs. Therefore the current `land` step's fetch from an independent Rift is unnecessary for a managed worktree in the same repository: review the branch directly, without merging it. [Worktree docs][worktrees], [worktree creation/shared Git source][worktree-source], [current land][land]

**It is not a Rift snapshot.** Rift's current delegate contract copies the user's uncommitted work; Paseo starts from a Git ref. Fresh worktrees lack installed dependencies and ignored files such as `.env`. Setup/teardown hooks in committed `paseo.json` can install or copy required assets using `PASEO_SOURCE_CHECKOUT_PATH`. Proposed policy: delegate from a committed base, or explicitly prepare a snapshot/patch before spawning when dirty state is essential. Do not silently change this behavior. [Current spawn][spawn], [Paseo worktrees/setup][worktrees]

Agents run on the daemon machine with its provider installation and authentication. A brief can instruct ordinary `git add`, `git commit`, and `git push`; full-access mode permits filesystem/command/network work, but successful pushes still depend on Git credentials and connectivity. This research session already occupies the requested managed worktree and branch; that alone does not confirm a fresh child's Git delivery. [Codex setup][codex], [mode implementation][codex-modes], [worktree docs][worktrees]

Archive the workspace only after verifying/preserving the branch and artifacts: archiving also archives its agents/terminals and removes a managed worktree after the last active workspace reference is archived. This differs from current `finish`, which sends Rift to its trash and leaves the Herdr tab. Proposed replacement `finish` must keep reports outside the removed worktree or retain the committed research artifact. [Workspace lifecycle][mcp], [worktree lifecycle][worktrees], [current finish][finish]

## Finish and hang detection

| Situation | Current delegate | Paseo evidence and proposed mapping |
| --- | --- | --- |
| Task reports done | `DONE` marker → exit 0 | Keep marker/report and verify actual files, tests, commits. Lifecycle idle is only a trigger to inspect. [await][await], [run idle mapping][run] |
| Needs a person | `BLOCKED`, OpenCode permission/form → exit 2 | Pending permissions and notifications are native; retain `BLOCKED` for decisions/credentials that are not permission requests. [await][await], [notifications][notify], [MCP permissions][mcp] |
| Stops early | Three idle checks without `DONE` → exit 3 | Idle/error/closed plus missing contract artifact identifies incomplete work; expose the reason. [await][await], [wait statuses][wait] |
| Wall deadline | Default 60 minutes → exit 4 | CLI `wait --timeout`; timeout means the waiter stopped, not that the worker was cancelled. Diagnose before `cancel_agent`/`paseo stop` or resend. [await][await], [wait implementation][wait], [MCP cancellation][mcp] |
| Running silently | No token-total increase for 900 seconds → exit 5 | No equivalent inactivity detector confirmed in inspected wait/notification paths. Use a wall deadline and inspect activity; label suspected hang separately from confirmed failure. [await][await], [wait implementation][wait], [notification implementation][notify] |

Paseo's finish notification implementation uses an in-memory event subscription; it skips archived parents and logs notification-delivery errors. I could not confirm durable replay of an armed callback across daemon restarts. Keep IDs and report paths so a resumed orchestrator can recover with list/inspect/activity and artifacts rather than relying on a callback as a durable job ledger. This is a recovery recommendation derived from the source, not a tested restart guarantee. [Notification implementation][notify]

## Permission modes, cost, and limits

For explicitly authorized unattended write/commit/push jobs, choose Codex `full-access`; its preset maps to approval policy `never` and sandbox `danger-full-access`. `auto` maps to `on-request`/`workspace-write`, and `auto-review` keeps that sandbox while selecting an automatic reviewer. Neither is a guarantee that a run will never need a person. Provider-specific overrides can supersede preset fields; inspect the effective mode instead of assuming the launch label proves the effective permissions. Forward pending approvals to the user, consistent with the existing delegate/herdr rules. [Codex mode presets and override handling][codex-modes], [live modes](#live-evidence), [delegate][delegate], [herdr][herdr]

Paseo's Codex docs say it adds no Codex charge: ChatGPT login uses the plan's Codex allowance; API-key login uses the OpenAI Platform account's billing. Normal provider limits/pricing still apply. This does not establish this account's remaining allowance, a per-job dollar estimate, or that Sol-medium is cheaper than the current `oai/astralow` route. No quantitative concurrency ceiling or enforced per-job spending cap was confirmed from the inspected sources/tools. Budget those as unknown rather than claiming unlimited/free work. [Paseo Codex billing docs][codex], [current model routing][models], [live discovery](#live-evidence)

## What the Notes' model tiers would become

The map Notes currently specify default `oai/astralow`, light `openai/gpt-6-luna#high`, hard `openai/gpt-6-astra#high`. The checked-in `delegate/models` additionally has `sol openai/gpt-6.1-sol#high`. Paseo's live Codex discovery supports the proposed replacements below; these are routing recommendations, not measured equivalence in quality, latency, or billing. [Map Notes][map], [model file][models], [live discovery](#live-evidence)

| Tier | Proposed provider/model | Explicit thinking | Intent |
| --- | --- | --- | --- |
| default | `codex/gpt-6.1-sol` | `medium` | Normal research, review, implementation, chores. |
| light | `codex/gpt-6-luna` | `high` | Small lookups; preserve the existing model/effort intent. |
| hard | `codex/gpt-6-astra` | `high` | Failed default jobs and independent verification. |
| sol (optional compatibility alias) | `codex/gpt-6.1-sol` | `high` | Explicit high-effort Sol job. |

Prefer named Paseo profiles with task-selection notes when the user configures them; otherwise keep this tiny fallback tier table in delegate's model configuration. Changing provider/model spelling does not preserve the custom `oai/astralow` endpoint/authentication behavior. No local profiles or matching custom Paseo provider were observed. [Profiles][profiles], [current tiers][models], [recorded probes](#live-evidence)

## What I could not confirm

- A fresh agent's complete create → brief → callback → report → follow-up → commit/push → archive cycle. Research used read-only CLI/MCP probes and source inspection; the launch examples were not executed.
- Callback delivery through daemon restart, parent archival, or transport failure. Source shows subscriptions and failure handling, not a durable delivery guarantee. [Notifications][notify]
- A native equivalent to the 15-minute token-silence detector, automatic repair of hung providers, or complete parity for every OpenCode form/question. The inspected wait API reports lifecycle/permission/deadline outcomes. [Wait source][wait], [current await][await]
- Automatic preservation of dirty/untracked/ignored checkout contents equivalent to Rift; the documented setup mechanism requires explicit preparation. [Worktree docs][worktrees], [spawn][spawn]
- Exact cost, remaining account quota, maximum parallelism, or equivalent quality/latency for the tier change. Discovery confirms availability/settings, not those quantities. [Codex billing][codex], [recorded probes](#live-evidence)
- Identical behavior between installed CLI `0.4.0`, daemon `0.10.2`, and upstream main. Local help and CLI source corroborate the commands inspected; source conclusions are pinned, not a claim of full runtime parity. [Recorded probes](#live-evidence)

## Source index

Paseo docs were selected from the first-party [llms.txt index](https://paseo.sh/llms.txt) and fetched directly. Local-only paths are intentionally cited as such because the user's Paseo skills are untracked; the compact live observations above preserve the evidence needed to read this report from GitHub. Repository and upstream source links below are pinned for review.

[mcp]: https://paseo.sh/docs/mcp.md
[cli]: https://paseo.sh/docs/cli.md
[codex]: https://paseo.sh/docs/codex.md
[worktrees]: https://paseo.sh/docs/worktrees.md
[orchestration]: https://paseo.sh/docs/orchestration.md
[profiles]: https://paseo.sh/docs/agent-profiles.md
[map]: https://github.com/saiashirwad/skills/issues/1
[delegate]: https://github.com/saiashirwad/skills/blob/74a3d6f355ffb0b6a3073d25079dc7dce5b6de32/delegate/SKILL.md
[herdr]: https://github.com/saiashirwad/skills/blob/74a3d6f355ffb0b6a3073d25079dc7dce5b6de32/herdr/SKILL.md
[models]: https://github.com/saiashirwad/skills/blob/74a3d6f355ffb0b6a3073d25079dc7dce5b6de32/delegate/models
[spawn]: https://github.com/saiashirwad/skills/blob/74a3d6f355ffb0b6a3073d25079dc7dce5b6de32/delegate/scripts/spawn#L48-L81
[await]: https://github.com/saiashirwad/skills/blob/74a3d6f355ffb0b6a3073d25079dc7dce5b6de32/delegate/scripts/await
[land]: https://github.com/saiashirwad/skills/blob/74a3d6f355ffb0b6a3073d25079dc7dce5b6de32/delegate/scripts/land
[finish]: https://github.com/saiashirwad/skills/blob/74a3d6f355ffb0b6a3073d25079dc7dce5b6de32/delegate/scripts/finish
[run]: https://github.com/getpaseo/paseo/blob/e0a0cf990d27f9a40cb1ef2fc490a1d2d7a7e4ef/packages/cli/src/commands/agent/run.ts
[send]: https://github.com/getpaseo/paseo/blob/e0a0cf990d27f9a40cb1ef2fc490a1d2d7a7e4ef/packages/cli/src/commands/agent/send.ts
[wait]: https://github.com/getpaseo/paseo/blob/e0a0cf990d27f9a40cb1ef2fc490a1d2d7a7e4ef/packages/cli/src/commands/agent/wait.ts
[notify]: https://github.com/getpaseo/paseo/blob/e0a0cf990d27f9a40cb1ef2fc490a1d2d7a7e4ef/packages/server/src/server/agent/agent-prompt.ts#L383-L588
[tools-workspaces]: https://github.com/getpaseo/paseo/blob/e0a0cf990d27f9a40cb1ef2fc490a1d2d7a7e4ef/packages/server/src/server/agent/tools/paseo-tools.ts
[tools-create]: https://github.com/getpaseo/paseo/blob/e0a0cf990d27f9a40cb1ef2fc490a1d2d7a7e4ef/packages/server/src/server/agent/tools/paseo-tools.ts#L1430-L1557
[tools-send]: https://github.com/getpaseo/paseo/blob/e0a0cf990d27f9a40cb1ef2fc490a1d2d7a7e4ef/packages/server/src/server/agent/tools/paseo-tools.ts#L1892-L1988
[tools-activity]: https://github.com/getpaseo/paseo/blob/e0a0cf990d27f9a40cb1ef2fc490a1d2d7a7e4ef/packages/server/src/server/agent/tools/paseo-tools.ts#L3053-L3104
[worktree-source]: https://github.com/getpaseo/paseo/blob/e0a0cf990d27f9a40cb1ef2fc490a1d2d7a7e4ef/packages/server/src/utils/worktree.ts
[codex-modes]: https://github.com/getpaseo/paseo/blob/e0a0cf990d27f9a40cb1ef2fc490a1d2d7a7e4ef/packages/server/src/server/agent/providers/codex-app-server-agent.ts

## Concrete recommendation and losses

**Make `delegate` the small task policy and report layer over Paseo.** Keep `spawn`, `followup`, `await`, `jobs`, `land`, and `finish` as compatibility entry points, but store `agentId`, `workspaceId`, cwd, tier, branch, and report path. `spawn` creates a worktree for writing jobs and submits a complete brief; `await` uses a finish notification in agent-scoped MCP or bounded CLI wait, then enforces the report markers and validates the work. `followup` rearms the contract, `jobs` recovers IDs/state, `land` shows the already-local Git branch/diff, and `finish` archives only after delivery and artifact preservation. Adopt the explicit tier table above, subject to available human-configured profiles. This is proposed implementation, justified by the current script contract and Paseo's available surfaces. [Delegate scripts][spawn], [current await][await], [Paseo MCP][mcp], [CLI][cli], [profiles][profiles]

**Retire `herdr` from the delegate dependency chain and use the existing `paseo` reference for session operations.** Keep `herdr` only if the user still wants to operate actual Herdr panes; its visible-terminal reads, pane identities, and `HERDR_ENV` gate are not Paseo agent operations. The separate policy/reference boundary already exists in delegate/herdr and can stay small. [Current delegate][delegate], [current herdr][herdr], [Paseo tools][mcp]

**We would lose** automatic Rift copying of uncommitted checkout contents; the current exit-5 token-silence heuristic unless rebuilt; the custom `oai/astralow` route unless configured separately; and the Herdr/OpenCode TUI pane used to watch and take over a worker. Paseo supplies its own subagent conversations, timelines, and terminals, but those do not establish identical TUI interaction. Keep the report/verification protocol so task completion semantics survive these losses. Proceed with this migration decision, then validate one writing job and one blocked/follow-up job before switching the default backend. [Current spawn/models][spawn], [model routing][models], [await][await], [herdr][herdr], [Paseo orchestration][orchestration], [MCP][mcp]
