# C11-E E3 Negative Controls — V1.5 Test Plan

**Date:** 2026-11-03  
**Purpose:** Complete E3 fail-closed media QA without changing the D3 V5 engine, E1 shared service, C11-C generators/mechanics, D9 governance or GUI dispatcher.

## 1. Scope of implementation

The only production-code replacement in this overlay is `c11c-suite/c11c-producer/c11e_e3_audio_pipeline.py`. It extracts final A/V stream metadata checks into `_validate_mux_probe()` and extends final-MP4 QA to run FFmpeg `volumedetect` against the muxed output. This closes an evidence gap: previously the pipeline measured mastered PCM before mux, while the final AAC output itself was not separately proved non-silent.

The overlay does not change D3 V5 generation, D3.3 mastering parameters, FFmpeg mux arguments, the R4 source, seed values, E1 intent semantics, `main.py`, CLI adapter or GUI callback. It does not rerender gameplay.

## 2. Negative-control matrix

| Area | Injection / invalid condition | Required result |
|---|---|---|
| E1 seeds | gameplay seed 0; music seed 0 | Reject during intent validation |
| D3 profile | missing pinned profile file | Reject source pin before generation |
| D3 profile | unsupported Challenge style-profile ID | Reject before WAV output |
| R4 input | missing source file | Reject before engine or mux |
| Output policy | output root already exists | Reject; existing sentinel remains unchanged |
| Streams | no audio stream | Reject |
| Streams | no video stream | Reject |
| Streams | multiple audio streams | Reject |
| Streams | multiple video streams | Reject |
| Video | codec not H.264 or frame count not R4 count | Reject |
| Video | dimensions differ from 720×1280 or frame rate differs from 30 FPS | Reject |
| Audio | codec not AAC | Reject |
| Audio | sample rate not 48,000 Hz | Reject |
| Audio | channel count/layout not stereo | Reject |
| Audio content | silent final audio | Reject using FFmpeg volume metrics |
| Timing | zero, negative or malformed media duration | Reject |
| Timing | audio truncated beyond 0.15 s end-time tolerance | Reject |
| Timing | start-time drift over 0.15 s | Reject |
| Timing | end-time drift over 0.15 s | Reject |
| File/process | corrupt MP4 or nonzero FFprobe process | Reject and preserve stderr/native exit code |

The tests are fail-closed contract/unit tests using synthetic FFprobe metadata and real local FFmpeg/FFprobe probes for silence/corruption. They do not fabricate successful physical production media.

## 3. Final MP4 validator

The final mux validator requires exactly one 720×1280 H.264 video stream at 30 FPS with the source frame count, and exactly one AAC audio stream at 48 kHz stereo. It requires positive finite media durations and checks both A/V start-time and end-time drift against the historical D9.2 tolerance of 0.15 seconds. It records both drift values. The muxed AAC is independently scanned for non-silence; mastering measurements alone are not treated as proof that the muxed track is audible.

No new tolerance is introduced. `0.15 s` remains the only A/V start/end drift tolerance. A/B/C existing pilot fixture parameters remain fixed historical test inputs, not production defaults.

## 4. Run protocol

1. Apply this overlay only if all source preimages match the inventory in its manifest. If any live hash differs, stop without patching and reconcile the active checkout.
2. Run the V1.5 Windows runner with Python 3.13, FFmpeg and FFprobe on PATH.
3. Compile the changed modules without writing bytecode into the repository.
4. Run the full discovery suite `test_c11e*.py`, not only the new negative module, because the E3 pipeline changed. Expected inventory: 31 prior tests + 19 new tests = 50.
5. Preserve stdout/stderr, native process exit code, source/postimage hashes, tool versions, test count, duration and immutable receipt in a fresh Documents evidence directory.
6. Stop on the first failed stage. No PASS marker may be emitted after a failure.

This runner does not create a production video or invoke the gameplay renderer. Existing E3 integration tests use temporary test media/output directories. The test suite is not a substitute for the separate GUI operator review already recorded in E3 Pilot V2.

## 5. Offline preparation verification (not Windows acceptance)

- Python syntax compilation: both changed modules passed locally.
- New module: 19 tests discovered; 18 PASS, one deliberate environment skip because the read-only context snapshot does not contain the pinned R4 source MP4. The skipped test is the standalone E3 worker CLI subprocess integration; the Windows checkout runner first verifies that fixture exists with the exact pinned SHA and then treats any skip as a hard failure.
- The actual user-supplied A and C MP4 files from the pilot archive were independently fed to the V1.5 final-mux validator. Both passed: one H.264 High 720×1280/30 FPS/270-frame video stream and one AAC 48 kHz stereo stream, 9.0 seconds, start/end drift 0.0 seconds, and non-silent FFmpeg volume analysis. A and C were each checked; this does not replace the required Windows suite.
- The complete 50-test Windows regression suite has **not** yet been run. No Windows PASS is claimed in this document.

## 6. Acceptance and next gate

- `50/50 PASS`, compile PASS, Python 3.13, FFmpeg/FFprobe detected, postimage pins verified: `E3_NEGATIVE_CONTROLS=PASS`.
- Any test failure: `E3_NEGATIVE_CONTROLS=BLOCKED`, preserve evidence, fix the smallest E3-only defect, version the next overlay, and rerun the full suite.
- On PASS, update the authority and matrix, close E3, and start E4A Challenge presentation/layout/editorial integration.

This overlay grants no renderer authority, production release authority, baseline promotion or freeze eligibility.
