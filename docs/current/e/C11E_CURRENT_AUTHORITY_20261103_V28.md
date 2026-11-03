# C11-E Current Authority — V28

**Date:** 2026-11-03  
**Authority:** active Windows checkout only. This revision records the E3 V1.5 recovery receipt and corrects the failed E4A discovery tooling; it does not authorize production promotion.

## 1. Product mission and development workflow

One C11-E production service for Challenge, Visual Loop and Visual Drill. Preserve C11-C generators/mechanics and existing family audio implementations. Add the currently authorized D presentation/layout and scoped editorial values, family-correct audio, FFmpeg mux, FFprobe/audio QA and immutable run receipts.

Implement the reusable service/worker through CLI first where practical, then wire the same implementation into the current low-fidelity Producer GUI as a dispatcher. Both CLI and GUI execution/testing remain required during engineering. A future workflow where generation is done entirely through a new GUI applies only after the D/E baseline replaces C; CLI remains available for CI/compatibility.

## 2. Accepted evidence

- E0, E1, bounded E2 R4, E3.2, V1.3/V1.4 and the E3 CH001 R4 audio/mux pilot remain accepted within their declared scopes.
- E3 pilot receipt SHA-256: `910d600e06dcdb2356f9f787fd0c82d45db203e35b471cd5c7cdba10d6ec5aab`. Operator confirmed A and C are the expected audiovisual results and defect-free; B repeats A.
- E3 V1.5 pipeline postimage: `46b087683a3dcb460601c925373b84e390999d44d73141328285e6c8a633ba5d`.
- E3 V1.5 negative-control test module postimage: `f88e2a52ad32851de9c47526aaf1159e7814f96b2e33f8a857e0c1df6ef3512b`.
- Windows V1.5 run: source pins/preflight PASS; Python 3.13, FFmpeg and FFprobe exit 0; `py_compile=0`; full C11-E discovery exit 0; runner assertions reached exactly 50 tests, zero skips and `OK` before a later evidence-inventory error.
- V1.5 recovery script completed with `C11E_E3_NEGATIVE_CONTROLS_V1_5_RECOVERY=PASS`; supplemental receipt SHA-256 `8e01946da3de35c05430335259a88e14f5bae1b660c6896de5d8f13c37c3fafe`. The recovery validated stored logs/pins and did not rerun tests or media.

## 3. E3 formal closure

`E3=PASS_FORMALLY_CLOSED_TEST_ONLY`. The test suite passed 50/50 with zero skips. Original runner status `BLOCKED` is preserved as an evidence-packaging defect: V1.5 attempted to hash `runner_transcript.log` while `Start-Transcript` still held it open, after all test assertions had passed. The supplemental recovery receipt is the closure evidence. No gameplay renderer, rerender or production-media generation was performed by recovery.

## 4. E4A discovery incident and correction

The first read-only source discovery script V1 returned `Los tipos de argumentos no coinciden` and emitted no PASS. The failure is attributed to its PowerShell 5.1 collection/pattern handling pending successful V2 execution; V2 avoids generic collection method binding and multi-pattern invocation, uses simple arrays and one Select-String pattern per call, and records exception type, script line and stack trace on failure.

The V1 documentation apply script was also blocked before writes because its manifest contained a truncated expected SHA for V26 authority (`...fed1`); the observed complete hash is `c4bc1bb8b62b64d3b60685b30428c47adfff6ecbfd53826647c0184aa91fed1a`. V2 fixes the pin and uses strict add-only preimage/postimage classification.

`E4A.0=DISCOVERY_PENDING_V2`. No E4A production source modification is authorized until V2 discovery passes and identifies the actual consumer, slot contract, CLI call and GUI dispatch callback.

## 5. E4A implementation target

Reuse the existing Challenge consumer/binder; do not create a parallel binder, second renderer or producer. Trace the request/editorial data through E1, D9 bridge/adapter and the existing visual consumer into pixels. Confirm the live D contract before enabling fields. Candidate fields: `title`, `subtitle`, `call_to_action`, `language` (metadata-only), and Challenge-specific `player_name`, `challenge_label`. Reserved hook/preparation/final/header/footer fields and visibility switches remain disabled. Never map title to hook or CTA. Do not serialize all `FrameSnapshot.custom_data`.

Use Challenge's D3 V5 profile/music seed through the accepted E3 mux/QC boundary. CLI first where practical; connect the same worker/service to the current Producer GUI and test both.

## 6. Full family and historical coverage

- E4A Challenge, E4B Visual Loop, E4C Visual Drill.
- E5 three-family determinism, independent gameplay/music seed domains, family/profile non-leakage and CLI/GUI parity.
- E6 Smoke18: six audiovisual cases per family.
- E7 Matrix101: 54 Challenge + 27 Loop + 20 Drill; CH_008/009 held until the 11-second declared duration versus 12-second phase sum (3+7+0+2) is authority-corrected; 99 provisional runnable cases.
- Before E8, map every historical C11-C production/review/test case row by row, including the 27 review cases, 9 Challenge cases and all remaining visual categories. Smoke18 and Matrix101 do not replace historic coverage.
- E8 independent acceptance, immutable freeze and separate explicit production promotion.

Every applicable row must capture visual source/family/variant, editorial fields, layout/presentation profile, correct family audio, gameplay and music seeds, output receipt, FFprobe/audio QA, determinism/repeat status and CLI/GUI path coverage.

## 7. Governance

C11-C 2.19.12 remains the sole production baseline. Frozen manifest: 796,318 bytes; SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.

`release_authority=NONE`  
`baseline_promotion=false`  
`freeze_eligible=false`
