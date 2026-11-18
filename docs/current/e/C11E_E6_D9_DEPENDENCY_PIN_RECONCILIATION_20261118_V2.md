# C11-E E6 D9 dependency-pin reconciliation — V2

**Date:** 2026-11-18  
**Disposition:** `V1_AUDIT_PASS_ACTIVE_CHECKOUT; V1_FOCUSED_TESTS_ENVIRONMENT_FAILURE; V2_PORTABLE_TEST_AND_APPLICATOR_PREPARED; EXECUTION_HELD`

## 1. Incident summary

The operator's `PS log.md` records three distinct outcomes:

1. The V1 installer completed all six add-only copies, printed `INSTALL_STATUS=PASS_ADD_ONLY`, `INSTALL_FILES=6/6`, and verified each payload postimage. A following `if ($LASTEXITCODE -ne 0)` nevertheless threw `INSTALL_FAILED`. This was a caller-side false failure: `$LASTEXITCODE` is the exit code of the last native process and is not a success contract for a PowerShell `.ps1` invocation. No installer failure is evidenced by the log.
2. Twelve focused unit tests passed. `test_rejects_symlink_escape` errored while creating an actual Windows symbolic link with `OSError: [WinError 1314]`, because the process lacked the required symbolic-link privilege. The test failed before reaching `safe_project_file`; this is an environment-dependent test fixture failure, not a failed path-containment assertion.
3. The V1 audit runner then completed independently with `PASS_DEPENDENCY_PIN_RECONCILIATION_EXECUTION_HELD`: fixed evidence pins/sidecars 13/13, accepted source pins 33/33, additional route dependencies 9/9, observed-current CH004 hashes 2/2, failures 0. Report: `E6D9PINREC_20261118T090219Z_97FFB0DD`, SHA-256 `fa54b47826f58acc823d45a8771a2dc12827d34d46d9586a34b8f6813a9e0603`.

The V1 focused suite must therefore be recorded as **12/13 PASS, 1 environment-dependent ERROR**, not 13/13 on the active Windows checkout. Do not rerun the V1 symlink test as a gate.

## 2. V2 correction

V2 does not modify or replace the V1 audit module or any accepted evidence. It adds:

- a distinct `..._v2.py` focused test module;
- an integrated PowerShell 5.1 apply-and-run script;
- this incident/authority document and refreshed handover/start prompts.

The V2 symlink-escape test patches `Path.resolve()` for the candidate path to simulate resolution through a link/junction to an outside target. It verifies the same `PATH_ESCAPES_PROJECT_ROOT` containment rejection without calling `os.symlink()` or requiring Developer Mode/elevated privilege. The runtime function under test remains the unchanged V1 `safe_project_file()` implementation.

The integrated PowerShell script checks its own AST, preflights every package payload and destination before copying, rejects reparse-point destination ancestors, enforces add-only/idempotent SHA-256 postimages, then runs the V2 tests and V1 audit. It reads `$LASTEXITCODE` **only immediately after native Python processes**. It never interprets `$LASTEXITCODE` after invoking a PowerShell script.

## 3. Evidence and state

V1 active-checkout audit remains valid and is not invalidated by the test harness issue:

- fixed evidence and sidecars: 13/13;
- accepted live source pins: 33/33;
- route dependency fingerprints: 9/9;
- CH004 observed-current source hashes: 2/2;
- report blockers: 0.

CH004 reuse remains unaccepted. `universal_editorial_model.py` retains `UNRESOLVED_HISTORICAL_E4A7_PIN_DIVERGENCE_NO_AUTO_WAIVER`. The historical `c11e_production_service.py` E4A.7 pin is superseded for current source-baseline purposes by the accepted 33-pin receipt, but this does not retroactively prove the old media's provenance. No historical files or receipts are rewritten.

## 4. Next phase

After V2 apply-and-run returns all PASS, continue the D9 Challenge execution seam in PREPARE_ONLY: verify source-pinned invocation boundaries, config/selector mapping, A/B/C identity relations, and output-ledger closure. In parallel, perform an explicit CH004 historical lineage adjudication using the exact E4A.7 receipt and nested artifacts. Do not re-run accepted E4A media to repair provenance.

## 5. Render authorization remains blocked

The operator's approval to continue engineering does not override D4.8 R1V V2. That policy remains immutable and does not authorize E6 Smoke18, Godot capture, D3/audio/PCM or FFmpeg mux. A distinct E6 TEST_ONLY authorization and explicit governance resolution are mandatory before media execution. No media/render command is part of this V2 applicator.

## 6. Permanent invariants

C11-C 2.19.12 remains the sole production baseline. Frozen manifest SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`; D4.8 R1V V2 SHA-256 `0866b53ad4fcdebe74d01f66864b2dfb00eb644ca28dcd59301c8f3208239c07`. E1 `PREPARE_ONLY`; renderer OFF; production dispatch/media false; `release_authority=NONE`. No protected C11-C changes, no parallel Producer/binder/renderer, no Git checks, commits operator-managed, SHA-256 pins enforced.
