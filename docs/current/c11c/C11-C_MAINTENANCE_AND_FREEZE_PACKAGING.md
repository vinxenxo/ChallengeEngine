# C11-C — Maintenance and Freeze Packaging

## Safe cleanup

`tools/prototypes/c11c_bulk/clean_c11c_artifacts.ps1` is dry-run by default and targets only generated media inside explicitly named C11-C prototype roots. It never targets `artifacts/production`, `artifacts/qa`, `artifacts/regression`, `artifacts/releases`, `artifacts/tests` or `artifacts/legacy`.

## Documentation consolidation

`tools/maintenance/consolidate_c11c_2_19_documentation.ps1` archives superseded 2.15-2.19.x C11-C material and old Suite/Producer/Studio current docs into `docs/history/`. It uses hashes to avoid destructive collisions and supports `-DryRun`.

## Freeze package

`tools/maintenance/create_c11c_freeze_zip.ps1` is the sole C11-C freeze authority. It requires the final 2.19.12 PASS report, a non-empty **historical real** `build_factory.py`, no root `override.cfg`, and no superseded documents left under `docs/current`. It excludes caches, generated media, scratch, regenerable prototype/production payloads and nested archives. Repository source such as `.githooks` is retained. It writes adjacent SHA-256 and package-manifest files. It explicitly rejects the temporary canonical-producer compatibility wrapper.

`Make_zip.ps1` is historical/generic and must not be used for the C11-C baseline.
