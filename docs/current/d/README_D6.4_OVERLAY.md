# C11-D D6.4 Overlay

Apply this overlay at the repository root.

## Included

- D6.4 seed provenance schema
- D6.4 integration adapter
- D6.4 PowerShell 5.1 runner
- D6.4 contract
- current D handover updates
- current start prompt/master prompt updates

The runner generates its four D6.4 evidence JSON files under:

`artifacts/tests/c11d_d6/d6_4/`

Only that evidence directory is allowed to change during D6.4 validation.

## Run

```powershell
Set-Location "C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS"

powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\tools\c11d\d6\run_d6_4_seed_request_plan_integrator.ps1
```

The runner itself performs two complete integration runs and compares the four evidence files byte-for-byte and by SHA-256. Running the runner a second time from a clean prompt is recommended as an external repeat.

Expected close:

`D6.4 = PASS / CLOSED`

`NEXT = D6.5 - Full D6 Acceptance`
