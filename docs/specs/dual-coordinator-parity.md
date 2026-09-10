---
slug: dual-coordinator-parity
title: Either Claude or Codex can coordinate the same Forge workflow
status: confirmed
saved: 2026-09-10T03:20:36+00:00
---

# Either Claude or Codex can coordinate the same Forge workflow

## What changed in this revision

Compared with confirmed `fb7ac63` (event `7b5cf1e91877458c8a2f3751a5476771`), this revision adds accepted0063's first-task ordering rule. Frontmatter and confirmation records identify its current state; earlier approvals remain preserved.

- **Start the first workspace through the existing command:** [Bootstrap task preparation](#canonical-behavior-and-changed-surfaces) applies0063 only to the first native foreground support task: genuinely review and approve its preliminary contract in the planning checkout, create its owned worktree with the existing task-start command, then freshly ground and approve its detailed target contract before stage start or writes. Workspace-first planning remains the delivered behavior under0059.
- **Publish approved planning documents before code tasks:** [Bootstrap handoff](#ownership-upgrade-and-dogfood-handoff) permits a bounded, independently reviewed planning-document PR carrying approved canon without an implementation claim or task marker. Code tasks still own complete prepared changes and all normal proof gates.
- **Close the handoff gaps:** [AC11](#acceptance-criteria) covers both planning passes, refusal cases and successor workspace creation. [Handoff semantics](#exact-handoff-semantics) specifies marker-free draft commands, retries and truthful standing approval. Earlier bootstrap `--trunk` instructions are historical only.
- **Retain the accepted delivery requirements:** All twelve acceptance criteria, Luna/max policy, review limits, staged quality activation, exact question provenance and six native platform cells remain required. This transition adds no writer exception, alternate runtime-source mechanism, proof transfer or Claude fallback.

## Why

Developers should be able to choose Claude Code with its Codex rescue/companion plugin, or Codex CLI/Desktop alone, as the interface to Symphony Forge. All existing execution roles remain Codex. Choosing the coordinator must not change approvals, worker policy, evidence or shipping gates.

The original Codex adapter lacked the human-answer provenance required by the grill gates, and delegation/setup assumed Claude plugin state. The user explicitly directed native Codex bootstrap on 2026-09-07. The prepared candidate changes are pre-stage work, not normal approved-task proof. All further normal implementation uses the existing approved delegation route; this history creates no additional coordinator write permission.

## Behaviour

This specification defines the target of the story and its bounded delivery tasks. The remaining code gaps
named below are implementation requirements; they are not claims that those
behaviors have already passed. Spec handoff requires defined behavior and
resolved policy conflicts; release additionally requires the actual proof.

- Both coordinators use the same Forge phase engine, approved contracts, recorders and protected authority. Their adapters only translate runtime events and launch mechanisms.
- Claude retains its existing rescue/companion integration. Codex operates without Claude or its plugin installed.
- Worker defaults follow accepted Decision0062: Luna/max for read-only exploration and routine implementation. Independent cold reads/reviews, implementer-owned tests, conditional functional QA, modes and failure semantics remain in force; the other phase and specialist settings retain their own authority.
- Required human decisions and approvals use the actual host's permitted interface; in Codex Default, main asks directly in ordinary chat. Optional structured answers from either runtime retain truthful provenance and exact matching. All six grill gates retain freshness, resolved findings and explicit empty-frontier checks, with eligibility and single-use consumption for structured rounds actually used. No human-round minimum or invented closing question remains. An unanswered or canceled question, an empty round list and a passing technical grill are not approval.
- Coordinator product/canon edits remain locked under the existing write policy; planning/docs, recorder-mediated evidence, prototypes and Git operations retain their existing exceptions. Legitimate delegated workers remain admitted; native hook activation must not block existing companion workers or rely on disabling hooks.
- Native execution retains the same brief/task/stage binding, derived write permission, sandbox requirements, process lifecycle, recovery, status and proof requirements as the existing route.
- Setup, init, adopt and upgrade deliver the supported routes while preserving client settings and historical proof. Setup uses an explicit coordinator choice, then the detected interface; if neither identifies it, interactive setup asks. Unattended setup requires a detectable choice or `--coordinator claude|codex` / `FORGE_COORDINATOR` and explains the missing choice before dependency installation.
- Prepared native bootstrap changes remain distinct from task contribution. Keep every unanswered Claude question canceled. Normal task execution requires the existing approvals, registered worker admission and task-bound proof; bootstrap bytes are not a passing gate or task marker.
- A developer switches coordinators between completed tasks, with no active worker or unfinished question. Both choices use the same stored project artifacts; unfinished-task transfer is outside this capability.
- Plan authoring remains mode-agnostic. Prepare and present the saved revision, then obtain explicit acceptance in the host-permitted interface; Codex Default uses ordinary main chat for required approval. Use its synchronous question tool only for optional questions the host permits. Existing authorization persists for unchanged content; a changed approval-bound revision needs its own confirmation. No manual mode switch or repeated “continue” is required. Workflow status, a continuation reply and a mode change are not approvals.
- The native dogfood task must deliver real scoped work and complete its own human handover, delegation, verification and independent review for the review-only draft PR checkpoint. Full release additionally requires conditional functional QA and all normal shipping gates after every live-proof cell passes. Fixture-only tests do not constitute native end-to-end proof.
- Repair native parity defects through Codex within the authorized scope. Do not require a Claude session for native setup or recovery. Do not invent answers, manually write proof, or mislabel this bootstrap as a companion outage.

Setup is owned by `./setup`. Selection precedence is `--coordinator`, then
`FORGE_COORDINATOR`, then detected current interface, then an interactive
choice. Empty, canceled or EOF input refuses before any install or repair;
invalid explicit choices also refuse. The choice applies to that setup run
and is passed to both doctor invocations; it does not rewrite the user's
shell profile or create persistent coordinator state. Bootstrap skill files
may be delivered into both adapter directories under existing ownership rules;
choosing Codex does not install or start the Claude application or companion.

For setup detection, a nonempty `CODEX_THREAD_ID` or `CODEX_SHELL` identifies
Codex; a nonempty `CLAUDECODE` identifies Claude. When both families are present,
treat detection as ambiguous instead of guessing. With neither an explicit
choice nor one unambiguous detected interface, ask only when standard input is
a TTY. Otherwise refuse before repair and print both exact selectable commands:
`./setup --coordinator codex` and `./setup --coordinator claude`. The unattended
caller supplies its intended choice. Invalid explicit input never falls back.
This setup rule does not silently replace legacy defaults in unrelated callers.

`./setup` is the existing POSIX entrypoint. Native Windows retains the existing
`forge.cmd` bootstrap documented in `docs/windows.md`; no Git Bash installation
is assumed before that launcher runs. Choose the coordinator explicitly in
`forge.cmd doctor --fix --coordinator codex` (or `claude`), then verify with
`forge.cmd doctor --coordinator codex` using that same choice. FORGE-COORD-1.1 updates
the Windows instructions alongside the POSIX setup guidance; it does not add
a second bootstrap launcher or change Windows user-scope prerequisite repair.

### Presenting revisions for a decision

For both coordinators, before each spec, story-plan or task-plan approval question:

1. Save the current artifact as a draft through its existing workflow. Identify the exact current revision and the last user-confirmed revision. Immediately after each actual confirmation, preserve the confirmed artifact in Git and record its artifact path, commit and existing body digest through the existing Forge scratchpad note command before subsequent edits. The note is only a convenience pointer: recover independently from the existing committed spec-confirmed event and artifact in the same Git history, or the existing story/task approval artifact and its committed plan. Commit those existing records with the confirmed artifact before later edits. Never make scratchpad retention the authority or guess from mutable status or timestamps. If no confirmation exists, label it as the first review; if confirmation is known but its baseline cannot be recovered, report that gap instead of calling it a first review.
2. Update a short “What changed in this revision” section near the beginning. Explain each substantive change in plain English and link to every affected section. Show the diff against the last user-confirmed revision alongside the full current artifact; a summary alone does not replace the artifact. On the first review, show the complete artifact without inventing a comparison baseline.
3. Open or refresh the reader in the user's main conversation and inspect its actual displayed content against the saved revision, including the changed sections. An open request that is queued, failed, stale or for a different task is not successful presentation. Retry through available supported capabilities. In an interface without a reader, present the artifact and changed passages directly in the main conversation. A bare file link is not proof that the artifact is displayed. Issue the question only after presentation succeeds.
4. Ask for explicit approval through the host's permitted interface, identifying the same revision and its change summary. In Codex Default, ask directly in ordinary main chat, not through the optional question tool. Spec confirmation requires the existing fresh spec grill and the human's actual confirmation of that revision before running `forge spec confirm`; a technical “no gaps” answer or empty grill-round list alone does not imply it. Reuse explicit confirmation already given for the same revision instead of asking again. Story and task plans retain their existing approval commands and prerequisites. Keep dependent work pending until the required answer, record it through the existing decision/artifact-approval commands, then continue automatically. Do not create a tool event from chat or require an optional tool answer before approval. Any further approval-bound content change repeats presentation and the existing fresh grill/approval requirements.

The canonical procedure lives in factory/skills/forge.md; both runtime entrypoints, docs/native-coordinator.md and AGENTS.md carry concise pointers. Approved support tasks own its delivery, and FORGE-COORD-1.1 verifies the integrated behavior. Reuse the current reader, Git diff and scratchpad; add no display-receipt schema, approval registry or claim that instruction text mechanically certifies Desktop delivery. Review the ordered workflow and exercise current, queued, stale and unavailable-reader cases in the existing runtime dogfood report. A queued or stale reader must not be followed by an approval question; a supported fallback must display the actual content first.

### Canonical behavior and changed surfaces

The baseline is the current accepted decision corpus, not older runtime-specific
prose. Decision0050 keeps plan authoring mode-agnostic;0051 as amended by0061
requires all six grill gates to resolve findings and explicitly attest an empty
frontier, retaining exact provenance and single-use consumption for structured
rounds actually used without a compulsory human round. Decision0052 retains its
autonomous approval-to-PR loop. Accepted0059 amends only obsolete sequential,
single-frontier and pre-worktree-JIT clauses in0007/0018/0021/0032/0044/0047.
Task worktrees, scoped admission, approvals, proof and marker-on-trunk handoff
remain required. Accepted0061 amends the compulsory human-round, synchronous-only and manual-mode-switch clauses of0048/0051/0053/0054/0057/0059. Its explicit Decision paragraph on unanswered optional questions also governs the inconsistent blanket pause in0057: only work depending on a required answer waits; independent work supported by existing facts continues.
Reconcile those obsolete instructions and the gate implementation while retaining
every other accepted approval, admission, proof and shipping requirement.

Main completes story planning, independent story grilling, approval and the
frozen decomposition. Create or attach a dependency-ready task worktree before
that task's detailed plan or grill exists. Require the approved story, matching
decomposition, correct story/task identity, refreshed exact trunk baseline and
every effective dependency's marker on trunk. Normal attachment accepts only a
clean, unowned, registered worktree sharing the same Git common directory;
validate before hydration and publish ownership last. A verified retry returns
the existing owner without resetting it or creating a duplicate. The task waits
for ownership before phase discovery. Creation or attachment grants no product
write authority; stage start and delegation still require the full JIT contract,
task plan, fresh grill, approval and admission.

The task owns JIT authoring, its independent grill, implementation, tests,
verification, the existing autoreview/fix loop, PR and green CI. Main presents
its exact artifacts and asks all human questions. Codex Desktop uses one
authorized app task for each owner; CLI uses available local coordination
capabilities without requiring Desktop controls. Claude remains one coordinator
managing the same task workspaces and Codex companion workers. Native Plan mode
is optional, not a prerequisite to this ownership split.

Preserve current dependency semantics: omitted or empty dependencies follow the
immediate predecessor; a nonempty explicit list names the dependencies.
Dependency-ready tasks may run concurrently only in distinct worktrees with
disjoint protected scopes. The approved IDs, order and dependency graph remain
frozen. A task enriches only its own permitted execution fields; sibling and
completed contracts are not rewritten. Read progress from verified owners by
story plus task identity, including tasks still planning. After actual trunk
integration, refresh non-own rows from the incorporated trunk while retaining
the owner's contract, approvals and stage baseline, then perform the existing
verification and review. Unmerged sibling work never becomes completed evidence
in another task PR. Missing or conflicting ownership refuses without overwriting
unrelated state; recovery reuses existing records rather than a new registry.

Accepted0058 permits only explicitly scoped native bootstrap support tasks to
use the existing isolated candidate instead of the normal trunk start. Validate
their exact scopes, target preparation, baselines and complete review boundaries
before implementation. Preserve actual dependency markers and sequential merges
for those bootstrap tasks;0059 does not turn their dirty candidate into a normal
attachment target. Neither decision approves a story/task plan or proves that a
proposed preparation route works. Accepted0063 additionally permits only the
first native foreground bootstrap task to use the existing pre-workspace
contract/grill/approval sequence needed by `task start`. Its detailed contract
is then completed, freshly grounded, grilled and approved in the real target
before stage start and native delegation. This temporary ordering rule grants
no product-write authority and does not replace the delivered0059 workflow.

Accepted Decision 0053 amends the coordinator and transport wording of
0037/0018, the literal Claude coordinator wording of 0011, and the Claude-only
recording consequence of 0051. The corresponding
product brief, AGENTS/Claude adapter, WORKFLOW, shared Forge skill, griller and
planner prompts, `docs/native-coordinator.md` (including free-text and mode guidance),
harness routing descriptions, hook registrations, hook event
normalization, schemas and parity checks are explicitly changed surfaces.
The six underlying handover requirements and independent check ownership stay.

Accepted Decision0054 records the user's selected task-scoped proof policy:
verify, automated tests, all three review lenses and conditional functional
proof are required for each task before normal task PR readiness;
story closeout consumes shipped task proof. It amends the older once-per-story
timing in Decisions0001/0007 and 0047 while preserving stage-local certification,
review ownership and fix/review-until-clean. Proposed Decision0049 is not accepted.

### Native runtime and human-answer contract

The native coordinator surfaces are local Codex CLI and local Codex Desktop;
remote/cloud-hosted Codex is not added by this capability. The current candidate
CLI baseline is 0.153.4. Desktop readiness is checked against its actual bundled
runtime, not inferred from the separately installed CLI version. The platform
release scope preserves every platform already supported by Symphony, as the
requested implementation plan requires. This statement does not claim a
completed native question event.

The release checklist has six native surface/OS cells: CLI and Desktop each
on macOS, Linux and native Windows. WSL2 remains the documented Windows
fallback and does not substitute for native Windows proof. Each cell needs
its actual runtime version, checkout and trusted hook source, a real submitted
question with matching session/tool/question/event identities, startup/resume/
compaction observations, denied coordinator write and admitted worker proof.
Retain these observations in the existing task test record and referenced
runtime logs; use the existing schema recorder, not a new evidence family.
An unavailable host or missing capability leaves that cell unverified and
blocks a full-parity release claim. This matrix preserves the selected platform
scope; it is not a claim that the candidate has passed those checks.
Current upstream platform references: [desktop](https://learn.chatgpt.com/docs/app)
and [CLI](https://learn.chatgpt.com/docs/codex/cli), checked 2026-09-07. The
current [Linux desktop preview documentation](https://learn.chatgpt.com/docs/linux/linux-app)
explicitly includes Codex; availability is not proof that its Forge hooks work.

Readiness requires working SessionStart (including resume/clear/compact), PreToolUse,
PostToolUse, PreCompact and Stop behavior for the relevant tools. Doctor checks
the selected coordinator's CLI prerequisites and trusted/enabled hook
registrations. Its PATH CLI probe cannot certify Desktop delivery; the
separate Desktop session check below owns that observation. Unsupported runtimes
refuse with the missing capability; they do not silently skip a gate. Live
proof must capture actual synchronous native question input and completed
output, not merely demonstrate that a generic function-tool hook exists.

In Codex Default, main asks necessary decisions and approvals directly in
ordinary chat. Existing decision, spec, story-plan and task-approval commands
record the actual human confirmation against the identified revision; they do
not require a question-tool event. Use synchronous `request_user_input` only for
optional questions the host permits. An unanswered optional question cannot block
work that can proceed from existing facts and grants no permission. Forge adds
no chat collector, parallel approval ledger, host-instruction override or private
host patch. The six-cell release observations below still include real permitted
structured-question delivery; missing that proof does not make the optional tool
a prerequisite to an otherwise valid artifact approval.

For structured rounds actually used, Codex's stable
question IDs and returned answer arrays are normalized to the shared
question/options/chosen representation, where chosen is the exact submitted
answer string for either an offered option or free text. Claude keeps AskUserQuestion and its
existing human interface. A submitted single nonempty, non-whitespace answer can satisfy a new certified round,
whether it selects an offered option or contains free text. Preserve the exact
submitted text; do not coerce it to an option label. Exact event, question and
answer matching and single-use consumption remain required. Recording a free-text
answer does not itself approve a plan. Empty/canceled results, asynchronous
issuance acknowledgments and request-cleanup notifications cannot certify a
round. General asynchronous conversation remains available outside that proof
path; its initial acknowledgment is never a human answer.

For a structured round, the certifying input is the completed PostToolUse hook
payload, not the raw
App Server notification. For native Codex, the adapter reads questions from
`tool_input.questions` and the submitted choice from
`tool_response.answers[question_id].answers`, with session and tool-call
identity from the hook envelope. `item/tool/requestUserInput` describes the
upstream UI request; the runtime delivers its completed tool input/result to
the hook. `serverRequest/resolved`, cancellation/error results, and empty or
multiple answers cannot substitute for that completion. CLI and Desktop
must each demonstrate this mapping with an actual completed event. Claude
keeps the existing AskUserQuestion mapping in `post_tool_use.py`.

New structured round records carry truthful runtime, session, tool-call and question
identity, plus turn identity when the runtime supplies it. They target the existing story/ceremony context,
and are idempotent for the same completed runtime event. A new recorder claim
must identify an available matching answered round; the same recorded response
cannot authorize a second gate. Repeated wording in a newly answered question
is a distinct event, not an authorization to reuse the old response. Existing
completed grill artifacts remain valid without rewriting history. Unanswered
legacy ledger entries cannot be promoted into new certified answers; obtain a
real new answer instead. This closes the current matcher's `chosen: null`
wildcard when recording new proof, equally for both coordinators.

New event-bearing records capture the active story in an optional `story`
field; its absence means the question was asked before a story was active.
Requirements, plan and task gates require an exact active-story match.
Project-wide spec, signoff and epics gates accept pre-story records or records
from the currently active story, and refuse records bound to another story.
Malformed story identities refuse. Historical eventless Claude records retain
their existing interpretation. Existing event-bearing records without a story
are root-context records and cannot certify a story-specific gate. No age limit
or new ceremony system is introduced.

The trust model remains the existing trusted-command model shared with Claude;
the ledger is not cryptographic runtime attestation. Live support requires an
observed native question/answer and its matching completed hook record, with
the runtime, checkout, session, tool-call and question identities retained for
review. Handcrafted fixture payloads prove parser behavior, not human input.

### Worker admission and native lifecycle

Forge remains the sole launcher and authority owner. Both routes use the
existing Forge commands for implementation, exploration and certifying grills;
the native adapter runs launcher-owned Codex processes and reuses the protected
Git-control ledger, locks, stage/brief digests and process cleanup. Direct native
subagent writer or certifying-griller transport is deferred. Optional native
explorer/validator helpers are read-only advisory assistance; they neither grant
writes nor replace a required Forge launch or independent grill. Do not ship
unused native implementer/griller presets for that deferred transport.

Resolve model and effort through the existing harness helpers and accepted0062:
read-only exploration and routine implementation use Luna/max; validation
remains Sol/xhigh and cold-read grilling remains Terra/xhigh. A different model
for a difficult task is an explicit choice, not an automatic retry. The proposed
POLICY allocation owns integration of the prepared defaults, supported effort
parsing, focused regression coverage and live instructions through its normal
approved task; preparation alone does not activate those settings. Optional read-only presets define roles and
sandboxes, omit model/effort overrides, and receive both resolved values at
explicit dispatch. Installing a preset does not invoke it. Autoreview retains
its existing independent procedure and settings.

An admitted worker is bound to the protected launch ID, live process identity,
target worktree, stage incarnation,
task contract, brief and derived write scope. The coordinator cannot gain
that admission by setting an environment variable or claiming a role. A launch
starts unadmitted; tool execution waits for completed registration. Registration
failure or timeout grants no writes. Cancellation revokes admission before
process cleanup; failed cleanup retains revocation. Completion, failure or stage
closure also revokes admission. Runtime session identity, when emitted, is
retained for launch correlation and read-only conversation recovery; it is not
a substitute for process-bound admission. Resuming stored conversation requires a fresh Forge
preflight and launch; history does not revive an old grant. Existing companion
workers must still pass admission when native coordinator hooks are enabled.

Both adapters produce the same starting/running/terminal lifecycle through
the shared launcher. Stage close validates the precise invocation for the
recorded transport as well as the existing scope and proof checks. Native
progress, session identity and logs belong to that launch; status and recovery
read the launch's transport identity rather than assume a Claude registry.
Read-only exploration can start without a write stage and cannot satisfy a
write-launch requirement. A background command acknowledges success only after
protected registration; acknowledged detached readers remain observable and
cancelable. Before registration, the starting command owns startup failure and
timeout cleanup and grants no write authority.
Dead-worker reconciliation retains the existing PID identity, reaping and
retry safeguards; uncertain live authority blocks conflicting launches.
A failure before process creation, including dependency or process-discovery
failure, must publish a failed launch without an invented PID or exit code.
Once a process exists, verified cleanup still precedes terminal publication.
Accepted0060 retains the existing POSIX child signal-mask restoration during
atomic registration, including its narrow preexec_fn use, with platform guards
and Windows behavior unchanged. It amends only0042's blanket removal wording;
psutil identity and cleanup remain authoritative. Add no unrelated child callback
work or replacement process framework. Both adapters must independently retain every
mandatory hook and its correct handler; deleting the same protection from
both adapters cannot make structural validation pass.

### Ownership, upgrade and dogfood handoff

Both adapter directories continue to be vendored even in Codex-only projects;
an inert `.claude` adapter directory is not a dependency on the Claude runtime
or plugin. Existing scaffold ownership lists remain authoritative. `COPY_CODEX` owns
`.codex/config.toml`, `.codex/explore.config.toml` and `.codex/hooks.json`;
client-added runtime files remain client-owned. Preserve current preflight and
replacement semantics for owned files, and test preservation of unowned files
at their real delivered destinations. The existing `GATE_FILES` inclusion of
`.codex/hooks.json` remains, consistent with Decision0041 and the live
vendor-integrity checker. Doctor and the independent structural check
add hook-health checks without replacing or weakening vendor integrity. Added
runtime adapters are Forge-owned entries in those lists; existing unowned
client skills, agents and local settings remain project-owned. Upgrade retains
its existing conflict and preservation behavior, updates vendor hashes only for
changed hash-controlled owned files, and does not rewrite historical evidence.
`.codex/config.toml` remains outside `GATE_FILES`, as Decision0041 requires;
Forge ownership alone does not make a file hash-controlled. Any necessary
new ownership conflict must be reported before writes, not silently resolved
by deleting client configuration.

The proposed native dogfood outcome is complete coordinator parity. A separate
fresh `/tmp` Task tracker client exercises the installed harness, with its own
origin, meaningful CI and normal confirmed-spec/story/task lifecycle. Main
arranges that client and keeps its human decisions in the main conversation;
its task owner delivers a real admitted contribution, tests/verification,
autoreview, required UI functional proof and a task PR with green CI. Reference
its actual repository, PR and logs from integration evidence; client work is not
harness-task contribution. Under
accepted0058, complete, independently reviewed support PRs may precede the final
parity integration task. Bind each prepared change and remaining repair to its
actual approved support-task review or final complete activation review; do not
ship omitted or partially reviewed bytes. The final parity task retains composed
lifecycle coverage for native questions, approval, delegated writes and task
proof against the integrated result. Exact ownership of setup, story-context,
mandatory-hook and pre-spawn repairs must be validated and approved in the
revised story/task contracts before implementation. It reuses existing fixtures and shared policy. Existing
bootstrap code and focused init/adopt/upgrade tests are
declared pre-stage work, not attributed to that later worker.
The Forge parity-integration leaf is `user_facing: false` under the current
per-task definition in factory/prompts/planner.md because it builds no UI
components. This does not describe the separate Task tracker client: its UI leaf
is `user_facing: true` and must record real functional proof. The aggregate
decomposition flag is distinct from each leaf flag. Native live-platform and
composed lifecycle evidence remain mandatory for the Forge integration leaf
regardless of that flag. Also test the conditional functional-checker gate with
a true-valued fixture; the fixture does not replace either real proof obligation.

The first native foreground support task uses only0063's real source contract,
grill and approval, followed by `forge task start`, exact bounded target
preparation and fresh target planning, grounding, grill and approval before
stage start or delegation. `forge stage start --trunk` is not an alternative
for this task. Earlier KERNEL or bootstrap drafts selecting that route are
obsolete execution instructions; retain their bytes solely as history.
Accepted0058 permits the preserved candidate, not a new preparation mechanism
or implicit activation permission. Support tasks retain registered delegated
writes, completion, verification, complete independent autoreview, normal task
PR gates, actual predecessor markers on main and sequential merge ordering.
The first admitted worker also delivers the minimal0059 workspace-creation
ordering repair so its successors can create their owned workspace before JIT.
The later TASKS owner retains attachment, owner reads, scheduling and full-journey
work. Diagnostics and source-bound proof never substitute for target proof.
Under0063, approved
specifications, decisions and roadmap records may first reach trunk in their
own bounded planning-document PR with complete independent document review.
That PR claims no implementation and carries no task-ready marker; it cannot
substitute for a support task's admitted contribution or proof. The following
review-only checkpoint concerns the final parity integration task. After approved delegation, verification and independent review, open the
review-only PR using the existing Git/GitHub draft operation against the actual
default branch. Missing live cells keep it draft and unmerged, without a task
marker. Only after complete clean proof may normal task readiness/sealing run;
its marker must reach refreshed trunk before story closeout.
The stage records pre-existing dirty bytes; unchanged bootstrap bytes cannot
satisfy its contribution requirement. Every committed path, including the
bootstrap, must fit the approved scope. The worker must contribute the real
remaining integration coverage and retain all verify/review/PR gates.

The supported switch is a coordinator-operated handoff using existing checks:

1. Run `./forge next` and inspect the existing task/stage state to confirm the
   previous task is complete and no stage is open. Finish that task's required
   proof and marker-on-main handoff before beginning the next task's rounds.
2. Run `./forge codex status`, resolve any live/recovering launch through its
   existing finish/cancel path, and wait for verified worker termination.
3. In the current interface, finish or cancel any pending structured question:
   Claude `AskUserQuestion` or Codex `request_user_input`.
   Completed-question records do not prove that another interface has no
   unanswered question; this check belongs to the coordinator's actual session.
4. Select the new coordinator, retain the same project artifacts, run
   `./forge next` there and begin the next task's normal human handoff.

FORGE-COORD-1.1 owns these instructions and exercises the handoff at a completed
fixture task boundary. Its lifecycle regressions retain existing refusals for
active-stage questions, conflicting/unregistered workers, and unanswered or
replayed approval claims. This is a workflow procedure under the existing
trusted-command model, not an automatic cross-session switch detector. A bare
environment-variable change selects a transport; it supplies no task approval,
worker admission or proof of a completed handoff. No persistent coordinator
registry or additional pending-question evidence system is introduced.

FORGE-COORD-1.1 owns final coordinator-parity integration. Separately approved
support tasks in the same story may own complete prepared-change reviews under
accepted0058; their exact allocations remain to be validated and approved.
Native write-hook activation and legitimate worker admission must land together
in their approved owning task. Separately approved predecessor tasks retain
accepted0055/0056 staged quality cleanup and final mandatory quality activation.

Before this handoff, no stage may be open, no launch may be live or recovering,
and no human interaction may be unfinished. Normal task workspaces are created
or safely attached at refreshed trunk under0059 before JIT planning, so that
route requires its enabling changes to land first. Only explicitly scoped accepted0058 bootstrap
support tasks may use the validated isolated-candidate starting exception;
actual predecessor markers on main and sequential merge ordering still apply.
Neither route treats diagnostics as task proof.

## Acceptance criteria

1. Required Codex Default decisions and approvals use ordinary main chat and existing revision-bound approval commands without a tool-round prerequisite. Real permitted Codex CLI/Desktop structured questions and submitted answers pass the same grill provenance checks as Claude. Cover pre-story, current-story, other-story, malformed-story and historical eventless records; missing, canceled, mismatched and replayed structured claims refuse. Test offered-option and free-text answers in both adapters; preserve exact submitted text and refuse whitespace-only or multiple answers. All six grills accept canonical top-level `frontier_empty: true` with empty or populated rounds, subject to existing finding-resolution and artifact/grounding-digest checks. Round-bearing payloads in the existing format omitting that field may retain final-round `frontier_empty: true`; explicit top-level false cannot be overridden by a round. Empty rounds without top-level true refuse. A technical pass is not approval. Question age alone is never a refusal and no expiry timer is added.
2. Both coordinators are denied direct locked writes while legitimate delegated workers can perform their approved work; registration timing, failed admission and expired/resumed authority are tested.
3. Codex-only launch, status, recovery and setup require no Claude installation or companion-plugin metadata, while the shipped inert Claude adapter and existing rescue route remain supported. Here “no Claude dependency” means no Claude executable/process, companion-plugin registry or Claude environment state is required. Static vendored .claude adapter/configuration files remain allowed and supported; their presence does not make native execution depend on Claude.
4. Worker model/effort selection and all existing downstream gates are independent of coordinator choice.
5. Startup, resume, clear, compaction and question/Stop interception execute through installed runtime registrations; removing a required registration makes parity validation fail.
6. At the review-only draft PR checkpoint, existing delegation, deterministic verification and independent source review run without fabricated evidence; incomplete platform proof remains explicit. Final parity-task readiness, marker, shipping and full-parity completion require all six live cells and all existing task/worktree and shipping checks to pass. Accepted0058 support tasks retain their own complete approved proof and normal PR gates; their shipment does not certify full parity or waive any required live proof in their scope. The six-cell live matrix certifies native Codex only; Claude retains its existing adapter/regression proof rather than a second six-cell live matrix.
7. After separately approved accepted0058 support tasks, Codex coordinates the bounded final integration task through the existing approved stage route to an unmerged review-only draft PR, retaining actual runtime proof through schema-validated recorders and identifying bootstrap work separately. This checkpoint grants no task-ready marker or shipping status; normal completion follows only after complete live proof.
8. `./setup` honors explicit/environment/detected/interactive selection and cancel/EOF refusal before installation, forwarding the selection through both doctor calls. Fresh, adopted and upgraded clients receive both adapters without losing project-owned configuration or invalidating existing evidence.

9. Both coordinators continue executable in-scope work after passing checks and resume automatically after a required human answer, without repeated “continue”. Optional unanswered questions do not block work supported by existing facts. The planned POLICY task introduces a new bounded optional `forge grill run --context-file <notes>` argument through the existing grill launcher so prior resolutions reach each required cold reader separately from the artifact and its unchanged digest contract. A supplied missing/unreadable context file refuses before launch. The context-file path is selected by the coordinator as a trusted command input and must resolve to a readable local UTF-8 file. Its contents are separately delimited, labeled untrusted, nonauthoritative hints beneath the trusted prompt, not executable instructions or authority. They cannot command actions or change scope. They supply prior resolutions and changes but cannot amend the authoritative artifact, decisions or user-approved scope and are not gate evidence. Preserve artifact identity/digest, finding-resolution and explicit empty-frontier checks, model policy and read-only launch authority. Settled decisions and explicitly planned implementation are not new human questions; real missing decisions and required approvals remain blockers and use the actual host's permitted interface. POLICY also repairs the existing material-shape `--reread` route: preserve the supplied nonblank reason verbatim in its generated, stored launch brief, bound by the existing launch brief path/hash and artifact identity. Refuse an explicitly blank or whitespace-only reason before launch; do not change the existing cap or permit the reason or context file to bypass it. Use existing launch artifacts, not a new ledger/schema. Required regressions prove reason recovery from the persisted brief, blank-reason refusal, second-read refusal without a reason and refusal beyond the existing cap. Contract C6 and its context-file/reread regressions verify these invariants.
10. Coordinator switching occurs only at a completed-task boundary with existing active-worker checks passing and an actual observation of no pending interface question recorded in the existing test report. Contract C7 lifecycle regressions cover allowed completed handoff and refused active-work/incomplete-proof cases; no cross-session question registry is introduced.

11. The presentation sequence in [Presenting revisions for a decision](#presenting-revisions-for-a-decision) is required for specs and both plan levels: show the current artifact, section-linked changes and comparison against the last user-confirmed revision before asking. The canonical Forge skill owns the shared procedure, with concise runtime/native-guide/AGENTS pointers. POLICY also reconciles obsolete sequential-task language in `docs/product/BRIEF.md`, `AGENTS.md` and the canonical `factory/skills/forge.md` with accepted0059, preserving disjoint scopes, separate task worktrees, dependency markers and all approval/admission gates. Main owns story planning, independent story grilling, frozen decomposition, scheduling and human questions. Each task owns JIT planning through its PR and green CI in a workspace created or safely attached under0059 before JIT; stage and write gates remain unchanged. For only the first native foreground task,0063 requires a complete source contract, independent grill and approval before task-start hydration, followed by a freshly grounded target contract, independent grill and approval before stage/delegation. Its acceptance includes refusal of a placeholder or incomplete source contract and refusal of source-bound proof after target preparation. The first admitted task repairs normal workspace-creation ordering for successors; subsequent TASKS work owns attachment and the remaining task journey. Exercise these transitions and refusals in task-start/stage/delegation regressions and the actual first native run. Verify story/task owner reads, retries, dependency-ready disjoint execution, task-only contract enrichment and safe trunk reconciliation. Preserve real returned handles and pending dispatches without duplicates, stable display titles and custom titles, existing scratchpad recovery and quiet child results. Approved support tasks deliver these changes and FORGE-COORD-1.1 verifies them together. Respect host question-tool restrictions and preserve the Claude route. No new registry or management framework is introduced.
12. Separately approved cleanup predecessors retain current verification and independent review during migration; final activation requires full authored-source/test coverage with pinned Ruff lint/format and Pyright, identical local/CI checks, missing-configuration and deliberate-violation refusals, and client-specific stack commands. No blanket suppression or review-limit bypass is permitted. This activated baseline must pass on the integrated parity result before parity ships.

### Parity contract labels

C1-C10 retain the following parity requirements, not external or already-approved
contracts. Accepted0058 permits bounded support-task allocation of prepared
changes; the revised story/task contracts must map exact ownership and evidence
before recording and approval. FORGE-COORD-1.1 verifies the complete integrated
result; support-task completion alone cannot close these parity requirements.

- **C1:** Setup selects explicit flag, environment, unambiguous detected runtime or TTY-only interactive choice in that order; ambiguous runtime detection without a TTY, cancellation, EOF and unknown unattended runs refuse before installation, and both doctor calls receive the same selection without a Claude dependency for Codex.
- **C2:** New Claude and Codex structured question events carry the actual story and exact event/question identities; story gates reject other-story or unbound new claims, project gates accept pre-story/current-story claims, and replay, cancellation and malformed claims fail while completed historical grills remain valid. Required Codex Default decisions and artifact approvals use ordinary main chat and the existing approval records; structured rounds are optional and no-round grill success grants no approval.
- **C3:** Each adapter independently requires the correct startup, question, compaction, write-policy and completion handlers, including SessionStart startup/resume/clear/compact on both Claude and Codex; deleting or replacing a handler or required source in either adapter or both together fails validation.
- **C4:** Native foreground and background startup failures before process creation terminate truthfully without a PID or exit code; registered workers retain scoped process-bound admission, verified cleanup, revocation, observable status and refusal of expired authority or incomplete output.
- **C5:** Init, adopt and upgrade deliver native assets through existing ownership and target-boundary checks, preserve client-owned settings and historical proof, and retain the working Claude companion route.
- **C6:** The planned POLICY task adds the bounded optional context-file argument through the existing grill launcher, carrying separately labeled untrusted context without changing artifact identity, finding-resolution and explicit empty-frontier checks or read-only authority. Reconcile the shared gate/recorder, generated brief and prompt wording under0061: one independent cold read, resolve facts and necessary human decisions, amend once and record against the amended artifact; no compulsory human round, forced closing question or clean-next-round instruction remains. Top-level `frontier_empty: true` is canonical for empty or populated rounds. Round-bearing payloads in the existing format omitting it may use final-round `frontier_empty: true`; explicit top-level false always refuses. Structured rounds actually used retain exact matching, eligibility and single-use consumption. A reasoned reread uses only the existing material-shape-change route and cap. POLICY preserves its exact nonblank reason in the existing stored launch brief and verifies recovery plus blank-reason, missing-reason second-read and cap refusals as specified in AC9; no new evidence family is added. `forge next` routes the active missing/draft spec before requirements, and shared instructions continue authorized work after answers and passing gates.
- **C7:** Composed lifecycle coverage verifies approved delegation, task-scoped tests/reviews, the conditional functional-check gate, completed-task handoff and active-worker refusal; unanswered or canceled questions cannot satisfy approvals. Before switching coordinators, the coordinator also observes that the actual interface has no pending question and records that observation in the existing test report.
- **C8:** A real native worker contribution after stage start and before stage done passes repository verification and the existing autoreview procedure, with all required CLI/Desktop platform observations recorded honestly before final parity-task PR readiness and normal shipping gates.
- **C9:** Task, branch and actual autoreview lens briefs include the complete approval-bound saved task plan and existing automated-test report details, so prose-only deliverables and incomplete validation can be checked; absent, unapproved or stale plan text is never labeled approved, and legacy cleanup preserves explicitly required live Claude and historical-proof consumers.
- **C10:** Managed save metadata alone preserves a story-plan grill while substantive changes invalidate it; normal task PR readiness requires existing task verify, automated tests, all three review lenses and conditional functional proof; existing phase launchers deliver their required skills without new policy or proof families. Both task readiness and the committed PR marker checker reject automated blockers even with status passed and require functional proof when the owning task is user_facing, using shared predicates and existing historical compatibility.

The revised story-plan candidate maps AC1-AC12 to proposed support, cleanup,
activation and integration owners. Those inventories, task IDs and counts remain
unapproved estimates until the existing story/decomposition approvals. Each task
binds its exact JIT scope and required tests against actual predecessor output;
an old parity inventory grants no permission to edit unlisted files. Support
allocation includes management criterion11, with final integrated verification
owned by FORGE-COORD-1.1.

## Proof and review checkpoint

All six native Codex CLI/Desktop × macOS/Linux/native-Windows cells are required before
full parity is certified. Each records the actual OS release, CPU, runtime,
checkout, trusted hook source, commands, outcomes and event/launch/log references.
The Linux baseline is Ubuntu 24.04 LTS x64, selected through a real native
answer. Other distributions and architectures remain unobserved; this is not
universal platform certification. The [Linux desktop requirements](https://learn.chatgpt.com/docs/linux/linux-app)
include that baseline. Availability alone does not prove Forge delivery.

Use the following six fixed labels in the existing report’s pass_fail_summary, one row per label: `native-cli-macos`, `native-desktop-macos`, `native-cli-linux-ubuntu-24.04-x64`, `native-desktop-linux-ubuntu-24.04-x64`, `native-cli-windows`, `native-desktop-windows`. Each row states its actual status (passed, failed or unobserved), runtime/build, and log/event references; unobserved fields are explicitly unavailable, never invented. Keep actual commands/interactions in commands_run and all failed/unobserved rows in both remaining_gaps and blocking_findings. These are labeled entries in existing text/report fields, not new schema properties or a new matrix artifact. Independent review checks the six labels and their proof against actual logs; no automated omission detection is claimed.

Use existing automated-test fields and schema-validated recorders. Describe
actual checks in `commands_run`, cover every cell in `pass_fail_summary`, and
list every missing or failed cell in both `remaining_gaps` and
`blocking_findings`. Aggregate `status` stays failed until all required cells
pass. The implementer owns this report; the coordinator collects observations
from accessible hosts and authorized platform operators. The maintainer owns
supplying missing access or assigning operators. No external operator or
outbound communication is assumed authorized.

Independent review checks six-cell coverage and actual outcomes against logs.
Existing clean-proof predicates enforce recorded blockers; they do not
automatically discover omitted cells. Add no matrix validator, platform registry,
evidence family or automatic Desktop-inspection API. A CLI doctor result cannot
certify Desktop. Each actual Desktop bundled runtime must demonstrate that its
completed event normalizes to the shared contract; a different version number
alone is not a refusal, but missing identity or unsupported shape is.

The user selected a review-only draft PR with green CI and explicit missing
platform observations. That checkpoint does not waive normal task readiness,
sealing, merge or story closeout. Keep aggregate live proof failing while cells
are missing. Stage closure still obeys its local-review and committed-diff gates
and cannot certify full parity. After actual missing observations arrive, the
implementer updates the report through its recorder and the coordinator repeats
verification and independent review before normal readiness. No missing host waives a required live cell or reopens settled product choices.
Accepted0058's bounded support allocation resolves the native-support delivery
cycle; it is not a platform-proof workaround. Each support task needs its own
complete approved proof before normal readiness, and final parity remains
blocked by any missing required cell.

## Shared approval and review behavior

Grill convergence and approval are separate. Under0061 and C6, reconcile the
shared gate/recorder, generated brief and prompt text to remove compulsory human
rounds, forced closing questions and the erroneous clean-next-round instruction.
Run one independent cold read, resolve repository-answerable facts and necessary
human decisions, amend once and record the pass against the amended artifact.
A further independent read requires the existing reasoned material-shape-change
route and cap; a helper does not add a second certifying reader. Every gate must
resolve its blocking findings and explicitly attest an empty final frontier,
retaining the existing artifact/grounding-digest checks. Canonical top-level
`frontier_empty: true` attests closure with empty or populated rounds; it does not
require a second final-round closure field. Round-bearing payloads in the existing format that
omit the top-level field may use final-round `frontier_empty: true`. Explicit
top-level false always refuses and cannot be overridden by a round. Empty rounds
without top-level true refuse. An empty round list is allowed when no human
decision is needed; it is never human approval. Structured rounds actually used
retain exact matching, eligibility, historical compatibility and single-use
consumption.

Main asks actual missing decisions and approvals through the host's permitted
interface. In Codex Default, required input belongs in ordinary main chat and
the synchronous question tool is only for permitted optional questions. Isolated
workers return findings to main and never ask the user or wait on empty agent
mailboxes. Record actual decisions and artifact confirmations through existing
commands. For structured rounds actually used, reuse ceremony-target routing and
the genuine completed hook event; never import transcripts, relabel chat as a
tool call or create a parallel approval ledger. Missing hook delivery leaves the
affected structured proof unverified; it does not block the host-supported chat
approval route or justify changing host instructions.

Keep work that depends on a necessary decision or approval pending until the
actual answer arrives. Continue independent authorized work when the host
permits it, and proceed from existing facts when an optional question is
unanswered. Preserve authorization for unchanged scope and resume automatically
after a required answer; changed approval-bound content still needs confirmation.
Cancellation, an asynchronous acknowledgment, ordinary steering, continuation
or mode switching cannot supply missing approval. A canceled write worker needs
fresh Forge delegation admission; history does not revive its grant. Existing
decision acceptance, client signoff and merge ownership remain human-controlled.

Decision0061 places the immediate interaction repair in the already authorized
Decision0054 bootstrap preparation. Keep that change bounded, test it and obtain
independent review before relying on it. It supplies no normal task contribution,
stage completion or release proof. KERNEL owns its complete prepared-change
integration and POLICY owns the remaining shared workflow instructions under
their approved task scopes; all normal task and release gates remain required.

Managed save metadata alone must preserve a story-plan grill; substantive edits
must invalidate it. Until that repair lands, re-grill the actual served plan if
its first save stales the earlier proof. Preserve the existing pre-save checks,
active-decision attestation, approval freshness and one-save marker consumption.
An earlier refusal must not persist an awaiting plan. Decision0029's existing
trust ceiling remains audited human attribution, not cryptographic acceptance
attestation. Never stage a pending approval marker or claim stronger storage
isolation than the current implementation provides.

Normal task readiness and the committed PR-side task-proof check both enforce
verify, clean automated tests, all three review lenses and conditional functional
proof. Automated `status: passed` with blockers still refuses; a user-facing task
missing functional proof refuses. Preserve historical and reconciled-marker
compatibility and stage-local certification. Story closeout consumes shipped
task proof. Review retains its ownership and fix/review-until-clean loop;
proposed Decision0049 is not accepted by implication.

Existing phase launchers deliver their required skills. Task, branch and actual
autoreview lens briefs receive the complete approval-bound task plan and all
existing automated report commands, summaries, gaps and blockers. Missing,
unapproved or stale plan text is labeled honestly. Reuse existing policy and
helpers; do not introduce board-view approval enforcement or new proof rules.
These review inputs and clean-proof predicates must ship before any affected
support task relies on them for its own PR; they are not final-integration-only
repairs.

The role boundary retains existing orchestration/client exemptions and scoped
worker admission. Degraded mode remains the reviewed outage exception with its
existing five-file limit and protected authority. Native setup, questions and
approval gaps are not worker outages. Both adapters must preserve supported
mutation, source/client and degraded-operation checks; concise adapter policy
continues to obey existing document limits.

## Boundaries and handoff

Accepted Decisions0050/0053/0054/0055/0056/0057/0058/0059/0060/0061/0062/0063 own the current amendments. The completed
strict-role-split and plan-approval specs retain their historical bytes and
confirmation; do not reopen those stories or invent reconfirmation gates.
Confirmed `fb7ac63` and event `7b5cf1e91877458c8a2f3751a5476771` preserve the prior revision; `b700c05` is older history. Changed revisions need their own technical grill and confirmation record. Apply the user's10 September2026 standing in-scope approval to each finalized artifact after its technical gates, without inventing answers. The roadmap amendment is already applied at `e218db6`. Revalidate the current derived requirements digest before story-plan, decomposition and JIT approvals; historical confirmation does not establish freshness.
Preserve genuine requirements-gate question history and settled decisions;
existing provenance and freshness checks determine what remains eligible.
Prior rounds may carry forward only when the existing recorder rematches their
exact identity and story under the same gate-consumption owner.
Unchanged answers do not imply an unchanged machine digest or a fresh gate.
Refresh stale requirements through the existing recorder with explicit empty
frontier attestation and obtain any genuinely necessary human decision through
the host-permitted interface; no compulsory new round remains under0061. Never
reuse a consumed structured answer across gates.
Earlier spec proof does not certify an edited artifact. Prepared bootstrap work
is reviewed in full but earns no delegated contribution; retain the actual stage
base and pre-existing dirty inventory. Exact paths, commands and review budget
belong to the existing story/task contracts. A real scope overrun raises the
existing signal rather than widening or splitting the task silently.

The existing linked roadmap's three criteria remain the handoff: preserved
worker policy/gates covers setup, lifecycle, roles and proof; plugin-free native
provenance covers human answers and the Codex route; the bounded repaired
lifecycle chain covers independently reviewed native support tasks and the final
parity leaf's review-only/full-release distinction under0058; accepted0055/0056
retain separately approved staged quality predecessors within this story. AC3 received the exact reviewed amendment stated below at `e218db6`; do not repeat that approval or edit.
For the remaining handoff, refresh existing spec linkage and revalidate requirements
against the current derived digest through the existing workflow. Retain settled
decisions and genuine same-gate history without treating them as automatic
freshness. Do not rederive the roadmap or add a roadmap schema.

This spec defines the target behavior and does not authorize implementation.
The coordinator is interchangeable; execution roles, constitution, model policy,
independent review, human approvals and delivery gates are retained. Planned
repairs are not claims of completed behavior.

The developer describes intent and makes decisions in the main conversation.
Main handles story-level decisions and scheduling; each task owner runs its
complete JIT-to-PR lifecycle, preserving answers and completing review/fix loops.
Both coordinators continue authorized work after answers, passing checks and
status requests, stopping only for completed scope, necessary input or a genuine
blocker after concrete recovery attempts. Routine work must not send the developer
to another task, terminal command or manual Plan-mode switch. Unavoidable platform
trust or login is one guided setup action, not an ongoing workflow. Dogfood must
observe this actual journey: intent, one main-conversation decision flow, delegated
work and review handoff without repeated user pushes. This clarifies existing
main-only routing and adds no framework or new gate.

### Exact handoff semantics

The main coordinator presents the saved plan and asks explicitly whether the
human approves that identified plan revision for the named story/task, using
ordinary main chat in Codex Default. An
unambiguous affirmative answer to that approval question authorizes the existing
approval command; a general grill answer does not. Use the actual human
attribution already established in the conversation for `forge plan approve
--by <name>`, then the existing digest-bound approved save. A refusal, cancellation,
missing answer or ambiguous acceptance retains awaiting-approval; clarify only
the ambiguity. Do not manufacture an identity or infer approval from continuation.
Explicit standing in-scope authorization also permits these commands after each artifact's technical gates; record the statement and artifact binding without inventing answers. A generic request to continue is not approval. Optional structured answers are not prerequisites.

Under0054 and0059, the final parity task owner owns the review-only draft
operation, retries and CI after normal contract approvals, a registered admitted
contribution, deterministic verification and independent review of the committed
source. Main retains human questions and merge decisions. Despite declared
missing platform cells, the task owner may push the reviewed branch, create or
reuse its Git-only draft PR and poll/fix CI through the existing workflow.
The body names every missing live-proof cell. This narrow operation creates no
Forge task marker, claims no normal readiness and leaves the PR draft/unmerged.
Only for this0054 checkpoint, authorize existing Git/GitHub operations after
verifying the approved contract, registered contribution, current deterministic
and source-test reports, complete clean three-lens review and no product dirt.
Pin the reviewed commit, origin, head and default base; refuse changed reviewed
source or missing non-platform proof. Use
`git push origin HEAD:refs/heads/<actual-head>` and inspect
`gh pr list --repo <actual-owner/repo> --head <actual-head> --base <actual-base> --state all --json number,url,state,isDraft,headRefOid,baseRefName`.
A successful lookup with no matching PR permits
`gh pr create --repo <actual-owner/repo> --head <actual-head> --base <actual-base> --draft --title <review-only-title> --body-file <prepared-body-file>`;
otherwise verify and reuse the actual matching draft. Use
`gh pr checks <actual-number> --repo <actual-owner/repo>` to inspect CI and
repeat after actual changes. Preserve command outcomes and URLs in the existing
scratchpad/test-report fields. This is not `forge task pr-ready`: do not invoke
its seal/marker mutation while declared platform proof is missing. No guard,
review, admission or protected-state override is authorized by these commands.

Resolve the actual repository/head/base and reuse a verified existing PR; a
failed lookup is not absence, and an uncertain creation result is rechecked
before retry. Preserve user prose and unrelated staged work. The complete task
proof preflight applies before normal readiness, marker/seal mutations and draft
promotion; it must not block0054's review-only push/create/reuse/CI operation
solely for its declared missing platform cells. When later observations make
proof complete, the same task owner repeats normal verification and review,
satisfies stage/task readiness and continues the same PR through the existing
marker and human-merge flow. A valid seal retry must not mint duplicate marker
commits or reset its timestamp. Update that PR's Forge-owned evidence and promote
the draft only after complete proof; no duplicate task/PR or fabricated readiness
is permitted.

Follow the actual host's interaction rules under0061. Its rule for unanswered optional questions amends0057’s blanket pause-after-every-question clause: only work dependent on a necessary answer waits; independent work supported by existing facts continues. In Codex Default, ask
necessary decisions and approvals directly in main chat and reserve the
synchronous tool for permitted optional questions. A restriction on that tool
does not prevent ordinary-chat approval. Do not require manual mode switching,
an asynchronous approval tool, a private host patch or repeated “continue”.
Honor an explicitly requested mode separately. Reconcile the guide's obsolete
forced-mode and synchronous-only wording with this procedure.

`clear` is a documented SessionStart `source`; the runtime audit found its
required registration matcher missing. KERNEL owns that repair alongside
startup, resume and compact. Required-handler tests remove each source
independently in each adapter and both together, and live observations must
include clear delivery. A CLI inspection does not certify Desktop. See the
[native hook source contract](https://learn.chatgpt.com/docs/hooks#sessionstart).

Decision0053's joint-delivery requirement remains under0058: the approved owning
task must ship native write-hook activation and legitimate worker admission
together, whether allocated to a bounded support task or final integration. Verify the delivered
combination admits both native and companion workers with hooks enabled. An
incomplete installation cannot be certified ready; existing hook/readiness and
admission checks fail closed, and existing upgrade preflight/conflict handling
must preserve client settings. This requires testing the incomplete combination
and successful delivered pair, not a new transactional installer or permission
to disable hooks to obtain write access.

At the review checkpoint, close the implementation stage only after its existing
scoped deterministic tests, verified contribution, reviewed-commit and launch
checks pass. This stage closure is distinct from task readiness: aggregate live
proof can remain failed, and independent review must report that limit honestly.
Open the Git-only draft with no marker. Collect outstanding real platform
questions at this no-open-stage boundary, or before the initial stage starts;
never solicit them during an open implementation stage. If a later observation
reveals a code defect, use `forge task reopen FORGE-COORD-1.1` while unshipped,
retain the original base, and follow the existing re-grill/approval, delegated
repair, verification and review route. Evidence-only observations require no
product rewrite. All later readiness and shipping gates still apply.

The parity leaf FORGE-COORD-1.1 preserves integrated C1-C10 closure and its
measured review budget. Accepted0058 requires validated, separately approved
support-task scopes, target preparation, baselines and complete review boundaries
before execution; the former single-task inventory does not approve those
allocations. Preserve every prepared change in a complete support-task review or
final complete activation review and retain its original provenance. Staged
cleanup predecessors retain their exact-scope approval and complete
patch/review-input ceilings. No broad joint-quality budget, larger review limit
or automatic scope waiver is granted.


## Staged quality rollout — accepted0055/0056

Under accepted0055/0056, bounded mechanical cleanup PRs and separately reviewed semantic repairs precede final mandatory full-repository Ruff/Pyright activation. Existing verification and independent review remain active throughout migration. FORGE-COORD-1.1 owns final integrated coordinator-parity proof; separately approved tasks in this same story own complete native support reviews under0058 and staged quality cleanup under0055/0056. Bounded support PRs may ship through their own full task gates before final mandatory quality activation; no full quality or full-parity shipping claim is permitted before activation passes. Preserve supported native hooks/schema/completion and registered admission requirements; native write-hook activation and legitimate worker admission still land together in their approved owning task.

The story-plan candidate proposes measured formatter units, diagnostic-grounded semantic responsibilities and final activation. Task counts and file/range inventories are unapproved estimates, not capability-spec authority; refresh them from actual pinned-tool output after support/predecessor integration. Measurements justify proposed units but do not approve task identities, budgets or a recorded decomposition. Main must obtain the existing saved story/task-plan approvals before recording/admitting execution. Exact JIT scopes/tests/budgets bind each actual task before implementation. Every complete product patch stays below120,000bytes and full autoreview input below180,000bytes, with headroom and independently enforced line/file budgets. These are agreed Forge task bounds, not a statement of the installed review helper's limits. Formatter-only changes require AST-equivalence and separate comments/directives inspection; semantic changes remain separate full review with regression proof. No blanket suppression, permanent legacy exclusion, review truncation, artificial clean result or fabricated task approval is permitted.

Final activation pins Ruff0.16.6 lint/format and Pyright1.1.411, runs identical meaningful local/CI checks over all authored Python including tests, and fails for absent required configuration or deliberate lint/format/type violations. Generated clients declare their own stack checks. Staged migration delays activation honestly; it does not weaken final coverage. Before parity ships, verify the activated baseline against the actual integrated coordinator result as well as all C1-C10 and platform proof.

The reviewed edit at commit `1bb1704` preserved the story/epic identity and every other roadmap field and ordering value. Its historical AC3, superseded by the separately approved0058/0059 amendment recorded below, was: “After the existing approvals, separately approved staged quality-cleanup predecessor tasks complete their normal task PR gates and activate mandatory full-repository quality checks before parity ships. Codex delivers the remaining coordinator parity repairs and lifecycle coverage through the bounded FORGE-COORD-1.1 leaf and its complete approval-to-PR chain; prepared bootstrap bytes are reviewed but are not credited as its delegated contribution.”; do not add task IDs to story depends_on. Main owns story planning, scheduling and human decisions; each cleanup task owner owns its complete JIT-to-PR execution under0059. Each predecessor retains normal task worktree, approval, registered delegation, verification, review, PR and actual marker-on-main gates. No independent cleanup story or advance merge approval is implied. Target runtime transport must pass actual target-owned hooks/schema/admission/completion checks; this spec grants no bypass. Preserve the dirty native candidate and real receipts.

Approved support tasks deliver the canonical management procedure in factory/skills/forge.md and concise pointers in both runtime entrypoints, docs/native-coordinator.md and AGENTS.md; the parity leaf verifies the integrated result. Preparation patches are inputs to reconcile, not approved scopes. Acceptance: main-only human interaction; authorized host capabilities; task-owned JIT workspaces and dependency-marker handoff under0047 as amended by0059; task titles `<project> | <story>/<task> | <title>` with escaped table pipes, real IDs and preserved custom titles; no duplicate pending dispatch; existing forge note/scratchpad recovery; quiet child results; unchanged Claude route. Follow actual question-tool restrictions and app creation authorization; queued client IDs are not task IDs. An app worktree requires validated Forge attachment before task operation and never substitutes for write admission. No new framework, registry, fake receipt or forced mode switch is introduced.

Context-file C6 and switching C7 remain explicit acceptance: untrusted hints preserve artifact/digest/read-only authority; coordinator switching uses completed-task and active-worker checks plus actual no-pending-question observation in the existing test report. No new cross-session registry or six-cell omission validator is introduced. Independent review checks complete six-cell coverage against actual logs and recorded blockers remain enforced. The parity-only review draft may report incomplete platform proof under0054; final parity-task readiness/marker, merge and story closeout remain blocked until all required proof is complete; bounded support tasks retain their own complete approved proof and normal PR gates.

### Recorded roadmap amendment and remaining gate order

The earlier AC3 edit at `1bb1704` remains history. The user approved the exact
versioned0058/0059 replacement in main chat; its refreshed digest-bound epics
review is recorded and commit `e218db6` applies only FORGE-COORD-1 AC3. The
approved proposal and resulting roadmap both have SHA256
`c37199034d36f19942d133c691a5bc234df1f756a9c1347ae176640090af27ab`. Recorded replacement:

> After the existing approvals, explicitly scoped native bootstrap support tasks may use the existing isolated candidate under Decision0058 and deliver prepared changes through complete, independently reviewed support PRs. Validate exact scopes, target preparation, baselines and complete review boundaries before execution. Preserve genuine approvals, registered delegated writes, existing review limits, normal task PR gates, actual predecessor markers on main and sequential merge ordering for this overlapping bootstrap and quality delivery; native write-hook activation and legitimate worker admission land together. General dependency-ready scheduling under Decision0059 remains available where dependencies and disjoint scopes permit. Separately approved staged quality-cleanup predecessor tasks activate mandatory full-repository quality checks before full parity ships. FORGE-COORD-1.1 completes the remaining bounded parity integration and its approval-to-PR chain, including all six required native live platform cells before full parity shipping. Original prepared bootstrap bytes retain their provenance and are reviewed completely, but are not credited as delegated contribution.

Preserve every other roadmap field, identity and ordering value and intervening
unrelated work; add no task IDs to story depends_on. Use the existing versioned
roadmap proposal and reviewed-edit procedure from0057, not the incompatible
importer or roadmap fill. Do not repeat the completed amendment or ask for its approval again.
Fresh requirements grounding and the delivery plan’s own revision, grill and
story/task-plan approvals remain before normal support-task implementation.
Accepted0059/0060/0061/0062/0063 settle only their stated policy reconciliations; they do not
establish exact scopes/targets, a working preparation route or plan approval.
Decision0061's bounded0054 bootstrap repair retains its separate preparation
authorization and review obligations, not normal task or release credit.

### Explicit evidence and closure boundaries

The six-cell matrix is native Codex only: CLI and Desktop on macOS, Ubuntu24.04LTSx64 Linux, and native Windows. Each cell records the actual runtime/build, OS/CPU, executed command or interaction, completed event identity and observed payload-to-shared-contract mapping with event/launch/log references. Unsupported or incomplete actual event shape fails closed and leaves that cell and its dependent gate pending. Fixture normalization tests are regression evidence, never substitute live delivery. This adds no doctor cross-host inspection or runtime registry. Claude retains existing adapter/compatibility regressions; no second six-cell matrix is required.

Accepted0054 deliberately assigns omission detection to independent review of all six cells against actual logs under the trusted-command model. Existing predicates enforce recorded failed status/blockers; they do not discover an omitted cell mechanically. Preserve this explicit boundary. A new six-cell schema validator is a scope change contrary to that settled design, not a required correction.

Accepted0054 also requires preserving the exact unambiguous submitted free-text answer and its identity. No speculative secret-shaped-answer filter, warning gate, redaction or retention subsystem is added. The old native guide's contrary free-text wording is a scheduled parity-owned correction; it does not override the accepted decision. Ordinary runtime/tool restrictions still apply.

Acceptance closure covers every numbered spec criterion1-12, referred to here as AC1-AC12 for closure accounting. Earlier parity-task C1-C10 labels retain their stated task-level meaning; their closure cannot stand in for management criterion11 and staged-quality criterion12. Before recording the approved task contracts, map each numbered spec criterion to its actual owning task and evidence: validated and approved support-task contracts may own complete prepared native changes under0058 and workflow/workspace/delivery changes, parity owns final integrated behavior, cleanup/activation owns quality rollout, and final parity proof confirms the activated baseline and all six live cells on the integrated result. Map every prepared change to its complete support-task review or final complete activation review; no omitted or partially reviewed bytes may ship. No completed report may assert whole-spec closure from C1-C10 alone.

Temporary paths in preparation notes are not durable approval authority. The repository roadmap proposal is plans/exploration/coordinator-staged-quality-roadmap-proposal.json; commit it before the digest-bound epics grill and reviewed-edit gate. Save the final story/task plans and exact inventories through the existing versioned repository artifacts and digest-bound recorder/approval flow before task approval. The unapproved parity preview is planning context only, not proof of scope authorization; reconcile actual integration needs and bind the final exact scope/required tests before admission. References to /tmp patch/audit drafts identify preparation inputs only; preserve required content/evidence in repository-owned records before relying on it for an approval or closure claim.

### Retired Codex agent definitions under Decision0057

Remove only the shipped planner-high, docs-decomposer and functional-checker TOML definitions under .codex/agents, together with obsolete delivery and scaffold-check requirements. Preserve their logical workflow roles, phase prompts, evidence producer identities, current harness model policy and all gates. Preserve client-owned custom agents and any modified copies of the three formerly shipped files. Fresh deliveries omit the retired definitions. For existing clients, compare against the previously delivered harness version using existing ownership/conflict checks; retire only an unchanged harness-owned copy through the existing reviewed upgrade procedure. Retain modified or unverifiable copies and report the existing upgrade conflict for a user decision; never delete solely by filename. Native coordination must not depend on loading the removed definitions. The approved delivery support task owns this removal and its destination/boundary regressions; FORGE-COORD-1.1 verifies the integrated outcome. Optional read-only explorer/validator presets use the same ownership and preflight checks and do not restore these retired definitions.
