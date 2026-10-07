# C11-D D6.5 Full Acceptance — Repair V2

This overlay repairs two acceptance-harness false negatives only.

1. C11-C freeze verification now treats the already-closed D5.5 frozen-identity receipt as the authoritative predecessor gate, with direct local ZIP/build checks used as supplemental evidence when available. D6.5 no longer requires all three protected hashes to appear in one evidence blob.
2. D6.5 negative tests now exercise explicit gate predicates for closed receipts and D4.8 blocking, so tampered states are tested as actual rejection conditions rather than literal comparisons only.

No functional runtime, D3, D4, D5, or D6 authority is changed. D6.5 evidence remains the only generated output tree.
