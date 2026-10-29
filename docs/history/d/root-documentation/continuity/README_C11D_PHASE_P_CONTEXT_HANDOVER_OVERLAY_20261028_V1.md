# C11-D Phase P context and documentation handover overlay V1

Este overlay preserva la evidencia anterior y añade el estado de Phase P después de la reparación del probe de versión Python. Incluye master handover prompt V25, start prompt V25, checkpoint V25, ledger V2, registro JSON de tests estáticos, playbook PowerShell 5.1, reporte de recuperación/next gate y roadmap hacia un render real del baseline D. También actualiza cuatro punteros estables con reemplazos guardados y prehash exacto.

## No es una aceptación de runtime

El operador reportó Python 3.13.14, normalización 5/5 y tests estáticos Phase P 30/30. La ejecución runtime Phase P sigue pendiente. El primer error de probe y el parche intermedio con precondición fallida quedan como fallos históricos; no deben repetirse ni convertirse en PASS.

## Cómo usarlo

1. Descarga el ZIP en `Downloads`.
2. Desde la raíz del checkout, extrae el ZIP a un directorio temporal nuevo y ejecuta `apply_phase_p_context_handover_overlay_20261028_v1.ps1 -Root (Get-Location).Path`.
3. La aplicación valida que los artefactos de Phase P tengan los hashes esperados, que el manifiesto del checkout activo siga siendo el canónico y que los cuatro apuntadores estables coincidan exactamente con sus prehashes. Si una precondición falla, no escribe ningún archivo.
4. Si aplica, genera backups de los cuatro apuntadores en `%TEMP%` y añade los nuevos documentos. Reejecutar solo se permite cuando los add-only existentes son byte idénticos.
5. Usa el playbook para el runtime Phase P; no ejecutes el runtime durante el apply.

## Snapshot esperado para la siguiente ventana

`ChallengeEngineV01_STATELESS_C11-D10_CONTEXT_SNAPSHOT_20261028_POST_PHASE_P_STATIC_PASS.zip`

Se trata de un snapshot de contexto del árbol tras el overlay, generado por `c11c-suite`, no de una nueva aprobación del baseline D. La nueva huella del ZIP es esperada. No copiar su manifiesto empaquetado encima del checkout ni confundir la huella del ZIP con la autoridad del manifiesto canónico activo.


## Nota específica sobre el ZIP de releases y la captura usada

El snapshot que llegó primero a la biblioteca (`ChallengeEngineV01_STATELESS_C11-D10_latest_FROZEN_20261028_163525.zip`) se inspeccionó con SHA-256 `199a65ee76eb72a878808cb7b3c862a3eeb945b356cab9726c5d6c86f64b55a1`, tamaño 8.366.872 bytes, 3.476 entradas y CRC limpio. Ese archivo no contenía todavía los artefactos Phase P y, por tanto, no es la captura correcta de continuidad posterior a Phase P.

Aclaración del operador: la divergencia observada en el contenido empaquetado de `releases` está causada por la generación del ZIP freeze/snapshot mediante `c11c-suite` para continuar el trabajo en otra ventana; no es un defecto adicional que deba abrir otra línea de investigación. La nueva captura tendrá una huella de archivo distinta intencionadamente. No invertir más iteraciones en intentar normalizar esa huella del ZIP. Solo comprobar la integridad del archivo y el estado del checkout vivo; no reescribir ni sustituir el manifiesto canónico desde el ZIP.
