# R1V Python Executable Resolution Recovery — V3

## Incident timeline

1. Wrapper V2 failed preflight under Windows PowerShell 5.1 because native STDERR flowed into PowerShell's error stream; the process exit variables remained null. No R1V launcher/media.
2. Installer V3 failed before copying (`INSTALLED_FILES=0/15`). It selected a command using `py.exe` semantics and appended `-3.13`; the operator host resolved the executable to `Python313\python.exe`, which rejected `-3` (`Unknown option: -3`). No files were copied by that attempt; no R1V launcher/media.
3. The user also tried the wrapper path while the new files were absent; Windows reported file-not-found. An earlier wrapper preflight receipt ended `FAIL_R1V_WRAPPER_PREFLIGHT`; no launcher invocation.

## V4 architecture change — remove redundant installer preflight

The V4 installer is pure PowerShell and intentionally has no Python execution path. It validates package manifest and payload hashes, frozen C11-C/governance/R1P pins, allowlisted paths, AST and add-only destinations; then copies. It does not call `Start-Process`, `py.exe`, `python.exe`, nor the 32-test suite. Identical pre-existing files are verified and skipped; differing bytes abort; no overwrite.

Wrapper V3 is the sole Python-preflight owner. It locates a direct `python.exe` candidate, probes `sys.version_info[:2] == (3,13)` with `-c`, and executes the 32-test active-checkout suite exactly once using `Start-Process -Wait -PassThru` plus separate stdout/stderr files. It records a numeric exit code. Only that 32/32 PASS allows the ten approved captures.

## Acceptance state

The 32-test suite passed locally against a reconstructed V84 integration fixture with its R1P and Option C evidence. This is not a Windows active-checkout receipt and does not claim PowerShell 5.1 execution. Await V4 installer receipt and wrapper V3 Windows receipt. No R1V capture has yet passed.
