# E4B Loop Family Contract V1 — Test Failure Review V1

**Disposition:** `TEST_HARNESS_DEFECT_CONFIRMED; CONTRACT_TESTS_6_OF_7_PASS; NO_PRODUCT_SOURCE_REGRESSION`.

## Evidence

The operator's V1 runner log shows PowerShell 5.1 AST PASS, frozen C11-C manifest PASS, 40/40 source pins and 4/4 local tool pins. The Python suite ran seven tests: six passed and `test_operator_decision_and_static_family_audit` failed at line 137 because `mp4_present_in_snapshot_count` was expected to equal zero but the audit returned 27.

The test harness called `contract_audit.build_report(PROJECT_ROOT)`. That function scans `PROJECT_ROOT/artifacts/production/audiovisual/...` and checks whether each manifest-listed MP4 path exists under that root. In the operator's active checkout, 27 matching MP4 files were present. The audit report field name incorrectly described those as snapshot files. The V1 runner repeated the same brittle assumption after the test stage with a hard failure if the count was nonzero.

## Root cause

Three distinct concepts were conflated: (1) contents of the V77 ZIP archive, (2) files present in the live checkout at execution time, and (3) actual visual review/acceptance. The audit measured (2), while the test and runner assumed (1), and the documentation treated (3) as if it could be inferred from (1). File existence cannot prove video decoding, expected dimensions, frame order, visual composition, typography or human acceptance.

## Corrective action in V2

- Add a V2 audit adapter; preserve V1 source and evidence unchanged.
- Rename the measurement to `mp4_present_in_project_root_count` and each row to `mp4_present_in_project_root`.
- Recompute and validate the aggregate against all 27 per-selector booleans.
- Require `visual_review_performed=false` and explicitly state `NO_MP4_VISUAL_REVIEW`.
- Remove the runner's hard-coded zero requirement. Accept any integer from 0 through 27 only when it matches the per-selector rows.
- Add test fixtures for 0/27 absent, 27/27 present and a mixed count of 13; add a negative aggregate-mismatch test.
- Run the full 8-test suite before the read-only audit; record exit codes and stdout/stderr hashes.

## Scope boundary

No C11-C source, production manifests, MP4 files, D9.8 model, GUI/CLI request schema, family launcher, renderer, audio engine or media is modified. V2 only corrects the audit/test semantics. A successful V2 result remains static contract evidence, not render acceptance.
