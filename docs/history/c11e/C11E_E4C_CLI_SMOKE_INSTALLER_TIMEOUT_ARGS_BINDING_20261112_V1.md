# E4C CLI smoke installer timeout — V1.5 failure and V1.6 correction

Date: 2026-11-12

## Observed Windows result

V1.5 passed package SHA, 19/19 source pins, PowerShell AST 2/2 and destination preflight. It failed closed in `STAGING_AND_PYTHON_TESTS` with `PYTHON_TIMEOUT: ;`. Failure diagnostic: `E4C_CLI_SMOKE_OVERLAY_V1_5_20261112T062654Z_25a3aa0b_FAILURE.json`. The transaction journal was empty; `c11c_source_mutation=false`, `production_dispatch=false`, `release_authority=NONE`. No project file writes occurred.

## Root-cause assessment

The V1.5 installer declared a function parameter named `$Args`, colliding by name (case-insensitive) with PowerShell's automatic `$args` variable, and invoked the function positionally with an array expression. The failure string exposed an empty argument rendering (`PYTHON_TIMEOUT: ;`), consistent with Python starting without the intended script argument and waiting for stdin. This is the specific defect being addressed; the user's log does not provide a Python process command line, so the diagnosis is marked HIGH-CONFIDENCE, not asserted as a directly captured command.

## V1.6 correction

- Renames the parameter to `$PythonArguments`.
- Calls `Invoke-Python` with named parameters and a concrete `[string[]]` argument array.
- Rejects empty/null argument arrays and empty command lines before starting a process.
- Redirects standard input and closes it immediately after process start, preventing an accidental interactive Python wait.
- Logs the exact executable and argument line, and records it in failure diagnostics.
- Includes installer-contract tests asserting these controls and stages the installer into the test root so the tests inspect the exact packaged bytes.
- Raises the bounded test process timeout to 300 seconds while retaining nonzero exit checks and output assertions.

## Scope and gates

V1.6 remains ADD_ONLY: it adds documentation, the CLI runner, runner tests and continuity prompts. It does not replace GUI/CLI/business logic or the accepted D execution adapter. It retains 19 source pins and the accepted GUI baseline hashes. The CLI A/V smoke remains OPEN until an actual Windows run completes with the full A/V receipt and operator review. No E4C closure or production promotion is inferred.
