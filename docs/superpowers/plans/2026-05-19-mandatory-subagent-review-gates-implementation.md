# Mandatory Subagent Review Gates Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn the four fixed reviewer checkpoints in `math-modeling-v4` into mandatory hard gates that block continuation when the required reviewer artifact is missing.

**Architecture:** Enforce the change at three layers: dispatcher/package rules, delegation protocol, and affected stage contracts. Add regression coverage for both documentation contracts and behavior contracts so missing fixed-review artifacts block Stage 5 and export flow instead of letting the main agent self-review and continue.

**Tech Stack:** Markdown documentation, Python `pytest` regression helpers

---

## File Map

- Modify: `C:\Users\zty\.agents\skills\math-modeling-v4\SKILL.md`
- Modify: `C:\Users\zty\.agents\skills\math-modeling-v4\CLAUDE.md`
- Modify: `C:\Users\zty\.agents\skills\math-modeling-v4\references\protocol-subagent-delegation.md`
- Modify: `C:\Users\zty\.agents\skills\math-modeling-v4\references\stage-4-model-spec.md`
- Modify: `C:\Users\zty\.agents\skills\math-modeling-v4\references\stage-5-solution-implementation.md`
- Modify: `C:\Users\zty\.agents\skills\math-modeling-v4\references\stage-6-independent-validation.md`
- Modify: `C:\Users\zty\.agents\skills\math-modeling-v4\references\stage-10-paper-materials.md`
- Modify: `C:\Users\zty\.agents\skills\math-modeling-v4\regression\test_markdown_first_contracts.py`
- Modify: `C:\Users\zty\.agents\skills\math-modeling-v4\regression\command_readiness_gate_flow.py`
- Modify: `C:\Users\zty\.agents\skills\math-modeling-v4\regression\command_export_flow.py`
- Modify: `C:\Users\zty\.agents\skills\math-modeling-v4\regression\test_readiness_gate_command_flow.py`
- Modify: `C:\Users\zty\.agents\skills\math-modeling-v4\regression\test_export_command_flow.py`

### Task 1: Add failing contract tests for mandatory fixed-review gates

**Files:**
- Modify: `C:\Users\zty\.agents\skills\math-modeling-v4\regression\test_markdown_first_contracts.py`
- Test: `C:\Users\zty\.agents\skills\math-modeling-v4\regression\test_markdown_first_contracts.py`

- [ ] **Step 1: Extend the documentation contract tests with hard-gate assertions**

Append a new test like this:

```python
def test_fixed_review_points_are_mandatory_hard_gates():
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    claude = (ROOT / "CLAUDE.md").read_text(encoding="utf-8")
    protocol = (ROOT / "references" / "protocol-subagent-delegation.md").read_text(
        encoding="utf-8"
    )
    stage5 = (ROOT / "references" / "stage-5-solution-implementation.md").read_text(
        encoding="utf-8"
    )
    stage10 = (ROOT / "references" / "stage-10-paper-materials.md").read_text(
        encoding="utf-8"
    )

    assert "fixed review points are mandatory review gates" in skill
    assert "actual subagent-produced review artifacts" in claude
    assert "## Mandatory Review Gates" in protocol
    assert "reviews/stage5-implementation-readiness-review.md" in protocol
    assert "reviews/stage10-evidence-claim-review.md" in protocol
    assert "must stop and spawn the required reviewer" in protocol
    assert "reviews/stage5-implementation-readiness-review.md" in stage5
    assert "reviews/stage10-evidence-claim-review.md" in stage10
```

- [ ] **Step 2: Run the focused test and verify it fails**

Run:

```bash
python -m pytest regression/test_markdown_first_contracts.py -q
```

Expected:

```text
FAIL
```

The failure should indicate the new hard-gate wording is not yet present.

- [ ] **Step 3: Commit the failing contract test**

```bash
git add regression/test_markdown_first_contracts.py
git commit -m "test: add mandatory fixed-review gate contract assertions"
```

### Task 2: Add failing behavior tests for Stage 5 and export blockers

**Files:**
- Modify: `C:\Users\zty\.agents\skills\math-modeling-v4\regression\test_readiness_gate_command_flow.py`
- Modify: `C:\Users\zty\.agents\skills\math-modeling-v4\regression\test_export_command_flow.py`
- Test: `C:\Users\zty\.agents\skills\math-modeling-v4\regression\test_readiness_gate_command_flow.py`
- Test: `C:\Users\zty\.agents\skills\math-modeling-v4\regression\test_export_command_flow.py`

- [ ] **Step 1: Add a failing Stage 5 missing-review blocker test**

Add a test similar to:

```python
def test_stage5_blocks_when_implementation_review_is_missing():
    result = explain_stage_command(
        command="/math-modeling stage 5",
        fixed_reviews={"stage5": False},
        pending_decisions=[],
    )

    assert result["ok"] is False
    assert result["review_required"] is True
    assert result["required_review_file"] == "reviews/stage5-implementation-readiness-review.md"
```

- [ ] **Step 2: Add a failing export missing-review blocker test**

Add a test similar to:

```python
def test_export_blocks_when_evidence_claim_review_is_missing():
    result = explain_export_command(
        command="/math-modeling export",
        final_gate_passed=True,
        claims_supported=True,
        pending_decisions=[],
        fixed_reviews={"stage10": False},
    )

    assert result["ok"] is False
    assert result["export_allowed"] is False
    assert result["review_required"] is True
    assert result["required_review_file"] == "reviews/stage10-evidence-claim-review.md"
```

- [ ] **Step 3: Run the two focused tests and verify they fail**

Run:

```bash
python -m pytest regression/test_readiness_gate_command_flow.py regression/test_export_command_flow.py -q
```

Expected:

```text
FAIL
```

The failure should show the helpers do not yet enforce fixed review files.

- [ ] **Step 4: Commit the failing behavior tests**

```bash
git add regression/test_readiness_gate_command_flow.py regression/test_export_command_flow.py
git commit -m "test: require fixed review artifacts in stage5 and export flows"
```

### Task 3: Harden dispatcher and package rules

**Files:**
- Modify: `C:\Users\zty\.agents\skills\math-modeling-v4\SKILL.md`
- Modify: `C:\Users\zty\.agents\skills\math-modeling-v4\CLAUDE.md`

- [ ] **Step 1: Update `SKILL.md` expert-review language**

Replace the soft policy wording with explicit hard-gate wording. The resulting section should include lines like:

```md
## Expert Review Policy

Default mode is main-agent execution with expert review.

- The main agent owns workflow synthesis, user-facing decisions, artifact updates, and final judgement on whether work can continue.
- Expert subagents are reviewers, not stage owners.
- Fixed review points are mandatory review gates.
- If a required fixed-review artifact is missing, the main agent must stop and spawn the required reviewer before proceeding.
- The main agent must not satisfy a fixed review gate by reading reviewer profiles and performing the review itself.
```

- [ ] **Step 2: Update `CLAUDE.md` package rules**

Add explicit non-bypass wording like:

```md
- Reviewer profiles are not sufficient by themselves to satisfy fixed review gates.
- Fixed review gates require actual subagent-produced review artifacts in `reviews/`.
- The main agent must not self-review past a fixed review gate.
```

- [ ] **Step 3: Run the contract test to confirm these assertions now pass where applicable**

Run:

```bash
python -m pytest regression/test_markdown_first_contracts.py -q
```

Expected:

```text
still failing
```

At this point the protocol and stage docs should still be the remaining failure source.

- [ ] **Step 4: Commit the dispatcher and package-rule updates**

```bash
git add SKILL.md CLAUDE.md
git commit -m "docs: make fixed reviewer checkpoints hard gates"
```

### Task 4: Harden delegation protocol and stage contracts

**Files:**
- Modify: `C:\Users\zty\.agents\skills\math-modeling-v4\references\protocol-subagent-delegation.md`
- Modify: `C:\Users\zty\.agents\skills\math-modeling-v4\references\stage-4-model-spec.md`
- Modify: `C:\Users\zty\.agents\skills\math-modeling-v4\references\stage-5-solution-implementation.md`
- Modify: `C:\Users\zty\.agents\skills\math-modeling-v4\references\stage-6-independent-validation.md`
- Modify: `C:\Users\zty\.agents\skills\math-modeling-v4\references\stage-10-paper-materials.md`

- [ ] **Step 1: Add a `Mandatory Review Gates` section to the protocol**

Insert a section like:

```md
## Mandatory Review Gates

| Workflow point | Required reviewer | Required file |
|---|---|---|
| Before algorithm/model freeze | Algorithm/Model Reviewer | `reviews/stage4-algorithm-model-review.md` |
| Before implementation/code writing | Implementation Readiness Reviewer | `reviews/stage5-implementation-readiness-review.md` |
| After main result generation | Validation Reviewer | `reviews/stage6-validation-review.md` |
| Before claim/export | Evidence/Claim Reviewer | `reviews/stage10-evidence-claim-review.md` |

If a required fixed-review artifact is missing, the main agent must stop and spawn the required reviewer before proceeding.
```

- [ ] **Step 2: Add explicit forbidden bypass wording**

Add or update the forbidden behavior section so it clearly says the main agent must not:

```md
- satisfy a fixed review gate by only reading reviewer profile documents,
- self-review past a mandatory fixed-review checkpoint,
- treat a missing fixed review as a warning instead of a blocker.
```

- [ ] **Step 3: Update Stage 4, 5, 6, and 10 contracts**

Add blocking rules that mention the fixed files explicitly:

```md
Before algorithm/model freeze, `reviews/stage4-algorithm-model-review.md` must exist.
Before implementation code, `reviews/stage5-implementation-readiness-review.md` must exist.
After main result generation, `reviews/stage6-validation-review.md` must exist before downstream interpretation continues.
Before claim/export, `reviews/stage10-evidence-claim-review.md` must exist.
```

Place each rule in the relevant `## Blocking Rules` section and make the required next action explicit:

```md
If missing, stop and spawn the required reviewer subagent first.
```

- [ ] **Step 4: Run the contract test and verify it passes**

Run:

```bash
python -m pytest regression/test_markdown_first_contracts.py -q
```

Expected:

```text
PASS
```

- [ ] **Step 5: Commit the protocol and stage-contract updates**

```bash
git add references/protocol-subagent-delegation.md references/stage-4-model-spec.md references/stage-5-solution-implementation.md references/stage-6-independent-validation.md references/stage-10-paper-materials.md regression/test_markdown_first_contracts.py
git commit -m "docs: require mandatory fixed-review artifacts"
```

### Task 5: Implement behavior blockers in command-flow helpers

**Files:**
- Modify: `C:\Users\zty\.agents\skills\math-modeling-v4\regression\command_readiness_gate_flow.py`
- Modify: `C:\Users\zty\.agents\skills\math-modeling-v4\regression\command_export_flow.py`

- [ ] **Step 1: Extend the Stage 5 command helper**

Update the helper so it accepts a `fixed_reviews` input and blocks when Stage 5 review is missing:

```python
stage5_review_present = fixed_reviews.get("stage5", False)
if not stage5_review_present:
    return {
        "ok": False,
        "command": command,
        "review_required": True,
        "required_review_file": "reviews/stage5-implementation-readiness-review.md",
        "required_reviewer": "Implementation Readiness Reviewer",
        "blockers": ["missing mandatory fixed-review artifact"],
    }
```

- [ ] **Step 2: Extend the export helper**

Update the export helper so it blocks when Stage 10 review is missing:

```python
stage10_review_present = fixed_reviews.get("stage10", False)
if not stage10_review_present:
    return {
        "ok": False,
        "command": command,
        "review_required": True,
        "required_review_file": "reviews/stage10-evidence-claim-review.md",
        "required_reviewer": "Evidence/Claim Reviewer",
        "blockers": ["missing mandatory fixed-review artifact"],
        "export_allowed": False,
    }
```

- [ ] **Step 3: Run the focused behavior tests and verify they pass**

Run:

```bash
python -m pytest regression/test_readiness_gate_command_flow.py regression/test_export_command_flow.py -q
```

Expected:

```text
PASS
```

- [ ] **Step 4: Commit the helper updates**

```bash
git add regression/command_readiness_gate_flow.py regression/command_export_flow.py regression/test_readiness_gate_command_flow.py regression/test_export_command_flow.py
git commit -m "test: block stage5 and export without fixed reviews"
```

### Task 6: Run full regression and perform scope review

**Files:**
- Modify: all files from earlier tasks

- [ ] **Step 1: Run the full regression suite**

Run:

```bash
python -m pytest regression/test_markdown_first_contracts.py regression/test_readiness_gate_checks.py regression/test_readiness_gate_smoke_flow.py regression/test_readiness_gate_command_flow.py regression/test_gate_and_rollback_checks.py regression/test_export_command_flow.py regression/test_rollback_command_flow.py -q
```

Expected:

```text
all tests pass
```

- [ ] **Step 2: Review scope and non-goals**

Confirm:

- fixed review points are mandatory,
- specialist risk-triggered reviewers are still optional,
- reviewers are still not stage owners,
- no YAML state driver was reintroduced,
- old `math-modeling` package remains untouched.

- [ ] **Step 3: Commit the finished slice**

```bash
git add SKILL.md CLAUDE.md references/protocol-subagent-delegation.md references/stage-4-model-spec.md references/stage-5-solution-implementation.md references/stage-6-independent-validation.md references/stage-10-paper-materials.md regression/test_markdown_first_contracts.py regression/command_readiness_gate_flow.py regression/command_export_flow.py regression/test_readiness_gate_command_flow.py regression/test_export_command_flow.py
git commit -m "feat: enforce mandatory fixed review gates"
```

## Self-Review

### Spec coverage

- Hard-gate semantics in dispatcher/package rules: covered by Task 3.
- Mandatory review-gate protocol: covered by Task 4.
- Stage contract blockers: covered by Task 4.
- Behavior enforcement for Stage 5 and export: covered by Task 2 and Task 5.
- No legacy skill changes: enforced by Task 6 scope review.

### Placeholder scan

No placeholders remain. All changed files, assertions, and commands are explicit.

### Type consistency

The plan consistently uses the same fixed review files:

- `reviews/stage4-algorithm-model-review.md`
- `reviews/stage5-implementation-readiness-review.md`
- `reviews/stage6-validation-review.md`
- `reviews/stage10-evidence-claim-review.md`

No alternative names are introduced.
