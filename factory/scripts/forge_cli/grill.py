"""forge grill run — release the read-only cold reader through the ledger.

Grills were the one Codex release the harness could not see. A delegation
records a pid and a review now does too, so a launcher killed uncatchably is
still detectable afterwards; a grill went out through the plugin directly, so
nothing on the forge side knew it had ever started. That is backwards: the
grill is the release the coordinator is told to WATCH every single round.

Releasing it through `launch_companion` — the same launcher a delegation uses —
gives it the same treatment for free: the pid and process create-time are
ledgered before the wait, the process tree is reaped on exit, the argv is
pinned, and `forge codex status` reports it dead if its launcher was killed.

It stays READ-ONLY. `write=False` means no delegation lock is taken and the
row can never satisfy `stage done`, which matches on a write launch bound to a
task contract. The cold read returns findings; recording the gate remains the
coordinator's job through the ledger-matched recorder, exactly as before.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from factory_lib import load_json, repo_root, run_state_path
from grill_gates import FLOOR_IS_NOT_A_TARGET, get_gate

def _artifact_text(base: Path, gate: str, task_id: str,
                   file_arg: str = "") -> tuple[str, str]:
    """Ask the gate table where this gate's artifact lives.

    This used to be a hand-written if-chain that knew two of the six gates;
    the other four failed with "no artifact resolver yet" and sent the
    coordinator around the ledgered launcher, which is where the pid that
    makes a dead grill detectable gets recorded. A missing lookup silently
    cost liveness detection in an unrelated subsystem.
    """
    return get_gate(gate).locate(base, task_id, file_arg)


def _grill_skill_section() -> str:
    """The grill technique, INLINED rather than named.

    Naming it does not work for a Codex cold reader. What `doctor` installs
    into ~/.codex/skills/grill-me is a 164-byte STUB whose whole body is "Call
    the Skill tool with 'grilling'" — and `grilling`, the 2KB skill that holds
    the actual technique, is installed only on the Claude side. So a Codex
    reader told to load grill-me finds a pointer to a Skill tool its runtime
    does not have, and falls back to the harness contract alone.

    `_skill_text` already looks in BOTH runtimes' skill directories, which is
    what lets the Claude-side text travel to Codex inside the brief. Prefer the
    real skill, accept grill-me only when it is not merely the stub, and carry
    a written floor when neither is installed — the same reason delegate
    inlines ponytail instead of trusting a per-machine install.
    """
    from .delegate import _skill_text

    for name in ("grilling", "grill-me"):
        text = _skill_text(name)
        # The stub points at a tool the reader may not have; it is not technique.
        if text and "Call the Skill tool" not in text:
            return ("## Interrogation technique\n\n"
                    "Run the interrogation this way. The harness contract above "
                    "is the floor; this is the technique.\n\n" + text)
    return ("## Interrogation technique\n\n"
            "No grill skill is installed (`./forge doctor --fix` installs it). "
            "Interrogate to the harness contract above: one line of questioning "
            "at a time, press each answer until it is concrete and checkable, "
            "and surface every place the artifact leaves the reader to guess.")


def _lessons_section(base: Path, gate: str, task_id: str) -> str:
    """Lessons in force for the paths this task may touch.

    Task-gate only: it is the one gate whose artifact names a write scope, and
    a lesson list unrelated to the work would be noise the reader learns to
    skip.
    """
    if gate != "task" or not task_id:
        return ""
    try:
        from factory_lib import (
            load_json, protected_decomposition_state_path,
        )
        from .lessons import relevant_lessons
        tasks = load_json(protected_decomposition_state_path(base),
                          default={}).get("tasks", [])
        task = next((t for t in tasks if t.get("id") == task_id), None)
        scope = [str(entry) for entry in (task or {}).get("write_scope") or []]
        lessons = relevant_lessons(base, scope) if scope else []
    except Exception:
        return ""
    if not lessons:
        return ""
    lines = ["## Lessons already in force for these paths", "",
             "The plan must design AROUND these. A plan that ignores one is "
             "not merely unlucky later — it is wrong now, and saying so is "
             "part of this read.", ""]
    lines += [f"- {entry.get('lesson', '')}" for entry in lessons]
    return "\n".join(lines) + "\n"


# The brief travels to the launcher as a file; the reader's prompt budget is
# finite. Measured on a 44-round story the whole history was 14.5 KB, so this
# ceiling is a backstop, not a working limit.
SETTLED_BUDGET_CHARS = 60_000


def _settled_rounds(base: Path, gate: str) -> str:
    """Every question already answered for this story, and the answer.

    Read from the AskUserQuestion ledger the recorder validates against, not
    from a summary: a summary would be written by the party whose work is being
    audited, and it would break the provenance the recorder depends on.
    """
    try:
        from factory_lib import evidence_path, load_json, run_state_path
        story = load_json(run_state_path(base), default={}).get("issue_key", "")
        directories = [d for d in (
            evidence_path(base, story, "grill-rounds"),
            evidence_path(base, None, "grill-rounds"),
        ) if d.is_dir()]
    except Exception:
        return ""

    seen: set[tuple[str, str]] = set()
    answered: list[tuple[str, str, str]] = []
    for directory in dict.fromkeys(directories):
        for path in sorted(directory.glob("*.json")):
            try:
                record = load_json(path, default={})
            except Exception:
                # One unreadable record costs THAT record. Letting it escape
                # loses every settled answer, which is the failure this
                # section exists to prevent.
                continue
            if not isinstance(record, dict):
                continue
            when = str(record.get("at") or "")
            for entry in record.get("questions", []):
                if not isinstance(entry, dict):
                    continue
                question = str(entry.get("question") or "").strip()
                chosen = str(entry.get("chosen") or "").strip()
                if not question or not chosen:
                    continue  # an unanswered round settles nothing
                key = (question, chosen)
                if key in seen:
                    continue
                seen.add(key)
                answered.append((when, question, chosen))
    if not answered:
        return ""

    answered.sort(key=lambda row: row[0])
    lines = [f"- Q: {q}\n  A: {a}" for _, q, a in answered]

    # Oldest first when it must be cut, and SAID so. A brief that silently
    # drops content is how a chunked review lost its verdicts.
    omitted = 0
    while sum(len(line) for line in lines) > SETTLED_BUDGET_CHARS and len(lines) > 1:
        lines.pop(0)
        omitted += 1

    header = [
        "## Already answered on this story — verify, do not re-ask",
        "",
        "These questions were put to the human and answered. Two obligations:",
        "",
        "1. Do NOT raise them again as open questions. They are settled.",
        "2. DO check each answer still holds — that the artifact actually "
        "honours it, and that it does not contradict another answer, an "
        "accepted decision, or the constitution. An answer can be wrong, or "
        "right and never applied. Saying so is part of this read.",
        "",
    ]
    if omitted:
        header.append(
            f"[{omitted} earlier answered question(s) omitted for length — "
            "ask for them if a gap seems to depend on settled ground.]")
        header.append("")
    return "\n".join(header + lines) + "\n"


def _compose_brief(base: Path, gate: str, label: str, artifact: str,
                   task_id: str = "") -> str:
    contract = base / "factory" / "prompts" / "griller.md"
    contract_text = (contract.read_text(encoding="utf-8")
                     if contract.is_file() else "")
    skill_section = _grill_skill_section()
    return "\n".join([
        f"# Cold-read grill — gate: {gate} — {label}",
        "",
        "You did NOT write what follows. Read it cold, as an adversary trying "
        "to break the handover, never as its author defending it. You are "
        "READ-ONLY: return findings, change nothing.",
        "",
        skill_section,
        "",
        "## Harness grill contract",
        "",
        contract_text,
        "",
        _lessons_section(base, gate, task_id),
        _settled_rounds(base, gate),
        f"## The artifact under interrogation ({label})",
        "",
        artifact,
        "",
        "## What to return",
        "",
        "Findings only: contradictions, gaps, unstated assumptions, and "
        "anything a reader would have to guess. Say what would break and why. "
        "Do not record a gate — the coordinating session records it.",
        "",
        FLOOR_IS_NOT_A_TARGET,
        "",
    ])


def cmd_grill_run(args: argparse.Namespace) -> None:
    from .delegate import launch_companion, mode_run_config

    base = Path(args.repo).resolve() if args.repo else repo_root()
    gate = args.gate
    task_id = (args.task or "").strip()
    label, artifact = _artifact_text(
        base, gate, task_id, (getattr(args, "file", "") or "").strip())
    text = _compose_brief(base, gate, label, artifact, task_id)

    # Keyed apart from real task ids so a grill row can never be mistaken for
    # a task's delegation, and so concurrent grills of different gates do not
    # collide in the ledger.
    ledger_id = f"grill-{gate}" + (f"-{task_id}" if task_id else "")
    path = base / ".factory" / f"grill-brief-{gate}" \
        f"{'-' + task_id if task_id else ''}.md"
    model, effort, _bound = mode_run_config(base, "grill")

    launch_companion(
        base,
        task_id=ledger_id,
        text=text,
        path=path,
        task_sha256_value="",
        model=model,
        effort=effort,
        write=False,          # a cold read never writes, and never authorises
        story=load_json(run_state_path(base), default={}).get("issue_key", ""),
        print_only=bool(args.print_only),
    )
    if args.print_only:
        return
    print(f"NEXT: carry these findings into your own rounds, then record with "
          f"`python3 factory/scripts/record_grill_from_json.py --gate {gate}"
          f"{' --task ' + task_id if task_id else ''} --input <json>`")
