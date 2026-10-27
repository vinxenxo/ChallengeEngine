# C11-D — Runtime Receipt Guard Fix Overlay V1

**Fecha:** 27-10-2026  
**Modo:** reemplazo controlado con precondiciones hash + dos destinos add-only  
**Workstream:** unión canónica solicitud → payload instance → editorial sidecar  
**Reglas:** no sobrescribir si los hashes base difieren; backup previo; parar ante primer fallo.

## Motivo

La primera ejecución real del runner V2 llegó correctamente a ambos harnesses de materialización en memoria y falló durante el join del recibo dinámico. El fallo no era una contradicción de política: el código V2 leía `candidate_input_admissible` desde el nivel raíz, pero el contrato/schema V1 lo define bajo `readiness`. El test sintético V2 anterior no replicaba fielmente la forma del recibo de producción y dejó pasar el bug.

## Corrección y cobertura

El runner ahora valida el campo anidado, exige `readiness` como mapping y conserva tanto `candidate_input_admissible=false` como `video_render_ready=false`. El test construye un recibo sintético con la forma del contrato real, prueba un join válido, rechaza la mutación de admisión y rechaza `readiness` ausente. No se cambia la implementación ni el contrato del binder V1; no se aflojan comprobaciones ni se cambia el scope.

Preparación aislada posterior a la corrección: `12 tests`, `OK`. Esta cifra solo describe sandbox. El operador debe validar el mismo test en Windows y ejecutar de nuevo el runtime para obtener una aceptación real.

## Destinos del overlay

Reemplazos controlados:

- `tools/c11d/d9/d_renderer_request_scoped_payload_materialization_binding_v2.py`
- `tools/c11d/d9/test_d_renderer_request_scoped_payload_materialization_binding_v2.py`
- `docs/current/d/C11D_ENGINEERING_PHASE_LEDGER_20261027_V1.md`

Nuevas adiciones (deben estar ausentes antes de aplicar):

- `docs/current/d/D_RENDERER_REQUEST_PAYLOAD_INSTANCE_INTEGRATION_CHECKPOINT_V2_1.md`
- Este documento.

Los hashes `before_sha256` y `after_sha256`, tamaños y el SHA/bytes del manifiesto C11-C quedan declarados en `OVERLAY_MANIFEST.json`, incluido dentro del ZIP.

## Secuencia obligatoria en checkout Windows

1. Verificar SHA-256 del ZIP entregado.
2. Verificar C11-C: SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`; tamaño `796318` bytes.
3. Comprobar los tres hashes previos de reemplazo y que los dos destinos nuevos no existan. Si cualquiera difiere, detenerse; no forzar.
4. Crear backup de los tres reemplazos, aplicar cinco destinos del manifiesto con validación de hashes después de copiar y volver a verificar C11-C.
5. Ejecutar el test focalizado V2 corregido (12/12, exit `0`). No lanzar runtime si falla.
6. Solo tras el PASS unitario, ejecutar el runtime V2 con Godot `4.7.1.stable.mono.official.a13da4feb` y stdout/stderr separados a un directorio nuevo.
7. Aceptar el runtime solo si el propio runner emite un resumen `... V2 PASS` y un recibo JSON completo y autoconsistente. Si aparece otro FAIL, conservar evidencia y corregir la siguiente arista mediante overlay versionado y documentado.

## Límites no modificados

`renderer=OFF`; `media_created=false`; `candidate_input_admissible=false`; `D4.8=BLOCKED`; `release_authority=NONE`. C11-C sigue siendo el baseline autoritativo e inmutable. La corrección no autoriza payload persistido, renderer input, dispatch, pixels/media, aprobación de políticas, freeze ni promoción.
