# C11-D — Registro acumulado de fases y continuidad técnica

**Fecha de corte:** 27-10-2026  
**Workstream:** enlace canónico solicitud → instancia de payload → evidencia de revisión  
**Estado actual:** `V2.2_WINDOWS_RUNTIME_PASS; IO_IDENTITY_REFRESH_PASS; PHASE_K_CHALLENGE_COLLISION_EXPANSION_PASS; PHASE_L_V2B_STATIC_TESTS_PASS; PHASE_M_V2B_RUNTIME_MATRIX_PASS; PHASE_N_V2C_SOURCE_FRAME_RUNTIME_PASS; NEXT_PHASE_O_SOURCE_FRAME_SEMANTIC_BINDING_CROSSWALK`  
**Checkout operativo:** `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`

## 0. Para reanudar sin repetir trabajo aprobado

Este documento es el índice acumulado de las fases de este workstream. La fuente de verdad para ejecución/aceptación en Windows es siempre la salida real aportada desde el checkout activo. Los resultados de sandbox/preparación se identifican por separado y nunca se elevan a aceptación Windows.

**Regla de repetición:** no volver a ejecutar una fase ya aceptada si sus fuentes fijadas no han cambiado y la siguiente puerta no exige evidencia fresca. Tras integrar V2, se permite una única actualización de auditoría I/O e inventario de identidad porque el árbol D habrá cambiado. No repetir V2B 402/402 ni la prueba de propuesta V1 como rutina.

**Próxima acción única:** auditar en modo de solo lectura los nueve recibos source-frame V2-C y cruzarlos con la propuesta de binding semántico existente; clasificar datos temporales, contadores de episodio, candidatos de custom_data y ausencias, sin aprobar bindings ni materializar payload/media.

## 1. Invariantes de autoridad

- Baseline C11-C 2.19.12 permanece inmutable y autoritativo hasta la aceptación formal, freeze y promoción de C11-D.
- `release/C11C_FREEZE_PACKAGE_MANIFEST.json`: SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`; tamaño `796318` bytes.
- Docket de política: `definitions/c11d/production/D_RENDERER_POLICY_DECISION_DOCKET_V1.json`, SHA-256 `e008217bd57303b638e13329d21e5ae56ee3b4efef790566e3702c89ee41a83f`.
- Permanecen: `renderer=OFF`; `media_created=false`; `payload_materialized=false`; `candidate_input_admissible=false`; `seed_domains_complete_for_candidate_input=false`; `automatic_seed_generation=false`; `master_seed=NOT_ADOPTED`; `approved_bindings=0`; `approved_custom_data_bindings=0`; `approved_renderer_projection_bindings=0`; `D4.8=BLOCKED`; `D9.10=PREPARE_ONLY`; `D9.14=BLOCKED`; `D9.16=BLOCKED`; `D9.17=BLOCKED_NO_GO`; `D10=BLOCKED_FOR_PROMOTION`; `baseline_approval=MISSING`; `freeze_eligible=false`; `release_authority=NONE`.
- No renderer-native input, dispatch, persistent payload, output manifest, pixels, media, approval, freeze or promotion is authorized by this workstream.
- `winning_frame` remains the sole Challenge timing anchor; `close_calls` remains an episode count only. The CHALLENGE_008/009 declared 11-second duration versus 12-second phase sum remains unresolved.

## 2. Fases cerradas y evidencias que no deben repetirse sin cambio de fuentes

### Fase A — Validación de evidencia runtime V2B (26-10-2026)

**Estado:** `WINDOWS_VALIDATED; ACCEPTED_FOR_ISOLATED_RUNTIME_EVIDENCE_ONLY`.

- Validador: `402/402`, exit code `0`.
- Marcador: `C11D_V2B_SOURCE_COMPOSITION_RUNTIME_EVIDENCE_VALIDATION_STATUS=PASS_RECEIPT_AND_CURRENT_SOURCE_PINS`.
- Receipt SHA-256: `c09e7beee55c3458e7f6d8778f090cb98ec12650a237787b72f6806ea8d3767b`.
- Schema SHA-256: `9c41d4bdc64be321638e895ffe5e7ed21051b81d20b33d7059ab9e525738b79c`.
- Runtime stdout SHA-256: `b5e1465894a9d5ad5a26715f10459bf578809d4a3fadce7fc030b4964aa2c3bb`.
- Godot observado: `4.7.1.stable.mono.official.a13da4feb`; alcance: CHALLENGE_003/005/006/007, 1680/1680 source frames y marcadores lógicos cerrados.
- Decisión independiente: `C11D_V2B_ALLOWLISTED_COORDINATE_SOURCE_COMPOSITION_RUNTIME_DECISION_V2_20261026.md`, SHA-256 `22715d2139dd5a1fd7d747d74cbb7eab9c87f37c3d8f074c5c4a69da4db5aa59`.
- Límite: evidencia aislada in-memory; no pixels/video, materialización de payload, renderer input o admisibilidad.

**Reutilizar:** receipt, schema, stdout y decisión anteriores si permanecen idénticos los pines. No relanzar el validador como requisito para la siguiente puerta de integración.

### Fase B — Auditoría I/O e identidad (27-10-2026, Windows)

**Estado:** `WINDOWS_PASS_REPORTS_ONLY; CANDIDATE_NOT_READY`.

Auditoría I/O:

```text
C11-D CANDIDATE I/O CONFORMANCE GAP AUDIT PASS | groups=10/10 | complete=0/10 | partial=6 | blocked=4 | source_pins=54/54 | input_instance_emitted=false | output_manifest_created=false | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE
EXIT_CODE_CANDIDATE_IO_GAP=0
```

Inventario de identidad:

```text
C11-D RENDERER CANDIDATE IDENTITY PASS | source_files=164 | fingerprint=0b4168bddac991ac03ea45d424f5af4fa2316c275dc31c1866c5cf8baf532d25 | report_sha256=74e518b620d297c5e09cf6e9495864dbe96e9394b6520e9a5e492775642b92bf | python=3.13.14 | godot_probe=VERSION_PROBED | C11-C=IMMUTABLE_REFERENCE_MATCH | renderer=OFF | renderer_build=NONE | media_created=false | D4.8=BLOCKED | release_authority=NONE | baseline_approval=MISSING | freeze_eligible=false
EXIT_CODE_CANDIDATE_IDENTITY=0
```

- Log folder: `%TEMP%\C11D_GAP_IDENTITY_20261027`.
- La huella de 164 archivos identifica la superficie declarada para revisión, no el árbol completo del repositorio.
- Grupos parciales: `content_identity`, `source_lineage`, `payload_instance`, `seed_domains`, `editorial`, `delivery`.
- Grupos bloqueados: `presentation`, `timeline`, `audio`, `authorization`.

**Reutilizar:** los valores mostrados aquí son el baseline de auditoría anterior a V2.2. Tras el runtime V2.2 PASS, queda pendiente un solo refresh de ambos reportes; las nuevas cifras no se presuponen y se documentarán solo con la salida Windows observada.

### Fase C — Propuesta de integración V1 aplicada (27-10-2026, Windows)

**Estado:** `WINDOWS_APPLY_PASS`.

- ZIP de propuesta: `C11D_REQUEST_PAYLOAD_INSTANCE_INTEGRATION_PROPOSAL_20261027_V1.zip`.
- SHA-256 del ZIP: `5ddb0906e949cab05b8f18ac8641e766359983f19ac17f980a7e5c023c107ca3`.
- Destinos añadidos: `5/5`, hashes verificados; `FROZEN_C11C_MANIFEST=UNCHANGED`.

### Fase D — Test de propuesta V1 (27-10-2026, Windows)

**Estado:** `WINDOWS_PASS`.

```text
C11-D REQUEST-PAYLOAD INSTANCE INTEGRATION PROPOSAL PASS | source_pins=54/54 | io_gap_groups=10/10 | complete=0 partial=6 blocked=4 | schema_engine=DRAFT2020_12 | schema_negatives=6/6 | renderer=OFF | media_created=false | candidate_input_admissible=false | D4.8=BLOCKED | release_authority=NONE
PROPOSAL_TEST_EXIT_CODE=0
REQUEST_PAYLOAD_INTEGRATION_PROPOSAL_VALIDATION=PASS
SOURCE_PINS=54/54
FROZEN_C11C_MANIFEST=UNCHANGED
```

Artefactos fijados: proposal contract `3e65d03532417502ff9a957bc9a6efca01a974641aeaa1b9b00a11b1bdad4e81`; schema `f75a98b9e666a2d668bdbc1f5c5605fb12851b704e0f5ee9df0bd798b0385cba`; focused test `965619065a41a609c84a8dabc7302e4d87c4e9e157b0966ef0ba1990faeb3280`; proposal checkpoint `66bacf230f0b6e931802f9f4eba15b0b73783b8e45989e6731fc6ba3f5a19958`.

**Reutilizar:** no repetir mientras estos hashes y los 54 pins no cambien.

### Fase E — Decisión técnica V1 (27-10-2026)

**Estado:** `ACCEPTED_FOR_BOUNDED_NONPRODUCTION_INTEGRATION_IMPLEMENTATION_AND_RUNTIME_REVIEW_ONLY`.

- JSON: `definitions/c11d/production/D_RENDERER_REQUEST_PAYLOAD_INSTANCE_INTEGRATION_DECISION_V1.json`, SHA-256 `68d1e6e992f5d426c9553cbc0ae4da360e94a0cad3363b9b7c89a43e77c34711`.
- Markdown: `docs/current/d/D_RENDERER_REQUEST_PAYLOAD_INSTANCE_INTEGRATION_DECISION_V1.md`, SHA-256 `edd014e7e38f2305afc03e82da97bb310a96ad7abed1a96eac590505f09d3f03`.
- Alcance autorizado: revisión in-memory/stdout de tres fixtures fijos: Challenge `parking_v2/CHALLENGE_004` (gameplay seed 314159), Loop `c11c_geometric_waves_v1/harmonic_membrane` (seed 12345), Drill `tracking/tier-2` (seed 12345); music seed 840001.
- Digest del dynamic binder y digest del payload materialization V1 tienen namespaces/serializaciones diferentes. Deben conservarse separados; no declarar equivalencia.

**Límite:** no es aprobación de renderer, I/O, políticas, pixels, producción o medios; no amplía Drill a 20 selectores.

## 3. Fase F — V2 integrada en Windows; fallo de guard detectado y aislado (27-10-2026)

**Estado:** `WINDOWS_RUNTIME_FAIL_GUARD_BUG_ISOLATED; CORRECTIVE_OVERLAY_PREPARED; WINDOWS_RETEST_PENDING`.

### V2 original — aceptación unitaria Windows

El operador ejecutó la prueba focalizada del checkout activo: `UNIT_TESTS=10/10`, salida `OK`, exit code `0`; `FROZEN_C11C_MANIFEST=UNCHANGED`. Los diez tests cubrían pins, digest namespaces, identidad, sidecar y mutaciones negativas, pero su binder sintético no reflejaba fielmente la ubicación de la admisión en el recibo V1 real. Esta suite PASS no anticipó el bug de integración que apareció en runtime.

Fuentes originales V2 antes de la corrección:

- Runner SHA-256 `4ca3f35d87ba4201d7a31c77069022811869a9057b7a95855b71e5953813a968`.
- Test SHA-256 `35f0f4072c8b6dae96391b7316f7701ea7879e6837509fc629d997027e9daf86`.
- Contrato V2 SHA-256 `0bc9f904810b853ab0857ae03c143c0287edc527b597ec954de57bcfd28b8d1c`.
- Schema de salida V2 SHA-256 `3d8d85f76bef958062badb1cd1e6d22d5ab17e439d22f3947f2e774e4769c203`.
- Decisión JSON SHA-256 `68d1e6e992f5d426c9553cbc0ae4da360e94a0cad3363b9b7c89a43e77c34711`; decisión Markdown SHA-256 `edd014e7e38f2305afc03e82da97bb310a96ad7abed1a96eac590505f09d3f03`.

### V2 runtime — resultado real Windows

Godot ejecutable por WinGet se verificó mediante captura redirigida: `4.7.1.stable.mono.official.a13da4feb`, exit code `0`. Los dos harnesses previos emitieron sus marcadores PASS in-memory (Visual Loop/Drill `materialized=2/3`; Challenge `payload=1/1`), pero el join dinámico terminó con:

```text
C11-D REQUEST-PAYLOAD INSTANCE INTEGRATION V2 FAIL | Dynamic binder receipt schema/status/admission mismatch | renderer=OFF | media_created=false | candidate_input_admissible=false | D4.8=BLOCKED | release_authority=NONE
V2_RUNTIME_EXIT_CODE=1
RUNTIME_STDOUT_SHA256=4c0436069f9c0c8010a33b654ef233511cbc3caf09482572d55ca1ccdc5592fc
RUNTIME_STDERR_SHA256=e5eed2ae6854c661e8e16643f84be6445c9156f1aa7fafbb0b27359d799465ee
```

Log folder Windows: `%TEMP%\C11D_REQUEST_PAYLOAD_INTEGRATION_V2_RUNTIME_20261027`.

### Causa raíz confirmada

El recibo real del dynamic binder V1 aplica el schema estricto con `candidate_input_admissible=false` dentro de `readiness`, junto a `video_render_ready=false`; no declara ese flag en la raíz del recibo. El join V2 lo consultaba erróneamente como `binder.get("candidate_input_admissible")`, obtenía ausencia (`None`) y fallaba cerrado aunque el recibo estuviera correctamente bloqueado. Además, el fixture sintético del test V2 inicial añadía ese flag a la raíz y por tanto ocultaba el desacuerdo de contrato.

### Corrección V2 Runtime Receipt Guard Fix V1

La corrección limitada cambia únicamente el guard de interfaz y la fidelidad de los tests:

1. Comprobar que `readiness` es un mapping y que `readiness.candidate_input_admissible is false`.
2. Seguir exigiendo `readiness.video_render_ready is false`, el schema/status V1 exactos, digest propio, manifest hash, lineage, selector y las demás igualdades.
3. Ajustar el recibo sintético a la forma real: no hay flag de admisión raíz; ambos valores de gobernanza quedan bajo `readiness`.
4. Añadir una prueba de aceptación de esa forma real y una prueba negativa para `readiness` ausente; la negativa de promoción muta el flag anidado.

No se modifica el binder dinámico V1, sus contratos, sus harnesses, el contrato/schema V2, los digest namespaces ni el límite de gobernanza. La corrección no tolera admisión `true`; alinea la consulta al schema ya vigente. En la preparación aislada, la suite corregida pasó **12/12** pruebas. Esto es validación de sandbox, no aceptación Windows ni runtime Godot de la corrección.

Artefactos del overlay correctivo: runner V2 y test V2 son reemplazos controlados con hashes `before_sha256`; el ledger se reemplaza de forma acumulativa, y se añaden un checkpoint V2.1 y una ficha de overlay. El ZIP debe verificar hashes de origen/destino, backup de los tres reemplazos y conservar intacto el manifiesto C11-C antes/después.

## 3.1 Fase G — Runtime V2.1; segundo defecto aislado (27-10-2026)

**Estado histórico:** `WINDOWS_RUNTIME_FAIL_EDITORIAL_DIGEST_NAMESPACE_MISMATCH; RESOLVED_BY_FASE_H_V2_2_WINDOWS_PASS`.

### Evidencia de Windows

El operador ejecutó la suite V2.1 después del primer arreglo, con `UNIT_TESTS=12/12`, `OK`, exit code `0`. La siguiente ejecución confirmó Godot Mono `4.7.1.stable.mono.official.a13da4feb` con exit code `0` y ambos harnesses de materialización in-memory pasaron sus marcadores, pero el join integrado falló:

```text
C11-D REQUEST-PAYLOAD INSTANCE INTEGRATION V2 FAIL | Canonical editorial hash does not join to the sidecar | renderer=OFF | media_created=false | candidate_input_admissible=false | D4.8=BLOCKED | release_authority=NONE
V2_1_RUNTIME_EXIT_CODE=1
RUNTIME_STDOUT_SHA256=4c0436069f9c0c8010a33b654ef233511cbc3caf09482572d55ca1ccdc5592fc
RUNTIME_STDERR_SHA256=a863b8582f41dcf099073953466e3cbfa2f0c9bbc4e2ee6f937943279161e4ab
```

Log folder: `%TEMP%\C11D_REQUEST_PAYLOAD_INTEGRATION_V2_1_RUNTIME_20261027`. No receipt integrated; runtime acceptance remains **FAIL**.

### Causa raíz

El productor canónico calcula `editorial_hash` con dos componentes: selección canónica completa (`content_type`, `family_id`, `subtype_id`, `variant_id`, `variant_scope_id`, `difficulty_tier`) y mapa editorial. El sidecar calcula `editorial_values_sha256` con solo el mapa editorial. El join comparaba hashes de namespaces distintos, y la sección `digest_semantics` del contrato V2 también describía mal esa igualdad. No era un error de Godot ni una justificación para ignorar el sidecar.

### Corrección V2.2 aplicada y aceptada en Windows

El nuevo runner reevalúa en memoria los tres requests canónicos fijos, verifica el mapa exacto reconstruido desde los campos sidecar (`value_sha256` por campo más digest de mapa), y calcula `SHA256({selection: full_canonical_selection, editorial: sidecar_values})`. El digest reconstruido debe igualar el `editorial_hash` del productor y del dynamic binder. El recibo separa los campos `editorial_values_sha256`, `canonical_editorial_sha256` y `canonical_editorial_reconstructed_sha256`, más namespaces explícitos; el schema y la declaración contractual también se actualizan.

Prueba aislada de esta implementación: **16/16 PASS**, incluyendo reconstrucción de hash para los tres request fixtures reales, divergencia deliberada entre namespaces, rechazo de valor lateral modificado aunque se recalculen hashes del sidecar y rechazo de selección canónica mutada. Esto aún es sandbox PASS, no Windows acceptance.

Overlay: `C11D_REQUEST_PAYLOAD_V2_EDITORIAL_HASH_NAMESPACE_FIX_OVERLAY_20261027_V1.zip`, SHA-256 `b7ee45e2060258381d240b4aa5dfd14ff00f84c56fb2e65e84589fd546e37b5a`; aplicación Windows aceptada: cinco reemplazos guardados y dos destinos add-only verificados. La fase fue preparada en sandbox y posteriormente aceptada en el checkout Windows en la Fase H que sigue.

Hashes de destino para el overlay V2.2:

- Runner: `709d5ff670561d2bfc8b5926ba616b6773589bb783dc10f767354b26c3c62cbd`.
- Test: `120b99b58e4ba09ff74c01a5f1acf57252353d61a659aaa440723436f5900da6`.
- Contrato V2: `0c3f03cbfa3990e093ccbc3e74f777f8f537682570e75cc304b393c2a6eb1100`.
- Schema de recibo V2: `e1b586f4ec4abc31ca92e2ebdbdbaa293c17efb9493b0385f1af79e652dfc83f`.

### Fase H — V2.2 aceptación real Windows (27-10-2026)

**Estado:** `WINDOWS_PASS; BOUNDED_IN_MEMORY_REQUEST_PAYLOAD_JOIN_ONLY`.

- Aplicación: `C11D_V2_2_EDITORIAL_HASH_FIX_APPLY=PASS`; `V2_2_OVERLAY_PINS=7/7_HASH_VERIFIED`; `FROZEN_C11C_MANIFEST=UNCHANGED`.
- Overlay ZIP SHA-256: `b7ee45e2060258381d240b4aa5dfd14ff00f84c56fb2e65e84589fd546e37b5a`.
- Unit tests Windows: `16/16`, exit `0`; stdout SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`; stderr SHA-256 `3183ebabac73872621e28e140dc029fb9875826166ab85b7a0fe2687f6b7215f`. Log `%TEMP%\C11D_REQUEST_PAYLOAD_V2_2_TEST_20261027_46ad02316d824c46884fc1a6ec6f4a01`.
- Godot Mono: `4.7.1.stable.mono.official.a13da4feb`; WinGet executable path was verified with redirected stdout; version probe exit `0`.
- Runtime exit `0`; marker `C11D_REQUEST_PAYLOAD_V2_2_RUNTIME_VALIDATION=PASS`; `C11D_V2_2_PIPELINE=PASS`.
- Runtime stdout SHA-256 `00a0d51627618ae3ee167a7d2ca029f6ed5cd05ecf369f8d816ef5774d99051a`; stderr SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (vacío).
- Receipt SHA-256 `1a2a729137458f633cf520c211180ce5a3fff2d21ed441e866ae0e1c946169af`; runtime evidence directory `%TEMP%\C11D_V2_2_RUNTIME_20261027_d2425963e21448bd9d04c2a044a7bea9`.
- Summary: fixtures/joins/manifests `3/3`; editorial sidecar joins `3/3`; fields `14/14`; visual payload consumed `0/14`; distinct digest namespaces preserved; source pins `60/60`.
- Locks observed: renderer OFF, media false, candidate input inadmissible false, D4.8 blocked, release authority none; C11-C manifest unchanged.

Esta fase resuelve los dos defectos de contrato registrados en las fases anteriores: ubicación de `readiness.candidate_input_admissible` en el recibo real V1 y comparación indebida entre digest editorial compuesto y digest map-only. Los dos intentos runtime fallidos permanecen como evidencia histórica; no se sobrescribieron. No hubo render, media, payload persistido, renderer-native input ni promoción.

### Fase I — Refresh post-V2.2 de I/O gap + candidate identity (27-10-2026)

**Estado:** `WINDOWS_PASS_READ_ONLY_AUDITS; INPUT_READINESS_STILL_FAIL_CLOSED`.

La ejecución real de `tools/c11d/d9/refresh_d_renderer_candidate_io_and_identity_after_v2_2.ps1` terminó con `C11D_POST_RUNTIME_IO_IDENTITY_REFRESH=PASS`, ambos procesos Python con exit code `0`, y el manifiesto congelado C11-C intacto.

**I/O gap:** grupos `10/10`; completos `0/10`, parciales `6`, bloqueados `4`; source pins `54/54`; candidate input inadmisible. `audit_sha256=b8c5d5994d349c1ce9fef518d7633f72565f3c927cd7bc51cdd89fe5d2df2fe2`; stdout SHA `b3488932ec9075c42f1b505dd384b15c452834f0da0d4830e61a0567a527c677`; stderr SHA `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (vacío).

**Identity inventory:** `source_files=164`; fingerprint `0b4168bddac991ac03ea45d424f5af4fa2316c275dc31c1866c5cf8baf532d25`; `report_sha256=74e518b620d297c5e09cf6e9495864dbe96e9394b6520e9a5e492775642b92bf`; Python `3.13.14`; Godot probe `VERSION_PROBED`; versión `4.7.1.stable.mono.official.a13da4feb`; stdout SHA `c9e21562264e5189fdbba76da215f5bac2db8b797b327f2404e95ff930e5c6cf`; stderr SHA vacío (`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`).

Evidencia Windows `%TEMP%\C11D_V2_2_POST_RUNTIME_AUDITS_20261027_6260c069a2114d4893f2d567b5308ed0`; completion marker `%TEMP%\C11D_V2_2_POST_RUNTIME_GAP_IDENTITY_REFRESH_20261027.completed.json`. Los resultados no cierran los seis grupos parciales ni los cuatro bloqueados, no admiten input y no permiten inferir renderer readiness.

### Fase J — Auditoría de rechazo de semillas explícitas y colisiones (siguiente; pendiente Windows)

**Estado:** `PREPARATION_CONTRACT_PINNED; ACTIVE_WINDOWS_RUN_PENDING`.

La auditoría I/O especifica como siguiente incremento seguro `RUN_SEED_DOMAIN_COLLISION_REJECTION_AUDIT_ON_ACTIVE_WINDOWS_CHECKOUT`, seguido de cobertura incremental de selectores canónicos Challenge y gramáticas Visual Loop, manteniendo el renderer apagado. Se añade un wrapper PowerShell de solo lectura que invoca `tools/c11d/d9/d_renderer_seed_domain_collision_audit.py --full-report`, captura stdout/stderr separados bajo `%TEMP%`, valida el informe y crea un marcador de una sola ejecución. El audit debe confirmar 20/20 casos de semillas implícitas/incorrectas y 4/4 colisiones numéricas rechazadas antes de Godot, con 23/23 source pins y cero invocaciones de Godot. Los resultados del árbol de preparación no cuentan como evidencia Windows; la fase J sigue pendiente hasta recibir esa salida real.

## 4. Puertas siguientes (orden obligatorio)

1. Aplicar el overlay de aceptación I/O/identidad y del wrapper de la fase J con hashes `before`/`after`, respaldo verificado, rutas add-only ausentes y manifiesto C11-C inalterado.
2. Ejecutar el wrapper de colisión una sola vez en el checkout Windows. Aceptar solo si exit code `0`, marker PASS único, `20/20`, `4/4`, source pins `23/23`, `runtime_invocations=0`, self-hash/schema correctos y stderr vacío.
3. Registrar los hashes reales y el directorio de evidencia después de observar el resultado. Si hay fallo, conservar stdout/stderr y detener; no relajar el contrato ni repetir a ciegas.
4. Solo tras PASS, preparar un gate separado y acotado para ampliar cobertura de variantes Challenge y familias/gramáticas Loop. Mantener fuera los cambios de política de presentación, timeline, audio, renderer y media.
5. Nunca equiparar estos PASS de preparación a admisibilidad del input: ningún grupo I/O está completo y `candidate_input_admissible=false`.

## 5. Cuestión de baseline separada que no debe confundirse con este gate

Existe un hallazgo previo de baseline preflight: `AGENTS.md` en el checkout fue registrado con hash `a33caf3528a239049d7a84189584dfd661a1b12d6c48ec599ba3de51315b06f2`, mientras que el manifiesto histórico declaraba `a8a9925256a7dc812fe5d50179c43f347351c629ef1310414e53b938d7054a21`. `.continue/rules/CONTINUE.md` fue registrado con `8a6ea4611a2bc710a41fde7d02da2dcbf108e910c4daaad9b37f611d234541cd`, pero el SHA esperado no se ha establecido con una fuente canónica verificada. No restaurar desde un ZIP de contexto ni modificar el manifiesto. Resolver este incidente antes de intentar de nuevo baseline preflight; no bloquea la aceptación focalizada de V2 si sus propias precondiciones permanecen válidas.

## 6. Criterios de finalización de este workstream

No considerar cerrado el enlace solicitud→payload hasta que se cumplan, por separado:

- Test V2 Windows PASS con sus 60 source pins exactos.
- Receipt de runtime Godot 4.7.1 Mono en los tres fixtures, joins exactos de solicitud/selector/seed/perfiles/linaje/manifest digest/editorial sidecar y exit code 0.
- Digest namespaces diferenciados; `payload_digest_equivalence_proven=false`.
- Sidecar editorial 14/14 unido con hashes, pero `visual_payload_consumed=0/14` explícito.
- I/O gap e identity refrescados después del cambio, con los grupos incompletos reflejados con honestidad.
- Todos los locks y la inmutabilidad C11-C siguen iguales.

Incluso tras un PASS V2, la integración solo valida identidad/provenance de una instancia en memoria. No prueba texto dibujado, píxeles, render, vídeo final ni admisibilidad de candidato.


### Fase J — Auditoría de rechazo de colisiones de semillas, dos selectores (27-10-2026, Windows)

**Estado:** `WINDOWS_PASS; TWO_SELECTORS_ONLY; CATALOG_WIDE_COMPLETENESS_NOT_ESTABLISHED`.

- Aplicación de overlay: `C11D_POST_V2_2_AUDIT_ACCEPTANCE_OVERLAY_APPLY=PASS`; reemplazos guarded `2/2`; add-only `3/3`; manifiesto C11-C sin cambios.
- Runner: exit code `0`; `SELECTORS=2`; `EXPLICIT_SEED_NEGATIVE_CASES=20/20`; `NUMERIC_SEED_COLLISION_REJECTIONS=4/4`; colisiones `12345,840001`; `ALL_REJECTIONS_PRECEDE_GODOT=true`; `SOURCE_PINS=23/23`; `RUNTIME_INVOCATIONS=0`.
- `AUDIT_SHA256=2eb512f38740052ab2a3f06bda35eae3374c6a28d241734dafa7567a99f6fcd0`; report SHA `aa386c6f61a993c52353814b03dc581bef27f45de805b1278e212cb78a3cf642`; stdout SHA `8e093a5c9f1ceab56aa825795c8290f3abe282119a3f471f4aa7beba898dab0d`; stderr SHA `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
- Evidencia: `%TEMP%\C11D_SEED_DOMAIN_COLLISION_AUDIT_20261027_1bc24be1ec5c406ea02434e9b3514cb5`.
- Alcance: Challenge `parking_v2/CHALLENGE_004` y Visual Loop `c11c_geometric_waves_v1/harmonic_membrane`. No se ejecutó Godot ni se creó entrada de renderer.

### Fase K — Rechazo de colisiones en nueve selectores Challenge (overlay preparado; Windows pendiente)

**Estado:** `PREPARED_READ_ONLY_PREFLIGHT; ACTIVE_CHECKOUT_EXECUTION_PENDING`.

El audit add-only reutiliza el selector map verificado por el preflight Challenge V2 (`CHALLENGE_001..009`) y ejercita el rechazo de semillas inválidas y colisiones en el camino D9.9/D9.10. Scope fijo: 9 selectores × 10 negativos (`90/90`) más 9 × 2 valores de colisión (`18/18`, 12345 y 840001), 27 pins y cero invocaciones de Godot. El script exige el motivo de rechazo esperado para evitar contar como PASS un rechazo causado por un selector fuera de alcance. No modifica el binding D9.9/D9.10, ni el contrato del binder ni los selectores autorizados de payload.

Si el audit pasa en Windows, se considera aceptada solo la cobertura de rechazo en planning para los nueve Challenges. Permanecen pendientes los loops adicionales, sensibilidad visual de gameplay seed para Challenge, los conflictos de duración de `CHALLENGE_008/009`, admisibilidad y todos los gates de renderer/media/release.


### Fase K — Rechazo de colisiones en nueve selectores Challenge (27-10-2026, Windows PASS)

- Overlay aplicado: `C11D_CHALLENGE_COLLISION_EXPANSION_OVERLAY_APPLY=PASS`; replacements `2/2`; add-only `6/6`; manifiesto congelado intacto.
- Auditoría de preflight: exit `0`; selectores `9`; rechazos por semillas explícitas/implícitas inválidas `90/90`; colisiones numéricas rechazadas `18/18`; valores `12345,840001`; todos los rechazos antes de Godot; pins `27/27`; runtime invocations `0`.
- `AUDIT_SHA256=274f2b24c09d830b345556f0a456cf45a95c6b649dc2ebb5ddaeb073b15c4c0b`; report `61224477f8bca50c864001cf1d3e2eda6af8f1ec5d04bb4cf6922dccf6e20341`; stdout `11140895e83c58ef79e6011f49ee33193eec1a16572ceb4b0f676bcd9a1beb02`; stderr `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
- Evidencia: `%TEMP%\C11D_CHALLENGE_SEED_COLLISION_AUDIT_20261027_18a3310ea91f4b959a31bfe7f4c55549`.
- Esta fase valida únicamente el rechazo en planning. No completa los dominios de semillas ni demuestra sensibilidad visual de gameplay seed.

### Fase L — V2-B implementación estática (puerta activa siguiente)

Se requiere ejecutar el test de implementación V2-B (`test_d_renderer_challenge_visual_payload_v2b_safe_projection_runtime.py`) en Windows y aceptar solo `198/198`, exit `0`, marker PASS y pins `81/81 + 9/9`. El test no debe lanzar Godot. Un recibo temporal estricto y verificado es requisito del siguiente gate, no evidencia de render.

La siguiente puerta después de Fase L es la matriz V2-B de 45 llamadas al planner canónico y 45 procesos Godot Mono independientes, con repetición determinista, sensibilidad del estado visual seguro al gameplay seed y ortogonalidad frente a music seed y cambios editoriales. El runner debe detenerse en el primer fallo y conservar stdout/stderr por proceso.

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
### Fase M — Matriz V2-B de sensibilidad de estado visual seguro (27-10-2026, Windows PASS; recuperación de postcondición)

- Reporte runtime: $ReportPath; SHA-256 $reportSha; estado PASS_SAFE_PROJECTION_SEED_SENSITIVITY; isual_seed_sensitivity=ACCEPTED_BY_SAFE_PROJECTION_HASH.
- Planner canónico 45/45; procesos independientes de Godot Mono 45/45; selectores aceptados 9/9; cinco variantes por selector (BASELINE_R1, BASELINE_R2, GAMEPLAY_SEED_MUTATION, MUSIC_SEED_MUTATION, EDITORIAL_MUTATION).
- Godot: $godotVersion; stdout agregado SHA-256 $stdoutSha; stderr SHA-256 $stderrSha (vacío). Se verificaron $processEvidenceCount archivos de evidencia por sus hashes.
- Test estático de implementación previo: 198/198; recibo SHA-256 $ExpectedReceiptSha; pins estáticos 81/81 y authority-input pins 9/9 registrados en la aceptación de Fase L.
- Integridad de fuentes runtime: $pinCount/14 pins confirmados; errores de pins antes/después vacíos; manifiesto congelado C11-C sin cambios.
- El wrapper original imprimió C11D_V2B_RUNTIME_MATRIX=BLOCKED pese a que el reporte estricto y las 45/45 ejecuciones comunicaban PASS; la comprobación post-run del wrapper no reconoció los marcadores de stdout. Esta recuperación volvió a comprobar el reporte, las nueve filas, los locks, el archivo de salida y sus líneas normalizadas, sin reejecutar la matriz ni iniciar procesos Godot.
- Alcance: evidencia de estado visual source-frame en memoria y sensibilidad de hash; **no es render de vídeo, no aprueba bindings y no admite input de candidato**.

**Siguiente puerta:** V2-C source-frame runtime receipts para los nueve Challenges mediante planner canónico y ChallengeRuntimeBridge.run_effective_pipeline, primero recibos en memoria y validación de contrato/pins. Mantener sin cambios la gobernanza de render.

**Bloqueos inalterados:** enderer=OFF; media_created=false; payload_materialized=false; candidate_input_admissible=false; seed_domains_complete_for_candidate_input=false; pproved_bindings=0; pproved_custom_data_bindings=0; D4.8=BLOCKED; D9.10=PREPARE_ONLY; D9.14=BLOCKED; D9.16=BLOCKED; D9.17=BLOCKED_NO_GO; D10=BLOCKED_FOR_PROMOTION; aseline_approval=MISSING; reeze_eligible=false; elease_authority=NONE.
### Fase N — Runtime source-frame V2-C (27-10-2026, Windows PASS; route-only)

- Contrato Python: 28/28; stdout SHA-256 $ExpectedV2CTestStdoutSha; stderr SHA-256 $ExpectedEmptySha (vacío).
- Contrato V2-C y source pins: 81/81; planner canónico 9/9; sonda de versión Godot 1; procesos Godot Mono independientes 18/18; selectores aceptados 9/9; artefactos de proceso 36/36 con hashes verificados.
- Godot: 4.7.1.stable.mono.official.a13da4feb; estado de reporte PASS_SOURCE_FRAME_ROUTE_ONLY.
- Reporte: $ReportPath; SHA-256 $ExpectedRuntimeReportSha; stdout SHA-256 $ExpectedRuntimeStdoutSha; stderr SHA-256 $ExpectedEmptySha (vacío).
- Directorio de logs: $LogDirectory; directorio de evidencia: $EvidenceDirectory; completion marker: $CompletionPath.
- Cada Challenge tiene una llamada al planner y dos procesos aislados con recibos SOURCE_FRAME_RECEIPT a través de ChallengeRuntimeBridge.run_effective_pipeline. Los recibos confirman ausencia de escritura de payload, creación de media, emisión de input nativo de renderer, nodos de render, llamadas al servidor de render, captura de viewport, mutación del estado canónico y dispatch de producción.
- Alcance aceptado: repetibilidad de recibo source-frame y ruta runtime efectiva en memoria. isual_seed_sensitivity=NOT_TESTED; esta fase no demuestra dibujo de texto, píxeles, proyección de entrega ni vídeo.

**Siguiente puerta:** Fase O — auditoría de solo lectura del cruce recibo source-frame → propuesta de binding semántico, sin aprobar ningún binding. Debe distinguir winning_frame como único anclaje temporal Challenge y close_calls como contador, y mantener en revisión cualquier campo custom_data, proyección y tratamiento temporal.

**Gobernanza inalterada:** enderer=OFF; media_created=false; payload_materialized=false; candidate_input_admissible=false; seed_domains_complete_for_candidate_input=false; pproved_bindings=0; pproved_custom_data_bindings=0; pproved_renderer_projection_bindings=0; D4.8=BLOCKED; D9.10=PREPARE_ONLY; D9.14=BLOCKED; D9.16=BLOCKED; D9.17=BLOCKED_NO_GO; D10=BLOCKED_FOR_PROMOTION; aseline_approval=MISSING; reeze_eligible=false; elease_authority=NONE. El conflicto CHALLENGE_008/009 (11 s declarados y 12 s de fases) sigue pendiente.