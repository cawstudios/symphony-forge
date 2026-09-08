---
status: proposed
confirmed_by: ""
date: 2026-09-07
stories: []
---

# Codex-native runtime: subagent delegation, plan-mode grills, per-runtime doctor

## Context

The README promises a Codex-only runtime "on the same artifact contract",
but every Codex release in the hybrid design goes through a Claude Code
plugin: `forge delegate` and `forge grill run` resolve the codex-plugin-cc
companion from `~/.claude/plugins` and pin its node launch argv,
`forge codex status` reads the plugin's job registry, and every grill
gate is ledger-matched against `AskUserQuestion` records that only Claude's
`PostToolUse` hook writes. `forge doctor` hard-requires the `claude` CLI.
A machine with only the Codex CLI cannot delegate, grill, or ship.

Codex now provides the pieces the hybrid design borrowed from Claude:
in-session subagents declared in `.codex/agents/*.toml` and driven by
`spawn_agent` / `wait_agent` / `send_input` / `close_agent`; lifecycle hooks
for `PreToolUse`, `PostToolUse`, `PreCompact`, `UserPromptSubmit`,
`SubagentStart` and `SubagentStop` with the same deny contract; a
human-switched plan mode hooks see as `permission_mode: plan`; and a
structured `request_user_input` tool inside plan mode. The operator's
direction (2026-09-07): use Codex alone with no loss of workflow or
features, never shell out to `codex exec` from a running Codex session, use
Codex's own user-input tool for grills, and accept that only the human can
switch Codex into plan mode. Spec: `docs/specs/codex-native-runtime.md`.

## Decision

**The coordinating runtime is a machine fact, resolved by `forge`, and the
`.factory` contract, recorders, schemas and gates are identical under
either.** codex-plugin-cc is needed only when Claude Code coordinates; a
Codex-native session uses Codex hooks and subagents only. Under Codex:

- **Delegation is a ledgered subagent spawn.** `forge delegate` composes the
  same brief, takes the same lock, derives write access from stage state,
  records a `backend: subagent` row carrying the digest of the exact spawn
  message, and prints the spawn contract; the `SubagentStart` and
  `SubagentStop` hooks stamp the row with the runtime's own identifiers, and
  `forge stage done` accepts only a hook-stamped row whose digest matches
  the current brief. The `PreToolUse` hook denies spawning a write-sandbox
  role without such a row. Raw `codex exec` stays denied everywhere.
- **Grill rounds are recorded from `request_user_input`** by the Codex
  `PostToolUse` hook as the same `grill-round` artifact, `generated_by:
  codex:plan-mode`; the ledger-matched recorder is unchanged. Grills run in
  `/plan`, the posture the Claude flow already requires.
- **The write lock covers every Codex write shape**: `apply_patch`, `Edit`,
  `Write`, `Bash` and `spawn_agent`, with the same messages and windows.
- **Machine readiness is per runtime**: under Codex the `claude` CLI,
  codex-plugin-cc and gstack are optional; required skills install into
  `~/.codex/skills` directly.
- Decision 0011's wording (the orchestrating Claude session runs autoreview
  directly) is superseded by what `forge review` already implements and
  decision 0049 states: one Codex-run three-lens pass per task under either
  coordinator. That supersession is recorded when a human confirms it.

## Consequences

- Decision 0018 stands one level up: the pinned launch is the spawn
  message digest plus the hook-stamped `agent_id` instead of a process argv
  and pid. Companion rows keep their shape, so Claude machines change
  nothing.
- `check_dual_runtime.py` loses the stale "Codex has no `PostToolUse` or
  `PreCompact`" exemption and compares hook matchers, not only events.
- `harness.yaml` names `plan-mode` as the planning owner for both runtimes
  and `codex:implementer` as the implementation owner; the `grill-round`,
  `plan-mode-marker` and `decomposition` schemas admit `codex:plan-mode`.
- Codex plan mode is prompt-level, not sandboxed, so the hook remains the
  real enforcement, as it already is for Claude. The model never switches
  modes itself; refusals ask the human to press `/plan`.
- Named custom agents are not spawnable from app-server or MCP-backed Codex
  sessions (openai/codex#15250); the CLI and the Codex app thread are the
  supported surfaces. A hook-contract probe (story FORGE-CDX-0) pins whether
  hooks fire inside subagent threads and whether `PostToolUse` fires for
  `request_user_input`; a `forge grill ask` + `UserPromptSubmit` fallback
  keeps answers human-originated if it does not.
- Parallel stories stay one Codex thread per worktree; no MCP servers, no
  new workflow mode, and both adapters stay vendored in every repo.
