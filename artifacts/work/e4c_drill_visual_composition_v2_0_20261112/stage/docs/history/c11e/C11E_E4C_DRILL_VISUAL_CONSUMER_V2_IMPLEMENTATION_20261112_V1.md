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
