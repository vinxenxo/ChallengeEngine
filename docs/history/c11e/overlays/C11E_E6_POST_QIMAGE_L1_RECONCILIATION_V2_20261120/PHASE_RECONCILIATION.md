# E6 post-QImage L1 phase reconciliation — V2

## Result contract

The V2 read-only audit keeps the original 18-check scope. The correction affects only the active rehash of the 23 source rows embedded in the exact V2.7 receipt. Four null-byte-count rows must pass by exact SHA-256 match, while all declared byte counts remain exact comparisons.

## Evidence carried forward

- V2.7 runner receipt SHA-256 `95819ea730283ded149faa490b21e0df392341366a853b3c0913318fb203d783`; 37/37 QImage tests; seven benchmark iterations; P95 5.5743 ms.
- V2.7 installer receipt SHA-256 `48dc18147f2e2f3eaed4b72d42df1d97fa39eb20b0a464eea9debc6b3acd6173`; 18/18 files and 11/11 documentation files installed.
- Challenge static contract remains static only; runtime readback not performed.
- CH004 remains eligible for E6 ledger requalification, not accepted.
- Loop A3 V4 lineage pass is not six-selector D-compositor acceptance.

## Independent pending decision

The three V2.7 preview PNGs are byte/hash/PNG-structure validated by the audit, but resampler quality still requires operator visual review. A successful 18/18 reconciliation does not close that human decision or the subsequent Loop source-frame and D-consumer gates.
