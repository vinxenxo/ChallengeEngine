# E4C Drill consumer V2 implementation and verification — V1 (2026-11-12)

## Changed files

- Replace `tools/c11d/d9/c11e_e4c_drill_visual_composition_consumer.py`.
- Replace `tests/test_c11e_e4c_drill_visual_composition_consumer.py`.
- Add exact-hash V2 composition proposal/schema and user-direction record.
- Add existing-media requalification Python tool and PowerShell runner.
- Add versioned current documentation and continuity prompts.

No GUI, CLI facade, E1 service, shared AV executor, C11-C launcher, binder, music generator or C11-C source is changed.

## Consumer behavior

The consumer validates the V2 proposal, schema, decision, unmodified V1 timebase and `PresentationProfile.gd` hash. It creates a V2 plan bound to exact hashes and the E1 source intent. PRE_ROLL/END_CTA return a copy of the entire source QImage. GAME crops only the full-width social body and draws that crop at the same position on the D canvas; no scaling or interpolation is used. D editorial remains restricted to GAME. END_CTA native ownership is preserved.

## Focused tests (18)

Tests pin proposal/schema/decision/timebase/profile; verify full-width geometry; reject the V1 centered 504×896 viewport; compare full-frame passthrough for PRE_ROLL and END_CTA; prove pixel-exact same-position GAME body; ensure native family header/footer are absent from GAME bands; verify D editorial only in GAME; test no-editorial passthrough; prove source non-mutation; assert 90/630/90 mapping; validate plan integrity/governance; verify pinned Spanish font coverage; reject unsupported glyphs and suppress UNKNOWN sentinels.

The tests deliberately do not rerun Binder, native source capture, 100/100 V1 pixel tests, E1 parity, or music generation. Windows installer must run all 18 tests under the existing Python 3.13 + PySide6 runtime before its transaction.

## Existing-media requalification

Use the accepted CLI smoke receipt and original `native_source` MP4 plus FAMILY_MUSIC_V4 A/B/C WAVs. The requalifier verifies source hashes and original 91-pin equality, then decodes and processes all 810 frames. It requires 630 GAME body pixel comparisons and 180 PRE_ROLL/END_CTA full-frame comparisons. It encodes one corrected silent V2 stream, reuses the WAV files for A/B/C mux, and checks H.264 A/B/C equality, AAC A/B equality/C difference, FFprobe, timebase, stream start and unchanged pins. Seven frames are extracted for human review.

The output receipt is technical-only and remains pending operator visual/listening acceptance. No Godot, C11-C launcher, music generator or CLI facade is run during requalification.

## V2.1 authoritative reconciliation (2026-11-12)

`E4C_OPEN_V2_REQUALIFICATION_PENDING`. Geometry V2 and the Test 04 boundary correction are accepted: `validate_plan()` now requires `source_frame_viewport == EXPECTED_SOCIAL_REGIONS["body_rect"]`. Reconciled consumer SHA-256: `e5cf97651e546ad86e2a4d46698553038e4161dc97a55da2654f197ed71f623c` (36,678 bytes); unchanged test SHA-256: `62327e32ed4c15b497efb4a93fecc1d484cebff0b79beaa7ced5099905ffb2bf`; isolated Python 3.13.14 evidence is py_compile PASS and 20/20 PASS.

V1.7 destination preflight, V1.8 operation/package binding, V1.9 geometry contract and V2.0 staging Test 04 failures are closed before transaction; none installed this correction. V2.1 is rebuilt and pending Windows installation, complete receipt and postimage review. Do not install V2.0 and do not repeat GUI, CLI smoke, native capture, music or Binder.

Preserve evidence GUI `D99-GUI-6514F1066E79`, CLI `E4C-CLI-SMOKE-20261112T091253Z-5a2e96b8`, native silent MP4, WAV A/B/C, seeds and bitstreams. V1 composition was visually rejected; `tracking/tier-1` is not yet an accepted V2 matrix row.

Required sequence: documentation; V2.1 installation; receipt/postimage audit; one existing-media requalification; seven-image/three-MP4 review; operator visual/audio acceptance; row 1/20; remaining 19; E4C close; E5, E6 Smoke18, E7 Matrix101, E8. C11-C 2.19.12 only; frozen manifest `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`; E1 `PREPARE_ONLY / NOT_CONNECTED_E1`; no Git, pip, C11-C mutation, dispatch or release; operator-managed commits.
