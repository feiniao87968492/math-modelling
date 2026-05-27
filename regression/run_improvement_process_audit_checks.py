from __future__ import annotations

from pathlib import Path

REQUIRED_REFERENCES = {
    "regression/improvement-finding-id-consistency.md": [
        "Finding ID Consistency",
        "must match the F-IDs",
        "renumbered F-IDs",
    ],
    "regression/improvement-decision-preload-coverage.md": [
        "Decision Preload Must Cover All Critique Blocking Risks",
        "Pre-load Skepticism BLOCKING risks",
        "silently drops a Blocking risk",
    ],
    "regression/improvement-frontier-no-premature-skepticism-tag.md": [
        "Frontier Status Tags Must Wait For Skepticism Review",
        "before `reviews/improvement-round-N-skepticism.md` is written",
        "process audit defect",
    ],
}


def check_required_references(root: Path) -> dict:
    missing = []
    checked_files = []
    for relative_path, needles in REQUIRED_REFERENCES.items():
        path = root / relative_path
        checked_files.append(relative_path)
        if not path.exists():
            missing.append({"file": relative_path, "missing": "file"})
            continue
        content = path.read_text(encoding="utf-8")
        for needle in needles:
            if needle not in content:
                missing.append({"file": relative_path, "missing": needle})
    return {"ok": not missing, "missing": missing, "checked_files": checked_files}


def simulate_finding_id_check(scenario: dict) -> dict:
    critique_ids = set(scenario.get("critique_finding_ids", []))
    round_n_ids = set(scenario.get("round_n_finding_ids", []))
    frontier_ids = set(scenario.get("frontier_finding_ids", []))
    decision_option_targets = scenario.get("decision_option_target_ids", [])

    drift = []
    if critique_ids and round_n_ids and not round_n_ids.issubset(critique_ids):
        drift.append("round_n_has_unknown_F_ids")
    if critique_ids and frontier_ids and not frontier_ids.issubset(critique_ids):
        drift.append("frontier_has_unknown_F_ids")
    for target in decision_option_targets:
        if target not in critique_ids:
            drift.append(f"decision_option_targets_unknown_F:{target}")

    if drift:
        return {"status": "BLOCKED", "drift": drift}
    return {"status": "PASS", "drift": []}


def simulate_decision_preload_coverage(scenario: dict) -> dict:
    critique_blocking = set(scenario.get("critique_blocking_ids", []))
    preload_blocking = set(scenario.get("decision_preload_blocking_ids", []))
    critique_findings = set(scenario.get("critique_finding_ids", []))
    decision_option_targets = set(scenario.get("decision_option_target_ids", []))

    missing = []
    dropped = critique_blocking - preload_blocking
    if dropped:
        missing.append({"missing_blocking": sorted(dropped)})

    uncovered_findings = critique_findings - decision_option_targets
    if uncovered_findings:
        missing.append({"uncovered_findings": sorted(uncovered_findings)})

    if missing:
        return {"status": "BLOCKED", "gaps": missing}
    return {"status": "PASS", "gaps": []}


def simulate_frontier_premature_tag_check(scenario: dict) -> dict:
    skepticism_review_present = scenario.get("skepticism_review_present", False)
    frontier_entries = scenario.get("frontier_entries", [])

    violations = []
    for entry in frontier_entries:
        text = entry.get("annotation", "")
        cites_skepticism_risk = (
            "blocked by Skepticism" in text
            or "Skepticism B" in text
            or "per Skepticism" in text
        )
        neutral_placeholder = "pending Skepticism review" in text
        if cites_skepticism_risk and not neutral_placeholder and not skepticism_review_present:
            violations.append({
                "entry": entry.get("id", "<unnamed>"),
                "annotation": text,
                "reason": "frontier cites Skepticism risk before Skepticism review file exists",
            })

    if violations:
        return {"status": "BLOCKED", "violations": violations}
    return {"status": "PASS", "violations": []}
