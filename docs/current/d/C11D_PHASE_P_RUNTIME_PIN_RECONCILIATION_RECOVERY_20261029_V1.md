# C11-D Phase P — Live source-pin reconciliation recovery V1

**Fecha:** 2026-10-29  
**Estado:** `RUNTIME_BLOCKED_SOURCE_PIN_RECONCILIATION`; no formal Phase P acceptance.

## Propósito

Registrar los hitos verificados y corregir la divergencia documental que detuvo la segunda ejecución runtime. Este documento es add-only; no sustituye entradas históricas, no actualiza el baseline C11-C y no concede permisos de renderer, payload, media, bindings o release.

## Hitos ya verificados desde Windows

1. El manifiesto canónico vivo `release/C11C_FREEZE_PACKAGE_MANIFEST.json` mantiene 796.318 bytes y SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.
2. Corrección del preflight de Python aplicada con guardas. La versión observada es Python 3.13.14; `--version` y `sys.executable` terminan con código 0. Runner intermedio tras ese fix: `8c3d2a3b5fa137fe4bac7989f8a6a394464f432a75c0a73257836f6eb3989249`.
3. Corrección de aislamiento de evidencia aplicada add-only. Runner actual antes de reconciliar pins: `e472af0dd7675e85eb2a030eaf06604a78ef409405d8f9a44fa1892d41016a3d`.
4. Regresión de aislamiento: código 0, `PHASE_P_EVIDENCE_DIRECTORY_ISOLATION_REGRESSION=6/6`; stdout SHA-256 `9fdd7aaa170004770f4f1e319456705819aa0aac74b1f43fb71c14854d291f29`; stderr SHA-256 `190ca6a3faa8ec09de9856e879d56af5f03dfd599364b441be770de7f66cf716`.
5. Regresión de versión Python: código 0, `PHASE_P_PYTHON_VERSION_CHECK_REGRESSION=6/6`; stdout SHA-256 `4a1fd011ad29d742c907c7524328a98e1395cdd6f3f253edf2b05d34d5ee360e`; stderr SHA-256 `e349c0fa0d6014009bf303f3c784b5bbca28d25fadc8390f805c50fda263b6ca`.
6. Suite estática Phase P: código 0, 30/30; stdout SHA-256 `b0d6d3091b61e313136207a82f2e3d4e6a7e1d7fc9db79c132cd3c9f1aa52089`; stderr vacío, SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
7. Preflight combinado más pruebas estáticas confirmó Python 3.13.14, aislamiento 6/6, regresión Python 6/6 y suite Phase P 30/30. No se invocó Godot en esa etapa.

## Incidentes runtime registrados, sin reejecución automática

### Intento runtime 1 — directorio de evidencia prellenado

- Código de salida del runner: `1`.
- Causa: `EVIDENCE_DIR_NOT_EMPTY`; el wrapper había creado `runner.stdout.txt` y `runner.stderr.txt` en el mismo directorio que la auditoría Python exige vacío.
- Stdout exterior SHA-256: `db51bc16904b4f31707603ec53da775f0e4de899d4a03e75afbca2be03f03198`.
- Stderr exterior SHA-256: `dc573088162a53ab651f59a1f862d37b219133fb372517be17e9bd304b2fe36e`.
- Resolución implementada: separar los logs del wrapper en el directorio padre y usar un subdirectorio `audit` que el wrapper no precrea.

### Intento runtime 2 — pin de instrucciones obsoleto

- Código de salida del runner: `1`.
- La auditoría falló en la verificación de pins, antes de resolver Godot y antes de crear procesos runtime.
- Error: `PHASE_P_SOURCE_PIN_RECONCILIATION_FAILED:PIN_MISMATCH:AGENTS.md:sha=67c5f237035c121f27733c24f3b2fe2da2bb104eaaa5f95e4c7a88b573071599:bytes=4851`.
- Stdout exterior SHA-256: `4297171e7decdf5e3978ac8ee4a2b3fb46ebe61e6da6d110fef1620df8ea12ce`.
- Stderr exterior SHA-256: `39be1a0a75600dabe437a2444c0aac1e42f11beab067af03c475358b18d4a23a`.
- Directorio de evidencia conservado: `%TEMP%\C11D_PHASE_P_SOURCE_VALUE_FRAME_PROVENANCE_debc2c59d0f8425db686ccf236ce9b2c`.

## Causa demostrada y corrección

El contrato Phase P original (SHA-256 `4412fe2291e82e71dae14fe0b48862ba504c879c01882f9216f83d1d04deb041`) incluía los pins V24 de `AGENTS.md` (4.137 bytes, SHA `a33caf3528a239049d7a84189584dfd661a1b12d6c48ec599ba3de51315b06f2`) y `.continue/rules/CONTINUE.md` (2.493 bytes, SHA `8a6ea4611a2bc710a41fde7d02da2dcbf108e910c4daaad9b37f611d234541cd`). El checkout vivo tiene la continuidad V25, con estos contenidos e identidades:

| Archivo | Bytes actuales | SHA-256 actual |
|---|---:|---|
| `AGENTS.md` | 4.851 | `67c5f237035c121f27733c24f3b2fe2da2bb104eaaa5f95e4c7a88b573071599` |
| `.continue/rules/CONTINUE.md` | 3.599 | `8ee4f47588acbc981bd11400ad4186a598e052e279b8f2e2cc0bd87cb6b21c71` |

No se deben restaurar los documentos V24: los contenidos V25 son los activos declarados en la continuidad actual. Tampoco se debe desactivar la reconciliación de pins.

La corrección acotada actualiza exclusivamente esas dos entradas `source_pins` del contrato, mantiene `source_pin_count=95` y mantiene todos los controles de gobernanza. Se actualiza la constante `EXPECTED_PHASE_P_CONTRACT_SHA256` del auditor al nuevo SHA del contrato `a237e950953e70406cecd4ef94460eb8617482d1d27feebce03e3ef2f6afbb6a`. No se cambian los pins de C11-C ni ningún archivo de su baseline. El hash SHA-256 del auditor tras ajustar esa constante será `2ac08c9e45bbd2f19dbffb0e51f05bb083612f497291e341c15b31ff267ecd62`.

## Prueba de regresión añadida

`tools/c11d/d9/test_d_renderer_phase_p_live_source_pin_reconciliation_20261029.py`

SHA-256: `5c5abd891ad3c566075e62149a97d7bbe5d274d93ec01840cbdb96270c705dc3`.

Verifica: identidad y hash del contrato; pins de ambos documentos V25; los 95 pins sobre el checkout vivo; unicidad/denominador; manifiesto canónico C11-C; y locks de gobernanza. Es una prueba estática, sin Godot ni runtime.

## Secuencia pendiente

1. Aplicar el overlay de reconciliación con precondiciones exactas y backup.
2. Ejecutar el test nuevo de pins 7/7 y los tests Phase P estáticos 30/30, porque el contrato y el auditor han cambiado. La regresión de aislamiento 6/6 y la de Python 6/6 ya pasaron y sus objetivos no cambian en este parche; no repetirlas salvo que cambie su código. Si algún pin vivo adicional no coincide, detenerse y registrar esa divergencia antes de runtime.
3. Solo si los cuatro resultados pasan, ejecutar una sola vez la auditoría runtime con logs y recibo preservados.
4. Revisar el recibo y los hashes antes de aceptar formalmente Phase P. Actualizar los documentos de continuidad vigentes solo tras esa revisión; mantener el ledger histórico sin sobrescribirlo.

## Gobernanza activa

`renderer=OFF`; `media_created=false`; `payload_materialized=false`; `candidate_input_admissible=false`; `seed_domains_complete_for_candidate_input=false`; `automatic_seed_generation=false`; `master_seed=NOT_ADOPTED`; `approved_bindings=0`; `approved_custom_data_bindings=0`; `approved_renderer_projection_bindings=0`; `D4.8=BLOCKED`; `D9.10=PREPARE_ONLY`; `D9.14=BLOCKED`; `D9.16=BLOCKED`; `D9.17=BLOCKED_NO_GO`; `D10=BLOCKED_FOR_PROMOTION`; `baseline_approval=MISSING`; `freeze_eligible=false`; `release_authority=NONE`.

`winning_frame` sigue siendo el único anclaje temporal de Challenge; `close_calls`, contador de episodios. El conflicto de duración de `CHALLENGE_008/009` (11 s declarados frente a 12 s por suma de fases) permanece sin resolver. La prueba de esta conciliación no aprueba bindings, no crea renderer/media/payload y no supone aceptación de Phase P.
