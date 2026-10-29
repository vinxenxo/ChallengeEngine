# C11D_RENDERER_UNIFIED_CONTENT_REVIEW_FIX_V2

Minimal follow-up correction for the unified in-memory review coordinator. It replaces only:
- `tools/c11d/d9/d_renderer_unified_content_review.py`
- `tools/c11d/d9/test_d_renderer_unified_content_review.py`

It does not modify the five Godot harnesses, frozen C11-C source, or renderer activation controls.

## Exact failure and cause

The actual `review_challenge_delivery_timeline_in_memory.gd` summary emits `delivery_profile` with `profile_id`, `fps`, `width`, and `height`; it does not emit a `delivery_profile.total_frames` property. The authoritative delivery frame ranges are supplied separately in `delivery_segments`:
- HOOK: 90
- GAME: 210
- REVEAL: 90
- CTA: 60

The previous coordinator incorrectly required `delivery_profile.total_frames == 450`, yielding `actual=None` and rejecting a valid 900@60 FPS to 450@30 FPS proposal.

## Correction

The coordinator now derives the delivery frame total from the four declared phase segment counts and verifies it equals 450, verifies the required delivery profile identity/FPS/dimensions, and checks duration preservation via the exact integer relation:

`source_total_frames * delivery_fps == derived_delivery_total_frames * source_fps`

The optional `delivery_profile.total_frames`, if a later producer adds it, is only a consistency check against the segment-derived total. The test fixture now mirrors the real Godot summary shape and adds regression tests for the absent property, incorrect segment total, and conflicting optional total.

## Apply and test

```powershell
cd C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS
Get-FileHash "$env:USERPROFILE\Downloads\C11D_RENDERER_UNIFIED_CONTENT_REVIEW_FIX_V2.zip" -Algorithm SHA256
Expand-Archive -LiteralPath "$env:USERPROFILE\Downloads\C11D_RENDERER_UNIFIED_CONTENT_REVIEW_FIX_V2.zip" -DestinationPath "." -Force
python -m py_compile .\tools\c11d\d9\d_renderer_unified_content_review.py .\tools\c11d\d9\test_d_renderer_unified_content_review.py .\tools\c11d\d9\run_d_renderer_unified_content_review.py
python .\tools\c11d\d9\test_d_renderer_unified_content_review.py
python .\tools\c11d\d9\run_d_renderer_unified_content_review.py --godot godot
```

Expected contractual result includes `negative=8/8` and (in the full checkout) `source_files=11/11`. The unified Godot command must complete all five child harnesses, produce `C11-D RENDERER UNIFIED CONTENT REVIEW PASS`, and emit no `ERROR:` or `SCRIPT ERROR:` child lines.

Only after that joined PASS should you run:

```powershell
.\tools\c11d\d9\append_unified_content_review_doc_updates.ps1
```

Then repeat `test_cross_suite_lifecycle.py`, `test_d_baseline_candidate.py`, and `python -u .\c11c-suite\self_test.py`.

## Preserved governance

The delivery total is derived from proposed segments only; this does not approve the timebase policy or produce a video. Renderer remains OFF, media creation false, D4.8 BLOCKED, and release authority NONE. The report remains console-only/in-memory and C11-C remains immutable.
