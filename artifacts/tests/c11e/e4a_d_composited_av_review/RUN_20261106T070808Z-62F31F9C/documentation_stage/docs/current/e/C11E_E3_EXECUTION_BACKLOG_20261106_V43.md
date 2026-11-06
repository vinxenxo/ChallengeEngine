# C11-E Execution Backlog — V43

**Date:** 2026-11-06. E4A.6 visual/reserved-band subgate accepted test-only; next work is E4A.7 D-composited Challenge audiovisual review.

## Completed — E4A.6 visual

Recovery V1.2 PASS receipt: SHA-256 `3279011fa16479d4901c5b271463707a437ce7458d306c1667ab222cb1603980`. User visual review PASS. Silent D-composited MP4 SHA `841b03531301c7e70c0e09ce3e9f536241d2072a87792e099ed7a955bef8c52f`, 720×1280 / 30 FPS / 450 frames / 15 s / H.264 High / yuv420p / TV range / zero audio. Pixel audit: inactive reserved-band 12/12 PASS (RGB max tolerance 3); active HOOK/CTA 4/4 PASS. Eight boundary frames reviewed. 22 Python tests, Godot and Movie Maker runtime were reused, not rerun. Do not repeat these tests or render.

## Immediate — E4A.7 D-composited Challenge A/V

Run `RUN_C11E_E4A7_D_COMPOSITED_CHALLENGE_AV_V1.ps1` from Downloads. It contains the Python worker and versioned docs bundle internally; only this `.ps1` is required. No Git commands or state inspection.

Preflight checks exact active source pins and the Recovery V1.2 receipt/MP4/output-still metadata. Important current source pins include E1 service SHA `348997e575d985fe153a4f433f089c5f205be5d4d8f3853baf07be917a134951`, E3 pipeline `46b087683a3dcb460601c925373b84e390999d44d73141328285e6c8a633ba5d`, D3 V5 engine/spec/profile/contract pins recorded in Authority V68 and the E4A.7 plan. Old E4A.4 E1 service pin `f0655d8...` is historical and must not be reused. If any live source SHA differs, stop before audio generation and reconcile; do not weaken pins.

The D-composited input is the exact Recovery V1.2 MP4 at `artifacts/tests/c11e/e4a6_reserved_bands_black/RECOVERY_V1_2/CHALLENGE_004_D_BLACK_BANDS_720x1280_30FPS_SILENT.mp4`. Verify 671,647 bytes and SHA `841b035...`; do not rerender, transcode, or replace it. The worker also validates the recovery receipt SHA, its 8 stills, contact sheet and pixel audit.

### A/V test case

- Prepare three sealed E1 TEST intents for Challenge / CHALLENGE_004 / REVIEW_720, audio enabled, explicit `show_hook_countdown=true`; validate `PASS_E1_PREPARATION_ONLY` and `dispatch_authorized=false`.
- Historical fixture seeds: gameplay 314159 constant; music A/B 840001; C 840002; variation index 0. Reuse only as test fixtures, not defaults.
- D3 V5 renders three raw WAVs. Require A/B identical output/parameter hashes; C differs.
- E1 still reports `tempo_bpm` and `duration_seconds` as unresolved. For this test only, use 104 BPM as the historical D9.2 pilot fixture and duration 15 s derived by FFprobe from 450 frames / 30 FPS. Do not change E1, D3 profile, or create a product default.
- D3.3: deterministic 30-second looped QA window, loudnorm -14 LUFS / -1 dBTP / LRA 7, no clipping, audible mono compatibility; trim delivery WAV to 15 seconds / PCM S16LE / 48 kHz stereo. Require A/B equality and C difference.
- Mux AAC-LC 192 kbps / 48 kHz / stereo. Use `-c:v copy`; require one H.264 video and one AAC audio stream, H.264 bitstream SHA identical to the Recovery V1.2 source across all A/B/C, non-silent audio, 15 seconds, 450 frames, 30 FPS, start/end A/V drift <=0.15 s. Decoded AAC A=B; C differs.
- Preserve raw/mastered/delivery WAVs, A/B/C MP4s, FFprobe JSON, volumedetect/EBUR128 reports, process commands/stdout/stderr/exit codes, H.264 extractions, decoded audio hashes, SHA256SUMS, report and receipt. Test media only.

The E4A.7 worker does not make an E4A production acceptance claim. After it passes, the operator must listen to A/B/C and review sync. E1 GUI/CLI parity must then be recorded through the shared E1 service. Full E4A closes only after both human audio disposition and GUI/CLI parity are accepted.

## Then — family campaign

After full E4A: E4B Loop (retain C11-C grammar, variant timeline, binder and current family music); E4C Drill (retain phase timeline, binder, END_CTA precedence and current family music); E5 cross-family determinism, independent gameplay/music seed, adapter/profile non-leakage and GUI/CLI parity; E6 Smoke18 (six full A/V cases per family); E7 Matrix101 (54 Challenge + 27 Loop + 20 Drill); E8 historical C→E regression map, independent acceptance, immutable freeze and separate explicit promotion.

CH_008/009 remain held because declared 11 seconds conflicts with phase sum 12 seconds. Do not call Matrix101 complete while they remain unresolved.

## Do not repeat / governance

Do not repeat E4A.2/.3/.4/.5B/.6 accepted captures, V2 22-test suite, Godot, Movie Maker or Recovery V1.2. No Git checks. Do not modify `GeneradorMaestro.gd`, C11-C shared layer, C generators/mechanics, RNG, simulation truth, timelines, binders or core audio. C11-C 2.19.12 remains production authority; renderer/dispatch/production media OFF; `release_authority=NONE`.
