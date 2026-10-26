# Informe de reconciliación del snapshot C11-D — 2026-10-26, V1

## Identidad del snapshot revisado

- Archivo de referencia: `ChallengeEngineV01_STATELESS_C11-D_20261026_013616.zip`
- SHA-256 del ZIP: `3e48ee2d815593137f5863139e05c1aa04eb40b4a58ddfb3bed4507125c96874`
- Tamaño: `8,001,498` bytes
- Entradas ZIP: `3,378`; `ZipFile.testzip()` no encontró entrada corrupta.
- El ZIP pasa la comprobación CRC de integridad; esto solo acredita que las entradas ZIP no presentan errores CRC. El manifiesto embebido declara `generated_at_utc=2026-10-26T00:38:03.0481714Z` y `source_tree_sha256=74c3cc20ba41ba51b131f6c42c313161409b05ffa54911790833e7312ce5ba43`; esos valores no sustituyen la identidad congelada conocida.
- **Discrepancia crítica de procedencia:** el archivo `release/C11C_FREEZE_PACKAGE_MANIFEST.json` dentro del ZIP tiene SHA-256 `f6b2fc6ce36973eb620738c8446d529d98da0fb79892132cf4708e6f453051b5` y tamaño `1070256` bytes. Su propia entrada `source_files` declara SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953` y tamaño `796318` bytes. El hash `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953` es la identidad congelada esperada; el archivo incluido en este ZIP no coincide con ella.
- Auditoría de los pins fuente declarados por el contrato de composición: `80/81` parent source pins coinciden con los bytes del snapshot; el único desacuerdo es `release/C11C_FREEZE_PACKAGE_MANIFEST.json`. Los runtime-input pins coinciden `6/6`. Esta comparación del ZIP no sustituye la comprobación del checkout Windows activo.
- El transcript Windows previo a la subida informó `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953` para el manifiesto del checkout activo, pero esa identidad debe reconfirmarse en el checkout vivo antes de aplicar el overlay o validar el recibo. No extraer este ZIP sobre el checkout, no restaurar el manifiesto desde este ZIP y detenerse si el hash/tamaño activo no son exactamente los esperados.
- El ZIP se usó como snapshot de referencia. El checkout Windows activo sigue siendo la autoridad para ejecutar y aceptar pruebas; no se debe extraer el ZIP encima del checkout.

## Resultado del estado técnico reconciliado

1. La corrección de callsites de V2B está en el snapshot: los dos suites estáticos de consumo permiten exactamente los tres callsites de pruebas (V1, V2 y source-composition harness), y el inventario estático mantiene `production_calls=0`.
2. Los tres gates de esta secuencia pasaron en la consola Windows del operador: runtime static V1 `113/113`, runtime static V2 `115/115`, source-composition static `132/132`. Códigos de salida `0`; los tres `stderr` están vacíos.
3. El runtime de composición en Godot Mono `4.7.1.stable.mono.official.a13da4feb` terminó con código `0`, un marcador PASS, cero marcador FAIL, cero marcador de error, candidatos `CHALLENGE_003/005/006/007` `4/4`, source frames `1680/1680`, marker frames `1680/1680` y `stderr` vacío.
4. La prueba es de composición en memoria del `SimulationResult` real con el consumidor review-only. No genera video ni frames renderizados de entrega, no llama al renderer, no serializa `FrameSnapshot.custom_data` completo, no registra valores crudos ni crea medios.

## Reconciliación de la evidencia histórica

El recibo histórico `definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_ALLOWLISTED_COORDINATE_SOURCE_COMPOSITION_RUNTIME_EVIDENCE_V1_20261023.json` sí está incluido y conserva SHA-256 `a4684fdb7b3ea4b85f68b561d9aaa64981517f65530ba8a8787f820eb5e3960f`. Su decisión asociada `docs/current/d/C11D_V2B_ALLOWLISTED_COORDINATE_SOURCE_COMPOSITION_RUNTIME_DECISION_V1_20261023.md` conserva SHA-256 `a52d5d8a4564cc96d47633c5527248bdc102152da8ce13ad699575fb5b677a08`. No se han alterado ni deben sobrescribirse.

Sin embargo, el recibo V1 se refiere a la revisión anterior de las fuentes:

| Artefacto | SHA histórico V1 | SHA actual del snapshot |
|---|---|---|
| Contrato de composición | `d3265f1ba91dc664e85bbb0dc87ea6b145f0fed34ffa4552412c8fa70c19b2ab` | `575717bb3f36b476c9742488c8cace622a217c8861e376d17c519d02c70534b7` |
| Suite estática de composición | `5c69f08194213b7bcf48fe7f52bd17e8ec29a2d6e275c4c73787e7fa20b174ff` | `37317cd3462e555afba5c883aef97e6632ec9387d099fd33c24e4ab1d0c14c14` |
| Harness runtime | `74fe446ef69c92de0291aa739caf1b5c25dbcdaed7f9939eb1e63c9a4623cfe2` | `06417bf63a8c89c4ac5afb0ab818b3b395c48e31c5a0c6d45bd10e1aadccaa28` |

El stdout de la ejecución actual tiene SHA `b5e1465894a9d5ad5a26715f10459bf578809d4a3fadce7fc030b4964aa2c3bb` (el mismo hash de salida registrado históricamente). Esa igualdad de salida no reemplaza la obligación de fijar los hashes actuales de contrato y harness. Además, el desacuerdo del manifiesto de congelación dentro del ZIP se mantiene como discrepancia de procedencia independiente y bloquea cualquier afirmación de que la copia del manifiesto dentro del snapshot sea el artefacto congelado canónico. Por ello, el overlay adjunta un recibo V2 con nueva identidad de fuente y estado `CAPTURED_OPERATOR_RUNTIME_PASS_PENDING_FORMAL_REVIEW`.

## Autoridad y bloqueos

El contrato de composición actual conserva `status=PENDING_OPERATOR_SOURCE_RUNTIME_COMPOSITION_TEST` y `runtime_test_contract.status=PENDING_OPERATOR_GODOT_MONO_RUN`. Ese estado se mantiene intencionadamente: la suite estática vigente verifica el estado pre-ejecución del contrato. La nueva evidencia post-ejecución se registra separadamente; no se cambia ni se reescribe el contrato en este incremento.

Se conservan `renderer=OFF`, `media_created=false`, `payload_materialized=false`, `candidate_input_admissible=false`, `seed_domains_complete_for_candidate_input=false`, `automatic_seed_generation=false`, `master_seed=NOT_ADOPTED`, bindings aprobados `0`, `D4.8=BLOCKED`, `D9.10=PREPARE_ONLY`, `D9.14=BLOCKED`, `D9.16=BLOCKED`, `D9.17=BLOCKED_NO_GO`, `D10=BLOCKED_FOR_PROMOTION`, `baseline_approval=MISSING`, `freeze_eligible=false` y `release_authority=NONE`.

El conflicto `CHALLENGE_008/009` (declarado 11 s frente a 12 s sumados por las fases) no se resuelve en esta revisión. Tampoco se demuestra sensibilidad visual a la semilla en los nueve desafíos, la admisión general de candidatos, integración con el renderer, salida media real ni aptitud de cierre D10.

## Higiene documental identificada

Los apuntadores estables `AGENTS.md`, `.continue/rules/CONTINUE.md`, `docs/current/d/MASTER_HANDOVER_C11D_CURRENT.md` y `docs/current/d/START_PROMPT_C11D_CURRENT.md` señalan checkpoints de 16–17 de octubre que preceden al trabajo actual. El overlay los actualiza mediante reemplazo protegido por SHA previo, copia de seguridad y comprobación post-aplicación; antes de aplicar, exige que el manifiesto en el checkout activo coincida con el hash congelado y tamaño conocidos. El desacuerdo del manifiesto incluido en el ZIP no se corrige ni se copia desde el snapshot. Los checkpoints y prompts fechados antiguos no se sobrescriben.

## Próxima secuencia autorizada

1. Confirmar en el checkout activo que `release/C11C_FREEZE_PACKAGE_MANIFEST.json` tiene exactamente SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953` y tamaño `796318` bytes. Si no coincide, parar y reconciliar la procedencia; no sustituirlo con la copia del ZIP.
2. Aplicar el overlay con comprobación del SHA del ZIP, precondiciones, backup de los cuatro apuntadores estables, ausencia de los destinos nuevos y verificación post-aplicación.
3. Ejecutar en el checkout Windows el validador del recibo V2 contra el log real de `%TEMP%`. El validador vuelve a verificar 81 pins fuente declarados por el contrato además de los pins V2 y los logs.
4. Revisar el recibo V2 y registrar, como artefacto separado, el resultado de la revisión de operador. No proponer integración productiva hasta terminar esa revisión y revisar todos los permisos pertinentes.
5. Cualquier propuesta posterior es un gate separado; este PASS no autoriza bindings, consumo productivo, dispatch, payload materialization, renderer, media, render test, baseline freeze, promotion ni release.
