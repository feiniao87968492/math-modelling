# Command Export And Rollback Flow Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add command-flow regression helpers and tests for `/math-modeling export` and review-triggered rollback behavior in `math-modeling-v4`.

**Architecture:** Keep the new command helpers thin and deterministic, matching the style of the existing stage-5 command-flow helper. Reuse the scenario-level gate and rollback checks where possible, return the same broad metadata shape (`ok`, `command`, `required_reads`, `review_policy`), and add command-specific blocker/rollback fields.

**Tech Stack:** Python regression helpers, pytest, existing Markdown references.

---

## File Structure Map

### Files to create

- `C:\Users\zty\.agents\skills\math-modeling-v4\regression\command_export_flow.py` - command-style helper for `/math-modeling export`.
- `C:\Users\zty\.agents\skills\math-modeling-v4\regression\command_rollback_flow.py` - command-style helper for review-triggered rollback.
- `C:\Users\zty\.agents\skills\math-modeling-v4\regression\test_export_command_flow.py` - pytest coverage for export command flow.
- `C:\Users\zty\.agents\skills\math-modeling-v4\regression\test_rollback_command_flow.py` - pytest coverage for rollback command flow.

### Files to reuse

- `C:\Users\zty\.agents\skills\math-modeling-v4\regression\run_gate_and_rollback_checks.py`
- `C:\Users\zty\.agents\skills\math-modeling-v4\regression\command_readiness_gate_flow.py`
- `C:\Users\zty\.agents\skills\math-modeling-v4\references\protocol-markdown-audit.md`
- `C:\Users\zty\.agents\skills\math-modeling-v4\references\protocol-human-confirmation.md`
- `C:\Users\zty\.agents\skills\math-modeling-v4\references\protocol-memory-update.md`
- `C:\Users\zty\.agents\skills\math-modeling-v4\references\protocol-readiness-gate.md`
- `C:\Users\zty\.agents\skills\math-modeling-v4\references\protocol-rollback.md`
- `C:\Users\zty\.agents\skills\math-modeling-v4\references\protocol-subagent-delegation.md`
- `C:\Users\zty\.agents\skills\math-modeling-v4\references\evidence-gate.md`
- `C:\Users\zty\.agents\skills\math-modeling-v4\references\stage-10-paper-materials.md`
- `C:\Users\zty\.agents\skills\math-modeling-v4\references\stage-8-visualization.md`
- `C:\Users\zty\.agents\skills\math-modeling-v4\references\stage-9-figure-review.md`
- `C:\Users\zty\.agents\skills\math-modeling-v4\references\subagent-validation-paper.md`

---

### Task 1: Add failing export command-flow tests

**Files:**
- Create: `C:\Users\zty\.agents\skills\math-modeling-v4\regression\test_export_command_flow.py`

- [ ] **Step 1: Write the failing test**

Create `regression/test_export_command_flow.py` with:

```python
from pathlib import Path

from command_export_flow import run_export_command_flow

ROOT = Path(__file__).resolve().parents[1]


def test_export_command_flow_blocks_when_pending_decision_exists(tmp_path):
    project_dir = tmp_path / "project"
    result = run_export_command_flow(
        "/math-modeling export",
        project_dir,
        ROOT,
        {
            "pending_decisions": ["decisions/decision-stage10-export.md"],
            "final_gate_status": "PASS",
            "claims_supported": True,
        },
    )

    assert result["ok"]
    assert result["export_allowed"] is False
    assert "pending_decisions" in result["blockers"]
    assert "references/evidence-gate.md" in result["required_reads"]


def test_export_command_flow_allows_export_when_gate_is_clear(tmp_path):
    project_dir = tmp_path / "project"
    result = run_export_command_flow(
        "/math-modeling export",
        project_dir,
        ROOT,
        {
            "pending_decisions": [],
            "final_gate_status": "PASS",
            "claims_supported": True,
        },
    )

    assert result["ok"]
    assert result["export_allowed"] is True
    assert result["blockers"] == []
```

- [ ] **Step 2: Run tests to verify they fail**

Run:

```powershell
python -m pytest regression/test_export_command_flow.py -q
```

Expected: FAIL with `ModuleNotFoundError: No module named 'command_export_flow'`.

- [ ] **Step 3: Commit**

```bash
git add C:/Users/zty/.agents/skills/math-modeling-v4/regression/test_export_command_flow.py
git commit -m "test: add failing export command flow tests"
```

---

### Task 2: Implement export command-flow helper

**Files:**
- Create: `C:\Users\zty\.agents\skills\math-modeling-v4\regression\command_export_flow.py`
- Test: `C:\Users\zty\.agents\skills\math-modeling-v4\regression\test_export_command_flow.py`

- [ ] **Step 1: Write the minimal implementation**

Create `regression/command_export_flow.py` with:

```python
from pathlib import Path

from run_gate_and_rollback_checks import simulate_export_gate

EXPORT_REQUIRED_READS = [
    "references/protocol-markdown-audit.md",
    "references/protocol-human-confirmation.md",
    "references/protocol-readiness-gate.md",
    "references/protocol-rollback.md",
    "references/protocol-subagent-delegation.md",
    "references/evidence-gate.md",
    "references/stage-10-paper-materials.md",
]


def run_export_command_flow(
    command_text: str, project_dir: Path, skill_root: Path, scenario: dict
) -> dict:
    if command_text != "/math-modeling export":
        return {"ok": False, "error": "unsupported_command"}

    missing = [path for path in EXPORT_REQUIRED_READS if not (skill_root / path).exists()]
    if missing:
        return {"ok": False, "error": "missing_required_reads", "missing_required_reads": missing}

    gate = simulate_export_gate(scenario)
    project_dir.mkdir(parents=True, exist_ok=True)

    return {
        "ok": True,
        "command": {"active_command": "export"},
        "required_reads": EXPORT_REQUIRED_READS,
        "review_policy": {
            "main_agent_role": "final export readiness synthesis",
            "fixed_reviewers": ["Evidence/Claim Reviewer"],
            "risk_triggered_reviewers": ["Evidence-Gate Reviewer", "Figure-Review Reviewer"],
        },
        "blockers": gate["blockers"],
        "gate_path": "gates/final-evidence-gate.md",
        "export_allowed": gate["status"] != "BLOCKED",
    }
```

- [ ] **Step 2: Run the export command-flow tests**

Run:

```powershell
python -m pytest regression/test_export_command_flow.py -q
```

Expected: PASS.

- [ ] **Step 3: Commit**

```bash
git add C:/Users/zty/.agents/skills/math-modeling-v4/regression/command_export_flow.py C:/Users/zty/.agents/skills/math-modeling-v4/regression/test_export_command_flow.py
git commit -m "feat: add export command flow regression"
```

---

### Task 3: Add failing rollback command-flow tests

**Files:**
- Create: `C:\Users\zty\.agents\skills\math-modeling-v4\regression\test_rollback_command_flow.py`

- [ ] **Step 1: Write the failing test**

Create `regression/test_rollback_command_flow.py` with:

```python
from pathlib import Path

from command_rollback_flow import run_rollback_command_flow

ROOT = Path(__file__).resolve().parents[1]


def test_rollback_command_flow_requires_rollback_for_structural_defect(tmp_path):
    project_dir = tmp_path / "project"
    result = run_rollback_command_flow(
        "/math-modeling review",
        project_dir,
        ROOT,
        {
            "stage": 8,
            "defect_severity": "structural_revision",
            "downstream_patch_possible": True,
        },
    )

    assert result["ok"]
    assert result["rollback_required"] is True
    assert result["rollback_path"] == "rollbacks/rollback-stage8-structural-defect.md"
    assert result["requires_user_confirmation"] is True
    assert "references/protocol-rollback.md" in result["required_reads"]


def test_rollback_command_flow_returns_no_rollback_when_no_structural_defect(tmp_path):
    project_dir = tmp_path / "project"
    result = run_rollback_command_flow(
        "/math-modeling review",
        project_dir,
        ROOT,
        {
            "stage": 8,
            "defect_severity": "minor_revision",
            "downstream_patch_possible": True,
        },
    )

    assert result["ok"]
    assert result["rollback_required"] is False
    assert result["rollback_path"] is None
    assert result["requires_user_confirmation"] is False
```

- [ ] **Step 2: Run tests to verify they fail**

Run:

```powershell
python -m pytest regression/test_rollback_command_flow.py -q
```

Expected: FAIL with `ModuleNotFoundError: No module named 'command_rollback_flow'`.

- [ ] **Step 3: Commit**

```bash
git add C:/Users/zty/.agents/skills/math-modeling-v4/regression/test_rollback_command_flow.py
git commit -m "test: add failing rollback command flow tests"
```

---

### Task 4: Implement rollback command-flow helper

**Files:**
- Create: `C:\Users\zty\.agents\skills\math-modeling-v4\regression\command_rollback_flow.py`
- Test: `C:\Users\zty\.agents\skills\math-modeling-v4\regression\test_rollback_command_flow.py`

- [ ] **Step 1: Write the minimal implementation**

Create `regression/command_rollback_flow.py` with:

```python
from pathlib import Path

from run_gate_and_rollback_checks import simulate_rollback_decision

ROLLBACK_REQUIRED_READS = [
    "references/protocol-markdown-audit.md",
    "references/protocol-memory-update.md",
    "references/protocol-subagent-delegation.md",
    "references/protocol-rollback.md",
    "references/stage-8-visualization.md",
    "references/stage-9-figure-review.md",
    "references/subagent-validation-paper.md",
]


def run_rollback_command_flow(
    command_text: str, project_dir: Path, skill_root: Path, scenario: dict
) -> dict:
    if command_text != "/math-modeling review":
        return {"ok": False, "error": "unsupported_command"}

    missing = [path for path in ROLLBACK_REQUIRED_READS if not (skill_root / path).exists()]
    if missing:
        return {"ok": False, "error": "missing_required_reads", "missing_required_reads": missing}

    rollback = simulate_rollback_decision(scenario)
    project_dir.mkdir(parents=True, exist_ok=True)

    return {
        "ok": True,
        "command": {"active_command": "review"},
        "required_reads": ROLLBACK_REQUIRED_READS,
        "review_policy": {
            "main_agent_role": "late-stage review synthesis and rollback handling",
            "fixed_reviewers": ["Validation Reviewer"],
            "risk_triggered_reviewers": ["Figure-Review Reviewer", "Evidence-Gate Reviewer"],
        },
        "rollback_required": rollback["status"] == "ROLLBACK_REQUIRED",
        "rollback_path": rollback["rollback_path"],
        "requires_user_confirmation": rollback["requires_user_confirmation"],
    }
```

- [ ] **Step 2: Run the rollback command-flow tests**

Run:

```powershell
python -m pytest regression/test_rollback_command_flow.py -q
```

Expected: PASS.

- [ ] **Step 3: Commit**

```bash
git add C:/Users/zty/.agents/skills/math-modeling-v4/regression/command_rollback_flow.py C:/Users/zty/.agents/skills/math-modeling-v4/regression/test_rollback_command_flow.py
git commit -m "feat: add rollback command flow regression"
```

---

### Task 5: Run the full regression suite

**Files:**
- Review only. Fix any issues found in the newly created command-flow helpers or tests.

- [ ] **Step 1: Run all regression tests**

Run:

```powershell
python -m pytest regression/test_markdown_first_contracts.py regression/test_readiness_gate_checks.py regression/test_readiness_gate_smoke_flow.py regression/test_readiness_gate_command_flow.py regression/test_gate_and_rollback_checks.py regression/test_export_command_flow.py regression/test_rollback_command_flow.py -q
```

Expected: PASS for all tests.

- [ ] **Step 2: Sanity-check the two new helpers**

Run:

```powershell
python -c "from pathlib import Path; root=Path(r'C:\Users\zty\.agents\skills\math-modeling-v4\regression'); checks={'command_export_flow.py':['run_export_command_flow','export_allowed','gate_path'],'command_rollback_flow.py':['run_rollback_command_flow','rollback_required','rollback_path']}; 
for rel, needles in checks.items():
    text=(root/rel).read_text(encoding='utf-8')
    print(rel, all(n in text for n in needles), [n for n in needles if n not in text])"
```

Expected:

- `command_export_flow.py True []`
- `command_rollback_flow.py True []`

- [ ] **Step 3: Commit**

```bash
git add C:/Users/zty/.agents/skills/math-modeling-v4/regression
git commit -m "feat: complete export and rollback command flow regressions"
```

---

## Self-Review

### Spec coverage

- export command contract: Tasks 1-2.
- rollback command contract: Tasks 3-4.
- return shape consistency and full regression: Task 5.

### Placeholder scan

No placeholders remain.

### Type consistency

- both helpers use the same broad return shape as the existing command-flow style,
- tests assert command-specific fields only after verifying `ok`,
- required-read sets align with the approved spec.
