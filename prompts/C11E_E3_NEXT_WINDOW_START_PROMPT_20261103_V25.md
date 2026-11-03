# C11-E next-window start prompt — V25 / E3 audio pilot

Continue in the active Windows checkout:

`C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`

## Mission

Deliver complete C11-E audiovisual production for Challenge, Visual Loop and Visual Drill, with the existing C11-C generators/mechanics preserved, D presentation/editorial and family layouts integrated, independent gameplay/music seed domains, FFmpeg mux, FFprobe validation, deterministic evidence and one shared production service. The Producer GUI is the operator's primary workflow from now on. CLI remains only compatibility/automation through the same service.

## Operator constraint: do not create Git administration work

Do not require a clean worktree, branch/HEAD checks, a local commit, `git add`, or `git status` to apply overlays or run tests. Do not add Git checks unless the user explicitly requests repository governance work. Keep file-level SHA pins only when needed to protect exact source preimages and required contract versions. The user commits locally at their discretion; it is not a prerequisite for continuing engineering.

The E3 audio overlay's Apply script, test runner and Downloads launcher deliberately perform no Git operations. User applies/runs it directly from Downloads without `cd`.

## Current code and evidence state

- E3.2 code commit: `3cc1caa6d740b1525a4ebb30a4ff7f02868ac5a8`.
- E3.2 parent: `a30b63d31b2d071ebab9c67ec9f8ff7393731488`.
- E3.2 implementation and all 21 E1/E3.2 tests were verified by the user; seven payload files passed SHA/size audit.
- V24 documentation overlay was applied and all 12 payload files verified. It remains permissible for those docs to be uncommitted; do not request an administrative commit.
- C11-C manifest remains SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953` (796,318 bytes).
- E2 R4 bounded CHALLENGE_001 title-to-pixels/gameplay-invariance result is accepted and formally closed. It used a video-only 720x1280 H.264 MP4, 270 frames, 30 FPS, 9 seconds, gameplay seed 193847. This is not full Challenge-family or full product acceptance.
- E3.2 binds the D3 V5 Challenge music contract into E1 intent, but E1 itself remains preparation-only/non-dispatchable.
- E3.2 engine/service/contract pins are checked by the new overlay installer and E3 tests.

## Immediate action already prepared

Use `C11E_E3_AUDIO_TEST_OVERLAY_V1.zip` with `START_C11E_E3_FROM_DOWNLOADS.ps1` or `START_C11E_E3_FROM_DOWNLOADS.cmd`, all placed directly under `%USERPROFILE%\Downloads`.

Invoke from any directory:

`powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$env:USERPROFILE\Downloads\START_C11E_E3_FROM_DOWNLOADS.ps1"`

Or double-click the CMD launcher. It verifies the ZIP hash, extracts under Downloads to a unique folder, applies the source-pinned overlay without Git operations, runs compile and the full `test_c11e*.py` suite, and launches the Producer GUI only on PASS.

The overlay adds an E3 audio/mux action inside the existing D9.9 Editorial Universal tab and an output subview within that tab. It does not add a top-level tab or a sixth operational surface. The GUI action prepares the E1 intent through the existing D9.9 shared service and checks GUI/CLI semantic parity before launching the E3 worker.

## E3 Challenge audio pilot contract

- Reuse the pinned accepted E2 R4 video-only MP4; never rerender gameplay for E3.
- Source: H.264 720x1280, 30 FPS, 270 frames; derive duration from FFprobe (9 sec).
- Gameplay seed 193847; music seed A/B 840001; changed-seed control C 840002.
- D3 Music V5 5.0, profile `challenge_8bit_v1` 1.0, variation 0, tempo 104 BPM as the fixed D9.2 pilot fixture only (not a global default).
- Generate A/B repeats with identical raw WAV hash and C with changed hash.
- Apply D3.3 deterministic 30-second QA window/loudnorm targets to each seed; preserve original WAV; trim the delivery master to the exact source-video duration.
- FFmpeg mux: H.264 video stream copy, AAC 192 kb/s, 48 kHz stereo, `-shortest`, `+faststart`.
- FFprobe: exactly one video and one audio stream, expected codec/size/FPS/frames/rate/channels, A/V duration drift <=0.15 sec.
- Extract H.264 elementary stream and prove it is identical to source for all music seeds; decode AAC to compare A/B identical and C different.
- All media are test evidence, not production. Output root for the GUI operator run is Documents/C11E_E3_AUDIO_PILOT_TESTS/<run-id>. Automated integration test output uses TemporaryDirectory.
- `release_authority=NONE`, `baseline_promotion=false`, `production_product_created=false`.

## GUI-primary constraint

Manual operation from this point is via the existing Producer GUI. Do not create a new GUI application, second Producer, new top-level tab or `c11d-control`. Keep exactly the existing three Producer top-level tabs and add E actions only inside the D9.9 universal editorial surface and its existing nested output tabs. CLI is not an alternative operator workflow; preserve it for test automation and semantic parity.

E1 manual GUI observation is still pending until the user runs and reviews the Windows GUI. Static tests do not equal manual GUI acceptance.

## After E3 pilot

1. Inspect Windows test runner stdout/stderr, exit code and SHA-256 evidence. Do not repeat a green suite without a source change.
2. Launch the Producer via the Downloads launcher and click `C11-E E3 · AUDIO + MUX PILOT CHALLENGE_001 / R4 (SIN RERENDER)` in the D9.9 editorial tab.
3. Review the three MP4s, receipt, A/V sync and audio quality. Record operator result separately from automated PASS.
4. If E3 passes, update the authority/gate matrix and continue E4A Challenge presentation/editorial integration. Then E4B Loop and E4C Drill using their correct family binders and existing family audio paths. Do not map the Challenge 8-bit profile onto Loop/Drill.
5. E5 seed isolation/determinism/parity; E6 Smoke18; E7 Matrix101; E8 independent acceptance/freeze/promotion.

## Immutable boundaries

Do not change `core/audio`, protected C11-C generators/mechanics/timing/frame stream/RNG, C11-C frozen manifest, or D release/governance locks. Keep the five existing `c11c-suite` modules. C11-C 2.19.12 remains production authority until E8. No render, audio pilot, automated PASS, or user test authorizes production promotion.
