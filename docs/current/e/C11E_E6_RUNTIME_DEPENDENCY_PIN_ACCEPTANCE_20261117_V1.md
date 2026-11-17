# C11-E E6 — Aceptación del baseline de dependencias runtime V1

**Fecha:** 2026-11-17  
**Estado:** `ACCEPTED_FOR_E6_STATIC_ROUTE_DEPENDENCY_SCOPE_ONLY`  
**Alcance:** identidad de fuentes para cerrar la ruta estática Challenge; no autorización de ejecución.

## Decisión técnica

Se acepta el conjunto de nueve dependencias adicionales como pins de fuente del alcance estático E6 Challenge. La aceptación se basa en tres evidencias encadenadas: auditoría de ruta V2, auditoría de dependencias 33/33 y la instalación del handover que volvió a rehashear 33/33 archivos. El instalador de este overlay vuelve a verificar todas las huellas en el checkout activo antes de añadir el suplemento.

Esta aceptación es estrictamente de **identidad de bytes**. No certifica el comportamiento runtime de Godot, no prueba el Movie Maker, no autoriza D3/audio/FFmpeg/FFprobe/mux, no acepta Smoke18 ni modifica D4.8. Tampoco cambia el manifest congelado C11-C.

## Nueve pins aceptados en el alcance E6 estático

| Dependencia | Bytes | SHA-256 |
|---|---:|---|
| `project.godot` | 868 | `d20b0f275c58a34881420705bb1990564d719427c550478c434345ced72805d3` |
| `Main.tscn` | 1086 | `5271714b9a5c31aeda1d7347347f1429ca37a48c081e59e6ec42383626731de7` |
| `core/authoring/ChallengeMigrationAdapter.gd` | 8977 | `79099cbb5fea9d9c5c519370b1c56d72c8394db14e9adf5b0bb744410e507c13` |
| `core/execution/ChallengeTimelineBuilder.gd` | 3721 | `35a47ad126a2e11577933a03b251f47732e580693e5c08e45d3b6af047c8c9af` |
| `core/authoring/ChallengeTimeLiine.gd` | 1501 | `a0276e86ac27389f4abd0d5cd9b998e97a32162de44e2f917d7158255892ce71` |
| `core/authoring/TemporalCore.gd` | 851 | `f076e9090c3d13be63b7ccda91a5861576a4d32eb673380a95272b3b3fa27966` |
| `core/validation/ChallengeDefinitionValidator.gd` | 4906 | `d7c1c50f505853ebef376b75ac8ef675a4bab24d6733c96bc14a00db0d3904c4` |
| `core/presentation/PresentationProfile.gd` | 8837 | `187b1cf8ab96b9031785a0f36b0054a60383c97cb3d81906c7d9bbcd373bef24` |
| `core/validation/PresentationProfileValidator.gd` | 4517 | `486191d276b4dbc62acc1ff43121ddb5eca8a74e0f22e270b5c429694f83ad49` |

## Cadena de evidencia

- Ruta Challenge: `E6ROUTEAUDIT_20261117T125614Z_54A34DBA`, receipt SHA-256 `8deb1c23022ecde3f0b66e7ff07778172adecbd6e6a7f6ec045f6698657b4190`, 24/24 pins, 6/6 definiciones, 18/18 comprobaciones estáticas.
- Runtime dependencies: `E6DEPPINAUDIT_20261117T130110Z_A1CCE574`, receipt SHA-256 `bff36af655abba65aa7ddb2e59c108c57593b6ca19aad586aafe7077b7428f3d`, manifiesto candidato SHA-256 `6f607d0a59202a23673905ea69542c07d1f43b2cf405e379b30257bba281483a`, 24 + 9 = 33/33.
- Instalación handover: `E6HANDOVERINSTALL_20261117T140558Z_FA4BA49C`, receipt SHA-256 `a232a5df421725c9fd710f06f6d2d0e837490e848c4cf06a62e9257bfd29b02d`, 8/8 documentos ADD_ONLY, 33/33 rehash.
- Manifiesto independiente resultante: `C11E_E6_RUNTIME_ROUTE_DEPENDENCY_PIN_SET_V1.json` (33 pins). El JSON no sustituye al manifest C11-C ni a D4.8.

## Próximo gate de ingeniería

Con la identidad de dependencias fijada, el siguiente trabajo será el diseño/implementación del orquestador D9 `PREPARE_ONLY`. Debe reutilizar el servicio E1 y la lógica plan-only ya aceptada; no duplicar Producer, binder, renderer, módulo de suite ni worker multimedia. Debe crear únicamente preparación/recibos estructurados y mantener explícitamente `runtime_authorized=false`.

La ruta de render sigue bloqueada por el alcance D4.8, la ausencia de autorización E6 TEST_ONLY, los workers CH004/CH001 de alcance limitado, los valores E1 `tempo_bpm`/`duration_seconds` no resueltos y los detalles de reutilización aún no cerrados a nivel de artefacto.

## Invariantes

- C11-C 2.19.12 y su manifest `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953` permanecen inmutables.
- D4.8 R1V V2 `0866b53ad4fcdebe74d01f66864b2dfb00eb644ca28dcd59301c8f3208239c07` permanece `BLOCKED_UNCHANGED`.
- E1 `PREPARE_ONLY`; renderer `OFF`; dispatch/media false; `release_authority=NONE`.
- No Git checks; commits bajo gestión del operador; pins SHA-256 obligatorios.
