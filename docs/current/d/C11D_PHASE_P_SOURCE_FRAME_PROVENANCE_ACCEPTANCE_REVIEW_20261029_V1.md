# C11-D Phase P — revisión de evidencia runtime y decisión de alcance V1

**Fecha:** 2026-10-29  
**Decisión:** `ACCEPTED_FOR_SOURCE_FRAME_PROVENANCE_ONLY_NO_BINDING_APPROVAL`  
**Checkout evaluado:** `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`

## 1. Decisión

Se acepta la evidencia técnica de Phase P exclusivamente para el objetivo delimitado de procedencia `source-value` frente a `frame-value` de los seis candidatos permitidos. La decisión se basa en el recibo de auditoría, el código de salida real del runner y la verificación posterior de los archivos de evidencia. No se extiende a aprobación semántica/visual, aprobación de bindings, admisión de candidate input, habilitación del renderer, creación de media o promoción de baseline.

Este registro separa la evidencia de runtime de los falsos bloqueos producidos por las verificaciones PowerShell exteriores. El runner terminó con código `0`; el resultado se verificó posteriormente sin volver a invocar Godot.

## 2. Evidencia runtime aceptada

- Runner: `tools/c11d/d9/run_d_renderer_phase_p_source_value_frame_value_provenance_20261028.ps1`; SHA-256 `e472af0dd7675e85eb2a030eaf06604a78ef409405d8f9a44fa1892d41016a3d`.
- Contrato Phase P: `definitions/c11d/production/D_RENDERER_PHASE_P_SOURCE_VALUE_VS_FRAME_VALUE_PROVENANCE_CONTRACT_V1.json`; SHA-256 `a237e950953e70406cecd4ef94460eb8617482d1d27feebce03e3ef2f6afbb6a`.
- Auditor Python: `tools/c11d/d9/audit_d_renderer_phase_p_source_value_frame_value_provenance_20261028.py`; SHA-256 `2ac08c9e45bbd2f19dbffb0e51f05bb083612f497291e341c15b31ff267ecd62`.
- Manifiesto canónico C11-C: 796318 bytes; SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.
- Godot: `4.7.1.stable.mono.official.a13da4feb`.
- Informe runtime: `C:\Users\vinxe\AppData\Local\Temp\C11D_PHASE_P_SOURCE_VALUE_FRAME_PROVENANCE_8737e080d2724186b7b6dd8e90243a86\audit\phase_p_provenance_report.json`; SHA-256 `9686240a0e2caa46f05cea4ca2c8fcaaa1499d006ac6ac75d128137693fc2ef7`.
- Stdout exterior del runner: `C:\Users\vinxe\AppData\Local\Temp\C11D_PHASE_P_RUNTIME_909376b47e1e4a15bf0bb3e45f3c8d5f.stdout.txt`; SHA-256 `03fe970ae8bf671f91d54495126d229d62aaa211805768e604d47385d79306d2`.
- Stderr exterior del runner: `C:\Users\vinxe\AppData\Local\Temp\C11D_PHASE_P_RUNTIME_909376b47e1e4a15bf0bb3e45f3c8d5f.stderr.txt`; vacío; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
- Stdout de auditoría interna: SHA-256 `78830f94b3f5bf5f6534edb4387cd14fbcb489ed1b576d201f9c4063c1e10033`; stderr vacío SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
- Suite estática ejecutada por el runner: 30/30; stdout SHA-256 `467bbc50acd40227c3f348839807210295018f71ecbdf33757d46e0c5e038876`; stderr vacío SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
- Registro de verificación de evidencia: `docs/current/d/C11D_PHASE_P_RUNTIME_EVIDENCE_VERIFICATION_20261029_9bb3b12b1f9b4658b5892679672bbf1a.md`; SHA-256 `8eddd995c4351154275b3a6d60d328a6833c57fd6699dfb4dd698fe30b226d04`.

## 3. Resultados verificados

| Control | Resultado aceptado |
|---|---|
| Contrato/source pins Phase P | 95/95; `PASS` antes y después del runtime |
| Pins parent V2C | `PASS` |
| Selectores | 6/6 |
| Invocaciones del planner canónico | 6/6 |
| Procesos runtime Godot independientes | 12/12 |
| Concordancia de hashes entre repeticiones | `PASS` en los seis selectores |
| Relaciones source/frame | 0 mismatches por selector |
| Serialización de valores candidatos | `false` |
| Serialización del mapa `custom_data` completo | `false` |
| Media creada / payload materializado | `false` / `false` |
| Renderer | `OFF` |
| Bindings aprobados | 0 |

Selectores cubiertos en orden contractual:

1. `CHALLENGE_003.target_x` — permanece escalar.
2. `CHALLENGE_005.target_position`.
3. `CHALLENGE_006.target_position`.
4. `CHALLENGE_007.target_position`.
5. `CHALLENGE_008.active_selection`.
6. `CHALLENGE_009.displayed_count`.

El conflicto temporal de `CHALLENGE_008` y `CHALLENGE_009` se preservó sin resolver: duración declarada de 11 segundos frente a suma de fases de 12 segundos. No se ha inferido una corrección.

## 4. Pruebas previas ya superadas; no repetir por rutina

- Preflight de Python: `Python 3.13.14`; `py -3.13 --version` y la consulta de `sys.executable` devolvieron código `0`.
- Regresión de normalización/preflight: 6/6; stdout SHA-256 `4a1fd011ad29d742c907c7524328a98e1395cdd6f3f253edf2b05d34d5ee360e`.
- Regresión de aislamiento de evidencias: 6/6; stdout SHA-256 `9fdd7aaa170004770f4f1e319456705819aa0aac74b1f43fb71c14854d291f29`.
- Reconciliación de pins vivos: 7/7; stdout SHA-256 `58d538e7d2b9929e9b2d4c9ed75bb2dd462697c3543edec4b55f190a47925529`.
- Suite estática Phase P tras reconciliación: 30/30, código `0`; stdout SHA-256 `f964adbd7707591ce90b1a6c37f2d1bf7ce948af47457884cb696d8e11f9e500`; stderr vacío `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
- Preflight de gobernanza antes del runtime: manifiesto, runner, contrato y auditor coincidieron con sus hashes fijados.

## 5. Historial de bloqueos y cómo se clasifican

Los registros anteriores son históricos e inmutables; no se borran ni se convierten retroactivamente en PASS:

1. Sonda inicial Python combinada falló por comillas internas retiradas por la invocación nativa; se reemplazó por consultas separadas y validación de versión normalizada.
2. Aplicador V3 de aislamiento: abortó por precondición incompatible; no aplicó.
3. Primer runtime: `EVIDENCE_DIR_NOT_EMPTY`; bloqueado antes de acreditar procesos de los seis selectores. Se corrigió el enrutamiento a un subdirectorio de auditoría vacío.
4. Runtime posterior: `PIN_MISMATCH:AGENTS.md`; bloqueado antes de acreditar matriz runtime. Se reconciliaron de forma exacta los pins del contrato y la constante del auditor.
5. Intento de verificación exterior: error al leer `approved_bindings` en la raíz del contrato; propiedad ubicada dentro de `semantic_binding_policy`. El runner no se había ejecutado en ese intento.
6. Runtime real posterior: el runner acabó con código `0` y emitió los marcadores runtime correctos, pero el wrapper exterior informó `PHASE_P_RUNTIME_SUCCESS_MARKERS_MISSING`. La comprobación literal posterior validó los marcadores y el informe existente sin volver a ejecutar Godot. Registro del intento: `C11D_PHASE_P_RUNTIME_ATTEMPT_20261029_909376b47e1e4a15bf0bb3e45f3c8d5f.md`, SHA-256 `00e3155bb7ac74d1d8f171bc3ae66b5b9029a7bbf29012509df348db94a56eda`. Registro de verificación posterior: SHA-256 `8eddd995c4351154275b3a6d60d328a6833c57fd6699dfb4dd698fe30b226d04`.

## 6. Límite de aceptación

Esta decisión acepta la procedencia runtime, no la semántica de presentación ni el enlace a un renderer. El contrato mantiene `PREPARATION_ONLY_PROVENANCE_EVIDENCE_NOT_BINDING_APPROVAL`. Los datos siguen siendo valores acotados y hashes: no se vuelca el mapa completo `FrameSnapshot.custom_data`.

## 7. Próxima puerta de ingeniería

Abrir un workstream de decisión review-only (Phase Q) para seis candidatos; producir una matriz de decisión que separe por candidato: evidencia source/frame, significado de producto, política temporal, proyección/rounding, sampling, visibilidad y autoridad requerida. No escribir bindings ni callsites productivos. Los selectores 008/009 permanecen bloqueados para una decisión semántica definitiva hasta que exista autoridad explícita sobre 11s frente a 12s. Toda futura revisión que dependa de `AGENTS.md`/`CONTINUE.md` debe reanclar sus pins porque estas instrucciones de continuidad se actualizan después del recibo Phase P.

## 8. Hard locks

`renderer=OFF`; `media_created=false`; `payload_materialized=false`; `candidate_input_admissible=false`; `seed_domains_complete_for_candidate_input=false`; `automatic_seed_generation=false`; `master_seed=NOT_ADOPTED`; `approved_bindings=0`; `approved_custom_data_bindings=0`; `approved_renderer_projection_bindings=0`; `D4.8=BLOCKED`; `D9.10=PREPARE_ONLY`; `D9.14=BLOCKED`; `D9.16=BLOCKED`; `D9.17=BLOCKED_NO_GO`; `D10=BLOCKED_FOR_PROMOTION`; `baseline_approval=MISSING`; `freeze_eligible=false`; `release_authority=NONE`.
