# C11-E R1V FFmpeg 9 pixel-decode compatibility correction — V1

**Date:** 2026-11-08. **Phase:** E4B / R1V integrated family-native A/V qualification. **Status:** correction prepared; Windows re-execution pending.

## Exact evidence and failure boundary

- Windows path-budget correction V2 installed successfully: `PASS_PINNED_REPLACEMENTS_AND_ADD_ONLY_DOCS`, 13/13 payloads. Install receipt SHA-256: `f57999151f94f378d08290b15bd30586a2180f855e280ef96b2ff4056b1decc5`.
- The integrated Windows wrapper passed the active-checkout gate: 52 tests, 0 errors, 0 failures, 0 skips. Wrapper run: `R1V_AV_WRAPPER_V1_20261108_012250_5CC5EFEF`; receipt SHA-256: `f8149461d80029bacbf8aa3ddb59ad33ee75246e5225c176a3190063594380b0`.
- A/V run: `Q5_022257_316922`; preflight `PASS_R1V_AV_PRELAUNCH_PREFLIGHT`; report SHA-256 `67759765d0c4d55737b3480d1d54f56e9b878dde75f2e462225bbc57f5412a70`; process receipt SHA-256 `f904e08edac76d07f5324b88937c71b0104ea1db18201d12154e6ec7df4ec74b`.
- The accepted Fractal Bloom A source was reused, and its FFprobe metadata/frame inventory were read. FFprobe measured one H.264 video stream at 720x1280/30, 660 frames, 22 seconds, `yuvj420p/pc`; source MP4 SHA remains `7971ced1d9cdbb7dd76a0d8d76e766faa9a051fc27419c9e737c41264796f659`.
- Pixel-decode stderr is exact: `Unrecognized option 'vsync'. Error splitting the argument list: Option not found`. Observed host runtime was FFmpeg `9.0-full_build-www.gyan.dev`, binary SHA `05f4251bce9293c2ab492cb17ca7724a0ffd0d06c881ba2ee83b82a89c2fc740`.
- Runner failed closed before any new C11-C launcher, WAV generation or AAC mux: `new_launcher_invocations=0`, `completed_av_outputs=0`, `audio_generation_count=0`, `aac_mux_count=0`. No source video was changed and no production gate was opened.

## Root cause

The pixel decoder used legacy global `-vsync 0`. FFmpeg 9 removed `-vsync`, so the command failed before emitting raw video bytes. This is a command-line compatibility defect, not a source MP4, timing, pixel format, PTS or frame-count defect.

## Correction

Replace only the decoder argument with output/per-stream `-fps_mode passthrough`. This preserves each input frame/timestamp for the rawvideo pipe and does not duplicate/drop frames. Keep `-pix_fmt yuv420p`, rawvideo stdout pipe, per-frame SHA-256, total byte/frame accounting and no-disk-frame policy unchanged. Improve failure detail to include process exit, decoded/expected frame counts and stderr excerpt.

The 52-test suite count is preserved: the existing path-budget test (test_04) now also asserts `-fps_mode passthrough`, rejects `-vsync`, and verifies rawvideo output remains pipe-only. A local reproduction with FFmpeg 7.1.5 decoded the accepted 660-frame MP4 to exactly 912,384,000 bytes (660 × 1,382,400 bytes), with no stderr. The target Windows runtime is FFmpeg 9.0; final confirmation remains the integrated Windows wrapper.

## Non-changes / boundaries

No change to selectors, gameplay/music seeds, C11-C native music helper or profile registry, WAV format, AAC mux contract, H.264 stream-copy contract, Option C, R1P, prior Fractal A, D3 V5, D compositor, D9.10 dispatch, render gates or approvals. Do not rerun R1P, Option C, or prior Fractal A. Do not create a silent-only intermediate phase. The next wrapper run must use a fresh compact run ID and fresh evidence roots; never clean/reuse failed run `Q5_022257_316922`.

## Provenance pins

- Evidence ZIP SHA-256: `a3388fe4bf26928ad3459562041a9dd6a2df5454059b92360a9a493d20443343`.
- V2 installer-receipt evidence ZIP SHA-256: `c3ba9392e273a4fcc8eb32843fd9a21ef37dd054f1f3792063daa7fa2a9c2ad8`.
- Frozen C11-C manifest SHA-256: `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.
