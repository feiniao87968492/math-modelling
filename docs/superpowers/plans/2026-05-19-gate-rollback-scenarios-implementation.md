# Gate And Rollback Scenarios Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add focused v4 scenario regressions that lock rollback-required behavior, export blocking, and final evidence gate pass conditions.

**Architecture:** Keep the implementation narrow and deterministic: one new regression helper, one pytest module, three scenario markdown files, and a small README update. Follow the existing v4 bootstrap pattern where workflow boundaries are protected by small pure-Python simulation helpers plus reference-presence checks.

**Tech Stack:** Markdown docs, Python regression helpers, pytest.

---

## File Structure Map

### Files to create

- `C:\Users\zty\.agents\skills\math-modeling-v4\regression\run_gate_and_rollback_checks.py` - deterministic helper for rollback/export/final gate scenario checks.
- `C:\Users\zty\.agents\skills\math-modeling-v4\regression\test_gate_and_rollback_checks.py` - pytest contract coverage for the new helper.
- `C:\Users\zty\.agents\skills\math-modeling-v4\regression\rollback-late-stage-structural-defect.md` - scenario anchor for rollback-required behavior.
- `C:\Users\zty\.agents\skills\math-modeling-v4\regression\export-blocked-by-pending-decision.md` - scenario anchor for blocked export.
- `C:\Users\zty\.agents\skills\math-modeling-v4\regression\final-evidence-gate-grounded-claims-only.md` - scenario anchor for evidence-gate alignment.

### Files to modify

- `C:\Users\zty\.agents\skills\math-modeling-v4\README.md` - add the new regression module to the documented test command.

---

### Task 1: Add failing tests for rollback/export/final-gate scenarios

**Files:**
- Create: `C:\Users\zty\.agents\skills\math-modeling-v4\regression\test_gate_and_rollback_checks.py`

- [ ] **Step 1: Write the failing test**

Create `regression/test_gate_and_rollback_checks.py` with:

```python
from pathlib import Path

from run_gate_and_rollback_checks import (
    check_required_references,
    simulate_export_gate,
    simulate_final_evidence_gate,
    simulate_rollback_decision,
)

ROOT = Path(__file__).resolve().parents[1]


def test_gate_and_rollback_references_are_registered():
    result = check_required_references(ROOT)
    assert result["ok"], result["missing"]


def test_late_stage_structural_defect_requires_rollback():
    result = simulate_rollback_decision(
        {
            "stage": 8,
            "defect_severity": "structural_revision",
            "downstream_patch_possible": True,
        }
    )
    assert result["status"] == "ROLLBACK_REQUIRED"
    assert result["rollback_path"] == "rollbacks/rollback-stage8-structural-defect.md"
    assert result["requires_user_confirmation"] is True


def test_export_is_blocked_by_pending_decision():
    result = simulate_export_gate(
        {
            "pending_decisions": ["decisions/decision-stage10-export.md"],
            "final_gate_status": "PASS",
            "claims_supported": True,
        }
    )
    assert result["status"] == "BLOCKED"
    assert "pending_decisions" in result["blockers"]


def test_final_evidence_gate_requires_grounded_claims():
    result = simulate_final_evidence_gate(
        {
            "pending_decisions": [],
            "claims_supported": False,
            "reviews_complete": True,
            "gate_checks_complete": True,
        }
    )
    assert result["status"] == "BLOCKED"
    assert "unsupported_claims" in result["blockers"]
```

- [ ] **Step 2: Run test to verify it fails**

Run:

```powershell
python -m pytest regression/test_gate_and_rollback_checks.py -q
```

Expected: FAIL with `ModuleNotFoundError: No module named 'run_gate_and_rollback_checks'`.

- [ ] **Step 3: Commit**

```bash
git add C:/Users/zty/.agents/skills/math-modeling-v4/regression/test_gate_and_rollback_checks.py
git commit -m "test: add failing gate and rollback scenario tests"
```

---

### Task 2: Implement the deterministic regression helper

**Files:**
- Create: `C:\Users\zty\.agents\skills\math-modeling-v4\regression\run_gate_and_rollback_checks.py`
- Test: `C:\Users\zty\.agents\skills\math-modeling-v4\regression\test_gate_and_rollback_checks.py`

- [ ] **Step 1: Write the minimal implementation**

Create `regression/run_gate_and_rollback_checks.py` with:

```python
from __future__ import annotations

from pathlib import Path

REQUIRED_REFERENCES = {
    "regression/rollback-late-stage-structural-defect.md": [
        "ROLLBACK_REQUIRED",
        "rollbacks/rollback-stage8-structural-defect.md",
    ],
    "regression/export-blocked-by-pending-decision.md": [
        "BLOCKED",
        "decisions/decision-stage10-export.md",
    ],
    "regression/final-evidence-gate-grounded-claims-only.md": [
        "PASS_WITH_WARNINGS",
        "BLOCKED",
        "unsupported_claims",
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


def simulate_rollback_decision(scenario: dict) -> dict:
    if scenario.get("defect_severity") == "structural_revision":
        return {
            "status": "ROLLBACK_REQUIRED",
            "rollback_path": "rollbacks/rollback-stage8-structural-defect.md",
            "requires_user_confirmation": True,
        }
    return {
        "status": "NO_ROLLBACK",
        "rollback_path": None,
        "requires_user_confirmation": False,
    }


def simulate_export_gate(scenario: dict) -> dict:
    blockers = []
    if scenario.get("pending_decisions"):
        blockers.append("pending_decisions")
    if scenario.get("final_gate_status") == "BLOCKED":
        blockers.append("final_gate_blocked")
    if not scenario.get("claims_supported", False):
        blockers.append("unsupported_claims")
    return {"status": "BLOCKED" if blockers else "READY", "blockers": blockers}


def simulate_final_evidence_gate(scenario: dict) -> dict:
    blockers = []
    if scenario.get("pending_decisions"):
        blockers.append("pending_decisions")
    if not scenario.get("claims_supported", False):
        blockers.append("unsupported_claims")
    if not scenario.get("reviews_complete", False):
        blockers.append("reviews_incomplete")
    if not scenario.get("gate_checks_complete", False):
        blockers.append("gate_checks_incomplete")
    if blockers:
        return {"status": "BLOCKED", "blockers": blockers}
    return {"status": "PASS", "blockers": []}
```

- [ ] **Step 2: Run test to verify it still fails for reference reasons**

Run:

```powershell
python -m pytest regression/test_gate_and_rollback_checks.py::test_gate_and_rollback_references_are_registered -q
```

Expected: FAIL because the three scenario markdown files do not exist yet.

- [ ] **Step 3: Commit**

```bash
git add C:/Users/zty/.agents/skills/math-modeling-v4/regression/run_gate_and_rollback_checks.py
git commit -m "feat: add deterministic gate and rollback regression helper"
```

---

### Task 3: Add scenario markdown anchors

**Files:**
- Create: `C:\Users\zty\.agents\skills\math-modeling-v4\regression\rollback-late-stage-structural-defect.md`
- Create: `C:\Users\zty\.agents\skills\math-modeling-v4\regression\export-blocked-by-pending-decision.md`
- Create: `C:\Users\zty\.agents\skills\math-modeling-v4\regression\final-evidence-gate-grounded-claims-only.md`
- Test: `C:\Users\zty\.agents\skills\math-modeling-v4\regression\test_gate_and_rollback_checks.py`

- [ ] **Step 1: Write the scenario files**

Create `regression/rollback-late-stage-structural-defect.md` with:

```markdown
# Regression - Rollback Late Stage Structural Defect

## Input Scenario

- active stage is 8, 9, or 10
- late review discovers an earlier structural defect
- downstream patching would hide the original defect

## Expected Output

- status: `ROLLBACK_REQUIRED`
- rollback path: `rollbacks/rollback-stage8-structural-defect.md`
- user confirmation required

## Forbidden Outcomes

- patching downstream artifacts and continuing
- exporting while the structural defect remains unresolved
```

Create `regression/export-blocked-by-pending-decision.md` with:

```markdown
# Regression - Export Blocked By Pending Decision

## Input Scenario

- export is requested
- `decisions/decision-stage10-export.md` is still pending
- final gate may otherwise look passable

## Expected Output

- status: `BLOCKED`
- blocker: `pending_decisions`
- do not emit export-ready state

## Forbidden Outcomes

- exporting with a pending decision
- treating silence as approval
```

Create `regression/final-evidence-gate-grounded-claims-only.md` with:

```markdown
# Regression - Final Evidence Gate Grounded Claims Only

## Input Scenario

- claim registry exists
- reviews and gates are present
- some claims are not fully supported by evidence

## Expected Output

- `BLOCKED` when `unsupported_claims` exist
- `PASS_WITH_WARNINGS` or `PASS` only when claims are grounded

## Forbidden Outcomes

- passing the gate with unsupported claims
- passing while pending decisions remain
```

- [ ] **Step 2: Run the new regression module**

Run:

```powershell
python -m pytest regression/test_gate_and_rollback_checks.py -q
```

Expected: PASS.

- [ ] **Step 3: Commit**

```bash
git add C:/Users/zty/.agents/skills/math-modeling-v4/regression
git commit -m "feat: add gate and rollback scenario docs"
```

---

### Task 4: Update README and run the full regression suite

**Files:**
- Modify: `C:\Users\zty\.agents\skills\math-modeling-v4\README.md`

- [ ] **Step 1: Update the documented regression command**

Append `regression/test_gate_and_rollback_checks.py` to the existing README command:

```powershell
python -m pytest regression/test_markdown_first_contracts.py regression/test_readiness_gate_checks.py regression/test_readiness_gate_smoke_flow.py regression/test_readiness_gate_command_flow.py regression/test_gate_and_rollback_checks.py
```

- [ ] **Step 2: Run the full suite**

Run:

```powershell
python -m pytest regression/test_markdown_first_contracts.py regression/test_readiness_gate_checks.py regression/test_readiness_gate_smoke_flow.py regression/test_readiness_gate_command_flow.py regression/test_gate_and_rollback_checks.py -q
```

Expected: PASS for all tests.

- [ ] **Step 3: Scan for accidental old-state regressions outside tests**

Run:

```powershell
python -c "from pathlib import Path; root=Path(r'C:\Users\zty\.agents\skills\math-modeling-v4'); files=[p for p in root.rglob('*') if p.is_file() and p.suffix in {'.md','.py'}]; bad=[]; forbidden=['pending_confirmations','confirmed_decisions','HUMAN_REVIEW_REQUIRED','IN_PROGRESS']; 
for p in files:
    if 'docs\\\\superpowers' in str(p) or 'regression\\\\test_' in str(p):
        continue
    text=p.read_text(encoding='utf-8')
    hits=[t for t in forbidden if t in text]
    if hits:
        bad.append((str(p.relative_to(root)), hits))
print(bad)"
```

Expected: `[]`.

- [ ] **Step 4: Commit**

```bash
git add C:/Users/zty/.agents/skills/math-modeling-v4/README.md C:/Users/zty/.agents/skills/math-modeling-v4/regression
git commit -m "feat: lock gate and rollback scenario regressions"
```

---

## Self-Review

### Spec coverage

- rollback-required boundary: Tasks 1-3.
- export blocking boundary: Tasks 1-3.
- final evidence gate grounded-claims boundary: Tasks 1-3.
- README update and full regression run: Task 4.

### Placeholder scan

No placeholders or TBD sections remain.

### Type consistency

- helper names match the approved spec,
- return field names are consistent across tests and implementation,
- scenario file names match the required reference checks.
