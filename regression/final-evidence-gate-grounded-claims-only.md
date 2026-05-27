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
