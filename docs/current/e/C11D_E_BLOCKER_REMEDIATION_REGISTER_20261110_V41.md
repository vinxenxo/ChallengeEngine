# C11-D / C11-E Blocker Remediation Register — V40 (2026-11-10)

| ID | Gate / issue | State | Required closure |
|---|---|---|---|
| E4C-A3-LINEAGE | Current D review-manifest D9.8 pointer stale versus A.3 historical pin | READY_FOR_PINNED_OVERLAY | V4 installs explicit 2075…→5702… third replacement and adds historical preimage archive; bridge verifies sole JSON-pointer delta. |
| E4C-DRILL-SOURCE | Native Drill phase and ownership | PASS_READ_ONLY | 8 exact C11-C pins /12 checks; do not alter native header/footer or END_CTA CTA. |
| E4C-DRILL-GEOMETRY | D outer-band composition | APPROVED_AS_PROPOSED | Exact geometry SHA approved in separate V1 operator decision record. |
| E4C-DRILL-TIMEBASE | GAME payload → final-presentation frame mapping | APPROVED_AS_PROPOSED | Exact timebase SHA approved in separate V1 operator decision record. |
| E4C-DRILL-CONSUMER | D-owned visual consumer and pixel proof | READY_FOR_D_OWNED_IMPLEMENTATION | Both exact hashes approved; implement at existing D-owned boundary and run isolated pixel/visual tests. Renderer-native input remains OFF. |
| E4C-DRILL-AV | Native family music, mux and human review | NOT_QUALIFIED | Protected silent C11-C capture; `FAMILY_MUSIC_V4`; independent seeds; FFmpeg/FFprobe; human listen/review. D.1 is envelope only. |
| E4C-GUI | Existing Qt Producer GUI runtime use | OPEN | Observe actual GUI dispatch through E1 shared service. |
| E5 | Cross-family determinism/seed isolation/profile non-leakage/GUI-CLI parity | PENDING | After E4C family closeout. |
| E6 | Smoke18 | PENDING | Six complete A/V scenarios per family. |
| E7 | Matrix101 | PENDING | 54+27+20 target; CH_008/009 held, 99 provisional. |
| E8 | Historical C-to-E regression, independent acceptance, freeze/promotion | BLOCKED | Complete E7, independent acceptance and separate explicit authority. |

Permanent governance: C11-C 2.19.12 sole production authority; manifest SHA `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`; renderer OFF, dispatch/media false, D4.8 BLOCKED, D9.10 PREPARE_ONLY, D9.14/16 BLOCKED, D9.17 NO-GO, D10 blocked, release NONE.


Operator approval record SHA-256: `eb95da188065b8ebcb2371e2a6bcff6762ce000a5ca74f8ea384ecec4ee58303`. Geometry and GAME timebase are approved as proposed for D-owned design/contract implementation only.


V3 installer attempt reached STAGED_VALIDATION but stopped before the transaction: under PowerShell StrictMode, a stage-validation filter accessed `.mode` on non-payload package metadata entries. V4 scopes both staged replacement verification and receipt replacement enumeration to the 29-entry `$operationEntries` payload subset.


V4 Windows result: package/AST/pins/destination/staging validation passed, then `py_compile` failed with `Unknown option: -3`. Root cause is command/argument mismatch: `Get-Command py.exe` resolved to `...Python313\python.exe`, but the installer passed the Python Launcher selector `-3.13`, which is not a valid CPython executable option. V5 invokes the discovered `python.exe` directly without `-3.13`, probes `sys.version_info` and requires 3.13 before compilation/tests.
