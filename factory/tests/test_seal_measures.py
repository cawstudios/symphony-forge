"""`stage done` measures and records; it refuses only on failed proof.

Owner decisions (2026-09-09): strays, budget overruns and required-test id
misses are MEASURED on the stage, never refused (the one refusal left on a
measure is a delta above twice the line budget); a closed, bounded, in-scope
degraded window is the stage's write launch; plan digests are BODY digests so
`plan save` never invalidates a grill; harness-owned paths (decision records,
the context ledger) never stale a task grill and never count as strays; the
PR-contract check counts only the PR's own commits.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from test_gates import (  # noqa: F401
    DECOMP, HARNESS, STAGE_TASK, check_pr_ticket, git, head, intake,
    measured_stage, plan_draft, pr_ticket_base, record_grill,
    record_skeleton_then_frontier, record_task_grill, repo, run, save_plan,
    sign_off, stamp_and_commit, start_stage, write_in_scope,
)

sys.path.insert(0, str(HARNESS / "factory" / "scripts"))
from factory_lib import (  # noqa: E402
    load_json, plan_digest_without_assumptions,
    protected_decomposition_state_path, require_task_grill, task_rows,
)


def _claim(repo: Path, *files: str) -> str:
    """Record the files a degraded window touched (what the hook records)."""
    active = json.loads((repo / ".factory" / "quickfix.json").read_text())
    active["files"] = list(files)
    (repo / ".factory" / "quickfix.json").write_text(json.dumps(active))
    return active["id"]


def test_closed_in_scope_degraded_window_is_the_stages_write_launch(
        repo, tmp_path):
    start_stage(repo, tmp_path, STAGE_TASK, launch=False)
    write_in_scope(repo, "src/core.py")
    code, out = run(repo, "forge.py", "mode", "degraded", "start",
                    "--reason", "host-only check")
    assert code == 0, out
    window_id = _claim(repo, "src/core.py")
    code, out = run(repo, "forge.py", "mode", "done")
    assert code == 0, out
    stamp_and_commit(repo)
    code, out = run(repo, "forge.py", "stage", "done", "T1")
    assert code == 0 and window_id in out, out
    stage = measured_stage(repo)
    assert stage["status"] == "done" and stage["host_window"] == window_id
    code, out = run(repo, "forge.py", "stage", "list")
    assert code == 0 and f"host-fix window: {window_id}" in out, out


def test_an_open_or_out_of_scope_degraded_window_is_not_a_launch(
        repo, tmp_path):
    start_stage(repo, tmp_path, STAGE_TASK, launch=False)
    write_in_scope(repo, "src/core.py")
    stamp_and_commit(repo)
    code, out = run(repo, "forge.py", "mode", "degraded", "start",
                    "--reason", "host-only check")
    assert code == 0, out
    _claim(repo, "billing/ledger.py")
    # Still open: nothing closed, nothing bounded — not a launch.
    code, out = run(repo, "forge.py", "stage", "done", "T1")
    assert code != 0 and "no successful write launch" in out, out
    code, out = run(repo, "forge.py", "mode", "done")
    assert code == 0, out
    # Closed, but it touched a path outside the task's write scope.
    code, out = run(repo, "forge.py", "stage", "done", "T1")
    assert code != 0 and "no successful write launch" in out, out
    assert "host_window" not in measured_stage(repo)


def test_one_plan_grill_before_save_still_matches_after_save(repo, tmp_path):
    # The recipe "record the grill against the draft, save, record again
    # against the saved copy" is gone: the digest is the plan BODY, so the
    # `saved:` timestamp `plan save` writes into the frontmatter cannot
    # invalidate the one record.
    sign_off(repo)
    intake(repo)
    draft = tmp_path / "plan.md"
    draft.write_text(plan_draft(repo))
    code, out = record_grill(repo, "plan", digest_of=draft)
    assert code == 0, out
    code, out = run(repo, "forge.py", "plan", "save", "--from", str(draft),
                    "--story", "ENG-1")
    assert code != 0 and "awaiting-approval" in out, out
    active = next((repo / "plans" / "active").glob("ENG-1-*.md"))
    assert "saved:" in active.read_text(encoding="utf-8")
    assert (plan_digest_without_assumptions(draft)
            == plan_digest_without_assumptions(active))
    code, out = run(repo, "forge.py", "plan", "approve", "--by", "Ravi")
    assert code == 0 and "http://127.0.0.1:" in out, out
    code, out = run(repo, "forge.py", "plan", "save", "--from", str(active),
                    "--story", "ENG-1")
    assert code == 0 and "approved" in out, out


def _write_decision(repo: Path, name: str = "0999-measured-not-refused") -> str:
    rel = f"docs/decisions/{name}.md"
    path = repo / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("---\nid: 0999\nstatus: proposed\n---\n# Measured\n")
    return rel


def _recorded_task(repo: Path, task_id: str = "T1") -> dict:
    tasks = load_json(protected_decomposition_state_path(repo), default={})
    return next(t for t in tasks.get("tasks", []) if t.get("id") == task_id)


def test_decision_record_and_context_ledger_never_stale_a_task_grill(
        repo, tmp_path):
    sign_off(repo)
    intake(repo)
    save_plan(repo, tmp_path)
    record_skeleton_then_frontier(repo, [STAGE_TASK])
    code, out = record_task_grill(repo, STAGE_TASK)
    assert code == 0, out
    assert task_rows(repo)[0]["grill_freshness"] == "fresh"

    ledger = repo / "docs" / "context" / "ledger.json"
    ledger.parent.mkdir(parents=True, exist_ok=True)
    ledger.write_text('{"files": []}\n')
    git(repo, "add", _write_decision(repo), "docs/context/ledger.json")
    git(repo, "commit", "-qm", "workflow bookkeeping")
    assert task_rows(repo)[0]["grill_freshness"] == "fresh"
    require_task_grill(repo, "T1", _recorded_task(repo))  # does not raise

    # The PRODUCT tree still grounds the grill before the stage opens.
    write_in_scope(repo, "src/other.py")
    git(repo, "add", "src/other.py")
    git(repo, "commit", "-qm", "product moved under the grill")
    assert task_rows(repo)[0]["grill_freshness"] == "stale"


def test_stage_start_keeps_an_approved_grill_fresh(repo, tmp_path):
    sign_off(repo)
    intake(repo)
    save_plan(repo, tmp_path)
    record_skeleton_then_frontier(repo, [STAGE_TASK])
    code, out = record_task_grill(repo, STAGE_TASK)
    assert code == 0, out
    code, out = run(repo, "forge.py", "stage", "start", "T1", "--trunk")
    assert code == 0, out
    assert task_rows(repo)[0]["grill_freshness"] == "fresh"
    git(repo, "add", _write_decision(repo))
    git(repo, "commit", "-qm", "decision taken mid-stage")
    assert task_rows(repo)[0]["grill_freshness"] == "fresh"
    require_task_grill(repo, "T1", _recorded_task(repo))


def test_decision_record_is_never_a_write_scope_stray(repo, tmp_path):
    start_stage(repo, tmp_path, STAGE_TASK)
    write_in_scope(repo, "src/core.py")
    _write_decision(repo)
    stamp_and_commit(repo)
    code, out = run(repo, "forge.py", "stage", "done", "T1")
    assert code == 0 and "NOTE" not in out, out
    measured = measured_stage(repo)["measured"]
    assert measured["strays"] == [] and measured["files"] == 1


def _window_record(repo: Path, window_id: str, name: str) -> None:
    ledger = repo / "plans" / "quickfixes"
    ledger.mkdir(exist_ok=True)
    (ledger / f"{name}.json").write_text(json.dumps({
        "event": "done", "id": window_id, "files": ["src/fix.py"],
    }) + "\n")
    git(repo, "add", f"plans/quickfixes/{name}.json")
    git(repo, "commit", "-q", "-m", f"complete {window_id}")


def test_check_pr_ticket_ignores_records_merged_in_from_the_trunk(repo):
    base = pr_ticket_base(repo)
    trunk = git(repo, "rev-parse", "--abbrev-ref", "HEAD")
    own, merged = "Q-0042-own1", "Q-0043-trnk"
    git(repo, "checkout", "-q", "-b", "fix/own-window")
    _window_record(repo, own, "own-done")
    git(repo, "checkout", "-q", trunk)
    _window_record(repo, merged, "trunk-done")
    git(repo, "checkout", "-q", "fix/own-window")
    git(repo, "merge", "-q", "--no-ff", "--no-edit", trunk)

    code, out = check_pr_ticket(repo, base, "fix/own-window", f"Ticket: {own}\n")
    assert code == 0 and f"window {own}" in out and merged not in out, out


FAKE_UPSTREAM = "a" * 40


def _fake_git(monkeypatch, *, online: bool = True, upstream: str = FAKE_UPSTREAM):
    """Stand in for run_quiet: no network, a fake upstream, a fake clone."""
    from forge_cli import doctor

    calls: list[list[str]] = []

    def run_quiet(argv, **_kwargs):
        calls.append(list(argv))
        if argv[:2] == ["git", "ls-remote"]:
            return (0, f"{upstream}\tHEAD") if online else (128, "could not resolve host")
        if argv[:2] == ["git", "clone"]:
            if not online:
                return 128, "could not resolve host"
            skill = Path(argv[-1]) / "skills" / "autoreview"
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text("fresh reviewer\n")
            return 0, ""
        if "rev-parse" in argv:
            return 0, upstream
        return 0, ""

    monkeypatch.setattr(doctor, "run_quiet", run_quiet)
    return calls


def test_doctor_reports_a_stale_autoreview_copy_and_fix_refreshes_both_homes(
        tmp_path, monkeypatch):
    from forge_cli import doctor

    codex_copy = doctor._autoreview_dir(tmp_path)
    claude_copy = tmp_path / ".claude" / "skills" / "autoreview"
    for copy in (codex_copy, claude_copy):
        copy.mkdir(parents=True)
        (copy / "SKILL.md").write_text("old reviewer\n")
    _fake_git(monkeypatch)

    # Installed before refreshes existed (no recorded sha): stale.
    sha = doctor._autoreview_upstream_sha()
    assert sha == FAKE_UPSTREAM
    ok, detail = doctor._autoreview_status(tmp_path, sha)
    assert not ok and detail == f"stale (upstream {FAKE_UPSTREAM})"

    assert doctor._autoreview_install(tmp_path, sha)
    for copy in (codex_copy, claude_copy):
        assert (copy / "SKILL.md").read_text() == "fresh reviewer\n"
        assert (copy / ".upstream-sha").read_text().strip() == FAKE_UPSTREAM
    assert doctor._autoreview_status(tmp_path, sha) == (True, str(codex_copy))

    # Upstream moves again: stale again, until the next --fix.
    assert not doctor._autoreview_status(tmp_path, "b" * 40)[0]


def test_doctor_autoreview_refresh_skips_offline_and_never_creates_claude_copy(
        tmp_path, monkeypatch):
    from forge_cli import doctor

    codex_copy = doctor._autoreview_dir(tmp_path)
    codex_copy.mkdir(parents=True)
    (codex_copy / "SKILL.md").write_text("old reviewer\n")

    _fake_git(monkeypatch, online=False)
    assert doctor._autoreview_upstream_sha() == ""
    # No network, no verdict: the copy is not called stale.
    assert doctor._autoreview_status(tmp_path, "") == (True, str(codex_copy))
    assert not doctor._autoreview_install(tmp_path, "")
    assert (codex_copy / "SKILL.md").read_text() == "old reviewer\n"

    _fake_git(monkeypatch)
    assert doctor._autoreview_install(tmp_path, FAKE_UPSTREAM)
    # Only ~/.codex is the required home; ~/.claude is refreshed when it
    # already holds a copy, never created.
    assert not (tmp_path / ".claude" / "skills" / "autoreview").exists()
    assert (codex_copy / ".upstream-sha").read_text().strip() == FAKE_UPSTREAM
    # A missing copy reads as not installed, not stale.
    assert doctor._autoreview_status(tmp_path / "other", FAKE_UPSTREAM) == (
        False, "not installed")
