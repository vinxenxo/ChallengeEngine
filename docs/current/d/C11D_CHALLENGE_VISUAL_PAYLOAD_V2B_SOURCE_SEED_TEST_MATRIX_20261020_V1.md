# C11-D V2-B — Source-State Seed Test Matrix V1

**Status:** DESIGN ONLY; zero runtime invocations in this increment.

The matrix contract is `definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_SEED_TEST_MATRIX_V1.json`.

Per selector: five canonical planner invocations and five independent Godot processes (`BASELINE_R1`, `BASELINE_R2`, gameplay-seed mutation, music-seed mutation, editorial-only mutation). Nine selectors produce a denominator of 45 planner invocations and 45 Godot processes. All rows must remain visible on failures; no selector may be omitted to make the denominator appear green.

Critical oracle separation:

- Request/plan identity: canonical inputs and plan lineage only.
- Safe source-state projection hash: actual gameplay-source output over the allowlisted six base `FrameSnapshot` fields.
- Candidate field hash: an independent field-level digest, with no raw values, for one explicitly reviewed candidate field at a time.
- Payload identity: not created.

V2-B acceptance requires gameplay-seed mutation to change the safe source-state projection hash for all nine seed-consuming primary source-state tracks; a changed request/plan hash is insufficient. Music-seed mutation must preserve safe state and candidate field hashes. Editorial-only mutation must preserve simulation input and state hashes. Repeats must agree across independent processes.

CHALLENGE_003 `target_x` is expected invariant under gameplay seed mutation; it is a scalar configured track and not the seed oracle. CHALLENGE_005 `target_position` is a per-run constant repeated over frames. CHALLENGE_006/007 `target_position` are per-frame tracks. CHALLENGE_008 `active_selection` and CHALLENGE_009 `displayed_count` remain source-frame-only, with phase/timeline acceptance blocked.
