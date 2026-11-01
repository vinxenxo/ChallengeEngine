# C11D â†’ C11E full-family roadmap â€” V10

## Product objective

Deliver three production families: Challenge, Visual Loop and Visual Drill. Preserve C11-C generators/mechanics; add the C/D-specified presentation layer, enabled editorial and D3 Music V5. The same shared production service serves GUI and CLI. The complete flow must support deterministic gameplay with its own seed, independent `request.music_seed`, audio generation, FFmpeg mux and FFprobe A/V verification.

## Gate sequence

1. E0/E1 restart and shared service: accepted automated gates retained; E1 GUI observation pending.
2. E2 CHALLENGE_001 A/B: native Godot numeric 30/30 and Python contract 9/9 now pass; runner source pin now aligned with corrected test. R1/R2 failed before render. R3 must produce exactly two isolated no-audio renders and complete A/B invariance/difference checks, then human/independent review.
3. E3 D3 Music V5: independent music seed, deterministic audio, FFmpeg mux, FFprobe A/V streams/metadata/duration/sync. Enter only after formal E2 acceptance.
4. E4A Challenge presentation/editorial adapter.
5. E4B Visual Loop presentation/editorial binder and adapter.
6. E4C Visual Drill presentation/editorial binder and adapter.
7. E5 determinism, independent seed-domain validation and GUI/CLI parity across all families.
8. E6 Smoke18: six tests per family (18 total).
9. E7 Matrix101: planned population 54 Challenge + 27 Loop + 20 Drill.
10. E8 independent acceptance, freeze and explicit promotion.

## Matrix qualification

CH_008 and CH_009 are held: each declares 11 seconds while phase durations sum to 12 seconds (3+7+0+2). The presently runnable matrix is 99, not 101. Do not silently alter the source or report 101 complete without a separately authorized resolution.

## Governance

C11-C 2.19.12 and its frozen manifest remain production authority until E8. No protected C generator/mechanic or release pin changes. E2 has no audio and grants no release/promotion authority. Preserve unique request IDs, evidence ZIPs, exact hashes, independent decision artifacts and separate human review.