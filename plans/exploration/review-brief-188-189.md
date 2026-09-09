# Review brief — symphony-forge #188 + #189 (harness simplification)

Scope: everything between main-before-#188 (10f8117) and HEAD of feat/one-review-per-task.

What the change is for, in order:
1. `task reopen --review-fix` (#188): a done, unshipped stage returns to active with base ref, contract digest and plan approval intact; only the stage-local review stamp and completed_at drop. Refuses a non-done stage or one a later stage built on. `stage start`, `forge review` and the stamp recorder point at it.
2. One review per task (#189): `forge review` with no P0/P1 finding stamps the stage itself (`stamp_stage_review`) so `stage done` / `task pr-ready` seal on it; `_score` never drops below 8 without a blocking finding; `_next_hint` names the single loop.
3. Settled contracts in the brief: `_settled_section` appends the story plan's Decisions/rulings sections and the plan_contracts of tasks whose stage is done.
4. `forge review <id> --reject MATCH --lens L --reason --cite --by`: moves the single matching recorded blocking finding into `rejected_findings`, ledgers a lesson on the finding's area, recomputes score/recommendation, stamps when no lens blocks.
5. Grill: `ROUNDS_BEFORE_ESCALATING` 5 → 2; task-gate contract treats file-list/line drift as non-blocking; decomposer asks for area-level write_scope.

Review for: correctness of the state transitions (can a stamp be stale-but-accepted? can a reopened stage lose its measured delta? can `--reject` be used to launder a real defect — is the citation requirement enough?), path safety of the artifact rewrite (`evidence_path(..., for_write=True)` + `dump_json`), the lesson ledger interaction (duplicate detection, applies_to glob shape `area/**`), the review-run token / branch-diff digest interplay after an artifact rewrite (does the recorder's later validation break?), and whether `stamp_stage_review` from `forge review` on a DONE stage bypasses `_require_reviewed_commit`'s dirty-tree checks (it binds product_tree_digest; is that sufficient?). Tests are under factory/tests/test_review_fix_reopen.py, test_one_review_per_task.py, test_review_settled_contracts.py. Report P0–P2 only; cite file:line.
