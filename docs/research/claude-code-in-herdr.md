# Can delegate drive Claude Code sessions in Herdr like OpenCode?

Research for [ticket #4](https://github.com/saiashirwad/skills/issues/4), in [map #1](https://github.com/saiashirwad/skills/issues/1). Researched 2026-09-30.

## Answer

**Yes, but not by swapping the executable in the current scripts.** Keep the brief, Rift, report, and `DONE`/`BLOCKED` contract; add a Claude backend for launch, state, interruption, and follow-up. Herdr already supports `--kind claude` and interactive prompt/wait/read. Unlike the OpenCode service calls used today, this path submits through the terminal, and Herdr's Claude lifecycle detection is screen-based. [D1][D2][H1][H2][H3]

**Recommendation:** implement the smallest interactive Claude backend first, with explicit acknowledgment that its tab hosts the worker rather than merely watching a service. If worker independence from the tab is required, prototype **Claude's native background sessions** before building a print-mode supervisor: the installed CLI already has `--bg`, `attach`, and supported JSON state polling. Background mode is research preview, has additional isolation behavior, and its Herdr attachment needs validation. Print mode is an alternative for structured automation, not an interactive Claude tab with approvals for free. [C1][C2][C4]

No agent jobs were started for this research; command help, installed integration status, official documentation, and Herdr source were inspected. The implementation and acceptance tests below are proposals, not tested changes.

## Evidence and version boundary

Read-only local checks found:

- `claude --version`: **2.1.285**. Its `--help` lists `--session-id`, `--resume`, `--model`, `--effort`, print/stream flags, hooks-related output, `--bg`, and `--permission-prompts`.
- `herdr status`: **client 0.9.3; running server 0.9.1**, endpoint/private protocol compatible, server binary stale. No restart or upgrade was performed.
- `herdr agent`: lists `claude` as a supported kind and the start/prompt/wait/get/read/send-keys commands.
- `herdr integration status`: Claude integration **v10**, current. The inspected v0.9.3 source is also v10. The integrations page's general minimum-version list says v6 for Claude, while its Claude-specific section describes v10; use the specific source and installed status, not that minimum list, for current behavior. [H2][H3]

Herdr references below are pinned to v0.9.3. Claude documentation is living documentation read on the research date. Installed help confirms flag availability, not successful end-to-end execution. In particular, client/server compatibility does not prove every 0.9.3 behavior exists in the running 0.9.1 server.

## What delegate does now

| Surface | Current behavior | What can stay |
| --- | --- | --- |
| `spawn` | Parses a tier into OpenCode provider/model/variant; creates a session with `POST /api/session`; starts an OpenCode watcher tab; sends the brief path via the service API | Job directory, brief augmentation, source path, Rift snapshot/branch, no-focus tab creation |
| `await` | Checks report markers, active sessions, pending permissions/forms; compares cumulative input/output/reasoning tokens for a 15-minute hang heuristic | Report formatting, deadlines, exit meanings, explicit human escalation |
| `followup` | Clears markers and posts another prompt to the saved session | Same context/Rift, report rewrite contract |
| `lib.sh` / `jobs` | Common status assumes `/api/session/active` | Job lookup and TL;DR extraction; status needs dispatch by backend |
| `land` / `finish` | Fetches the Rift branch into the source checkout without merging; later removes the Rift | Git/Rift mechanics, provided the worker actually edits that Rift and is no longer using it |

Sources: `spawn` lines 33–81; `await` lines 22–51; `followup` lines 8–15; `lib.sh` lines 14–27; `land` lines 8–14; `finish` lines 8–14. [D1][D2][D3][D4][D5][D6]

A watcher startup failure is currently nonfatal because work can still run in the OpenCode service. **That assumption must not carry over to an interactive Claude backend:** if the Claude tab fails to launch, no independent worker has been created. [D1][H1]

## Option A — Interactive Claude in the job's Herdr tab

This is the smallest change that preserves a real approval/question UI.

### Spawn

Proposed sequence, after the existing brief/Rift preparation (variables are placeholders; not a complete script):

```bash
# Save the UUID as this job's Claude conversation ID, separate from pane/name.
sid=$(python3 -c 'import uuid; print(uuid.uuid4())')
created=$(herdr tab create --workspace "$HERDR_WORKSPACE_ID" \
  --cwd "$cwd" --label "$name" --no-focus)
pane=$(printf '%s\n' "$created" | jq -r '.result.root_pane.pane_id')
herdr agent start "$name" --kind claude --pane "$pane" --timeout 60000 -- \
  --session-id "$sid" --model "$claude_model" --add-dir "$job"
# Run this wait as part of the job watcher, not as a blocking spawn call.
herdr agent prompt "$name" "Read $job/brief.md and carry it out." \
  --wait --timeout 3600000
```

`agent start` waits for readiness, so launch **without the initial brief as a positional prompt**, then submit the brief once ready. Store `backend=claude-interactive`, conversation UUID, pane, name, cwd, and resolved model. Validate Herdr's actual name limit (`[a-z][a-z0-9_-]{0,31}`), stricter than the current spawn regex. Claude accepts model aliases/full Claude model names, not OpenCode `provider/id#variant`; create backend-specific tier mappings instead of translating an OpenAI model string. `--effort` is separate and model-dependent. `--add-dir` grants access to the job directory; it is not blanket approval for all writes or shell commands. [H1][C1]

The `--wait` prompt matters: Herdr checks for observed working/blocked activity after submission from an idle state. A separate prompt without waiting followed by `agent wait` can see the old idle state before the new turn begins. A watcher should record submission/turn generation and own this start gate, while checking report files in parallel. Do not let multiple follow-ups overlap: waits observe lifecycle, not a particular turn. [H1]

A startup trust/login/approval dialog can produce `agent_not_ready`; keep the pane/name for inspection and return blocked/startup failure, not “started.” Never auto-accept it. If `defaultToAgentsView` is configured, launching `claude` without a prompt may open agent view instead of a conversation; the adapter must explicitly override that setting for this job (for example session `--settings '{"defaultToAgentsView":false}'`) and verify the expected conversation UI. [H1][C4]

### Await and status

Preserve the public exit contract, but replace OpenCode endpoints:

| Observation | Proposed delegate handling |
| --- | --- |
| Current-generation `DONE` plus readable report | Success (0); inspect the changed files separately |
| `BLOCKED`, or Herdr `blocked` | Needs human (2); read visible pane, retain the pending UI; never answer it automatically |
| Observed turn settles idle/done with no marker | Stalled (3), after a short filesystem grace period |
| Deadline exceeded | Timed out (4); leave work intact |
| Working without activity for the configured interval | Suspected hung (5), **not proof**; inspect before interrupting |
| `unknown`, missing agent, failed state read | Unknown/transport/worker failure; not success and not automatically “idle” |

Herdr `done` only means idle and not yet seen; focusing can change it to idle. Neither state proves the report contract was fulfilled. `unknown` does not prove completion. Claude's Herdr hook supplies session identity only: its `SessionStart` handler calls `pane.report_agent_session`, not a lifecycle report. Actual state is detected from title/spinner/prompt/dialog rules, including Bash permission and MCP elicitation forms. Treat that as a fallible observation, especially after Claude UI changes. [H1][H2][H3][H4]

The current token counter has no equivalent supplied by `herdr agent get`. For a first version use a bounded overall timeout plus screen/hook activity as diagnostics, or label an inactivity timeout “suspected hung.” Long tools, retry waits, and unchanged spinners make inactivity imperfect; do not call it the same token-based guarantee. The existing OpenCode token test itself is only a heuristic. [D2][H1][H4]

### Follow-up, interruption, report

Only follow up when the prior turn is settled and not blocked. Re-arm markers after validating the target, then send the new instructions through the same gated `herdr agent prompt ... --wait` path. Persist a new turn generation to prevent stale files/events from satisfying the next run. If the process exited, use `claude --resume "$sid"` in the saved cwd, not a new `--session-id`, `--continue`, or `--fork-session`. `--continue` can select the wrong conversation when jobs share a directory; `--fork-session` deliberately creates a new ID. [C1][C2][H1]

For deliberate cancellation, use `herdr agent send-keys "$name" esc` or `ctrl+c` and re-read state; do not interpret the keypress itself as a completed cancellation. Read `result.md` directly, retaining the existing TL;DR contract. Use `agent read --source visible` for blockers; larger history reads can require idle and may not recover the entire alternate-screen transcript. [H1][D3][D4]

## Option B — Native Claude background worker, Herdr attachment

**Important new capability:** a service-like model is available in the installed Claude version. `claude --bg --model <model> --name <name> "Read <brief> ..."` starts a supervised worker and returns a short job ID. `claude attach <id>` opens its interactive session, and the worker survives detachment. `claude agents --json --all` is the supported state interface; do not parse `~/.claude/jobs/*/state.json`. [C1][C4]

A candidate adapter would:

1. Launch in the job's Rift, capture the returned short `id`, then correlate it with `sessionId` from the JSON list. Store both: the short ID is for attach/logs/stop, the UUID for resume. Launch output is human text with possible startup messages, so do not assume stdout is just a UUID. [C4]
2. Open the watcher tab with the native `claude attach <id>` command. Herdr's passthrough suggests `agent start ... --kind claude -- attach <id>`, but readiness while attaching to an already-working/blocked job is **not verified**; raw `pane run` plus explicit detection may be needed. A watcher failure can then be nonfatal because the worker is independently hosted. [H1][C4]
3. Poll the exact JSON entry: `state` is `working|blocked|done|failed|stopped`; live `status` is `busy|waiting|idle`; `waitingFor` distinguishes permission prompt, input needed, sandbox request, worker request, and dialog open. Honor markers as the task-level success contract; `done` without the report is still a delegate stall. JSON read failure or missing entry is unknown, not done. [C4]
4. Send follow-ups through the attached conversation when available. `--resume <full-UUID> --bg "follow-up"` can continue in place **or create a copy** when it cannot reuse the running session, so it is not an unconditional same-session prompt API. Do not silently switch the recorded ID after such a copy. Use `claude stop <short-id>` only for deliberate interruption/stop, not as an automatic prelude to every follow-up. [C4]

Two integration hazards make this a prototype rather than the default recommendation:

- Background mode checks workspace trust and fails in a noninteractive script if trust has not been granted. A new Rift can require human trust. Do not bypass it to make spawn succeed. [C4]
- Background workers normally move into their own git worktree before editing. Rift is described by delegate as a checkout copy, not necessarily a linked git worktree. This can break `land`, which expects the branch in the recorded Rift. A background adapter must explicitly keep isolation owned by delegate, e.g. job-scoped `--settings '{"worktree":{"bgIsolation":"none"}}'` **only inside the already-isolated Rift**, or redesign branch/path tracking. Verify actual cwd/branch before landing. Do not globally turn isolation off. [D1][D5][C4]

The background supervisor is also a different process environment. Validate that session-identity hooks identify the attached Herdr pane correctly, rather than attributing the worker to the dispatcher's inherited pane. No source inspected here establishes this interaction. Agent view is explicitly research preview. [H3][C4]

## Option C — Print/stream-json worker

Use this when a structured process boundary matters more than an interactive Claude tab:

```bash
claude -p "Read $job/brief.md and carry it out." \
  --session-id "$sid" --model "$claude_model" --add-dir "$job" \
  --output-format stream-json --verbose --include-partial-messages \
  --permission-prompts none
# Later, after that process has exited:
claude -p "<follow-up and renewed report contract>" --resume "$sid" \
  --output-format stream-json --verbose --include-partial-messages \
  --permission-prompts none
```

A supervisor must set cwd, store stdout/stderr and process exit status, parse newline-delimited events, retain persistence, and enforce timeouts. `--include-partial-messages` enables model-output activity tracking; tool/hook events provide other progress signals. The `result` event and exit status indicate a run ended, not that the delegated artifact is correct. Success requires the report/marker too. Do not rely exclusively on the last line being `result`: optional prompt suggestions and version-specific events exist; parse by event type. [C1][C2]

**A denied permission is not a pending interactive approval.** Without a permission host, unresolved requests in print mode are denied. `--permission-prompts none` makes this explicit and removes tools requiring a person's answer; `permission_denied` stream events and final `permission_denials` report denials. A denial can be recoverable, so classify “blocked” based on an unresolved task requirement/report rather than blindly treating any past denial as a pending question. For genuine pause-and-ask semantics, add an Agent SDK `canUseTool` host or documented MCP permission-prompt tool, retain pending requests, and route them to the human. That is additional orchestration, not a Herdr UI feature. [C1][C2]

Show logs in a Herdr **pane**, not `agent start -p`: Herdr start expects a recognized interactive agent ready for input. Do not assume an interactive `--resume` watcher can safely share a live print session. For cancellation, print-mode SIGTERM exits 143 without a final result and leaves the turn unfinished; SIGINT ends the turn instead. Keep that distinct from a completed report. [H1][C2]

## Hooks: useful telemetry, not completion authority

Optional job-scoped command hooks can record `SessionStart`, `UserPromptSubmit`, `PreToolUse`/`PostToolUse`, `PermissionRequest`, `Notification`, `Stop`, `StopFailure`, and `SessionEnd`. Hook inputs include session identity and transcript path. Route by the exact conversation/job/turn, serialize or atomically replace state, and ignore subagent events if only the main worker is tracked. Use `--settings <job-settings.json>` rather than overwriting user settings or Herdr's managed hook script. [C1][C3][H3]

- `PermissionRequest` signals a permission decision point; a logging hook must return no allow/deny decision. It is not coverage for every question, trust screen, login, or cancelled dialog. `Notification` includes permission/elicitation types, but lifecycle gaps still require reconciliation. [C3][H2]
- `Stop` means Claude finished responding; it is not proof the job is finished, and stop hooks can continue the turn. `StopFailure` covers API-error termination; `SessionEnd` means session termination, not success. Never create `DONE` on every Stop/SessionEnd. [C3]
- `--bare` and safe mode affect hooks/configuration; bare mode also changes authentication and context loading. Do not silently enable them for a delegate task relying on installed skills, CLAUDE.md, Herdr hooks, or subscription login. The local help and current docs differ in some bare-mode discovery wording; this research does not resolve every discovery detail. [C1][C2]

## Implementation boundary and acceptance tests

Suggested shared interface: `start`, `submit`, `state`, `interrupt`, `read`, with persisted backend-specific IDs. Leave the OpenCode path unchanged; make Claude opt-in. Keep filesystem reports independent of transport. Extend `jobs` through backend-dispatched `lib.sh` status; `land` remains backend-agnostic only with verified cwd/branch. `finish` must not remove a Rift still used by a Claude process. These are design recommendations derived from the differences above, not existing APIs. [D1–D6]

Before shipping, test in an explicitly authorized disposable job:

1. Start/model selection, read brief, write report then DONE, follow up with retained context.
2. Startup trust/login blocking; tool approval; question; MCP/sandbox input; human cancellation. No automatic approval.
3. Idle without DONE; crash; unknown detection; watcher tab loss; missing report; state query failure.
4. Very fast completion, prompt stalled after delivery, stale markers, concurrent follow-up rejection.
5. Long quiet tool, model retry, timeout, deliberate interrupt/resume; no false success.
6. Background variant: attachment readiness, short ID/UUID mapping, no accidental copied session, no nested worktree, correct Herdr pane attribution.
7. `land` sees the actual branch and only intended files; no cleanup while worker remains active.

**Not confirmed:** end-to-end behavior against this user's running Herdr 0.9.1 server and Claude 2.1.285 UI; native-background attach detection; integration environment attribution; exact background launch parsing; a stable token-growth metric equivalent to OpenCode's session endpoint. None requires answering a human decision to finish this research; they are implementation validation work.

## Primary sources

Repository sources are pinned to the inspected baseline `74a3d6f355ffb0b6a3073d25079dc7dce5b6de32`:

- [D1 — delegate spawn](https://github.com/saiashirwad/skills/blob/74a3d6f355ffb0b6a3073d25079dc7dce5b6de32/delegate/scripts/spawn)
- [D2 — delegate await](https://github.com/saiashirwad/skills/blob/74a3d6f355ffb0b6a3073d25079dc7dce5b6de32/delegate/scripts/await)
- [D3 — delegate followup](https://github.com/saiashirwad/skills/blob/74a3d6f355ffb0b6a3073d25079dc7dce5b6de32/delegate/scripts/followup)
- [D4 — delegate lib.sh](https://github.com/saiashirwad/skills/blob/74a3d6f355ffb0b6a3073d25079dc7dce5b6de32/delegate/scripts/lib.sh)
- [D5 — delegate land](https://github.com/saiashirwad/skills/blob/74a3d6f355ffb0b6a3073d25079dc7dce5b6de32/delegate/scripts/land)
- [D6 — delegate finish](https://github.com/saiashirwad/skills/blob/74a3d6f355ffb0b6a3073d25079dc7dce5b6de32/delegate/scripts/finish)
- [D7 — delegate instructions](https://github.com/saiashirwad/skills/blob/74a3d6f355ffb0b6a3073d25079dc7dce5b6de32/delegate/SKILL.md)
- [H1 — Herdr agent automation, v0.9.3](https://github.com/herdrdev/herdr/blob/v0.9.3/docs/next/website/src/content/docs/agent-automation.mdx); also checked installed `herdr --skill`, `herdr --help`, and `herdr agent`.
- [H2 — Herdr integrations, v0.9.3](https://github.com/herdrdev/herdr/blob/v0.9.3/docs/next/website/src/content/docs/integrations.mdx)
- [H3 — actual Claude integration hook, v0.9.3](https://github.com/herdrdev/herdr/blob/v0.9.3/src/integration/assets/claude/herdr-agent-state.sh)
- [H4 — Claude screen-detection manifest, v0.9.3](https://github.com/herdrdev/herdr/blob/v0.9.3/src/detect/manifests/claude.toml)
- [C1 — Claude Code CLI reference](https://code.claude.com/docs/en/cli-reference); cross-checked installed `claude --help` and `claude --version`.
- [C2 — Run Claude Code programmatically](https://code.claude.com/docs/en/headless), especially streaming, permissions, SIGTERM, and continuation.
- [C3 — Claude Code hooks reference](https://code.claude.com/docs/en/hooks), especially common input fields, PermissionRequest, Notification, Stop, StopFailure, and SessionEnd.
- [C4 — Claude Code agent view/background sessions](https://code.claude.com/docs/en/agent-view), especially shell dispatch, JSON state schema, isolation, and the supervisor.
