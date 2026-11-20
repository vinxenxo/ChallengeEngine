# E6 Next Gates — V6

## Closed

1. V2 phase reconciliation correction: installer ADD_ONLY 18/18; 15/15 documentation/prompt files verified in repository; focused tests 21/21; read-only audit 18/18 PASS. Preserve V1 incident receipt unchanged.
2. QImage L1 synthetic pixel-stage benchmark: 37/37; seven iterations; P95 5.5743 ms. This is not an end-to-end consumer test.

## Immediate next gate — human visual review

Review the exact three preview files listed in `docs/history/c11e/overlays/C11E_E6_POST_QIMAGE_L1_CLOSEOUT_V3_20261120/QIMAGE_VISUAL_RESAMPLER_REVIEW_PROTOCOL.md`. Confirm hashes before inspection. Record an explicit accept/decline for `SmoothTransformation` and observations for registration bars, smooth RGB gradient and one-pixel checkerboard. Geometry approval is already established and must not be conflated with filter approval.

## Following gate — Loop source closure (read-only)

Complete one evidence row per actual Loop selector: source path/size/SHA, stream/frame/ordering, PTS/DTS/duration/timebase, decoded dimensions/pixel format, planes/component order/stride/packing, color range/matrix/primaries/transfer, orientation/alpha and D9.9/D9.10/R1P receipt lineage. Preserve original integer ticks and rational timebase. Use UNKNOWN for unsupported fields; conflicts block closure. No decoder, Godot, FFmpeg or FFprobe execution.

## D-owned consumer gates

- L2: one copied source frame at the existing Option C seam, only after a separately approved exact TEST_ONLY policy/manifest.
- L3: negative controls, source no-change, geometry/bands/body identity, layout/stride validation and operator visual review.
- L4: six Loop selectors with exact input/output hashes and per-row receipts.

Challenge runtime readback and Drill runtime readback remain independent. Smoke18 remains draft/unarmed; E6 accepted 0; no renderer/media/dispatch/BatchId authority is granted by this document.
