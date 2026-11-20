# C11-E installer and audit incident register — V60

## Closed
- L1 reconciliation V1 size-null false negative: historic SHA pins matched; V2 correctly made byte length optional only where undeclared. L1 reconciliation V2 passed 18/18.
- L1 docs V3: PowerShell 5.1 AST PASS; 16/16 ADD_ONLY destinations verified.
- Loop source closure V1 installer: PS 5.1 AST PASS, 22/22 ADD_ONLY, 27/27 tests PASS.

## V1 Loop auditor false negatives — corrected in V2 package, awaiting operator run
- D4.8 expected hash transposition in auditor constant only; actual immutable file hash/bytes match the correct pin.
- QImage semantic receipt check compared nested map to scalar.
- L1 semantic receipt check queried top-level `e6_accepted` rather than nested `phase_state` and `governance`.
- V2 adds explicit exact-shape tests; it does not alter the historical receipts or the D4.8 file.

## Active gates
- Source MP4 rehash complete for the six selected rows in the active checkout.
- Color primaries/transfer/matrix remain undeclared; no BT.709 assumption.
- Resampler review awaits the three exact PNGs.
- Real RGB24 buffers remain absent; do not infer conversion or authorize L2.

No incident permits weakening C11-C/D4.8 pins or enabling media execution.
