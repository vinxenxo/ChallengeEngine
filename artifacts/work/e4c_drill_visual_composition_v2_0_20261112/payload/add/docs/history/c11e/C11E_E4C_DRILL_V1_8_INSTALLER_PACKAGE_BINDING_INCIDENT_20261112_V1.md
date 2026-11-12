# C11-E E4C V1.8 installer package-binding incident — V1

**Date:** 2026-11-12  
**Disposition:** FAIL_CLOSED_PRE_TRANSACTION / NO_DESTINATION_MUTATION  
**Superseding package:** V1.9 consolidated rebuild only

## Operator diagnostic

`PACKAGE_ZIP_SHA256=PASS/b546b5af018fe7baa3a423b5bf9979c03fdc829053b986eabe184cca1565b026`. The installer then reported `OPERATION_PACKAGE_FILE_BINDING_FAIL: docs/current/e/C11D_E_BLOCKER_REMEDIATION_REGISTER_20261112_V54.md`.

## Root cause

V1.8 physically renamed current documentation payload files from previous versions to next versions (for example `C11D_E_BLOCKER_REMEDIATION_REGISTER_20261112_V55.md`) but did not update the operation rows' `destination` and `package_path`. Its manifest row therefore pointed to `payload/add/docs/current/e/...V54.md`, which was absent from `package_files`; the physical package row correctly recorded V55. The first failing row was the Blocker Register, but the stale-destination defect affected the version-renamed document and prompt rows as a class. The package-file binding guard correctly stopped before transaction.

## Transaction disposition

The failure occurred during `PACKAGE_PREFLIGHT`/operation-to-package-file consistency validation, before `DESTINATION_PREFLIGHT`, evidence-root/journal creation and destination mutation. The in-memory transaction journal was empty. No source file or checkout destination was written by this attempt.

## V1.9 consolidated correction

V1.9 rebuilds the operation matrix from the actual payload filesystem, not from stale rows carried forward from V1.8. For all payloads:

- `payload/replace/<relative>` is mapped to exactly one `REPLACE` destination `<relative>`.
- `payload/add/<relative>` is mapped to exactly one `ADD_ONLY` destination `<relative>`.
- Every payload appears in exactly one operation row; no operation row may reference a missing or duplicate package path.
- Every destination is unique and safe; every package file has an exact size/SHA row.
- Manifest `replace_count`, `add_count` and `payload_count` are checked against actual operation arrays.

The expected transaction is one replacement of the existing D-owned consumer plus 23 additions, including the focused test under the new `tests/` path. The V2 consumer, tests, requalifier and runner are otherwise unchanged. V1.9 must pass Windows PowerShell 5.1 AST, source pins, Python 3.13/PySide6 runtime, py_compile, 18 tests, File.Replace round-trip, immediate rechecks and transactional receipts before any E4C media requalification.

## Governance

C11-C 2.19.12 remains sole production authority; frozen manifest SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`. E1 is `PREPARE_ONLY` / `NOT_CONNECTED_E1`; production dispatch false; `release_authority=NONE`. No Git, pip, GUI/CLI, E1, executor, binder, C11-C or shared dependency changes.
