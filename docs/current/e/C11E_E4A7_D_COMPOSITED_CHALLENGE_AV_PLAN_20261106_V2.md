# C11-E E4A.7 — D-Composited Challenge A/V Plan and Post-Run Disposition — V2

**Date:** 2026-11-06. Runtime worker reports `PASS_TEST_ONLY`; full evidence archive audit and human review remain pending.

## Immutable source video

Use only `artifacts/tests/c11e/e4a6_reserved_bands_black/RECOVERY_V1_2/CHALLENGE_004_D_BLACK_BANDS_720x1280_30FPS_SILENT.mp4`, 671,647 bytes, SHA-256 `841b03531301c7e70c0e09ce3e9f536241d2072a87792e099ed7a955bef8c52f`. It is H.264 High / 720×1280 / 30 FPS / 450 frames / 15 s / yuv420p TV range / no audio. Do not rerender, decode/re-encode, or otherwise alter the H.264 bitstream; all muxes must use `-c:v copy`.

## Windows run result

The PowerShell wrapper completed on 2026-11-06 with PS 5.1.26100.9818 AST PASS, Python worker exit 0, `timed_out=false`, stdout 872 bytes, stderr 0 bytes and final marker `C11E_E4A7_D_COMPOSITED_CHALLENGE_AV=PASS_TEST_ONLY_D3V5_D33_MUX`.

Wrapper ZIP SHA: `2a2c7be634e0d74d12b91f1ab74f850910f4d5dc77f545bda981903f06bd38ee`. Worker SHA: `52c20df87dcca747295a2c513cded1e43bdf06740b24a115c9ce71f5aedbc238`. Reported child run ZIP SHA: `ad4024cc6caa3b9140a284390b852c76f3dcd5d50d88cf03813d6bb4e374d293`. Reported worker receipt SHA: `102cf07a0b8920318c3ba211a3bd4374c3e080018486363d701f81e65613aaa0`.

The uploaded wrapper does not include the child run ZIP. Until it is uploaded and independently checked, classify detailed artifact audit as `PENDING_CHILD_ARCHIVE`; do not claim that numerical FFprobe/loudness/drift/hash measurements have been reviewed here.

## Assertions the worker reports passing

1. E1 A/B/C intents are preparation-only, Challenge hook/countdown explicit, audio enabled, independent gameplay/music seed domains, dispatch false.
2. D3 V5 raw A/B WAV and parameter hashes match; changed music seed C produces different raw WAV.
3. D3.3 30-second mastering and mono QA pass for all cases; case-specific mono artefacts are preserved separately; 15-second delivery WAVs are PCM S16LE / 48 kHz / stereo and non-silent.
4. A/B/C muxes contain exactly one H.264 video and one AAC audio stream; AAC-LC / 192 kbps / 48 kHz / stereo; 720×1280 / 30 FPS / 450 frames / 15 s.
5. H.264 elementary stream hashes equal the source for all outputs; decoded AAC A=B and C differs; A/V start/end drift each <=0.15 s.

These are the worker's fail-closed assertions, not figures independently transcribed from the child receipt yet.

## Fixtures and source pins

Challenge `CHALLENGE_004`, `REVIEW_720`, `social_default_v1`, gameplay seed 314159, music seeds A/B 840001 and C 840002, variation 0, hook/countdown true. Tempo 104 BPM is the historical D9.2 fixture, not a product default. Duration is FFprobe-derived 15 s. E1 source intent remains preparation-only; D3 is invoked explicitly as a separate TEST operation.

Current E1 service pin is `348997e575d985fe153a4f433f089c5f205be5d4d8f3853baf07be917a134951`; old E4A.4 pin `f0655d8...` is obsolete. Other source pins are in Authority V69 and source-pin reconciliation V1. No Git/HEAD/status checks.

## Required closeout

- Upload and verify child ZIP `RUN_20261106T070808Z-62F31F9C.zip` from `artifacts/tests/c11e/e4a_d_composited_av_review/`; expected SHA `ad4024cc6caa3b9140a284390b852c76f3dcd5d50d88cf03813d6bb4e374d293`.
- Operator listening review A/B/C and A/V sync: PENDING.
- E1 GUI/CLI parity through existing D9.9/D9.10 surface: PENDING.
- Full E4A acceptance: OPEN until all above pass.

No renderer, production dispatch or production media. `release_authority=NONE`.
