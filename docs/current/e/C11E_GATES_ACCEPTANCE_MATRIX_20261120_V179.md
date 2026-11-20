# C11-E gates and acceptance matrix — V179

| Gate | State | Evidence / remaining condition |
|---|---|---|
| Option C QImage L1 | PASS synthetic only | 37/37; P95 5.5743 ms; not end-to-end |
| L1 read-only reconciliation | PASS | V2 receipt SHA `24c2a4f09901a3d1c888d972aabf2a7016496f48e5011b512a1e261338d72474`; 18/18 |
| L1 documentation V3 | PASS | 16/16 ADD_ONLY |
| Loop Source Closure V1 | BLOCKED by auditor false negatives | 113 PASS, 2 PENDING, 3 semantic false negatives; six source MP4 rehashes complete |
| Loop Source Closure V2 | PREPARED / NOT RUN | Corrects D4.8 pin typo and QImage/L1 receipt-shape checks; adds 10 semantic regression tests; expected 116 PASS, 2 PENDING, zero BLOCKED if source inputs remain unchanged |
| L1b resampler | PENDING | Three exact V2.7 PNG previews require operator inspection |
| L1c source colorimetry | PENDING | Matrix/primaries/transfer undeclared; no assumed BT.709 |
| QImage real RGB24 source buffer | NOT PRESENT | Historical R1P manifests contain YUV420P decoded hashes only; no materialized RGB24 buffer |
| L2 copied real frame | BLOCKED | Requires RGB24 buffer, color semantics, L1b decision, approved successor policy and exact TEST_ONLY manifest |
| L3 controls/review | BLOCKED | One-frame proof and negative controls are not authorized |
| L4 six Loop selectors | BLOCKED | Depends on L2/L3 and separate scope approval |
| Challenge runtime readback | NOT PERFORMED | Independent gate |
| Drill runtime readback | NOT PERFORMED | Independent gate |
| Smoke18 | DRAFT / NOT ACCEPTED | 18 rows; 13 reuse candidates; E6 accepted 0 |

Historical R1V/Loop22 A/V acceptances do not establish E6 acceptance or approval of the new D compositor.
