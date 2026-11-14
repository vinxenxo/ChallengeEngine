# C11-E E4C V2.3 R2 timeout unit defect and R3 correction

Date: 2026-11-14

## Evidence

- Previous V2.3 R2 installation: PASS, 27/27 staged tests, four replacements plus thirteen add-only operations.
- Independent post-install audit V2: PASS, 17/17 postimages, 4/4 backups, source pins 21/21, frozen C11-C manifest and immutable decision PASS.
- Diagnostic request: `E4C-CLI-COMPOSITION-V2-20261113T072452Z-6fe44217`.
- Diagnostic ZIP SHA-256: `dbed566f629ec2cb30d86f812ed52f97a6b2af801adaa9825c9ecb46a4d4e4df`.
- ZIP contains `d_composition_plan_v2.json` (8,077 bytes), empty qualification and review directories, and empty stdout/stderr logs.

## Root cause

The wrapper called `.WaitForExit(1800)`. In .NET, `Process.WaitForExit(int milliseconds)` accepts milliseconds. The actual timeout was 1.8 seconds, although the intended timeout was 1,800 seconds. The request was killed before FFmpeg frame composition started. Therefore the log does not demonstrate slow FFmpeg or a 30-minute rendering failure.

## R3 change

- Explicit `timeoutSeconds=1800` and `$timeoutMilliseconds=1800000`; each `Process.WaitForExit(int)` poll is bounded to at most 3,000 milliseconds while the overall monotonic stopwatch deadline is 1,800,000 milliseconds.
- Progress polling and display in PowerShell.
- Python atomically publishes `V2_REQUALIFICATION_PROGRESS.json`: evidence validation, plan, toolchain, native probe, frame compositor, mux A/B/C, stream hashes, review frames and completion. Frame compositor updates every 30 frames.
- Timeout failure metadata records seconds, milliseconds, elapsed milliseconds, last progress, stdout/stderr and process-tree termination output.
- On true timeout, `taskkill /T /F` terminates Python and descendants; auto diagnostic packaging captures the last progress checkpoint and all partial outputs.

## Non-changes

No E1 service or `DENY_EXISTING` behavior change; no C11-C generator, mechanics, manifest, binder, executor or production dispatch change; no new native capture; no family music generation; no production release authority. Previous failed output is preserved, and R3 must use a fresh run id.

## Acceptance

R3 target installer performs source pins and frozen manifest checks, PowerShell AST checks, Python compile and a focused 10-test timeout/progress contract suite. It intentionally does not repeat the previously accepted 27-test consumer suite. Operator runs the independent R3 post-install audit before the next A/V qualification.
