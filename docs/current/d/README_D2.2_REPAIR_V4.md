# C11-D D2.2 Semantic Repair Overlay V4

Root-relative overlay. Extract directly into the project root.

Purpose:
- Correct the D2.2 semantic classification so cross-family asset reuse is admissible.
- Define TRUE_FAMILY_CONFLICT only for the same Challenge + resolved asset binding with multiple explicit families.
- Remain compatible with PowerShell 5.1 StrictMode.
- Do not modify renderer, simulation, mechanics, RNG or frozen C11-C sources.

Commands from project root:

    Expand-Archive -LiteralPath "$env:USERPROFILE\Downloads\C11D_D2.2_ASSET_ROLE_EVIDENCE_REPAIR_OVERLAY_V4.zip" -DestinationPath "." -Force
    Set-ExecutionPolicy -Scope Process Bypass
    .\tools\c11d\d2\repair_d2_2_family_reuse_conflict.ps1

Expected result:

    C11-D D2.2 — REPAIRED / READY FOR VALIDATION
