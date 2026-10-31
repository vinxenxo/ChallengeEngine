# C11-E — E2 V6 V1 installer File.Replace incident (V1)

**Observed:** 2026-10-31 10:59:22 Europe/Madrid.

## Evidence

- Checkout: `main`, HEAD `a3c7c5d284a96ce115ca52208b4039002502753b`.
- V6 V1 installer receipt: `C:\Users\vinxe\Documents\C11E_E2_V6_FIX_20261031_105922\C11E_E2_V6_FIX_RECEIPT.json`.
- Receipt SHA-256: `408fd6fa62f7e549475779621073a05e570d65b268168e4c87ce8b4f764d559e`.
- Status `FAILED_PARTIAL_OR_NONE`; `files verified/applied=0/9`; renderer/media false.
- Runner SHA after failure remained V5: `9340907afd4e787495be5a9d711024a8a7ab2787aa507842ea7c7ada0c198b72`.

## Root cause

The installer created a same-directory temporary copy for the first replacement and called `[IO.File]::Replace($Temp, $Destination, $null)`. On Windows/.NET the null backup path was normalized as a path and raised `System.ArgumentException` (“La ruta de acceso no tiene un formato válido”). The operation failed before replacing the runner. The temporary copy was left beside the runner.

## Impact and operator transcript

No payload was applied, no renderer or media was created, and E2 V6 was not installed. The subsequent runner hash check correctly failed because it still equaled V5. The operator then printed “E2 V6 REMEDIATION INSTALLED AND VERIFIED” after the `throw`; that message is manually emitted text, not a successful installer or hash check. It is explicitly classified as false PASS and must not be cited as evidence.

## Remediation

V2 pins this failure receipt and verifies the 0/9 result. It identifies exactly one orphan runner temp by exact filename pattern and intended V6 SHA-256, copies it into the new receipt evidence directory and verifies the copy before deleting the original. Replacements use a unique non-null backup path on the same volume, preserve/hash-check the preimage backup, record each operation and verify all nine postimages. Any unexpected temp or installer failure stops the runner.
