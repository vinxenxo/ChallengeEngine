# E4C Drill CLI A/V smoke procedure — 2026-11-12

## Purpose
Qualify the existing CLI facade as the second entrypoint into the one shared D-owned execution adapter. This is not another service, Producer, binder or E1 dispatch connection.

## Preconditions
- V1.4 locale-safe shared adapter installed and proven by the accepted GUI `tracking/tier-1` run.
- GUI A/V receipt accepted and preserved under `artifacts/production/c11e/D99-GUI-6514F1066E79/`.
- Existing CLI facade `c11c-suite/c11c-producer/c11e_production_cli.py` and D executor `tools/c11d/d9/c11e_e4c_drill_execution.py` match the 19 source pins embedded in the runner.
- Use Python 3.13; no pip or dependency changes. No Git checks.

## Run
From the active checkout, call `tools/c11d/d9/RUN_C11E_E4C_DRILL_CLI_SMOKE_V1.ps1` with `ProjectRoot`, `PythonExe`, and optionally `BaseRequestPath`. The default base request is `artifacts/production/c11e/D99-GUI-6514F1066E79/request.json`. The runner clones the canonical successful GUI request, writes a fresh `E4C-CLI-SMOKE-*` request ID, sets `provenance.request_origin=CLI`, preserves `tracking/tier-1`, gameplay seed 12345, music seed 840001 and editorial, hash-pins the exact accepted GUI request and GUI A/V receipt, checks all 19 source pins before and after, and invokes the facade with explicit `--origin CLI --execute-drill-av`.

The runner uses .NET `ProcessStartInfo` with separately drained stdout/stderr, timeout and explicit exit-code handling. It writes all request, output, logs and summary to `artifacts/tests/c11e/e4c_cli_smoke/<request_id>/`; media goes to `artifacts/production/c11e/<request_id>/`. It never reuses or overwrites the GUI pilot output root.

## Acceptance
Require process exit 0; CLI execution summary and full qualification receipt status `PASS_E4C_DRILL_SINGLE_SELECTOR_A_V_QUALIFICATION`; `request_origin=CLI`; same shared executor identity; GUI/CLI E1 semantic parity PASS; `e1_validation.status=PASS_E1_PREPARATION_ONLY`; 91 source pins consistent; `FAMILY_MUSIC_V4` A/B identical and C changed; final A/C video bitstream identical and audio bitstream different; final FFprobe profile REVIEW_720, 27s, 720×1280/30fps/810 frames, AAC-LC 48k stereo and start delta zero; C11-C frozen manifest unchanged; dispatch false and release NONE. Operator visual/listening review of the CLI output is required.

Do not infer CLI A/V PASS from the earlier `c11e_gui_cli_parity.json`: that file only establishes E1 semantic plan parity.

After CLI PASS, proceed to the remaining 19 rows in the family/tier matrix. The accepted GUI `tracking/tier-1` pilot counts as row 1/20.
