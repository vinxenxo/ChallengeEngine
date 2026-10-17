# C11-D Challenge Visual Payload Semantic Binding Proposal V1 — Checkpoint (2026-10-17)

## Closed evidence immediately preceding this proposal

The operator confirmed the Challenge visual-payload capability matrix on the active Windows checkout:

- `UNIT TESTS: PASS | 15/15`.
- Summary: selectors 9/9; source pins 43/43; mechanic registry routes 9/9; asset-role references 27/27; unique assets 15/15; custom_data inventory 9/9.
- Explicit total timebase conflicts: 2; existing V1 runtime preview coverage: 1/9.
- Godot invocations 0; payload materialized false; candidate input inadmissible; renderer OFF; media_created false; D4.8 BLOCKED; release authority NONE.
- C11-C manifest SHA-256 unchanged: `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.
- Evidence folder: `C:\Users\vinxe\AppData\Local\Temp\C11DVP1E_20261017_135011`.
- `tests.out`: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
- `tests.err`: `6c462e43d7f48a450a30ce5b0eddbaa9d24beaa00ec4e71552583f44c6f34807`.
- `audit.out`: `fac01dcd530ac11f29561ae9dc6e4d595ef907699c246a5ba5de3b81632fc113`.
- `audit.err`: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
- `report.json`: `36c014734892fee2d7a1beb2662cd610c6856b4ecb48d9e06bf596f826795327`.

The earlier Challenge Seed-Domain Planner Preflight V2 was also operator-confirmed PASS: 9/9 selectors, 27/27 seed-variant cases, 27/27 repeats, 27/27 D4 parity; 54 planner calls and zero Godot/payload materialization. Its saved report SHA-256 was `1e41001f83cf9b093919f46ee2f327553c93464f8369ecfb0dc3b34b0a0c9d43`.

## Current increment

This overlay is a **static semantic-binding proposal**, not the generalized runtime materializer. It derives a source-specific proposal for the primary `FrameSnapshot` track and candidate secondary fields while keeping all binding approval flags false.

- Three source-declared static target bindings: Challenge 001, 002, 004.
- Six `custom_data` field proposals: `target_x` (003), `target_position` (005/006/007), `active_selection` (008), and `displayed_count` (009).
- Candidate telemetry such as distances, speed, steering/braking, score, `winning_frame`, `close_calls`, and `target_count` remains excluded by default.
- `PILOT_0X100` stays scalar and must not be fabricated into a 2D coordinate or projected onto 1080x1920.
- `CHALLENGE_008/009` remain blocked pending a timebase decision: declared total 11s, phase sum 12s.
- Challenge 004 V1 stays unchanged and acts as a regression fixture.

## How to validate this proposal

1. Apply the add-only overlay.
2. Run `test_d_renderer_challenge_visual_payload_semantic_binding_proposal_v1` (20 tests expected).
3. Run `d_renderer_challenge_visual_payload_semantic_binding_proposal_v1.py --root . --full-report` and capture the JSON/evidence hashes.
4. If static checks pass, review these candidate bindings before creating the subsequent runtime harness. Do not mark this proposal as runtime acceptance.

## Governance locks

`renderer=OFF`; `media_created=false`; `candidate_input_admissible=false`; `seed_domains_complete_for_candidate_input=false`; `D4.8=BLOCKED`; `D9.10=PREPARE_ONLY`; `D9.17=BLOCKED_NO_GO`; `D10=BLOCKED_FOR_PROMOTION`; `release_authority=NONE`. Frozen C11-C manifest remains `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.
