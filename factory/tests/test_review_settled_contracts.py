"""The review brief carries what is settled, and a finding that contradicts it
can be rejected on the record instead of re-fought every round.

A client's three-lens review demanded, three rounds running, a guard that the
approved T3b contract explicitly forbids, and the "fix" broke the story's
pinned scenario — because the reviewer only ever saw the one task's slice.
Now the brief carries the story plan's decisions/rulings and the contracts of
tasks already sealed, and `forge review <id> --reject` moves a recorded
blocking finding into `rejected_findings` with the citation, ledgers the
contract as a lesson (so the next brief carries it), and stamps the stage when
no lens blocks any more.
"""
from __future__ import annotations

import json

from test_gates import (  # noqa: I001 — test_gates puts factory/scripts on sys.path
    git, head, intake, record_skeleton_then_frontier, repo, run, save_plan,
    sign_off, skeletal_stage_task, write_stages,
)
from factory_lib import (  # noqa: E402
    evidence_path, load_json, protected_decomposition_state_path,
)
from forge_cli.lessons import load_lessons  # noqa: E402
from forge_cli.review import LENSES  # noqa: E402
from forge_cli.review_brief import _plan_section_bodies, _task_section  # noqa: E402
from forge_cli.stages import load_stages  # noqa: E402

__all__ = ["repo"]


def test_plan_sections_are_picked_by_header_word():
    text = ("# Plan\n\n## Problem\nwhy\n\n## Decisions\n0154 amended; 0118.\n\n"
            "## Owner rulings (Ravi)\n- rows are recoverable-only\n\n## Risks\nnone\n")
    picked = _plan_section_bodies(text, ("decision", "ruling"))
    assert [h for h, _ in picked] == ["Decisions", "Owner rulings (Ravi)"]
    assert picked[0][1] == "0154 amended; 0118."
    assert picked[1][1] == "- rows are recoverable-only"


def _story(repo, tmp_path, *, t1_status: str = "done") -> None:
    sign_off(repo)
    intake(repo)
    save_plan(repo, tmp_path)
    t1 = {**skeletal_stage_task("T1"),
          "plan_contracts": [{"id": "T1-AC1", "statement": "the exact memory answers a destructive ask",
                              "source": "plan#ac"}]}
    t2 = skeletal_stage_task("T2")
    record_skeleton_then_frontier(repo, [t1, t2])
    base = head(repo)
    (repo / "src").mkdir(exist_ok=True)
    (repo / "src" / "work.py").write_text("task work\n")
    git(repo, "add", "src/work.py")
    git(repo, "commit", "-q", "-m", "T2 work")
    write_stages(repo, {
        "issue": "ENG-1",
        "stages": [
            {"id": "T1", "title": "first", "status": t1_status, "task_sha256": "abc",
             "base_sha": base, "started_at": "2026-09-09T00:00:00+00:00",
             "dirty_at_start": {}},
            {"id": "T2", "title": "second", "status": "active", "task_sha256": "def",
             "base_sha": base, "started_at": "2026-09-09T01:00:00+00:00",
             "dirty_at_start": {}},
        ],
    })


def test_brief_carries_plan_decisions_and_sealed_contracts(repo, tmp_path):
    _story(repo, tmp_path)
    plan = next((repo / "plans" / "active").glob("ENG-1-*.md"))
    plan.write_text(plan.read_text() + "\n## Decisions\n0154 (amended): old rows are not listed.\n")
    task = next(t for t in load_json(
        protected_decomposition_state_path(repo), default={})["tasks"] if t["id"] == "T2")
    brief = "\n".join(_task_section(task, repo))
    assert "Settled — do not relitigate" in brief
    assert "0154 (amended): old rows are not listed." in brief
    assert "T1-AC1" in brief and "the exact memory answers a destructive ask" in brief
    # A task that is not sealed contributes nothing.
    _story_pending = load_stages(repo)
    _story_pending["stages"][0]["status"] = "pending"
    write_stages(repo, _story_pending)
    assert "T1-AC1" not in "\n".join(_task_section(task, repo))


def _record_lens(repo, lens: str, blocking: list[dict]) -> None:
    code, out = run(repo, "forge.py", "review-brief", "--all")
    assert code == 0, out
    payload = {
        "generated_by": "autoreview", "score": 10 - 3 * len(blocking),
        "summary": f"{lens} lens", "blocking_findings": blocking,
        "non_blocking_findings": [], "recommendation": "request-changes" if blocking else "approve",
        "skills_used": ["review-animations"],
    }
    if lens == "quality":
        payload["contract_verdicts"] = [
            {"contract_id": "T1-AC1", "verdict": "implemented", "evidence": "src/work.py:1"},
        ]
    code, out = run(repo, "record_review_from_json.py", "--aspect", lens,
                    stdin=json.dumps(payload))
    assert code == 0, out


def test_reject_moves_the_finding_ledgers_a_lesson_and_stamps_when_clean(repo, tmp_path):
    _story(repo, tmp_path)
    hard = {"category": "security", "area": "src/runtime",
            "summary": "Gate every remembered-Allow lookup on hardFloor (src/runtime/coordinator.ts:266)"}
    _record_lens(repo, "security", [hard])
    _record_lens(repo, "quality", [])
    _record_lens(repo, "performance", [])

    code, out = run(repo, "forge.py", "review", "T2", "--reject", "hardFloor",
                    "--lens", "security", "--reason", "T3b-AC3 keys the consult on the rail case",
                    "--cite", "T3b-AC3; story S4", "--by", "autoreview")
    assert code == 0 and "Rejected security finding" in out, out
    recorded = load_json(evidence_path(repo, "ENG-1", "reviews/security.json"), default={})
    assert recorded["blocking_findings"] == []
    assert recorded["rejected_findings"][0]["finding"] == hard
    assert recorded["rejected_findings"][0]["cite"] == "T3b-AC3; story S4"
    assert recorded["score"] == 10 and recorded["recommendation"] == "approve"
    lessons = load_lessons(repo)
    assert any("T3b-AC3" in l.get("lesson", "") and l.get("applies_to") == ["src/runtime/**"]
               for l in lessons)
    assert "review stamp recorded" in out
    stamp = next(s for s in load_stages(repo)["stages"] if s["id"] == "T2")["local_review_stamp"]
    assert stamp["lenses"] == list(LENSES)


def test_reject_refuses_without_a_citation_or_with_an_ambiguous_match(repo, tmp_path):
    _story(repo, tmp_path)
    _record_lens(repo, "quality", [
        {"category": "x", "area": "src", "summary": "one hardFloor thing"},
        {"category": "x", "area": "src", "summary": "another hardFloor thing"},
    ])
    code, out = run(repo, "forge.py", "review", "T2", "--reject", "hardFloor",
                    "--lens", "quality", "--reason", "r", "--by", "autoreview")
    assert code != 0 and "--cite" in out, out
    code, out = run(repo, "forge.py", "review", "T2", "--reject", "hardFloor",
                    "--lens", "quality", "--reason", "r", "--cite", "c", "--by", "autoreview")
    assert code != 0 and "2 blocking quality findings match" in out, out
    code, out = run(repo, "forge.py", "review", "T2", "--reject", "nothing-like-this",
                    "--lens", "quality", "--reason", "r", "--cite", "c", "--by", "autoreview")
    assert code != 0 and "no blocking quality finding matches" in out, out
