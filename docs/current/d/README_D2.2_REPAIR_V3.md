# C11-D D2.2 — Semantic Repair Overlay V3

Root-relative overlay. Descomprímelo directamente en la raíz de
`ChallengeEngineV01_STATELESS`.

PowerShell 5.1:

    Expand-Archive -LiteralPath "$env:USERPROFILE\Downloads\C11D_D2.2_ASSET_ROLE_EVIDENCE_REPAIR_OVERLAY_V3.zip" -DestinationPath "." -Force
    Set-ExecutionPolicy -Scope Process Bypass
    .\tools\c11d\d2\repair_d2_2_family_reuse_conflict.ps1

V3 corrige el fallo de V2 al intentar asignar una propiedad inexistente
bajo StrictMode.

La reparación:
- recalcula la reutilización entre familias usando el audit D2.0;
- distingue CROSS_FAMILY_REUSE de TRUE_FAMILY_CONFLICT;
- añade propiedades JSON faltantes de forma segura;
- no modifica renderer, simulation, mechanics, RNG ni C11-C congelado;
- actualiza matriz, contrato, receipt, MASTER y START;
- crea snapshots históricos de MASTER y START.

No requiere pegar un script largo en PowerShell.
