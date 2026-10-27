# C11-D — Corrección de codificación del aceptador V2-C (Fase N)

**Motivo:** la primera ejecución del aceptador terminó antes del write-back porque Windows PowerShell 5.1 no interpretó correctamente literales Unicode del script guardado como UTF-8 sin BOM. La búsqueda de la línea `**Próxima acción única:**` no encontró el token de ledger.

**Corrección:** sustituir el mismo aceptador por byte-for-byte el mismo texto UTF-8, precedido de un BOM UTF-8. No se cambia la lógica del aceptador, sus pines, contratos, filtros, umbrales ni el write-back. El BOM permite que Windows PowerShell 5.1 identifique explícitamente la codificación del código fuente y compare correctamente los literales acentuados.

**Evidencia runtime preservada:** contrato V2-C `28/28`; source pins `81/81`; planner `9/9`; procesos Godot `18/18`; selectores `9/9`; evidencia `36/36`; informe SHA-256 `7f96c9aec3849212299afbcabe7fd3045fee815807c9cafe555ad8cb947f91f2`. No se vuelven a ejecutar tests, planner ni Godot.

**Alcance:** la corrección solo permite que el aceptador llegue a sus guardas reales de write-back. La fase solo se acepta si el propio aceptador revalida todos los hashes, los nueve selectores, los 18 recibos, los 36 artefactos y la gobernanza. El informe sigue siendo `PASS_SOURCE_FRAME_ROUTE_ONLY`; no demuestra píxeles ni vídeo.

**Gobernanza:** manifiesto congelado C11-C inalterado; `renderer=OFF`; `media_created=false`; `payload_materialized=false`; `candidate_input_admissible=false`; `D4.8=BLOCKED`; `release_authority=NONE`. No se aprueban bindings ni se promociona el baseline.
