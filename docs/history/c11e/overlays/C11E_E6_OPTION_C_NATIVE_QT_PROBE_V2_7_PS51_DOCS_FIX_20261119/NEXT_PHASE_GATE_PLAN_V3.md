# C11-E E6 Option C next-phase gate plan — V3

## Gate L1 — synthetic native pixel stage (current)

Close only when: A3 V4 adjudication passes; all active source pins pass (including explicit QImage module and 37-test suite SHA/byte pins); eight bootstrap regressions pass; the original 37 target tests pass without skips/errors/failures; seven native iterations complete; P95 <= 33.333 ms. Record P50/P95 and preferred 16.667 ms target separately. This remains `PASS_QIMAGE_STAGE_BENCHMARKED_NOT_END_TO_END`.

## Gate L1b — visual resampler decision

Inspect the exact three synthetic preview PNGs, their SHA/format/geometry and the visual behavior of `SmoothTransformation`. Geometry is already approved (720x1280; content 504x896 at 108,192; black reserved bands/gutters). Resampler quality requires separate operator approval; a benchmark cannot grant it.

## Gate L1c — read-only Loop source closure

Against the active checkout only, inventory exact C source producer/capture, ordered frames, pixel encoding (RGB24), width/height, stride, color interpretation, selector/seed and metadata/receipts D9.9/D9.10/R1P. Pin each source and prove there is a non-guessed input seam. This step must not invoke a renderer or decode media without policy permission.

## Governance bridge before L2

Draft a separate, narrowly scoped successor to the blocked D4.8 V2 policy and a separate E6 TEST_ONLY execution manifest with exact executable path/hash/version, arguments, input paths/hashes, expected output roots, process counts, timeouts, stop-on-first-failure and prohibited side effects. They remain proposals until explicit governance approval. D4.8 V2 is never edited or bypassed.

## L2/L3/L4

- L2: one copied real frame at existing D seam, only after approved policy + manifest; source remains read-only.
- L3: pixel/geometry proofs, negative controls and human review.
- L4: widen the same consumer to the six Loop selectors; no new binder, Producer or family adapter.
- L5: only later consider eligible rows in Smoke18 under its own authorization.

The mainline current authority V178 still identifies the Challenge static consumer contract audit as the next executable mainline increment. This Option C lane does not supersede it.
