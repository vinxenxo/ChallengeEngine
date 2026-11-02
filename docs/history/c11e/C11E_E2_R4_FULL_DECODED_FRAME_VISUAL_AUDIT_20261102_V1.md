# C11-E E2 R4 — Full Decoded-Frame Visual Audit V1

**Date:** 2026-11-02
**Input evidence ZIP SHA-256:** `f33431bb131697baf9dc3df6ed1ed8e4ca14ecb40d7b9ef07c812a5bca67a3de`
**R4 receipt SHA-256:** `2f8c355453d8558c6af42aa5da35f603b767726d64ba04f842dc799a2cadef7f`

## Method

Both delivery MP4 files were decoded from beginning to end using OpenCV/FFmpeg-backed video decoding. Each file reported 720×1280 at 30.0 fps and exactly 270 frames. Exactly 270 frames were decoded from A and exactly 270 from B. Every decoded frame was placed into a contact sheet at native aspect ratio, in chronological order, in twelve boards: six boards for A and six for B, 45 consecutive frames per board. The reviewer inspected all twelve boards, covering frames 0–269 in each output. The individual board SHA-256 values and byte counts are recorded in `C11E_E2_R4_FULL_FRAME_VISUAL_AUDIT_MANIFEST_20261102_V1.json`.

This is an exhaustive frame-by-frame visual inspection of decoded video frames, not a claim of human operation of a media player. E2 contains no audio by design; no audio listening review applies.

## Findings

1. Each output contains all 270 expected frames; no decode failure or missing frame was found.
2. The header is stable throughout; `C11-E TITLE A` and `C11-E TITLE B` are legible and not clipped.
3. The key moves through the same sequence relative to the stationary lock in both outputs. The C11-C gameplay/body crop is already proven pixel-identical by the R4 runner for all 540 source frames.
4. The CTA begins in the final segment at approximately 7 seconds and remains visible to the end in both outputs.
5. No unexpected black/gray corruption, tearing, title bleed, or A/B gameplay discrepancy was observed.
6. The key leaves the visible play area at approximately 4.5 seconds and the lock remains on screen until the CTA segment. This is inherited C gameplay behavior and is identical in both renders; no E2 source mechanic was altered. Keep it as a possible later content-design review note, not a presentation regression.

## Decision

`FULL_DECODED_FRAME_VISUAL_AUDIT=PASS_NO_E2_PRESENTATION_DEFECT_OBSERVED`

In response to the user's instruction on 2026-11-02 to visually confirm and close E2, this audit is the visual basis of the separate E2 formal closure decision. The original R4 receipt is immutable and retains its original `human_visual_review=PENDING` field; this report does not rewrite it.
