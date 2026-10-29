# C11-D — Validación del snapshot y organización documental V1

**Fecha de verificación:** 29-10-2026  
**Objeto:** archivos subidos a la biblioteca: ZIP de contexto, sidecar `.sha256` e informe `.report.json`.

## 1. Identidad verificada

| Campo | Resultado observado |
|---|---|
| ZIP | `C11D_WORKING_CONTEXT_20261029_193950.zip` |
| Tamaño del ZIP | 9,190,399 bytes |
| SHA-256 ZIP | `5b8d06ad82bca798c94db03f943a85afb309d91484d4499ed40fed36056ca774` |
| Sidecar | coincide exactamente con el SHA-256 anterior y el nombre del ZIP |
| Informe externo | coincide en `archive_sha256`, `archive_bytes`, `archive_entries`, `context_tree_sha256` y hashes de manifiesto |
| CRC del ZIP | PASS; lectura completa sin errores |
| Entradas ZIP | 3,721; 3,721 nombres únicos (sin duplicados sensibles a mayúsculas/minúsculas) |
| Inventario interno | 3,720 filas de payload más el manifiesto del snapshot; todas las rutas esperadas están presentes y no hay entradas adicionales |
| SHA/tamaño por entrada | 3,720/3,720 coinciden contra `C11D_CONTEXT_SNAPSHOT_MANIFEST.json` |
| Rutas inseguras | 0 absolutas, 0 `..`, 0 separadores inversos en los nombres normalizados |
| Manifiesto C11-C | aparece exactamente una vez; 796,318 bytes; SHA-256 canónico `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953` |
| Identidad de origen declarada | commit `be5d04c64080723e5f53d651109e45db07c43054` |

El inventario declara 3,716 archivos del checkout, tres evidencias compactas y un README del snapshot (3,720 entradas antes de añadir el manifiesto del propio snapshot). La suma descomprimida es aproximadamente 28.27 MB incluyendo el manifiesto del snapshot, frente a 9.19 MB comprimidos. Esto concuerda con una exportación de contexto pequeña; no es el freeze canónico.

## 2. Tree fingerprint

`context_tree_sha256` declarado: `e7378235e719605fd89d601609ed34e2db9b92fc84c08de2bb7313c31187549e`. Se recalculó sobre las filas `path<TAB>bytes<TAB>sha256`, UTF-8, LF final, usando exactamente el orden serializado en la lista `files` del manifiesto interno: **MATCH**.

La ordenación no debe rehacerse con el sort de otra cultura/locale si se quiere reproducir este fingerprint. Para próximas versiones, una mejora útil es declarar explícitamente que el orden viene del array de inventario serializado o fijar una comparación ordinal multiplataforma; no afecta a la verificación individual ya completada de esta versión.

## 3. Dictamen

**SNAPSHOT STRUCTURAL VALIDATION = PASS_FOR_CONTEXT_TRANSFER.** Los hashes por archivo, el ZIP, el sidecar y el informe se concilian; el manifiesto C11-C permanece intacto y único. Es adecuado para estudiar y clasificar la documentación/código del proyecto.

No representa un checkout activo ni prueba que todos los archivos excluidos estén ausentes de la máquina. No debe extraerse sobre el checkout, no es un freeze ni un release, no aprueba el renderer D ni concede autoridad de producción/promoción. Los cambios posteriores deben hacerse sobre la checkout activa de Windows y verificar sus pins.

## 4. Hallazgos de volumen y organización

En este snapshot:

- `docs/current/d`: 565 archivos.
- `docs/history/c11d`: 35 archivos.
- `docs/history/master-prompts/c11d`: 52 archivos.
- `prompts/` con nombre C11-D: 93 archivos.
- `docs/master-prompts/` con nombre C11-D: 37 archivos.
- `tools/c11d/d9`: 276 archivos; muchos son propuestas, schemas y auditorías incrementales.

No conviene mover cientos de registros/versiones automáticamente: hay referencias por ruta en manifests, prompts, JSON de gates, hashes y recibos. La organización propuesta es un catálogo de navegación generado que clasifica tema y linaje, conserva las rutas originales y evita afirmar que una versión antigua está supersedida solo por fecha o nombre.

## 5. Frontera funcional encontrada para la siguiente tarea

El camino físico heredado C se ejecuta a través de `tools/qa/c11/run_c11c_challenge_bulk_qa.ps1` y `tools/prototypes/c11c_bulk/run_c11c_challenge_production.ps1`; Producer `GENERAR` también usa los runners C. La ruta D de `c11c_gui_request.py`/`universal_producer.py`/`editorial_render_bridge.py`/`d_render_adapter.py` crea request/plan/envelope de inspección y sigue sin emitir input de renderer. La tarea funcional pendiente es identificar y conectar —en un slice D separado y gobernado— el valor editorial visible en el compositor y después el camino A/V, conservando C y las semillas aisladas.

El gate AD está validado pero sin decisión de operador: no correr el renderer D ni crear un MP4 D hasta que la autoridad exacta y gates posteriores lo permitan. Continuar ingeniería no modifica esta situación.
