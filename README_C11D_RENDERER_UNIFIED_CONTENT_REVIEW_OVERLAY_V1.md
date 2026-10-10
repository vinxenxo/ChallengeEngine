# C11D_RENDERER_UNIFIED_CONTENT_REVIEW_OVERLAY_V1

Minimal overlay for `ChallengeEngineV01_STATELESS`; it adds a unified in-memory review coordinator and does not replace the repository.

## Why this increment

The individually passing review stages now cover the actual Visual Loop and Visual Drill authoring payloads, the frozen `CHALLENGE_004` runtime result, presentation profile identity separation, the proposed `REVIEW_720@30FPS` delivery timeline and the proposed Challenge editorial field windows. This overlay joins their console summaries and verifies cross-artifact consistency in one pass.

## Key behavior

- Runs the five existing Godot 4.7.1 headless harnesses sequentially, without modifying them.
- Requires exit code zero, one exact PASS marker and exactly one JSON summary for every child.
- Rejects `ERROR:` or `SCRIPT ERROR:` output even when the process also prints PASS.
- Verifies 11 pinned source/contract hashes, consistent `CHALLENGE_004` identity, presentation render-model digest, runtime frame signature and `winning_frame`, phase timing, proposed editorial field windows, and deterministic Loop/Drill payload hashes.
- Prints a joined JSON review manifest to stdout only. It writes no review report, payload, image, or video file.
- Remains `REVIEW_CHAIN_CONSISTENT_NOT_VIDEO_READY`, never a production or baseline-approval signal.

## Apply and check frozen manifest

```powershell
cd C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS
Get-FileHash "$env:USERPROFILE\Downloads\C11D_RENDERER_UNIFIED_CONTENT_REVIEW_OVERLAY_V1.zip" -Algorithm SHA256
Expand-Archive -LiteralPath "$env:USERPROFILE\Downloads\C11D_RENDERER_UNIFIED_CONTENT_REVIEW_OVERLAY_V1.zip" -DestinationPath "." -Force
(Get-FileHash .\release\C11C_FREEZE_PACKAGE_MANIFEST.json -Algorithm SHA256).Hash
```

The C11-C manifest must remain `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.

## Test the contract

```powershell
python -m py_compile .\tools\c11d\d9\d_renderer_unified_content_review.py .\tools\c11d\d9\run_d_renderer_unified_content_review.py .\tools\c11d\d9\test_d_renderer_unified_content_review.py
python .\tools\c11d\d9\test_d_renderer_unified_content_review.py
```

## Run the joined in-memory review

```powershell
python .\tools\c11d\d9\run_d_renderer_unified_content_review.py --godot godot
```

If `godot` is not on PATH, pass the full path to the Godot 4.7.1 console executable, e.g. `--godot "C:\Path\To\Godot_v4.7.1-stable_mono_win64_console.exe"`. No media is produced. The command is expected to run five child harnesses and then print `C11-D RENDERER UNIFIED CONTENT REVIEW PASS` plus `C11-D UNIFIED CONTENT REVIEW SUMMARY=...`.

Run documentation updates only after the joined runner itself passes without runtime error logs:

```powershell
.\tools\c11d\d9\append_unified_content_review_doc_updates.ps1
```

Then run the renderer integration regression, baseline candidate preflight, and the frozen 22-step aggregate as separate commands. Keep this new coordinator outside the frozen aggregate until a distinct integration checkpoint accepts it.

## Known remaining blockers

Loop and Drill editorial fields/windows have not been defined by their source contracts. The Challenge visual payload is not yet materialized. Simulation sample-selection/interpolation and mapping of `winning_frame` to delivery frames remain unresolved. The timebase and field-window policies are unapproved. Independent renderer baseline acceptance and D4.8 authorization remain blocked/external.

## Governance locks

C11-C source and manifest are immutable; renderer OFF; `media_created=false`; `D4.8=BLOCKED`; `release_authority=NONE`; no persistent report and no renderer-native input are emitted.
