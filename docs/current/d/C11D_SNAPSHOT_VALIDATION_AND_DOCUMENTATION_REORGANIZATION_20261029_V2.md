# C11-D — Validación del snapshot y reorganización documental V2

**Fecha:** 29-10-2026. **Fuente:** snapshot que el operador subió tras instalar el empaquetador de estilo C11-C.

## Validación independiente del snapshot anterior

Archivo: `C11D_WORKING_CONTEXT_20261029_193950.zip`  
SHA-256 declarado y observado: `5b8d06ad82bca798c94db03f943a85afb309d91484d4499ed40fed36056ca774`  
Tamaño: 9.190.399 bytes  
Entradas ZIP: 3.721; duplicados exactos/case-insensitive: 0; CRC: PASS.  
Inventario: 3.720 entradas de payload, todas con tamaño y SHA-256 coincidentes con el manifiesto interno.  
Manifiesto C11-C: `release/C11C_FREEZE_PACKAGE_MANIFEST.json`, una aparición, 796.318 bytes, SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.  
Huella de árbol: `e7378235e719605fd89d601609ed34e2db9b92fc84c08de2bb7313c31187549e`, reproducible con las filas `path<TAB>bytes<TAB>sha256` en el orden serializado en `C11D_CONTEXT_SNAPSHOT_MANIFEST.json`, UTF-8, separador LF y LF final.

La comprobación del sidecar `.sha256`, el informe `.report.json`, los hashes por fichero y el árbol da PASS. Este archivo es el snapshot pre-migración y debe considerarse antecedente después de producir el nuevo.

## Auditoría de documentación de raíz

Se inspeccionó el contenido de raíz de ese ZIP. Había 121 Markdown de raíz contando `AGENTS.md` y `README.md`, 120 candidatos de D/metadata tras excluir esas dos entradas convencionales, y manifiestos JSON de overlays relacionados. Los candidatos eran principalmente README de overlays históricos, además del checkpoint/handover D9.10 y metadata del snapshot.

La auditoría confirmó que dos README de D aparecen en la lista del manifiesto C11-C y deben permanecer en raíz. También hay README referenciados por manifiestos históricos o por registros de continuidad/decisión actuales. No se permite moverlos a ciegas. La política V1 archiva solo candidatos no fijados ni referenciados, y publica las excepciones por ruta y hash.

## Herramienta/flujo de test entregados

- `tools/c11d/documentation/organize_c11d_root_documentation.ps1`: preflight/apply, clasificación por tema y mapa generado. No reescribe contenido.
- `tools/c11d/documentation/organize_c11d_documentation.ps1`: catálogo live; ahora indexa también `docs/history/d` y la metadata D que permanezca en raíz.
- `tools/c11d/documentation/Test-C11DDocumentationReorganization.ps1`: prueba de scripts/pins; aplica migración opcional, regenera catálogo y puede generar el snapshot siguiente.
- `tools/c11d/packaging/Test-C11DWorkingSnapshot.ps1`: lectura independiente del ZIP, CRC/entradas únicas, hashes de cada payload, hash de árbol, sidecar/reporte y presencia del catálogo/mapa/prompt de continuidad.

## Test completo para obtener el snapshot de la siguiente ventana

```powershell
& .\tools\c11d\documentation\organize_c11d_root_documentation.ps1 -PreflightOnly
& .\tools\c11d\documentation\Test-C11DDocumentationReorganization.ps1 -ApplyRootMigration -GenerateSnapshot
```

El test runner repite el preflight antes de escribir, aplica solo si no hay conflictos, confirma hash de los documentos desplazados y de los pins, regenera catálogo, vuelve a comprobar el preflight de snapshot, genera un ZIP nuevo con nombre timestamp y llama a `Test-C11DWorkingSnapshot.ps1`. El resultado esperado final incluye `C11D_DOCUMENTATION_OVERLAY_TESTS=PASS_INCLUDING_NEW_SNAPSHOT` y la ruta/hash del nuevo ZIP.

Sube los tres archivos del nuevo snapshot (`.zip`, `.zip.sha256`, `.zip.report.json`) a la siguiente ventana. Nunca extraigas el ZIP sobre el checkout activo.

## Límites de esta evidencia

La validación del snapshot acredita la integridad del paquete de contexto, no la aceptación D. No ejecuta renderer, no produce MP4 D y no concede autoridad de baseline. C11-C 2.19.12 permanece inmutable; Phase AD y los gates técnicos conservan su estado explícito en los pins del checkout.


La huella agregada `context_tree_sha256` se reproduce recorriendo `manifest.files` en el orden serializado definido por el empaquetador y calculando SHA-256 sobre las filas `path<TAB>bytes<TAB>sha256` separadas por LF, incluida la LF final.
