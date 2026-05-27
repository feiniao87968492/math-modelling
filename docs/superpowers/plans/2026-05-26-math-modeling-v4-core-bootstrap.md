# math-modeling-v4 Core Bootstrap Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the first runnable `math-modeling-v4` skill package as a new coexisting package, with a Markdown-first dispatcher, core protocol docs, and minimal regression coverage.

**Architecture:** Keep the old `math-modeling` package untouched and build a new package under `C:\Users\zty\.agents\skills\math-modeling-v4`. Implement the v4 runtime in three layers: dispatcher and package rules, Markdown audit protocols, then minimal regression helpers that enforce the new contract. Defer full stage-doc and README migration until the core runtime and tests are stable.

**Tech Stack:** Markdown skill docs, Python regression helpers, pytest, local filesystem checks.

---

## Scope Check

This plan only covers the first implementation slice for the new package:

- create the new skill package skeleton,
- write the dispatcher and package instructions,
- add the Markdown audit protocol,
- rewrite the core runtime protocols,
- add minimal contract regression tests,
- add smoke and command-flow regression for the new package.

This intentionally does **not** yet rewrite all ten stage docs or full README polish. Those are Phase 2 follow-up work after the core package proves stable.

## File Structure Map

### Files to create

- `C:\Users\zty\.agents\skills\math-modeling-v4\SKILL.md` — thin dispatcher for the new skill.
- `C:\Users\zty\.agents\skills\math-modeling-v4\CLAUDE.md` — edit/use rules for the new package.
- `C:\Users\zty\.agents\skills\math-modeling-v4\README.md` — package overview for v4 bootstrap.
- `C:\Users\zty\.agents\skills\math-modeling-v4\references\protocol-markdown-audit.md` — authoritative Markdown audit protocol.
- `C:\Users\zty\.agents\skills\math-modeling-v4\references\protocol-human-confirmation.md` — Markdown decision protocol.
- `C:\Users\zty\.agents\skills\math-modeling-v4\references\protocol-readiness-gate.md` — Markdown gate protocol.
- `C:\Users\zty\.agents\skills\math-modeling-v4\references\protocol-rollback.md` — Markdown rollback protocol.
- `C:\Users\zty\.agents\skills\math-modeling-v4\references\protocol-memory-update.md` — memory rules for Markdown-first workflow.
- `C:\Users\zty\.agents\skills\math-modeling-v4\references\protocol-subagent-delegation.md` — expert-review protocol.
- `C:\Users\zty\.agents\skills\math-modeling-v4\references\protocol-state-writeback.md` — deprecation/redirect page.
- `C:\Users\zty\.agents\skills\math-modeling-v4\references\protocol-fallback-and-deviation.md` — fallback boundary rules compatible with v4.
- `C:\Users\zty\.agents\skills\math-modeling-v4\references\subagent-model-building.md` — reviewer profile for algorithm/model review.
- `C:\Users\zty\.agents\skills\math-modeling-v4\references\subagent-validation-paper.md` — reviewer profile for validation/evidence review.
- `C:\Users\zty\.agents\skills\math-modeling-v4\references\subagent-specialists.md` — reviewer profile bundle for risk-triggered specialists.
- `C:\Users\zty\.agents\skills\math-modeling-v4\references\modeling-memory-template.md` — fallback memory template.
- `C:\Users\zty\.agents\skills\math-modeling-v4\references\stage-5-solution-implementation.md` — minimal stage contract needed for bootstrap command regression.
- `C:\Users\zty\.agents\skills\math-modeling-v4\references\evidence-gate.md` — final evidence gate guidance for bootstrap package.
- `C:\Users\zty\.agents\skills\math-modeling-v4\regression\markdown_doc_checks.py` — helper functions for heading/content checks.
- `C:\Users\zty\.agents\skills\math-modeling-v4\regression\test_markdown_first_contracts.py` — dispatcher and protocol contract tests.
- `C:\Users\zty\.agents\skills\math-modeling-v4\regression\smoke_readiness_gate_flow.py` — deterministic Markdown skeleton smoke writer.
- `C:\Users\zty\.agents\skills\math-modeling-v4\regression\test_readiness_gate_smoke_flow.py` — smoke-flow tests.
- `C:\Users\zty\.agents\skills\math-modeling-v4\regression\command_readiness_gate_flow.py` — stage 5 command flow simulation.
- `C:\Users\zty\.agents\skills\math-modeling-v4\regression\test_readiness_gate_command_flow.py` — command-flow tests.

### Existing files to reuse as reference only

- `C:\Users\zty\.agents\skills\math-modeling\SKILL.md`
- `C:\Users\zty\.agents\skills\math-modeling\README.md`
- `C:\Users\zty\.agents\skills\math-modeling\CLAUDE.md`
- `C:\Users\zty\.agents\skills\math-modeling\references\*.md`
- `C:\Users\zty\.agents\skills\math-modeling\regression\*.py`

Do not modify these old-package files during this plan.

---

### Task 1: Create the new package skeleton

**Files:**
- Create: `C:\Users\zty\.agents\skills\math-modeling-v4\SKILL.md`
- Create: `C:\Users\zty\.agents\skills\math-modeling-v4\CLAUDE.md`
- Create: `C:\Users\zty\.agents\skills\math-modeling-v4\README.md`
- Create: `C:\Users\zty\.agents\skills\math-modeling-v4\references\`
- Create: `C:\Users\zty\.agents\skills\math-modeling-v4\regression\`

- [ ] **Step 1: Write the failing package-layout test**

Create `C:\Users\zty\.agents\skills\math-modeling-v4\regression\test_markdown_first_contracts.py` with:

```python
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_new_package_has_core_files():
    required = [
        ROOT / "SKILL.md",
        ROOT / "CLAUDE.md",
        ROOT / "README.md",
        ROOT / "references" / "protocol-markdown-audit.md",
    ]
    missing = [str(path) for path in required if not path.exists()]
    assert not missing, missing
```

- [ ] **Step 2: Run test to verify it fails**

Run:

```powershell
python -m pytest regression/test_markdown_first_contracts.py::test_new_package_has_core_files -q
```

Expected: FAIL because `SKILL.md`, `CLAUDE.md`, `README.md`, and protocol docs do not exist yet.

- [ ] **Step 3: Create the minimal package files**

Write `C:\Users\zty\.agents\skills\math-modeling-v4\SKILL.md` with:

```markdown
---
name: math-modeling-v4
description: "数学建模 Markdown-first 规则约束工作流。保留 10 阶段 checklist，使用 Markdown 审计文档与专家评审。Invoke when user wants the v4 non-state-machine workflow."
---

# /math-modeling — Markdown-first Rule-Constrained Workflow

你是 `math-modeling-v4` 的数学建模工作流编排器。
```

Write `C:\Users\zty\.agents\skills\math-modeling-v4\CLAUDE.md` with:

```markdown
# CLAUDE.md — math-modeling-v4 skill instructions

- Treat `SKILL.md` as dispatcher and `references/` files as the source of execution detail.
- Do not add new behavior that depends on `modeling_state.yaml` as the workflow driver.
- Keep the old `math-modeling` package untouched.
```

Write `C:\Users\zty\.agents\skills\math-modeling-v4\README.md` with:

```markdown
# math-modeling-v4 — Markdown-first 数学建模工作流 Skill

这是一个新的 skill 包，与旧版 `math-modeling` 并存。
```

- [ ] **Step 4: Run the package-layout test again**

Run:

```powershell
python -m pytest regression/test_markdown_first_contracts.py::test_new_package_has_core_files -q
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add C:/Users/zty/.agents/skills/math-modeling-v4
git commit -m "feat: bootstrap math-modeling-v4 package"
```

---

### Task 2: Add Markdown-first dispatcher and package instructions

**Files:**
- Modify: `C:\Users\zty\.agents\skills\math-modeling-v4\SKILL.md`
- Modify: `C:\Users\zty\.agents\skills\math-modeling-v4\CLAUDE.md`
- Modify: `C:\Users\zty\.agents\skills\math-modeling-v4\README.md`
- Test: `C:\Users\zty\.agents\skills\math-modeling-v4\regression\test_markdown_first_contracts.py`

- [ ] **Step 1: Extend the contract test**

Append to `regression/test_markdown_first_contracts.py`:

```python
def test_dispatcher_is_markdown_first_and_not_yaml_state_machine():
    content = (ROOT / "SKILL.md").read_text(encoding="utf-8")

    assert "Markdown-first" in content
    assert "Rule-First Execution" in content
    assert "Expert Review Policy" in content
    assert "总状态机" not in content
    assert "pending_confirmations" not in content
```

- [ ] **Step 2: Run the dispatcher test to verify it fails**

Run:

```powershell
python -m pytest regression/test_markdown_first_contracts.py::test_dispatcher_is_markdown_first_and_not_yaml_state_machine -q
```

Expected: FAIL because the bootstrap dispatcher is too small.

- [ ] **Step 3: Rewrite `SKILL.md`**

Write `C:\Users\zty\.agents\skills\math-modeling-v4\SKILL.md` with these required sections:

```markdown
---
name: math-modeling-v4
description: "数学建模 Markdown-first 规则约束工作流。保留 10 阶段 checklist 与 /math-modeling 命令；主 agent 高自由度推进，多专家 subagent 做评审。Invoke when the user wants the v4 non-state-machine workflow."
metadata:
  author: zty
  version: 4.0.0
  created: 2026-05-26
  last_reviewed: 2026-05-26
  review_interval_days: 90
---

# /math-modeling — Markdown-first Rule-Constrained Workflow

## 触发条件

## 命令入口

## Rule-First Execution

## Markdown Audit Documents

## Expert Review Policy

## 强阻断规则

## 必读 references
```

Inside that file, include:

- `workflow.md`
- `decisions/`
- `gates/`
- `branches/`
- `rollbacks/`
- `claims/claim-registry.md`
- `reviews/`

- [ ] **Step 4: Rewrite `CLAUDE.md` and `README.md`**

Write `CLAUDE.md` so it includes:

```markdown
- v4 is Markdown-first.
- Do not use `modeling_state.yaml` as the workflow driver.
- Subagents are expert reviewers, not stage owners.
```

Write `README.md` so it includes:

```markdown
# math-modeling-v4 — Markdown-first 数学建模工作流 Skill

## Markdown-first v4

- workflow.md
- decisions/
- gates/
- branches/
- rollbacks/
- claims/claim-registry.md
- reviews/
```

- [ ] **Step 5: Run the dispatcher contract test**

Run:

```powershell
python -m pytest regression/test_markdown_first_contracts.py::test_dispatcher_is_markdown_first_and_not_yaml_state_machine -q
```

Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add C:/Users/zty/.agents/skills/math-modeling-v4/SKILL.md C:/Users/zty/.agents/skills/math-modeling-v4/CLAUDE.md C:/Users/zty/.agents/skills/math-modeling-v4/README.md C:/Users/zty/.agents/skills/math-modeling-v4/regression/test_markdown_first_contracts.py
git commit -m "feat: add markdown-first dispatcher for math-modeling-v4"
```

---

### Task 3: Add the Markdown audit and core runtime protocols

**Files:**
- Create: `C:\Users\zty\.agents\skills\math-modeling-v4\references\protocol-markdown-audit.md`
- Create: `C:\Users\zty\.agents\skills\math-modeling-v4\references\protocol-human-confirmation.md`
- Create: `C:\Users\zty\.agents\skills\math-modeling-v4\references\protocol-readiness-gate.md`
- Create: `C:\Users\zty\.agents\skills\math-modeling-v4\references\protocol-rollback.md`
- Create: `C:\Users\zty\.agents\skills\math-modeling-v4\references\protocol-memory-update.md`
- Create: `C:\Users\zty\.agents\skills\math-modeling-v4\references\protocol-subagent-delegation.md`
- Create: `C:\Users\zty\.agents\skills\math-modeling-v4\references\protocol-state-writeback.md`
- Create: `C:\Users\zty\.agents\skills\math-modeling-v4\references\protocol-fallback-and-deviation.md`
- Test: `C:\Users\zty\.agents\skills\math-modeling-v4\regression\test_markdown_first_contracts.py`

- [ ] **Step 1: Add protocol existence and heading tests**

Append:

```python
def test_core_protocols_exist_and_use_markdown_contracts():
    protocol_paths = [
        ROOT / "references" / "protocol-markdown-audit.md",
        ROOT / "references" / "protocol-human-confirmation.md",
        ROOT / "references" / "protocol-readiness-gate.md",
        ROOT / "references" / "protocol-rollback.md",
        ROOT / "references" / "protocol-memory-update.md",
        ROOT / "references" / "protocol-subagent-delegation.md",
    ]
    missing = [str(path) for path in protocol_paths if not path.exists()]
    assert not missing, missing

    audit = (ROOT / "references" / "protocol-markdown-audit.md").read_text(encoding="utf-8")
    assert "Markdown Audit Documents" in audit
    assert "workflow.md" in audit
    assert "Forbidden State-Machine Behavior" in audit
```

- [ ] **Step 2: Run the protocol test to verify it fails**

Run:

```powershell
python -m pytest regression/test_markdown_first_contracts.py::test_core_protocols_exist_and_use_markdown_contracts -q
```

Expected: FAIL because protocol files do not exist.

- [ ] **Step 3: Write the protocol files**

Write `protocol-markdown-audit.md` with these exact headings:

```markdown
# Protocol — Markdown Audit Documents
## Core Rule
## Required Project Documents
## Blocking Decision Documents
## Gate Documents
## Workflow Navigation
## Forbidden State-Machine Behavior
```

Write `protocol-human-confirmation.md` with these exact headings:

```markdown
# Protocol — Human Confirmation
## Core Rule
## Decision Markdown Required Sections
## Blocking Nodes
## Confirmation Record Template
## Command Contract
## Allowed Output While Blocked
```

Write `protocol-readiness-gate.md` with these exact headings:

```markdown
# Protocol — Readiness Gate
## Purpose
## Core Rule
## Mandatory Checkpoints
## Markdown gate report Required Sections
## Claim Levels
## Branch Rules
## Blocking Confirmation Rules
```

Write `protocol-rollback.md` with these exact headings:

```markdown
# Protocol — Rollback
## Purpose
## Core Rule
## Severity Levels
## Rollback Document Required Sections
## Confirmation Rules
```

Write `protocol-memory-update.md` with these exact headings:

```markdown
# Protocol — Memory Update
## Core Rule
## Pre-Work Read Rule
## Memory Check
## Markdown Record Locations
## Allowed Memory Categories
## Forbidden Content
```

Write `protocol-subagent-delegation.md` with these exact headings:

```markdown
# Protocol — Expert Review
## Purpose
## Core Rule
## Main Agent Owns
## Expert Reviewers Own
## Fixed Review Points
## Risk-Triggered Reviewers
## Review Document Required Sections
## Forbidden Reviewer Behavior
```

Write `protocol-state-writeback.md` as a short redirect saying v4 does not use global YAML state writeback.

Write `protocol-fallback-and-deviation.md` so it says fallback may happen, but method/evidence-path changes require a new blocking decision document.

- [ ] **Step 4: Run the protocol test again**

Run:

```powershell
python -m pytest regression/test_markdown_first_contracts.py::test_core_protocols_exist_and_use_markdown_contracts -q
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add C:/Users/zty/.agents/skills/math-modeling-v4/references C:/Users/zty/.agents/skills/math-modeling-v4/regression/test_markdown_first_contracts.py
git commit -m "feat: add markdown-first runtime protocols for math-modeling-v4"
```

---

### Task 4: Add reviewer profiles, minimal stage contract, and evidence gate

**Files:**
- Create: `C:\Users\zty\.agents\skills\math-modeling-v4\references\subagent-model-building.md`
- Create: `C:\Users\zty\.agents\skills\math-modeling-v4\references\subagent-validation-paper.md`
- Create: `C:\Users\zty\.agents\skills\math-modeling-v4\references\subagent-specialists.md`
- Create: `C:\Users\zty\.agents\skills\math-modeling-v4\references\stage-5-solution-implementation.md`
- Create: `C:\Users\zty\.agents\skills\math-modeling-v4\references\evidence-gate.md`
- Create: `C:\Users\zty\.agents\skills\math-modeling-v4\references\modeling-memory-template.md`
- Test: `C:\Users\zty\.agents\skills\math-modeling-v4\regression\test_markdown_first_contracts.py`

- [ ] **Step 1: Add the failing stage/reviewer contract test**

Append:

```python
def test_stage5_and_reviewer_docs_exist():
    required = [
        ROOT / "references" / "subagent-model-building.md",
        ROOT / "references" / "subagent-validation-paper.md",
        ROOT / "references" / "subagent-specialists.md",
        ROOT / "references" / "stage-5-solution-implementation.md",
        ROOT / "references" / "evidence-gate.md",
        ROOT / "references" / "modeling-memory-template.md",
    ]
    missing = [str(path) for path in required if not path.exists()]
    assert not missing, missing
```

- [ ] **Step 2: Run test to verify it fails**

Run:

```powershell
python -m pytest regression/test_markdown_first_contracts.py::test_stage5_and_reviewer_docs_exist -q
```

Expected: FAIL.

- [ ] **Step 3: Write the minimal docs**

Write `subagent-model-building.md` as:

```markdown
# Reviewer Profile — Algorithm and Model
## Role
## Review Scope
## Required Review Output
## Review Focus
## Must Recommend a Decision or Gate When
## Forbidden Behavior
```

Write `subagent-validation-paper.md` as:

```markdown
# Reviewer Profile — Validation and Evidence
## Role
## Review Scope
## Required Review Output
## Review Focus
## Must Recommend Rollback When
## Forbidden Behavior
```

Write `subagent-specialists.md` as:

```markdown
# Reviewer Profiles — Specialists
## Purpose
## Global Boundary
## Data-Audit Reviewer
## Code-Review Reviewer
## Figure-Review Reviewer
## Evidence-Gate Reviewer
## Literature/Method Reviewer
```

Write `stage-5-solution-implementation.md` as:

```markdown
# Stage 5 — Solution Implementation
## Stage Contract
## Inputs
## Required Reads
## Outputs
## Blocking Rules
## Expert Review
## Done When
## Memory Check
## Revision or Rollback Triggers
```

Write `evidence-gate.md` as:

```markdown
# Final Evidence Gate
## Purpose
## Core Rule
## Required Inputs
## Gate Checks
## Final Evidence Gate Report Template
## Result Values
```

Write `modeling-memory-template.md` as:

```markdown
# Modeling Memory Template

## Rules

## Pitfalls

## Counterexamples

## User Preferences
```

- [ ] **Step 4: Run the stage/reviewer test**

Run:

```powershell
python -m pytest regression/test_markdown_first_contracts.py::test_stage5_and_reviewer_docs_exist -q
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add C:/Users/zty/.agents/skills/math-modeling-v4/references C:/Users/zty/.agents/skills/math-modeling-v4/regression/test_markdown_first_contracts.py
git commit -m "feat: add reviewer profiles and bootstrap stage contract for math-modeling-v4"
```

---

### Task 5: Add Markdown contract helpers and smoke-flow regression

**Files:**
- Create: `C:\Users\zty\.agents\skills\math-modeling-v4\regression\markdown_doc_checks.py`
- Create: `C:\Users\zty\.agents\skills\math-modeling-v4\regression\smoke_readiness_gate_flow.py`
- Create: `C:\Users\zty\.agents\skills\math-modeling-v4\regression\test_readiness_gate_smoke_flow.py`

- [ ] **Step 1: Write the failing smoke test**

Create `regression/test_readiness_gate_smoke_flow.py` with:

```python
from smoke_readiness_gate_flow import run_smoke_flow


def test_stage5_smoke_flow_writes_markdown_artifacts(tmp_path):
    project_dir = tmp_path / "project"
    result = run_smoke_flow(project_dir)

    assert result["ok"]
    assert not (project_dir / "modeling_state.yaml").exists()
    assert (project_dir / "workflow.md").exists()
    assert (project_dir / "gates" / "stage5-readiness-gate.md").exists()
    assert (project_dir / "decisions" / "decision-stage5-implementation-readiness.md").exists()
```

- [ ] **Step 2: Run test to verify it fails**

Run:

```powershell
python -m pytest regression/test_readiness_gate_smoke_flow.py -q
```

Expected: FAIL because `smoke_readiness_gate_flow.py` does not exist.

- [ ] **Step 3: Write the helper and smoke-flow implementation**

Write `regression/markdown_doc_checks.py` with:

```python
from pathlib import Path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")
```

Write `regression/smoke_readiness_gate_flow.py` with:

```python
from pathlib import Path


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def run_smoke_flow(project_dir: Path) -> dict:
    project_dir.mkdir(parents=True, exist_ok=True)
    _write(project_dir / "memory.md", "# Modeling Memory\n\n## Rules\n\n")
    _write(project_dir / "workflow.md", "# Modeling Workflow\n\n## Active blockers\n- decisions/decision-stage5-implementation-readiness.md\n\n## Current claim ceiling\nfeasible_baseline\n\n## Next safe action\nWait for confirmation.\n\nMemory check: no new memory\n")
    _write(project_dir / "gates" / "stage5-readiness-gate.md", "# Stage 5 Readiness Gate\n\n## Gate result\nBlocked: missing required inputs and solver capability\n\n## Intended claim level\nvalidated_optimum\n\n## Supported claim level\nfeasible_baseline\n\n## Blocked claims\n- Global optimum\n- True ROI breakpoint\n")
    _write(project_dir / "decisions" / "decision-stage5-implementation-readiness.md", "# Decision: Stage 5 Implementation Readiness\n\n## Confirmation record\nPending.\n")
    _write(project_dir / "branches" / "branch-stage5-relationship-data.md", "# Branch\n")
    _write(project_dir / "branches" / "branch-stage5-solver-setup.md", "# Branch\n")
    _write(project_dir / "claims" / "claim-registry.md", "# Claim Registry\n")
    _write(project_dir / "reviews" / "stage5-implementation-readiness-review.md", "# Review\n")
    _write(project_dir / "logs" / "workflow-trace.md", "# Workflow Trace\n")
    return {
        "ok": True,
        "workflow_path": str(project_dir / "workflow.md"),
        "gate_path": str(project_dir / "gates" / "stage5-readiness-gate.md"),
        "decision_path": str(project_dir / "decisions" / "decision-stage5-implementation-readiness.md"),
        "supported_claim_level": "feasible_baseline",
    }
```

- [ ] **Step 4: Run smoke regression**

Run:

```powershell
python -m pytest regression/test_readiness_gate_smoke_flow.py -q
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add C:/Users/zty/.agents/skills/math-modeling-v4/regression
git commit -m "feat: add markdown smoke regression for math-modeling-v4"
```

---

### Task 6: Add command-flow regression for stage 5

**Files:**
- Create: `C:\Users\zty\.agents\skills\math-modeling-v4\regression\command_readiness_gate_flow.py`
- Create: `C:\Users\zty\.agents\skills\math-modeling-v4\regression\test_readiness_gate_command_flow.py`

- [ ] **Step 1: Write the failing command-flow test**

Create `regression/test_readiness_gate_command_flow.py` with:

```python
from pathlib import Path

from command_readiness_gate_flow import run_command_flow

ROOT = Path(__file__).resolve().parents[1]


def test_stage5_command_flow_uses_markdown_protocols(tmp_path):
    project_dir = tmp_path / "project"
    result = run_command_flow("/math-modeling stage 5", project_dir, ROOT)

    assert result["ok"]
    assert "references/protocol-markdown-audit.md" in result["required_reads"]
    assert "Implementation Readiness Reviewer" in result["review_policy"]["fixed_reviewers"]
    assert not (project_dir / "modeling_state.yaml").exists()
```

- [ ] **Step 2: Run test to verify it fails**

Run:

```powershell
python -m pytest regression/test_readiness_gate_command_flow.py -q
```

Expected: FAIL because `command_readiness_gate_flow.py` does not exist.

- [ ] **Step 3: Write the command-flow implementation**

Write `regression/command_readiness_gate_flow.py` with:

```python
from pathlib import Path

from smoke_readiness_gate_flow import run_smoke_flow

STAGE5_REQUIRED_READS = [
    "references/protocol-markdown-audit.md",
    "references/protocol-human-confirmation.md",
    "references/protocol-memory-update.md",
    "references/protocol-subagent-delegation.md",
    "references/protocol-readiness-gate.md",
    "references/protocol-rollback.md",
    "references/subagent-model-building.md",
    "references/subagent-specialists.md",
    "references/protocol-fallback-and-deviation.md",
    "references/stage-5-solution-implementation.md",
]


def run_command_flow(command_text: str, project_dir: Path, skill_root: Path) -> dict:
    if command_text != "/math-modeling stage 5":
        return {"ok": False, "error": "unsupported_command"}

    missing = [path for path in STAGE5_REQUIRED_READS if not (skill_root / path).exists()]
    if missing:
        return {"ok": False, "error": "missing_required_reads", "missing_required_reads": missing}

    smoke = run_smoke_flow(project_dir)
    return {
        "ok": True,
        "command": {"active_command": "stage", "stage": 5},
        "required_reads": STAGE5_REQUIRED_READS,
        "review_policy": {
            "main_agent_role": "workflow synthesis and Markdown audit updates",
            "fixed_reviewers": ["Implementation Readiness Reviewer"],
            "risk_triggered_reviewers": ["Data-Audit Reviewer", "Code-Review Reviewer"],
        },
        "gate_path": smoke["gate_path"],
    }
```

- [ ] **Step 4: Run command-flow regression**

Run:

```powershell
python -m pytest regression/test_readiness_gate_command_flow.py -q
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add C:/Users/zty/.agents/skills/math-modeling-v4/regression
git commit -m "feat: add markdown command regression for math-modeling-v4"
```

---

### Task 7: Run the bootstrap regression suite and scan for stale state-machine terms

**Files:**
- Modify any file in `C:\Users\zty\.agents\skills\math-modeling-v4\` that fails the checks.

- [ ] **Step 1: Run the full bootstrap pytest suite**

Run:

```powershell
python -m pytest regression/test_markdown_first_contracts.py regression/test_readiness_gate_smoke_flow.py regression/test_readiness_gate_command_flow.py -q
```

Expected: all tests pass.

- [ ] **Step 2: Scan the new package for stale old-runtime terms**

Run:

```powershell
python -c "from pathlib import Path; root=Path(r'C:\Users\zty\.agents\skills\math-modeling-v4'); files=[p for p in root.rglob('*') if p.is_file() and p.suffix in {'.md','.py'}]; forbidden=['pending_confirmations','confirmed_decisions','HUMAN_REVIEW_REQUIRED','IN_PROGRESS']; bad=[]; [bad.append((str(p.relative_to(root)), [t for t in forbidden if t in p.read_text(encoding='utf-8')])) for p in files if any(t in p.read_text(encoding='utf-8') for t in forbidden)]; print(bad)"
```

Expected: `[]`.

- [ ] **Step 3: Review diff only inside the new package**

Run:

```powershell
git diff -- C:/Users/zty/.agents/skills/math-modeling-v4
```

Expected: only files under `math-modeling-v4` appear.

- [ ] **Step 4: Commit**

```bash
git add C:/Users/zty/.agents/skills/math-modeling-v4
git commit -m "feat: complete math-modeling-v4 core bootstrap"
```

---

## Self-Review

### Spec coverage

- New package instead of overwriting old package: Tasks 1, 7.
- Markdown-first dispatcher: Task 2.
- Markdown audit protocol: Task 3.
- Human confirmation, readiness, rollback, memory, and expert-review core protocols: Task 3.
- Reviewer profiles and minimal stage/evidence docs: Task 4.
- Minimal regression helpers and smoke flow: Task 5.
- Command-flow simulation: Task 6.
- No old package mutation: Tasks 1 and 7.

### Placeholder scan

No TBD/TODO placeholders remain. Every task contains concrete files, concrete headings, and concrete commands.

### Type and naming consistency

- New package root is consistently `C:\Users\zty\.agents\skills\math-modeling-v4`.
- Dispatcher name is consistently `math-modeling-v4`.
- Markdown audit protocol is consistently `protocol-markdown-audit.md`.
- Claim registry path is consistently `claims/claim-registry.md`.
- Review model consistently uses expert reviewers, not stage owners.

## Execution Handoff

Plan complete. Use one of these execution modes after user approval:

1. Subagent-Driven execution: dispatch a fresh subagent per task, review between tasks, fast iteration.
2. Inline execution: execute tasks in this session with checkpoints after each group of changes.
