# Revisión de evidencia de composición V2B — 2026-10-26, V1

**Estado de esta captura:** `CAPTURED_OPERATOR_RUNTIME_PASS_PENDING_FORMAL_REVIEW`  
**Alcance:** prueba aislada de composición de cuatro `SimulationResult` reales; no es aceptación de integración productiva.

## Evidencia observada en la consola Windows

### Gates estáticos

| Gate | Resultado | Código | stdout SHA-256 | stderr SHA-256 |
|---|---:|---:|---|---|
| `runtime_static_v1` | 113/113 PASS | 0 | `ca63239a81d23fd3bef046db02c67d7565aa4b24aefef4c1b849af71d1ecef8e` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `runtime_static_v2` | 115/115 PASS | 0 | `bbf030cb4aa8319d007eae259a7dac52294a29fc9cddd1d242b09306b25548df` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `composition_static` | 132/132 PASS | 0 | `74aad0a3ef62052e211932328d0a7d780c00ea1bb1bc1c118c2ff01a4e30a84f` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

Hashes de las fuentes de test: V1 `c18082f7ad62722153088b07ade0f1753be739a7a6b00da0d08bf1db4e671946`, V2 `a3e13c382cf0fb7ebaa57896b75d36809ebfd09e6425f87936b9f2a2b8be7a1e`, composición `37317cd3462e555afba5c883aef97e6632ec9387d099fd33c24e4ab1d0c14c14`. Recibo de diseño anterior `235/235`: `9148ad3dfc21857d7decf5885a3fb0e10a839234ba7672040cfdfa86b57c7bd2`.

### Runtime Godot

- Runtime: `4.7.1.stable.mono.official.a13da4feb`; proceso headless, código de salida `0`.
- stdout SHA-256: `b5e1465894a9d5ad5a26715f10459bf578809d4a3fadce7fc030b4964aa2c3bb`; stderr SHA-256 (vacío): `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
- Marcador PASS de composición: una aparición; marcador FAIL: cero; error/traceback: ninguno.
- `CHALLENGE_003`: 420 source frames y 420 marker frames.
- `CHALLENGE_005`: 420 source frames y 420 marker frames.
- `CHALLENGE_006`: 420 source frames y 420 marker frames.
- `CHALLENGE_007`: 420 source frames y 420 marker frames.
- Totales: candidatos `4/4`; source frames `1680/1680`; marker frames `1680/1680`.
- Acceso a `custom_data`: una llamada allowlisted `Dictionary.get` por frame en el consumidor; lecturas directas del harness `0`; valores crudos en logs `false`.
- Llamadas de producción `0`; renderer `OFF`; medios creados `false`; payload materializado `false`; C11-C inmutable `true`.

## Identidad de las fuentes actuales

| Artefacto | SHA-256 actual |
|---|---|
| Manifiesto congelado C11-C | `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953` |
| Contrato de composición V1 (retiene estado pre-run) | `575717bb3f36b476c9742488c8cace622a217c8861e376d17c519d02c70534b7` |
| Esquema del contrato de composición | `a24948379e03762b8074b571801a3eb12f5ae006fcf4443ce4f4f7b9330cebae` |
| Harness runtime corregido | `06417bf63a8c89c4ac5afb0ab818b3b395c48e31c5a0c6d45bd10e1aadccaa28` |
| Suite estática de composición corregida | `37317cd3462e555afba5c883aef97e6632ec9387d099fd33c24e4ab1d0c14c14` |
| Consumidor review-only V2 | `2376d4c9208d749b3681f8083d1d0be1a5658f62930b9b92167916196aec3eef` |
| Suite estática runtime V1 | `c18082f7ad62722153088b07ade0f1753be739a7a6b00da0d08bf1db4e671946` |
| Suite estática runtime V2 | `a3e13c382cf0fb7ebaa57896b75d36809ebfd09e6425f87936b9f2a2b8be7a1e` |
| Recibo de aceptación de consumidor V2 (predecesor) | `5ce4cddace9a8a04b4c1ba520cfdeeb79ee3a7e1952dc70f60baf45e02623d34` |

El contrato de composición declara 81 pins de fuentes parent. El validador nuevo los vuelve a comprobar en el checkout activo, junto con los 6 runtime-input pins del contrato y los hashes enumerados arriba.

## Discrepancia adicional del manifiesto congelado dentro del ZIP

El archivo ZIP íntegro contiene un `release/C11C_FREEZE_PACKAGE_MANIFEST.json` cuyo hash actual es `f6b2fc6ce36973eb620738c8446d529d98da0fb79892132cf4708e6f453051b5` y tamaño `1070256`; además, ese manifiesto declara `generated_at_utc=2026-10-26T00:38:03.0481714Z` y `source_tree_sha256=74c3cc20ba41ba51b131f6c42c313161409b05ffa54911790833e7312ce5ba43`. La entrada que se auto-declara en `source_files` fija `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953` y `796318` bytes. No son los mismos bytes. El checkout Windows había reportado previamente el hash congelado esperado `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`, pero debe verificarse de nuevo sobre el checkout activo antes de aplicar este overlay o validar la evidencia. El manifiesto incluido en el ZIP no se trata como autoridad y jamás debe copiarse encima del manifiesto congelado.

## Diferencia frente al recibo histórico

El recibo histórico V1 de 23-10-2026 conserva SHA `a4684fdb7b3ea4b85f68b561d9aaa64981517f65530ba8a8787f820eb5e3960f` y la decisión de aquella ejecución conserva SHA `a52d5d8a4564cc96d47633c5527248bdc102152da8ce13ad699575fb5b677a08`. Aquellos artefactos fijan contrato `d3265f1ba91dc664e85bbb0dc87ea6b145f0fed34ffa4552412c8fa70c19b2ab`, suite estática `5c69f08194213b7bcf48fe7f52bd17e8ec29a2d6e275c4c73787e7fa20b174ff` y harness `74fe446ef69c92de0291aa739caf1b5c25dbcdaed7f9939eb1e63c9a4623cfe2`. El recibo V2 adjunto preserva la historia y liga el resultado a los hashes actuales. No se infiere que el contenido sea productivo por haber pasado la prueba.

## Clasificación y siguiente gate

El recibo V2 se ha generado a partir del transcript confirmado por el operador y espera validación contra los archivos temporales reales en Windows. Su estado no equivale a una decisión de aprobación.

**Siguiente gate:** ejecutar `tools/c11d/d9/test_d_renderer_challenge_visual_payload_v2b_source_composition_runtime_evidence_v2.py` con la raíz del repositorio y el directorio temporal runtime. Si el validador pasa, completar revisión separada del recibo antes de redactar cualquier propuesta de integración.

## Bloqueos que no cambian

`renderer=OFF`; `media_created=false`; `payload_materialized=false`; `candidate_input_admissible=false`; `seed_domains_complete_for_candidate_input=false`; `automatic_seed_generation=false`; `master_seed=NOT_ADOPTED`; `approved_bindings=0`; `approved_custom_data_bindings=0`; `approved_renderer_projection_bindings=0`; `D4.8=BLOCKED`; `D9.10=PREPARE_ONLY`; `D9.14=BLOCKED`; `D9.16=BLOCKED`; `D9.17=BLOCKED_NO_GO`; `D10=BLOCKED_FOR_PROMOTION`; `baseline_approval=MISSING`; `freeze_eligible=false`; `release_authority=NONE`.
