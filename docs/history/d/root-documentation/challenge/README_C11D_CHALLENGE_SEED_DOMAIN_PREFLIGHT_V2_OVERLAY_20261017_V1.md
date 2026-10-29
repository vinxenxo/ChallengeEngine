# C11-D Challenge Seed-Domain Planner Preflight V2 — Overlay V1

## Purpose

This additive overlay records the accepted Visual Loop seed-domain runtime gate from 17 October 2026 and adds a source-pinned, Python-only preflight of all nine canonical Challenge selections through the existing D9.9 universal planner.

It does **not** claim Challenge visual-payload seed sensitivity, does not invoke Godot, and does not make any request admissible to a renderer.

## Accepted predecessor evidence

- Visual Loop exact-selector payload V2 runtime: PASS; five grammars, deterministic payload instances 5/5, 70/70 direct source pins.
- Visual Loop seed-domain V2 runtime: PASS; 5/5 selectors, 27/27 seed-variant cases, 27/27 repeat-consistency checks, gameplay seed plan/projection sensitivity 5/5 and music seed orthogonality 5/5.
- Godot 4.7.1: `4.7.1.stable.mono.official.a13da4feb`.
- Runtime report SHA-256: `be5ef149aa30c99c76501acafe6e1161ecc05e9980630d2309d7146f57ca7683`.
- Runtime stdout SHA-256: `e87770484fbb1a535330484f5f45de80b34fcf7ffc15d1b6b22034f279d0a301`.
- Runtime stderr SHA-256 (empty): `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
- Saved report SHA-256: `e738749b9326b3fbb237091f742ed1d42cf0686c5d9d91484082748206b10ca7`.
- Operator evidence directory: `%TEMP%\C11D_VISUAL_LOOP_SEED_DOMAIN_V2_RUNTIME_20261017_122346`.

These are operator-supplied Windows runtime results, captured and retained as evidence in this checkpoint. They are not renderer approval.

## New preflight scope

`d_renderer_challenge_seed_domain_preflight_v2.py` plans all nine selectors using the canonical D9.9 planner and the existing base-request constructor. It exercises 9 Challenges × 3 explicit seed variants × 2 planner calls = 54 planning calls. It validates request and plan identity sensitivity, editorial identity invariance, canonical D4 GUI/CLI parity, source pins, unknown selector rejection and invalid seed rejection.

## Important uncovered architectural boundary

The accepted D9.9 binder V1 and `materialize_dynamic_request_payload_in_memory.gd` explicitly admit only `CHALLENGE_004 / parking_v2`. The harness also pins `CHALLENGE_004.json`, the `parking_v2` mechanic and its specific visual asset/timebase assumptions. This is a real scope limit, not a defect in the universal planner: the canonical D9.9 planner resolves all nine Challenge variants, but that does not imply that the downstream payload binder/materializer supports them.

The preflight is deliberately **planner-only**. Its report uses `challenge_visual_payload_seed_sensitivity=NOT_TESTED`, `godot_invocations=0`, and `payload_materialized=false`.

## Additional blocking finding

`CHALLENGE_008.json` and `CHALLENGE_009.json` each declare `video.total_duration=11.0`, while their component durations (`hook=3`, `game=7`, `reveal=0`, `CTA=2`) sum to 12 seconds. The preflight flags these two mismatches and does not choose a precedence rule. The existing shared temporal-alignment policy must resolve the conflict before either Challenge's presentation timeline/payload can be accepted.

## Authority boundary

- Frozen C11-C manifest remains unchanged: `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.
- `renderer=OFF`; `candidate_input_admissible=false`; `media_created=false`.
- `master_seed=NOT_ADOPTED`; automatic seed generation remains disabled.
- `D4.8=BLOCKED`; `D9.10=PREPARE_ONLY`; `D9.17=BLOCKED_NO_GO`; `D10=BLOCKED`; `release_authority=NONE`.

## Operator sequence

1. Apply the ZIP as add-only using its internal overlay manifest and sidecar SHA-256.
2. Run the 20-test suite `test_d_renderer_challenge_seed_domain_preflight_v2.py` in the active Windows checkout.
3. If the suite passes, run the planner preflight with `--full-report` and retain stdout/stderr/report hashes.
4. Use that evidence to specify the Challenge-specific V2 materialization extension. Do not mutate the already accepted V1 binder contract or claim visual seed sensitivity for Challenges until an actual Godot receipt proves it.
