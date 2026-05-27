# Ground-Truth Fixture - Stage 5 Buggy Implementation Mismatch

## Reviewer under test
mm-implementation-readiness-reviewer

## Buggy artifact summary
The Stage 4 model spec freezes a Crank-Nicolson finite-difference scheme with explicit numerical parameters (Δt = 0.001, mesh 200x200, BC type Dirichlet). The Stage 5 readiness assessment reports that the implementation will use forward-Euler with no mention of Δt. The Δt is hard-coded as 0.01 in `code/python/main.py` skeleton, which exceeds CFL stability for the chosen mesh.

## Ground-truth artifact paths
- `data/model-spec.md` — declares Crank-Nicolson, Δt=0.001, mesh 200x200, Dirichlet BC
- `code/python/main.py` — uses forward-Euler with Δt=0.01
- `gates/stage4-model-readiness-gate.md` — supported claim level = `feasible_baseline`

## Buggy quotes
- "时间推进采用 Crank-Nicolson 隐式格式，时间步 Δt = 0.001 s" (model-spec.md)
- "for k in range(N_steps): u_new = u + dt * rhs(u)" (main.py — explicit Euler)
- "dt = 0.01" (main.py top constant)

## A profile-conformant Implementation Readiness Reviewer is expected to flag
- `solver-route-mismatches-spec` — forward-Euler vs frozen Crank-Nicolson
- `cfl-violation-risk` — Δt=0.01 with mesh 200x200 likely violates stability for parabolic PDE
- `dt-divergence-from-spec` — code Δt 10× larger than spec Δt
- `implementation-must-not-proceed-without-rollback` — diverging from frozen Stage 4 spec is a fallback that requires rollback decision per protocol-rollback.md
