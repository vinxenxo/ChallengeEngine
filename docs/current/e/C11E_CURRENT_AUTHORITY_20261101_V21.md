# C11-E current authority â€” V21

**Date:** 2026-11-01
**Branch:** `main`
**Checkout:** `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`
**Status:** E2 pre-render contracts PASS; R3 partially rendered A and failed output pixel-range acceptance; R4 is the next physical attempt.

## Production and baseline authority

C11-C 2.19.12 remains the authoritative production baseline until E8 independent acceptance, freeze and explicit promotion. The frozen manifest remains 796,318 bytes, SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`. No protected C generator or mechanic was changed in this incident.

The complete product goal remains all three familiesâ€”Challenge, Visual Loop and Visual Drillâ€”with the C11-D presentation layer, enabled editorial, D3 Music V5, independent music seed, FFmpeg mux, FFprobe A/V validation, and one shared production service for GUI and CLI.

## Accepted pre-render gates

- E0 restart accepted as previously recorded.
- E1 shared production service automated suite 2/2 PASS; manual GUI observation remains pending.
- V9 reconciled installation: 16 operations, 12 applied, 4 already present; receipt SHA `d039360862d034b8f05f67cf8d0ddf914a1ed27075200f6a6c04462b92367972`.
- Godot 4.7.1 Mono JSON numeric contract: 30/30 PASS; gameplay and music JSON values are floats; full sidecar validation true.
- Python pair contract: 9/9 PASS after test 09 repair; test SHA `ab4ed3fd421ef0cac86d4ef25167f0161a186ef5bd90373414abed7bea17d2a9`; repair receipt SHA `6cbe3fe05d1b6f7cc7fe3971171d398a3b2197477668fce5b7b7a93b74dfd855`.
- V20 runner source-pin repair: PASS; runner SHA before R3 `c5d6bc26c70151238f60466fa401e1fd14ef9b0a25b34aa45d98ebce2ba5c763`; receipt SHA `41993b21c69f3197bf3bbe538e956bb356c4e4cf3866f7edbd1ec0eec0eb075e`.
- V21 V2 applicator attempt: FAILED during PowerShell 5.1 capture of Python unittest stderr; rollback attempted; not an E2 test failure. V21 V3 corrects this by capturing native stdout/stderr with `System.Diagnostics.ProcessStartInfo` and validates FFmpeg QA + Python 9/9 + Godot 30/30 before writing the runner.

## R3 result and exact failure

R3 request ID: `C11E-E2-CH001-AB-20261101-V9-R3`; checkout HEAD `7fbdf8529d2af6ba7089eacd8fd9b38682466d84`. Failure evidence ZIP: 802,218 bytes, 76 entries, CRC clean, SHA-256 `cff29f245a1c8cf97ac02cd7bed3455a0a2ac364248f7cf257a2b148f2e0f6ab`.

Godot numeric contract 30/30 and Python pair contract 9/9 passed inside R3. Renderer invocation count was 1: A completed; B was not invoked. The A source AVI was MJPEG `yuvj420p` full-range (`pc`), 540Ã—960, 60 FPS, 540 frames, 9 seconds. The A review MP4 was H.264 High, 720Ã—1280, 30 FPS, 270 frames, 9 seconds, with no audio stream, but FFprobe reported `pix_fmt=yuvj420p`, `color_range=pc` rather than the required `yuv420p` limited-range. The runner stopped at `Final MP4 codec/pixel format mismatch for run A.` R3 is a failed partial attempt; it is not an E2 PASS. No B render and no final A/B comparison exist.

## V21 V2 apply attempt and PowerShell 5.1 capture defect

The V21 V2 script validated the retained R3 media and built the expected runner patch, but it ran Python by invoking the native executable through PowerShell stream redirection while `$ErrorActionPreference = Stop`. Python `unittest` writes its progress and summary to stderr even when successful. Windows PowerShell 5.1 surfaced that redirected native stderr as a terminating `RemoteException`, causing the script to rollback the runner and stop. The failure was in the patch applicator's process capture, not in Python's nine tests or the FFmpeg media QA. No V21 documents/receipt were accepted from that attempt. V21 V3 captures stdout/stderr through `System.Diagnostics.ProcessStartInfo` and `ReadToEndAsync`, writes both logs as files, validates exit code and test markers separately, and only then writes the runner and documents.

## R3 output range defect and correction

The prior FFmpeg command requested `-pix_fmt yuv420p` but the scale filter retained the full-range input and propagated `yuvj420p/pc`. The corrected encode graph explicitly converts YCbCr range and format: `scale=720:1280:flags=lanczos:in_range=pc:out_range=tv,format=yuv420p`, plus encoder `-pix_fmt yuv420p -color_range tv`. FFmpeg's scale filter documents `in_range`/`out_range` and the `pc/full/jpeg` versus `tv/limited/mpeg` ranges. The actual retained R3 AVI has been transcoded using the installed FFmpeg 9.0 and FFprobe verified as H.264 High, `yuv420p`, `tv`, 720Ã—1280, 30 FPS, 270 frames, no audio.

Runner SHA after this correction: `158325324626085ebf319f68906ca8778f9a08eb39c6e8441da146c12ee4f953`. Only FFmpeg conversion arguments and the final color-range assertion changed. Renderer scene, shared sidecar validator, pair-builder, Python tests and C11-C source remain unchanged.

## Next controlled action

After committing the V21 V3 runner correction and documentation, run the same runner with new request ID `C11E-E2-CH001-AB-20261101-V9-R4`, gameplay seed `193847`, music seed `840001`, Godot 4.7.1 Mono, Python 3.13 and FFmpeg/FFprobe 9.0. Do not reuse R3. The runner repeats the Godot 30/30 and Python 9/9 tests before starting the two isolated renders. R4 must produce both A and B, both H.264 High / yuv420p / tv / 720Ã—1280 / 30 FPS / 270 frames / no audio, then pass all pixel identity/difference tests and output integrity checks.

E2 remains open until R4 automated A/B evidence and separate human/independent review of both videos. E3 remains blocked before E2 acceptance. No release authority or baseline promotion is granted.