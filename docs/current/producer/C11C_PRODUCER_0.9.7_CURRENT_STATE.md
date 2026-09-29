# C11-C Producer 0.9.7 — Current State / C11-C 2.19.12 Closure Candidate

## Authority

The live Producer is `c11c-suite/c11c-producer/`.

C11-C 2.19.12 is the final closure candidate, not yet frozen. Producer version remains 0.9.7.

## Boundary

Producer remains orchestration-only. It invokes canonical launchers and does not duplicate engine mechanics, RNG, timing truth or gameplay calculations.

## Review relationship

The Producer invokes the canonical Art Direction review runner, whose `Workers=7` contract uses private worker-local Godot roots and canonical `WorkerRoot` values.

## Suite ownership

No operational path requires the retired `c11c-studio/`.
