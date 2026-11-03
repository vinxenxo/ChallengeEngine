# C11-E E3 Execution Backlog — V3

**Date:** 2026-11-03  
**Status:** GUI runtime + physical Challenge audio pilot + operator review PASS; negative controls/regression V1.5 pending.

## Accepted, do not repeat

- E3.2 D3 V5/E1 contract and source binding.
- V1.3 implementation overlay: 10/10 postimages previously verified.
- V1.4 Windows compile/tests: 31/31 PASS; Python 3.13.14; PySide6 6.11.2.
- Existing Producer GUI launched from the active entry point; E3 control invoked the worker through `QProcess` after preparing E1 intent.
- E1 GUI/CLI semantic parity PASS; CLI uses the shared service and is retained as a separate-process development/test route.
- Physical CH001 R4 audio pilot PASS; full receipt and sidecar hashes independently verified; no gameplay render/rerender.
- Operator confirmed A and C are the expected outputs without audio/render defects; B is the repeated A case.

## Development execution clarification

Implement and exercise scripts/service through CLI first where practical. Then connect the same scripts to the current low-fidelity Producer GUI as a thin dispatcher. Maintain both CLI and GUI execution/testing during development. The future GUI-only operating mode applies after the D/E baseline replaces C and the new GUI exists. Do not duplicate business logic in the GUI.

## Immediate next gate — E3 negative controls V1.5

Apply `C11E_E3_NEGATIVE_CONTROLS_OVERLAY_V1_5.zip`, with strict preimage hash check. It adds `_validate_mux_probe()` to the E3 pipeline and independently validates the muxed AAC for non-silence.

New coverage (19 tests):
- Valid final mux metadata.
- Missing video/audio and multiple video/audio streams.
- Zero/negative/malformed duration.
- Wrong H.264/AAC codec, video dimensions/frame rate/frame count, sample rate and channel layout.
- Truncated audio and excessive start/end drift.
- Invalid gameplay/music seeds.
- Missing/unsupported style profile and missing R4 source.
- Silent audio, corrupt MP4, FFprobe process failure.
- Existing output collision without overwriting evidence.

Offline preparation has compiled both modified Python modules, run the new module (18 PASS, one environment skip because the context snapshot omits the immutable R4 source fixture), and validated both actual A/C pilot MP4s against the new stream/timing/non-silence validator. This is not Windows acceptance. Because the production validator changes, rerun the full C11-E discovery suite on Windows. Expected: 31 existing + 19 new = 50 tests with zero skips. The runner verifies the exact R4 fixture and fails closed otherwise. Capture Python 3.13, FFmpeg/FFprobe versions, compile result, native exit code, stdout/stderr hashes, full test transcript, all relevant postimage hashes and a structured receipt in a fresh Documents folder. No gameplay render/rerender. Do not repeat the prior physical GUI pilot.

## E3 exit

On `50/50 PASS`, compile PASS and all postimage pins verified, record E3 negative controls PASS and formally close E3. If any failure, stop on first failure, retain output and prepare the smallest versioned E3-only correction. No PASS marker after failure.

## Next phases

- **E4A Challenge:** implement/validate the full Challenge visual presentation/layout/editorial consumer against the existing C generators; apply Challenge D3 V5 audio through the established E3 mux/QC contract. CLI-first script/service, then same implementation exposed by current Producer GUI.
- **E4B Visual Loop:** connect grammar/variant-specific timeline and editorial/layout binding; preserve existing C11-C Loop music path through an audio-only E adapter.
- **E4C Visual Drill:** connect phase mapping, countdown and END_CTA precedence; preserve existing C11-C Drill music path through an audio-only E adapter.
- **E5:** cross-family determinism, independent gameplay/music seeds, no adapter/profile leakage, and both CLI and GUI paths.
- **E6:** Smoke18, six audiovisual scenarios per family.
- **E7:** Matrix101: 54 Challenge + 27 Loop + 20 Drill; CH_008/009 held because declared 11s conflicts with 12s phase sum (3+7+0+2), so provisional runnable total 99.
- **E8:** independent acceptance, immutable freeze, explicit promotion authority.

Before E8, map every historical C11-C visual/review case (including the existing 27 review cases and 9 Challenge cases plus all other test categories) into a row-level E test disposition. Every Challenge, Loop and Drill variant must receive the D editorial/layout/audio layers that apply to its family. No untested case can be assumed covered by Smoke18.

C11-C 2.19.12 stays authoritative; release authority NONE; no freeze or promotion.
