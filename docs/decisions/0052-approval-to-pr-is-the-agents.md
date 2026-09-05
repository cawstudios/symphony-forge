---
status: accepted
confirmed_by: "Nandu"
date: 2026-09-06
stories: [upgrade-preserves-doc-contracts]
---

# From plan approval to the PR, the run is the agent's

## Context
<!-- Why this decision was needed; the forces at play. -->

One story recorded the cost of the previous arrangement: roughly twenty
task-grill rounds, fifty Codex jobs, and twenty-six interruptions of the human
between approving the task plan and reaching a pull request.

The grill is the lock that authorises delegation, and it was bound to two
things it should not have been. It hashed the WHOLE task contract, so resolving
a grill finding — which is done by editing the contract — invalidated the grill
that found it. Raising a review-file ceiling from 38 to 58, pure bookkeeping,
cost a full adversarial round; the human's own instruction to raise it and stop
asking was itself a stop. It also hashed the whole product tree, so committing
the implementation invalidated the grill that `forge delegate` needs in order
to FIX that implementation. Neither loop can converge.

Four places asked "is this grill still grounded?" and answered three different
ways. The one behind the board and `forge next` never consulted the stage at
all, so it reported STALE the moment the tree moved and kept routing delivered
work back to a gate that exists to authorise work not yet started.

The interruptions divided cleanly when counted: eight were the sandbox refusing
a dependency install, six a review-budget ceiling, five a `write_scope` one
file short of what the work mechanically implied, and seven genuine design
questions. Nineteen of twenty-six were answerable from something already
recorded. The rule saying so was written in WORKFLOW.md and ignored — and the
delegate brief actively ordered the worker to stop at the ceiling and return
incomplete "so the orchestrator can split the task", which framed a planning
decision as an implementation event.

## Decision
<!-- What was decided, in one or two sentences. -->

**Everything reaches the human during PLANNING. After the plan is approved, the
next thing they see is a sound PR.**

**The grill re-runs only when what the work IS changes** — objective,
acceptance criteria, plan contracts, write scope, required tests, verify
commands, `user_facing`. `review_budget` and `reviewer_focus` still enforce and
still reach the reviewer; they no longer re-grill. The product tree is bound
only until the stage opens; after that it moves BECAUSE OF the work the grill
authorised. One predicate answers this for every caller.

**A plan edited after approval returns to the person who approved it**, not to
another cold read. The grill already converged on that design; what changed is
the text they signed off. Before approval it remains a re-grill.

**Both ways of interrupting the human are gated while a stage is open.** A
pre-tool gate refuses the question tool and the Stop hook refuses ending the
turn, because a tool gate alone leaves prose as the back door. Passage requires
naming the decision that does not exist and where it was already looked for —
the contract, the plan, the constitution, an accepted decision, a lesson in
force. A budget ceiling, a scope short by files the work implies, and an
environment block with a documented path are refused WITH the answer. One
escalation authorises one interruption.

**It is an allow-list of denials, not a permit-list.** A reason the harness
cannot self-answer passes after the challenge, because a novel situation
probably does need the human, and a permit-list would block exactly the cases
nobody foresaw. Every escalation is recorded, and `forge audit` counts them per
story.

## Consequences
<!-- What follows: tradeoffs accepted, doors closed, work implied. -->

- A stage that is open and unfinished cannot be abandoned to ask a question the
  contract already answers. The way out is to FINISH the task; there is no
  proxy for having finished it, and the window is exactly the open stage.
- The hooks fail OPEN on unreadable state, a missing control directory, and
  every tool that is not the question tool. A missed interruption costs one
  question; a hook that traps a session costs the session.
- Three things move into planning, where the human already is: a required test
  the task must create but may not write is refused at approval, the grill
  brief carries the lessons in force for the task's paths, and the ceiling is
  no longer renegotiated mid-flight.
- `stage start` requires `task start`, or `--trunk` to say the trunk is the
  choice. The stage-based flow stays available; skipping the worktree step
  silently does not.
- Approving a task plan requires the board to have served that exact text.
- `--effort` is reachable, so the escalation harness.yaml documents can be
  performed.
- Accepted cost: a novel bad interruption still reaches the human once. It is
  counted, so a recurring one becomes a number instead of an impression formed
  over eighteen rounds, and a recurring reason becomes a new denial.
- This extends decision 0051 rather than superseding it: every grill gate stays
  ledger-matched with a floor of one round.
