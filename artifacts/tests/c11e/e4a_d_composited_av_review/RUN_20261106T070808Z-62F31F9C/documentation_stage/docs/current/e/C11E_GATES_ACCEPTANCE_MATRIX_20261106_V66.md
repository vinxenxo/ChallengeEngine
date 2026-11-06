# C11-E Gates / Acceptance Matrix — V66

| Gate | Status | Evidence / next condition |
|---|---|---|
| E0 foundation / governance | ACCEPTED | Reuse; do not restart. |
| E1 shared GUI/CLI service | ACCEPTED_BOUNDED | Shared E1 service; current service pin `348997...`; parity for final E4A output still required. |
| E2 Challenge control | ACCEPTED_BOUNDED | Existing bounded title-to-pixels control; no repeat without relevant drift. |
| E3 D3 V5 / D3.3 / mux | ACCEPTED_BOUNDED | Retain accepted contract/tests; not production dispatch. |
| E4A.2 Challenge base | PASS_TEST_ONLY | Real C11-C BODY baseline. |
| E4A.3D.1 isolated compositor | PASS_TEST_ONLY | Technical compositor proof only. |
| E4A.4 audio/mux pilot | PASS_TEST_ONLY | D3 V5 A/B/C validated on earlier uncomposited C11-C MP4; not D-composited final A/V. |
| E4A.5B source review | PASS_STATIC_SOURCE_REVIEW | Latest submitted snapshot reviewed; do not infer Git provenance. |
| E4A.6 live D visual / reserved bands | **PASS_TEST_ONLY_USER_VISUAL_REVIEW** | Recovery V1.2 receipt `327901...`; silent D-composited H.264 SHA `841b...`; 12/12 inactive black and 4/4 active editorial. |
| E4A.7 D-composited D3 V5 A/V | READY_FOR_EXECUTION_RECEIPT_GOVERNED | Runner V1 is self-contained and ready; verify its Windows receipt for the outcome. Verify source pins, reuse visual MP4 unchanged, generate D3 A/B/C, D3.3, stream-copy mux and FFprobe. |
| Full E4A Challenge | IN_PROGRESS | Requires E4A.7 pass + user audio review + E1 GUI/CLI parity. |
| E4B Visual Loop | ON_HOLD | Start only after full E4A; preserve Loop C11-C binder/grammar/music. |
| E4C Visual Drill | ON_HOLD | Start only after E4B; preserve Drill binder/phase/END_CTA/music. |
| E5 cross-family determinism | NOT_STARTED | Three-family seed isolation, profile/binder non-leakage, GUI/CLI parity. |
| E6 Smoke18 | NOT_STARTED | Six full audiovisual scenarios per family. |
| E7 Matrix101 | NOT_STARTED | 54 Challenge + 27 Loop + 20 Drill; CH_008/009 held; 99 provisional runnable. |
| E8 independent acceptance | NOT_STARTED | Historical C→E matrix, independent review, freeze, separate promotion authority. |

## Hard limits

C11-C 2.19.12 frozen manifest SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`. `renderer=OFF`; production dispatch/media OFF; D4.8 BLOCKED; D9.10 PREPARE_ONLY; D9.14/D9.16 BLOCKED; D9.17 BLOCKED_NO_GO; D10 BLOCKED_FOR_PROMOTION; `release_authority=NONE`. CH_008/009 unresolved (11 s declared vs 12 s phases).
