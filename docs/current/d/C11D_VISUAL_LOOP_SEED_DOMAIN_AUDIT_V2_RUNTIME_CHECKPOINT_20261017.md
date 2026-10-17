# C11-D Visual Loop Seed-Domain Audit V2 — Runtime Acceptance Checkpoint

**State: PASS / RUNTIME PREPARATION-ONLY.** This checkpoint records the Windows runtime output supplied by the operator on 17 October 2026.

## Exact runtime evidence

- Godot: `4.7.1.stable.mono.official.a13da4feb`
- Audit command: `d_renderer_visual_loop_seed_domain_audit_v2.py --root <repo> --godot <Godot 4.7.1 console executable> --timeout 120`
- Source guards: 6/6.
- Selectors: 5/5 (`harmonic_membrane`, `interference_plane`, `parametric_ribbon`, `lattice_wave`, `orbital_wave`).
- Seed variant chains: 15/15; independent repeat pairs: 15/15.
- Request, plan, parameter-instance and full-payload hash variants: 15/15 each.
- Gameplay-seed visual projection sensitivity: 5/5.
- Music-seed visual orthogonality: 5/5.
- Policy reference pairs: 135/135; policy values consumed: false.
- Godot invocations: 60 (30 parameter-instance materializations + 30 exact payload materializations).
- Automatic seed generation: false; `master_seed` adopted: false.
- `seed_domains_complete_for_candidate_input=false`; `candidate_input_admissible=false`.

## Evidence hashes

- Audit report digest printed by the runner: `be5ef149aa30c99c76501acafe6e1161ecc05e9980630d2309d7146f57ca7683`
- stdout: `e87770484fbb1a535330484f5f45de80b34fcf7ffc15d1b6b22034f279d0a301`
- stderr: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (empty)
- saved JSON file: `e738749b9326b3fbb237091f742ed1d42cf0686c5d9d91484082748206b10ca7`
- operator evidence directory: `%TEMP%\C11D_VISUAL_LOOP_SEED_DOMAIN_V2_RUNTIME_20261017_122346`

The stdout JSON report file hash and the runner's internal report digest describe different byte sequences and are intentionally recorded separately. Do not substitute one for the other.

## Decision

The explicit seed experiment is accepted for the five geometric Visual Loop selectors. It does not establish default/automatic seed behavior, arbitrary cross-domain combinations, Challenge visual payload behavior, candidate I/O completeness, policy approval or renderer admission.

**Locks remain:** renderer OFF; media false; D4.8 BLOCKED; D9.10 PREPARE_ONLY; D9.17 BLOCKED_NO_GO; D10 BLOCKED; release authority NONE.
