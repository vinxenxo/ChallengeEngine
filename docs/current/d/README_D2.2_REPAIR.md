# C11-D D2.2 — Semantic Repair Overlay V2

This overlay is root-relative and must be extracted directly into the ChallengeEngineV01_STATELESS project root.

It corrects the D2.2 semantic classification where cross-family reuse of the same logical asset was incorrectly counted as a family conflict.

Allowed:
- One logical asset referenced by Challenges from different evidence-backed families = CROSS_FAMILY_REUSE.
- A true family conflict exists only when the same Challenge binding for one logical asset resolves to multiple distinct families.

The overlay updates the D2.2 matrix, contract, receipt, MASTER handover, START prompt, and creates historical prompt snapshots.

No renderer, simulation, mechanics, RNG, or frozen C11-C source is modified.

## Apply

From the project root:

```powershell
Expand-Archive -LiteralPath "$env:USERPROFILE\Downloads\C11D_D2.2_ASSET_ROLE_EVIDENCE_REPAIR_OVERLAY_V2.zip" -DestinationPath "." -Force
Set-ExecutionPolicy -Scope Process Bypass
.\tools\c11d\d2\repair_d2_2_family_reuse_conflict.ps1
```

## Expected result

`C11-D D2.2 — REPAIRED / READY FOR VALIDATION`
