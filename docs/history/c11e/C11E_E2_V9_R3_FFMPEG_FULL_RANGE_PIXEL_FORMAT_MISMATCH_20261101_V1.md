# C11-E E2 V9 R3 â€” FFmpeg full-range pixel-format mismatch

**Date:** 2026-11-01  
**Request:** `C11E-E2-CH001-AB-20261101-V9-R3`  
**Failure ZIP SHA-256:** `cff29f245a1c8cf97ac02cd7bed3455a0a2ac364248f7cf257a2b148f2e0f6ab` (802,218 bytes; 76 entries; ZIP CRC clean)

## Result

Godot native numeric contract passed 30/30; Python contract passed 9/9. Godot rendered A; FFmpeg created A review MP4; runner stopped before B with `Final MP4 codec/pixel format mismatch for run A.` Diagnostic records renderer invocation count 1, media created true, accepted false, release authority NONE.

The source AVI is MJPEG, 540Ã—960, 60 FPS, 540 frames, 9 seconds, pixel format `yuvj420p` (full range). The final A MP4 is H.264 High, 720Ã—1280, 30 FPS, 270 frames, 9 seconds, one video stream and no audio, but FFprobe shows `pix_fmt=yuvj420p`, `color_range=pc`. The existing command's `-pix_fmt yuv420p` was insufficient because the scale filter propagated the input full-range format.

## Corrective change

The encode filter now uses `scale=720:1280:flags=lanczos:in_range=pc:out_range=tv,format=yuv420p`, and the encoder receives `-pix_fmt yuv420p -color_range tv`. The final probe assertion requires H.264, `yuv420p`, and `tv`. Installed FFmpeg 9.0 was used to transcode the actual R3 source AVI as a QA-only file; FFprobe confirmed the required format, range, geometry, frame rate, frame count and absence of audio.

This incident does not accept E2. Only R4's two renders, automated A/B comparisons, and separate visual/independent review can close E2. The renderer, source challenge and C11-C baseline were not modified.