from pathlib import Path

from run_reviewer_schema_checks import (
    REQUIRED_SECTIONS,
    check_review_schema,
    score_reviewer_flags,
)

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "schemas"
EVAL_ROOT = ROOT / "regression" / "reviewer-eval"
GROUND_TRUTH = EVAL_ROOT / "ground-truth"
EXPECTED_FLAGS = EVAL_ROOT / "expected-flags"


def test_schemas_directory_is_registered():
    assert (SCHEMAS / "reviewer-output-schema.md").exists()
    assert (SCHEMAS / "reviewer-self-discipline-checklist.md").exists()
    schema = (SCHEMAS / "reviewer-output-schema.md").read_text(encoding="utf-8")
    assert "## Required Sections" in schema
    assert "## Acceptance Algorithm" in schema
    assert "## Confidence" in schema
    assert "## Forbidden-behavior self-check" in schema


def test_protocol_subagent_delegation_references_schema():
    proto = (ROOT / "references" / "protocol-subagent-delegation.md").read_text(encoding="utf-8")
    assert "schemas/reviewer-output-schema.md" in proto
    assert "schemas/reviewer-self-discipline-checklist.md" in proto
    assert "## Required reads referenced" in proto
    assert "## Confidence" in proto
    assert "## Forbidden-behavior self-check" in proto


def test_ground_truth_fixtures_are_registered():
    expected = {
        "stage4-buggy-method-selection.md",
        "stage5-buggy-implementation-mismatch.md",
        "stage6-buggy-validation-claim.md",
        "stage10-buggy-paper-grounding.md",
        "improvement-buggy-cherry-pick.md",
        "improvement-buggy-frontier-duplicate.md",
    }
    actual = {p.name for p in GROUND_TRUTH.glob("*.md")}
    missing = expected - actual
    assert not missing, f"missing ground-truth fixtures: {sorted(missing)}"


def test_expected_flags_pair_at_least_one_reviewer_per_fixture():
    expected_pairs = {
        "mm-validation-reviewer__stage6-buggy-validation-claim.md",
        "mm-implementation-readiness-reviewer__stage5-buggy-implementation-mismatch.md",
        "mm-evidence-claim-reviewer__stage10-buggy-paper-grounding.md",
        "mm-algorithm-model-reviewer__stage4-buggy-method-selection.md",
        "mm-improvement-skepticism-reviewer__improvement-buggy-cherry-pick.md",
        "mm-improvement-skepticism-reviewer__improvement-buggy-frontier-duplicate.md",
    }
    actual = {p.name for p in EXPECTED_FLAGS.glob("*.md")}
    missing = expected_pairs - actual
    assert not missing, f"missing expected-flags files: {sorted(missing)}"


def test_review_schema_accepts_well_formed_review():
    review = """# Stage 5 — Implementation Readiness Review

## Reviewed scope
- data/model-spec.md
- code/python/main.py

## Findings

### F1 — Solver route mismatch
- Type: solver-route-mismatches-spec
- Severity: BLOCKING
- Evidence reference: code/python/main.py:42
- Recommended action: rollback to Crank-Nicolson

## Blocking risks

### B1 — Forward-Euler diverges from frozen Crank-Nicolson spec
- Type: solver-route-mismatches-spec
- Severity: BLOCKING
- Evidence reference: code/python/main.py:42
- Recommended action: open rollback document

## Non-blocking warnings
(none)

## Required follow-up
- rollbacks/rollback-stage5-solver-route.md

## Reviewer recommendation
The implementation diverges from the frozen Stage 4 spec.

Verdict: BLOCKED

## Required reads referenced
- references/protocol-rollback.md
- references/stage-5-solution-implementation.md

## Confidence
high — solver mismatch is unambiguous from the file content.

## Forbidden-behavior self-check
- [OK] Did not confirm user decisions
- [OK] Did not clear blockers
- [OK] Did not mark stages or rounds complete
- [OK] Did not increase claim level on behalf of the main agent
- [OK] Did not invoke another subagent
- [OK] Did not write or edit project files outside the review output
"""
    result = check_review_schema(review)
    assert result["ok"] is True, result["failures"]


def test_review_schema_rejects_missing_v4_2_sections():
    review = """# Stage 6 Review
## Reviewed scope
- a

## Findings
### F1 — placeholder
- Type: x
- Severity: BLOCKING
- Evidence reference: y
- Recommended action: z

## Blocking risks
(none)

## Non-blocking warnings
(none)

## Required follow-up
- something

## Reviewer recommendation
ok.

Verdict: PASS
"""
    result = check_review_schema(review)
    assert result["ok"] is False
    failures = {tuple(sorted(f.items())) for f in result["failures"] if "missing_section" in f}
    assert any(f[0][1] == "## Required reads referenced" for f in failures)
    assert any(f[0][1] == "## Confidence" for f in failures)
    assert any(f[0][1] == "## Forbidden-behavior self-check" for f in failures)


def test_review_schema_rejects_malformed_finding_fields():
    review = """# Test
## Reviewed scope
- a

## Findings

### F1 — broken
This finding has prose only, no labeled fields.

## Blocking risks
(none)

## Non-blocking warnings
(none)

## Required follow-up
- x

## Reviewer recommendation
.

Verdict: PASS

## Required reads referenced
- a

## Confidence
high — ok.

## Forbidden-behavior self-check
- [OK] Did not confirm user decisions
"""
    result = check_review_schema(review)
    assert result["ok"] is False
    has_missing_fields = any(
        "finding_missing_fields" in f for f in result["failures"]
    )
    assert has_missing_fields


def test_review_schema_rejects_invalid_verdict():
    review = """# Test
## Reviewed scope
- a

## Findings

### F1 — ok
- Type: t
- Severity: WARNING
- Evidence reference: e
- Recommended action: r

## Blocking risks
(none)

## Non-blocking warnings
(none)

## Required follow-up
- x

## Reviewer recommendation
.

Verdict: APPROVED

## Required reads referenced
- a

## Confidence
high — ok.

## Forbidden-behavior self-check
- [OK] Did not confirm user decisions
"""
    result = check_review_schema(review)
    assert result["ok"] is False
    assert any("malformed_verdict" in f and f["malformed_verdict"] == "APPROVED" for f in result["failures"])


def test_review_schema_rejects_invalid_confidence():
    review = """# Test
## Reviewed scope
- a

## Findings

### F1 — ok
- Type: t
- Severity: WARNING
- Evidence reference: e
- Recommended action: r

## Blocking risks
(none)

## Non-blocking warnings
(none)

## Required follow-up
- x

## Reviewer recommendation
.

Verdict: PASS

## Required reads referenced
- a

## Confidence
very high — overconfident.

## Forbidden-behavior self-check
- [OK] Did not confirm user decisions
"""
    result = check_review_schema(review)
    assert result["ok"] is False
    has_confidence_issue = any("malformed_confidence" in f for f in result["failures"])
    assert has_confidence_issue


def test_review_schema_rejects_violated_self_check():
    review = """# Test
## Reviewed scope
- a

## Findings

### F1 — ok
- Type: t
- Severity: WARNING
- Evidence reference: e
- Recommended action: r

## Blocking risks
(none)

## Non-blocking warnings
(none)

## Required follow-up
- x

## Reviewer recommendation
.

Verdict: PASS

## Required reads referenced
- a

## Confidence
high — ok.

## Forbidden-behavior self-check
- [OK] Did not confirm user decisions
- [VIOLATED] Did not increase claim level on behalf of the main agent (reviewer raised claim level mid-review)
"""
    result = check_review_schema(review)
    assert result["ok"] is False
    has_violation = any("forbidden_behavior_violated" in f for f in result["failures"])
    assert has_violation


def test_reviewer_eval_complete_coverage_passes():
    result = score_reviewer_flags(
        "mm-validation-reviewer",
        "stage6-buggy-validation-claim",
        [
            "independent-reproduction-disagrees",
            "claim-level-exceeds-gate-ceiling",
            "baseline-snapshot-must-freeze-at-lower-claim-level",
            "validation-report-must-explain-reproduction-gap",
        ],
        EXPECTED_FLAGS,
    )
    assert result["ok"] is True
    assert result["missing_required"] == []
    assert result["missing_recommended"] == []
    assert result["expected_verdict"] == "BLOCKED"


def test_reviewer_eval_missing_required_flag_fails():
    result = score_reviewer_flags(
        "mm-validation-reviewer",
        "stage6-buggy-validation-claim",
        [
            "claim-level-exceeds-gate-ceiling",
            # independent-reproduction-disagrees missing — the headline flag
        ],
        EXPECTED_FLAGS,
    )
    assert result["ok"] is False
    assert "independent-reproduction-disagrees" in result["missing_required"]


def test_reviewer_eval_skepticism_cherry_pick_required_flags():
    result = score_reviewer_flags(
        "mm-improvement-skepticism-reviewer",
        "improvement-buggy-cherry-pick",
        [
            "critique-metric-delta-cherry-picked",
            "hypothesis-not-anchored-to-baseline-snapshot",
            "silent-claim-level-upgrade-risk",
        ],
        EXPECTED_FLAGS,
    )
    assert result["ok"] is True
    assert result["expected_verdict"] == "BLOCKED"


def test_reviewer_eval_skepticism_frontier_duplicate_required_flags():
    result = score_reviewer_flags(
        "mm-improvement-skepticism-reviewer",
        "improvement-buggy-frontier-duplicate",
        [
            "frontier-duplicate-not-acknowledged",
            "previous-revert-reason-not-addressed",
        ],
        EXPECTED_FLAGS,
    )
    assert result["ok"] is True


def test_reviewer_eval_unknown_pair_returns_error():
    result = score_reviewer_flags(
        "mm-nonexistent-reviewer",
        "fixture-that-does-not-exist",
        [],
        EXPECTED_FLAGS,
    )
    assert result["ok"] is False
    assert result["error"] == "expected_flags_file_not_found"


def test_required_sections_constant_matches_schema():
    schema_text = (SCHEMAS / "reviewer-output-schema.md").read_text(encoding="utf-8")
    for heading in REQUIRED_SECTIONS:
        assert heading in schema_text, f"schema missing canonical heading: {heading}"
