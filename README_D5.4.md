# C11-D D5.4 Overlay V1

Copy/expand this overlay into the existing C11-D repository root. It is cumulative and does not replace the repository.

## Files

- `definitions/c11d/artifacts/C11D_ARTIFACT_LIFECYCLE_POLICY_V1.json`
- `tools/c11d/d5/artifact_lifecycle_quarantine_rules.py`
- `tools/c11d/d5/run_d5_4_artifact_lifecycle_quarantine_rules.ps1`
- `docs/current/d/D5.4_ARTIFACT_LIFECYCLE_QUARANTINE_RULES_CONTRACT.md`

The runner creates its own D5.4 evidence under:

`artifacts/tests/c11d_d5/d5_4/`

## PowerShell 5.1 command

```powershell
Expand-Archive `
  -LiteralPath "$env:USERPROFILE\Downloads\C11D_D5.4_ARTIFACT_LIFECYCLE_QUARANTINE_RULES_V1.zip" `
  -DestinationPath "C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS" `
  -Force

Set-Location "C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS"

.\tools\c11d\d5\run_d5_4_artifact_lifecycle_quarantine_rules.ps1
.\tools\c11d\d5\run_d5_4_artifact_lifecycle_quarantine_rules.ps1
```

## Important

D5.4 is validate/governance-only. It does not move, delete, reclassify, quarantine physically, promote, retire or activate any artifact. The 9 `ORPHANED` records and the 12,304 global candidates remain untouched.
