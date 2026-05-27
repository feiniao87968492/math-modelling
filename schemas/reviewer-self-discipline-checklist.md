# Reviewer Self-Discipline Checklist (v4.2)

## Purpose

Provide every reviewer subagent the canonical list of forbidden behaviors that its `## Forbidden-behavior self-check` section must enumerate. Each item is either `[OK]` (asserted not violated), `[N/A]` (does not apply to this profile), or `[VIOLATED]` (review fails acceptance and must be re-spawned).

## Universal items (apply to all reviewer profiles)

```markdown
- [OK|N/A|VIOLATED] Did not confirm user decisions
- [OK|N/A|VIOLATED] Did not clear blockers
- [OK|N/A|VIOLATED] Did not mark stages or rounds complete
- [OK|N/A|VIOLATED] Did not increase claim level on behalf of the main agent
- [OK|N/A|VIOLATED] Did not invoke another subagent
- [OK|N/A|VIOLATED] Did not write or edit project files outside the review output
```

## Improvement loop additional items (Critique + Skepticism)

```markdown
- [OK|N/A|VIOLATED] Compared against baseline snapshot, not the previous round
- [OK|N/A|VIOLATED] Did not silently approve proposals
- [OK|N/A|VIOLATED] Did not propose changes that bypass v4 readiness gate or rollback protocols
```

## Improvement-Skepticism only

```markdown
- [OK|N/A|VIOLATED] Did not run without an upstream Critique review file
- [OK|N/A|VIOLATED] Every Blocking risk includes Evidence reference + Required mitigation
- [OK|N/A|VIOLATED] Did not reject proposals without an evidence reference
```

## Improvement-Critique only

```markdown
- [OK|N/A|VIOLATED] Did not invoke the Improvement-Skepticism Reviewer (main agent's responsibility)
- [OK|N/A|VIOLATED] Every Finding includes Hypothesis + Expected metric delta + Implementation cost + Required new data or solver + Touches confirmed method or model structure + Suggested claim level after success
```

## Stage 6 Validation Reviewer additional

```markdown
- [OK|N/A|VIOLATED] Did not write claims/baseline-snapshot.md (only recommended freezing)
- [OK|N/A|VIOLATED] Did not export when the final evidence gate has not passed
```

## Stage 10 Evidence/Claim Reviewer additional

```markdown
- [OK|N/A|VIOLATED] Did not write gates/final-evidence-gate.md (main agent's responsibility)
- [OK|N/A|VIOLATED] Audited every claim in claim-registry against its supporting gate's claim level
```

## Usage

Reviewer profile docs (`references/subagent-*.md` and registered agent docs in `~/.claude/agents/mm-*-reviewer.md`) reference this file. Each reviewer's `## Forbidden-behavior self-check` section in its output must enumerate the universal items plus any profile-specific items applicable to its role.

`[VIOLATED]` is permitted only as a transparency mechanism: a reviewer who realized mid-review that it crossed a boundary should mark the item `[VIOLATED]` with a one-line note, write the review, and let the dispatcher re-spawn. Hidden violations are worse than disclosed ones.
