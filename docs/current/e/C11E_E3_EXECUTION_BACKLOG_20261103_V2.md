# C11-E E3 Execution Backlog — V2

**Date:** 2026-11-03
**Current implementation:** V1.3 audio pipeline patch APPLIED 10/10.
**Automated Windows result:** V1.4, 31/31 tests PASS; Python compile PASS; PySide6 6.11.2.
**Current gate:** E3-GUI-01, manual Producer GUI runtime and operator pilot.

## Objective

Create the first C11-E audiovisual Challenge pilot by attaching deterministic D3 Music V5 to the accepted video-only E2 R4 `CHALLENGE_001` MP4, without rerendering gameplay. Preserve decoded visual frames exactly. Execute through the existing Producer GUI and E1 shared service. Keep outputs test-only until E3 acceptance.

## Already completed — do not repeat

- E3.2 D3 V5 contract/binding to E1 intent; contract, profile and seed independence tests accepted.
- V1.3 code overlay applied: main.py integration, audio pipeline, audio pilot, audio tests, GUI integration tests and immutable R4 fixture/receipt.
- V1.4 Python compile and all `test_c11e*.py`: 31/31 PASS on Python 3.13.14.
- PySide6 import: PASS, 6.11.2.
- Temporary integration test executed D3 V5, mastering/mux path and seed isolation; no production output.

## E3-GUI-01 — manual GUI runtime and control observation (next)

1. Read the live Producer GUI launch path in the active checkout; do not invent an entrypoint or use an unrelated CLI. Identify the existing window/control where universal editorial production is initiated.
2. Launch the GUI in Windows and record an actual operator-visible result: application startup, E3 action visibility, enabled/disabled controls, selected R4 source provenance, family/profile, gameplay/music seeds, pilot parameters, progress, logs, errors and final output reference.
3. Confirm the action builds/prepares the canonical E1 production intent and calls the E3 pipeline through the same service. There must be no second producer, no sixth tab and no independent CLI production branch.
4. Run the pilot from the GUI with a unique run ID and a fresh test-only output root. If the GUI cannot launch or the action is absent, stop at that precise failure and capture logs/screenshots. Do not rerun tests that already passed.
5. The old E1 manual GUI operator observation is closed only when this live interaction is recorded and independently reviewed; a PySide6 import or source-inspection test is not enough.

## E3-RAW — physical raw WAV generation

Input must be the R4 A review MP4 resolved from the verified R4 receipt/fixture. Confirm path, SHA-256, stream and 9-second duration before use.

- Profile: `challenge_8bit_v1`.
- Gameplay seed: `193847`, recorded as R4 visual provenance only.
- Music seed: `840001`; second-seed control `840002`.
- `variation_index=0`.
- `tempo_bpm=104` only as the historic D9.2 CH001 test fixture; never treat as a global default.
- Derive `duration_seconds` from FFprobe. R4 input is 270 frames / 30 fps = 9 seconds. Reject V5's 4-second fallback/default.
- Preserve raw WAV and record the canonical request/parameter hash, profile/spec/engine pins, sample rate/channel count/sample format, byte length and SHA-256.
- Same canonical inputs + same music seed must produce byte-identical deterministic raw WAV. Changing only music seed must change it. Changing gameplay seed with all music inputs fixed must leave it identical.

## E3-MASTER — D3.3 mastering

- Inspect and pin the current D3.3 implementation before use; docs alone are not sufficient.
- Preserve raw D3 V5 WAV unchanged.
- Reproduce the implemented D3.3 30-second repeated measurement window and FFmpeg loudnorm precedent `I=-14`, `TP=-1`, `LRA=7`.
- Deliver the specified 48 kHz stereo PCM master; record integrated loudness, true peak, clipping and mono compatibility.
- The 30-second QA measurement window is not the final 9-second audio. Implement and verify deterministic trim/alignment to the video duration. Do not invent fades, ducking, tempo shifts or gain defaults.
- Examine first/last-sample discontinuity/clicks; document issues instead of inventing a remedy where the contract is silent.

## E3-MUX — FFmpeg mux and FFprobe

- Refresh D9.2 runner/validator hashes, then use the historical Challenge pilot precedent: video stream copy, AAC 192 kb/s, 48 kHz stereo, `-shortest`, `+faststart`.
- Exactly one video and one audio stream.
- Preserve 720x1280, video codec/profile, frame rate, frame count and every decoded video frame. Prefer video elementary-stream hash equality where feasible; otherwise prove decoded-frame equality over all frames.
- AAC must be non-silent and not truncated; verify 48 kHz stereo/channel layout.
- Inspect start time and duration of both streams and container. Historical D9.2 tolerance is <=0.15 s; do not invent extra tolerances.
- Record full FFmpeg argument vector, tool versions, exit code, stdout/stderr hashes, FFprobe JSON and all media hashes.

## E3-DET — repeatability, seed isolation and negative controls

- Same music request/seed twice: identical raw WAV and mastered PCM; compare decoded AAC samples or elementary stream for mux repeats rather than assuming MP4 container hashes must match.
- Change only music seed 840001 -> 840002: audio differs, video decoded frames identical.
- Change only gameplay seed with music inputs fixed: audio identical; do not rerender gameplay merely for this audio assertion.
- Negative tests: audio disabled; missing/invalid profile/source; invalid seeds; zero/negative duration; output collision; missing/multiple audio streams; silence; truncation; wrong codec/sample rate/channels; excessive duration drift; corrupt MP4; FFprobe failure. Stop at first failed stage and preserve evidence.

## E3-GUI/CLI — operator and parity acceptance

- GUI is the only human-operated product path. It must show video provenance, family/profile, both seeds, audio state, progress, error details, final artifact and QA summary.
- CLI is invoked only by automated separate-process tests through the same canonical E1 service. Compare request, editorial, music contract, adapter, seed domains, result and receipt semantics. No parallel CLI product implementation.

## E3 exit evidence (all required)

1. Refreshed source-pin inventory after V1.3.
2. Existing 31/31 V1.4 Windows test result receipt/logs (already supplied; do not rerun).
3. GUI launch/action/operator observation.
4. Raw WAV provenance and deterministic/seed-isolation evidence.
5. D3.3 source pins and mastering QA with raw WAV preserved.
6. Full FFmpeg mux command/exit/logs.
7. FFprobe JSON proving one video/one audio, metadata, duration and stream timing.
8. Proof every decoded video frame equals the R4 source.
9. CLI separate-process parity test through E1 service.
10. Structured run receipt, hashes and isolated test-only output, with no C11-C/release mutation.

E3 closure does not close E4, Smoke18, Matrix101 or grant release authority.

## After E3 — full roadmap

- E4A: full Challenge presentation, layout and editorial binding; family-specific timeline tests.
- E4B: Visual Loop binder/adapter, grammar-specific editorial and existing C11-C music via audio-only E orchestration.
- E4C: Visual Drill binder/adapter, phase mapping and END_CTA precedence, existing C11-C music via audio-only E orchestration.
- E5: three-family determinism, independent gameplay/music seeds, no family leakage, GUI primary workflow and CLI compatibility parity.
- E6: Smoke18, six audiovisual cases per family.
- E7: Matrix101: 54 Challenge + 27 Loop + 20 Drill. CH_008/009 remain held because 11-second declared duration conflicts with 12-second phase sum (3+7+0+2); runnable subset is provisionally 99.
- E8: independent acceptance, immutable freeze, explicit authority and promotion.
