# C11-E Gates Acceptance Matrix — V28

| Gate | Status | Evidence / next action |
|---|---|---|
| E0 | PASS retained | No rerun |
| E1 | PASS retained | Shared service; separate-process CLI adapter; current GUI dispatch path |
| E2 | PASS bounded | CH001 R4 title-to-pixels only |
| E3.2 | PASS retained | D3 V5/E1 contract |
| E3 GUI/audio pilot | PASS | CH001 R4 physical pilot; operator audiovisual review confirmed |
| E3 V1.5 compile | PASS | Windows py_compile exit 0 |
| E3 V1.5 negative suite | PASS 50/50, zero skips | Runner's ordered checks succeeded before evidence-inventory error |
| E3 V1.5 recovery receipt | PASS | Supplemental receipt SHA `8e01946da3de35c05430335259a88e14f5bae1b660c6896de5d8f13c37c3fafe` |
| E3 formal closure | PASS_TEST_ONLY | Original wrapper BLOCKED preserved; recovered supplemental receipt proves completed assertions |
| E4A.0 discovery V1 | BLOCKED_TOOLING | PowerShell type argument mismatch; read-only, no changes |
| E4A.0 discovery V2 | READY | Corrected self-extracting launcher; must pass on Windows |
| E4A implementation | NOT_STARTED | Wait for V2 report, then minimal existing consumer patch |
| E4B Visual Loop | NOT_STARTED | After E4A |
| E4C Visual Drill | NOT_STARTED | After E4B |
| E5 | NOT_STARTED | Cross-family determinism, seed domains, non-leakage, CLI/GUI |
| E6 Smoke18 | NOT_STARTED | Six complete audiovisual cases per family |
| E7 Matrix101 | NOT_STARTED | 54+27+20; CH_008/009 held (99 provisional) |
| E8 | NOT_STARTED | Historic corpus reconciliation, independent acceptance, freeze and separate approval |

C11-C 2.19.12 remains sole production baseline; manifest SHA `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`. `release_authority=NONE`, `baseline_promotion=false`, `freeze_eligible=false`.
