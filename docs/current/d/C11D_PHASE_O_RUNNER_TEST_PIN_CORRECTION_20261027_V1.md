# C11-D Fase O — corrección del pin de tests V4

Fecha: 2026-10-27

## Registro del fallo V3

La aplicación del overlay de firma del resolver se verificó con `3/3` sustituciones guarded y `1/1` archivo add-only. Al iniciar el lanzador de Fase O, este se detuvo antes de ejecutar los tests porque el pin de tests todavía esperaba el SHA de la versión anterior (`3fe5e53bd338e91d52b3e460f5d052d151b6fc8aabd2bffbf8db8e8b36f9bc4f`), mientras que el archivo instalado por V3 tenía SHA-256 `b5bbf67e071a5eac7e1aeb6eda002782914b1d4790ebce7b825fd774050c23f9`.

## Corrección V4

Se sustituye únicamente ese valor esperado en `run_d_renderer_phase_o_source_frame_semantic_binding_crosswalk_20261027.ps1`. No cambian el audit Python, el test Python ni los contratos de entrada. El aceptador exige ahora el hash real de la suite V3 y el marcador `PHASE_O_UNIT_TESTS=28/28`.

- Hash previo del lanzador: `da084c197fefbb66b5efd7dbc3a3ebc6a609c31f986c8adcf50f2c04fa3d74af`
- Hash actualizado del lanzador: `4625d36d5673dbe8f2f759fe5b6a1a1f98ce138c077bb6a3f9dbf04203a1b80b`
- Hash del test Python esperado: `b5bbf67e071a5eac7e1aeb6eda002782914b1d4790ebce7b825fd774050c23f9`

## Política y siguiente puerta

La próxima ejecución vuelve a ejecutar únicamente los tests de la auditoría Fase O y después la auditoría de solo lectura sobre los recibos V2-C existentes. No se repite V2-C, no se llama al planner ni a Godot, no se materializa payload/media y no se actualizan checkpoint/ledger desde este parche.

Los 27 tests previos de V3 habían sido incorporados, y la suite V3 se había verificado en preparación como 28/28; la ejecución Windows aún debe aportar la evidencia final de esta revisión. Un `PASS` de la auditoría clasificará evidencia, no aprobará bindings.

## Invariantes preservados

- `renderer=OFF`
- `media_created=false`
- `payload_materialized=false`
- `candidate_input_admissible=false`
- `D4.8=BLOCKED`
- `release_authority=NONE`
- `approved_bindings=0`

Se conserva el intento de Fase O anterior y sus logs en `%TEMP%`; no eliminar marcadores ni relanzar sobre un marcador de finalización existente.
