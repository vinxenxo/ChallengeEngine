# E4C Drill Shared A/V Installer V1.1 Correction Record — 2026-11-11

## Incident

The first Windows PowerShell 5.1 installation attempt of `C11E_E4C_DRILL_SHARED_AV_EXECUTION_V1_20261111.zip` passed the ZIP checksum, extracted the package, and found the co-located manifest and payload. It then failed while invoking the Python version probe. The console error began `File "<string>", line 1`.

## Boundary and impact

The failure occurred in staged validation, after the temporary source staging area was made but before the installer created `artifacts/tests/c11e/e4c_drill_shared_av_overlay/<run-id>`, wrote `TRANSACTION_JOURNAL.json`, or touched any destination. The failed run therefore requires no rollback. The active checkout remains unchanged by this attempt. The package's earlier Linux-side checks did not test the PowerShell 5.1 native argument serialization behavior.

## Root cause

The V1 installer supplied quote-bearing Python source as a `-c` command-line argument via a PowerShell 5.1 array splat. That boundary is not reliable for nested quoting in Windows PowerShell 5.1. This is the same class of quoting failure previously observed in the project and should not have been reintroduced.

## Corrective implementation

V1.1 writes version and PySide6/Qt probes as two UTF-8 Python files under its unique `%TEMP%` stage and invokes Python with those file paths. There are no inline `python.exe -c` probes. The two scripts are also included in the staged `py_compile` check, bringing it to 6 files (the four overlay modules plus the two probes). On every failure, V1.1 reports a named stage and attempts to write a JSON diagnostic containing the exception and PowerShell script stack to `%TEMP%`, even when the transaction evidence directory has not yet been created.

## Preserved contract

- Existing Producer GUI and existing E1 CLI facade remain the only entry points.
- One D-owned adapter remains the shared execution path.
- E1 remains `PREPARE_ONLY`; `family_adapter.status=NOT_CONNECTED_E1`.
- Source support pins and exact two replacement preimages remain unchanged.
- A/B music seed 840001, C seed 840002; gameplay seed remains independent.
- C11-C source capture remains silent (`-NoSound`); FAMILY_MUSIC_V4 is used; D3 V5 and gameplay-coupled audio remain excluded.
- No Git checks, pip, dependency mutation, C11-C edits, production dispatch or release promotion.

## Qualification still required

The corrected installer must pass Windows PowerShell 5.1 AST, package inventory, all source pins and destination checks, Python 3.13/PySide6/Qt runtime, six staged `py_compile` targets, 13/13 tests, immediate pre-transaction rechecks and a complete transaction receipt. Only after installation should the operator launch the existing Producer and perform the single `tracking/tier-1` A/V pilot. V1.1 is not yet installed or runtime-qualified by this record.


## V1.2 correction — correct native stderr handling

The operator's V1.1 Windows attempt passed both runtime probes and all six staged compile targets, then failed at `STAGED_UNIT_TESTS`. The diagnostic's reported first line was a unittest case ending in `... ok`. In Windows PowerShell 5.1, `unittest -v`'s normal stderr progress was converted into a terminating `NativeCommandError` because the installer used `2>&1` with `$ErrorActionPreference='Stop'`. It therefore never reached the actual process exit-code check.

V1.2 replaces the helper with .NET `ProcessStartInfo`: arguments are quoted using the Windows command-line backslash/quote rules; stdout and stderr are redirected separately; both streams are drained asynchronously; `WaitForExit()` is followed by reading each task result; and only `$process.ExitCode` determines success. Standard stderr is retained as diagnostic content but cannot independently fail a zero-exit Python process.

The V1.1 run's failure JSON reports `stage=STAGED_UNIT_TESTS`, no journal entries, `rollback=NOT_NEEDED`, and `c11c_source_mutation=false`. No checkout writes occurred. The adapter, 13 tests, main.py/CLI postimages, E1 service, source pins and transaction operations are unchanged. The V1.2 package remains unqualified until the operator receives the complete Windows installation receipt.


## V1.3 correction — non-null, hash-verified File.Replace backup paths

The operator's V1.2 Windows run reached `TRANSACTION_START` after all staged tests and immediate pre-transaction checks passed. OP-001 (`main.py`) was journaled and its independent preimage backup was copied and SHA-256 verified. The transaction then failed because the installer called `[System.IO.File]::Replace($tempPath, $target, $null, $true)`. The same null backup argument existed in rollback. The run diagnostic confirms `rollback=COMPLETE`, `OP-001=ALREADY_PREIMAGE`, and the target was still exactly the preimage; no source mutation occurred.

V1.3 provides a unique, previously non-existing `destinationBackupFileName` to every forward call, records that path in the journal and verifies that the framework-created backup hashes to the preimage. Rollback likewise creates and journals a unique retired-postimage path before calling `File.Replace`, then verifies both the restored preimage and displaced postimage. A disposable same-volume API probe executes both directions in isolated staging before any repository transaction. The independent copied preimage backup remains preserved as an additional rollback source.

This is an installer-only correction. It does not change the two Producer entrypoint postimages, shared D adapter, E1 service, 13 adapter tests, family music, gameplay/music seed separation, C11-C sources or governance. Windows PowerShell 5.1 execution of V1.3 remains required; local packaging does not claim that platform test.
