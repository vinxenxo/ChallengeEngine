# C11-D Seed-Domain / Challenge Materialization Next Increment Plan — 2026-10-17 V4

## Closed / accepted scoped gates

1. Visual Loop exact-selector payload V2 runtime: PASS, five selector payloads, direct lineage 70/70, no renderer input.
2. Visual Loop seed-domain V2 runtime: PASS, five selectors, 15 seed variants and repeats, gameplay visual sensitivity 5/5, music orthogonality 5/5, 60 Godot invocations.
3. Challenge planner preflight V2: PASS, nine selectors, 27 seed variants, 54 planner calls, stable repeats 27/27, D4 parity 27/27, request/plan identity seed sensitivity 9/9, editorial identity invariance 9/9, five negatives. Zero Godot and zero payload work.

## Immediate sequence

**C2-A — Design frozen / source-aware contract.** Use `C11D_CHALLENGE_VISUAL_PAYLOAD_MATERIALIZER_V2_DESIGN_PROPOSAL_20261017.md`. The currently accepted Challenge V1 binder stays fixed to `CHALLENGE_004`. Do not alter its selector matrix to get broader counts.

**C2-B — Build the V2 static contract and source matrix (Python-only).** Nine exact selectors, definition/source/asset pins, mechanic branch classification, path confinement, timeline arithmetic, seed-domain identity, governance false/blocked values, schema validation, mutation and negative tests. Reuse D9.9 canonical planning and D4 parity. Do not invoke Godot in this stage.

**C2-C — Runtime source-frame receipt pilot.** From a verified active checkout, use the actual Godot 4.7.1 Mono runtime; one selector at a time and two independent runtime repetitions. First determine per-mechanic snapshot shape, supported runtime path, required source dependencies, asset roles and source FPS. No rendering nodes or disk payloads. Stop at the first real blocker and preserve evidence.

**C2-D — Full seed matrix.** For supported source routes, test baseline `(12345, 840001)`, gameplay-only `(54321, 840001)`, music-only `(12345, 840002)` with two independent processes per case (54 planned runtime invocations for nine selectors). Assert gameplay visual sensitivity only where the frozen mechanic accepts that seed; assert music orthogonality against a visual projection, not the whole request-bound envelope. Never silently drop a failed selector from the denominator.

**C2-E — Source-timebase payload assembly.** Build in-memory semantic payloads only for eligible timebase-coherent selectors. `CHALLENGE_008/009` remain blocked for timeline-bound payload acceptance until the shared temporal-policy owner settles the 11s/12s conflict. Source-frame/seed checks, where isolated correctly, must not be labelled timebase acceptance.

**C2-F — Regression / gap refresh.** Re-run V1 Challenge preview and binder tests, Loop and Drill V2 seed tests, D4 parity, and relevant unified suites. Refresh candidate I/O and all policy gap evidence from active source pins. Only then reconsider renderer admission in canonical order.

## Design constraints

Do not duplicate D9.9 selector/planner logic; do not clone or weaken the 1,378-line V1 binder contract; use the bridge/D-only adapter where supported; report all per-selector status/lineage; do not assume three assets, 420 frames, 900 total frames or a common mechanic path. Preserve source FPS and only the allowlisted `SimulationResult.frames` snapshot fields. No `winning_frame` sampling or `close_calls` timing inference. No renderer-native input, media, file payloads, release authority or promotion.

## Frozen locks

`renderer=OFF`; `candidate_input_admissible=false`; `seed_domains_complete_for_candidate_input=false`; `media_created=false`; `automatic_seed_generation=false`; `master_seed=NOT_ADOPTED`; `D4.8=BLOCKED`; `D9.10=PREPARE_ONLY`; `D9.17=BLOCKED_NO_GO`; `D10=BLOCKED_FOR_PROMOTION`; `release_authority=NONE`. C11-C manifest remains `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953.
