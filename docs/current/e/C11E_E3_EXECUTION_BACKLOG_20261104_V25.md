# C11-E execution backlog — V25

**Date:** 2026-11-04

## Immediate: repair and complete E4A.3D.1

1. Apply `C11E_E4A3D1_GODOT_4_7_COMPAT_FIX_V1` using the packaged Windows PowerShell 5.1 runner. It changes only the D-owned adapter and its regression test, checks exact preimages + 16 protected source pins + frozen manifest, runs 81 focused tests and py_compile, and creates eight add-only V48/V25 documents. No C11-C source, renderer, dispatch, FFmpeg or media is touched.
2. Rerun only the existing isolated compositor on the already accepted E4A.2 real-body base:
   `python tools/c11d/d9/c11e_e4a_d_compositor_real_body_pixel_review.py --base-run "artifacts/tests/c11e/e4a_real_body_pixel_review/RUN_20261104_002559_542bcf60"`
3. Require Godot 4.7.1 exit 0; 6/6 source-frame extraction; 18/18 compositor PNGs; 12/12 pixel comparisons; BODY identity; overlap false; exact native hook first line at both HOOK endpoints; measured fit ≤3 lines/468 px/120 px; CTA single-owner. Inspect the real PNGs and report.
4. Keep visual placement unapproved until operator review and Challenge-specific D1.5/layout authority are reconciled. A parse pass is necessary but not sufficient.

## Next work after E4A closes

- Only after Challenge technical and visual acceptance, connect its D-composited result to the accepted E3 D3 V5 audio/mux/QC path under its separate gates.
- Continue E4B Loop and E4C Drill using their own binders, timelines and C11-C family music; do not reuse Challenge D3 or `show_hook_countdown`.
- E5 GUI/CLI parity and independent seed domains; E6 Smoke18; E7 Matrix101 (54 Challenges + 27 Loop + 20 Drill). Hold CH_008/009 while declared 11s conflicts with 12s phase sum; do not claim complete coverage until resolved.
- E8 independent acceptance, freeze and explicit promotion before C11-E replaces C11-C.

## Constraints

Challenge title, subtitle and CTA remain individually optional; empty fields omitted; language metadata-only. `player_name` and `challenge_label` remain blocked. Production `renderer=OFF`, dispatch/media false, and `release_authority=NONE`.
