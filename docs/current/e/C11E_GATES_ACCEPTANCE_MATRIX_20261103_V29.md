# C11-E Gates Acceptance Matrix — V29

| Gate | Status | Evidence / next action |
|---|---|---|
| E0 | PASS retained | No rerun |
| E1 | PASS retained | Shared service; CLI adapter and current GUI dispatch |
| E2 | PASS bounded | CH001 R4 title-to-pixels only |
| E3.2 | PASS retained | D3 V5/E1 contract |
| E3 GUI/audio pilot | PASS | CH001 R4; operator audiovisual review confirmed |
| E3 V1.5 negative suite | PASS 50/50, zero skips | Supplemental recovery receipt validates existing evidence |
| E3 formal closure | PASS_TEST_ONLY | Receipt SHA `8e01946da3de35c05430335259a88e14f5bae1b660c6896de5d8f13c37c3fafe` |
| E4A.0 discovery V2 | PASS_READ_ONLY | 751 files / 803 matches / 111 candidates / 0 scan errors |
| E4A source pins V3 | PASS 10/10 | All expected current source hashes matched |
| E4A D9 focused tests V3 | PASS 6/6 | Retain; do not rerun absent pin change |
| E4A legacy Producer GUI test | BLOCKED_STALE_VERSION_LITERAL | First assertion expects 0.11.1; main.py reports 0.12.0-E3 |
| E4A diagnostic V4 | PASS_READ_ONLY | Main/test clean; HEAD `dd1a40f4df797c80ebcbfc90f0d40c55b4e186bd`; C11-C manifest PASS |
| E4A successor GUI contract V1 | PENDING | Run isolated successor test; original historical test remains unchanged |
| E4A static audit closure | PENDING | Requires successor all-functional-assertions PASS plus six retained passes |
| E4A physical Challenge render | NOT_STARTED | Only after static audit closure and source/slot contract review |
| E4B Visual Loop | NOT_STARTED | After E4A |
| E4C Visual Drill | NOT_STARTED | After E4B |
| E5 | NOT_STARTED | Cross-family determinism, seed domains, non-leakage, CLI/GUI |
| E6 Smoke18 | NOT_STARTED | Six audiovisual cases per family |
| E7 Matrix101 | NOT_STARTED | 54+27+20; CH_008/009 held (99 provisional) |
| E8 | NOT_STARTED | Historic corpus reconciliation, independent acceptance, freeze and separate approval |

C11-C 2.19.12 remains the sole production baseline; manifest SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`. `renderer=OFF`, `release_authority=NONE`, `baseline_promotion=false`, `freeze_eligible=false`.
