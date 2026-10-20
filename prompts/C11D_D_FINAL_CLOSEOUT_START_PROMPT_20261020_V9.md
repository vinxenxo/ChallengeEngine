# C11-D Start Prompt — V2-B Safe Projection Design Continuation (2026-10-20, V9)

Continue from the authoritative Windows checkout `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`. The active checkout is truth; the analysis baseline ZIP is a reference and does not itself prove current-checkout identity.

## Confirmed gates

- V2-C source-frame/route runtime acceptance: operator-confirmed 9/9 selectors, 9/9 canonical planner calls, 18/18 independent Godot 4.7.1 Mono processes, 81/81 pins. Report SHA-256 `35e5985f47055fc11cbc0fcd7317f4d0a4ebe6bfe4d8bb22bdab67b7bcbe56a7`. This is not renderer payload acceptance or visual seed sensitivity.
- Source semantic review: operator-confirmed tests 34/34, 81/81 pins, approved bindings 0.
- Frozen C11-C manifest SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`. Never modify it.

## Current increment

Apply and test `C11D_CHALLENGE_VISUAL_PAYLOAD_V2B_SAFE_VISUAL_PROJECTION_DESIGN_OVERLAY_20261020_V1.zip`. Its design test suite is static/contract-only and must produce `C11D_V2B_DESIGN_CONTRACT_TESTS_PASS=90/90`. It does not run Godot and does not implement the runtime harness. Verify ZIP, manifest, all ten unique absent destinations, the 81 source pins, and nine authority-input pins before writing anything.

## V2-B design constraints

- Safe in-memory test projection includes only FrameSnapshot `position`, `rotation`, `scale`, `opacity`, `texture_index`, `variant_id`; source order and raw coordinates preserved; no transforms or resampling.
- Whole `custom_data` map serialization is prohibited. Six candidate rows remain unapproved; candidate probes may only hash one field stream at a time with raw values omitted.
- Keep request hash, plan hash, projection-instance identity, safe state hash, candidate-field hashes and payload identity distinct. No payload identity is created.
- Actual state projection hash—not request/plan hash—is the gameplay-seed sensitivity oracle.
- Variants: baseline repeat, gameplay seed changed, music seed changed, editorial-only fields changed. Later runtime design denominator is 45 planner calls and 45 Godot processes.
- `target_x` remains scalar and is expected seed-invariant; Hit target is per-run constant; Catch/Find targets are per-frame vectors; Choose/Count remain source-frame-only.
- CHALLENGE_008/009 timeline acceptance remains blocked; CHALLENGE_004 V1 harness unchanged.

Do not approve any semantic binding, materialize payload/media, drive rendering, modify challenge JSON, alter C11-C, enable renderer or authorize promotion. After the design overlay tests pass, proceed to separately versioned V2-B runtime harness implementation. No runtime PASS may be claimed before real Windows/Godot evidence.
