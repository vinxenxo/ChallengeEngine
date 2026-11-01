# C11-E continuation master prompt â€” V20

## Mission

Complete the full C11-E production system: Challenge, Visual Loop and Visual Drill. Preserve the established C11-C generators/mechanics. Add D presentation and enabled editorial, integrate D3 Music V5 with independent `request.music_seed`, FFmpeg mux and FFprobe A/V verification. GUI and CLI must use the same shared production service.

## Current evidence state (2026-11-01)

- E0 restart: accepted.
- E1 shared service: automated tests 2/2 PASS; GUI observation pending.
- E2 V9 reconciled installation: APPLIED, 16 operations (12 applied + 4 already present); receipt SHA `d039360862d034b8f05f67cf8d0ddf914a1ed27075200f6a6c04462b92367972`.
- E2 native Godot JSON numeric contract: PASS 30/30; gameplay/music parse as float; full sidecar validation PASS.
- E2 Python pair contract: PASS 9/9 after test 09 source-layout assertion was corrected; repair receipt SHA `6cbe3fe05d1b6f7cc7fe3971171d398a3b2197477668fce5b7b7a93b74dfd855`.
- Runner source pin corrected to the active Python test SHA. Runner SHA `c5d6bc26c70151238f60466fa401e1fd14ef9b0a25b34aa45d98ebce2ba5c763`.
- R1 and R2 physical attempts failed before renderer invocation because they were run before the test 09 repair. Their evidence records zero renders and no media. Request IDs are permanently consumed.

## Immediate action

Verify the V20 runner-pin fix receipt and current pins, commit local changes, then run the existing E2 V9 runner with fresh request ID `C11E-E2-CH001-AB-20261101-V9-R3`, gameplay seed 193847 and music seed 840001. Explicit paths: Godot 4.7.1 Mono, Python 3.13 and FFmpeg/FFprobe 9.0. The runner must repeat the Godot JSON 30/30 and Python 9/9 tests before preparing A/B. E2 scope remains exactly two isolated CHALLENGE_001 renders, no audio, no release/promotion.

If R3 fails, preserve the complete failure ZIP and diagnose its first failing gate. If R3 automated acceptance passes, inspect both source AVIs and final MP4s, verify 540Ã—960@60/540 source frames and 720Ã—1280@30/270 delivery frames, zero audio streams, nonuniform source content, gameplay-body identity, title-slot difference, outside-slot header identity, final MP4 A/B differences, source/output hashes and receipt. Human visual review and an independent E2 decision are still required before E3.

## Roadmap after E2

- E3 D3 Music V5: audio/music seed isolation, deterministic audio, FFmpeg mux, FFprobe A/V validation.
- E4A Challenge presentation/editorial adapter.
- E4B Visual Loop binder/adapter.
- E4C Visual Drill binder/adapter.
- E5 determinism, seed isolation and GUI/CLI parity.
- E6 Smoke18 (six per family).
- E7 Matrix101 planned 54 Challenge +27 Loop +20 Drill; CH_008/009 remain held due 11-second declared duration vs 12-second phase sum, so runnable count is 99 until formally resolved.
- E8 independent acceptance, freeze and explicit promotion.

## Non-negotiable governance

C11-C 2.19.12 and frozen manifest remain production authority until E8 is independently accepted and promotion explicitly authorized. Do not mutate protected C generators/mechanics or release pins. No E2 audio, no implicit release authority. Use unique request IDs. Stop on first nonzero exit; never print manual PASS after a failure; never trust stale PowerShell variables or success receipts from older runs.