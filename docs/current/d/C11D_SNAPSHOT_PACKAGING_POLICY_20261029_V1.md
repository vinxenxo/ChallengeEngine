# Política de empaquetado del snapshot C11-D — estilo C11-C freeze

**Fecha:** 29 de octubre de 2026  
**Tipo:** corrección de empaquetado de contexto; no es un freeze ni un gate de render.

## Hallazgo

La herramienta de snapshot anterior excluía solamente `artifacts/production`, `artifacts/releases` y un conjunto reducido de medios de revisión. Como consecuencia, incorporó corpus QA y salidas generadas desde otras ramas de `artifacts/`, y produjo el 29 de octubre de 2026 un archivo de 9.333.452.157 bytes con 22.047 entradas.

El mecanismo C11-C de referencia es `tools/maintenance/create_c11c_freeze_zip.ps1`, invocado por `c11c-suite/c11c-maintenance/run_freeze_package.bat`. Su higiene de contenido excluye todo directorio `artifacts`, cachés/build outputs, archivos temporales y archivos ZIP/7z/RAR anidados; además genera inventario de ruta, tamaño y SHA-256 y valida el ZIP terminado.

## Cambio en esta versión

`tools/c11d/packaging/New-C11DWorkingSnapshot.ps1` es una sola implementación autónoma. Escribe directamente en las entradas ZIP, sin materializar primero una copia temporal del árbol. Sigue la higiene tipo C11-C y añade filtros para medios binarios generados, archivos locales de entorno/credenciales y ficheros excesivamente grandes (más de 100 MiB por fichero por defecto). El tamaño final del ZIP tiene además un límite predeterminado de 256 MiB; si se supera, el proceso aborta y elimina el ZIP parcial.

Para no perder la evidencia compacta de mayor valor, puede incluir en un namespace separado `C11D_CONTEXT_EVIDENCE/`:

- `artifacts/tests/reports/C11C_2.19.12_ACCEPTANCE_REPORT.json`, si existe;
- `artifacts/prototypes/c11c_art_direction_review/C11-C_COMPLETE_VIDEO_REVIEW_REPORT.json`, si existe;
- archivos JSON/Markdown/TXT/CSV de `artifacts/evidence/d9_15_operator/`, limitados a 10 MiB por archivo.

No incluye el corpus de vídeos, frames ni los manifiestos de los resultados QA de `artifacts/qa/`.

## Manifiestos e integridad

- El archivo activo `release/C11C_FREEZE_PACKAGE_MANIFEST.json` se copia desde el checkout sin reconstruirlo y debe aparecer exactamente una vez en el ZIP con SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953` y tamaño 796.318 bytes.
- El manifiesto del snapshot se ubica en la raíz como `C11D_CONTEXT_SNAPSHOT_MANIFEST.json`; no se reutiliza el nombre del manifiesto de C11-C ni se añade una segunda entrada con esa ruta.
- Se leen todas las entradas del ZIP, se verifican tamaños y SHA-256, unicidad de rutas y CRC antes de publicar el archivo final.
- Se emiten un `.sha256` y un `.report.json` externos. El límite de salida se puede ajustar con `-MaxArchiveMiB`; el límite por fichero se puede ajustar con `-MaxFileMiB`.
- El modo `-PreflightOnly` no escribe archivos.

## Uso

Desde la raíz del checkout:

```powershell
& .\tools\c11d\packaging\New-C11DWorkingSnapshot.ps1 -PreflightOnly
& .\tools\c11d\packaging\New-C11DWorkingSnapshot.ps1
```

El primer comando es opcional. La segunda orden crea el snapshot final y sus comprobantes en `Desktop\C11D_CONTEXT_EXPORT`.

## Límites

Este ZIP es un snapshot filtrado de código, configuración, pruebas y documentación del checkout de trabajo. No sustituye al checkout activo, no constituye un release ni un freeze, no demuestra aceptación audiovisual D y no concede permiso para activar el renderer o promover el baseline. Nunca debe extraerse por encima del checkout activo.
