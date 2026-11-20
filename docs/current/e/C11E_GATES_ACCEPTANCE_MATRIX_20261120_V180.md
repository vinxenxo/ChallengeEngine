# C11-E gates and acceptance matrix — V180

| Gate | State | Evidence / next criterion |
|---|---|---|
| QImage synthetic stage | PASS_TEST_ONLY | V2.7 receipt `95819ea...`; never E6 acceptance. |
| Loop source closure | PASS_PROVENANCE | V2: 116 PASS / 2 PENDING / 0 BLOCKED; six selector rows and media rehash complete. |
| L1 visual resampler | PENDING_OPERATOR | Review the original three pinned V2.7 PNGs and the new actual composed frame; geometry approval is not resampler approval. |
| Historical MP4 colour metadata | UNDECLARED | Matrix/primaries/transfer absent; do not infer BT.709. |
| L2 direct RGB24 single-frame visual probe | ARMED_TEST_ONLY | One fresh E6-L-01 viewport recapture from pinned C11-C scene, one QImage composition; no historical MP4 decode. |
| L3 negative controls | NOT_STARTED | Must follow operator visual approval and independent pixel/geometry controls. |
| L4 six Loop selectors | BLOCKED | Requires L2/L3 acceptance and a separate bounded manifest. |
| Challenge/Drill runtime readback | BLOCKED | Independent family policies and manifests remain required. |
| E6 Smoke18 | DRAFT_ONLY | Six rows per family; no execution authorization. |
| E7 Matrix101 | NOT_FROZEN | CH_008/009 remain held; 99 provisional runnable cases. |
| E8 | BLOCKED | Full historical regression, independent acceptance, freeze and separate promotion. |

D4.8 V2 remains immutable and BLOCKED. This V1 successor permits only the one-frame TEST_ONLY visual probe; it does not alter production authority or promote E6.
