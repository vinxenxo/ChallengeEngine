# C11-D D2.1 — Validation Overlay V1

Overlay destinado a descomprimirse directamente sobre la raíz de `ChallengeEngineV01_STATELESS`.

## Uso

```powershell
Expand-Archive -LiteralPath "$env:USERPROFILE\Downloads\C11D_D2.1_VALIDATION_OVERLAY_V1.zip" -DestinationPath "." -Force
Set-ExecutionPolicy -Scope Process Bypass
.\tools\c11d\d2\validate_d2_1_registry.ps1
```

## Qué valida

- D2.0 receipt = PASS
- Registry V1 presente y legible
- 15 assets lógicos
- 9 Challenge bindings
- 2 explicit families
- 5 UNKNOWN family bindings
- 27 asset references
- 0 unresolved references
- runtime_authority = NONE
- reglas canónicas presentes
- MASTER / START prompts actualizados
- snapshots históricos presentes cuando existían
- no se modifica runtime, renderer, simulation, mechanics, RNG ni C11-C congelado

La validación no promociona familias ni activa routing runtime.
