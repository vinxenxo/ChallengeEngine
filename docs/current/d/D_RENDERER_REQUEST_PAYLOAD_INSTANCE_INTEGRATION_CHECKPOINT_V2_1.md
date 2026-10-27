# C11-D — Request→Payload Instance Integration Checkpoint V2.1

**Fecha:** 27-10-2026  
**Estado:** `GUARD_BUGFIX_PREPARED_SANDBOX_12_OF_12_WINDOWS_RUNTIME_RETEST_PENDING`  
**Predecesor:** `D_RENDERER_REQUEST_PAYLOAD_INSTANCE_INTEGRATION_CHECKPOINT_V2.md`  
**Ledger acumulativo:** `C11D_ENGINEERING_PHASE_LEDGER_20261027_V1.md`

## 1. Resultado del intento de runtime V2 original

Windows verificó Godot Mono `4.7.1.stable.mono.official.a13da4feb`, exit code `0`. Los harnesses de materialización in-memory de Visual Loop/Drill y Challenge se ejecutaron y emitieron sus marcadores PASS, pero la composición solicitud→payload se detuvo antes de emitir el recibo V2 integrado:

```text
C11-D REQUEST-PAYLOAD INSTANCE INTEGRATION V2 FAIL | Dynamic binder receipt schema/status/admission mismatch | renderer=OFF | media_created=false | candidate_input_admissible=false | D4.8=BLOCKED | release_authority=NONE
V2_RUNTIME_EXIT_CODE=1
RUNTIME_STDOUT_SHA256=4c0436069f9c0c8010a33b654ef233511cbc3caf09482572d55ca1ccdc5592fc
RUNTIME_STDERR_SHA256=e5eed2ae6854c661e8e16643f84be6445c9156f1aa7fafbb0b27359d799465ee
```

Evidencia aportada por el operador: `%TEMP%\C11D_REQUEST_PAYLOAD_INTEGRATION_V2_RUNTIME_20261027`. El resultado es **FAIL**, no aceptación parcial del join. Los PASS individuales de los harnesses son evidencia acotada anterior y no sustituyen el recibo integrado.

## 2. Causa raíz

El recibo real de `d_renderer_dynamic_request_payload_binding.py` cumple su schema estricto V1: el valor `candidate_input_admissible=false` pertenece a `readiness`, no a la raíz del recibo. El join V2 consultaba un campo raíz que no existe, convirtiendo la ausencia en fallo. El fixture sintético del test original reflejaba erróneamente esa misma raíz y omitía el campo anidado; por eso las 10 pruebas anteriores no detectaron el problema.

## 3. Cambios exactos de esta corrección

- Runner V2: leer `readiness` como mapping, comprobar `readiness.candidate_input_admissible is false` y comprobar `readiness.video_render_ready is false` dentro de la misma sección.
- Test V2: modelar el recibo dinámico real sin `candidate_input_admissible` de nivel raíz; mover el estado al objeto `readiness`.
- Regresión positiva: aceptar una forma válida de recibo V1 con ambos flags anidados.
- Regresiones negativas: rechazar `readiness.candidate_input_admissible=true` y rechazar una sección `readiness` ausente.
- Ledger: registrar el runtime fallido, los hashes de logs, la causa raíz y la siguiente puerta pendiente.

La corrección no modifica el dynamic binder V1 ni contratos/esquemas upstream. No relaja la política: un flag ausente o `true` sigue fallando cerrado. Tampoco cambia fuentes fijadas por los 60 source pins, nombres de digest, selectores, seeds, manifiesto C11-C ni políticas de renderer.

## 4. Validación previa al overlay

La versión corregida se probó en el sandbox aislado:

```text
Ran 12 tests
OK
```

Incluye el join válido con la forma real del recibo, la mutación adversa del flag anidado y `readiness` ausente. Este resultado **no es** aceptación Windows ni aceptación de runtime Godot corregido.

## 5. Siguiente comando en Windows

Después de aplicar y verificar el overlay correctivo, ejecutar solo el test focalizado:

```powershell
python -B .\tools\c11d\d9\test_d_renderer_request_scoped_payload_materialization_binding_v2.py
if ($LASTEXITCODE -ne 0) { throw 'V2.1 request-payload integration unit test failed.' }
```

Requisito: `Ran 12 tests`, `OK`, exit code `0`. Solo tras ese resultado se repetirá el runner con Godot 4.7.1 Mono, stdout/stderr separados y un directorio de evidencias nuevo. No reusar la carpeta del runtime fallido. No repetir la propuesta V1 ni V2B 402/402.

## 6. Invariantes permanentes

- C11-C 2.19.12 y su manifiesto permanecen inmutables: SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`, 796318 bytes.
- `renderer=OFF`; `media_created=false`; `candidate_input_admissible=false`; `D4.8=BLOCKED`; `D9.10=PREPARE_ONLY`; `D9.14/D9.16=BLOCKED`; `D9.17=BLOCKED_NO_GO`; `D10=BLOCKED_FOR_PROMOTION`; `baseline_approval=MISSING`; `freeze_eligible=false`; `release_authority=NONE`.
- No recibo JSON persistido, manifest de payload persistido, renderer input, dispatch, píxeles ni medios.
- La integración conserva dos namespaces de digest distintos y no afirma equivalencia entre `dynamic_payload_sha256` y `legacy_payload_instance_sha256`.
- Editorial sidecar: se verifica el join de 14 valores; el consumo por payload sigue `0/14`.
- Un eventual PASS de runtime únicamente verifica joins de identidad/procedencia in-memory; no cierra políticas de presentación, timeline/timebase, audio, autorización o admisibilidad de candidate input.
