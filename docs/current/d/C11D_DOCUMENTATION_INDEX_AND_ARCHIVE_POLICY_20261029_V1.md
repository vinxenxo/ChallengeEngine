# C11-D — Índice documental, jerarquía de autoridad y política de archivo V1

**Fecha:** 2026-10-29  
**Finalidad:** reducir la dispersión de documentación y devolver el trabajo a la integración funcional de producción D.  
**Naturaleza:** índice y regla de continuidad; no altera contratos ni concede autoridad de producción, release, freeze o promoción.

## 1. Regla de oro: checkout activo y evidencia, no el ZIP más reciente

El único árbol operativo de referencia es `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`. Los ZIP de contexto son exportaciones derivadas. Pueden contener archivos duplicados (incluido históricamente `release/C11C_FREEZE_PACKAGE_MANIFEST.json`) y no prueban que su contenido sea idéntico al checkout.

La copia histórica `ChallengeEngineV01_STATELESS_C11-D10_latest_FROZEN_20261028_163525.zip` tiene 3.494 entradas y 3.493 nombres únicos; contiene dos entradas con el nombre `release/C11C_FREEZE_PACKAGE_MANIFEST.json`. **No extraerla completa sobre el checkout ni usar sus conteos/hashes como verdad actual.**

Pins vigentes que este overlay espera encontrar, instalados/cerrados en la última continuidad proporcionada:

| Fuente | SHA-256 esperado |
|---|---|
| `AGENTS.md` | `0d4565e57b9fe9bba88a88f10babd175f3bb5e3fb437014866ed1e67d3016b37` |
| `.continue/rules/CONTINUE.md` | `52776e55023a36e1ead71cf39a93337ca96f6097bd2c88018c3353484145ac86` |
| `release/C11C_FREEZE_PACKAGE_MANIFEST.json` | `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953` (796.318 bytes) |
| `docs/current/d/C11D_ENGINEERING_PHASE_LEDGER_20261029_V18.md` | `7731b98a79ca3b0cbe42256866bb8c1093389c40d5fe502bbfba7ac038b2ea90` |
| `docs/current/d/C11D_FULL_CONTEXT_CONTINUITY_CHECKPOINT_20261029_V41.md` | `2d2f165872e76f40afa86fbf774500c1a97c5cec3c193e26c9cc46c39f2f5ff4` |
| `prompts/C11D_D_FINAL_CLOSEOUT_HANDOVER_MASTER_PROMPT_20261029_V41.md` | `e1b26b08ca7782d4aa104ddd813c013448eb32b05de7b74e9c398589d07a79b4` |
| `prompts/C11D_D_FINAL_CLOSEOUT_START_PROMPT_20261029_V41.md` | `816ee5308eb3b51822acea476141061ffa0aabf300c422f698e94b44345cfb6f` |

Si cualquiera de estos pins no coincide, detener la aplicación del overlay e inspeccionar el checkout. No recuperar ni sobrescribir el archivo desde un snapshot.

## 2. Jerarquía de lectura

Leer en este orden al empezar una ventana de ingeniería:

1. `AGENTS.md` y `.continue/rules/CONTINUE.md` — límites del repositorio y forma de operar.
2. Este índice — qué documento es vigente, histórico o solo evidencia.
3. `docs/current/d/C11D_FUNCTIONAL_RECOVERY_AND_MEDIA_ACCEPTANCE_PLAN_20261029_V1.md` — plan funcional activo hacia vídeos físicos y cutover a D.
4. `docs/current/d/C11D_FULL_CONTEXT_CONTINUITY_CHECKPOINT_20261029_V41.md` y `docs/current/d/C11D_ENGINEERING_PHASE_LEDGER_20261029_V18.md` — estado/pins y decisiones ya registradas.
5. `docs/current/d/C11D_PHASE_AD_EXECUTION_CLOSEOUT_20261029_V1.md` y `docs/current/d/C11D_PHASE_AD_OPERATOR_AUTHORITY_DECISION_GATE_20261029_V1.json` más su Markdown — estado y alcance del gate AD existente.
6. `docs/current/c11c/` — aceptación congelada del baseline C, generadores, corpus y criterios de vídeo.
7. Contratos técnicos D relevantes, por esta prioridad: `D9.8` Universal Editorial Model; `D9.9` Producer/request-plan; `D9.10` adapter/bridge; D3 audio/music; renderer request/payload/I/O; editorial field-consumption; region/temporal/timebase; D9.14 runbook; D9.16/D9.17 and D10 candidate evaluation.
8. El código/manifest vivo de `c11c-suite` y `tools/qa/c11/` — la implementación actual y los launchers son autoridad para conocer cómo se ejecutan las pruebas.

No leer todos los prompts antiguos en cada ventana. El master prompt define las reglas duraderas; el start/initial prompt define la tarea; el overhand prompt define cómo entregar la continuidad siguiente. Abrir un documento histórico concreto solo cuando sea necesario entender la decisión o el resultado al que apunta el índice.

## 3. Clasificación documental

### A. Fuentes operativas vigentes

- `AGENTS.md`, `.continue/rules/CONTINUE.md`.
- Ledger V18 y checkpoint V41 de 2026-10-29, tras verificar sus hashes en el checkout.
- `C11D_PHASE_AD_EXECUTION_CLOSEOUT_20261029_V1.md` y su recibo de ejecución.
- Este índice y el plan de recuperación funcional agregados por el overlay.
- `tools/c11d/packaging/New-C11DWorkingSnapshot.ps1`: entrada simplificada para generar un snapshot ZIP del checkout activo en un único comando; no crea release ni freeze.
- Contratos y código cuyas identidades se verifiquen en el checkout activo.

El ledger/checkpoint son fuentes de estado y trazabilidad; no convierten una propuesta en política aprobada.

### B. Baseline C — referencia protegida y patrón de aceptación

- `release/C11C_FREEZE_PACKAGE_MANIFEST.json`: fuente canónica, bytes inmutables.
- `docs/current/c11c/C11-C_2.19.12_ACCEPTANCE_EVIDENCE.md`.
- `docs/current/c11c/C11-C_2.19_CONSOLIDATED_ACCEPTANCE_GATE.md` y documentos de cierre/freeze relacionados.
- `c11c-suite/self_test.py`, `tests/run_all.py`, `tools/qa/c11/run_c11c_challenge_bulk_qa.ps1`, `tools/qa/c11/run_c11c_complete_video_review.ps1`, los respectivos launchers de Test y el corpus de aceptación.

La aceptación C es referencia de cobertura y de conducta de producción. No significa que el renderer protegido C deba modificarse para implementar D.

### C. Contratos funcionales D vigentes o relevantes

- D9.8: `definitions/c11d/personalization/C11D_UNIVERSAL_EDITORIAL_MODEL_V1.json` y `tools/c11d/d9/universal_editorial_model.py`.
- D9.9: el Producer universal, solicitudes/planes canónicos y paridad GUI/CLI.
- D9.10: `D9.10_EDITORIAL_TO_RENDER_BRIDGE_PLANNING_CHECKPOINT.md` y el adaptador D-only. Su sobre sigue siendo `PREPARE_ONLY`; **no** es un dispatcher de vídeo.
- Música/semillas: D3 Music Engine V5, política audio/música y separación de `request.seed` frente a `request.music_seed`.
- Renderer: `D_RENDERER_BASELINE_PREPARATION_PLAN_V1.md`, candidate I/O/identity, request-scoped payload/materialization/binding, renderer-neutral frame program, composition, temporal/timebase y contratos de editorial/visibilidad.
- `D_RENDERER_EDITORIAL_FIELD_CONSUMPTION_AUDIT_CHECKPOINT_V1.md` y `D_RENDERER_REQUEST_PAYLOAD_INSTANCE_INTEGRATION_CHECKPOINT_V2_2.md` para entender con precisión que una cadena editorial/sidecar válida no es lo mismo que consumo de texto por el payload visual.
- `D9.14_PRODUCTION_QUALIFICATION_RUNBOOK_V1.md` para el alcance del smoke audiovisual histórico y sus límites.

Antes de modificar/crear un componente, buscar si ya existe un contrato, binder, adaptador o servicio compartido. No duplicar el binder universal ni el modelo editorial.

### D. Documentación histórica — mantener, no reescribir masivamente

- `docs/history/c11d/`, `docs/history/c11c/`, antiguos `prompts/C11D_*`, anteriores checkpoints D9/D10 y los paquetes de fases X–AD son evidencia histórica, resultados de fases concretas o prompts supersedidos.
- Las secciones `CURRENT`, `NEXT`, `PENDING` o `BLOCKED` incrustadas en documentos antiguos describen su fecha, no necesariamente el estado actual.
- Los paquetes X–AD centrados en búsqueda de autoridad documentan esa investigación; no deben convertirse en el objetivo funcional permanente del proyecto.

No mover ni renombrar de golpe estos documentos: tests, pins, manifest y enlaces pueden referenciarlos. Primero se indexan. Cualquier traslado futuro será un cambio independiente, auditado y de bajo riesgo.

### E. Retirado / no reactivar

- No crear `c11d-control`, `c11c-studio` ni una sexta superficie operativa.
- No usar archivos ZIP históricos como árbol activo ni extraerlos sobre el checkout.
- No transformar un `PASS` de contrato/preflight en un `PASS` de vídeo físico, aprobación de renderer, freeze o release.

## 4. Estado funcional D sin ambigüedad

| Área | Lo demostrado | Lo que NO se ha demostrado aún |
|---|---|---|
| D9.8 editorial | Modelo/resolver y contratos de valores editables | El vídeo final consume todos los campos de forma visible |
| D9.9 solicitud/plan | Planes canónicos y paridad GUI/CLI en el alcance validado | Que el plan se convierta en salida de vídeo D |
| D9.10 bridge | Sobre/adapter de preparación y paridad de registros | Dispatch final, render de todos los tipos, salida MP4 D |
| Request/payload | Joins/sidecar y bindings/preview de solicitud | Admisibilidad general del candidato o consumo editorial visual |
| Audio/música | Motor y rutas históricas A/V acotadas; semillas separadas en los tests correspondientes | Cobertura end-to-end de todas las variantes D |
| Renderer D | Diseño, programas neutrales, composición y propuestas | El inventario histórico declara implementación física del renderer D como no implementada |
| CLI/GUI | Facades, planes y pruebas de contrato/runtime acotadas | El flujo final de generación D completo, observable y equivalente |

La auditoría de 2026-10-11 registró revisión editorial 14/14 pero consumo visual 0/14; el registro V2.2 de 2026-10-27 conserva el mismo 0/14. Esas cifras son la línea base de la brecha, no resultados de un render nuevo.

## 5. Política para ordenar/archivar sin romper integridad

1. Añadir primero índice y referencias cruzadas; no reescribir documentos pinneados ni crear otro `README.md` que colisione.
2. Mantener `docs/current/c11c/` como evidencia C histórica protegida, aunque el futuro Productor por defecto pueda pasar a D tras aceptación formal.
3. Mantener una sola línea de prompts activos para el nuevo trabajo de render D: `MASTER_PROMPT`, `START_PROMPT`, `INITIAL_PROMPT` y `OVERHAND_PROMPT` agregados por este overlay.
4. No borrar ni regenerar checkpoints, recibos, archivos de tests, manifest, freeze ZIP ni historia de fases X–AD como parte de una limpieza documental.
5. Cada futura limpieza/movimiento físico necesita lista exacta de rutas, precondiciones de hash, audit de referencias, tests de layout y overlay independiente.

## 6. Próximo objetivo

El siguiente trabajo se mide por un **vídeo físico producido por la ruta D**, usando la mecánica/generador C conservado y las capas de presentación, editorial y música integradas por D; luego por cobertura de todas las familias, CLI/GUI y cutover. No se iniciará otra fase de preparación documental genérica como sustituto del cambio funcional.
