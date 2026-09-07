"""One cold read per gate, with the human's questions asked inside it.

The loop was never a habit — it was forced. Fixing a finding means EDITING the
artifact, and the gates bind a recorded grill to the artifact's digest, so the
edit invalidated the grill that authorised it and a re-read became mandatory.
Re-reading is also what diverges: a fresh unconstrained reader has no memory of
the last one's findings, so it returns a DIFFERENT frontier. Each round
manufactured the next round's work; stories reached eleven, twenty-six and
forty rounds, the last costing six hours.

The shape under test: one unconstrained cold read → every finding put to the
human in that same grill → one amendment → a BOUNDED confirm read that is
handed the findings and the answers and may return nothing else. A confirm
cannot open a frontier, so it terminates.

Its own module for the same reason test_grill_round_cap.py is: test_gates.py is
one very large file where every added branch collides with every other.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from test_gates import HARNESS, git, load_factory_lib, repo, run  # noqa: F401

sys.path.insert(0, str(HARNESS / "factory" / "scripts"))


def _seed(repo: Path, story: str = "ENG-1") -> None:
    lib = load_factory_lib(repo)
    control = Path(git(repo, "rev-parse", "--absolute-git-dir")) / "forge"
    control.mkdir(parents=True, exist_ok=True)
    lib.dump_json(control / "run.json", {"issue_key": story})


def _cold_read(repo: Path, gate: str = "plan", task_id: str = "",
               at: str = "2026-09-07T10:00:00+00:00") -> None:
    """A cold read, as the ledgered launcher records one."""
    from forge_cli.delegate import delegations_path  # noqa: E402
    ledger_id = f"grill-{gate}" + (f"-{task_id}" if task_id else "")
    path = delegations_path(repo)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps({
            "launch_id": f"{ledger_id}-{at}", "task": ledger_id, "at": at,
            "launch_status": "succeeded", "write": False,
        }) + "\n")


def _cold_read_with_digest(repo: Path, digest: str,
                           gate: str = "plan", task_id: str = "",
                           at: str = "2026-09-07T10:00:00+00:00") -> None:
    """A cold read that stamped WHICH bytes it was shown, as the launcher does."""
    from forge_cli.delegate import delegations_path  # noqa: E402
    ledger_id = f"grill-{gate}" + (f"-{task_id}" if task_id else "")
    path = delegations_path(repo)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps({
            "launch_id": f"{ledger_id}-{at}", "task": ledger_id, "at": at,
            "launch_status": "succeeded", "write": False,
            "task_sha256": digest,
        }) + "\n")


def _answer(repo: Path, story: str, question: str, chosen: str,
            options: list[str] | None = None,
            at: str = "2026-09-07T11:00:00+00:00") -> None:
    """An AskUserQuestion round, as post_tool_use.py ledgers one.

    The recorder matches question AND options exactly, so a fixture that
    invents its own options proves nothing about provenance.
    """
    lib = load_factory_lib(repo)
    directory = lib.evidence_path(repo, story, "grill-rounds", for_write=True)
    directory.mkdir(parents=True, exist_ok=True)
    lib.dump_json(directory / f"{abs(hash((question, at)))}.json", {
        "at": at,
        "questions": [{"question": question,
                       "options": options or [chosen, "No"],
                       "chosen": chosen}],
    })


def _refuse(repo: Path, gate: str = "plan", task_id: str = "",
            reread: str = "") -> None:
    from forge_cli.grill import _refuse_a_second_cold_read  # noqa: E402
    ledger_id = f"grill-{gate}" + (f"-{task_id}" if task_id else "")
    _refuse_a_second_cold_read(repo, ledger_id, gate, task_id, reread)


# --------------------------------------------------------- one read per pass


def test_the_first_cold_read_is_allowed(repo: Path):
    _seed(repo)
    _refuse(repo)  # must not raise


def test_a_second_cold_read_is_refused_and_names_the_confirm(repo: Path, capsys):
    _seed(repo)
    _cold_read(repo)
    try:
        _refuse(repo)
    except SystemExit:
        message = capsys.readouterr().out
    else:
        raise AssertionError("the second cold read was allowed")

    # It must name the way forward, or it is a wall: the frontier is not
    # closed, so nothing records and nothing proceeds.
    assert "grill confirm" in message
    # And say WHY, or it reads as bureaucracy rather than the reason the
    # twenty-six-round grill happened.
    assert "different frontier" in message.lower()
    assert "--reread" in message


def test_a_reread_with_a_reason_is_allowed(repo: Path):
    """Not a wall. Answers that change an artifact's SHAPE need a real read.

    A choice with a recorded reason, like `stage start --trunk` — never an
    omission that happens to work.
    """
    _seed(repo)
    _cold_read(repo)
    _refuse(repo, reread="the human dropped the whole sync component")


def test_another_gate_is_unaffected(repo: Path):
    # A task grill must not consume the plan gate's single read.
    _seed(repo)
    _cold_read(repo, gate="task", task_id="T1")
    _refuse(repo, gate="plan")


def test_a_recorded_pass_releases_the_next_read(repo: Path):
    """A later legitimate grill starts fresh.

    Without this the first story to record a pass could never be grilled
    again, because its one read is spent forever.
    """
    _seed(repo)
    lib = load_factory_lib(repo)
    _cold_read(repo, at="2026-09-05T10:00:00+00:00")
    try:
        _refuse(repo)
    except SystemExit:
        pass
    else:
        raise AssertionError("expected the second read to be refused")

    record = lib.evidence_path(repo, "ENG-1", "grills/plan.json", for_write=True)
    record.parent.mkdir(parents=True, exist_ok=True)
    lib.dump_json(record, {"verdict": "pass",
                           "recorded_at": "2026-09-06T00:00:00+00:00"})
    _refuse(repo)  # must not raise


def test_an_unreadable_ledger_never_refuses_a_grill(repo: Path):
    # A check that cannot check must not block the gate: a missed refusal
    # costs a round, a false refusal costs the story.
    _seed(repo)
    from forge_cli.delegate import delegations_path  # noqa: E402
    path = delegations_path(repo)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("{not json\n", encoding="utf-8")
    _refuse(repo)  # must not raise


# ------------------------------------------------- the confirm is bounded


def test_confirm_needs_a_cold_read_first(repo: Path):
    _seed(repo)
    code, out = run(repo, "forge.py", "grill", "confirm", "--gate", "plan",
                    "--print-only")
    assert code != 0
    assert "has not been cold-read" in out


def test_confirm_needs_an_answered_question(repo: Path):
    """A clean read has nothing to confirm — that is the single-grill path."""
    _seed(repo)
    _cold_read(repo)
    code, out = run(repo, "forge.py", "grill", "confirm", "--gate", "plan",
                    "--print-only")
    assert code != 0
    assert "no question has been put to the human" in out


def test_only_answers_given_after_the_cold_read_are_confirmed(repo: Path):
    """Settled ground from an earlier gate is not this grill's findings.

    Carrying it in would ask the reader to re-confirm decisions that were
    never in question here, which is how a bounded read grows back into a
    grill.
    """
    _seed(repo)
    from forge_cli.grill import _answers_since  # noqa: E402
    _answer(repo, "ENG-1", "Which store owns stock?", "SAP",
            at="2026-09-07T09:00:00+00:00")
    _answer(repo, "ENG-1", "Is the card printable?", "Yes",
            at="2026-09-07T11:00:00+00:00")
    after = _answers_since(repo, "2026-09-07T10:00:00+00:00")
    assert [q for q, _ in after] == ["Is the card printable?"]


def test_the_confirm_brief_forbids_new_findings(repo: Path):
    """The whole reason a confirm terminates.

    Given the griller contract instead, a reader hunts — and a hunting reader
    returns a frontier, which restarts the loop.
    """
    from forge_cli.grill import _compose_confirm_brief  # noqa: E402
    brief = _compose_confirm_brief(
        repo, "plan", "the plan", "# Plan\nThe card is printable.",
        [("Is the card printable?", "Yes")])
    flat = " ".join(brief.split())

    assert "Is the card printable?" in flat
    assert "HUMAN'S ANSWER: Yes" in flat
    assert "This is NOT a grill" in flat
    assert "Do NOT raise anything else" in flat
    # The verdict shape has to be per-finding, or the coordinator is back to
    # interpreting prose.
    assert "HONOURED" in flat and "NOT HONOURED" in flat
    # The griller contract must NOT be in here — that is what makes it hunt.
    assert "Hunt:" not in flat


def test_the_confirm_brief_carries_the_amended_artifact(repo: Path):
    from forge_cli.grill import _compose_confirm_brief  # noqa: E402
    brief = _compose_confirm_brief(
        repo, "plan", "the plan", "SENTINEL-ARTIFACT-BODY",
        [("q", "a")])
    assert "SENTINEL-ARTIFACT-BODY" in brief


# ------------------------------------------- the recorder demands the confirm


def _grill_payload(gaps: list[str]) -> dict:
    rounds = [{"question": gap, "options": ["Fix it", "Leave it"],
               "chosen": "Fix it"} for gap in gaps]
    rounds.append({"question": "Any remaining gap before we hand off?",
                   "options": ["No", "Yes"], "chosen": "No",
                   "frontier_empty": True})
    return {
        "gate": "plan",
        "generated_by": "griller", "verdict": "pass", "gaps": gaps,
        "contradictions": [], "resolutions": ["Amended the plan"],
        "inspected_refs": ["plans/x.md"], "current_flow": "n/a",
        "criteria_map": {}, "decision": "keep", "new_abstractions": ["None"],
        "rounds": rounds,
        "citations": [{"finding": gap, "source": "plans/x.md"} for gap in gaps],
        "open_items": [],
    }


def test_a_clean_pass_needs_no_confirm(repo: Path, tmp_path: Path):
    """No findings means nothing was amended, so nothing was left unread.

    This is the single-grill path -- one cold read, record, approve -- and it
    must stay free of ceremony, or the common case pays for the exception.
    """
    _seed(repo)
    plan = repo / "plan.md"
    plan.write_text("# Plan\n", encoding="utf-8")
    _cold_read(repo)
    payload = tmp_path / "grill.json"
    payload.write_text(json.dumps(_grill_payload([])), encoding="utf-8")
    _answer(repo, "ENG-1", "Any remaining gap before we hand off?", "No",
            ["No", "Yes"])

    code, out = run(repo, "record_grill_from_json.py", "--gate", "plan",
                    "--input", str(payload), "--input-digest", str(plan))
    assert code == 0, out


def test_a_pass_with_findings_is_refused_without_a_confirm(repo: Path, tmp_path: Path):
    _seed(repo)
    gap = "the plan never says who owns stock"
    payload = tmp_path / "grill.json"
    payload.write_text(json.dumps(_grill_payload([gap])), encoding="utf-8")
    plan = repo / "plan.md"
    plan.write_text("# Plan\n", encoding="utf-8")
    # Provenance runs first: every recorded round must exist in the ledger.
    _answer(repo, "ENG-1", gap, "Fix it", ["Fix it", "Leave it"])
    _answer(repo, "ENG-1", "Any remaining gap before we hand off?", "No",
            ["No", "Yes"])
    _cold_read(repo)

    code, out = run(repo, "record_grill_from_json.py", "--gate", "plan",
                    "--input", str(payload), "--input-digest", str(plan))
    assert code != 0, out
    assert "grill confirm" in out, out
    # It must say WHY, or it reads as one more gate rather than the reason.
    assert "not the version anyone read" in out, out


def test_the_recorder_check_binds_to_the_confirmed_bytes(repo: Path):
    """Ordering alone would let the artifact be amended AGAIN after confirming.

    The receipt carries the digest of exactly what the bounded read was shown,
    and the recorder re-resolves the artifact through the receipt's own
    `--file` so a path difference can never cause a false refusal.
    """
    source = (HARNESS / "factory" / "scripts" / "record_grill_from_json.py"
              ).read_text(encoding="utf-8")
    flat = " ".join(source.split())
    assert 'receipt.get("file_arg")' in flat
    assert '_artifact_digest(artifact) != receipt.get("artifact_sha256")' in flat


def test_the_confirm_receipt_round_trips(repo: Path):
    from forge_cli.grill import confirm_receipt_path  # noqa: E402
    _seed(repo)
    path = confirm_receipt_path(repo, "plan", "")
    assert path.name == "plan.json"
    assert path.parent.name == "confirms"
    # Task gates key by task, so two tasks cannot share one receipt.
    assert confirm_receipt_path(repo, "task", "T1").name == "task-T1.json"


# -------------------------------------------------------- the contracts agree


def test_the_griller_contract_no_longer_says_loop(repo: Path):
    text = (HARNESS / "factory" / "prompts" / "griller.md").read_text(
        encoding="utf-8")
    flat = " ".join(text.split())
    assert "Codex grill again, until a round is clean" not in flat
    assert "ONE COLD READ PER GATE" in flat
    assert "forge grill confirm" in flat
    # The cost of one read has to be stated, not buried.
    assert "is not caught by a second reader at this gate" in flat


def test_the_adapter_no_longer_says_loop_until_clean(repo: Path):
    text = (HARNESS / ".claude" / "CLAUDE.md").read_text(encoding="utf-8")
    flat = " ".join(text.split())
    assert "loop until clean AND stable" not in flat
    assert "grill confirm" in flat
    # check_dual_runtime caps this file; a rewrite that grew it would fail CI
    # somewhere far from here.
    assert len(text.splitlines()) <= 40


def test_forge_next_describes_one_read(repo: Path):
    text = (HARNESS / "factory" / "scripts" / "forge_cli" / "phase.py"
            ).read_text(encoding="utf-8")
    flat = " ".join(text.split())
    assert "LOOP until a round" not in flat
    assert "grill confirm --gate task" in flat


def test_no_confirm_when_the_artifact_never_moved(repo: Path, tmp_path: Path):
    """A finding resolved WITHOUT touching the artifact costs no extra read.

    The recorder already refuses a pass with unresolved findings, so a listed
    gap can mean "the human confirmed what the plan already said". Charging a
    Codex launch for that is the ceremony that gets routed around, and it is
    avoidable: the cold read stamps the digest of what it was shown, so
    "was this amended?" is answerable from mechanism rather than from the
    coordinator's account.
    """
    _seed(repo)
    gap = "the plan never says who owns stock"
    plan = repo / "plan.md"
    plan.write_text("# Plan\nSAP owns stock.\n", encoding="utf-8")

    from forge_cli.grill import _artifact_digest, _artifact_text  # noqa: E402
    _, artifact = _artifact_text(repo, "plan", "", str(plan))
    _cold_read_with_digest(repo, _artifact_digest(artifact))

    payload = tmp_path / "grill.json"
    payload.write_text(json.dumps(_grill_payload([gap])), encoding="utf-8")
    _answer(repo, "ENG-1", gap, "Fix it", ["Fix it", "Leave it"])
    _answer(repo, "ENG-1", "Any remaining gap before we hand off?", "No",
            ["No", "Yes"])

    code, out = run(repo, "record_grill_from_json.py", "--gate", "plan",
                    "--input", str(payload), "--input-digest", str(plan))
    assert code == 0, out


def test_an_amended_artifact_is_refused_even_with_the_same_findings(
        repo: Path, tmp_path: Path):
    """The byte check is what makes the shortcut above safe."""
    _seed(repo)
    gap = "the plan never says who owns stock"
    plan = repo / "plan.md"
    plan.write_text("# Plan\n", encoding="utf-8")

    from forge_cli.grill import _artifact_digest, _artifact_text  # noqa: E402
    _, artifact = _artifact_text(repo, "plan", "", str(plan))
    _cold_read_with_digest(repo, _artifact_digest(artifact))
    plan.write_text("# Plan\nSAP owns stock.\n", encoding="utf-8")  # amended

    payload = tmp_path / "grill.json"
    payload.write_text(json.dumps(_grill_payload([gap])), encoding="utf-8")
    _answer(repo, "ENG-1", gap, "Fix it", ["Fix it", "Leave it"])
    _answer(repo, "ENG-1", "Any remaining gap before we hand off?", "No",
            ["No", "Yes"])

    code, out = run(repo, "record_grill_from_json.py", "--gate", "plan",
                    "--input", str(payload), "--input-digest", str(plan))
    assert code != 0, out
    assert "grill confirm" in out, out


def test_findings_with_no_ledgered_cold_read_record_unchanged(
        repo: Path, tmp_path: Path):
    """Never refuse blind.

    With no stamped cold read there is nothing to compare, so "was this
    amended?" is unanswerable here. The cold-read requirement is enforced by
    `grill run`; guessing at record time would refuse grills that predate this
    mechanism entirely.
    """
    _seed(repo)
    gap = "the plan never says who owns stock"
    plan = repo / "plan.md"
    plan.write_text("# Plan\n", encoding="utf-8")
    payload = tmp_path / "grill.json"
    payload.write_text(json.dumps(_grill_payload([gap])), encoding="utf-8")
    _answer(repo, "ENG-1", gap, "Fix it", ["Fix it", "Leave it"])
    _answer(repo, "ENG-1", "Any remaining gap before we hand off?", "No",
            ["No", "Yes"])

    code, out = run(repo, "record_grill_from_json.py", "--gate", "plan",
                    "--input", str(payload), "--input-digest", str(plan))
    assert code == 0, out


# ------------------------------------------------------ the whole way through


def test_a_plan_still_saves_and_approves_through_the_new_flow(
        repo: Path, tmp_path: Path):
    """draft -> one cold read -> answers -> amend -> confirm -> record -> save.

    The gates bind the recorded grill to the plan's digest, so this is the
    sequence that would break first if the confirm requirement were wrong: a
    grill that cannot be recorded is a plan that can never be saved.
    """
    from test_gates import (  # noqa: E402
        ensure_story, intake, log_grill_rounds, plan_draft, record_grill,
        run_state, sign_off,
    )
    from forge_cli.grill import (  # noqa: E402
        _artifact_digest, _artifact_text, confirm_receipt_path,
    )

    sign_off(repo)
    intake(repo)
    ensure_story(repo, "ENG-1", "Invoices")

    # 1. The dev drafts a plan.
    draft = tmp_path / "plan.md"
    draft.write_text(plan_draft(repo), encoding="utf-8")

    # 2. ONE cold read, stamping the bytes it was shown -- what `grill run`
    #    records through the ledgered launcher.
    _, read_bytes = _artifact_text(repo, "plan", "", str(draft))
    cold_at = "2026-09-07T10:00:00+00:00"
    _cold_read_with_digest(repo, _artifact_digest(read_bytes), at=cold_at)

    # 3. A second cold read is now refused, and names the way forward.
    try:
        _refuse(repo)
    except SystemExit:
        pass
    else:
        raise AssertionError("a second cold read was allowed")

    # 4. Its findings go to the human INSIDE this grill.
    gap = "the plan never says which service owns invoice numbering"
    rounds = [
        {"question": gap, "options": ["Ledger owns it", "Billing owns it"],
         "chosen": "Ledger owns it"},
        {"question": "Any remaining gap before we hand off?",
         "options": ["No", "Yes"], "chosen": "No", "frontier_empty": True},
    ]
    code, out = log_grill_rounds(repo, rounds)
    assert code == 0, out

    # 5. The plan is amended ONCE, to what the human decided.
    from test_gates import PLAN_BODY  # noqa: E402
    draft.write_text(
        plan_draft(repo, body=PLAN_BODY
                   + "\nThe ledger service owns invoice numbering.\n"),
        encoding="utf-8")

    # 6. The bounded confirm re-reads the amendment -- what `grill confirm`
    #    leaves behind after its launch.
    _, amended = _artifact_text(repo, "plan", "", str(draft))
    receipt = confirm_receipt_path(repo, "plan", "")
    receipt.parent.mkdir(parents=True, exist_ok=True)
    load_factory_lib(repo).dump_json(receipt, {
        "gate": "plan", "task_id": "", "at": "2026-09-07T12:00:00+00:00",
        "cold_read_at": cold_at, "file_arg": str(draft),
        "artifact_sha256": _artifact_digest(amended),
        "questions_confirmed": len(rounds),
    })

    # 7. The grill records -- findings and all.
    code, out = record_grill(
        repo, "plan", digest_of=draft, rounds=rounds, gaps=[gap],
        resolutions=["The ledger service owns invoice numbering."],
        citations=[{"finding": gap, "source": "docs/architecture/"}])
    assert code == 0, out

    # 8. And the plan saves, then approves, then saves as approved.
    code, out = run(repo, "forge.py", "plan", "save", "--from", str(draft),
                    "--story", "ENG-1")
    assert code != 0 and "awaiting-approval" in out, out

    active = next((repo / "plans" / "active").glob("ENG-1-*.md"))
    # The awaiting copy is a different file, so it needs its own grill --
    # unchanged by this PR, and the confirm must follow the bytes.
    _, awaiting = _artifact_text(repo, "plan", "", str(active))
    load_factory_lib(repo).dump_json(receipt, {
        "gate": "plan", "task_id": "", "at": "2026-09-07T12:30:00+00:00",
        "cold_read_at": cold_at, "file_arg": str(active),
        "artifact_sha256": _artifact_digest(awaiting),
        "questions_confirmed": len(rounds),
    })
    code, out = log_grill_rounds(repo, rounds)
    assert code == 0, out
    code, out = record_grill(
        repo, "plan", digest_of=active, rounds=rounds, gaps=[gap],
        resolutions=["The ledger service owns invoice numbering."],
        citations=[{"finding": gap, "source": "docs/architecture/"}])
    assert code == 0, out

    code, out = run(repo, "forge.py", "plan", "approve", "--by", "Nandu")
    assert code == 0, out
    code, out = run(repo, "forge.py", "plan", "save", "--from", str(active),
                    "--story", "ENG-1")
    assert code == 0, out
    assert run_state(repo)["plan_status"] == "approved"
