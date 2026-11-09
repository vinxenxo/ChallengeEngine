# C11-E Current Authority — 2026-11-09 V109

## State at V2 handoff

- E4A accepted. E4B active.
- R1P 27/27 and Loop22 projection 22/22 remain accepted; R1V five-selector audiovisual pilot remains closed/operator-accepted. None of those gates is rerun here.
- V1 Loop22 execution overlay installed successfully: `PASS_ADD_ONLY_INSTALL`, 30/30 source pins verified, 16/16 payload files added, frozen C11-C manifest unchanged.
- The first V1 execution-wrapper attempt stopped at the Python unit-test invocation. PowerShell 5.1 emitted a `NativeCommandError` at `RUN_C11E_E4B_LOOP22_AV_QUALIFICATION_V1.ps1:26`, while unittest wrote its normal progress to child `stderr`. This is a wrapper/process-stream handling defect, not evidence of a Python test assertion failure.
- The exception occurred before V1 wrapper line 33, which invokes the Loop22 runner. Therefore this attempt does not establish any media-launcher execution or completed capture. Do not infer a partial 44-slot result from the single displayed `test_01 ... ok` line.

## Root cause and corrective control

V1 used `& $python ... 2>&1` while `$ErrorActionPreference='Stop'`. Windows PowerShell 5.1 can surface redirected native-process `stderr` as an error record; under the global Stop preference, a normal unittest diagnostic line terminates the wrapper pipeline before its exit-code and test-count checks. The V2 wrapper never invokes native executables through PowerShell's `&` pipeline. It uses `.NET System.Diagnostics.Process` with `UseShellExecute=false`, both output streams redirected and drained concurrently using `ReadToEndAsync()`, and an explicit process `ExitCode`. The global error preference remains `Stop`.

Before running the 24 focused Loop22 tests, V2 self-tests the bridge with a Python child that writes distinct stdout/stderr markers and exits once with code 0 and once with code 23. The bridge must preserve stream separation and both exit codes, while each pipe carries more than 16 KB to exercise concurrent draining. V2 records stdout/stderr logs and a JSON receipt. It then performs PowerShell AST parse, Python AST parse, exact 24-test/exit-code assertions, and only after all pass invokes the pinned Loop22 runner. A zero exit from the runner is insufficient by itself: V2 also checks the structured 44 captures, 44 launcher invocations, 44 AV outputs and 22 A/B pairs.

## Installation and use

Install V2 add-only; it adds a separate wrapper and versioned documentation without replacing the V1 wrapper or runner. Execute `RUN_C11E_E4B_LOOP22_AV_QUALIFICATION_V2.ps1` only after the V2 installer reports `PASS_ADD_ONLY_INSTALL`. Do not run V1 again. The V2 wrapper pins the installed V1 runner/support/tests/matrix/amendment/approval files before execution.

## Scope and governance

The authorized scope remains 22 remaining Loop selectors × A/B = 44 new C11-C silent captures and 44 AV outputs. Native FAMILY_MUSIC_V4 WAV remains PCM16 stereo 44.1 kHz; delivery copy is PCM16 stereo 48 kHz exact samples; final audio is AAC-LC 192 kb/s / 48 kHz stereo; source H.264 is stream-copied. No filters or audio processing are introduced.

No R1P/R1V rerun, no C11-C source modification, no Git checks, no D renderer, D3 V5, dispatch, D4.8 activation, D9.10 promotion, D10 promotion, release authority or production delivery. Renderer OFF; D4.8 BLOCKED; D9.10 PREPARE_ONLY; D9.14/D9.16 BLOCKED; D9.17 BLOCKED_NO_GO; D10 BLOCKED_FOR_PROMOTION; `release_authority=NONE`.

## Evidence expected

V2 installation receipt: `artifacts/tests/c11e/e4b_loop22_av_ps_bridge_v2/INSTALL_RECEIPT.json`.
Preflight/test/process logs and execution receipt: `artifacts/tests/c11e/e4b_loop22_av_ps_bridge_v2/PSB2_<run-id>/`.
A technical qualification PASS still leaves operator visual/editorial/layout review and listening review pending for all 44 outputs.
