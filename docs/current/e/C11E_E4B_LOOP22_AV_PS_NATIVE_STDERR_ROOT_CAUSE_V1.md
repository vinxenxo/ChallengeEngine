# E4B Loop22 — PowerShell Native stderr Root Cause / V1

## Observed failure

The V1 runner wrapper line 26 invoked:

`$testOut = & $python $tests --project-root $root --r1p-recovered-zip $archive 2>&1`

The wrapper set `$ErrorActionPreference = 'Stop'` on line 6. Python's standard `unittest.TextTestRunner` writes its progress and summary to `stderr` by default. Windows PowerShell 5.1 handles native-process stderr as error-stream records, including when merged with `2>&1`; with the global Stop preference, a normal diagnostic record can terminate the wrapper while the child command is still being consumed. The visible first test line was `... ok`, but there is no complete test-count/exit-code receipt in the supplied log.

## Consequence

The exception occurred at line 26, before V1 line 28's exit-code and test-count assertions and before V1 line 33's media runner invocation. Consequently, do not infer any Loop22 media launcher invocation from the attempt. R1P and R1V remain accepted prior evidence; they are not rerun.

## Corrective design

V2 uses `System.Diagnostics.Process` directly with `UseShellExecute=false`, `RedirectStandardOutput=true`, `RedirectStandardError=true`. Both `ReadToEndAsync()` tasks are started before waiting, preventing either pipe from filling and deadlocking the child. The process exit code is read independently of stream contents. Windows command-line arguments are explicitly escaped/quoted; no command shell is involved. `$ErrorActionPreference` remains `Stop`.

The wrapper executes a regression child twice: one run returns 0 and one returns 23; both emit unique stdout and stderr markers. The wrapper asserts that each marker remains in its correct stream and that each exit code is retained. It then writes test stdout/stderr logs and proceeds only if AST parsing and exactly 24 focused tests pass. The actual runner result is additionally checked structurally for 44 captures, 44 launches, 44 AV outputs and 22 A/B pairs.

## Boundaries

This is a wrapper-only repair. The V1 Python qualification runner/support/matrix/approval remain pinned and unmodified. No C11-C files, generators, music logic, seeds, mechanics or frozen manifest are changed. The renderer remains OFF; release authority NONE.
