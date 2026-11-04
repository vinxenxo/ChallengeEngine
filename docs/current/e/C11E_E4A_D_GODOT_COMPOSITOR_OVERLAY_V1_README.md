# C11-E E4A.3 D-owned Godot compositor overlay — V1

## What this increment does

This overlay adds a bounded E4A.3 test for the existing D-owned Challenge materializer. It reuses the accepted E4A.2 `CHALLENGE_004` run and normalized silent review MP4, extracts six still frames, and lets the existing D materializer create transparent Godot SubViewport layers alpha-composited over the real frames. It produces 18 PNGs and 12 comparisons. It does not rerender C11-C, create a new MP4, add audio, dispatch D9.10, or enable production rendering.

## Apply and run

Save `C11E_E4A_D_GODOT_COMPOSITOR_PIXEL_OVERLAY_V1.zip` and the adjacent `.sha256` file in the Windows Downloads folder. From the active repository root, run the integrated PowerShell 5.1 block supplied with this handoff. It validates the ZIP/sidecar, the frozen C11-C manifest and every overlay payload/preimage before it writes; then it runs the 46 focused Python tests and the Godot 4.7.1 test runner against:

`artifacts/tests/c11e/e4a_real_body_pixel_review/RUN_20261104_002559_542bcf60`

The runner requires `C11D_GODOT_EXECUTABLE` or the existing WinGet Godot 4.7.1 Mono path, plus FFmpeg/FFprobe on PATH or configured in `C11E_FFMPEG_EXECUTABLE` / `C11E_FFPROBE_EXECUTABLE`. It creates a unique evidence folder under:

`artifacts/tests/c11e/e4a_d_compositor_pixel_review/RUN_*`

Capture the actual exit code. On error, do not print or reuse a PASS marker. Zip the entire reported RUN folder and upload it for review.

## Expected acceptance signals

- Python tests `46/46`.
- Godot exit code 0 and exact marker `C11E E4A D-OWNED GODOT REAL-BODY COMPOSITOR PASS`.
- `REAL_C11C_FRAMES_EXTRACTED=6/6`, Godot-composited PNGs `18/18`, comparisons `12/12`.
- BODY pixel identity across A/B/C at all six real samples.
- Original/normalized MP4s and all six extracted base-frame hashes unchanged by Godot.
- Frozen C11-C manifest and C11-C source hashes unchanged.

A successful E4A.3 test is still not production rendering, complete video composition, A/V acceptance, layout approval, GUI integration or release approval. Text coordinates are fixture placeholders. Safe area and generic typography remain unknown; visual placement is unapproved. `player_name`/`challenge_label` remain blocked.

## Current authority

C11-C 2.19.12 and its manifest remain frozen/authoritative. Production D renderer OFF, D9.10 PREPARE_ONLY, D4.8 BLOCKED, D9.14/D9.16 BLOCKED, D9.17 BLOCKED_NO_GO, D10 BLOCKED_FOR_PROMOTION, `release_authority=NONE`.
