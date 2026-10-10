# C11-D Renderer Challenge Visual Payload Preview V1

This minimal overlay adds a D-owned, in-memory logical visual payload preview for the real `CHALLENGE_004` runtime result. It is the next step after the unified content review showed `CHALLENGE_VISUAL_PAYLOAD_NOT_MATERIALIZED`.

## What it proves

- Invokes the existing frozen `ChallengeRuntimeBridge.run_effective_pipeline()` twice.
- Rebinds `social_default_v1` through `ChallengePresentationBinder` on a deep copy; it does not modify the source runtime's canonical dictionary.
- Verifies the frozen C11-C manifest and 10 pinned source/asset files.
- Loads `garage_background.svg`, `car.svg` and `parking_target.svg` as `Texture2D` resources and records canonical role, resource path, byte hash and intrinsic dimensions.
- Materializes all 420 GAME `FrameSnapshot` transforms at the native 60 FPS timebase. The payload includes only position, rotation, scale, opacity, texture index and variant ID; it excludes `custom_data`, metrics, `winning_frame` and `close_calls`.
- Hashes the complete logical payload and proves deterministic repetition and simulation invariance.

## What it does not do

No scene node creation, frame drawing, renderer-native input, renderer dispatch, payload-file writing, video/image/audio output, delivery resampling or coordinate projection. The Challenge declares `CANVAS_1080X1920`, while its `social_default_v1` profile exposes a 540×960 source canvas and 1080×1920 master output; choosing a coordinate mapping remains a separate reviewed decision. The 420 source samples remain at 60 FPS; no 30 FPS sample selection/interpolation is attempted.

## Apply and verify on Windows 11

From the existing repo root, verify the ZIP SHA-256 printed in the assistant response, then extract the overlay with `Expand-Archive -DestinationPath "." -Force`.

```powershell
python -m py_compile `
  .\tools\c11d\d9\d_renderer_challenge_visual_payload_preview.py `
  .\tools\c11d\d9\test_d_renderer_challenge_visual_payload_preview.py

godot --headless --path . --script res://tools/c11d/d9/materialize_challenge_visual_payload_in_memory.gd
python .\tools\c11d\d9\test_d_renderer_challenge_visual_payload_preview.py
```

The Godot harness must print `C11-D RENDERER CHALLENGE VISUAL PAYLOAD PREVIEW PASS` without any `ERROR:` or `SCRIPT ERROR:` output. If Godot fails, stop before the documentary updater or claiming runtime acceptance.

After a clean Godot PASS, add checkpoint references to current D docs with:

```powershell
.\tools\c11d\d9\append_challenge_visual_payload_preview_doc_updates.ps1
```

Then run `python .\tools\c11d\d9\test_cross_suite_lifecycle.py`, `python .\tools\c11d\baseline_candidate\test_d_baseline_candidate.py` and `python -u .\c11c-suite\self_test.py`. The currently installed unified review runner does not yet include this new Challenge payload harness; the follow-on increment will integrate it and update the aggregate gate summary. Do not treat the older unified review report as consuming this new proof.

## Immutable gates

C11-C frozen manifest SHA-256: `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`. `PREPARE_ONLY` remains in force. Renderer is OFF, no media is created, D4.8 is BLOCKED and release authority is NONE. This overlay cannot approve or freeze the D renderer baseline.
