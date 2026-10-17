# C11-D D9/D10 Overhand Master Prompt V3 — 2026-10-17

## Role and objective

Continue engineering C11-D toward formal baseline qualification and eventual replacement of frozen C11-C, with determinism and evidence discipline at the same standard as the C11-C release. This is a long-running gated project; continue from the live working checkout, not the stale snapshot content or historic D7/D8 state.

## Active repository and immutable reference

`C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`

The frozen C11-C manifest must match SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`. Never modify C11-C 2.19.12, its manifest, simulation truth, RNG, `SimulationResult`, `winning_frame` semantics or `close_calls` semantics. C11-C remains authoritative until all C11-D gates close and formal approval/freeze/promotion/cutover is explicitly recorded.

## Current state/evidence

- Active Windows Godot `4.7.1.stable.mono.official.a13da4feb` exact-selector Visual Loop V2 runtime PASS: 70/70 source pins, 5/5 plans/parameter instances/exact payloads/deterministic repeats, 45/45 policy references, no renderer inputs, no payload files and zero approvals. Evidence hashes are in `C11D_VISUAL_LOOP_EXACT_SELECTOR_PAYLOAD_V2_RUNTIME_ACCEPTANCE_CHECKPOINT_20261017.md`.
- The new Visual Loop explicit seed-domain V2 audit overlay has 17/17 staging unit/contract tests PASS and canonical request-chain planning 15/15 in the isolated snapshot. This is **not** runtime acceptance. Apply it first, run the tests on the live checkout, then execute the full runner under actual Godot 4.7.1.
- The new seed matrix is limited to five geometric grammars and three explicit variants, two independent repeats each: 30 receipts, each with parameter-binding and exact-payload probes (60 invocations) plus one version probe. It must validate gameplay sensitivity and preserve the gameplay-derived visual projection under music-only mutation.

## Mandatory current references

`AGENTS.md`; `docs/current/d/MASTER_HANDOVER_C11D_CURRENT.md`; `docs/current/d/C11D_FULL_CONTEXT_CONTINUITY_CHECKPOINT_20261017_V3.md`; `docs/current/d/C11D_RENDERER_CLOSEOUT_GATE_MAP_20261017_V3.md`; `docs/current/d/C11D_SEED_DOMAIN_NEXT_INCREMENT_PLAN_20261017_V2.md`; `docs/current/d/C11D_VISUAL_LOOP_SEED_DOMAIN_AUDIT_V2_CHECKPOINT_20261017.md`; `docs/current/d/C11D_WORKSTREAM_NON_DUPLICATION_REGISTER_20261017_V3.md`; `docs/current/d/C11D_POWERSHELL_EXECUTION_POLICY_20261016.md`.

## Work discipline

1. Before coding, hash-check active sources and read the current contract/lineage.
2. Additive overlays only by default; no parallel binder/contract/policy owner. Replacements require source-hash preconditions, backup and rollback. Separate apply from tests and live runtime.
3. After overlay apply: run focused 17-test unit suite; then run actual Godot seed-domain runner, capture stdout, stderr, actual exit code, report hash and evidence path; verify exactly 30 receipts and 60 probes plus semantic seed conditions and locks.
4. If the runtime gate passes, update only the seed-domain checkpoint with real operator evidence. Next create a separately pinned Challenge seed-domain audit beyond `CHALLENGE_004`; do not assume that one selector represents all nine Challenges.
5. After seed populations, revisit Candidate I/O (last state 0/10 complete, 6 partial, 4 blocked) and close existing editorial, layout, coordinate, temporal/sampling, delivery/timebase and audio/music policy owners before candidate input admission.
6. D9.14/D9.16/D9.17/D10 and baseline freeze/cutover must be performed in canonical order with explicit approval, not inferred from this preparation audit.

## Permanent safety and architecture constraints

Renderer OFF. No renderer-native input or dispatch; no shader/material creation or execution; no media; no baseline approval/freeze/promotion/cutover. `D4.8=BLOCKED`; `release_authority=NONE`; `D9.10=PREPARE_ONLY`; `D9.17=BLOCKED_NO_GO`; D10 blocked. `candidate_input_admissible=false`. `master_seed=NOT_ADOPTED`; automatic/default seed generation disabled; seed-domain completeness false until explicitly justified by actual population coverage and policy.

Preserve existing five C11-C suite surfaces (`c11c-test`, `c11c-producer`, `c11c-catalog`, `c11c-config`, `c11c-maintenance`); no `c11d-control`. Shared editorial/presentation rules remain common by default. Use `winning_frame` as sole temporal anchor and `close_calls` as episode count only. No claims of media output from preparation-only tests.
