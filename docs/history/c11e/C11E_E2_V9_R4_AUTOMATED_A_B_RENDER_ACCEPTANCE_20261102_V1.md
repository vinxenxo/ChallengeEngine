# C11-E E2 V9 R4 — Automated A/B Render Acceptance

**Date:** 2026-11-02
**RequestId:** `C11E-E2-CH001-AB-20261101-V9-R4`
**Branch / HEAD:** `main` / `7fbdf8529d2af6ba7089eacd8fd9b38682466d84`
**HEAD parent in receipt:** `b299521dcd738c0ab45f4db37e0d3ab70a00c06b`

## 1. Immutable evidence references

- Receipt: `artifacts/production/c11e/C11E-E2-CH001-AB-20261101-V9-R4/C11E_E2_RENDER_RECEIPT.json`
- Receipt SHA-256: `2f8c355453d8558c6af42aa5da35f603b767726d64ba04f842dc799a2cadef7f`
- Receipt checksum sidecar records that exact digest.
- Evidence ZIP: `C11E_E2_CH001_AB_EVIDENCE_20261101_154340_38e2c012.zip`
- ZIP size: `1,772,547` bytes.
- ZIP SHA-256: `f33431bb131697baf9dc3df6ed1ed8e4ca14ecb40d7b9ef07c812a5bca67a3de`.
- ZIP CRC test: clean.

The library copy's SHA-256 matches the runner-reported digest byte for byte. The archive contains the receipt/checksum, A/B source AVI and delivery MP4s, sidecars, request/effective configuration JSON, FFmpeg commands/logs, FFprobe JSON, pixel comparison logs, review samples and toolchain/contract logs.

## 2. Preflight and contracts

- C11-C manifest: 796,318 bytes; SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.
- E2 runner: `158325324626085ebf319f68906ca8778f9a08eb39c6e8441da146c12ee4f953`.
- Python pair contract: `ab4ed3fd421ef0cac86d4ef25167f0161a186ef5bd90373414abed7bea17d2a9`.
- Godot numeric test: `73fc4421f6ebfec8e3f458123600663cc772838731f57e240ef22abbebf2ef3b`.
- Godot `4.7.1.stable.mono`; Python `3.13.14`; FFmpeg/FFprobe `9.0`.
- Godot JSON numeric cases: 30/30 PASS.
- Python contract tests: 9/9 PASS.
- Runner exit code: 0 and explicit `C11-E E2 AUTOMATED A/B PASS.` marker.

## 3. A/B isolation

Both attempts use `CHALLENGE_001`, gameplay seed `193847`, music seed `840001`, and the same effective C configuration SHA-256 `ec8925fa5b4ab996a791c8cf7f5b139470774720f57880c5b01b2d0aa5b57bea`. The only declared request difference is `production_override.title`:

- A: `C11-E TITLE A`
- B: `C11-E TITLE B`

The receipt records exactly two isolated `CHALLENGE_001` renders. Audio is disabled in E2.

## 4. Pixel and delivery assertions

| Assertion | R4 result |
|---|---|
| Source timebase | 540 frames, 60 fps, 540×960, 9 s |
| Delivery | 270 frames, 30 fps, 720×1280, 9 s |
| Gameplay body crop | 540/540 pixel-identical |
| Editorial title slot crop | 540/540 pixel-different |
| Header regions outside title slot | top/bottom/left/right each 540/540 identical |
| Final MP4 full frame | 270/270 pixel-different |
| Final codec | H.264 High |
| Final pixel format / range | `yuv420p` / `tv` |
| Final audio streams | 0, as required for E2 |

Final MP4 metadata was independently inspected from the archived FFprobe JSON. Both A and B report `codec_name=h264`, `pix_fmt=yuv420p`, `color_range=tv`, 720×1280, 30/1 fps, 270 frames, 9.000000 s, and one video stream only.

## 5. Media SHA-256

| Render | Source AVI | Final MP4 |
|---|---|---|
| A | `0f265d8526793e25c12ae1fc55287133024d34716d92bcc47494023b70859e54` | `3d72e52cc7f7f8fc4b32c8719ab9800ba622e6069c7fa956526c108defce1afd` |
| B | `23ffc36f6121511f224e6f251f09f5f465393559dabefdf83e65cf711b271945` | `77c5ec4d432db9bebd174309d4e8e4039b437e78d08a16b30a3497fb5e1d3045` |

## 6. Governance disposition

Receipt values: `renderer_invoked=true`, `media_created=true`, `release_authority=NONE`, `baseline_promotion=false`, `d_governance_mutated=false`, `human_visual_review=PENDING`.

**Decision:** E2 automated physical render, pixel invariance/difference, and final delivery metadata assertions PASS. The R4 artifacts are immutable and are not release media. Full E2 closure remains pending the operator's visual sign-off, recorded as a separate V22+ decision. No E3 audio or mux was invoked in R4.
