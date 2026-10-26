# C11-D V2B — decisión formal de revisión de evidencia de composición de fuentes

Fecha de decisión: 2026-10-26  
Versión: V2  
Tipo de decisión: revisión limitada de evidencia runtime  
Estado: `ACCEPTED_FOR_ISOLATED_RUNTIME_EVIDENCE_ONLY`

## 1. Objeto y alcance

Se acepta la evidencia V2 únicamente como prueba de que la composición aislada, en memoria, ejecutada con el harness de revisión produjo los marcadores esperados para los cuatro candidatos enumerados en este registro. Esta decisión no es una aprobación de integración productiva ni de renderizado.

- Recibo V2: `definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_ALLOWLISTED_COORDINATE_SOURCE_COMPOSITION_RUNTIME_EVIDENCE_V2_20261026.json`
- SHA-256 del recibo: `c09e7beee55c3458e7f6d8778f090cb98ec12650a237787b72f6806ea8d3767b`
- Esquema V2: `definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_ALLOWLISTED_COORDINATE_SOURCE_COMPOSITION_RUNTIME_EVIDENCE_SCHEMA_V2_20261026.json`
- SHA-256 del esquema: `9c41d4bdc64be321638e895ffe5e7ed21051b81d20b33d7059ab9e525738b79c`
- Validador: `tools/c11d/d9/test_d_renderer_challenge_visual_payload_v2b_source_composition_runtime_evidence_v2.py`
- SHA-256 del validador, fijado por el recibo: `97173fef3d8f55086d0b090cb5366db9e76442473147208c8603fc659770f432`
- Contrato actual, que debe conservar su estado pre-run: `definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_ALLOWLISTED_COORDINATE_CONSUMER_SOURCE_COMPOSITION_CONTRACT_V1.json`
- SHA-256 del contrato: `575717bb3f36b476c9742488c8cace622a217c8861e376d17c519d02c70534b7`

## 2. Evidencia considerada

La revisión se basa en la salida de consola y los archivos de evidencia examinados por el operador, junto con el resultado del validador ejecutado en el checkout Windows activo.

- Validación del recibo y pins actuales: `402/402` comprobaciones; código de salida `0`; marcador `PASS_RECEIPT_AND_CURRENT_SOURCE_PINS`.
- Estado publicado por el validador: `C11D_V2B_SOURCE_COMPOSITION_RUNTIME_EVIDENCE_VALIDATION=PASS`.
- Godot Mono: `4.7.1.stable.mono.official.a13da4feb`; código de salida runtime informado: `0`.
- stdout runtime SHA-256: `b5e1465894a9d5ad5a26715f10459bf578809d4a3fadce7fc030b4964aa2c3bb`.
- stderr runtime vacío, SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
- Suites estáticas: runtime V1 `113/113`, runtime V2 `115/115` y composición `132/132`; los tres códigos de salida fueron `0`.
- Candidatos cubiertos: `CHALLENGE_003`, `CHALLENGE_005`, `CHALLENGE_006` y `CHALLENGE_007`; cada uno contiene `420/420` fotogramas fuente y `420/420` marcadores lógicos.
- Totales: `4/4` candidatos; `1680/1680` fotogramas fuente; `1680/1680` marcadores lógicos.
- Consumidor: una llamada allowlisted `Dictionary.get` por fotograma fuente; cero lecturas de `custom_data` directas por el harness; valores crudos de `custom_data` no registrados.
- Resultado observado: exactamente un marcador PASS de composición y cero marcadores FAIL; no se reportaron marcadores de error o traceback.

Estos datos demuestran composición lógica en memoria dentro del alcance cubierto. No demuestran fidelidad visual, resultado de píxeles, codificación de vídeo ni comportamiento del renderer productivo.

## 3. Identidad, procedencia y continuidad histórica

El manifiesto activo congelado de C11-C se verificó en el checkout Windows con tamaño `796318` bytes y SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.

El snapshot ZIP `ChallengeEngineV01_STATELESS_C11-D_20261026_013616.zip` conserva la identidad registrada `3e48ee2d815593137f5863139e05c1aa04eb40b4a58ddfb3bed4507125c96874`, pero su copia interna del manifiesto tiene SHA-256 `f6b2fc6ce36973eb620738c8446d529d98da0fb79892132cf4708e6f453051b5` y no coincide con el manifiesto congelado. El manifiesto dentro del ZIP no es autoridad y no debe copiarse sobre el del checkout.

Se verificó la continuidad de los artefactos históricos V1:

- Recibo runtime V1 del 2026-10-23: SHA-256 `a4684fdb7b3ea4b85f68b561d9aaa64981517f65530ba8a8787f820eb5e3960f`.
- Decisión runtime V1 del 2026-10-23: SHA-256 `a52d5d8a4564cc96d47633c5527248bdc102152da8ce13ad699575fb5b677a08`.

Los artefactos V1 conservan su significado histórico y sus pins anteriores; no se les atribuye la ejecución con las fuentes corregidas de V2 ni se modifican. El contrato de composición conserva su estado pre-run `PENDING_OPERATOR_SOURCE_RUNTIME_COMPOSITION_TEST`; el recibo V2 independiente registra el resultado capturado y no cambia por sí solo dicho contrato.

## 4. Decisión

**Se acepta la evidencia V2 únicamente para acreditar el PASS de la prueba aislada de composición de fuentes en memoria descrita arriba.** La aceptación es específica a los hashes, el harness, las suites, los candidatos y el alcance referenciados por el recibo V2.

No se declara aceptada la integración productiva, ni se aprueba ningún binding o proyección de renderer. La prueba no crea medios ni materializa payloads.

## 5. Bloqueos que permanecen sin cambios

- `renderer=OFF`
- `media_created=false`
- `payload_materialized=false`
- `candidate_input_admissible=false`
- `seed_domains_complete_for_candidate_input=false`
- `automatic_seed_generation=false`
- `master_seed=NOT_ADOPTED`
- `approved_bindings=0`
- `approved_custom_data_bindings=0`
- `approved_renderer_projection_bindings=0`
- `D4.8=BLOCKED`
- `D9.10=PREPARE_ONLY`
- `D9.14=BLOCKED`
- `D9.16=BLOCKED`
- `D9.17=BLOCKED_NO_GO`
- `D10=BLOCKED_FOR_PROMOTION`
- `baseline_approval=MISSING`
- `freeze_eligible=false`
- `release_authority=NONE`
- `runtime_implementation_authorized_for_production=false`
- `render_test_authorized=false`
- `production_dispatch=false`

C11-C permanece inmutable y autoritativo. No se modifica, regenera ni sustituye su manifiesto congelado.

## 6. Siguiente gate autorizado

Continuar con una auditoría de preparación, de solo lectura, sobre las brechas de entrada de candidatos y la identidad exacta entre solicitud, fuente y payload previsto. La auditoría debe identificar campos fuente, proyecciones potenciales, políticas de región/visibilidad, coordenadas, timebase, muestreo, audio y dominios de semillas sin aprobarlos implícitamente.

Tras esa auditoría, cualquier propuesta de integración deberá ser un artefacto separado, versionado y sujeto a revisión explícita, con pruebas negativas y sin despacho productivo. La ejecución de un render real requerirá sus autorizaciones independientes y explícitas en los gates correspondientes. Esta decisión no habilita dicho render.
