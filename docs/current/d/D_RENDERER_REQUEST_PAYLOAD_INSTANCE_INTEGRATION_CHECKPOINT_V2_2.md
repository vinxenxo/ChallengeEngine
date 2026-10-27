# C11-D — Request→Payload Instance Integration Checkpoint V2.2

**Fecha:** 27-10-2026  
**Estado:** `V2.2_WINDOWS_PASS; IO_IDENTITY_REFRESH_PASS; CHALLENGE_SEED_COLLISION_EXPANSION_WINDOWS_PASS; V2B_STATIC_TESTS_PASS; V2B_RUNTIME_MATRIX_PENDING`  
**Predecesor:** `D_RENDERER_REQUEST_PAYLOAD_INSTANCE_INTEGRATION_CHECKPOINT_V2_1.md`  
**Ledger acumulativo:** `C11D_ENGINEERING_PHASE_LEDGER_20261027_V1.md`


## 0. V2.2 — aceptación real en Windows (27-10-2026)

**Estado:** `WINDOWS_PASS_RUNTIME_RECEIPT_VALIDATED; IO_IDENTITY_REFRESH_PASS; CHALLENGE_COLLISION_EXPANSION_PASS; V2B_STATIC_TESTS_PASS; V2B_RUNTIME_MATRIX_PENDING`.

Aplicación del overlay `C11D_REQUEST_PAYLOAD_V2_EDITORIAL_HASH_NAMESPACE_FIX_OVERLAY_20261027_V1.zip`:

- ZIP SHA-256: `b7ee45e2060258381d240b4aa5dfd14ff00f84c56fb2e65e84589fd546e37b5a`.
- `C11D_V2_2_EDITORIAL_HASH_FIX_APPLY=PASS`; reemplazos guardados `5/5`; documentos add-only `2/2`; los siete destinos de overlay verificados; manifiesto C11-C intacto.
- Backup Windows: `%TEMP%\C11D_V2_2_BACKUP_48a1a99795454f66a3e58b0e4fe452a7`.

Prueba focalizada Windows:

```text
Ran 16 tests
OK
V2_2_TEST_EXIT_CODE=0
C11D_REQUEST_PAYLOAD_V2_2_UNIT_TEST=PASS
UNIT_TESTS=16/16
TEST_STDOUT_SHA256=e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
TEST_STDERR_SHA256=3183ebabac73872621e28e140dc029fb9875826166ab85b7a0fe2687f6b7215f
```

Log de test: `%TEMP%\C11D_REQUEST_PAYLOAD_V2_2_TEST_20261027_46ad02316d824c46884fc1a6ec6f4a01`.

Runtime Godot Mono real:

- Ejecutable: `C:\Users\vinxe\AppData\Local\Microsoft\WinGet\Packages\GodotEngine.GodotEngine.Mono_Microsoft.Winget.Source_8wekyb3d8bbwe\Godot_v4.7.1-stable_mono_win64\godot.exe`.
- Versión capturada por stdout redirigido: `4.7.1.stable.mono.official.a13da4feb`; verificación de versión exit code `0`.
- Runtime exit code `0`; `C11D_REQUEST_PAYLOAD_V2_2_RUNTIME_VALIDATION=PASS`; `C11D_V2_2_PIPELINE=PASS`.
- Runtime stdout SHA-256: `00a0d51627618ae3ee167a7d2ca029f6ed5cd05ecf369f8d816ef5774d99051a`.
- Runtime stderr SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (vacío).
- Log/evidencia Windows: `%TEMP%\C11D_V2_2_RUNTIME_20261027_d2425963e21448bd9d04c2a044a7bea9`; recibo de evidencia JSON: `runtime_validation_evidence.json`.
- Receipt SHA-256: `1a2a729137458f633cf520c211180ce5a3fff2d21ed441e866ae0e1c946169af`.
- Identidad runtime: implementation `709d5ff670561d2bfc8b5926ba616b6773589bb783dc10f767354b26c3c62cbd`; test `120b99b58e4ba09ff74c01a5f1acf57252353d61a659aaa440723436f5900da6`; contract `0c3f03cbfa3990e093ccbc3e74f777f8f537682570e75cc304b393c2a6eb1100`; schema `e1b586f4ec4abc31ca92e2ebdbdbaa293c17efb9493b0385f1af79e652dfc83f`.

Resultado integrado validado por el runner y guardas del pipeline:

```text
C11-D REQUEST-PAYLOAD INSTANCE INTEGRATION V2 PASS | fixtures=3/3 | canonical_request_joins=3/3 | payload_manifest_digests=3/3 | editorial_sidecar_joins=3/3 | sidecar_fields=14/14 | visual_payload_consumed=0/14 | payload_digest_equivalence=NOT_CLAIMED | source_pins=60/60 | renderer=OFF | media_created=false | candidate_input_admissible=false | D4.8=BLOCKED | release_authority=NONE
```

Los tres joins corresponden a Challenge `parking_v2/CHALLENGE_004`, Loop `c11c_geometric_waves_v1/harmonic_membrane` y Drill `tracking/tier-2`. Los hashes editoriales compuesto y map-only se informan en namespaces diferenciados; ningún campo editorial se inyectó en el payload visual. La verificación de runtime no constituye render, inspección de píxeles ni admisibilidad de candidato.


## 0.1. Fase I — I/O gap e identidad refrescados en Windows (27-10-2026)

**Estado:** `WINDOWS_PASS_READ_ONLY_AUDITS; INPUT_READINESS_STILL_FAIL_CLOSED`.

Aplicación del overlay documental previo: `C11D_V2_2_POST_RUNTIME_OVERLAY_APPLY=PASS`; reemplazos guarded `2/2`; adiciones add-only `3/3`; `FROZEN_C11C_MANIFEST=UNCHANGED`. Backup verificado bajo `%TEMP%\C11D_V2_2_POST_RUNTIME_BACKUP_ccea0878ad16480db3277f5c1e4eb508`.

Directorio de evidencia de los informes, separado del repositorio: `%TEMP%\C11D_V2_2_POST_RUNTIME_AUDITS_20261027_6260c069a2114d4893f2d567b5308ed0`. Marcador de finalización: `%TEMP%\C11D_V2_2_POST_RUNTIME_GAP_IDENTITY_REFRESH_20261027.completed.json`. No se escribieron informes de candidato ni payloads en el checkout.

**Auditoría de gaps I/O (exit code 0):**

- Grupos inspeccionados: `10/10`; completos `0/10`; parciales `6`; bloqueados `4`.
- Source pins: `54/54`; `candidate_input_admissible=false`.
- `audit_sha256`: `b8c5d5994d349c1ce9fef518d7633f72565f3c927cd7bc51cdd89fe5d2df2fe2`.
- stdout SHA-256: `b3488932ec9075c42f1b505dd384b15c452834f0da0d4830e61a0567a527c677`.
- stderr SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (vacío).

**Inventario de identidad de candidato (exit code 0; identidad solamente, no autorización de baseline):**

- Archivos fuente: `164`; fingerprint: `0b4168bddac991ac03ea45d424f5af4fa2316c275dc31c1866c5cf8baf532d25`.
- `report_sha256`: `74e518b620d297c5e09cf6e9495864dbe96e9394b6520e9a5e492775642b92bf`.
- Python: `3.13.14`; Godot probe: `VERSION_PROBED`; Godot: `4.7.1.stable.mono.official.a13da4feb`.
- stdout SHA-256: `c9e21562264e5189fdbba76da215f5bac2db8b797b327f2404e95ff930e5c6cf`.
- stderr SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (vacío).

Los informes confirman integridad y cobertura de sus fuentes, no readiness: ningún grupo I/O está completo, el inventario sigue en `IDENTITY_ONLY_REVIEW_PACKET_NOT_BASELINE_READY` y la admisibilidad del input sigue siendo falsa.

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

## 5. Next gates — ordered after the accepted refresh

1. Run once, on the active Windows checkout, the read-only explicit-seed/numeric-collision rejection audit via `tools/c11d/d9/run_d_renderer_seed_domain_collision_audit_readonly.ps1`. Its source runner validates the pinned 23-source contract and the frozen C11-C manifest; the wrapper captures full stdout/stderr and validates `20/20` explicit-seed negative cases, `4/4` equal-value collisions rejected before Godot, and `runtime_invocations=0`.
2. Accept that gate only from the actual Windows exit code, report self-hash, separate log hashes and evidence directory. The preparation-tree result is not substituted for Windows evidence.
3. If the active-checkout audit passes, prepare the next bounded selector-coverage increment for canonical Challenge variants and Visual Loop families/grammars. Preserve fixed-seed/independence constraints, source pins and negative rejection checks; do not widen all selectors at once.
4. Do not re-run V2.2 tests/runtime or the post-runtime I/O/identity refresh while their pinned sources are unchanged. Do not execute Godot for the collision rejection audit: it is a preflight rejection test by contract.
5. Keep `renderer=OFF`, `media_created=false`, `candidate_input_admissible=false`, `D4.8=BLOCKED`, `D9.10=PREPARE_ONLY`, `D9.14/D9.16=BLOCKED`, `D9.17=BLOCKED_NO_GO`, `D10=BLOCKED_FOR_PROMOTION`, `baseline_approval=MISSING`, `freeze_eligible=false`, `release_authority=NONE`.

## 6. Permanent governance locks

- Frozen C11-C SHA-256: `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`; bytes `796318`.
- `renderer=OFF`; `media_created=false`; `candidate_input_admissible=false`; `D4.8=BLOCKED`; `D9.10=PREPARE_ONLY`; `D9.14=BLOCKED`; `D9.16=BLOCKED`; `D9.17=BLOCKED_NO_GO`; `D10=BLOCKED_FOR_PROMOTION`; `baseline_approval=MISSING`; `freeze_eligible=false`; `release_authority=NONE`.
- No renderer-native input, dispatch, payload/receipt files, pixels or media are produced.
- Challenge coordinate projection and delivery resampling remain unresolved. Editorial values remain sidecar-only: `visual_payload_consumed=0/14`.
- No baseline acceptance, freeze, promotion, or C11-C replacement is authorized.


## Fase J — Rechazo de colisiones de dominios de semillas V1 aceptado en Windows (27-10-2026)

Resultado real del checkout Windows: `C11D_SEED_DOMAIN_COLLISION_REJECTION_AUDIT=PASS`; exit code `0`; dos selectores; negativos de semilla explícita `20/20`; colisiones numéricas `4/4`; valores `12345,840001`; todas las negativas precedieron a Godot; `source_pins=23/23`; `runtime_invocations=0`.

- `audit_sha256`: `2eb512f38740052ab2a3f06bda35eae3374c6a28d241734dafa7567a99f6fcd0`.
- Report file SHA-256: `aa386c6f61a993c52353814b03dc581bef27f45de805b1278e212cb78a3cf642`.
- stdout SHA-256: `8e093a5c9f1ceab56aa825795c8290f3abe282119a3f471f4aa7beba898dab0d`; stderr vacío SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
- Log directory: `%TEMP%\C11D_SEED_DOMAIN_COLLISION_AUDIT_20261027_1bc24be1ec5c406ea02434e9b3514cb5`.

La prueba cubrió solo `parking_v2/CHALLENGE_004` y `c11c_geometric_waves_v1/harmonic_membrane`. No prueba cobertura de todos los selectores ni completa dominios de semillas para admisión.

## Siguiente puerta — ampliación Challenge 9-selectores (preparada; Windows pendiente)

Se prepara un audit de solo preflight que reutiliza el mapa de selectores del contrato `D_RENDERER_CHALLENGE_SEED_DOMAIN_PREFLIGHT_V2` y el rechazo de colisiones D9.10. Cobertura prevista y bloqueada por schema: `CHALLENGE_001..009`, diez formas de semilla inválida por selector (`90/90`) y dos colisiones numéricas por selector (`18/18`), total `108` rechazos. La ejecución no invoca Godot, no genera payloads ni receipts, y no amplía el binding V1 fijado a `CHALLENGE_004`. La aceptación requiere la salida Windows, exit code, auditoría autohasheada y hashes stdout/stderr separados.


## Estado rector actualizado — 27-10-2026, después de la expansión Challenge

La sección histórica de auditoría de colisiones de dos selectores y cualquier nota previa que la marque como pendiente queda resuelta por las fases J/K aceptadas más abajo. El último resultado aceptado de Windows es la expansión de rechazo de semillas a los nueve selectores Challenge; esta aceptación sigue limitada a planning/preflight.

### Fase K — Rechazo de colisiones en los nueve Challenges (Windows PASS)

- Aplicación del overlay: `C11D_CHALLENGE_COLLISION_EXPANSION_OVERLAY_APPLY=PASS`; reemplazos guarded `2/2`; add-only `6/6`; manifiesto C11-C inalterado.
- Auditoría: exit `0`; `SELECTORS=9`; `EXPLICIT_SEED_NEGATIVE_CASES=90/90`; `NUMERIC_SEED_COLLISION_REJECTIONS=18/18`; valores `12345,840001`; `ALL_REJECTIONS_PRECEDE_GODOT=true`; `SOURCE_PINS=27/27`; `RUNTIME_INVOCATIONS=0`.
- `AUDIT_SHA256=274f2b24c09d830b345556f0a456cf45a95c6b649dc2ebb5ddaeb073b15c4c0b`; informe SHA-256 `61224477f8bca50c864001cf1d3e2eda6af8f1ec5d04bb4cf6922dccf6e20341`.
- stdout SHA-256 `11140895e83c58ef79e6011f49ee33193eec1a16572ceb4b0f676bcd9a1beb02`; stderr vacío SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
- Evidencia: `%TEMP%\C11D_CHALLENGE_SEED_COLLISION_AUDIT_20261027_18a3310ea91f4b959a31bfe7f4c55549`.
- Alcance: rechazo fail-closed en planning para `CHALLENGE_001..009`; no prueba sensibilidad visual de gameplay seed, admisibilidad del candidato ni render.

### Próxima puerta — V2-B implementación estática (198 tests)

La siguiente prueba activa es `tools/c11d/d9/test_d_renderer_challenge_visual_payload_v2b_safe_projection_runtime.py`. El lanzador de esta fase debe:

1. Verificar 81/81 source pins y 9/9 authority-input pins antes de aceptar el test.
2. Exigir exit code `0`, `Ran 198 tests`, `OK` y `C11D_V2B_RUNTIME_IMPLEMENTATION_TESTS_PASS=198/198`.
3. Crear y validar `implementation_test_receipt.json` bajo `%TEMP%` solo después de un PASS real; la recibida en `%TEMP%` no se versiona como payload ni se almacena en el repo.
4. No invocar Godot ni ejecutar la matriz runtime en esta puerta.

Solo tras la aceptación estática se puede abrir una puerta separada de `45/45` llamadas canónicas al planner y `45/45` procesos Godot independientes. El próximo trabajo todavía no es renderizar un vídeo.

### Bloqueos conservados

`approved_bindings=0`; `approved_custom_data_bindings=0`; `approved_renderer_projection_bindings=0`; `visual_payload_consumed=0/14`; `candidate_input_admissible=false`; `seed_domains_complete_for_candidate_input=false`; `renderer=OFF`; `media_created=false`; `D4.8=BLOCKED`; `D9.10=PREPARE_ONLY`; `D9.14/D9.16=BLOCKED`; `D9.17=BLOCKED_NO_GO`; `D10=BLOCKED_FOR_PROMOTION`; `release_authority=NONE`. Los conflictos de 11 s declarados frente a 12 s de fases de `CHALLENGE_008/009`, la proyección de coordenadas y el remuestreo de entrega siguen sin resolver.

### Fase L — V2-B implementación estática y recibo estricto (27-10-2026, Windows PASS; write-back recuperado)

- Test: 	ools/c11d/d9/test_d_renderer_challenge_visual_payload_v2b_safe_projection_runtime.py; Exit code  ; suite 198/198; marker C11D_V2B_RUNTIME_IMPLEMENTATION_TESTS_PASS=198/198.
- Source pins 81/81 y authority-input pins 9/9, verificados antes y después y revalidados durante la recuperación.
- Python: Python 3.13.14.
- Test stdout SHA-256: 02cf98c041d0e3c40282164500df99e16f0b058eb9d899081ada30829bd1cd43; stderr SHA-256: a14048cc73bbcda88c44e7bd7f889396ad73af5efb76cf0e91e32c889db99f8d.
- Recibo: $receiptPath; SHA-256: aa8cebd453b632e445becb936ff3520110d5f80fdf2a732818a6917885595e32; estado PASS_IMPLEMENTATION_STATIC_TESTS; validación real repetida: C11D_V2B_STATIC_RECEIPT_VALIDATION=PASS.
- Overlay ZIP SHA-256: 0e417f065bcb0a968684c51ab38471e8d5643bb9f3d8e1882d9fbf148a28e0aa; manifest SHA-256: 40e8a19c5f2f695cc796bbe5a69acc9724336405fff87c9bea4b289406c099c0.
- Logs: $LogDirectory. El lanzador original se detuvo antes del write-back documental porque su literal Unicode Próxima acción única se interpretó mal en Windows PowerShell 5.1 sin BOM. Los logs y el recibo se preservaron; esta recuperación no repitió los 198 tests ni invocó Godot.
- Esta aceptación es estática: no demuestra sensibilidad visual runtime, no aprueba bindings ni hace admisible el candidate input.

**Siguiente puerta:** matriz V2-B 45/45 llamadas al planner + 45/45 procesos Godot Mono independientes, detenida al primer fallo. Debe demostrar repetibilidad baseline, sensibilidad al gameplay seed y ortogonalidad de music seed/editorial.

**Gobernanza:** enderer=OFF; media_created=false; payload_materialized=false; candidate_input_admissible=false; seed_domains_complete_for_candidate_input=false; pproved_bindings=0; pproved_custom_data_bindings=0; D4.8=BLOCKED; D9.10=PREPARE_ONLY; D9.14=BLOCKED; D9.16=BLOCKED; D9.17=BLOCKED_NO_GO; D10=BLOCKED_FOR_PROMOTION; aseline_approval=MISSING; reeze_eligible=false; elease_authority=NONE.