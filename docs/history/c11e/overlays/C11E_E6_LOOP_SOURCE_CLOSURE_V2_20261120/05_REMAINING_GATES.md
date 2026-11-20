# Remaining Loop gates — V2

Two V1 pending conditions remain legitimate:

- Source colorimetry: primaries, transfer and matrix/space are undeclared. Full-range `pc` does not establish BT.709 or any other colorimetry. `conversion_authorized=false`.
- Operator visual review: exact V2.7 synthetic PNG previews must be inspected and `SmoothTransformation` accepted or declined explicitly. Geometry approval is separate.

A third downstream input gap is recorded as a state, not hidden: the R1P pixel evidence contains decoded YUV420P hashes, no frame files and no packed RGB24 buffer. QImage requires RGB24, 720x1280, stride 2160, 2,764,800 bytes/frame. The historical decoded YUV420P frame is 1,382,400 bytes. They are not interchangeable.

Even after source closure PASS, L2 remains false until a real RGB24 input contract, approved color semantics, visual resampler decision, separately approved successor policy and exact unarmed-to-approved TEST_ONLY manifest exist.
