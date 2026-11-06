# C11-E Current Authority — V68

**Date:** 2026-11-06. This authority supersedes V67 for the current execution point. It records the successful Recovery V1.2 receipt and the preparation of the next D-composited A/V test. It does not change any production, governance, or promotion lock.

## Active checkout and immutable baseline

The sole code authority is `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`. Never extract snapshots/evidence ZIPs over it. The operator commits each iteration. **No iteration runner may invoke Git, inspect `HEAD`/status, require `.git`, compare commit IDs, or record Git state.** Exact source-file SHA-256 pins and the C11-C frozen manifest remain mandatory.

C11-C 2.19.12 remains frozen. `release/C11C_FREEZE_PACKAGE_MANIFEST.json`: 796,318 bytes; SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.

## E4A.6 — visual/reserved-band subgate

<badge>PASS_TEST_ONLY</badge>

Recovery V1.2 was executed successfully on Windows PowerShell 5.1.26100.9818. Recovery receipt SHA-256: `3279011fa16479d4901c5b271463707a437ce7458d306c1667ab222cb1603980` (`C11E_E4A6_RESERVED_BANDS_BLACK_RECOVERY_V1_2_RECEIPT.json`, 2026-11-06 00:04:50 +01:00).

- Reused the V2 evidence: Python focused tests 22/22 PASS; Godot 4.7.1 editor import PASS; live-root 900 frames / one mount / 900 black-band frames; Movie Maker capture 900 frames, 540×960, 60 FPS, 15 s. Recovery did not rerun any of them.
- FFmpeg/FFprobe 9.0. AVI SHA-256 `2f6d0c73cb09571584db68e37760c933706473a07e559fc93113f26eabb89f45`; its incidental PCM S16LE 48 kHz stereo stream was discarded.
- D-composited silent review MP4: `artifacts/tests/c11e/e4a6_reserved_bands_black/RECOVERY_V1_2/CHALLENGE_004_D_BLACK_BANDS_720x1280_30FPS_SILENT.mp4`; 671,647 bytes; SHA-256 `841b03531301c7e70c0e09ce3e9f536241d2072a87792e099ed7a955bef8c52f`; H.264 High, 720×1280, 30 FPS, 450 frames, 15 s, yuv420p, TV range, zero audio streams.
- Eight delivery stills: frames 0, 89, 90, 299, 300, 389, 390, 449. Inactive reserved-band audit: 12/12 PASS, 31,680 samples per region/frame, zero non-black samples; the automated black tolerance permits maximum RGB 3. Active HOOK/HEADER and CTA/FOOTER audit: 4/4 PASS.
- The operator explicitly confirmed visual inspection PASS on 2026-11-06. This is approval of this test output; it is not a blanket D1.5/layout policy or production promotion authorization.
- Contact sheet SHA-256 `f45c911e97194020d0487ad6d8f22e3bb3370b15a87d8cd6d5e2884e7f61d4af`.

The V2 overall BLOCKED was a wrapper false-negative: a path-based Movie Maker log helper received stdout text. Recovery V1 failed on a stale Git HEAD gate; that gate is permanently retired. V1.1 failed because of a non-self-contained docs manifest; V1.2 fixed it by embedding and hash-verifying the documentation package. Keep all four incident records; do not rerun the visual capture, 22 tests, Godot, Movie Maker, or V1.2 absent concrete source drift/new defect.

The optional D envelope keeps HEADER (logical y=0..144) and FOOTER (y=816..960) black when inactive/empty. Title/subtitle remain HOOK/HEADER only; CTA remains CTA/FOOTER only. BODY and no-envelope legacy C behavior are preserved. The video/body background colour is not a blocker; user-selectable body background remains a separate future editorial feature. Never relax the reserved black-band invariant.

## Protected source pins

- Active D-only `GeneradorMaestro.gd`: `d42782e8f5bb94ff0ede653a1c4624dc91541cc8203abf136b09a8fc288a7d82` (not the frozen-manifest preimage). Do not edit or restore it blindly.
- Frozen `core/presentation/C11CVisualEditorialLayer.gd`: `f8f718c067a4d7a088cc16f244cc40209e7183bec93e44d8cb66eb6dd404cf7d`.
- D-only `tools/c11d/d9/C11EChallengeLiveEditorialConsumer.gd`: `eba81fff4c24ca75033c8f963665df1961136046c41fee0e88681fe55a631203`.
- Focused V2 test pin: `9845eda094037f8748493171755b32d3479ddf6548612e9a6ecebba187cbc512`.
- Recovery envelope pin: `2a62637072d34f2b68e11f92ddb1d7d981d870507e696c800396a8e15f8a527e`.

No source writes were made by Recovery V1.2. The visual consumer remains D-owned; no C11-C shared layer or C mechanics are changed.

## E4A.7 — D-composited Challenge A/V test (ready for execution; final outcome is governed by the runtime receipt)

The next increment is `RUN_C11E_E4A7_D_COMPOSITED_CHALLENGE_AV_V1.ps1`, a test-only D3 V5 / D3.3 / mux review. Its exact input is the Recovery V1.2 silent MP4 above. It must **not** re-render, re-encode, or alter the visual H.264 stream. FFmpeg mux uses `-c:v copy` and only adds D3-generated audio.

### Reconciled source pins

Latest reviewed E4A5B source snapshot pins:

- E1 service `c11c-suite/c11c-producer/c11e_production_service.py`: `348997e575d985fe153a4f433f089c5f205be5d4d8f3853baf07be917a134951` (current reviewed service, schema 1.1 / service 0.2.0-E3.2). The older E4A.4 E1 pin `f0655d8d93df3b766b157d80a76a5bfc7b514d740815646f54c88ca788f602c0` is historical and must not be used for this iteration.
- D9 resolver: `9ad2adbf54946f2225ae2ed36b88abfc5717387f2ff03bbed684aa8bd32d87d1`.
- D9 editorial model: `5c575be1942ba0613d66579d14db5cf9d7786e7062dfb001bd7be8a2e9c18ae5`.
- GUI request adapter: `0e95109ffd3ba5655d28292309196349470ab7958a467f096543a2c98c22976e`.
- E3 audio pipeline: `46b087683a3dcb460601c925373b84e390999d44d73141328285e6c8a633ba5d`.
- D3 V5 engine: `03ae7e2997796e0c67ca15c8886b1e5b290791a142b6631a572d1cba6eba4eb1`.
- D3 V5 spec: `8970f4e93c878285b727697f3d269f5ee464b6029fe79eabc5fcbf4245e9dbf2`.
- Challenge 8-bit style profile: `0c877cbe6e1c288890da31fc4481a58e1051749b45a50b2290cbef5d1120d2de`.
- E1 music contract: `12c59ce2a2135a49ce0d5968a29905a1e5890743507db1ee0039da1374efcfe8`.
- Approved Challenge policy: `764629384896a255cf992da89fa427c19f60f9b2e623b81ad17d909674b466b5`.

The E4A.7 runner independently verifies all pins against the live checkout before any music render. If any SHA differs, it stops before audio generation; do not replace a pin without reviewing the live source and documenting why. It never queries Git.

### Test fixture and acceptance predicates

- New E1 TEST intents use `CHALLENGE_004`, `REVIEW_720`, audio enabled, explicit `presentation_options.show_hook_countdown=true`, gameplay seed 314159, music seeds A/B=840001 and C=840002, variation index 0. These are historical test fixtures, not product defaults.
- E1 contract leaves `tempo_bpm` and `duration_seconds` unresolved. For this isolated test only, tempo 104 BPM is explicitly identified as the historical D9.2 audio-pilot fixture; duration is derived from the MP4's FFprobe result (450 frames / 30 FPS = 15 s). Do not patch E1 or infer a production tempo default.
- Prove raw D3 A/B WAV equality and C difference; D3.3 mastered A/B equality and C difference; 30-second loudness QA at -14 LUFS / -1 dBTP / LRA 7, no clipping and mono audibility; delivery WAV 48 kHz stereo / 15 s.
- Mux one H.264 video + one AAC-LC audio stream (192 kbps, 48 kHz stereo), non-silent; exact 15-second source video, 450 frames, 30 FPS, A/V start/end drift <=0.15 s. Require the muxed H.264 elementary stream SHA to equal the silent D-composited source bitstream for A/B/C. Require decoded AAC A=B and C differs.
- No gameplay rerender, no D renderer, no production dispatch/media. All outputs remain test evidence. Operator listening review and E1 GUI/CLI parity remain necessary before full E4A can close.

## Gate state

- E4A.6 visual/reserved-band: `PASS_TEST_ONLY`.
- E4A.7 D-composited D3 A/V: `READY_FOR_EXECUTION_RECEIPT_GOVERNED`.
- Full Challenge E4A: `IN_PROGRESS`; do not mark closed until A/V results, operator listening review and GUI/CLI parity are accepted.
- E4B Loop and E4C Drill remain on hold until full E4A closes. Then E5, E6 Smoke18, E7 Matrix101 and E8 remain ordered.
- CH_008/009 remain held because 11 s declared duration conflicts with 12 s phase sum.

## Governance locks

C11-C 2.19.12 remains the only production authority. Renderer OFF; production dispatch OFF; production media OFF; D4.8 BLOCKED; D9.10 PREPARE_ONLY; D9.14/D9.16 BLOCKED; D9.17 BLOCKED_NO_GO; D10 BLOCKED_FOR_PROMOTION; `release_authority=NONE`. No sixth module, second Producer, parallel binder, change to protected C mechanics/RNG/timeline, or commit manipulation by runners.
