# C11-D Next Increment Plan — 17 October 2026 (V3)

## Accepted gates

1. Visual Loop exact-selector payload V2: runtime PASS, five selector payload instances, 70/70 source pins, deterministic repeats, no renderer input.
2. Visual Loop seed-domain V2: runtime PASS on Godot 4.7.1; 5/5 selector seed sensitivity, 5/5 music orthogonality, 60 Godot invocations, 135/135 policy references only.
3. Challenge D9.9 planner: canonical inventory resolves all nine Challenge IDs to their declared mechanic family, demonstrated by this preflight matrix (execution result still requires operator runtime of the newly added Python-only preflight).

## Immediate sequence

**Phase C1 — planner preflight.** Apply and run `C11D_CHALLENGE_SEED_DOMAIN_PREFLIGHT_V2_OVERLAY_20261017_V1.zip`: execute 20 focused tests, then `d_renderer_challenge_seed_domain_preflight_v2.py --root . --full-report`. This must remain a Python-only planning gate with zero Godot/payload operations.

**Phase C2 — resolve Challenge payload scope before implementation.** Reconcile the fixed V1 `CHALLENGE_004` binder/harness with the nine mechanically heterogeneous Challenge definitions. Do not mutate V1 in place: its source is pinned by accepted audits, and its harness encodes assets/timebase for CHALLENGE_004. Draft an additive Challenge V2 materialization contract using the shared D9.9 planner and D9.10 bridge/adapter, exact per-Challenge source hashes, per-mechanic support matrix, deterministic repeats and fail-closed unsupported mechanics.

**Phase C3 — timebase/temporal policy dependency.** The preflight must flag CHALLENGE_008 and CHALLENGE_009: declared `total_duration=11s` conflicts with segment sum `12s`. Keep those selectors blocked for timeline/payload acceptance until the existing shared temporal-policy decision gives clear precedence. Do not silently rewrite challenge JSON.

**Phase C4 — Challenge runtime seed matrix.** Only after a generic supported source-frame receipt exists per challenge, test baseline/gameplay-only/music-only seed variants and two repeats per selector. Distinguish request/plan hash changes from visual-state/payload hash changes. Require gameplay seed to change visual projection and music seed to preserve it; preserve request identity change for both seeds.

**Phase C5 — close candidate I/O and shared policy gaps.** Reconcile current 0/10 complete, 6 partial and 4 blocked groups from fresh live evidence. Keep editorial field windows, coordinate projection, challenge sample composition/temporal alignment, delivery timebase, audio/music and shared presentation as explicit proposals until approved.

**Phase C6 — admission and release gates.** Only after all source, payload, I/O and policy requirements close can the team reconsider renderer admission, D4.8, D9.14/D9.16/D9.17, D10, baseline freeze and cutover. C11-C stays authoritative until a separate explicit approval/cutover.

## Non-negotiable boundary

`renderer=OFF`; `media_created=false`; `candidate_input_admissible=false`; `seed_domains_complete_for_candidate_input=false`; `automatic_seed_generation=false`; `master_seed=NOT_ADOPTED`; `D4.8=BLOCKED`; `D9.10=PREPARE_ONLY`; `D9.17=BLOCKED_NO_GO`; `D10=BLOCKED`; `release_authority=NONE`.
