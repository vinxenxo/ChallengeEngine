# E6 Next Phase Start Prompt — V3

The V2 QImage L1 phase reconciliation has returned 18/18 PASS; its focused suite passed 21/21. This closes only the read-only reconciliation substage. Do not repeat predecessor test suites.

1. Inspect the three exact V2.7 synthetic previews using `QIMAGE_VISUAL_RESAMPLER_REVIEW_PROTOCOL.md`; record an explicit accept/decline for `SmoothTransformation`. Do not infer approval from PNG hashes or the previously approved 720×1280 geometry.
2. Perform read-only Loop source closure using `LOOP_SOURCE_CLOSURE_PROTOCOL.md`. Pin source path/hash, selector mapping, frame order, PTS/timebase, decoded pixel layout/stride, color interpretation and D9.9/D9.10/R1P lineage. Unknown/conflicting evidence blocks closure; do not run a decoder or media tool.
3. After those gates only, prepare a separately scoped successor policy and exact E6 TEST_ONLY manifest for one copied frame at the existing D-owned Option C seam. No execution until separately approved.

Challenge runtime readback, Drill runtime readback, six Loop selectors and Smoke18 authorization remain separate gates. E6 accepted 0; D4.8 V2 BLOCKED/immutable; renderer OFF; media/dispatch OFF; release authority NONE. Keep all documentation under repository `docs/` overlays/current and prompts under `prompts/`.
