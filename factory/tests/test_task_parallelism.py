"""Tasks inside ONE story run in parallel worktrees when the plan allows it.

The order is the dependency graph, not the list: `task start` and `stage start`
gate on the task's dependencies being done, a second stage may be active when
the write scopes are disjoint, each worktree keeps its own delegation lock and
its own stage record file, and `forge next` lists every task that can move.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

from test_gates import (  # noqa: I001 — test_gates puts factory/scripts on sys.path
    DECOMP, STAGE_TASK, configure_origin_main, git, intake, publish_task_marker,
    record_skeleton_then_frontier, record_task_grill, repo, run, save_plan,
    sign_off, skeletal_stage_task, write_stages,
)
from factory_lib import (  # noqa: E402
    require_ready_task, task_frontier_items, task_frontier_state,
)
from forge_cli.delegate import delegation_lock_path  # noqa: E402
from forge_cli.stages import (  # noqa: E402
    active_stages_everywhere, load_stages, load_story_stages, scope_conflicts,
)

__all__ = ["repo"]

KEY = "ENG-1"


def _task(task_id: str, scope: str, **extra) -> dict:
    contracts = [{**c, "id": f"{c['id']}-{task_id}"} for c in STAGE_TASK["plan_contracts"]]
    return {**STAGE_TASK, "id": task_id, "title": f"{task_id} slice",
            "write_scope": [scope], "plan_contracts": contracts,
            "acceptance_criteria": [c["statement"] for c in contracts], **extra}


T1 = _task("T1", "src/core/")
T2 = _task("T2", "src/api/", dependencies=["T1"])
T3 = _task("T3", "src/ui/", dependencies=["T1"])
T4 = _task("T4", "src/api/handlers/", dependencies=["T2", "T3"])
T5 = _task("T5", "src/api/", dependencies=["T1"])  # overlaps T2 by area
TASKS = [T1, T2, T3, T4, T5]


def _control(tree: Path) -> Path:
    return Path(git(tree, "rev-parse", "--absolute-git-dir")) / "forge"


def _statuses(tree: Path) -> list[str]:
    return [s["status"] for s in json.loads((_control(tree) / "stages.json").read_text())["stages"]]


def _story_after_t1_shipped(repo: Path, tmp_path: Path) -> None:
    """T1 merged (marker on the trunk); T2, T3 and T5 carry contracts."""
    configure_origin_main(repo, tmp_path / "origin.git")
    sign_off(repo)
    assert intake(repo, KEY)[0] == 0
    assert save_plan(repo, tmp_path)[0] == 0
    skeletons = [
        {**skeletal_stage_task(t["id"]), "dependencies": t["dependencies"]}
        if "dependencies" in t else skeletal_stage_task(t["id"])
        for t in TASKS
    ]
    record_skeleton_then_frontier(repo, [T1, *skeletons[1:]])
    git(repo, "add", "-A", "--", "harness.yaml", "docs/decisions")
    if subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=repo).returncode:
        git(repo, "commit", "-qm", "settle fixture inputs")
    data = load_stages(repo)
    data["stages"][0]["status"] = "done"
    write_stages(repo, data)
    publish_task_marker(repo, KEY, "T1")
    code, out = run(repo, "record_decomposition_from_json.py",
                    stdin=json.dumps({**DECOMP, "tasks": [T1, T2, T3, skeletons[3], T5]}))
    assert code == 0, out


def _start_in_worktree(repo: Path, task: dict) -> Path:
    """The real ceremony: grill in the story worktree, `task start`, then grill
    again and `stage start` from inside the task's own worktree."""
    code, out = record_task_grill(repo, task)
    assert code == 0, out
    code, out = run(repo, "forge.py", "task", "start", task["id"])
    assert code == 0, out
    worktree = repo.parent / f"{repo.name}-{KEY}-{task['id']}"
    code, out = record_task_grill(worktree, task)
    assert code == 0, out
    return worktree


def test_tasks_with_disjoint_scopes_run_side_by_side_in_their_own_worktrees(repo, tmp_path):
    _story_after_t1_shipped(repo, tmp_path)
    assert task_frontier_state(repo)[1]["id"] == "T2"

    wt2 = _start_in_worktree(repo, T2)
    # T2 was seeded from the trunk's markers, not from list position.
    assert _statuses(wt2) == ["done", "pending", "pending", "pending", "pending"]
    code, out = run(wt2, "forge.py", "stage", "start", "T2")
    assert code == 0, out

    # T2 is active in ITS worktree, so the story worktree moves on to T3 —
    # and T3's dependency is T1, not the unmerged T2.
    assert {s["id"] for _root, s in active_stages_everywhere(repo)} == {"T2"}
    assert task_frontier_state(repo)[1]["id"] == "T3"
    wt3 = _start_in_worktree(repo, T3)
    assert task_frontier_state(wt3)[1]["id"] == "T3", "a task worktree's frontier is its task"
    code, out = run(wt3, "forge.py", "stage", "start", "T3")
    assert code == 0, out
    assert {s["id"] for _root, s in active_stages_everywhere(repo)} == {"T2", "T3"}
    code, out = run(repo, "forge.py", "stage", "list")
    assert code == 0 and "[>] T2" in out and "[>] T3" in out, out

    # Two worktrees never share a delegation lock.
    lock2, lock3 = delegation_lock_path(wt2, "T2"), delegation_lock_path(wt3, "T3")
    assert lock2 != lock3
    assert lock2.is_relative_to(_control(wt2)) and lock3.is_relative_to(_control(wt3))

    # A task worktree writes ONLY its own per-task record, so two parallel task
    # PRs never touch one shared file; the legacy single snapshot is gone.
    records2 = wt2 / ".factory" / "stories" / KEY / "stages"
    assert sorted(p.name for p in records2.glob("*.json")) == ["T2.json"]
    assert json.loads((records2 / "T2.json").read_text())["status"] == "active"
    assert not (wt2 / ".factory" / "stories" / KEY / "stages.json").exists()
    assert not git(wt2, "status", "--porcelain", "--", ".factory/stages.json")
    assert load_story_stages(wt2, KEY)["stages"][0]["id"] == "T2"

    # `forge next` in the story worktree lists both active stages and where.
    code, out = run(repo, "forge.py", "next")
    assert code == 0, out
    assert "T2 (delegate)" in out and "T3 (delegate)" in out, out
    assert f"T2 in {wt2.name}" in out.replace(str(wt2.parent) + "/", "") and \
        f"T3 in {wt3.name}" in out.replace(str(wt3.parent) + "/", ""), out

    # T5 overlaps T2's area: it can be grilled and started as a worktree, but
    # its stage refuses to open beside T2, naming the overlap.
    assert scope_conflicts(repo, "T5") == [f"T2 ({wt2.name}): src/api ~ src/api"]
    assert scope_conflicts(repo, "T4") == []
    assert "T5" not in {t["id"] for _s, t in task_frontier_items(repo)[1:]}
    wt5 = _start_in_worktree(repo, T5)
    code, out = run(wt5, "forge.py", "stage", "start", "T5")
    assert code != 0 and "T2" in out and "src/api ~ src/api" in out, out
    assert _statuses(wt5)[4] == "pending"

    # A scope-change signal into a sibling's scope is refused naming it; one
    # inside the run's own area still raises.
    code, out = run(wt3, "forge.py", "signal", "raise", "--kind", "scope-change",
                    "--by", "implementer", "-m", "need to edit src/api/routes.py as well")
    assert code != 0 and "belongs to task T2" in out, out
    code, out = run(wt3, "forge.py", "signal", "raise", "--kind", "scope-change",
                    "--by", "implementer", "-m", "need to touch src/ui/theme.css too")
    assert code == 0, out

    # T4 waits on both T2 and T3 markers, whatever the list order says.
    code, out = run(repo, "forge.py", "task", "start", "T4")
    assert code != 0 and "dependency T2, T3 marker is absent" in out, out

    # Merge order is the dependency order: a done stage cannot seal before its
    # dependencies' markers are on the trunk.
    data = load_stages(wt3)
    next(s for s in data["stages"] if s["id"] == "T3")["status"] = "done"
    next(s for s in data["stages"] if s["id"] == "T4")["status"] = "done"
    write_stages(wt3, data)
    with pytest.raises(SystemExit, match="T4 cannot seal before its dependencies ship"):
        require_ready_task(wt3, "T4", allow_completed=True,
                           require_approval=False, require_grill=False)
    require_ready_task(wt3, "T3", allow_completed=True,
                       require_approval=False, require_grill=False)
    # The story worktree reports the unmerged T3 as awaiting its merge.
    assert ("await-merge", "T3") in {
        (state, t["id"]) for state, t in task_frontier_items(repo)}


def test_stage_start_waits_on_dependencies_not_list_order(repo, tmp_path):
    sign_off(repo)
    intake(repo)
    save_plan(repo, tmp_path)
    record_skeleton_then_frontier(repo, [T1, skeletal_stage_task("T2")])
    code, out = run(repo, "forge.py", "stage", "start", "T2", "--trunk")
    assert code != 0 and "T2 waits on unfinished dependency task(s): T1" in out, out


def test_legacy_single_file_story_snapshot_is_still_read_then_replaced(repo):
    story = repo / ".factory" / "stories" / "OLD-1"
    story.mkdir(parents=True)
    (story / "stages.json").write_text(json.dumps({
        "issue": "OLD-1",
        "stages": [{"id": "T1", "title": "t", "status": "done"},
                   {"id": "T2", "title": "u", "status": "pending"}]}))
    assert [s["status"] for s in load_story_stages(repo, "OLD-1")["stages"]] == ["done", "pending"]
    write_stages(repo, {"issue": "OLD-1", "stages": [
        {"id": "T1", "title": "t", "status": "done"},
        {"id": "T2", "title": "u", "status": "active"}]})
    assert not (story / "stages.json").exists()
    assert sorted(p.name for p in (story / "stages").glob("*.json")) == ["T1.json", "T2.json"]
    assert [s["status"] for s in load_story_stages(repo, "OLD-1")["stages"]] == ["done", "active"]
