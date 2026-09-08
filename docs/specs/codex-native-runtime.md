---
slug: codex-native-runtime
title: Codex-native runtime: Codex coordinates and executes, same gates, same evidence
status: draft
saved: 2026-09-07T18:29:09+00:00
---

# Codex-native runtime: Codex coordinates and executes, same gates, same evidence

> Captured 2026-09-07 from operator direction: "make the harness usable with
> Codex alone, without Claude, and with no loss in the workflow or features.
> We do not need `codex exec` when we are already in Codex, Codex has a user
> request tool, and it cannot switch itself into plan mode."

## Why

The README promises a Codex-only runtime "on the same artifact contract", but
nothing implements it. A machine with only the Codex CLI cannot run the
harness at all today, for four mechanical reasons:

1. **The only write path is a Claude Code plugin.** `forge delegate` and
   `forge grill run` resolve the codex-plugin-cc companion script from
   `~/.claude/plugins/installed_plugins.json` and launch it with a pinned
   `node codex-companion.mjs task …` argv that `forge stage done` re-checks
   byte for byte. `forge codex status` and the board read that plugin's job
   registry. Without Claude Code installed there is no companion, no launch,
   no status.
2. **Grill provenance is Claude-only by construction.** Every grill gate is
   ledger-matched: each round must equal an `AskUserQuestion` record written
   by Claude's `PostToolUse` hook. Codex has no such tool, and the Codex hook
   registration carries no `PostToolUse` at all, so a Codex session can never
   pass spec confirm, plan save, or task approve.
3. **The Codex write lock has a hole.** `.codex/hooks.json` registers
   `PreToolUse` for `Bash` only; the session's `apply_patch`, `Edit`, and
   `Write` calls bypass the always-armed planning lock and the strict role
   split that the Claude adapter enforces.
4. **Machine readiness assumes both tools.** `forge doctor` hard-requires the
   `claude` CLI, the plugin, and skills under `~/.claude/skills`; the grill
   technique text (`grilling`) is installed only on the Claude side and
   mirrored across.

Codex now offers what the hybrid design borrowed from Claude: in-session
subagents (`spawn_agent` / `wait_agent` / `send_input` / `close_agent`, agents
declared in `.codex/agents/*.toml`), lifecycle hooks for `PreToolUse`,
`PostToolUse`, `PreCompact`, `UserPromptSubmit`, `SubagentStart` and
`SubagentStop` with the same deny contract, a human-switched plan mode that
hooks can see as `permission_mode: plan`, and a structured
`request_user_input` tool inside plan mode. The harness can therefore be
Codex-native without a second process launcher and without losing a gate.

## Behaviour

The `.factory` artifact contract, every recorder, every schema, and every
gate stay identical. What changes is how a Codex session reaches them.

### Runtime is a machine fact, not policy

- `forge` resolves the coordinating runtime once: `FORGE_RUNTIME` env, then
  the value the SessionStart hook recorded in `.factory/run.json`, then
  install detection (companion present → `claude`; otherwise `codex`).
  `harness.yaml` gains no runtime key; both adapters stay vendored in every
  repo, and `check_dual_runtime.py` keeps its path-parity checks.
- codex-plugin-cc is needed only when Claude Code coordinates, because it is
  the only way a Claude session can reach Codex. A Codex-native session
  reaches Codex through its own hooks and subagents; the plugin is neither
  installed, resolved, nor mentioned on that path.

### Delegation is a ledgered subagent spawn, never `codex exec`

- Under Codex, `forge delegate <task-id>` composes the same brief, takes the
  same delegation lock, derives write access from stage state exactly as
  today, and records a delegation row with `backend: subagent`,
  `agent_type: implementer`, the model and effort, and the digest of the
  exact spawn message (`Execute .factory/briefs/<id>.md (sha256 …)`). It then
  prints the spawn contract for the session: `spawn_agent(agent_type=
  "implementer", fork_turns="none", message=…)`, then `wait_agent`, then
  `forge stage done`.
- `.codex/agents/` declares the executor roles the hybrid runtime reached
  through `/codex:rescue`: `implementer` (the implementation pin from
  `harness.yaml`, `workspace-write`), `explorer` (the exploration lane,
  read-only), `validator` (the hard-thinking lane, read-only), and `griller`
  (the grill mode pin, read-only). Role pins mirror `harness.yaml` and a test
  asserts they agree. The existing `planner-high`, `docs-decomposer` and
  `functional-checker` registrations stay.
- `SubagentStart` and `SubagentStop` hooks stamp the open delegation row with
  the runtime's own identifiers — `agent_id`, `turn_id`, transcript path,
  final status, the first 2 KB of the last message — replacing pid and
  process-token ledgering for this backend. `forge stage done` accepts a
  subagent row only when the hook stamped it, the message digest matches the
  current brief, and the launch succeeded; the companion row shape stays valid
  under Claude.
- The `PreToolUse` hook matches `spawn_agent`: spawning a write-sandbox role
  is denied unless an open subagent delegation row exists for the active
  stage and the message digest matches; forking history into a role agent is
  denied because the brief is the whole context. Read-only roles spawn freely.
  Raw `codex exec` stays denied everywhere.
- `forge codex status` and the board derive liveness for subagent rows from
  the row status and the transcript's modification time; companion jobs are
  still read when the plugin is present.
- Review is unchanged: `forge review <task-id>` already runs the autoreview
  skill from `~/.codex/skills` with Codex as the engine.

### Grills reach the human through `request_user_input`

- The Codex `PostToolUse` hook records a `request_user_input` call as the
  same `grill-round` artifact the Claude hook records for `AskUserQuestion`:
  each question, its option labels, and the chosen answer, with
  `generated_by: codex:plan-mode`. `record_grill_from_json.py` is unchanged;
  it matches question, options, and choice, not the source runtime.
- Because that tool exists only in Codex plan mode, spec, plan, and task
  grills run while the human has the session in `/plan` — the same posture
  the Claude flow already requires. `forge next` and the SessionStart context
  say `/plan` where they say Shift+Tab today, and name the `explorer` and
  `validator` roles where they name `/codex:rescue`.
- The cold-read grill spawns `griller` instead of launching the companion; its
  findings return as the subagent's last message and the coordinator records
  the gate through the ledger-matched recorder exactly as now.
- If a Codex build does not surface `request_user_input` to `PostToolUse`,
  the fallback keeps the answer human-originated: `forge grill ask` writes a
  pending round, and the `UserPromptSubmit` hook closes it with the human's
  next prompt. The agent cannot self-answer either way.

### The write lock covers every Codex write shape

- `.codex/hooks.json` registers `PreToolUse` for `Bash`,
  `apply_patch|Edit|Write` and `spawn_agent`; `PostToolUse` for
  `apply_patch|Edit|Write|request_user_input`; plus `PreCompact`,
  `SubagentStart`, `SubagentStop`, and `UserPromptSubmit`. The feature flag
  is the canonical `hooks` key.
- `pre_tool_use.py` reads `apply_patch` targets from the patch headers
  (`*** Add File`, `*** Update File`, `*** Delete File`, `*** Move to`) so
  product and canon paths are denied under the planning lock and the strict
  role split with the same messages, and allowed inside the same windows.
- `check_dual_runtime.py` drops the stale "Codex has no PostToolUse or
  PreCompact" exemption and compares matchers as well as events, allowing
  only the subagent events to be Codex-only.
- Codex plan mode is enforced at the prompt level, not by a sandbox; the
  hook remains the real enforcement, as it already is for Claude.

### Machine readiness is per runtime

- `forge doctor` and the SessionStart fast check branch on the resolved
  runtime. Under Codex the required set is git, Python, psutil, the Codex CLI
  at or above the floor with a valid login, `~/.codex/skills/{autoreview,
  grilling, ponytail}`, the `.codex/agents` roles, and `multi_agent` plus
  `hooks` enabled; the `claude` CLI, codex-plugin-cc, gstack and node become
  optional. `--fix` installs `grill-me` and `grilling` into `~/.codex/skills`
  directly instead of mirroring from `~/.claude`.

### Dev experience does not change

- Setup is `git clone … && ./setup`, then open `codex` in the clone and say
  "set up my machine" or "Set up a new KnackLabs project called X"; the
  bootstrap skills already install into `~/.codex/skills`.
- Every sentence in the README's "You say" column keeps working; "what now?"
  answers with the Codex form of each step.
- Parallel stories stay one worktree per story: one Codex thread per worktree
  (the Codex app's per-thread worktrees or one CLI per `../repo-KEY`), so the
  sandbox root is always the worktree.
- `harness.yaml` names `plan-mode` as the planning owner for both runtimes,
  names the `explorer` and `validator` roles beside the `/codex:rescue` form,
  and pins `codex:implementer` as the implementation owner. The
  `grill-round`, `plan-mode-marker` and `decomposition` schemas admit
  `codex:plan-mode`.
- Decision 0011 (the orchestrating Claude session runs autoreview directly)
  is superseded by the rule the shipped `forge review` already implements and
  decision 0049 states: review is one Codex-run three-lens pass per task under
  either coordinator.

## Acceptance criteria

- On a machine with only the Codex CLI installed, `forge doctor` reports
  ready with the `claude` CLI, codex-plugin-cc and gstack listed as optional,
  and the SessionStart context does not say the machine is not ready.
- In a Codex session with no approved plan, an `apply_patch`, `Edit` or
  `Write` to a product or canon path is denied with the same message the
  Claude adapter gives; the same write inside an open quickfix, lite or
  degraded window is allowed.
- `forge delegate <task-id>` under Codex takes the delegation lock, records
  a `backend: subagent` row with the spawn message digest, and prints the
  spawn contract; it never launches a process and never mentions
  `codex exec`.
- Spawning the `implementer` role without an open delegation row, with a
  different message, or with a forked history is denied by the hook;
  spawning `explorer`, `validator` or `griller` is allowed at any time.
- After `SubagentStart` and `SubagentStop` stamp the row, `forge codex
  status` and the board show the run and its liveness, and `forge stage done`
  accepts the row as the stage's write launch; a row without the hook stamps
  or with a stale digest is refused.
- A `request_user_input` call in Codex plan mode produces a `grill-round`
  record that `record_grill_from_json.py --gate spec|plan|task` accepts when
  the payload's rounds match it, and refuses when they do not.
- `forge grill run` under Codex spawns `griller` read-only and never takes
  the delegation lock.
- `.codex/hooks.json` and `.claude/settings.json` pass the updated parity
  check, `check_dual_runtime.py` and `verify.py` are green, and the gate
  tests cover apply_patch deny/allow, spawn deny/allow, and the Codex grill
  round.
- The role TOML pins equal the `harness.yaml` implementation, exploration,
  validation and grill pins, asserted by a test.
- `forge next`, the SessionStart context, AGENTS.md, WORKFLOW.md,
  docs/FACTORY.md, docs/degraded-mode.md, docs/getting-started.md and the
  README describe the Codex-native path; getting-started no longer says
  degraded mode uses raw `codex exec`; the README no longer calls the
  Codex-only runtime planned.
- Under Claude nothing changes: the companion argv digest, the status
  source, and the existing gate tests pass untouched.

## Boundaries

- No `codex exec`, no MCP servers, no Codex multi-agent replacement for the
  ledgered `forge delegate` launch (decision 0018 stands, one level up).
- No new workflow mode; Full, Lite and degraded are unchanged.
- The model never switches itself into plan mode; the hook's refusal asks
  the human to press `/plan`, as it asks for Shift+Tab today.
- Both adapters stay vendored in every repo; a client repo without Claude
  keeps the thin `.claude/` so path parity holds.
- Named custom agents are not spawnable from app-server or MCP-backed Codex
  sessions (openai/codex#15250); the CLI and the Codex app thread are the
  supported surfaces.

## Decomposition (epic → stories)

1. **FORGE-CDX-0 — hook contract probe** — a scratch-repo logging
   `hooks.json` settles whether hooks fire inside subagent threads with
   `agent_id`, whether `PostToolUse` fires for `request_user_input` and its
   payload shape, and the exact `spawn_agent` input keys; findings recorded
   in `docs/memory/codex-hook-contract.md`.
2. **FORGE-CDX-1 — delegation by subagent** — role TOMLs, the `subagent`
   backend in `forge delegate`, the `SubagentStart`/`SubagentStop` hooks,
   the `spawn_agent` gate, `stage done` acceptance, `forge codex status` and
   board liveness.
3. **FORGE-CDX-2 — gate parity for every Codex write shape** — hook
   registrations, `apply_patch` parsing, the linter's matcher-level parity,
   gate tests.
4. **FORGE-CDX-3 — grill provenance through `request_user_input`** — the
   `PostToolUse` mapping, schema generators, the `griller` cold read, the
   `UserPromptSubmit` fallback, runtime-aware `forge next` wording.
5. **FORGE-CDX-4 — doctor and skills per runtime** — per-runtime required
   sets, direct `~/.codex/skills` installs, the runtime resolver.
6. **FORGE-CDX-5 — canon, schemas, prose, decisions** — `harness.yaml`,
   AGENTS.md, WORKFLOW.md, FACTORY.md, degraded-mode.md, getting-started.md,
   forge.md, README, the vendor manifest, superseding 0011 and accepting
   0049.
