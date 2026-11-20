# L3 V1 — negative controls

Nine in-memory negative controls must fail closed: wrong dimensions, wrong byte count, wrong stride, altered source hash, frame-order mismatch, historical MP4 source, write into protected evidence, write outside the L3 output root, and incorrect geometry.

`REJECTED_AS_EXPECTED` means the control was safely rejected. No negative fixture is written to the checkout or to V4/V5 evidence.
