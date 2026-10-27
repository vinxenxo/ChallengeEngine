# C11-D — Request→Payload Instance Integration Checkpoint V2.2

**Fecha:** 27-10-2026  
**Estado:** `EDITORIAL_HASH_NAMESPACE_FIX_PREPARED_SANDBOX_16_OF_16_WINDOWS_APPLY_AND_RUNTIME_PENDING`  
**Predecesor:** `D_RENDERER_REQUEST_PAYLOAD_INSTANCE_INTEGRATION_CHECKPOINT_V2_1.md`  
**Ledger acumulativo:** `C11D_ENGINEERING_PHASE_LEDGER_20261027_V1.md`

## 1. V2.1 Windows runtime result — not accepted

El operador confirmó primero el test V2.1 en el checkout Windows:

```text
V2_1_TEST_EXIT_CODE=0
C11D_REQUEST_PAYLOAD_V2_1_UNIT_TEST=PASS
UNIT_TESTS=12/12
```

El runtime posterior verificó Godot Mono `4.7.1.stable.mono.official.a13da4feb` y ejecutó ambos harnesses in-memory, pero el join de integración falló al unir el hash editorial de Challenge:

```text
C11-D REQUEST-PAYLOAD INSTANCE INTEGRATION V2 FAIL | Canonical editorial hash does not join to the sidecar | renderer=OFF | media_created=false | candidate_input_admissible=false | D4.8=BLOCKED | release_authority=NONE
V2_1_RUNTIME_EXIT_CODE=1
RUNTIME_STDOUT_SHA256=4c0436069f9c0c8010a33b654ef233511cbc3caf09482572d55ca1ccdc5592fc
RUNTIME_STDERR_SHA256=a863b8582f41dcf099073953466e3cbfa2f0c9bbc4e2ee6f937943279161e4ab
```

Log folder: `%TEMP%\C11D_REQUEST_PAYLOAD_INTEGRATION_V2_1_RUNTIME_20261027`. No se emitió recibo integrado. Los PASS de los harnesses individuales no significan que el join V2 haya pasado.

## 2. Root cause — two different editorial digest namespaces

El guard V2.1 hacía esta comparación inválida:

`source_identity.editorial_hash == carrier.editorial_values_sha256`

Pero ambos campos describen objetos distintos:

- El productor canónico calcula `editorial_hash = SHA256({"selection": full_canonical_selection, "editorial": canonical_editorial_map})`. La selección completa incluye `content_type`, `family_id`, `subtype_id`, `variant_id`, `variant_scope_id` y `difficulty_tier`.
- El carrier calcula `editorial_values_sha256 = SHA256(editorial_map)`. Es un digest del mapa editorial solamente.

Por tanto, la desigualdad entre ambos hashes no demuestra corrupción. El contrato V2 inicial también describía incorrectamente que debían ser iguales, y se corrige en esta revisión. No se debe solucionar quitando la comprobación del sidecar ni declarando que estos hashes pertenecen al mismo namespace.

## 3. Correction design

El runner V2 corregido conserva las verificaciones existentes de receipt/self-hash, manifest, request, selector, plan, linaje, seeds, perfiles y límites de gobernanza. Para el editorial join:

1. Reevalúa, en memoria, cada uno de los tres requests fijos con el productor canónico y retiene la selección completa y el mapa editorial canónico.
2. Reconstruye el mapa editorial desde los `fields` del sidecar; exige nombres únicos, valores de texto, SHA-256 correcto por campo y digest de mapa correcto.
3. Exige igualdad exacta entre el mapa reconstruido desde el sidecar y el mapa editorial canónico.
4. Calcula independientemente `SHA256({"selection": full_canonical_selection, "editorial": reconstructed_sidecar_map})` y exige que coincida con el `editorial_hash` del productor y del dynamic binder.
5. Publica por separado `editorial_values_sha256`, `canonical_editorial_sha256` y `canonical_editorial_reconstructed_sha256`, con identificadores explícitos de namespace. No los confunde ni infiere equivalencia por nombre.

El schema estricto del recibo se amplía para exigir esos campos y el nuevo marcador de join. El contrato V2 documenta la distinción entre digest map-only y digest compuesto.

## 4. Validation before Windows application

En una copia aislada con las 60 fuentes actuales fijadas y el manifiesto C11-C correcto, el test actualizado pasó:

```text
Ran 16 tests
OK
```

Incluye el hash compuesto reconstruido para los tres requests canónicos reales, aceptación del join válido con namespaces distintos, rechazo de alteraciones de valores aunque se recalculen los hashes del sidecar, rechazo de mutaciones de la selección completa, pins 60/60 y todos los negativos V2. Este resultado es **sandbox PASS**, no aceptación Windows ni aceptación runtime Godot.

Hashes SHA-256 de los destinos técnicos que define este overlay:

| Archivo | SHA-256 después del cambio |
|---|---|
| `tools/c11d/d9/d_renderer_request_scoped_payload_materialization_binding_v2.py` | `709d5ff670561d2bfc8b5926ba616b6773589bb783dc10f767354b26c3c62cbd` |
| `tools/c11d/d9/test_d_renderer_request_scoped_payload_materialization_binding_v2.py` | `120b99b58e4ba09ff74c01a5f1acf57252353d61a659aaa440723436f5900da6` |
| `definitions/c11d/production/D_RENDERER_REQUEST_SCOPED_PAYLOAD_MATERIALIZATION_BINDING_V2.json` | `0c3f03cbfa3990e093ccbc3e74f777f8f537682570e75cc304b393c2a6eb1100` |
| `definitions/c11d/production/D_RENDERER_REQUEST_SCOPED_PAYLOAD_MATERIALIZATION_BINDING_SCHEMA_V2.json` | `e1b586f4ec4abc31ca92e2ebdbdbaa293c17efb9493b0385f1af79e652dfc83f` |

## 5. Next gates

1. Aplicar `C11D_REQUEST_PAYLOAD_V2_EDITORIAL_HASH_NAMESPACE_FIX_OVERLAY_20261027_V1.zip` solo si el SHA-256 del ZIP, cada hash previo, todos los destinos add-only, los documentos V2.1 anteriores y el manifiesto C11-C coinciden.
2. Ejecutar el test focalizado del checkout Windows y exigir exit code `0`, `Ran 16 tests`, `OK`.
3. Solo después, lanzar el runner con Godot 4.7.1 Mono en un directorio nuevo `%TEMP%\C11D_REQUEST_PAYLOAD_INTEGRATION_V2_2_RUNTIME_20261027`. El intento previo debe conservarse como evidencia.
4. Aceptar la integración únicamente con un PASS inequívoco, recibo V2 íntegro con self-hash válido y verificaciones de schema, 3 joins canónicos, 3 payload manifest digests, sidecar 14/14 y consumo visual 0/14.
5. Tras runtime PASS, refrescar una sola vez el informe I/O y el inventario de identidad, y registrar sus nuevos hashes y salidas en el ledger.

## 6. Permanent governance locks

- Frozen C11-C SHA-256: `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`; bytes `796318`.
- `renderer=OFF`; `media_created=false`; `candidate_input_admissible=false`; `D4.8=BLOCKED`; `D9.10=PREPARE_ONLY`; `D9.14=BLOCKED`; `D9.16=BLOCKED`; `D9.17=BLOCKED_NO_GO`; `D10=BLOCKED_FOR_PROMOTION`; `baseline_approval=MISSING`; `freeze_eligible=false`; `release_authority=NONE`.
- No renderer-native input, dispatch, payload/receipt files, pixels or media are produced.
- Challenge coordinate projection and delivery resampling remain unresolved. Editorial values remain sidecar-only: `visual_payload_consumed=0/14`.
- No baseline acceptance, freeze, promotion, or C11-C replacement is authorized.
