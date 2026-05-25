# Lean Swarm Math Modeling Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add Lean Swarm subagent delegation, protocol-first execution, and rollback handling to the existing `math-modeling` skill without changing the 10-stage workflow.

**Architecture:** Keep `SKILL.md` as the thin dispatcher and add two cross-cutting protocols: subagent delegation and rollback. Add focused subagent prompt references, then annotate every stage file with ownership, delegation boundaries, and rollback behavior.

**Tech Stack:** Claude Code skill markdown files, protocol references, stage references, PowerShell for local verification, git for change review.

---

## File Structure

### Files to create

- `references/protocol-subagent-delegation.md` — defines Main Orchestrator authority, Lean Swarm mode, primary subagent routing, specialist triggers, and structured return contracts.
- `references/protocol-rollback.md` — defines rollback severity, `rollback_request` schema, confirmation requirements, and state writeback boundaries.
- `references/subagent-model-building.md` — prompt contract for the stages 1-5 Model-Building Subagent.
- `references/subagent-validation-paper.md` — prompt contract for the stages 6-10 Validation-Paper Subagent.
- `references/subagent-specialists.md` — prompt contracts and trigger boundaries for optional specialists.

### Files to modify

- `SKILL.md` — add Protocol-First Rule, Subagent Delegation Policy, rollback state shape, and dispatch table references.
- `README.md` — document Lean Swarm default mode, rollback behavior, new references, and why full swarm is out of scope.
- `references/stage-1-problem-understanding.md` — add Model-Building ownership and rollback response contract.
- `references/stage-2-algorithm-selection.md` — add Model-Building ownership and rollback response contract.
- `references/stage-3-innovation-design.md` — add Model-Building ownership and rollback response contract.
- `references/stage-4-model-spec.md` — add Model-Building ownership and rollback response contract.
- `references/stage-5-solution-implementation.md` — add Model-Building ownership and rollback response contract.
- `references/stage-6-independent-validation.md` — add Validation-Paper ownership and rollback request trigger.
- `references/stage-7-sensitivity-analysis.md` — add Validation-Paper ownership and rollback request trigger.
- `references/stage-8-visualization.md` — add Validation-Paper ownership and rollback request trigger.
- `references/stage-9-figure-review.md` — add Validation-Paper ownership and rollback request trigger.
- `references/stage-10-paper-materials.md` — add Validation-Paper ownership and rollback request trigger.

### Verification surface

- `SKILL.md` includes `Protocol-First Rule` and `Subagent Delegation Policy`.
- `SKILL.md` dispatch table mentions `protocol-subagent-delegation.md` and `protocol-rollback.md`.
- Stage files 1-5 contain `Owning Subagent` with `Model-Building Subagent`.
- Stage files 6-10 contain `Owning Subagent` with `Validation-Paper Subagent`.
- Stage files 6-10 contain `rollback_request`.
- New protocol files define schema and authority boundaries.
- README includes Lean Swarm and explicitly excludes full swarm as default.

---

### Task 1: Add the subagent delegation protocol

**Files:**
- Create: `references/protocol-subagent-delegation.md`
- Test: content scan via PowerShell

- [ ] **Step 1: Create `references/protocol-subagent-delegation.md`**

Write this exact content:

```markdown
# Protocol — Subagent Delegation

## Purpose

Define how `math-modeling` uses Lean Swarm delegation while keeping the Main Orchestrator responsible for global state, user confirmations, memory checks, and rollback execution.

## Default Mode

Default mode is Lean Swarm.

- Stages 1-5 MUST be delegated to Model-Building Subagent.
- Stages 6-10 MUST be delegated to Validation-Paper Subagent.
- Specialist subagents MAY be invoked only when explicitly triggered by a protocol or stage file.
- Subagents must return structured outputs, not free-form discussion.
- Subagents may recommend state changes, but only Main Orchestrator can write global state.
- Subagents may propose `rollback_request`, but cannot execute rollback directly.

## Authority Boundary

Main Orchestrator owns:

- active command and stage detection
- required reference loading
- `modeling_state.yaml` writes
- `memory.md` read and memory check
- `pending_confirmations`
- user-facing blocking confirmation
- rollback classification and execution
- final stage status transitions

Subagents own:

- scoped analysis for their assigned stage group
- candidate recommendations
- structured output drafts
- quality findings
- rollback recommendations or rollback requests

Subagents MUST NOT:

- mark a stage `DONE`
- write `modeling_state.yaml`
- clear `pending_confirmations`
- treat user silence as approval
- execute rollback without Main Orchestrator approval
- skip required protocol reads

## Routing Map

| Stage | Owning Subagent |
|-------|-----------------|
| 1 | Model-Building Subagent |
| 2 | Model-Building Subagent |
| 3 | Model-Building Subagent |
| 4 | Model-Building Subagent |
| 5 | Model-Building Subagent |
| 6 | Validation-Paper Subagent |
| 7 | Validation-Paper Subagent |
| 8 | Validation-Paper Subagent |
| 9 | Validation-Paper Subagent |
| 10 | Validation-Paper Subagent |

## Specialist Trigger Map

| Specialist | Trigger |
|------------|---------|
| Data-Audit Specialist | Raw or processed data has unclear fields, missing values, outliers, version drift, or schema ambiguity. |
| Code-Review Specialist | Stage 5 produces solver code, reproducibility checks, or blocking implementation errors. |
| Figure-Review Specialist | Stage 9 reviews figure readability, caption quality, and evidence consistency. |
| Evidence-Gate Specialist | Stage 10 checks whether claims are supported by files and stage outputs. |
| Literature/Method Search Specialist | A method background or external reference is required and cannot be answered from local materials. |

## Delegation Input Contract

When delegating, Main Orchestrator must provide:

```yaml
delegation_request:
  active_stage: 7
  stage_name: "Sensitivity Analysis"
  owning_subagent: "Validation-Paper Subagent"
  required_reads:
    - "references/protocol-human-confirmation.md"
    - "references/protocol-memory-update.md"
    - "references/protocol-state-writeback.md"
    - "references/protocol-subagent-delegation.md"
    - "references/protocol-rollback.md"
    - "references/stage-7-sensitivity-analysis.md"
  available_inputs:
    - "data/results/main_result.csv"
    - "data/model_spec.yaml"
  expected_outputs:
    - "data/sensitivity/sensitivity_report.md"
  blocking_confirmation_policy: "Generate pending confirmation before downstream-dependent decisions."
  state_write_policy: "Recommend changes only; Main Orchestrator writes global state."
```

## Delegation Output Contract

Subagents must return:

```yaml
subagent_result:
  owning_subagent: "Validation-Paper Subagent"
  active_stage: 7
  status_recommendation: "DONE"
  outputs:
    - path: "data/sensitivity/sensitivity_report.md"
      purpose: "Summarize parameter perturbation findings."
  findings:
    - severity: "INFO"
      summary: "Main result is stable within tested perturbation bounds."
      evidence:
        - "data/sensitivity/perturbation_table.csv"
  pending_confirmation: null
  rollback_request: null
  memory_check_recommendation:
    action: "no new memory"
    reason: "No reusable modeling rule was discovered."
```

If a blocking decision is needed, `pending_confirmation` must be populated. If a previous stage must be revisited, `rollback_request` must be populated according to `references/protocol-rollback.md`.
```

- [ ] **Step 2: Verify the protocol file contains required contracts**

Run:

```powershell
Select-String -Path "references/protocol-subagent-delegation.md" -Pattern "Default mode is Lean Swarm", "Authority Boundary", "Routing Map", "Delegation Input Contract", "Delegation Output Contract"
```

Expected: all five patterns are returned.

- [ ] **Step 3: Commit the delegation protocol**

Run:

```bash
git add references/protocol-subagent-delegation.md
git commit -m "feat: add math-modeling subagent delegation protocol"
```

Expected: commit succeeds with only `references/protocol-subagent-delegation.md` staged.

---

### Task 2: Add the rollback protocol

**Files:**
- Create: `references/protocol-rollback.md`
- Test: content scan via PowerShell

- [ ] **Step 1: Create `references/protocol-rollback.md`**

Write this exact content:

```markdown
# Protocol — Rollback

## Purpose

Define how later stages request controlled rollback when validation, sensitivity analysis, visualization, figure review, or claim grounding exposes defects in earlier modeling work.

## Core Rule

Stages 6-10 MUST NOT silently patch defects that belong to stages 1-5.

If a defect affects problem interpretation, assumptions, model structure, algorithm choice, implementation, result stability, or claim support, the owning subagent must generate `rollback_request` and return it to the Main Orchestrator.

## Severity Levels

| Severity | Meaning | Default Target |
|----------|---------|----------------|
| `MINOR_REVISION` | Issue is limited to explanation, figure styling, caption wording, table formatting, or non-structural paper expression. | Stay in stages 6-10 |
| `METHOD_REVISION` | Algorithm, parameter bounds, solver implementation, reproducibility, result stability, or model constraint implementation is defective. | Stage 5, or Stage 4 if equations/constraints must change |
| `STRUCTURAL_REVISION` | Problem interpretation, core assumption, algorithm route, model structure, or innovation claim is invalid. | Stage 1, Stage 2, or Stage 3 |

## rollback_request Schema

```yaml
rollback_request:
  from_stage: 7
  target_stage: 5
  severity: "METHOD_REVISION"
  reason: "sensitivity analysis shows unstable output"
  evidence:
    - "data/validation/sensitivity_report.md"
  affected_outputs:
    - "data/results/main_result.csv"
    - "data/model_spec.yaml"
  requires_user_confirmation: true
  recommended_action: "rerun stage 5 with revised parameter bounds"
```

Required fields:

- `from_stage`
- `target_stage`
- `severity`
- `reason`
- `evidence`
- `affected_outputs`
- `requires_user_confirmation`
- `recommended_action`

## Confirmation Rules

- `MINOR_REVISION` may continue without blocking confirmation if no confirmed method, model structure, evidence path, or paper claim changes.
- `METHOD_REVISION` requires blocking confirmation unless the user already approved the exact fallback path.
- `STRUCTURAL_REVISION` always requires blocking confirmation.
- User silence never approves rollback.

## State Writeback Rules

When Main Orchestrator accepts a rollback request, it must:

1. Write the rollback request into `modeling_state.yaml` under `quality_systems.rollback_requests`.
2. If confirmation is required, write a blocking item into `human_interaction.pending_confirmations`.
3. Set the current stage to `HUMAN_REVIEW_REQUIRED` when confirmation is pending.
4. After confirmation, set the target stage to `NEEDS_REVISION` or `IN_PROGRESS` according to the decision.
5. Keep affected downstream stages from being marked `DONE` until regenerated or explicitly accepted by the user.

## rollback_response Contract

Stages 1-5 may receive a rollback request. Their owning subagent must return:

```yaml
rollback_response:
  target_stage: 5
  accepted_request: true
  revised_outputs:
    - "data/results/main_result.csv"
  unchanged_outputs:
    - "data/model_spec.yaml"
  downstream_invalidated:
    - 6
    - 7
    - 8
  pending_confirmation: null
  memory_check_recommendation:
    action: "write memory"
    reason: "Parameter bounds should be checked before sensitivity analysis in similar models."
```

## Non-Goals

Rollback does not replace Human Confirmation, memory check, State Writeback, Fallback Control, or Final Evidence Gate. It connects those protocols when later stages expose earlier defects.
```

- [ ] **Step 2: Verify the rollback protocol contains required schema**

Run:

```powershell
Select-String -Path "references/protocol-rollback.md" -Pattern "Severity Levels", "rollback_request Schema", "Confirmation Rules", "State Writeback Rules", "rollback_response Contract"
```

Expected: all five patterns are returned.

- [ ] **Step 3: Commit the rollback protocol**

Run:

```bash
git add references/protocol-rollback.md
git commit -m "feat: add math-modeling rollback protocol"
```

Expected: commit succeeds with only `references/protocol-rollback.md` staged.

---

### Task 3: Add primary subagent prompt contracts

**Files:**
- Create: `references/subagent-model-building.md`
- Create: `references/subagent-validation-paper.md`
- Test: content scan via PowerShell

- [ ] **Step 1: Create `references/subagent-model-building.md`**

Write this exact content:

```markdown
# Subagent — Model-Building

## Role

You are the Model-Building Subagent for `math-modeling`. You handle stages 1-5: problem understanding, algorithm selection, innovation design, model specification, and solution implementation.

## Scope

You may analyze, propose, draft, and review outputs for:

- Stage 1: Problem Understanding
- Stage 2: Algorithm Selection
- Stage 3: Innovation Design
- Stage 4: Model Specification
- Stage 5: Solution Implementation

You must follow the required reads supplied by Main Orchestrator. Do not rely on memory of the skill.

## Authority Boundary

You may recommend state changes, pending confirmations, memory updates, and rollback responses. You must not write `modeling_state.yaml`, clear pending confirmations, mark stages complete, or execute rollback.

## Required Output Shape

Return:

```yaml
subagent_result:
  owning_subagent: "Model-Building Subagent"
  active_stage: 5
  status_recommendation: "DONE"
  outputs:
    - path: "data/results/main_result.csv"
      purpose: "Primary solution output."
  findings:
    - severity: "INFO"
      summary: "Initial result passed sanity checks."
      evidence:
        - "data/results/result_sanity_check.json"
  pending_confirmation: null
  rollback_request: null
  rollback_response: null
  memory_check_recommendation:
    action: "no new memory"
    reason: "No reusable modeling rule was discovered."
```

## Stage-Specific Responsibilities

- Stage 1: Separate facts, assumptions, unknowns, and constraints. Flag ambiguous interpretation before downstream work.
- Stage 2: Provide 2-3 algorithm candidates, recommendation, risks, and confirmation point before final selection.
- Stage 3: Propose innovation candidates, score them, and separate paper-worthy innovation from implementation detail.
- Stage 4: Specify variables, assumptions, constraints, objective functions, and model dependencies.
- Stage 5: Implement or plan solution code, sanity-check results, and trigger code review when required.

## Rollback Response

If Main Orchestrator passes a rollback request targeting stages 1-5, inspect the affected assumptions, algorithm route, model structure, implementation, and outputs. Return a `rollback_response` instead of silently regenerating downstream artifacts.
```

- [ ] **Step 2: Create `references/subagent-validation-paper.md`**

Write this exact content:

```markdown
# Subagent — Validation-Paper

## Role

You are the Validation-Paper Subagent for `math-modeling`. You handle stages 6-10: independent validation, sensitivity analysis, visualization, figure review, and paper material preparation.

## Scope

You may analyze, propose, draft, and review outputs for:

- Stage 6: Independent Validation
- Stage 7: Sensitivity Analysis
- Stage 8: Visualization
- Stage 9: Figure Review
- Stage 10: Paper Materials

You must follow the required reads supplied by Main Orchestrator. Do not rely on memory of the skill.

## Authority Boundary

You may recommend state changes, pending confirmations, memory updates, and rollback requests. You must not write `modeling_state.yaml`, clear pending confirmations, mark stages complete, or execute rollback.

## Required Output Shape

Return:

```yaml
subagent_result:
  owning_subagent: "Validation-Paper Subagent"
  active_stage: 7
  status_recommendation: "DONE"
  outputs:
    - path: "data/sensitivity/sensitivity_report.md"
      purpose: "Sensitivity analysis summary."
  findings:
    - severity: "INFO"
      summary: "Main result is stable within tested perturbation bounds."
      evidence:
        - "data/sensitivity/perturbation_table.csv"
  pending_confirmation: null
  rollback_request: null
  memory_check_recommendation:
    action: "no new memory"
    reason: "No reusable modeling rule was discovered."
```

## Stage-Specific Responsibilities

- Stage 6: Independently validate or request explicit confirmation before skipping validation.
- Stage 7: Test parameter sensitivity and identify unstable result dependencies.
- Stage 8: Produce visualization plans and figure metadata consistent with evidence.
- Stage 9: Review figures for readability, captions, and claim consistency.
- Stage 10: Build claim registry, run evidence gate, and prepare paper materials only after claims are grounded.

## Rollback Request Rule

If stages 6-10 reveal defects in stages 1-5, return a `rollback_request` following `references/protocol-rollback.md`. Do not silently patch earlier-stage defects in downstream prose, figures, or claims.
```

- [ ] **Step 3: Verify primary subagent files**

Run:

```powershell
Select-String -Path "references/subagent-model-building.md" -Pattern "Model-Building Subagent", "Required Output Shape", "Rollback Response"
Select-String -Path "references/subagent-validation-paper.md" -Pattern "Validation-Paper Subagent", "Required Output Shape", "Rollback Request Rule"
```

Expected: all six patterns are returned.

- [ ] **Step 4: Commit primary subagent prompt contracts**

Run:

```bash
git add references/subagent-model-building.md references/subagent-validation-paper.md
git commit -m "feat: add math-modeling primary subagent contracts"
```

Expected: commit succeeds with only the two subagent prompt files staged.

---

### Task 4: Add specialist subagent prompt contracts

**Files:**
- Create: `references/subagent-specialists.md`
- Test: content scan via PowerShell

- [ ] **Step 1: Create `references/subagent-specialists.md`**

Write this exact content:

```markdown
# Subagents — Specialists

## Purpose

Define optional specialist subagents for `math-modeling`. Specialists are not always-on reviewers. Main Orchestrator invokes them only when a protocol or stage file explicitly triggers their expertise.

## Global Specialist Boundary

Specialists may return findings, risks, recommended actions, and evidence references. Specialists must not write global state, clear confirmations, execute rollback, or mark stages complete.

## Data-Audit Specialist

Trigger when raw or processed data has unclear fields, missing values, outliers, version drift, schema ambiguity, or inconsistent units.

Return:

```yaml
specialist_result:
  specialist: "Data-Audit Specialist"
  findings:
    - severity: "WARNING"
      summary: "Column units are inconsistent across files."
      evidence:
        - "data/raw/source_a.csv"
        - "data/raw/source_b.csv"
  recommended_action: "Create or revise data dictionary before algorithm selection."
  rollback_request: null
```

## Code-Review Specialist

Trigger when Stage 5 produces solver code, reproducibility checks, or blocking implementation errors.

Return:

```yaml
specialist_result:
  specialist: "Code-Review Specialist"
  findings:
    - severity: "BLOCKING"
      summary: "Solver output is not reproducible from a clean run."
      evidence:
        - "data/results/reproducibility_check.json"
  recommended_action: "Fix deterministic inputs and rerun Stage 5."
  rollback_request:
    from_stage: 5
    target_stage: 5
    severity: "METHOD_REVISION"
    reason: "solver output is not reproducible"
    evidence:
      - "data/results/reproducibility_check.json"
    affected_outputs:
      - "data/results/main_result.csv"
    requires_user_confirmation: true
    recommended_action: "rerun Stage 5 after reproducibility fix"
```

## Figure-Review Specialist

Trigger when Stage 9 reviews figure readability, caption quality, source data alignment, or claim consistency.

Return:

```yaml
specialist_result:
  specialist: "Figure-Review Specialist"
  findings:
    - severity: "WARNING"
      summary: "Figure caption does not identify the data source."
      evidence:
        - "data/figures/figure_3.meta.json"
  recommended_action: "Revise caption and metadata before paper export."
  rollback_request: null
```

## Evidence-Gate Specialist

Trigger when Stage 10 checks whether paper claims are supported by stage outputs and files.

Return:

```yaml
specialist_result:
  specialist: "Evidence-Gate Specialist"
  findings:
    - severity: "BLOCKING"
      summary: "Primary innovation claim lacks supporting comparison output."
      evidence:
        - "data/paper/claim_registry.yaml"
  recommended_action: "Return to Stage 3 or Stage 5 to generate evidence for the comparison."
  rollback_request:
    from_stage: 10
    target_stage: 3
    severity: "STRUCTURAL_REVISION"
    reason: "innovation claim lacks supporting comparison output"
    evidence:
      - "data/paper/claim_registry.yaml"
    affected_outputs:
      - "data/paper/innovation_summary.md"
    requires_user_confirmation: true
    recommended_action: "revise innovation claim or generate valid comparison evidence"
```

## Literature/Method Search Specialist

Trigger when a method background or external reference is required and cannot be answered from local materials. Network access must follow the available web-access workflow and user authorization requirements.

Return:

```yaml
specialist_result:
  specialist: "Literature/Method Search Specialist"
  findings:
    - severity: "INFO"
      summary: "A comparable method family exists and should be considered as a baseline."
      evidence:
        - "external reference captured through authorized web workflow"
  recommended_action: "Add the method as a candidate in Stage 2 before final algorithm confirmation."
  rollback_request: null
```
```

- [ ] **Step 2: Verify specialist triggers and boundaries**

Run:

```powershell
Select-String -Path "references/subagent-specialists.md" -Pattern "Data-Audit Specialist", "Code-Review Specialist", "Figure-Review Specialist", "Evidence-Gate Specialist", "Literature/Method Search Specialist", "Global Specialist Boundary"
```

Expected: all six patterns are returned.

- [ ] **Step 3: Commit specialist prompt contracts**

Run:

```bash
git add references/subagent-specialists.md
git commit -m "feat: add math-modeling specialist subagent contracts"
```

Expected: commit succeeds with only `references/subagent-specialists.md` staged.

---

### Task 5: Update `SKILL.md` dispatcher

**Files:**
- Modify: `SKILL.md`
- Test: content scan via PowerShell

- [ ] **Step 1: Add protocol-first and subagent rules after the strong blocking rules**

In `SKILL.md`, after the list ending with `沉默不等于同意；只有明确回复才可解除阻断。`, insert:

```markdown
## Protocol-First Rule

Before answering, editing, calculating, coding, visualizing, validating, or exporting, identify the active command, stage, and protocol, then read the required reference files.

Rules:
1. Do not rely on memory of this skill; current reference files are authoritative.
2. If a protocol or stage might apply, load it before acting.
3. Before stage execution, identify active stage, required reads, expected outputs, owning subagent, and blocking confirmation point.
4. If a later stage exposes an earlier-stage defect, follow `references/protocol-rollback.md` instead of silently patching downstream artifacts.

## Subagent Delegation Policy

Default mode is Lean Swarm.

- Stages 1-5 MUST be delegated to Model-Building Subagent.
- Stages 6-10 MUST be delegated to Validation-Paper Subagent.
- Specialist subagents MAY be invoked only when their protocol is explicitly triggered.
- Subagents must return structured outputs, not free-form discussion.
- Subagents may recommend state changes, but only Main Orchestrator can write global state.
- Subagents may propose `rollback_request`, but cannot execute rollback directly.
```

- [ ] **Step 2: Update the dispatch table rows**

Replace the existing dispatch table rows with:

```markdown
| 场景 | 必读文件 |
|------|----------|
| invoke / progress / status | `references/protocol-state-writeback.md` |
| next / stage N | `references/protocol-human-confirmation.md` + `references/protocol-memory-update.md` + `references/protocol-state-writeback.md` + `references/protocol-subagent-delegation.md` + `references/protocol-rollback.md` + 对应 `references/stage-N-*.md` |
| pending / confirm / approve / reject | `references/protocol-human-confirmation.md` + `references/protocol-state-writeback.md` |
| rollback request / rollback response | `references/protocol-rollback.md` + `references/protocol-human-confirmation.md` + `references/protocol-state-writeback.md` + `references/protocol-subagent-delegation.md` |
| audit | `references/data-audit.md` + `references/protocol-state-writeback.md` + `references/subagent-specialists.md` |
| review | `references/stage-9-figure-review.md` + `references/figure-review.md` + `references/caption-spec.md` + `references/protocol-subagent-delegation.md` + `references/subagent-specialists.md` |
| gate / export | `references/stage-10-paper-materials.md` + `references/claim-grounding.md` + `references/evidence-gate.md` + `references/protocol-state-writeback.md` + `references/protocol-rollback.md` |
```

- [ ] **Step 3: Add subagent reads to stage additional reads**

Replace the existing `阶段附加读取` list with:

```markdown
阶段附加读取：
- 阶段 1：`references/anti-hallucination.md` + `references/subagent-model-building.md`
- 阶段 2：`references/anti-hallucination.md` + `references/subagent-model-building.md`
- 阶段 3：`references/innovation-design.md` + `references/subagent-model-building.md`
- 阶段 4：`references/subagent-model-building.md`
- 阶段 5：`references/code-review-pipeline.md` + `references/subagent-model-building.md` + `references/subagent-specialists.md`
- 阶段 6：`references/subagent-validation-paper.md`
- 阶段 7：`references/sensitivity-analysis.md` + `references/subagent-validation-paper.md`
- 阶段 8：`references/caption-spec.md` + `references/subagent-validation-paper.md`
- 阶段 9：`references/figure-review.md` + `references/caption-spec.md` + `references/subagent-validation-paper.md` + `references/subagent-specialists.md`
- 阶段 10：`references/claim-grounding.md` + `references/evidence-gate.md` + `references/caption-spec.md` + `references/subagent-validation-paper.md` + `references/subagent-specialists.md`
```

- [ ] **Step 4: Add rollback hard constraint**

In `全局硬约束`, add this item before the existing export gate item:

```markdown
9. 阶段 6-10 若发现阶段 1-5 的题意、假设、模型结构、算法、实现或证据缺陷，必须生成 `rollback_request`，不得静默修补下游产物。
10. `export` 之前必须通过 Final Evidence Gate。
```

If the existing export gate item is numbered `9`, renumber it to `10`.

- [ ] **Step 5: Extend the schema index**

Inside the existing YAML schema block, after `quality_systems.final_evidence_gate`, add:

```yaml
  rollback_requests:
    - from_stage: 7
      target_stage: 5
      severity: "METHOD_REVISION"
      reason: "sensitivity analysis shows unstable output"
      evidence: []
      affected_outputs: []
      requires_user_confirmation: true
      recommended_action: "rerun stage 5 with revised parameter bounds"
```

- [ ] **Step 6: Add new references to the reference map**

Under `协议文件`, add:

```markdown
- `references/protocol-subagent-delegation.md`
- `references/protocol-rollback.md`
```

After the stage file list, add:

```markdown
Subagent 文件：
- `references/subagent-model-building.md`
- `references/subagent-validation-paper.md`
- `references/subagent-specialists.md`
```

- [ ] **Step 7: Verify `SKILL.md` contains the Lean Swarm dispatcher updates**

Run:

```powershell
Select-String -Path "SKILL.md" -Pattern "Protocol-First Rule", "Subagent Delegation Policy", "protocol-subagent-delegation", "protocol-rollback", "subagent-model-building", "subagent-validation-paper", "rollback_request"
```

Expected: all seven patterns are returned.

- [ ] **Step 8: Commit `SKILL.md` dispatcher updates**

Run:

```bash
git add SKILL.md
git commit -m "feat: wire lean swarm protocols into math-modeling dispatcher"
```

Expected: commit succeeds with only `SKILL.md` staged.

---

### Task 6: Annotate stages 1-5 with Model-Building ownership

**Files:**
- Modify: `references/stage-1-problem-understanding.md`
- Modify: `references/stage-2-algorithm-selection.md`
- Modify: `references/stage-3-innovation-design.md`
- Modify: `references/stage-4-model-spec.md`
- Modify: `references/stage-5-solution-implementation.md`
- Test: content scan via PowerShell

- [ ] **Step 1: Add owning subagent section to each stage 1-5 file**

In each of these files, insert the following section after the title line:

```markdown
## Owning Subagent

Model-Building Subagent

## Delegation Contract

The Main Orchestrator loads required protocols, passes scoped inputs to the Model-Building Subagent, and receives structured outputs. The subagent may recommend state changes, pending confirmations, memory updates, and rollback responses, but must not write global state.
```

Files:

```text
references/stage-1-problem-understanding.md
references/stage-2-algorithm-selection.md
references/stage-3-innovation-design.md
references/stage-4-model-spec.md
references/stage-5-solution-implementation.md
```

- [ ] **Step 2: Add subagent and rollback protocols to required reads**

In each stage 1-5 file, ensure `## Required Reads` contains:

```markdown
- `references/protocol-subagent-delegation.md`
- `references/protocol-rollback.md`
- `references/subagent-model-building.md`
```

Keep existing required reads in place.

- [ ] **Step 3: Add rollback response section to each stage 1-5 file**

Before `## Done When`, insert:

```markdown
## Rollback Response

If this stage receives a `rollback_request`, inspect the affected assumptions, model structure, algorithm choice, implementation outputs, and downstream dependencies before regenerating artifacts. Return a structured `rollback_response` to the Main Orchestrator; do not directly mark downstream stages complete.
```

- [ ] **Step 4: Verify Model-Building ownership across stages 1-5**

Run:

```powershell
$files = @(
  "references/stage-1-problem-understanding.md",
  "references/stage-2-algorithm-selection.md",
  "references/stage-3-innovation-design.md",
  "references/stage-4-model-spec.md",
  "references/stage-5-solution-implementation.md"
)
foreach ($file in $files) {
  Select-String -Path $file -Pattern "Owning Subagent", "Model-Building Subagent", "protocol-subagent-delegation", "protocol-rollback", "subagent-model-building", "Rollback Response"
}
```

Expected: each file returns all six patterns.

- [ ] **Step 5: Commit stage 1-5 annotations**

Run:

```bash
git add references/stage-1-problem-understanding.md references/stage-2-algorithm-selection.md references/stage-3-innovation-design.md references/stage-4-model-spec.md references/stage-5-solution-implementation.md
git commit -m "feat: assign model-building subagent to math-modeling stages 1-5"
```

Expected: commit succeeds with only stage 1-5 files staged.

---

### Task 7: Annotate stages 6-10 with Validation-Paper ownership and rollback triggers

**Files:**
- Modify: `references/stage-6-independent-validation.md`
- Modify: `references/stage-7-sensitivity-analysis.md`
- Modify: `references/stage-8-visualization.md`
- Modify: `references/stage-9-figure-review.md`
- Modify: `references/stage-10-paper-materials.md`
- Test: content scan via PowerShell

- [ ] **Step 1: Add owning subagent section to each stage 6-10 file**

In each of these files, insert the following section after the title line:

```markdown
## Owning Subagent

Validation-Paper Subagent

## Delegation Contract

The Main Orchestrator loads required protocols, passes scoped inputs to the Validation-Paper Subagent, and receives structured outputs. The subagent may recommend state changes, pending confirmations, memory updates, and rollback requests, but must not write global state.
```

Files:

```text
references/stage-6-independent-validation.md
references/stage-7-sensitivity-analysis.md
references/stage-8-visualization.md
references/stage-9-figure-review.md
references/stage-10-paper-materials.md
```

- [ ] **Step 2: Add subagent and rollback protocols to required reads**

In each stage 6-10 file, ensure `## Required Reads` contains:

```markdown
- `references/protocol-subagent-delegation.md`
- `references/protocol-rollback.md`
- `references/subagent-validation-paper.md`
```

Keep existing required reads in place.

- [ ] **Step 3: Add rollback trigger section to each stage 6-10 file**

Before `## Done When`, insert:

```markdown
## Rollback Triggers

If validation, sensitivity analysis, visualization, figure review, claim grounding, or evidence gating exposes a defect in assumptions, model structure, algorithm choice, implementation, result stability, or evidence support from stages 1-5, generate a structured `rollback_request` instead of silently patching downstream artifacts.
```

- [ ] **Step 4: Verify Validation-Paper ownership across stages 6-10**

Run:

```powershell
$files = @(
  "references/stage-6-independent-validation.md",
  "references/stage-7-sensitivity-analysis.md",
  "references/stage-8-visualization.md",
  "references/stage-9-figure-review.md",
  "references/stage-10-paper-materials.md"
)
foreach ($file in $files) {
  Select-String -Path $file -Pattern "Owning Subagent", "Validation-Paper Subagent", "protocol-subagent-delegation", "protocol-rollback", "subagent-validation-paper", "rollback_request"
}
```

Expected: each file returns all six patterns.

- [ ] **Step 5: Commit stage 6-10 annotations**

Run:

```bash
git add references/stage-6-independent-validation.md references/stage-7-sensitivity-analysis.md references/stage-8-visualization.md references/stage-9-figure-review.md references/stage-10-paper-materials.md
git commit -m "feat: assign validation-paper subagent to math-modeling stages 6-10"
```

Expected: commit succeeds with only stage 6-10 files staged.

---

### Task 8: Update README for Lean Swarm behavior

**Files:**
- Modify: `README.md`
- Test: content scan via PowerShell

- [ ] **Step 1: Add Lean Swarm section after `新增行为保证`**

In `README.md`, after the existing fallback behavior section, insert:

```markdown
### 4. Lean Swarm subagent delegation

默认使用 Lean Swarm，而不是 full swarm：

- 阶段 1-5 由 Model-Building Subagent 负责；
- 阶段 6-10 由 Validation-Paper Subagent 负责；
- Data-Audit、Code-Review、Figure-Review、Evidence-Gate、Literature/Method Search 等 specialist 只在协议明确触发时调用；
- subagent 返回结构化建议，不直接写全局状态；
- Main Orchestrator 仍然唯一负责 `modeling_state.yaml`、`pending_confirmations`、memory check、用户确认与 rollback 执行。

### 5. rollback request

阶段 6-10 如果发现阶段 1-5 的题意、假设、模型结构、算法、实现或证据缺陷，不允许静默修补论文表达或图表，而是生成 `rollback_request` 交给 Main Orchestrator 判断。

默认回滚等级：

- `MINOR_REVISION`：留在阶段 6-10 内修正；
- `METHOD_REVISION`：回到阶段 5，必要时回到阶段 4；
- `STRUCTURAL_REVISION`：回到阶段 1-3。

暂不引入外部 full swarm prompt。当前目标是流程稳定性、证据链、状态写回和回滚可控性，而不是增加常驻角色数量。
```

- [ ] **Step 2: Add new quality systems to the cross-cutting table**

In the `横向质量系统` table, add these rows after `Fallback Control`:

```markdown
| Subagent Delegation | Lean Swarm 分工与权限边界 | `references/protocol-subagent-delegation.md` |
| Rollback Control | 后半阶段发现前半阶段缺陷时的受控回滚 | `references/protocol-rollback.md` |
```

- [ ] **Step 3: Add new protocol references**

Under `### 协议文件`, add:

```markdown
- `references/protocol-subagent-delegation.md`
- `references/protocol-rollback.md`
```

- [ ] **Step 4: Add subagent reference section**

After the `### 阶段文件` list, add:

```markdown
### Subagent 文件
- `references/subagent-model-building.md`
- `references/subagent-validation-paper.md`
- `references/subagent-specialists.md`
```

- [ ] **Step 5: Verify README documents Lean Swarm**

Run:

```powershell
Select-String -Path "README.md" -Pattern "Lean Swarm", "Model-Building Subagent", "Validation-Paper Subagent", "rollback_request", "protocol-subagent-delegation", "protocol-rollback", "full swarm"
```

Expected: all seven patterns are returned.

- [ ] **Step 6: Commit README updates**

Run:

```bash
git add README.md
git commit -m "docs: document lean swarm math-modeling workflow"
```

Expected: commit succeeds with only `README.md` staged.

---

### Task 9: Run final consistency verification

**Files:**
- Test: `SKILL.md`, `README.md`, `references/*.md`

- [ ] **Step 1: Verify all required new files exist**

Run:

```powershell
$files = @(
  "references/protocol-subagent-delegation.md",
  "references/protocol-rollback.md",
  "references/subagent-model-building.md",
  "references/subagent-validation-paper.md",
  "references/subagent-specialists.md"
)
foreach ($file in $files) {
  if (-not (Test-Path $file)) { throw "Missing $file" }
  Write-Output "OK $file"
}
```

Expected: five `OK` lines and no thrown error.

- [ ] **Step 2: Verify dispatcher and docs mention new protocols**

Run:

```powershell
Select-String -Path "SKILL.md", "README.md" -Pattern "protocol-subagent-delegation", "protocol-rollback", "subagent-model-building", "subagent-validation-paper", "subagent-specialists"
```

Expected: all five patterns appear in both `SKILL.md` and `README.md`.

- [ ] **Step 3: Verify stage ownership counts**

Run:

```powershell
$modelBuilding = Select-String -Path "references/stage-*.md" -Pattern "Model-Building Subagent"
$validationPaper = Select-String -Path "references/stage-*.md" -Pattern "Validation-Paper Subagent"
if ($modelBuilding.Count -lt 5) { throw "Expected Model-Building Subagent in stages 1-5" }
if ($validationPaper.Count -lt 5) { throw "Expected Validation-Paper Subagent in stages 6-10" }
Write-Output "OK model-building count: $($modelBuilding.Count)"
Write-Output "OK validation-paper count: $($validationPaper.Count)"
```

Expected: both counts are at least 5.

- [ ] **Step 4: Verify rollback triggers exist in stages 6-10**

Run:

```powershell
$files = @(
  "references/stage-6-independent-validation.md",
  "references/stage-7-sensitivity-analysis.md",
  "references/stage-8-visualization.md",
  "references/stage-9-figure-review.md",
  "references/stage-10-paper-materials.md"
)
foreach ($file in $files) {
  $match = Select-String -Path $file -Pattern "rollback_request"
  if (-not $match) { throw "Missing rollback_request in $file" }
  Write-Output "OK $file"
}
```

Expected: five `OK` lines and no thrown error.

- [ ] **Step 5: Check git status**

Run:

```bash
git status --short
```

Expected: no uncommitted files remain if each previous task committed successfully.

- [ ] **Step 6: Commit verification adjustments if any were needed**

If verification required edits, run:

```bash
git add SKILL.md README.md references/protocol-subagent-delegation.md references/protocol-rollback.md references/subagent-model-building.md references/subagent-validation-paper.md references/subagent-specialists.md references/stage-1-problem-understanding.md references/stage-2-algorithm-selection.md references/stage-3-innovation-design.md references/stage-4-model-spec.md references/stage-5-solution-implementation.md references/stage-6-independent-validation.md references/stage-7-sensitivity-analysis.md references/stage-8-visualization.md references/stage-9-figure-review.md references/stage-10-paper-materials.md
git commit -m "chore: align lean swarm math-modeling references"
```

Expected: commit succeeds only if verification edits were made. If `git status --short` is empty, skip this step.

---

## Self-Review Notes

Spec coverage:

- 10-stage flow remains unchanged: Tasks 5-8 only add dispatcher, protocols, and annotations.
- Stages 1-5 and 6-10 are assigned to different primary subagents: Tasks 3, 6, and 7.
- Lean Swarm is documented and full swarm is excluded by default: Tasks 4 and 8.
- Protocol-first rule is added to dispatcher: Task 5.
- Rollback protocol and stage triggers are added: Tasks 2, 5, and 7.
- Main Orchestrator authority boundary is preserved: Tasks 1, 3, 4, 5, 6, and 7.

Placeholder scan:

- The plan contains no `TBD`, `TODO`, or unspecified implementation steps.
- Every file creation task includes exact markdown content.
- Every verification step includes exact commands and expected results.

Type consistency:

- `rollback_request`, `rollback_response`, `subagent_result`, `pending_confirmation`, and `memory_check_recommendation` use consistent names across protocol, subagent, and stage tasks.
