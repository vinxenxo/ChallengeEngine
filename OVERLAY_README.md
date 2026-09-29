# C11-C 2.19.12 — FINAL QA MINIMAL REPAIR V5

Three narrowly-scoped fixes only:

1. `c11c-suite/self_test.py`
   Excludes the PowerShell parse harness itself from the operational-surface `c11c-studio` retired dependency scan. The harness intentionally contains the historical path as an exclusion rule; it is not a runtime dependency.

2. `c11c-suite/c11c-test/run_c11c_challenge_family_smoke.bat`
   Restores the correct `.ps1` path. The prior file contained an accidental line break inside the filename, causing PowerShell `-File` to receive a directory and then a truncated command name.

3. `tools/qa/c11/run_c11c_family_coverage_smoke.ps1`
   Makes the optional `reveal_duration` lookup explicit and safe under `Set-StrictMode`. Missing `reveal_duration` is interpreted as 0 seconds for QA timing only. No Challenge JSON is changed and the production launcher remains untouched.

No `core/`, no Challenge definition JSON, no simulation truth, no rendering mechanics, no producer logic, no worker implementation, and no override.cfg are modified by this overlay.
