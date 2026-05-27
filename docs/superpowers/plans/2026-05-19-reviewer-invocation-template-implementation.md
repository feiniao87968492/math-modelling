# Reviewer Invocation Template Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a dispatcher-level reviewer invocation template to `math-modeling-v4` so missing fixed-review artifacts lead to a concrete, standardized reviewer-spawn action rather than a vague blocker message.

**Architecture:** Keep the change documentation-first. Update the dispatcher, delegation protocol, and affected stage contracts so they all describe the same invocation template fields and the same four fixed-review file mappings. Protect the new wording with documentation contract tests only; do not add a new runtime orchestration API in this slice.

**Tech Stack:** Markdown documentation, Python `pytest` regression tests

---

## File Map

- Modify: `C:\Users\zty\.agents\skills\math-modeling-v4\SKILL.md`
- Modify: `C:\Users\zty\.agents\skills\math-modeling-v4\references\protocol-subagent-delegation.md`
- Modify: `C:\Users\zty\.agents\skills\math-modeling-v4\references\stage-4-model-spec.md`
- Modify: `C:\Users\zty\.agents\skills\math-modeling-v4\references\stage-5-solution-implementation.md`
- Modify: `C:\Users\zty\.agents\skills\math-modeling-v4\references\stage-6-independent-validation.md`
- Modify: `C:\Users\zty\.agents\skills\math-modeling-v4\references\stage-10-paper-materials.md`
- Modify: `C:\Users\zty\.agents\skills\math-modeling-v4\regression\test_markdown_first_contracts.py`

### Task 1: Add the failing documentation contract test

**Files:**
- Modify: `C:\Users\zty\.agents\skills\math-modeling-v4\regression\test_markdown_first_contracts.py`
- Test: `C:\Users\zty\.agents\skills\math-modeling-v4\regression\test_markdown_first_contracts.py`

- [ ] **Step 1: Read the current contract test file and place the new test after the fixed-review-gate assertions**

Use the existing test grouping so all reviewer-gate assertions stay together.

- [ ] **Step 2: Add a failing test for invocation-template wording**

Append a test like this:

```python
def test_reviewer_invocation_template_is_defined_for_fixed_review_gates():
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    protocol = (ROOT / "references" / "protocol-subagent-delegation.md").read_text(
        encoding="utf-8"
    )
    stage4 = (ROOT / "references" / "stage-4-model-spec.md").read_text(encoding="utf-8")
    stage5 = (ROOT / "references" / "stage-5-solution-implementation.md").read_text(
        encoding="utf-8"
    )
    stage6 = (ROOT / "references" / "stage-6-independent-validation.md").read_text(
        encoding="utf-8"
    )
    stage10 = (ROOT / "references" / "stage-10-paper-materials.md").read_text(
        encoding="utf-8"
    )

    assert "## Reviewer Invocation Template" in skill
    assert "Spawn Reviewer:" in skill
    assert "Expected Output Path:" in skill
    assert "## Reviewer Invocation Template" in protocol
    assert "Blocking Question:" in protocol
    assert "reviews/stage4-algorithm-model-review.md" in protocol
    assert "reviews/stage5-implementation-readiness-review.md" in protocol
    assert "reviews/stage6-validation-review.md" in protocol
    assert "reviews/stage10-evidence-claim-review.md" in protocol
    assert "emit the reviewer invocation template" in stage4
    assert "emit the reviewer invocation template" in stage5
    assert "emit the reviewer invocation template" in stage6
    assert "emit the reviewer invocation template" in stage10
```

- [ ] **Step 3: Run the focused test and verify it fails**

Run:

```bash
python -m pytest regression/test_markdown_first_contracts.py -q
```

Expected:

```text
FAIL
```

The failure should mention missing invocation-template headings or missing wording in the stage docs.

- [ ] **Step 4: Commit the failing test**

```bash
git add regression/test_markdown_first_contracts.py
git commit -m "test: require reviewer invocation template wording"
```

### Task 2: Add the invocation template to `SKILL.md`

**Files:**
- Modify: `C:\Users\zty\.agents\skills\math-modeling-v4\SKILL.md`

- [ ] **Step 1: Add a new `## Reviewer Invocation Template` section**

Insert a new section after `## Expert Review Policy` with content like:

```md
## Reviewer Invocation Template

When a mandatory fixed-review artifact is missing, the main agent must not only block continuation. The next legal action is to emit a reviewer invocation template and stop downstream work until the review artifact exists.

Template:

```text
Spawn Reviewer: <Reviewer Name>
Trigger: <Why this reviewer is now mandatory>
Required Reads:
- <reference/path>
- <reference/path>
- <project/path>
Expected Output Path:
- <reviews/...md>
Review Scope:
- <scope item>
- <scope item>
Blocking Question:
- <question that must be answered before continuation>
```
```

- [ ] **Step 2: Add one concrete example**

Include a Stage 5 example such as:

```text
Spawn Reviewer: Implementation Readiness Reviewer
Trigger: Missing mandatory fixed-review artifact before implementation code
Required Reads:
- references/protocol-subagent-delegation.md
- references/stage-5-solution-implementation.md
- workflow.md
- memory.md
Expected Output Path:
- reviews/stage5-implementation-readiness-review.md
Review Scope:
- confirmed model specification
- confirmed algorithm route
- implementation readiness blockers
Blocking Question:
- Is the project ready to enter implementation code work?
```

- [ ] **Step 3: Keep the section explicit that this is dispatcher guidance, not a runtime API**

Add one sentence clarifying:

```md
This template is dispatcher-level invocation guidance, not a process orchestration API.
```

- [ ] **Step 4: Commit the `SKILL.md` update**

```bash
git add SKILL.md
git commit -m "docs: add reviewer invocation template to dispatcher"
```

### Task 3: Define the invocation contract in the delegation protocol

**Files:**
- Modify: `C:\Users\zty\.agents\skills\math-modeling-v4\references\protocol-subagent-delegation.md`

- [ ] **Step 1: Add a `## Reviewer Invocation Template` section**

Insert a new section with the field list:

```md
## Reviewer Invocation Template

When a mandatory fixed-review artifact is missing, the main agent must emit a reviewer invocation template instead of only describing the blocker.

Required fields:

- `Reviewer`
- `Trigger`
- `Required Reads`
- `Expected Output Path`
- `Review Scope`
- `Blocking Question`
```

- [ ] **Step 2: Add the stable mapping for the four fixed review files**

Use a mapping table like:

```md
| Workflow point | Reviewer | Expected output path |
|---|---|---|
| Stage 4 pre-freeze | Algorithm/Model Reviewer | `reviews/stage4-algorithm-model-review.md` |
| Stage 5 pre-implementation | Implementation Readiness Reviewer | `reviews/stage5-implementation-readiness-review.md` |
| Stage 6 post-result | Validation Reviewer | `reviews/stage6-validation-review.md` |
| Stage 10 pre-claim/export | Evidence/Claim Reviewer | `reviews/stage10-evidence-claim-review.md` |
```

- [ ] **Step 3: Add the non-bypass wording**

Include language such as:

```md
The main agent must invoke the corresponding reviewer template and target the mapped `reviews/*.md` path. It must not stop at a generic blocker message.
```

- [ ] **Step 4: Commit the protocol update**

```bash
git add references/protocol-subagent-delegation.md
git commit -m "docs: define reviewer invocation contract"
```

### Task 4: Update the affected stage contracts

**Files:**
- Modify: `C:\Users\zty\.agents\skills\math-modeling-v4\references\stage-4-model-spec.md`
- Modify: `C:\Users\zty\.agents\skills\math-modeling-v4\references\stage-5-solution-implementation.md`
- Modify: `C:\Users\zty\.agents\skills\math-modeling-v4\references\stage-6-independent-validation.md`
- Modify: `C:\Users\zty\.agents\skills\math-modeling-v4\references\stage-10-paper-materials.md`

- [ ] **Step 1: Replace “stop and spawn” wording with template-based wording**

Update each stage’s blocking rule from:

```md
if missing, stop and spawn the required reviewer subagent first
```

to:

```md
if missing, emit the reviewer invocation template for the required reviewer and stop downstream work
```

- [ ] **Step 2: Keep each stage tied to its exact file**

Ensure the four stage docs still include:

- `reviews/stage4-algorithm-model-review.md`
- `reviews/stage5-implementation-readiness-review.md`
- `reviews/stage6-validation-review.md`
- `reviews/stage10-evidence-claim-review.md`

- [ ] **Step 3: Keep the stage docs concise**

Do not paste the full invocation template into every stage file. Keep the detailed field list centralized in the protocol.

- [ ] **Step 4: Commit the stage contract updates**

```bash
git add references/stage-4-model-spec.md references/stage-5-solution-implementation.md references/stage-6-independent-validation.md references/stage-10-paper-materials.md
git commit -m "docs: route fixed review blockers through invocation template"
```

### Task 5: Run tests and validate scope control

**Files:**
- Modify: `C:\Users\zty\.agents\skills\math-modeling-v4\SKILL.md`
- Modify: `C:\Users\zty\.agents\skills\math-modeling-v4\references\protocol-subagent-delegation.md`
- Modify: `C:\Users\zty\.agents\skills\math-modeling-v4\references\stage-4-model-spec.md`
- Modify: `C:\Users\zty\.agents\skills\math-modeling-v4\references\stage-5-solution-implementation.md`
- Modify: `C:\Users\zty\.agents\skills\math-modeling-v4\references\stage-6-independent-validation.md`
- Modify: `C:\Users\zty\.agents\skills\math-modeling-v4\references\stage-10-paper-materials.md`
- Modify: `C:\Users\zty\.agents\skills\math-modeling-v4\regression\test_markdown_first_contracts.py`

- [ ] **Step 1: Run the focused documentation contract test**

Run:

```bash
python -m pytest regression/test_markdown_first_contracts.py -q
```

Expected:

```text
PASS
```

- [ ] **Step 2: Run the full regression suite**

Run:

```bash
python -m pytest regression/test_markdown_first_contracts.py regression/test_readiness_gate_checks.py regression/test_readiness_gate_smoke_flow.py regression/test_readiness_gate_command_flow.py regression/test_gate_and_rollback_checks.py regression/test_export_command_flow.py regression/test_rollback_command_flow.py -q
```

Expected:

```text
all tests pass
```

- [ ] **Step 3: Review scope**

Confirm:

- no new helper API was added,
- no runtime process orchestration hook was introduced,
- only dispatcher/protocol/stage wording changed,
- the old `math-modeling` package remains untouched.

- [ ] **Step 4: Commit the finished slice**

```bash
git add SKILL.md references/protocol-subagent-delegation.md references/stage-4-model-spec.md references/stage-5-solution-implementation.md references/stage-6-independent-validation.md references/stage-10-paper-materials.md regression/test_markdown_first_contracts.py
git commit -m "docs: add reviewer invocation template guidance"
```

## Self-Review

### Spec coverage

- Dispatcher-level invocation template: covered by Task 2.
- Protocol-level invocation contract: covered by Task 3.
- Stage-doc routing through template behavior: covered by Task 4.
- Minimal documentation contract tests: covered by Task 1 and Task 5.
- No runtime API expansion: enforced by Task 5 scope review.

### Placeholder scan

No placeholders remain. All files, assertions, and commands are explicit.

### Type consistency

The plan consistently uses:

- `## Reviewer Invocation Template`
- `reviews/stage4-algorithm-model-review.md`
- `reviews/stage5-implementation-readiness-review.md`
- `reviews/stage6-validation-review.md`
- `reviews/stage10-evidence-claim-review.md`

No alternate names or duplicate template sections are introduced.
