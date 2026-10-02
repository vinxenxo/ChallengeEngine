# C11-D D2.2 — Asset Role / Evidence Matrix Overlay V1

Overlay intended for direct extraction into the project root.

## Apply

From the project root:

```powershell
Expand-Archive -LiteralPath "$env:USERPROFILE\Downloads\C11D_D2.2_ASSET_ROLE_EVIDENCE_OVERLAY_V2.zip" -DestinationPath "." -Force
Set-ExecutionPolicy -Scope Process Bypass
.\tools\c11d\d2\run_d2_2_asset_role_evidence.ps1
```

## Purpose

D2.2 converts D2.0 role/reference evidence into a descriptive asset-role matrix. It does not activate runtime routing.

Rules:

- explicit evidence only;
- UNKNOWN remains UNKNOWN;
- no filename-only inference;
- no SHA-256 asset merging;
- no historical promotion;
- no renderer/simulation/mechanics/RNG changes;
- updates MASTER/START and snapshots them before replacement.

## Outputs

- `artifacts\tests\c11d_d2\d2_2_asset_role_evidence_matrix.json`
- `docs\current\d\D2.2_ASSET_ROLE_EVIDENCE_MATRIX_CONTRACT.md`
- `artifacts\tests\c11d_d2\d2_2_validation_receipt.json`
- updated `docs\current\d\MASTER_HANDOVER_C11D_CURRENT.md`
- updated `docs\current\d\START_PROMPT_C11D_CURRENT.md`
- historical prompt snapshots under `docs\history\master-prompts\c11d\`

The overlay is root-relative and contains no enclosing project folder.
