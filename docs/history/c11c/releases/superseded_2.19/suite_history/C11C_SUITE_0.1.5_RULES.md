# C11-C Suite 0.1.5 Rules

The active operator surface is `c11c-suite`. CLI and GUI invoke the same canonical scripts.

Producer Challenge review uses `tools/qa/c11/run_c11c_challenge_bulk_qa.ps1`; A1 remains historical compatibility QA.

Maintenance cleanup is explicit and fail-closed. Frozen packaging uses `create_c11c_freeze_zip.ps1` and requires final acceptance PASS plus a non-empty historical `build_factory.py`.

## Freeze package

Use only `tools/maintenance/create_c11c_freeze_zip.ps1` from the Maintenance surface. It is fail-closed and excludes generated artifacts/caches.
