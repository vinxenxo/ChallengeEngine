# C11-E Current Authority — V26

**Date:** 2026-11-03  
**Authority source:** active Windows checkout remains authoritative; the 2026-11-03 V25 snapshot is context only.  
**Purpose of this revision:** record E3 GUI/audio pilot completion and operator review; clarify the development CLI/GUI sequence; authorize the next bounded E3 QA overlay only.

## 1. Product objective

Deliver one C11-E production system for Challenge, Visual Loop and Visual Drill. Preserve existing C11-C visual generators/mechanics and existing family audio implementations. Add the approved D presentation/layout, enabled family-specific editorial values, correct family audio path, FFmpeg mux, FFprobe/audio QA and immutable E run receipts.

Do not modify `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector`, `RenderedFrameStream`, protected C11-C generators/mechanics, `core/audio`, canonical content definitions, D4.8/D9.10 locks or the frozen C11-C manifest. No second producer, parallel binder, sixth suite module or `c11d-control`.

## 2. Development execution contract — clarified 2026-11-03

The previous wording that treated GUI as the only human-operated path during every development step is superseded by the operator's clarification.

**During development:**

1. Implement and validate the shared scripts/service through CLI first where practical. This is the fastest reproducible route for engineering and automated tests.
2. Keep those scripts independently executable from CLI for development runs, automated acceptance and compatibility.
3. Bring the exact same scripts/service into the current low-fidelity Producer GUI. The GUI dispatches the already-built script/worker; business logic must not be duplicated in GUI callbacks.
4. Test both execution paths. GUI-origin and CLI-origin metadata may differ, but canonical request, editorial, seed, adapter and result semantics must agree.
5. A GUI test must not be mistaken for proof that development must happen GUI-first. Conversely, CLI success alone does not prove GUI dispatch works.

**Later target after the D/E baseline replaces C:** build the new production GUI and move normal human production fully into that GUI. That is a future operating-model gate; it does not remove CLI support from this engineering phase or the automated compatibility route.

The current Producer GUI E3 pilot did run the worker via `QProcess`, after preparing a canonical E1 intent. The same `c11e_e3_audio_pilot.py` worker remains a standalone CLI script (`--root`, `--intent`, `--source-video`, `--source-receipt`, `--source-receipt-sha256`, `--output-root`); `--operator-gui` is provenance only.

## 3. Accepted evidence as of this revision

### E0 / E1 / E2 / E3.2

- E0: accepted; do not repeat.
- E1: shared GUI/CLI preparation service accepted. Separate-process CLI compatibility test is part of the accepted test suite. E1 remains preparation-only and does not dispatch a renderer.
- E2: bounded CH001 title-to-pixels R4 A/B control formally closed. It is not family-wide acceptance.
- E3.2: D3 V5 planning contract bound to E1 intent; contract and source pins remain accepted.

### E3 V1.3 / V1.4

- V1.3 code overlay applied: 10/10 postimages previously verified; do not reapply.
- V1.4 Windows suite: 31/31 tests PASS, Python 3.13.14 compile PASS, PySide6 6.11.2. Do not rerun unless code/test pins change. They will change in V1.5, so V1.5 explicitly reruns the complete suite.

### E3-GUI-01 and physical audiovisual pilot

- Actual existing Producer GUI entry point launched successfully.
- E3 action was visible inside the existing universal editorial surface; it prepared E1 intent and launched the E3 worker with `QProcess`.
- E1 GUI/CLI semantic parity preflight PASS; the CLI compatibility adapter remains in place.
- Pilot run: `C11E_E3_AUDIO_PILOT_GUI_20261103_152416_ea61bfbd.zip`.
- ZIP SHA-256: `b696663c704a623715debab7a978c1b41016151778a74214927c8151763da270`.
- Receipt SHA-256: `910d600e06dcdb2356f9f787fd0c82d45db203e35b471cd5c7cdba10d6ec5aab`.
- Receipt status: `PASS_E3_CHALLENGE_AUDIO_PILOT_TEST_ONLY`; execution origin `PRODUCER_GUI_QPROCESS`; `operator_gui_invoked=true`.
- Independent archive inspection: 223 entries, 49 exit-code records all zero; 21 stderr streams were diagnostic FFmpeg output; no error/fatal indicators in those logs. Receipt SHA matches sidecar.
- A/B repeat music seed 840001; C changed music seed 840002. Same-seed raw WAV/master/decoded AAC repeatability passed; changed music seed changed audio only. H.264 stream remained identical to the R4 source across A/B/C.
- Final A/B/C: H.264 High 720×1280, 270 frames, 30 FPS, AAC 48 kHz stereo, 9 seconds, A/V duration drift 0.0 seconds.
- No gameplay renderer invocation and no gameplay rerender.
- On 2026-11-03 the operator explicitly confirmed A and C are the expected outputs and have no audio or render defects. B is the repeated A case and did not require another listening check. Human review is `PASS_USER_CONFIRMED` for this bounded pilot only.

## 4. Current gate state

| Gate | State | Notes |
|---|---|---|
| E0 | PASS | Retained |
| E1 | PASS | Shared service; GUI and CLI compatibility semantics |
| E2 | PASS | Bounded CH001 R4 only |
| E3.2 | PASS | D3 V5/E1 binding |
| E3 V1.3 | PASS_APPLIED | Do not reapply |
| E3 V1.4 | PASS_31_OF_31 | Re-run only because V1.5 changes the validator |
| E3-GUI-01 | PASS | Existing GUI runtime + QProcess worker observed |
| E3 audiovisual pilot | PASS | Technical receipt + A/B/C controls + user review |
| E3 negative controls V1.5 | READY_NOT_RUN | Full regression suite required; expected 50/50 |
| E3 formal closure | PENDING_V1_5 | Do not mark closed before Windows evidence |
| E4A Challenge | NOT_STARTED | Starts after E3 V1.5 PASS |
| E4B Loop | NOT_STARTED | After E4A |
| E4C Drill | NOT_STARTED | After E4B |
| E5 cross-family | NOT_STARTED | Determinism/seed isolation/adapters/CLI+GUI paths |
| E6 Smoke18 | NOT_STARTED | 6 per family |
| E7 Matrix101 | NOT_STARTED | 54 Challenge + 27 Loop + 20 Drill; CH_008/009 held |
| E8 | NOT_STARTED | Independent acceptance/freeze/explicit promotion |

## 5. Next action: E3 negative-controls overlay V1.5

Apply `C11E_E3_NEGATIVE_CONTROLS_OVERLAY_V1_5.zip` only if every preimage hash in its manifest matches the live checkout. The overlay modifies only the E3 audio pipeline's final mux validator and adds the new E3 negative-control test module plus versioned documentation.

The new validator enforces exactly one H.264 video and one AAC audio stream, 720×1280/30 FPS/source frame count, 48 kHz stereo, positive finite durations, start-time and end-time drift within 0.15 seconds, and non-silent muxed AAC. The tests cover invalid seeds/profile/source, output collision, streams, codec, rate, channels, silence, truncation, drift, corrupt media and FFprobe failure.

Because the E3 pipeline source changes, run the full C11-E test discovery suite in Windows, not just the new module: 31 existing tests + 19 new tests = 50 expected. Use Python 3.13, FFmpeg and FFprobe. Do not run the gameplay renderer or rerender the R4 source.

Offline preparation check: both changed Python modules compile; the new 19-test module reports 18 PASS and one environment skip because the read-only snapshot lacks the R4 source MP4. The actual user-supplied A and C output MP4s both pass the new final-mux validator and FFmpeg non-silence scan (H.264 720×1280/30 FPS/270 frames; AAC 48 kHz stereo; 9.0 seconds; start/end drift 0.0 s). These local checks are not Windows acceptance and do not waive the required 50/50 run. The V1.5 runner checks for the exact R4 fixture and rejects any skips.

On any failed stage, stop, preserve logs and hashes, and do not print PASS. On `50/50 PASS`, update the current authority and formally close E3; the next implementation phase is E4A Challenge presentation/layout/editorial integration.

## 6. Complete test coverage commitment

The eventual acceptance must not stop at the E3 Challenge pilot. Inventory and reconcile the existing C11-C production/review corpus — including the established 27 review cases, 9 Challenge cases and all other historical content/test categories — into a traceable E/Evidence disposition matrix. Do not replace a previously tested case with a small smoke sample.

Required staged coverage:

- E4A/B/C: full family binders/adapters and presentation/editorial/layout timelines.
- E5: three-family request, determinism, gameplay/music seed isolation, family non-leakage, and both CLI and GUI execution paths.
- E6 Smoke18: 6 cases per family.
- E7 Matrix101: 54 Challenge + 27 Visual Loop + 20 Visual Drill. CH_008 and CH_009 remain held until the declared 11-second duration versus 12-second phase sum (3+7+0+2) is authoritatively reconciled. Current provisional runnable total is 99.
- Every matrix row must identify visual source, family/variant, editorial inputs, layout/presentation profile, family audio route/profile, seeds, output receipt, FFprobe/audio QA, determinism/repeat status and CLI/GUI route coverage.

A complete C-equivalent regression review of all historical visual types and presentation states is mandatory before E8. No family, grammar, drill variant, editorial field or layout case may be silently omitted.

## 7. Governance / authority

C11-C 2.19.12 remains the sole production authority. Frozen manifest remains 796,318 bytes / SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.

`release_authority=NONE`  
`baseline_promotion=false`  
`freeze_eligible=false`

E3 pilot PASS is test-only evidence; it does not confer renderer-wide production authority or promote D/E.
