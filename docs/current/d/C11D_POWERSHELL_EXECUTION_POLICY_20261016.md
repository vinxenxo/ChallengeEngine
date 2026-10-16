# C11-D operator execution policy — PowerShell 5.1 (2026-10-16)

This is a small, practical run discipline based on the latest successful Windows execution. It exists to stop test launching and log plumbing from becoming a second project.

## Known-good machine context

The latest user-confirmed successful runtime used:

`C:\Users\vinxe\AppData\Local\Microsoft\WinGet\Packages\GodotEngine.GodotEngine.Mono_Microsoft.Winget.Source_8wekyb3d8bbwe\Godot_v4.7.1-stable_mono_win64\godot.exe`

The auditor independently confirmed `4.7.1.stable.mono.official.a13da4feb`. This is the last verified local path, not a general path for every machine. Never replace it with an invented `C:\Godot\...` path.

## Defaults for the next context

1. Stay in `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`; run from the repository root.
2. Discover Python with `(Get-Command python.exe -ErrorAction Stop).Source`.
3. Use short, complete PowerShell blocks. Resolve paths once. No unnecessary generic launcher functions, nested wrappers, logging frameworks or giant one-liners.
4. Redirect native stdout and stderr into separate files using `Start-Process -RedirectStandardOutput ... -RedirectStandardError ... -Wait -PassThru` when Python's unittest output on stderr can trip PowerShell 5.1 native-command handling.
5. Check the actual process `.ExitCode`, confirm log files exist, read both logs, and check the expected exact PASS marker and expected test count/version/pin/receipt counts. Print PASS only after these checks.
6. If a precondition fails, stop at that step. Don't run dependent tests, hash nonexistent files, or continue to another test after failure.
7. Verify file hashes only for files that exist. Keep stdout hash, stderr hash, JSON audit hash and archive SHA-256 clearly labelled as different values.
8. Separate apply/precondition validation from focused tests/runtime tests. Keep every block balanced and pasteable as a whole; do not send a fragment that ends at `try`, `catch` or `finally`.
9. For additive files, require target paths to be absent and extract without force. For replacement overlays, require all before-hashes, back up the exact replacements, and only then use the required overwrite operation.
10. Never run a full source/context ZIP over the active checkout. Only apply a narrowly scoped overlay. Do not register new tests in the aggregate suite just to claim progress; follow the repository's canonical integration policy.

## Required result gate

For any automated test/runtime gate, the accepting predicate is all of:

- process actually started;
- process exit code is `0`;
- expected output logs exist;
- actual expected test count and/or exact summary marker is present;
- source pin counts and version are verified where the runner requires them;
- independent runtime receipt count is verified where required;
- governance output remains `renderer=OFF`, `media_created=false`, `D4.8=BLOCKED`, `release_authority=NONE` unless a separate, explicit authorization changes the allowed activity.

A console line that says PASS is insufficient when its process exit code or required receipts were not verified.
