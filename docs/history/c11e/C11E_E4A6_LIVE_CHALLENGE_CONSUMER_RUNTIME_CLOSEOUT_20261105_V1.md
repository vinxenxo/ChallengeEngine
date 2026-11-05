# C11-E E4A.6 Live Challenge Consumer — Runtime Closeout V1

**Date:** 2026-11-05. Evidence: `C11E_E4A6_LIVE_CONSUMER_V3_20261105_140409.zip`.

## Disposition

`E4A.6_LIVE_ROOT_RUNTIME=PASS_TEST_ONLY`.

The live Challenge root ran in the active Windows checkout with the E1 editorial envelope. The D consumer was invoked after the four existing native binder calls. This closes the E4A.6 live-root runtime gate in its bounded technical scope; it does **not** close the pixel/geometry subgate or full E4A.

## V3 evidence

- Evidence ZIP SHA-256: `1e5969c3b3a17f3a39381438f5fd12f97dd38573b62639de8db3e65caa39063d`; CRC PASS; 22 entries.
- Receipt SHA-256: `03e568bf78d442949c70495c946ab1995e07ee48b98db00fcc6efb729c7494fe`.
- Windows PowerShell 5.1.26100.9818 AST PASS; active checkout Git HEAD `a18444655cdb844104561840a59a473b7bbbb172`.
- Python `py_compile` PASS; focused tests 17/17 PASS; E1 envelope PASS.
- Godot 4.7.1 import/cache PASS and live root PASS with empty stderr.
- 900 frames at 60 FPS; HOOK 180, GAME 420, REVEAL 180, CTA 120; one shared-layer mount; D header owner 180 frames; D footer owner 120 frames; native CTA simultaneous owner 0.
- Renderer input false; production dispatch false; media created false; `release_authority=NONE`.

## `GeneradorMaestro.gd` integrity

The live source SHA-256 is `d42782e8f5bb94ff0ede653a1c4624dc91541cc8203abf136b09a8fc288a7d82`. This is the existing V2 D-only integration postimage. V3 explicitly records `generadormaestro_written=false`; its root test proves this exact postimage executes with the D envelope. Do not revert or alter it during pixel capture.

## Separate E4A.4 audio evidence

E4A.4 report SHA-256 `14cc43332e09c698a55e921be4538af8335d5495864a5c25c1c1611b689cdcbf`; receipt SHA-256 `8d351c513b6972d4f583dfe6678ab46e0441ab0466315a03abf1ce1179c115ca`. The isolated D3 V5/D3.3 + FFmpeg/FFprobe test passed on a C11-C review video. Same-seed audio repeated; changed `music_seed` changed audio; output was AAC 48 kHz stereo, non-silent, 15 s, and measured A/V start/end drift 0. The report explicitly sets `fullframe_d_compositor_embedded_in_mp4=false`; human listening/video review remains pending. It is not combined D-overlay A/V proof.

## Still open

V3 created no Movie Maker video, PNG, FFmpeg output or pixel evidence. D1.5/D1.1/D1.7 geometry, safe typography, overlap/clipping and visual acceptance remain open. `visual_placement_approved=false`; `production_compositor_layout_acceptance=NOT_GRANTED`.

## Next bounded gate

Run the V2 test-only silent pixel capture: no-envelope compatibility smoke, a 900-frame Godot Movie Maker capture, 720x1280/30 FPS silent review MP4, FFprobe validation, and eight delivery-frame boundary stills. This does not invoke the production launcher/GUI/CLI, export audio, mux audio or alter source code. Human review is required; a successful capture receipt does not grant layout approval.
