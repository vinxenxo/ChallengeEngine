# C11-D Renderer Profile Identity Separation Overlay V1

## Purpose

Separate legacy video-profile metadata, explicit presentation profile, inline runtime timing and D delivery profile without modifying frozen C11-C. The new harness performs a D-owned presentation rebind on a deep copy while checking simulation invariance.

## ZIP SHA-256

Will be supplied after archive creation.

## Apply

Extract the ZIP into the existing `ChallengeEngineV01_STATELESS` repository root. Verify `release/C11C_FREEZE_PACKAGE_MANIFEST.json` is still SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.

## Run

```powershell
python -m py_compile .\tools\c11d\d9\d_renderer_profile_identity_separation.py .\tools\c11d\d9\test_d_renderer_profile_identity_separation.py
python .\tools\c11d\d9\test_d_renderer_profile_identity_separation.py
godot --headless --path . --script res://tools/c11d/d9/rebind_challenge_presentation_profile_in_memory.gd
```

If Godot passes, append documentation with `tools/c11d/d9/append_profile_identity_separation_doc_updates.ps1`. This harness is review-only; it writes no report or payload file, emits no renderer input and creates no media. It does not authorize D4.8, baseline freeze or release.
