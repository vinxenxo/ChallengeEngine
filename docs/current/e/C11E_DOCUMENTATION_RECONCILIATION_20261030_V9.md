# C11-E — reconciliación documental (V9)

Este registro continúa V8 sin reescribir evidencias ni versiones anteriores.

## E1

Los recibos Windows aportados el 2026-10-30 confirman instalación de ocho archivos, pruebas Producer 2/2 PASS, Python 3.13.14, rama `main`, HEAD base E1 `bc8330e` y manifiesto C11-C exacto. El operador consolidó después la fundación E1 en el commit `a3c7c5d`, padre `bc8330e`; diff 28 paths, árbol limpio y rama `main` ahead 1 de `origin/main`. Los source pins del receipt corresponden a los archivos del commit.

## E2 V2/V3

- V2 esperaba `bc8330e` como HEAD y fue rechazado contra `a3c7c5d`; no escribió ni lanzó renderer.
- V3 corrigió el pin de HEAD, verificando `a3c7c5d`, padre `bc8330e`, receipts E1 y source pins.
- V3 falló en `Assert-SafeRelativePath`: el prefijo de checkout se construyó concatenando un literal de dos backslashes, de modo que `StartsWith()` no coincidía con la ruta absoluta válida. Falló antes de la primera escritura; el runner indicó que Godot no fue invocado.
- V4 normaliza el root absoluto, emplea exactamente un `DirectorySeparatorChar` al delimitar el prefijo y convierte `/` a `DirectorySeparatorChar` en el destino. Conserva checks de rooted path, traversal, reparse points y preflight completo.

## Errores de ejecución prevenidos

Los scripts anteriores también enseñaron que PowerShell 5.1 exige que `if/elseif/else` permanezcan en un mismo bloque pegado. El wrapper debe capturar `$LASTEXITCODE` inmediatamente y salir ante fallo; no imprimir mensajes PASS por una rama independiente. Los paquetes se entregan como ZIP autocontenido con nombres/rutas exactos.

## Estado

E1 automatizado PASS; GUI manual pendiente. E2 V4 no está aplicado ni ejecutado hasta recibir receipt Windows. Las copias históricas, el manifiesto congelado C y los registros D siguen inmutables.
