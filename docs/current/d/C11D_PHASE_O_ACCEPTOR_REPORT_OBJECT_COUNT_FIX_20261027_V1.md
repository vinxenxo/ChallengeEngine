# C11-D — Fase O: corrección de conteo del mapa de evidencias

**Tipo de cambio:** sustitución guarded del aceptador de Fase O más esta nota add-only.

## Causa

El informe `phase_o_crosswalk_report.json` genera `process_evidence_sha256` como objeto JSON (mapa ruta → SHA-256), no como array JSON. Windows PowerShell 5.1 deserializa ese mapa como `PSCustomObject`; `@($Report.process_evidence_sha256).Count` cuenta el objeto como una unidad y provoca el falso error `Phase O report array counts mismatch` aunque las 36 entradas ya se hayan verificado.

## Corrección

El aceptador cuenta las propiedades del objeto con `@($Report.process_evidence_sha256.PSObject.Properties).Count`. La comprobación sigue exigiendo 36 entradas de evidencia; no relaja el control ni cambia el formato del informe.

## Evidencia y límites

La auditoría Phase O se ejecutó correctamente en Windows con 28/28 tests, 9/9 selectores, 18/18 recibos, 36/36 archivos de evidencia, 15 pins de fuentes de assets, 54 filas de forma de campos base, seis candidatos `custom_data` estables en presencia/tipo y tres punteros estáticos presentes. Sus artefactos siguen identificados por hashes en el marcador de finalización en `%TEMP%`.

Esta corrección no repite la auditoría ni Godot. Solo permite al aceptador avanzar hasta las verificaciones restantes del informe. La aceptación documental solo se produce si todas las demás guardas y las precondiciones de escritura pasan.

**Gobernanza sin cambios:** `renderer=OFF`; `media_created=false`; `payload_materialized=false`; `candidate_input_admissible=false`; `approved_bindings=0`; `D4.8=BLOCKED`; `release_authority=NONE`. No se crea payload ni media y C11-C permanece inmutable.
