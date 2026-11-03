# C11-E E3 Challenge Audiovisual Implementation Plan V1

**Date:** 2026-11-03
**Scope:** first C11-E music-enabled Challenge test using the accepted E2 R4 visual artifact.
**Authorization boundary:** implementation and isolated test evidence only; no release/promotion.

## 1. Input visual

Resolve the R4 `CHALLENGE_001` video through the immutable E2 receipt/evidence ZIP. Verify the exact MP4 path exists and its current SHA-256 equals the R4 receipt. Select one visual variant (A) as the base. Do not render a new video. Probe the input and record codec, stream count, resolution, average/rational frame rate, `nb_frames`, duration, time base and start time.

R4 visual facts: 720×1280, 30 fps, 270 frames, 9 seconds, H.264 High, no audio. The E3 runner must still read and validate the actual artifact, not hardcode these values as a general policy.

## 2. Canonical E request

The E request retains:

- `content_type=Challenge`, `content_id=CHALLENGE_001`;
- gameplay seed `193847` from the R4 request;
- music seed `840001` for the first pilot; `840002` for the changed-seed negative/control;
- `audio_enabled=true`;
- D3 engine `c11d_music_engine_v5`, version 5.0;
- profile `challenge_8bit_v1`, version 1.0;
- `variation_index=0`;
- `tempo_bpm=104` only as the historical D9.2 fixed pilot fixture.

`duration_seconds` is calculated from the verified source video. For R4, check `270 / 30 = 9.0` seconds and ensure the FFprobe stream/container duration is consistent within the actual source metadata. If frame-rate/timebase/duration disagree, stop and record the mismatch.

Do not use V5 CLI's default duration 4 seconds. Do not silently default tempo 104 in E1 or GUI production requests.

## 3. Raw V5 output

Render to a fresh temporary location and preserve the source WAV. The output must be 22,050 Hz stereo PCM as declared by V5 implementation, with receipt fields engine/profile/seed/tempo/duration/variation/sample count/parameter hash/output SHA/peak/RMS/max PCM. A disabled-audio request must not invoke the engine at all.

Tests:
- same canonical music request twice → identical parameter hash and WAV SHA;
- changed music seed only → WAV hash differs;
- changed gameplay seed only while music request remains fixed → WAV hash is identical;
- incompatible profile, invalid/negative seed, nonpositive duration, invalid tempo or malformed config → fail closed.

## 4. D3.3 delivery mastering

The current D3.3 repair implementation is the operative historical precedent:

1. Preserve raw D3.2 source render.
2. Build a deterministic 30-second measurement window by repeating the source.
3. Apply FFmpeg `loudnorm=I=-14:TP=-1:LRA=7`, resample to 48 kHz, stereo, PCM signed 16-bit.
4. Verify integrated loudness/true peak, sample peak/clipping, mono downmix compatibility and QA receipt.

For E3 the music source is generated at the actual video duration, not copied from the old four-second D3 fixture. The E3 integration must define and test a final-duration extraction from the mastered output. The 30-second QA window is never muxed untrimmed into the R4 9-second MP4. Keep raw, QA-window and final-duration master as separate artifacts with hashes.

No new fades, ducking or tempo adaptation without an authoritative contract. Verify leading/trailing discontinuities and mobile mono behavior; record listening review separately.

## 5. FFmpeg mux

The D9.2 Challenge pilot runner provides the historical command contract:

- input 0 = verified video-only MP4;
- input 1 = final-duration mastered audio;
- map exactly `0:v:0` and `1:a:0`;
- copy video bitstream (`-c:v copy`);
- AAC audio, 192 kb/s, 48 kHz, 2 channels;
- `-shortest`, `-movflags +faststart`.

The active D9.2 runner must be re-pinned before coding. Do not overwrite the source MP4. Output to a fresh `artifacts/tests/c11e/e3/<RUN_ID>` root.

## 6. FFprobe and media QA

Require exactly one video stream and one audio stream. Verify:

- video codec/profile and dimensions match the input;
- frame rate, frame count and decoded frames remain identical to source;
- audio codec AAC, sample rate 48,000 Hz, stereo channel count/layout;
- audio is non-silent and not truncated;
- audio/video start times and end alignment are recorded;
- duration delta <= 0.15 seconds, matching D9.2 pilot implementation;
- format and stream metadata are internally consistent.

Do not assume MP4 container SHA equality across repeats. Compare source video elementary stream or decoded frames, and compare raw/mastered PCM/WAV bytes for deterministic audio. AAC may have encoder priming/container metadata; for repeatability compare decoded audio samples or AAC elementary-stream bytes according to the test contract.

## 7. Seed-isolation demonstration

Use one verified R4 visual MP4 for every E3 audio variant:

- A: music seed 840001;
- B: repeat 840001;
- C: music seed 840002.

Expected: A/B raw and mastered WAVs identical; C differs. The input video hash/frame sequence is identical for all three mux outputs. Changing music seed must not invoke Godot or alter video frames.

## 8. Receipt and GUI

The Producer GUI launches the same E service and displays: visual input identity, music seed, profile, tempo fixture/variation, derived duration, audio state, stage progress, logs, output MP4, FFprobe and QA summary. The service writes a structured E3 receipt binding request/plan/editorial hashes, source video hash, source/profile/spec pins, raw/mastered/audio/container hashes, FFmpeg/FFprobe version, exits and test statuses.

The CLI adapter is launched only by tests to prove separate-process parity. Do not require the operator to use CLI for production operation.

## 9. Stop conditions

Stop immediately for any source pin mismatch, stale/missing R4 source, changed C11-C manifest, protected path mutation, audio disabled yet engine invoked, missing/invalid receipt, nonzero native exit, missing stream, bad timing, failed mastering QA, changed decoded video frames or output-root collision. Retain failed evidence; never overwrite or synthesize a PASS.
