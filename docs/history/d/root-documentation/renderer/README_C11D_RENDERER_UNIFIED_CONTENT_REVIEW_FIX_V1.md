# C11D_RENDERER_UNIFIED_CONTENT_REVIEW_FIX_V1

Minimal corrective overlay for the unified in-memory review coordinator. It modifies only the coordinator and its Python contract test; it does not alter any Godot harness or frozen C11-C file.

## Cause and correction

The joined review correctly observed a Challenge source timeline of 900 frames at 60 FPS and a proposed `REVIEW_720` delivery of 450 frames at 30 FPS, but rejected the relationship with a generic profile/timebase mismatch. The corrected coordinator validates the required profile fields individually, permits additional non-authoritative metadata on the delivery profile, and explicitly verifies duration preservation using the integer relation `source_frames * delivery_fps == delivery_frames * source_fps`. It still strictly requires the pinned facts: source `900@60`, delivery `450@30`, profile `REVIEW_720`, and `720x1280`. Wrong FPS, frame count, resolution, profile ID, phase boundary, or duration mismatch remains a failure.

## Apply

From PowerShell at the repo root:

```powershell
Get-FileHash "$env:USERPROFILE\Downloads\C11D_RENDERER_UNIFIED_CONTENT_REVIEW_FIX_V1.zip" -Algorithm SHA256
Expand-Archive -LiteralPath "$env:USERPROFILE\Downloads\C11D_RENDERER_UNIFIED_CONTENT_REVIEW_FIX_V1.zip" -DestinationPath "." -Force
```

Expected unchanged C11-C manifest SHA-256: `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.

## Test and rerun the unified review

```powershell
python -m py_compile .\tools\c11d\d9\d_renderer_unified_content_review.py .\tools\c11d\d9\test_d_renderer_unified_content_review.py
python .\tools\c11d\d9\test_d_renderer_unified_content_review.py
python .\tools\c11d\d9\run_d_renderer_unified_content_review.py --godot godot
```

Do not update documentation unless the joined runner produces `C11-D RENDERER UNIFIED CONTENT REVIEW PASS` and the process contains no Godot `ERROR:` or `SCRIPT ERROR:` lines. This is still an in-memory review only, not an approval or video-ready signal.

## Preserved locks

C11-C remains immutable; source fps remains 60; delivery fps remains 30; renderer OFF; no media; D4.8 BLOCKED; release authority NONE.
