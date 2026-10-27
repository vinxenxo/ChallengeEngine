# C11-D — Editorial Hash Namespace Fix Overlay V1

**Fecha:** 27-10-2026  
**Overlay ID:** `C11D_REQUEST_PAYLOAD_V2_EDITORIAL_HASH_NAMESPACE_FIX_OVERLAY_20261027_V1`  
**Modo:** guarded replacements + add-only documentation  
**Estado:** preparación verificada en sandbox; aplicación Windows y runtime pendientes.

## 1. Defect addressed

Después de que el guard de recibo V2.1 pasara sus 12 tests Windows, el runtime volvió a ejecutar Godot 4.7.1 Mono y ambos harnesses in-memory. El join falló con `Canonical editorial hash does not join to the sidecar: challenges`, exit code `1`.

Evidencia del intento fallido (conservar; no sobrescribir):

- Carpeta: `%TEMP%\C11D_REQUEST_PAYLOAD_INTEGRATION_V2_1_RUNTIME_20261027`.
- Godot: `4.7.1.stable.mono.official.a13da4feb`, comprobación `--version` exit `0`.
- Runtime exit: `1`.
- stdout SHA-256: `4c0436069f9c0c8010a33b654ef233511cbc3caf09482572d55ca1ccdc5592fc`.
- stderr SHA-256: `a863b8582f41dcf099073953466e3cbfa2f0c9bbc4e2ee6f937943279161e4ab`.

## 2. Exact root cause

El campo `source_identity.editorial_hash` tiene namespace compuesto: `SHA256({selection: full canonical selection, editorial: canonical editorial map})`. El campo `carrier.editorial_values_sha256` tiene namespace map-only: `SHA256(editorial map)`. El guard los comparaba directamente. La comparación era conceptualmente incorrecta aunque los valores fueran correctos. La sección `digest_semantics.editorial_values_sha256` del contrato V2 también describía incorrectamente igualdad directa; este overlay corrige esa declaración.

## 3. Implementation change

- Ejecuta `dynamic.evaluate_universal_request` para cada request fijo, sin persistencia, para obtener la selección canónica completa.
- Reconstruye el mapa del sidecar a partir de sus campos hash-bound y verifica cada `value_sha256` y el hash agregado map-only.
- Comprueba igualdad exacta del mapa sidecar con el mapa editorial canónico.
- Reconstruye el digest compuesto usando la selección completa más los valores recuperados del sidecar y lo compara con el `editorial_hash` canónico.
- Conserva ambos digests bajo nombres y namespaces separados en el recibo.
- Añade regresiones para los tres requests canónicos, sidecar alterado con hashes recalculados y selección canónica modificada.
- Actualiza el schema estricto y la semántica del contrato. El conteo de pines fuente sigue siendo exactamente 60; el manifiesto congelado C11-C sigue siendo la primera autoridad inmutable.

No afloja la comparación de campos ni elimina verificación de hash. No cambia el binder V1, las decisiones aprobadas, los selectores, los seeds, ni ninguna política renderer.

## 4. Artifact changes

Reemplazos protegidos por SHA-256 previo:

1. `tools/c11d/d9/d_renderer_request_scoped_payload_materialization_binding_v2.py`
2. `tools/c11d/d9/test_d_renderer_request_scoped_payload_materialization_binding_v2.py`
3. `definitions/c11d/production/D_RENDERER_REQUEST_SCOPED_PAYLOAD_MATERIALIZATION_BINDING_V2.json`
4. `definitions/c11d/production/D_RENDERER_REQUEST_SCOPED_PAYLOAD_MATERIALIZATION_BINDING_SCHEMA_V2.json`
5. `docs/current/d/C11D_ENGINEERING_PHASE_LEDGER_20261027_V1.md` (ledger acumulativo; conserva todo el historial anterior y añade este incidente)

Destinos add-only (deben no existir al aplicar):

6. `docs/current/d/D_RENDERER_REQUEST_PAYLOAD_INSTANCE_INTEGRATION_CHECKPOINT_V2_2.md`
7. `docs/current/d/C11D_REQUEST_PAYLOAD_V2_EDITORIAL_HASH_NAMESPACE_FIX_OVERLAY_20261027_V1.md`

El manifiesto del ZIP contiene hashes `before_sha256`, `after_sha256` y bytes para cada destino. La aplicación debe crear respaldo verificado de los cinco reemplazos, detenerse ante la primera precondición fallida y comprobar los hashes finales.

Hashes SHA-256 finales de los cuatro artefactos de código/contrato:

- Runner V2: `709d5ff670561d2bfc8b5926ba616b6773589bb783dc10f767354b26c3c62cbd`.
- Test V2: `120b99b58e4ba09ff74c01a5f1acf57252353d61a659aaa440723436f5900da6`.
- Contrato V2 corregido: `0c3f03cbfa3990e093ccbc3e74f777f8f537682570e75cc304b393c2a6eb1100`.
- Schema de salida V2 corregido: `e1b586f4ec4abc31ca92e2ebdbdbaa293c17efb9493b0385f1af79e652dfc83f`.

## 5. Verification / current status

- Sandbox: `16/16` tests passed, including full canonical hash reconstruction for `challenges`, `visual_loops` and `visual_drills`.
- Windows: V2.1 unit test passed `12/12`; Windows V2.1 runtime failed at the editorial namespace guard above.
- Windows V2.2 focused test: pending overlay application.
- Windows V2.2 Godot runtime: not run.

The overlay is not considered accepted until applied and verified in the active Windows checkout and a real runtime produces a validated integrated receipt. No claim of runtime acceptance is made here.

## 6. Governance

C11-C 2.19.12 remains immutable and authoritative. `renderer=OFF`; `media_created=false`; `candidate_input_admissible=false`; `D4.8=BLOCKED`; `release_authority=NONE`; `baseline_approval=MISSING`; `freeze_eligible=false`. Editorial text remains in the sidecar; visual consumption stays `0/14`. No payload/receipt output files, renderer-native input, dispatch, pixels, media, freeze or promotion are authorized.
