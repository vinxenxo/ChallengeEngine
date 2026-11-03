# C11-E E3 Challenge Audio Pilot — V2

**Date:** 2026-11-03  
**Scope:** E3 test-only audiovisual attachment to the accepted E2 R4 `CHALLENGE_001` video.  
**Status:** `PASS_TECHNICAL_AND_OPERATOR_REVIEW; E3_NEGATIVE_CONTROLS_PENDING`

## 1. Immutable input and run identity

- Input video: `tools/c11e/e3/fixtures/CHALLENGE_001_R4_A_REVIEW_720.mp4`.
- Input SHA-256: `3d72e52cc7f7f8fc4b32c8719ab9800ba622e6069c7fa956526c108defce1afd`.
- Input size: 195,690 bytes; H.264 720×1280; 270 frames at 30 FPS; 9 seconds; no input audio stream.
- E2 receipt SHA-256: `2f8c355453d8558c6af42aa5da35f603b767726d64ba04f842dc799a2cadef7f`.
- E3 output evidence ZIP: `C11E_E3_AUDIO_PILOT_GUI_20261103_152416_ea61bfbd.zip`.
- ZIP SHA-256: `b696663c704a623715debab7a978c1b41016151778a74214927c8151763da270`.
- Structured E3 receipt SHA-256: `910d600e06dcdb2356f9f787fd0c82d45db203e35b471cd5c7cdba10d6ec5aab`.
- Execution origin: `PRODUCER_GUI_QPROCESS`; `operator_gui_invoked=true`.
- No Godot/render invocation and no gameplay rerender.

## 2. Physical result

The run generated A/B repeat audio using music seed `840001`, and C using changed music seed `840002`. All other music request inputs remained fixed. The raw WAVs, 30-second D3.3 mastering windows, final 9-second PCM masters, FFmpeg command records, FFprobe JSON, decoded audio, H.264 elementary streams, stdout/stderr and exit-code records are present in the run package.

- Raw WAV A/B SHA-256: `8acf42204bb535c3882b2e24c984779a122d9a1921cf58f7a2c63084b7631908`.
- Raw WAV C SHA-256: `7ebe776abb85ee6ae648ae320b7335140d69068bf9c38c77520e25987b28f569`.
- Final 9-second PCM master A/B SHA-256: `c91ce88a97209969c7008f449f9d7aa66be32c69809c8a4f1328593c6749aabd`.
- Final 9-second PCM master C SHA-256: `0d491b2b54d0bc5f6707e3935418d5effa7ddbff0582228794c226196499353d`.
- Decoded AAC A/B SHA-256: `332383deeeffad7b7931678cb9e61184191d6c2007c8e365ac916b7913e3c99e`.
- Decoded AAC C SHA-256: `077e0233ef38bfdc847c30d17d24d20b99bb16cf9c1f2cdd3294bc7e1606e5b5`.
- H.264 video elementary-stream SHA-256 for source and A/B/C: `7b1deea4ee10fdc6f9b96d57d93e1a82826b54ed38bec9835f12fc280e90c8fd`.
- Final A/B/C MP4s each contain one H.264 video stream and one AAC audio stream; 720×1280; 270 frames; 30 FPS; 9 seconds; 48 kHz stereo; reported A/V duration drift 0.0 seconds.
- A/B repeatability passed; changed music seed changed only audio. Gameplay seed remained source provenance and was not used to rerender gameplay.
- True peak measured at approximately -5.7 dBFS; `-1 dBFS` is the ceiling, not a requirement to hit exactly.

The receipt above is the authoritative exact source for all output hashes. In case of any discrepancy with this summary, retain the receipt and reopen the discrepancy rather than rewriting historical evidence.

## 3. Operator review

On 2026-11-03 the operator confirmed that both distinct outputs — `CHALLENGE_001_R4_AUDIO_A.mp4` and `CHALLENGE_001_R4_AUDIO_C_CHANGED_MUSIC_SEED.mp4` — are the expected results and have no defects in audio or rendering. B is byte-identical in its tested audio/master result to A and was not required as a separate listening case.

**Human review:** `PASS_USER_CONFIRMED`. This confirmation is limited to the reviewed E3 audiovisual outputs. It does not certify full Challenge editorial/layout coverage, Loop, Drill, the full test matrix, C11-E baseline freeze or release promotion.

## 4. GUI / CLI development clarification

The GUI execution proved that the existing low-fidelity Producer surface prepares the canonical E1 intent and starts the E3 Python worker through `QProcess`. This is not a requirement to implement every development step first inside the GUI.

During this engineering phase:

1. Implement and exercise the reusable scripts/service through CLI first where practical.
2. Keep the same runner independently executable from CLI for automated/manual development tests.
3. Expose the same work through the current low-fidelity Producer GUI as a thin dispatcher to those scripts; do not duplicate business logic.
4. Test both paths and compare semantic request/result/receipt identity where applicable.

The later GUI-only operating model belongs to the future phase after the D/E baseline replaces C and the new production GUI is built. It does not remove the CLI compatibility/test route from current development.

## 5. Remaining E3 acceptance

The physical pilot, GUI dispatch and user audio/render review are accepted. The remaining E3 item is the V1.5 negative-control/regression overlay. It adds explicit checks for final mux stream cardinality, H.264/AAC identity, 48 kHz stereo, non-silence, timing/start/end drift, corrupt media/FFprobe failure and fail-closed E1/source cases. Because it changes the E3 output validator, the full C11-E discovery suite must be rerun on Windows (31 previously accepted tests plus 19 new tests (including the standalone CLI worker), expected total 50).

E3 stays open until this regression result is accepted. E4A Challenge begins only after the V1.5 Windows run is PASS.

`release_authority=NONE`; `baseline_promotion=false`; C11-C 2.19.12 remains authoritative.
