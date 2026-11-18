# C11-E E6 — Challenge PREPARE_ONLY Orchestrator V1

**Hito:** `E6_CHALLENGE_PREPARE_ONLY_ORCHESTRATOR`  
**Estado del paquete:** `BUILT_40_TESTS_PASS_NIGHTLY_FIXTURE_INTEGRATION_PASS_ACTIVE_CHECKOUT_INSTALL_PENDING`  
**Estado funcional permitido:** `PREPARE_ONLY`  
**Fecha:** 2026-11-18

## 1. Propósito y alcance

Añadir un único orquestador D9 bajo `tools/c11d/d9/` para preparar seis grupos Challenge a través del servicio E1 existente y el constructor de envelopes estáticos del E6 plan-only existente. Cada grupo produce tres subpruebas A, B_REPEAT y C_CHANGED_MUSIC_SEED: 18 intents E1 y 18 envelopes D. Son subruns de seis escenarios Challenge, no 18 nuevos escenarios Smoke18.

El orquestador no ejecuta `run_plan()` ni reutiliza `_challenge_request()` del plan V1, porque ambos empaquetan selección y fixtures dentro del módulo. En su lugar, toma la selección, las seeds, la timebase y los parámetros de request de `C11E_E6_CHALLENGE_PREPARE_ONLY_INPUT_MANIFEST_V1.json`.

## 2. Interfaces existentes reutilizadas

- E1: `prepare_c11e_production_intent(raw_request, project_root, request_origin=..., resolver_module=...)`.
- E1: `validate_c11e_production_intent(intent, project_root)`.
- D plan-only: `build_envelope(root, intent, challenge)` y `validate_envelope_static(...)` del módulo `c11e_e6_challenge_plan_only_v1.py`.
- D9.9 resolver cargado por el servicio E1 mediante su `_load_d9_resolver(root)`.

No se reemplaza, modifica ni parchea el servicio E1, el resolver D9.9, el builder plan-only, el schema, las definiciones Challenge, el consumidor GDScript ni `GeneradorMaestro.gd`.

## 3. Inputs explícitos

El manifiesto de entrada contiene, sin defaults de código:

- los seis grupos propuestos y sus IDs de definición;
- el path y SHA-256 de cada definición canónica;
- mechanic, gameplay seed y timebase nativa (FPS, duración, frames);
- tres probes ordenados y la music seed explícita de cada probe;
- modo REVIEW, delivery profile, presentation profile, variation, audio flag, personalization flag, editorial containers y `presentation_options`;
- perfil de música y tempo histórico identificados exclusivamente como metadatos `PROPOSAL_ONLY_NOT_AUTHORIZED`.

El orquestador compara la definición contra su identidad interna, `producer_schema.json`, el SHA esperado y la suma de fases canónica. No completa seeds ausentes, no calcula IDs de selector, no usa defaults musicales y no escribe `tempo_bpm` ni `duration_seconds` en E1. Ambos parámetros permanecen `null` y en `unresolved_engine_parameters`.

La lista de seis selectores mantiene el estado `PROPOSAL_NOT_FROZEN`. La instalación de este orquestador no congela la matriz Smoke18.

## 4. Salidas y evidencia

Cada ejecución genera un directorio único bajo:

`artifacts/tests/c11e/e6_challenge_prepare_only_orchestrator/<RUN_ID>/`

Contiene:

- 18 intents E1 JSON y sus sidecars SHA-256;
- 18 envelopes D JSON y sus sidecars SHA-256;
- copia íntegra del manifiesto de entrada usado y sidecar SHA-256;
- plan resumen y recibo PREPARE_ONLY con sidecars SHA-256;
- pins pre/post de las fuentes y referencias de evidencia upstream.

El RUN_ID identifica una carpeta de evidencia; no es un BatchId. El output root de E1 (`artifacts/production/c11e/<request_id>`) sigue sin crearse.

## 5. Controles negativos

La suite cubre: selector desconocido/no permitido, ID de escenario o path de definición discordante, seed de gameplay ausente, music seed ausente, relación A/B/C incorrecta, orden/variante inválidos, timebase aritmética incorrecta, definición/identidad discordante, envelope con selector incorrecto, rutas absolutas, traversal, separadores inseguros, modo PRODUCTION, editorial override, perfil omitido, music fixture no autorizado, presentación implícita y cualquier flag/campo que intente cruzar PREPARE_ONLY.

## 6. Instalación y ejecución

El instalador usa PowerShell 5.1 nativo y es estrictamente ADD_ONLY. Antes de la primera escritura:

1. Parse AST del instalador y runner.
2. Comprueba Python 3.13.14 por proceso .NET (`python.exe --version`); no usa `python -c`.
3. Valida inventario exacto, rutas, bytes y SHA-256 de todos los payloads extraídos.
4. Ejecuta el validador estático y una única suite de 40 tests del paquete.
5. Revalida el manifiesto congelado C11-C, D4.8 y todos los pins de fuentes/evidencias (23 de checkout + 5 upstream), incluido el modelo de editorial D9.8.
6. Preflight de todos los destinos; acepta solo destino inexistente o bytes idénticos. Colisión diferente aborta antes de copiar.
7. Crea cada archivo nuevo con apertura exclusiva, verifica postimage y emite recibo. No reemplaza ni borra nada existente.

El instalador ejecuta la suite estática de 40 tests una sola vez contra el payload antes de escribir. El runner no repite esos tests: comprueba el recibo de instalación que registra 40/40, los hashes de los payloads instalados, su AST, Python 3.13.14 y los pins de fuentes a través del orquestador; después realiza una sola preparación E1/D. Valida el recibo real, el plan y la copia del manifiesto con sus sidecars SHA-256, sin depender de expresiones regulares sobre stdout para recuperar la ruta del recibo.

Si falla cualquier gate, detenerse y preservar los artefactos. No repetir automáticamente, limpiar ni reparar evidencias históricas.

## 7. Gobernanza

- E1 `PREPARE_ONLY`.
- D4.8 `BLOCKED`, sin override.
- E6 media authorization `FALSE`.
- renderer OFF; production dispatch/media false.
- sin Godot, FFmpeg, FFprobe, D3 audio, PCM, mux, BatchId o comandos de runtime.
- `E6_ACCEPTED=0`; matriz no congelada.
- `release_authority=NONE`.
- C11-C 2.19.12 y manifest congelado inmutables.
- `GIT_CHECKS=SKIPPED`; commits gestionados por el operador; source pins exigidos.

Un recibo PASS de este overlay demuestra exclusivamente la preparación E1 y los envelopes D estáticos. No demuestra runtime Godot, D-composición, A/V ni elegibilidad de promoción.

## 8. Validación de integración del paquete

La suite de regresión del paquete pasó 40/40. Además, se ejecutó una integración de extremo a extremo en una fixture aislada montada desde el nightly snapshot: el servicio E1 real generó 18 intents y el builder D plan-only existente generó 18 envelopes para seis definiciones. Se verificaron el recibo, el plan y sus sidecars, así como la copia pinneada del manifiesto.

Limitación de la fixture: el snapshot nightly no contiene el recibo de requalification generado por el operador a las 14:12. Para esta prueba aislada se usó un recibo sintético local con el contrato de campos informado por el operador y se recalculó únicamente el pin de la fixture. Esos datos sintéticos no están incluidos en el paquete. En el checkout real se exige el recibo original con SHA-256 `4d63b8caec7a975cc0362ee9d7a5924f5ab8371e8e8e1457e1d60956bf65ce33`. La ejecución del parser AST nativo de Windows PowerShell 5.1 sigue siendo una barrera local obligatoria del instalador y runner; no se declara PASS aquí.
