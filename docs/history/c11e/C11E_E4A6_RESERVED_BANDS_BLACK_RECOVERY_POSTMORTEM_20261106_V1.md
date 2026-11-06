# C11-E E4A.6 Reserved-Band Recovery — Postmortem V1

**Date:** 2026-11-06. This record closes the Recovery V1.2 investigation and supplements the capture/postprocess postmortems V10/V12.

## Final disposition

Recovery V1.2 passed on Windows PowerShell 5.1.26100.9818. Receipt SHA-256 `3279011fa16479d4901c5b271463707a437ce7458d306c1667ab222cb1603980`. User visual review PASS. This closes only the test-only visual/reserved-band subgate E4A.6.

## Evidence

- Recovery reused V2's 22/22 Python tests, Godot editor import/runtime and Movie Maker capture; no re-run.
- AVI source SHA `2f6d0c73cb09571584db68e37760c933706473a07e559fc93113f26eabb89f45`; MJPEG 540×960/60 FPS/900 frames/15s, plus an incidental PCM stream. PCM discarded.
- Silent review MP4 SHA `841b03531301c7e70c0e09ce3e9f536241d2072a87792e099ed7a955bef8c52f`; H.264 High/720×1280/30 FPS/450 frames/15s/yuv420p/TV range/no audio.
- Eight selected stills; 12 inactive band checks each observed zero non-black samples across 31,680 samples with RGB tolerance max 3; 4 active HOOK/CTA text checks passed. Operator visual inspection PASS.
- Six FFmpeg/FFprobe processes: exit code 0, no timeout, zero stderr bytes. `ffmpeg`/`ffprobe` 9.0.
- No source writes; C11-C manifest, shared layer and active D source pins preserved. No Git check was used in Recovery V1.2.

## Incident lessons retained

1. V2's Movie Maker capture did finish; the BLOCKED result was a path-versus-text helper contract bug.
2. Recovery V1 failed on stale Git HEAD and was invalidated; user manages commits. No future runner may consult Git.
3. Recovery V1.1's external docs manifest/dependency packaging failed twice before media processing.
4. Recovery V1.2 solved docs delivery with embedded self-hydrated archive and complete per-file SHA/byte validation; it passed.

## Remaining boundary

The silent MP4 intentionally contains no music. The next E4A.7 task uses that exact MP4 as the immutable H.264 source and adds D3 V5/D3.3 audio via stream-copy mux. Do not repeat visual capture or postprocess without a concrete defect.
