"""Reviewer schema acceptance + eval simulator for v4.2 工作项 2.

Two responsibilities:

1. `check_review_schema(review_text)` — text-level acceptance check against
   schemas/reviewer-output-schema.md. Detects missing sections, malformed
   findings, malformed verdict, malformed Confidence value, and any
   `[VIOLATED]` self-check items.

2. `score_reviewer_flags(reviewer_id, fixture_id, reviewer_output_flags)` —
   compares the actual flag set surfaced by a reviewer against the
   expected-flags fixture's Required flags. Returns a coverage report.

The simulators do not require an actual reviewer subagent run; they accept
pre-extracted text or flag lists so the regression suite remains fast and
deterministic.
"""
from __future__ import annotations

import re
from pathlib import Path

REQUIRED_SECTIONS = [
    "## Reviewed scope",
    "## Findings",
    "## Blocking risks",
    "## Non-blocking warnings",
    "## Required follow-up",
    "## Reviewer recommendation",
    "## Required reads referenced",
    "## Confidence",
    "## Forbidden-behavior self-check",
]

VALID_VERDICTS = {"PASS", "PASS_WITH_WARNINGS", "BLOCKED"}
VALID_CONFIDENCE = {"high", "medium", "low"}

FINDING_LABELED_FIELDS = ["Type:", "Severity:", "Evidence reference:", "Recommended action:"]


def check_review_schema(review_text: str) -> dict:
    failures = []

    for heading in REQUIRED_SECTIONS:
        if heading not in review_text:
            failures.append({"missing_section": heading})

    # Verdict line check
    verdict_match = re.search(r"^\s*Verdict:\s*([A-Z_]+)\s*$", review_text, re.MULTILINE)
    if not verdict_match:
        failures.append({"malformed_verdict": "Verdict: <PASS|PASS_WITH_WARNINGS|BLOCKED> line not found"})
    else:
        verdict_value = verdict_match.group(1)
        if verdict_value not in VALID_VERDICTS:
            failures.append({"malformed_verdict": verdict_value})

    # Confidence value check
    if "## Confidence" in review_text:
        confidence_section = _extract_section(review_text, "## Confidence")
        confidence_value = _confidence_value(confidence_section)
        if confidence_value not in VALID_CONFIDENCE:
            failures.append({"malformed_confidence": confidence_value or "(missing)"})

    # Findings labeled fields check
    findings_section = _extract_section(review_text, "## Findings")
    if findings_section:
        finding_blocks = _split_finding_blocks(findings_section)
        if not finding_blocks:
            failures.append({"findings_section_empty_or_unstructured": True})
        for idx, block in enumerate(finding_blocks):
            missing_fields = [f for f in FINDING_LABELED_FIELDS if f not in block]
            if missing_fields:
                failures.append(
                    {
                        "finding_missing_fields": {
                            "finding_index": idx,
                            "missing": missing_fields,
                        }
                    }
                )

    # Required reads referenced empty check
    rrr = _extract_section(review_text, "## Required reads referenced")
    if rrr is not None:
        bullet_lines = [
            line for line in rrr.splitlines() if line.strip().startswith(("- ", "* "))
        ]
        if not bullet_lines:
            failures.append({"required_reads_referenced_empty": True})

    # Forbidden-behavior self-check VIOLATED items
    self_check = _extract_section(review_text, "## Forbidden-behavior self-check")
    if self_check is not None:
        violated_lines = [line for line in self_check.splitlines() if "[VIOLATED]" in line]
        if violated_lines:
            failures.append({"forbidden_behavior_violated": violated_lines})

    return {
        "ok": not failures,
        "failures": failures,
    }


def score_reviewer_flags(
    reviewer_id: str,
    fixture_id: str,
    reviewer_output_flags: list,
    expected_flags_root: Path,
) -> dict:
    expected_path = expected_flags_root / f"{reviewer_id}__{fixture_id}.md"
    if not expected_path.exists():
        return {
            "ok": False,
            "error": "expected_flags_file_not_found",
            "looked_for": str(expected_path),
        }

    content = expected_path.read_text(encoding="utf-8")
    required = _flags_under_heading(content, "Required flags")
    recommended = _flags_under_heading(content, "Recommended additional flags")
    expected_verdict_match = re.search(
        r"^##\s+Verdict\s*$\s*\n+([A-Z_]+)", content, re.MULTILINE
    )
    expected_verdict = expected_verdict_match.group(1) if expected_verdict_match else None

    output_flags = set(reviewer_output_flags)
    required_set = set(required)
    recommended_set = set(recommended)

    missing_required = sorted(required_set - output_flags)
    missing_recommended = sorted(recommended_set - output_flags)

    return {
        "ok": not missing_required,
        "missing_required": missing_required,
        "missing_recommended": missing_recommended,
        "covered_required": sorted(required_set & output_flags),
        "covered_recommended": sorted(recommended_set & output_flags),
        "expected_verdict": expected_verdict,
    }


# ---------- helpers ----------


def _extract_section(text: str, heading: str) -> str | None:
    pattern = re.compile(
        rf"^{re.escape(heading)}\s*$(.*?)(?=^##\s|\Z)", re.MULTILINE | re.DOTALL
    )
    match = pattern.search(text)
    if not match:
        return None
    return match.group(1)


def _split_finding_blocks(findings_section: str) -> list[str]:
    blocks = re.split(r"^###\s+", findings_section, flags=re.MULTILINE)
    return [b for b in blocks[1:] if b.strip()]


def _confidence_value(section: str | None) -> str | None:
    if not section:
        return None
    for line in section.splitlines():
        line = line.strip()
        if not line:
            continue
        first_word = line.split(maxsplit=1)[0].lower().rstrip("—-—:.,")
        if first_word in VALID_CONFIDENCE:
            return first_word
    return None


def _flags_under_heading(content: str, heading_name: str) -> list[str]:
    pattern = re.compile(
        rf"^##\s+{re.escape(heading_name)}\s*$(.*?)(?=^##\s|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(content)
    if not match:
        return []
    body = match.group(1)
    flags = []
    for line in body.splitlines():
        line = line.strip()
        if line.startswith("- "):
            flag = line[2:].strip()
            # take only the leading flag id (drop trailing prose after a separator)
            for sep in [" — ", " - ", " – ", ":"]:
                if sep in flag:
                    flag = flag.split(sep, 1)[0].strip()
                    break
            flags.append(flag)
    return flags
