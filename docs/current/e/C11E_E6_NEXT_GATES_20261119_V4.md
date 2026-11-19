# C11-E E6 Next Gates — V4

## Immediate
1. Run post-QImage L1 read-only reconciliation V1 once; it must verify the V2.7 receipts and 3 preview PNG hashes.
2. Inspect previews visually and record operator resampler decision.
3. Perform read-only Loop source closure; exact input path/selector, frame order, PTS/timebase, dimensions, pixel format, RGB24 packing/stride and color metadata must be linked to receipt hashes.

## L2–L4
- L2: one copied frame through the D-only QImage consumer at the existing seam, after separately approved exact TEST_ONLY policy/manifest.
- L3: negative controls, no-change source verification, pixel/body identity, bands/gutters and human review.
- L4: six Loop selector rows with exact input/output hashes and per-row receipts.

## Other E6 gates
Challenge runtime readback and Drill runtime readback are independent and still blocked pending a scoped successor policy and exact process manifest. Smoke18 matrix remains a candidate draft, not frozen.

No renderer, Godot, FFmpeg, FFprobe, audio, mux, production media, dispatch or BatchId is authorized by this plan.
