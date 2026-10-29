# C11-D — Registro acumulado de fases y continuidad técnica V3

**Fecha de actualización:** 29-10-2026  
**Estado de corte:** `PHASE_O_ACCEPTED; PHASE_P_SOURCE_FRAME_PROVENANCE_ACCEPTED; NO_BINDING_APPROVAL; RENDERER_OFF`  
**Checkout:** `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`

## Jerarquía de esta actualización

Esta V3 es la vista acumulada más reciente. La V1 (27-10-2026) y la V2 (28-10-2026) son documentos históricos inmutables; no se editaron. La sección «Phase P — estado al 28-10-2026» más abajo conserva su significado temporal y queda superada por la decisión runtime fechada 29-10-2026 en §7. Los recibos de intentos fallidos se conservan tal cual y no se convierten en PASS.

## Fuente histórica y regla de no duplicación

`docs/current/d/C11D_ENGINEERING_PHASE_LEDGER_20261027_V1.md` conserva el libro de evidencia detallado de las fases previas y no se reescribe con retrospectiva. Esta V2 incorpora los cambios posteriores de 28-10-2026 y actualiza la siguiente acción. Los recibos, hashes, informes y fallos históricos siguen siendo inmutables.

## Invariantes globales

- C11-C 2.19.12 es la baseline productiva inmutable hasta que C11-D sea aceptada, aprobada, congelada y promovida formalmente.
- Manifiesto canónico del checkout: `release/C11C_FREEZE_PACKAGE_MANIFEST.json`; SHA-256 requerido `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`; tamaño `796318` bytes.
- Docket de política: `definitions/c11d/production/D_RENDERER_POLICY_DECISION_DOCKET_V1.json`; SHA-256 `e008217bd57303b638e13329d21e5ae56ee3b4efef790566e3702c89ee41a83f`.
- `renderer=OFF`, `media_created=false`, `payload_materialized=false`, `candidate_input_admissible=false`, `seed_domains_complete_for_candidate_input=false`, `automatic_seed_generation=false`, `master_seed=NOT_ADOPTED`.
- `approved_bindings=0`, `approved_custom_data_bindings=0`, `approved_renderer_projection_bindings=0`.
- `D4.8=BLOCKED`, `D9.10=PREPARE_ONLY`, `D9.14=BLOCKED`, `D9.16=BLOCKED`, `D9.17=BLOCKED_NO_GO`, `D10=BLOCKED_FOR_PROMOTION`, `baseline_approval=MISSING`, `freeze_eligible=false`, `release_authority=NONE`.
- `winning_frame` es el único anclaje temporal; `close_calls` solo es un conteo de episodios. Conflicto de duración 11s declarados frente a 12s por fases en Challenge 008/009 sin resolver.

## Historial reciente aceptado (no reejecutar por rutina)

### Request→payload V2.2 e I/O/identidad

- V2.2 Windows runtime PASS, 16/16 tests focalizados, tres fixtures, `canonical_request_joins=3/3`, `payload_manifest_digests=3/3`, sidecar `14/14`, consumo visual `0/14`, pins `60/60`. Recibo SHA-256 `1a2a729137458f633cf520c211180ce5a3fff2d21ed441e866ae0e1c946169af`.
- Auditoría I/O tras runtime: 10 grupos, 0 completos, 6 parciales, 4 bloqueados; pins 54/54; reporte `b8c5d5994d349c1ce9fef518d7633f72565f3c927cd7bc51cdd89fe5d2df2fe2`.
- Identidad candidata: 164 archivos; fingerprint `0b4168bddac991ac03ea45d424f5af4fa2316c275dc31c1866c5cf8baf532d25`; reporte `74e518b620d297c5e09cf6e9495864dbe96e9394b6520e9a5e492775642b92bf`.

### Auditorías de semillas y fases K–O

- Expansión de colisiones Challenge (9 selectores): negativos de semilla explícita 90/90; rechazos de colisión numérica 18/18; pins 27/27; cero invocaciones runtime. Audit SHA `274f2b24c09d830b345556f0a456cf45a95c6b649dc2ebb5ddaeb073b15c4c0b`; reporte SHA `61224477f8bca50c8640011f49ee33193eec1a16572ceb4b0f676bcd9a1beb02` según aceptación documentada del operador.
- Fase L V2B static: 198/198; source pins 81/81; authority input pins 9/9; recibo `aa8cebd453b632e445becb936ff3520110d5f80fdf2a732818a6917885595e32`.
- Fase M V2B matriz runtime: 45/45 llamadas al planner y 45/45 procesos Godot; 9/9 selectores, 90 archivos de evidencia; estado `PASS_SAFE_PROJECTION_SEED_SENSITIVITY`; reporte `6e19e88bcce6249f613c7e8566b92f78497c4749bfd079dda2b01e20385072a0`.
- Fase N V2C source-frame: 28 tests Python, pins 81/81, llamadas planner 9/9, 18 procesos Godot, selectores 9/9, evidencias 36/36; reporte `7f96c9aec3849212299afbcabe7fd3045fee815807c9cafe555ad8cb947f91f2`.
- Fase O crosswalk read-only PASS; tests 28/28; selectores 9/9; recibos 18/18; archivos de proceso 36/36; pins de assets 15; filas de campos base 54; custom_data candidates estables 6/6; invocaciones runtime 0; escrituras de fuentes de proyecto 0. Reporte `799d69eba67543b5254016dd3ebc9ac468a2a69f541acd99ee7476c1f53eb0bf`; CSV `a9a38bb2e9ebe01936074f23d9d3059cf3593622f357e3106c75e376a270b0ce`; resumen `36eb3a9aff52e29b727e217cc276b42bafea7e4733ebbdbb3bfb7af12225005e`; output manifest `3f9fda179304cdbded1993afccd097d8eaef93a7f158f92167626ecebce085a0`.

## Phase P — estado al 28-10-2026

### Implementación add-only aplicada

- Contrato V1 SHA `4412fe2291e82e71dae14fe0b48862ba504c879c01882f9216f83d1d04deb041`.
- Schema V1 SHA `b5617785109d543d13f0c5987874eefd5357b00b001348cc55cf23e3fecdba43`.
- Harness in-memory SHA `1124b2bf4fa66f6cd2b9f855cf8d395d7b5274be6a8c0222d53b5e2e95797727`.
- Auditor SHA `b4d06f8cd624037131785360f6658b9d001966d66e47c2a096ba40b73e92c788`.
- Test suite SHA `6ab4d5bacfe0dbe41c9fe9f672d4f264a8fad43ec090836f614cd4bd4a401cdb`.
- Runner con normalización de texto Python SHA `77644d982ed0f552d58561ba05eb4969a76c90703bbb8745dbf73d1bafa3e327`.
- Runbook SHA `a89a571aea726c944071eeb3ede6a57a674727185cb5fda2f0e5f3d1202b23ab`; checkpoint implementación SHA `e360ff642fe1616ce6267ffbaf9893d9bb600125257a5220887a8d3480a07fe6`.

### Evidencia estática del operador

- Preflight Python 3.13.14 PASS.
- Casos de normalización de versión 5/5 PASS; la normalización aparece inmediatamente antes de la validación de versión.
- Tests Phase P 30/30, exit code 0.
- Stdout SHA-256 `a32c904fad96c2068f689d39208029f50946ff73843e4d4055ac6dcc311e73e3`.
- Stderr vacío SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
- Temp log folder `%TEMP%\C11D_PHASE_P_STATIC_TESTS_20261028_6c3212888d134707a4300d1354cbc009`.

Estos datos se registran como evidencia de la salida del operador, no como ejecución independiente del asistente. El runtime Phase P no está aceptado todavía. Un fallo previo en el probe (`py.exe`, error en `<string>`, línea 1) y un parche V3 que no coincidía con su precondición permanecen fallos históricos; no son PASS y no deben repetirse a ciegas. La normalización que actualmente está fijada pasó los cinco casos y los tests estáticos.

## Alcance Phase P

Revisión de procedencia `source-value` vs `frame-value` para los seis candidatos, sin aprobar bindings ni persistir payload:

- `CHALLENGE_003.target_x`: scalar float/escalar; no convertirlo en vector.
- `CHALLENGE_005.target_position`.
- `CHALLENGE_006.target_position`.
- `CHALLENGE_007.target_position`.
- `CHALLENGE_008.active_selection`.
- `CHALLENGE_009.displayed_count`.

El harness solo debe leer la clave allowlisted, mantener valores en memoria, emitir tipos/presencia, relaciones y hashes canónicos; sin volcar todo `FrameSnapshot.custom_data`. Catch/find se tratan como track-only, hit como política constante por ejecución y choose/count mediante checks de relación declarados. La igualdad source↔frame, la estabilidad entre repeticiones y la semántica visual son preguntas diferentes.

## Próxima puerta única

Ejecutar una vez el runner `tools/c11d/d9/run_d_renderer_phase_p_source_value_frame_value_provenance_20261028.ps1` en el checkout Windows actual con el playbook V1. Capturar salida, código de salida, hashes y evidencia de cada proceso. No repetir el runtime si falla: conservar datos y diagnosticar la primera condición fallida.

Tras un runtime PASS, crear un registro de evidencia y revisión/aceptación independiente que valide reporte, recibos de repetición, pins, hashes y locks. Esa aceptación será de procedencia aislada, no de binding aprobado. Solo después revisar qué decisión separada de semántica/temporalidad se requiere. Nunca habilitar renderer/media por inferencia.

## Camino restante hacia un render real del baseline D

1. Aceptar la evidencia de Phase P runtime con un recibo/revisión independiente.
2. Adjudicar por decisiones separadas los candidatos y las condiciones sin resolver; el test de procedencia no decide qué debe mostrarse.
3. Mantener como bloqueantes los conflictos de CHALLENGE_008/009; obtener autoridad explícita antes de alterar duración/fases.
4. Revalidar identidad/I-O y source pins si una futura decisión cambia contrato, fuente o integración.
5. Completar decisiones de binding, regiones/visibilidad, proyección/rounding, sampling, timebase y política de audio/música, cada una con su propio contrato, revisión y pruebas cuando corresponda.
6. Recién con todas las entradas admissibles y gobernadas, preparar el renderer D-owned aislado y sus negative/determinism tests.
7. Mantener D4.8 y todos los gates de media bloqueados hasta su autorización formal; no confundir el primer render técnico con baseline approval.
8. D9.14 real-media certification → D9.16 full acceptance → D9.17 closure adjudication → D10 baseline approval/freeze/promotion, cada puerta por separado.
9. C11-D solo podrá reemplazar C11-C después de aceptación formal, promoción y freeze explícitos.

Este listado es una secuencia de dependencias, no una autorización de comenzar render/media.


## Nota específica sobre el ZIP de releases y la captura usada

El snapshot que llegó primero a la biblioteca (`ChallengeEngineV01_STATELESS_C11-D10_latest_FROZEN_20261028_163525.zip`) se inspeccionó con SHA-256 `199a65ee76eb72a878808cb7b3c862a3eeb945b356cab9726c5d6c86f64b55a1`, tamaño 8.366.872 bytes, 3.476 entradas y CRC limpio. Ese archivo no contenía todavía los artefactos Phase P y, por tanto, no es la captura correcta de continuidad posterior a Phase P.

Aclaración del operador: la divergencia observada en el contenido empaquetado de `releases` está causada por la generación del ZIP freeze/snapshot mediante `c11c-suite` para continuar el trabajo en otra ventana; no es un defecto adicional que deba abrir otra línea de investigación. La nueva captura tendrá una huella de archivo distinta intencionadamente. No invertir más iteraciones en intentar normalizar esa huella del ZIP. Solo comprobar la integridad del archivo y el estado del checkout vivo; no reescribir ni sustituir el manifiesto canónico desde el ZIP.


## 7. Phase P — cierre de procedencia source/frame, 29-10-2026

### Decisión técnica separada

`ACCEPTED_FOR_SOURCE_FRAME_PROVENANCE_ONLY_NO_BINDING_APPROVAL`. Se acepta únicamente la evidencia de procedencia source-value/frame-value de los seis candidatos. No implica aprobación de semántica visual, bindings, candidate input, renderer, media ni baseline. Registro de revisión: `docs/current/d/C11D_PHASE_P_SOURCE_FRAME_PROVENANCE_ACCEPTANCE_REVIEW_20261029_V1.md`.

### Evidencia runtime verificada en Windows

- Runner SHA-256 `e472af0dd7675e85eb2a030eaf06604a78ef409405d8f9a44fa1892d41016a3d`; código de salida `0`.
- Informe `C:\Users\vinxe\AppData\Local\Temp\C11D_PHASE_P_SOURCE_VALUE_FRAME_PROVENANCE_8737e080d2724186b7b6dd8e90243a86\audit\phase_p_provenance_report.json`; SHA-256 `9686240a0e2caa46f05cea4ca2c8fcaaa1499d006ac6ac75d128137693fc2ef7`.
- Stdout exterior SHA-256 `03fe970ae8bf671f91d54495126d229d62aaa211805768e604d47385d79306d2`; stderr exterior vacío `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
- Stdout del auditor SHA-256 `78830f94b3f5bf5f6534edb4387cd14fbcb489ed1b576d201f9c4063c1e10033`; stderr vacío `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
- Godot `4.7.1.stable.mono.official.a13da4feb`; pins Phase P 95/95, pins parent V2C `PASS`, selectores 6/6, planner 6/6, procesos Godot 12/12, hash de repetición `PASS`, 0 relation mismatches.
- Suite estática interna 30/30; stdout `467bbc50acd40227c3f348839807210295018f71ecbdf33757d46e0c5e038876`, stderr vacío `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
- Reconciliación de pins viva 7/7; stdout `58d538e7d2b9929e9b2d4c9ed75bb2dd462697c3543edec4b55f190a47925529`. Suite estática posterior al pin update 30/30; stdout `f964adbd7707591ce90b1a6c37f2d1bf7ce948af47457884cb696d8e11f9e500`.
- Registro de verificación de evidencia: `docs/current/d/C11D_PHASE_P_RUNTIME_EVIDENCE_VERIFICATION_20261029_9bb3b12b1f9b4658b5892679672bbf1a.md`, SHA-256 `8eddd995c4351154275b3a6d60d328a6833c57fd6699dfb4dd698fe30b226d04`.

### Selectores y límites

`CHALLENGE_003.target_x` (escalar), `CHALLENGE_005.target_position`, `CHALLENGE_006.target_position`, `CHALLENGE_007.target_position`, `CHALLENGE_008.active_selection`, `CHALLENGE_009.displayed_count`. Se verificaron dos procesos runtime aislados por selector. `CHALLENGE_008/009` conserva sin resolver la declaración de 11 segundos frente a 12 segundos sumados por fases. No se serializaron valores candidatos ni el mapa `FrameSnapshot.custom_data` completo; no hubo payload materializado ni media; renderer `OFF`; los tres contadores de bindings aprobados siguen a cero.

### Bloqueos previos que quedan históricos

Los registros de fallo quedan inmutables: error de invocación Python inicial; aplicador V3 abortado por precondición; `EVIDENCE_DIR_NOT_EMPTY`; discrepancia inicial del pin `AGENTS.md`; falso bloqueo del verificador por acceder `approved_bindings` en la raíz del contrato; y falso negativo del wrapper `PHASE_P_RUNTIME_SUCCESS_MARKERS_MISSING` después de que el runner terminase con código `0`. Este último se resolvió mediante inspección literal/hash del informe existente sin repetir Godot. Intento registrado en `C11D_PHASE_P_RUNTIME_ATTEMPT_20261029_909376b47e1e4a15bf0bb3e45f3c8d5f.md`, SHA `00e3155bb7ac74d1d8f171bc3ae66b5b9029a7bbf29012509df348db94a56eda`.

### Nueva siguiente acción

Iniciar Phase Q como revisión read-only de decisiones de candidatos y política semántica, usando el informe Phase P aceptado y los artefactos de Phase O. No rerun de Phase P ni de las matrices anteriores por rutina. No escribir bindings ni callsites de renderer. Obtener autoridad explícita antes de decidir `CHALLENGE_008/009` o cualquier binding. La actualización posterior de `AGENTS.md` y `CONTINUE.md` cambia solo la continuidad; todo gate futuro que dependa de esos archivos debe regenerar/reconciliar sus source pins de entrada.

### Gobernanza

Los invariantes de §1 no cambian: C11-C 2.19.12 permanece baseline autoritativo e inmutable; `D4.8=BLOCKED`, `D9.10=PREPARE_ONLY`, `D9.14=BLOCKED`, `D9.16=BLOCKED`, `D9.17=BLOCKED_NO_GO`, `D10=BLOCKED_FOR_PROMOTION`, `baseline_approval=MISSING`, `freeze_eligible=false`, `release_authority=NONE`.
