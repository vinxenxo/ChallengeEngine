# C11-E Execution Hygiene and Assistant Error Log — V21

**Date:** 2026-11-03

## Current rules

1. Separate patch installation, automated testing and GUI operation. One script must not chain all three.
2. A successful patch apply is not a test result. A Python compile/test PASS is not GUI runtime acceptance. PySide6 import is not GUI runtime acceptance.
3. Do not rerun V1.3 patch application or V1.4's 31-test suite after their supplied PASS unless code or test pins change.
4. The next immediate action is a real Producer GUI runtime observation and one controlled E3 CH001 audio attach pilot, not another installer revision.
5. Use only test output roots for E3 pilot runs. Never overwrite R4 input or create a release product.
6. Preserve first failure, native exit code, stdout/stderr, hashes and the full evidence. Do not run success-only assertions after nonzero exit.
7. No `File.Replace` for ordinary add-only documentation overlays. Validate all paths and preimages before writing. Do not put receipt/counting complexity into a patch-only script unless operationally required.
8. Do not use ambiguous PowerShell `$LASTEXITCODE` after a script invocation; capture the actual child process exit code at the invocation boundary. Avoid `py.exe -3.13` argument quoting bugs by resolving the Python 3.13 executable first and then invoking that `python.exe` directly.
9. Avoid PowerShell collection/type pitfalls in error paths. Keep failure-report writing independent of the primary test exit and never let a secondary error replace the original failure.
10. Do not take over Git housekeeping without user request. Do not make local commit/push/ref changes. Do not repeat Git checks solely to create activity.
11. The active checkout is authority; snapshots are context only. Never restore a snapshot ZIP over the checkout.
12. Snapshot outputs belong in Documents, never under repository `release`. Do not rebuild or alter the C11-C manifest.

## Recent incident record

### E3 overlay installer V1 / V1.1 / V1.2

- V1 failed in PowerShell 5.1 because `[IO.File]::Replace` was called with a null backup argument/path combination rejected by Windows.
- V1.1 progressed further but failed when computing counts on an object/array result; rollback restored the verified `main.py` preimage and removed added paths.
- V1.2 repeated a related object/type mismatch while constructing the apply manifest/receipt and rolled back additions plus the replacement.
- Lesson: a patch installer is only a patch installer. V1.3 applied ten files and postimage-verified them without launching tests, GUI, FFmpeg, audio or Git.

### E3 test runner V1.3

- It passed the Python launcher selector as an argument to `python.exe`, producing `Unknown option: -3`.
- It then raised a second PowerShell type mismatch while trying to report the failure.
- V1.4 fixed this by asking `py.exe -3.13` for the concrete `python.exe` path using native PowerShell argument binding, invoking the concrete interpreter thereafter, and simplifying failure-report creation.
- Operator result: compile PASS, 31/31 tests PASS and PySide6 6.11.2 import PASS. Evidence receipt SHA `84fc86c96ca237c7dd16837666882e80afe6dda8292a04527d19fcbd3579e30b`.

## Explicit non-claims

The V1.4 test success does not mean the Producer GUI was launched, E3 was operated manually, a production audio file was created, or a production/release MP4 was generated. The test mux used temporary media. E3 remains open until GUI runtime, the operator pilot, physical QA, provenance receipt and parity evidence are accepted.
