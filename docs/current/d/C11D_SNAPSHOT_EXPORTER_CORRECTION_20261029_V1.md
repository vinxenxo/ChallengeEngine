# Corrección del exportador de snapshots C11-D — V1

**Fecha:** 29 de octubre de 2026  
**Tipo:** corrección de utilidad de empaquetado; no es una gate de render ni un artefacto de release.

## Motivo

La utilidad V2 tenía dos scripts para la misma operación: `New-C11DWorkingSnapshot.ps1` era un lanzador y `export_c11d_working_snapshot.ps1` materializaba una copia temporal del árbol antes de comprimirla. En el checkout activo, el copiado falló en una ruta larga dentro de `artifacts/qa/c11c_one_video_each_type/...`, antes de crear el ZIP final. El preflight sí había pasado y el manifiesto C11-C se había validado.

## Cambio

Se sustituye el lanzador por una única implementación autónoma que escribe los archivos directamente como entradas ZIP. La verificación vuelve a leer todas las entradas comprimidas, compara SHA-256 y tamaño con el inventario, exige rutas únicas y comprueba que el manifiesto congelado C11-C aparece una sola vez con SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953` y 796.318 bytes. Esto elimina la copia intermedia de 22.000+ archivos y la causa inmediata del fallo observado.

## Aplicación controlada

La reparación reemplaza `tools/c11d/packaging/New-C11DWorkingSnapshot.ps1` y retira `tools/c11d/packaging/export_c11d_working_snapshot.ps1` **solo si ambos conservan los SHA-256 exactos publicados por el overlay V2**. Si cualquiera difiere, la reparación se detiene sin sobrescribirlo. No modifica `AGENTS.md`, `CONTINUE.md`, el manifiesto congelado C11-C, el ledger ni el checkpoint.

## Uso

Desde la raíz del checkout:

```powershell
& .\tools\c11d\packaging\New-C11DWorkingSnapshot.ps1
```

El ZIP, el `.sha256` y el `.report.json` se guardan fuera del checkout, en `Desktop\C11D_CONTEXT_EXPORT`. `-PreflightOnly` sigue disponible para el inventario sin crear archivos.

## Límites

El snapshot es una exportación filtrada de contexto de trabajo; no es freeze, release, baseline D ni evidencia de aceptación de vídeo. La ejecución de la utilidad reparada debe verificarse en el checkout Windows real.
