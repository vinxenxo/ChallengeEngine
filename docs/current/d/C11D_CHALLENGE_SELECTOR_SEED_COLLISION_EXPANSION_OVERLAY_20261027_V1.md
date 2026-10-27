# Overlay V1 — ampliación de rechazo de colisiones a los nueve selectores Challenge

**Estado:** preparado para aplicar y ejecutar en el checkout Windows; no es una aceptación de ejecución.

## Puerta previa aceptada
La auditoría Windows de dos selectores pasó con `20/20` negativos, `4/4` colisiones, `23/23` source pins y cero invocaciones Godot. Evidencia y hashes completos en `C11D_SEED_DOMAIN_COLLISION_REJECTION_AUDIT_ACCEPTANCE_20261027_V1.md`.

## Alcance añadido
- Mapa de selectores derivado del preflight canónico de nueve Challenges, con sus source pins exactos.
- Para cada Challenge: diez casos negativos de semillas explícitas o implícitas y dos colisiones numéricas (`12345`, `840001`).
- Rechazo esperado en el guard D9.9/D9.10 antes de Godot. En cada negativo se comprueba el fragmento de error específico; el rechazo genérico por selector fuera de matriz no cuenta como PASS.
- Reporte JSON autohasheado validado con JSON Schema Draft 2020-12; helper PowerShell one-shot con stdout/stderr separados, hashes y reporte en `%TEMP%`.

## Integridad/guardas
- Overlay ZIP: comprobar SHA-256, entradas exactas, bytes y destinos staged.
- Reemplazos `REPLACE_GUARDED`: checkpoint V2.2 y ledger; ambas fuentes deben seguir con los hashes previos del overlay.
- Adiciones `ADD_ONLY`: contrato/schema de auditoría, runner Python, helper PowerShell y dos documentos de registro. Ningún destino existente será sobrescrito.
- Verificar y preservar `release/C11C_FREEZE_PACKAGE_MANIFEST.json` SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`, bytes `796318`.
- Verificar sin cambios el docket de policy SHA-256 `e008217bd57303b638e13329d21e5ae56ee3b4efef790566e3702c89ee41a83f` y la decisión de integración V1.

## Resultado esperado, no afirmado
`selectors=9`, `explicit_seed_negative_cases=90/90`, `numeric_seed_collision_rejections=18/18`, `source_pins=27/27`, `runtime_invocations=0`. Si cualquier precondición/pin/schema falla, detenerse y conservar logs; no repetir la auditoría one-shot.

## Gobernanza
La auditoría no amplía el binder de payload más allá de su selector fijado. `renderer=OFF`, `media_created=false`, `candidate_input_admissible=false`, `seed_domains_complete_for_candidate_input=false`, `D4.8=BLOCKED`, `D9.10=PREPARE_ONLY`, `release_authority=NONE`.
