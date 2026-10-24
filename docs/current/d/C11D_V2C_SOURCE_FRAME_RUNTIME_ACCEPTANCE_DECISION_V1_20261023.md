# C11-D V2-C — decisión de aceptación de runtime de fotogramas fuente

Fecha de registro: 2026-10-23
Estado: PASS_SOURCE_FRAME_ROUTE_ONLY

## Evidencia fijada
- Informe runtime: definitions\c11d\production\D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2C_SOURCE_FRAME_RUNTIME_REPORT_V1_20261023.json
- SHA-256 del informe: 50cbd0604b91cae153dc6e71c3d704ad05bd00a09064096400715f5eb2ed223a
- Informe de origen: C:\Users\vinxe\AppData\Local\Temp\C11DV2CSOURCERUNTIME_056b0672e95a4440b88b46bce4ad5576\report.json
- SHA-256 del contrato runtime: 6d3c59214edbdd917cf63fe9ca4859edb6968d503368ec84e867bdd56a8df74c
- SHA-256 del esquema del informe: 0f75fac465130fed3ea54099d296ad79b0d044cbf11ec37dd1540a09c139d57d
- SHA-256 del harness Godot: ba8500c1db0b86539953c667bc1c48bc765e960f765f7ecef935ff4d206e2a9d
- SHA-256 del runner: a4f5aab8febfb49ec25a97d12f4604137dcbf1c63049a50b0fafe5c0c0c5cdcf
- SHA-256 del test de contrato: f8cb0717f9f90b46071dcbf292a4c308e3dac04b4090a3fd4a0ea53bf627ebfb
- SHA-256 del manifiesto C11-C: e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953

## Resultado
- Tests del contrato antes del runtime: 28/28 PASS.
- Selectores: 9/9 ACCEPTED_SOURCE_FRAME_ONLY.
- Invocaciones del planificador: 9/9.
- Procesos Godot Mono: 18/18; dos ejecuciones por desafío.
- Concordancia entre repeticiones: true para los nueve desafíos.
- Estado global: PASS_SOURCE_FRAME_ROUTE_ONLY.
- Materialización de payload: false.
- Medios creados: false.
- Bindings aprobados: 0.
- Sensibilidad visual a la semilla: NOT_TESTED.

## Conflicto temporal retenido
CHALLENGE_008 y CHALLENGE_009 declaran 11,0 segundos, mientras las fases suman 12,0 segundos. Las dos ejecuciones de cada desafío conservan:
- known_conflict=true
- phase_timeline_acceptance=BLOCKED_TIMEBASE_CONFLICT_SOURCE_FRAME_ONLY

Esta prueba acepta exclusivamente la ruta y los fotogramas fuente. No acepta el timeline ni normaliza el conflicto.

## Decisión
Se acepta la evidencia runtime V2-C para los nueve desafíos en el alcance SOURCE_FRAME_ROUTE_ONLY. El informe se conserva íntegro, con el mismo SHA-256 que el fichero de origen.

No se autoriza la implementación productiva, el binding visual, la admisión de candidatos, la generación automática de semillas, la materialización de payloads, la creación de medios, el renderer ni pruebas de render productivo.

renderer=OFF; media_created=false; approved_bindings=0; candidate_input_admissible=false; automatic_seed_generation=false; master_seed=NOT_ADOPTED; D4.8=BLOCKED; D9.10=PREPARE_ONLY; D9.14=BLOCKED; D9.16=BLOCKED; D9.17=BLOCKED_NO_GO; D10=BLOCKED_FOR_PROMOTION; baseline_approval=MISSING; freeze_eligible=false; release_authority=NONE.

C11-C permanece inmutable y autoritativo.