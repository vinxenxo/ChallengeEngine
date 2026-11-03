# C11-E E3 — Challenge audiovisual pilot test V1

- Date: 2026-11-03
- State: OVERLAY PREPARED; local integrated suite PASS; Windows checkout execution and operator GUI run pending.
- Entry code commit: `3cc1caa6d740b1525a4ebb30a4ff7f02868ac5a8` (E3.2)
- E3.2 service: `0.2.0-E3.2`; intent schema `C11-E-PRODUCTION-INTENT-V1` v1.1.
- Release authority: `NONE`.

## 1. Purpose and scope

Move from the E3.2 semantic binding into the first executable audiovisual test. This is a test-only Challenge pilot using the already accepted E2 R4 CHALLENGE_001 A video-only MP4. It must not rerender gameplay. It exercises the current E1 preparation contract, D3 Music V5, the D3.3 mastering chain, FFmpeg mux and FFprobe checks in one evidence-producing path.

The pilot is deliberately narrower than the product acceptance target. It does not close E3 family-wide, E4 editorial/layout, E5, Smoke18, Matrix101 or E8. The GUI button is placed inside the existing D9.9 Universal Editorial tab and the existing nested output tabs; no new top-level tab, no sixth operational surface and no second Producer are added.

## 2. No Git administration in the operational path

The Apply script, test runner and Downloads launcher do not call Git. They do not query branch, HEAD, `git status`, cleanliness, ancestry, stage files or create commits. A local commit is not a prerequisite for applying or running this overlay.

The installer uses file-level SHA-256 pins only to ensure that the target GUI source is the expected preimage and that the E3.2 service, V5 engine and contract are the expected implementation. This is source compatibility protection, not Git governance. The installer preserves a backup of the replaced `main.py` and refuses unknown pre-existing destination content rather than overwriting it.

## 3. Fixed R4 source fixture

The overlay contains the exact R4 evidence artifacts:

- Video: `CHALLENGE_001_R4_A_REVIEW_720.mp4`; 195,690 bytes; SHA-256 `3d72e52cc7f7f8fc4b32c8719ab9800ba622e6069c7fa956526c108defce1afd`.
- Receipt: SHA-256 `2f8c355453d8558c6af42aa5da35f603b767726d64ba04f842dc799a2cadef7f`.
- Receipt sidecar: SHA-256 `77ae09b3d65b8d219fd409b1ab062344290d4766c71bdc70eafff6d70affe958`.

The runner also verifies the receipt/video relationship and FFprobe metadata. Required source: one H.264 video stream, no audio, 720x1280, 30 FPS, exactly 270 frames. Duration is derived from frames divided by frame rate (9 seconds); it is not supplied by a V5 default.

R4 gameplay seed is `193847`. The first music seed is `840001`; the changed-seed control is `840002`. The music seed recorded in the historical R4 receipt was unused during E2. The source MP4 and E2 receipt are read-only fixtures.

## 4. Music and mastering test

Challenge uses `c11d_music_engine_v5` 5.0 and `challenge_8bit_v1` 1.0. The pilot fixture uses tempo 104 BPM and variation index 0. Tempo 104 is explicitly a fixed historical D9.2 pilot input, not a global production default. E1 does not supply or invent tempo/duration for general production requests.

Three independent V5 invocations are required:

1. A: `music_seed=840001`.
2. B_REPEAT: `music_seed=840001` again.
3. C_CHANGED_MUSIC_SEED: `music_seed=840002`.

Expected raw WAV behavior: A and B have identical parameter/output hashes; C has a different output hash. Gameplay seed remains 193847 throughout.

Each raw WAV is repeated to a deterministic 30-second D3.3 measurement window, passed through `loudnorm=I=-14:TP=-1:LRA=7`, encoded as stereo PCM S16LE at 48 kHz, and validated for integrated loudness, true peak, hard clipping, and mono compatibility. The 30-second QA window is never muxed as-is. A separate delivery master is trimmed to the duration measured from the video (9 seconds); it is checked for format, duration and clipping before mux.

D3.3 QA targets are read as constraints, not a license to alter the underlying V5 synthesis or to extend the final social video. The original raw WAV artifacts remain in test evidence.

## 5. Mux and FFprobe acceptance

For A, B_REPEAT and C_CHANGED_MUSIC_SEED:

- Video: map the R4 H.264 stream and use `-c:v copy`; do not re-encode gameplay.
- Audio: AAC-LC, 192 kb/s, 48 kHz, stereo.
- Use `-shortest` and `+faststart`.
- FFprobe must find exactly one video and one audio stream.
- Video must remain H.264, 720x1280, 30 FPS and 270 decoded frames.
- Audio must be AAC, 48 kHz, two channels.
- Absolute audio/video duration drift must be <= 0.15 seconds.
- Extracted H.264 elementary stream hash must be byte-identical to the source for all three muxes.
- Decoded AAC samples for A and B must be identical; C must differ from A.

The pilot writes a JSON receipt, SHA-256 sidecar, per-command JSON, stdout/stderr and exit-code logs. A failure writes a fail-closed receipt where the run output directory exists. Output root collisions are rejected.

## 6. Producer GUI integration

The existing Producer window keeps its three top-level tabs. The new E3 button is embedded in the existing `C11-D · EDITORIAL UNIVERSAL (D9.9)` tab and uses the existing D9.9 selectors/editorial model and E1 shared service.

The button sets the bounded R4 test fixture in the visible form (Challenge / key / CHALLENGE_001 / REVIEW_720 / gameplay seed 193847 / music seed 840001 / variation 0 / audio enabled), prepares the E1 GUI intent through the existing `_run_d9_universal_plan()` path, and requires the current GUI/CLI semantic parity checks to pass before launching the E3 worker with `QProcess`. The CLI is a worker/compatibility path of the shared service, not a second user-facing workflow.

GUI-created E3 media and logs go to:

`%USERPROFILE%\Documents\C11E_E3_AUDIO_PILOT_TESTS\<run-id>`

The test runner's automated integration test uses a temporary directory that is deleted after the test. The GUI operator run deliberately retains evidence under Documents for inspection.

## 7. Installer and launcher behavior

The standalone `START_C11E_E3_FROM_DOWNLOADS.ps1` expects the overlay ZIP, itself, and the `.cmd` helper directly in the user's Downloads directory. It:

1. Verifies the overlay ZIP SHA-256.
2. Extracts it into a unique new directory beneath Downloads (never overwrites a previous extraction).
3. Runs `APPLY_C11E_E3_AUDIO_TEST_OVERLAY.ps1` against the fixed checkout path.
4. Runs `RUN_C11E_E3_AUDIO_TESTS.ps1`.
5. Checks that PySide6 imports under the same Python 3.13 interpreter.
6. Launches the Producer GUI only if compile, the complete C11-E test suite and the GUI dependency check pass.

The operator does not need to change directory. Run the `.cmd` by double-clicking, or call the PowerShell launcher by its full Downloads path from any current directory.

## 8. Local validation performed while preparing the overlay

Against a reconstructed lab tree using the E3.2 source pins and the accepted R4 evidence fixture:

- Python compilation: PASS.
- Full `unittest discover -p test_c11e*.py`: **31/31 PASS**.
- Includes 13 E1 tests, 8 E3.2 tests, 5 audiovisual integration tests and 5 GUI integration/source-contract tests.
- The full audiovisual test executed V5, mastering, mux and FFprobe in a temporary directory; it verified deterministic repeats, changed music seed, identical H.264 video elementary streams and unchanged E2 gameplay source.

This local lab result is not the user's Windows execution receipt and is not a manual GUI observation. The launcher captures Windows stdout/stderr, exit codes and SHA-256 logs in Documents. The operator GUI click remains an explicit test after the launcher opens the Producer.

## 9. Protected boundaries

The overlay does not change `core/audio`, protected C11-C generators/mechanics/RNG, C11-C frozen release manifest, D governance locks, or production authority. It does not invoke Godot, a gameplay renderer, or any C generator. FFmpeg is used only to create temporary/isolated test audio and mux test MP4s from the pinned existing video fixture.

`release_authority=NONE`; `baseline_promotion=false`; `production_product_created=false`.

## 10. Exit criteria for this test overlay

- Windows complete test suite exits 0.
- All tests pass; compile stage passes.
- GUI starts from the same Producer entry point.
- E1 GUI/CLI parity passes before E3 worker starts.
- GUI E3 pilot produces the three test MP4s and a valid receipt/checksum in Documents.
- Operator reviews playback and confirms no audible defect or A/V sync issue.

Passing this overlay qualifies the Challenge audio/mux seam only. E4A full Challenge presentation/editorial, E4B Loop, E4C Drill, E5/E6/E7 and E8 remain on the roadmap.
