# C11-E E4A.4 — Challenge audiovisual/mux review plan V1

**State:** PREPARED_NOT_RUN  
**Target:** CHALLENGE_004, isolated review-only output  
**Inputs:** accepted E4A.2 normalized video and accepted E4A.3 compositor evidence  
**Execution:** test harness only; no production dispatch or renderer

## Why this is the next bounded step

E4A.3 proves the D-owned Godot layer can composite over real C11-C sample frames. Its visual placement is not approved: the test title/subtitle collides with existing C11-C hook text, and CTA collides with existing footer text. E4A.4 therefore validates the independent D3 V5/audio/mux seam on the previously accepted 15-second normalized C11-C video, without pretending the E4A.3 PNGs have been turned into a fullframe D video.

## Source and timing contract

Input: `artifacts/tests/c11e/e4a_real_body_pixel_review/RUN_20261104_002559_542bcf60/review_delivery/CHALLENGE_004_REVIEW_720_30FPS_TEST_ONLY.mp4`

- SHA-256 `edbd446d67142d20e138e55563f16cbae8d9a4c39469fd2bebcb3c9d5723fb9e`
- H.264, 720x1280, `yuv420p`, 30 FPS, 450 frames, 15 seconds; no audio stream.
- Original C11-C source video SHA `fdd0598e20ddc6201e54cc2dad7fd3362c2ef80961df44f3ef4676fb97a765de`; do not rerun its generator.
- Gameplay seed `314159` is retained across all three E1 intents; music seeds A/B `840001`, C `840002`; domains remain independent.

## Execution method

1. Verify E4A.2 and E4A.3 receipt/report exact SHA pins and their cross-lineage.
2. Verify E1 service, D9 resolver, D3 V5, its spec/profile/contract, E3 pipeline and approved editorial policy pins. Verify the frozen C11-C manifest.
3. Prepare three sealed E1 TEST intents through `prepare_c11e_production_intent`; require `audio_enabled=true`, E1 validation PASS, `PLANNED_NOT_RENDERED`, dispatch false, and exact independent seed identities.
4. Invoke the pinned D3 V5 engine for A/B/C. Use 104 BPM only as the historic D9.2 pilot fixture; derive duration from FFprobe. Preserve raw WAVs and their hashes.
5. Apply the previously accepted D3.3 30-second measurement/mastering method, trim delivery masters to 15 seconds, and require PCM S16LE/48 kHz/stereo, loudness [-18,-12] LUFS, true peak <= -1 dBFS, no hard clipping, mono audibility and non-silence.
6. Mux with H.264 video stream copy and AAC 192 kbit/s / 48 kHz / stereo; validate exactly one H.264 video and one AAC audio stream, 720x1280/30 FPS/450 frames, positive duration, non-silence and A/V start/end drift <=0.15 seconds.
7. Prove input/output H.264 elementary stream identity; decoded AAC A/B identity and C difference. Save command/stdout/stderr/exitcode logs, all media, E1 intents, report, receipt, SHA sums and ZIP.

## Bounded exit criteria

Automated PASS requires the source/evidence pins, all three E1 intents, all D3 raw renders, D3.3 QA, all three FFprobe muxes, source-video identity and audio determinism/seed control. Operator must separately listen/watch A/B/C and record perceived quality and A/V sync. Visual overlay placement remains unapproved regardless of the A/V result.

## Non-goals and safety boundaries

- Do not run C11-C renderer or any D production renderer.
- Do not modify C11-C generators/mechanics, `core/audio`, D3 V5, E1 service, GUI or frozen manifest.
- Do not write under `artifacts/production`; all outputs are under `artifacts/tests/c11e/e4a_audio_mux_review`.
- Do not call the output MP4 a D-overlay composite. E4A.3 images remain separate sample PNGs.
- `renderer=false`, `dispatch=false`, `production_media_created=false`, `release_authority=NONE`.
