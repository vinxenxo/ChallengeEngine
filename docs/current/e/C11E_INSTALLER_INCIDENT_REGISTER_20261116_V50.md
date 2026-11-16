# C11-E Installer Incident Register — V50 (2026-11-16)

## Current combined Peripheral Scan safeguards

- One installer invocation validates ZIP/manifest/inventory, PowerShell AST, atomic helper, staged Python tests, atomic I/O, 38 source pins, frozen C11-C manifest and staged/installed PREPARE_ONLY.
- Exactly 21 ADD_ONLY files and immutable install receipt/journal are committed before `-ExecuteBatch` launches the installed runner.
- Staged driver `PYTHONPATH` is temporarily set to the staged project to expose the deterministic PySide6 stub; previous environment value is restored in `finally`.
- Batch launch receipt destination/parent are checked before child start; CreateNew prevents overwrite. Combined receipt binds install receipt, journal, launch receipt and BATCH_RESULT without rewriting immutable snapshots.
- Driver persists BatchId, lock and authorization before emitting `BATCH_RESERVED_ID`; any failure after reservation consumes the ID. The committed installation remains; no automatic retry or rollback.

## Prior incident disposition

Pursuit's 810/27s coordinator mismatch was corrected to its native 690/23s contract. V5/V5.1/V5.2 installer staging/helper/syntax/transaction issues were superseded by V5.3, installed by the operator with 37/37 tests, 7/7 atomic I/O, 35/35 pins and 20/20 operations. Saccade V1 was subsequently installed with 42/42 tests, 7/7 atomic I/O, 37/37 pins and 20/20 ADD_ONLY operations. These installers are not to be rerun.

Current E4C acceptance is 15/20; Peripheral Scan is the only active family. Historical incidents remain audit-only.
