# C11-D D2.2 — Validation Overlay V2

Overlay root-relative. Descomprimir directamente en la raiz de
ChallengeEngineV01_STATELESS.

Esta V2 corrige un falso negativo del validador V1:
la validacion usa los contadores contractuales de la matriz D2.2 como
fuente autoritativa y no exige arrays auxiliares opcionales como
cross_family_reuse_rows.

Uso:

    Expand-Archive -LiteralPath "$env:USERPROFILE\Downloads\C11D_D2.2_VALIDATION_OVERLAY_V2.zip" -DestinationPath "." -Force
    Set-ExecutionPolicy -Scope Process Bypass
    .\tools\c11d\d2\validate_d2_2_asset_role_evidence_v2.ps1
