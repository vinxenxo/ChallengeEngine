# C11-E E3 Execution Backlog — V1

**Date:** 2026-11-03
**Code base:** E3.2 commit `3cc1caa6d740b1525a4ebb30a4ff7f02868ac5a8`
**Status:** E3 implementation not yet physically executed.

## Objective

Produce the first C11-E audiovisual Challenge artifact by attaching deterministic D3 Music V5 to the already accepted, video-only E2 R4 `CHALLENGE_001` MP4. Preserve that visual stream exactly. Generate, master, mux and probe audio through the C11-E service invoked from Producer GUI. No gameplay rerender is needed to prove music-seed isolation.

## Work items in order

### E3-00 — GUI runtime and checkout/source reconciliation

- Refresh branch/HEAD/tree and C11-C manifest pin after the V24 docs commit.
- Refresh hashes for E3.2 engine/service/contract plus D3 spec/profile/source, D3.2/D3.3 runners and D9.2 runner/validator.
- Inspect the live `c11c-producer/main.py`, service entry and GUI-to-service callback. Verify no second service has been introduced.
- Launch the existing Producer GUI on Windows and record a real operator-observable smoke. The old E1 manual GUI observation remains pending until this succeeds.
- Read active D3 and D9 runner code, not only docs. Confirm tool versions and paths.

### E3-01 — D3 V5 raw audio contract tests

Use the immutable R4 video from the E2 evidence package as the timing/provenance input. Resolve the actual media path through the verified R4 receipt/evidence; do not hardcode an unverified file path.

For the initial `CHALLENGE_001` test fixture:

- gameplay seed remains the R4 request's `193847`;
- music seed is explicit, first control `840001`, second-seed control `840002`;
- style profile `challenge_8bit_v1`;
- `variation_index=0`;
- `tempo_bpm=104` only as the historical D9.2 fixed pilot fixture, not as a production default;
- `duration_seconds` is derived from the validated visual stream (R4 MP4: 270 frames / 30 fps = 9 seconds), not from V5 CLI defaults.

Test same canonical music input + same music seed gives identical parameter hash and WAV SHA-256; changing only music seed changes WAV; changing only gameplay seed leaves WAV identical when music inputs are fixed; invalid profile/seed/duration/tempo fails closed according to active schema. Preserve raw WAV and its provenance/parameter/output hashes.

### E3-02 — D3.3 mastering integration

- Preserve raw D3 V5 WAV unchanged.
- Follow the active D3.3 repair implementation, including its 30-second repeated measurement window and `loudnorm=I=-14:TP=-1:LRA=7` precedent.
- Deliver 48 kHz stereo PCM master for the E3 audio stage; verify integrated loudness, true peak, clipping and mono compatibility using the D3.3 QA methods.
- Keep the measurement window distinct from the final video duration. Create a deterministic final audio segment aligned to the validated video's duration. Prove exactly how trimming occurs, and test the exact output rather than inferring from the 30-second QA master.
- No unspecified fades, ducking, tempo changes or gain defaults. Check start/end discontinuity and clicks; if the source contract does not specify a remedy, record the issue rather than inserting an unapproved fade.

### E3-03 — FFmpeg A/V mux and FFprobe

Use the D9.2 Challenge pilot as the historical implementation precedent after refreshing source pins:

- video stream copy (`-c:v copy`); no video recode;
- AAC-LC/AAC, 192 kb/s, 48 kHz, stereo;
- `-shortest` and `+faststart` as in the pilot runner;
- exactly one video stream and one audio stream;
- 720×1280, frame rate and frame count identical to input visual;
- 48 kHz stereo AAC audio, non-silent and not truncated;
- video/audio duration difference no greater than the D9.2 pilot tolerance of 0.15 seconds;
- inspect stream start times, duration, frame counts and container metadata; any additional tolerance must come from an active contract, not guesswork.

The source visual must remain byte-identical at the video elementary-stream level where feasible, or decoded-frame-identical across every frame. The resulting MP4 is a new E3 test artifact, never a release product.

### E3-04 — Determinism and negative suite

- Repeat same music request twice: raw WAV and mastered PCM equality per D3.2 rules; compare decoded AAC audio samples if container metadata makes MP4 hashes differ.
- Change music seed only: audio must differ; decoded video frames must remain identical.
- Change gameplay seed only while holding music inputs fixed: music must remain identical. Do not rerender gameplay to test the audio side; use service/adapter isolation tests and a separate visual-seed contract test as appropriate.
- Negative controls: audio disabled, missing/invalid music source/profile, invalid seed, zero/negative duration, output collision, missing audio stream, multiple audio streams, silent/truncated audio, wrong sample rate/channel count/codec, A/V duration drift beyond tolerance, corrupted MP4 and FFprobe failure.
- On every failure retain structured report and logs; do not run PASS assertions after nonzero exit.

### E3-05 — GUI and CLI parity

- The operator launches and observes the E3 workflow only through Producer GUI.
- GUI must display selected video provenance, family/profile, both seeds, audio state and progress/result stages.
- CLI runs only as a separate-process automated compatibility test against the same shared service.
- Compare canonical request hash, music contract hash, editorial hash, seed domains, selected adapter, output hashes and final receipt semantics.

## E3 exit criteria

E3 can close only when all of these exist and pass:

1. Refreshed live-source pin report.
2. Contract-derived tests and their raw logs/exit codes/stdout+stderr hashes.
3. Raw WAV provenance and deterministic/seed-isolation evidence.
4. D3.3 mastering source + result QA with raw audio preserved.
5. FFmpeg command record, exit code and mux log.
6. FFprobe JSON, exactly one video/one audio stream and timing/codec checks.
7. Proof the video frames are unchanged by music seed.
8. Windows Producer GUI runtime and operator workflow evidence.
9. CLI separate-process parity tests through the same service.
10. Fresh run receipt, all source/media hashes, isolated test output and no production/release mutation.

E3 PASS does not close E4, authorize the 101-case matrix, or grant production/release authority. E4A/B/C follow independently.
