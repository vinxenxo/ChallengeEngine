# C11-E E4A.6 Visual Contract and Full Test Campaign — Plan V12

## Reserved-band visual contract

The logical social frame is 540x960. HEADER y=0..144 and FOOTER y=816..960 are reserved opaque-black presentation bands whenever the optional D editorial envelope is enabled. At 720x1280 delivery, each band is 192 px. Optional title/subtitle appear only in HOOK/HEADER; optional CTA only in CTA/FOOTER. Inactive/empty regions retain black while text/rules hide. BODY and no-envelope legacy C rendering remain unchanged. Current body/video background colour is accepted; a user-selectable background is a separate later feature.

## V2 runner result and precise defect

V2 passed Windows PowerShell 5.1 AST; all 22 focused Python tests; Godot 4.7.1 editor import; 900-frame live root with one mount and 900 black-band frames; and Movie Maker capture (900 frames, 540x960/60 FPS/15 s). Movie Maker stdout includes configured envelope, full phase telemetry, audio export disabled and successful completion.

V2's overall BLOCKED is a runner false-negative. `Test-CaptureLog` is a path-based function (`Test-Path` then `ReadAllText`) but capture code supplied `$movie.Stdout` (text). The function returned false before checking log content. Do not claim the V2 overall status was PASS; do not repeat V2, Python, Godot or Movie Maker to repair this helper mismatch.

## Recovery-only V1.2 procedure

1. Verify the V2 failure receipt contains the known Movie Maker semantic postcondition error; pin the live-root summary, test stdout, Movie Maker stdout, envelope SHA and D-only source pins. Do not read Git HEAD/status or require `.git`; operator commits are expected each iteration.
2. Verify the uploaded source AVI SHA `2f6d0c73cb09571584db68e37760c933706473a07e559fc93113f26eabb89f45`; FFprobe confirms MJPEG 540x960/60 FPS/900 frames/15 s. The AVI has a PCM S16LE 48 kHz stereo track; always discard it.
3. Copy/reuse the AVI under a separate `RECOVERY_V1_2` output root without changing its bytes. Encode only stream `0:v:0`, with `-an`, to H.264 High 720x1280/30 FPS/450 frames/15 s, yuv420p and range `tv`.
4. Verify via FFprobe that the MP4 has exactly one video stream and no audio streams.
5. Extract output frame indices 0, 89, 90, 299, 300, 389, 390 and 449. Test inactive HEADER/FOOTER interiors (RGB channels <=8 on at least 99.9% of samples) and active HOOK header/CTA footer text (>=100 non-black samples each).
6. Preserve all inputs; write outputs/receipt and install the new versioned documentation add-only only after every check passes. Do not run gameplay, Godot or Python again.

The Windows recovery must use installed FFmpeg 9.0. An independent FFmpeg 7.1.5 analysis pass already corroborated the expected video contract and pixel samples, but does not replace the Windows receipt.

## Immediate next — full E4A Challenge A/V

Use the recovered D-composited silent MP4 unchanged. Reconcile exact D3 V5 engine/spec/profile and D3.3 mastering pins with accepted E4A.4 mux/FFprobe. Generate actual D3 V5 audio. A/B use the same gameplay/music seeds; C changes only `music_seed`. Prove A/B raw/mastered/decoded audio repeatability, C audio difference, identical H.264 elementary stream/frame identity across A/B/C, one AAC-LC 48 kHz stereo stream, non-silence, exact 15 s and A/V drift <=0.15 s. Preserve WAVs, muxed MP4s, FFprobe/volume reports, logs, commands and hashes. Complete human visual/listening review and E1 GUI/CLI parity.

Then E4B Loop, E4C Drill, E5, Smoke18, Matrix101 and E8 in order. CH_008/009 remain held for the 11 s/12 s discrepancy. No production rendering, dispatch, production media, release or promotion is authorized.


Recovery V1 stopped before evidence processing because it compared Git HEAD to a stale pre-commit value. V1.1 removed all Git checks and passed evidence/source preflight, but two subsequent attempts stopped at documentation preflight because the external manifest and then the document payload tree were missing from the runner directory. No media or source/docs writes occurred. V1.2 embeds the compressed doc manifest and all 15 documents in the runner, verifies and extracts them inside its run directory; only the runner `.ps1` needs to be copied to Downloads.
