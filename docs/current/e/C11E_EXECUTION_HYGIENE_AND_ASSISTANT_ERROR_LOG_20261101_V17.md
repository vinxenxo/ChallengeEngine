# C11-E execution hygiene and assistant error log â€” V17

**Date:** 2026-11-01

## R3: FFmpeg did not normalize full-range MJPEG input

R3 passed Godot numeric 30/30 and Python contract 9/9. It rendered A and encoded a valid H.264 High MP4 (720Ã—1280, 30 FPS, 270 frames, 9 seconds, no audio). The retained source AVI was MJPEG `yuvj420p` with full-range `pc`. FFmpeg command specified `-pix_fmt yuv420p`, but its `scale` stage auto-propagated full-range; FFprobe returned MP4 `yuvj420p/pc`. Runner correctly rejected the metadata and stopped before B.

Correction: explicitly set `scale` `in_range=pc:out_range=tv`, append `format=yuv420p`, pass `-color_range tv`, and verify `codec_name=h264`, `pix_fmt=yuv420p`, `color_range=tv`. The installed FFmpeg 9.0 test transcode of the retained R3 A AVI passed FFprobe with expected metadata. This changes only delivery encode normalization, not gameplay, renderer or C baseline.

## V21 V2: native stderr was misclassified by PowerShell 5.1

V21 V2 redirected a successful Python unittest process through PowerShell native command redirection under `ErrorActionPreference=Stop`. `unittest` emits its verbose test lines and summary on stderr; PowerShell converted the stream to a terminating `RemoteException` after displaying the first line. The V21 V2 catch path attempted rollback. This is not evidence that Python test 01 failed. V21 V3 uses `System.Diagnostics.ProcessStartInfo` for FFmpeg, FFprobe, Python and Godot, reads both redirected streams asynchronously, records their text and exit code, and validates the 9/9 summary without passing native stderr through PowerShell's error pipeline.

## Assistant execution lessons

- Do not loosen a media contract just to turn a test green; normalize sample range and enforce both pixel format and range.
- Do not infer A/B completion from a successful A-only MP4. R3 invocation count was 1; B and cross-run comparisons were not executed.
- Keep unique request IDs. R1/R2/R3 are consumed; next is R4.
- Runner exit code 1 is a gate failure even when one video looks good.
- No E3 or phase promotion before E2 A/B, frame invariance/difference checks, media hashes, and independent human review.
- Preserve FFmpeg/FFprobe commands, logs, probe JSON, source/final media hashes and output range fields in evidence ZIPs.

## Next action

Run R4 with runner SHA `158325324626085ebf319f68906ca8778f9a08eb39c6e8441da146c12ee4f953`. The runner itself repeats Godot 30/30 and Python 9/9 before A/B.