# C11-D — Índice documental y política de continuidad V2

**Fecha:** 29-10-2026  
**Alcance:** navegación y clasificación de la documentación D; no cambia contratos ni gates.  
**Fuente de la verificación del snapshot:** `C11D_WORKING_CONTEXT_20261029_193950.zip`, commit declarado `be5d04c64080723e5f53d651109e45db07c43054`.

## 1. Para qué sirve este índice

El problema no se resuelve leyendo cientos de documentos en cada ventana ni renombrándolos a ciegas. En el snapshot verificado había **565 archivos en `docs/current/d`**, **35 en `docs/history/c11d`**, **52 en `docs/history/master-prompts/c11d`**, **93 prompts C11-D en `prompts/`** y **37 master/start prompts C11-D en `docs/master-prompts/`**. La mayor parte de `docs/current/d` conserva registros de decisiones, pruebas, resultados y versiones sucesivas que necesitan seguir siendo localizables por su ruta original.

La organización se hace mediante una jerarquía de lectura y un catálogo generado por `tools/c11d/documentation/organize_c11d_documentation.ps1`. **No mueve, renombra ni borra documentos existentes.** Muchos registros contienen rutas, hashes, referencias cruzadas o evidencia inmutable; moverlos sin una migración explícita podría romper trazabilidad y gates.

Al ejecutar el script se crean/actualizan exclusivamente estos dos artefactos generados, y solo si los que ya existen llevan el marcador del propio generador:

- `docs/current/d/C11D_DOCUMENTATION_CATALOG_GENERATED.md`
- `docs/current/d/C11D_DOCUMENTATION_CATALOG_GENERATED.json`

El catálogo clasifica por tema, ubicación y linaje. Una etiqueta de versión/histórico no constituye por sí sola una declaración de supersesión.

## 2. Jerarquía de autoridad

1. **Checkout activo de Windows** `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`, incluido el código, la evidencia local y sus hashes. El snapshot subido es contexto derivado, no sustituye al checkout.
2. `AGENTS.md` y `.continue/rules/CONTINUE.md`.
3. Pins actuales de baseline y continuidad: `release/C11C_FREEZE_PACKAGE_MANIFEST.json`, Ledger V18 y Checkpoint V41. Comprobar los hashes esperados antes de modificar código o interpretar gates.
4. Fase AD ya cerrada técnicamente como validación, junto con su paquete de decisión: `C11D_PHASE_AD_EXECUTION_CLOSEOUT_20261029_V1.md`, `C11D_PHASE_AD_EXECUTION_EVIDENCE_RECEIPT_20261029_V1.json` y `C11D_PHASE_AD_OPERATOR_AUTHORITY_DECISION_GATE_20261029_V1.json`/`.md`.
5. Este índice V2, el plan funcional V2, el mapa de lectura V2 y el catálogo generado: documentación de navegación más reciente, sin alterar las decisiones AD ni sus pins.
6. Contratos D por dependencia real: D9.8 modelo editorial/resolver; D9.9 productor/request-plan; D9.10 bridge y adapter `PREPARE_ONLY`; binder/payload/identidad/semántica; políticas de región, tiempo y presentación; D3 música/audio/mux.
7. Código y manifests reales de `c11c-suite`, `tools/qa/c11/` y `tools/prototypes/c11c_bulk/`. Los scripts de ejecución dicen qué se invoca realmente; un documento no sustituye esa comprobación.
8. `docs/history/c11d/`, `docs/history/master-prompts/c11d/` y prompts antiguos: solo contexto histórico, salvo que un contrato o gate actual los cite expresamente.

## 3. Estado de continuidad que no debe reinterpretarse

- Ledger vigente para esta continuidad: `C11D_ENGINEERING_PHASE_LEDGER_20261029_V18.md`.
- Checkpoint vigente para esta continuidad: `C11D_FULL_CONTEXT_CONTINUITY_CHECKPOINT_20261029_V41.md`.
- Phase AD: 60/60 tests PASS y verificador estructural PASS **solo como validación del paquete de decisión**. La elección de operador sigue `PENDING_EVIDENCE_OR_KEEP_BLOCKED`; evidencias de autoridad presentadas = 0; decisiones adjudicadas = 0; adopción de política = NONE.
- La revisión AC cubrió 107 candidatas dentro del corpus revisado y no encontró autoridad aplicable al primer render bajo renderer D propio. El resultado se limita a ese corpus.
- `renderer=OFF`; media/payload no materializados; candidato no admisible; dominios de seed incompletos; `master_seed=NOT_ADOPTED`; bindings aprobados = 0; D4.8 BLOCKED; D9.10 PREPARE_ONLY; D9.14/D9.16 BLOCKED; D9.17 BLOCKED_NO_GO; D10 BLOCKED_FOR_PROMOTION; aprobación de baseline ausente; `freeze_eligible=false`; `release_authority=NONE`.
- `CHALLENGE_008` y `CHALLENGE_009` conservan el conflicto 11 s declarados frente a 12 s sumados. No se infiere corrección.
- La instrucción de continuar ingeniería hacia un render no es, por sí misma, adopción de una política ni autorización de renderer.

## 4. Orden de lectura de la próxima ventana

1. `AGENTS.md`, `.continue/rules/CONTINUE.md` y este índice.
2. `C11D_SNAPSHOT_VALIDATION_AND_DOCUMENTATION_REORGANIZATION_20261029_V1.md`.
3. `C11D_DOCUMENTATION_CATALOG_GENERATED.md`, una vez ejecutado el organizador.
4. `C11D_FUNCTIONAL_RECOVERY_AND_MEDIA_ACCEPTANCE_PLAN_20261029_V2.md` y `C11D_RENDER_INTEGRATION_READ_ORDER_20261029_V2.md`.
5. Ledger V18, Checkpoint V41 y los tres artefactos AD señalados arriba.
6. Aceptación y comandos de C en `docs/current/c11c/` y los runners reales enumerados en el plan.
7. Módulos D relevantes a la frontera encontrada; no leer todos los D9 ni todos los prompts antiguos en bloque.
8. `prompts/C11D_D_RENDER_INTEGRATION_CONTINUATION_PROMPT_20261029_V1.md` es el prompt de arranque listo para pegar; master/start/overhand V2 definen, respectivamente, invariantes, tarea inicial y entrega de continuidad.

## 5. Clasificación navegable

El catálogo generado agrupa los documentos en categorías funcionales como:

- Continuidad, índice y reglas vigentes.
- Integración de render D: request, editorial, payload/binding, compositor, regiones y timebase.
- Gobierno, decisiones y gates.
- Aceptación, evidencia, receipts, resultados y auditoría.
- Overlays, manifests y empaquetado.
- Historia archivada y referencias versionadas que no deben considerarse obsoletas automáticamente.
- Otros documentos D que requieren consultar el título/contexto.

La categoría es una ayuda de navegación, no una jerarquía de autoridad. Los archivos conservan sus rutas actuales para que los hashes y referencias sigan siendo válidos.

## 6. Política para archivar o reubicar

No mover lotes de `docs/current/d` a `docs/history/d` de forma automática. Primero debe existir un mapa de referencias internas/externas y un plan de migración que:

1. identifique cada destino y ruta fuente exacta;
2. detecte referencias en Markdown, JSON, scripts, prompts y paquetes de overlay;
3. distinga evidencia de decisión, contrato activo, receipt de prueba y propuesta supersedida;
4. conserve fuente original o registre una mudanza verificable con hash antes/después;
5. actualice referencias en una propuesta revisable, nunca en un script de limpieza genérico;
6. pase sus tests y conserve el manifiesto C11-C byte-for-byte.

Hasta entonces, el catálogo es la organización canónica, y los registros históricos siguen inmutables en su ubicación.

## 7. Líneas de producto y criterio de aceptación

- Tres familias: Challenge, Visual Loops y Visual Drills. Longform fuera del scope D actual.
- Smoke de cobertura: 18 productos (9 Challenge, 5 Loops representativos, 4 tipos de Drill).
- Matriz completa del scope: 101 salidas (54 Challenge, 27 gramáticas concretas Loop, 20 variantes Drill tipo/tier). Excluir 008/009 mientras siga el conflicto temporal.
- El render aprobado debe demostrar texto editorial visible en frames, A/V real, determinismo, identidad/provenance y paridad CLI/GUI a través del servicio compartido. Un plan/sidecar o harness de frames no equivale a MP4 aceptado.
- El cambio del baseline C al D solo puede ocurrir después de aceptar todos los gates independientes, cerrar la matriz y aprobar/fijar formalmente el baseline D.

## 8. Pins del baseline

| Fuente | SHA-256 esperado |
|---|---|
| `AGENTS.md` | `0d4565e57b9fe9bba88a88f10babd175f3bb5e3fb437014866ed1e67d3016b37` |
| `.continue/rules/CONTINUE.md` | `52776e55023a36e1ead71cf39a93337ca96f6097bd2c88018c3353484145ac86` |
| `release/C11C_FREEZE_PACKAGE_MANIFEST.json` | `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953` (796,318 bytes) |
| `docs/current/d/C11D_ENGINEERING_PHASE_LEDGER_20261029_V18.md` | `7731b98a79ca3b0cbe42256866bb8c1093389c40d5fe502bbfba7ac038b2ea90` |
| `docs/current/d/C11D_FULL_CONTEXT_CONTINUITY_CHECKPOINT_20261029_V41.md` | `2d2f165872e76f40afa86fbf774500c1a97c5cec3c193e26c9cc46c39f2f5ff4` |
| `docs/current/d/C11D_PHASE_AD_EXECUTION_CLOSEOUT_20261029_V1.md` | `22ed115bb58f9a9c84bb4942cd86af1f6d5a7bd2b72c3981037f209768ee4652` |
| `docs/current/d/C11D_PHASE_AD_EXECUTION_EVIDENCE_RECEIPT_20261029_V1.json` | `800cf33d7e53af989d05d5b8096d11e2909d1c486a6ebc469f025b0ea5bb94f3` |
| `docs/current/d/C11D_PHASE_AD_OPERATOR_AUTHORITY_DECISION_GATE_20261029_V1.json` | `63339254dd444c38a932b8b582bc0af600d309786f46d1e8dd2b92dbf07054e5` |
| `prompts/C11D_D_FINAL_CLOSEOUT_HANDOVER_MASTER_PROMPT_20261029_V41.md` | `e1b26b08ca7782d4aa104ddd813c013448eb32b05de7b74e9c398589d07a79b4` |
| `prompts/C11D_D_FINAL_CLOSEOUT_START_PROMPT_20261029_V41.md` | `816ee5308eb3b51822acea476141061ffa0aabf300c422f698e94b44345cfb6f` |

Si alguno de los tres pins principales (AGENTS, CONTINUE, manifiesto C) difiere, detener los cambios. Los demás hashes son referencias de continuidad y deben reconciliarse con la checkout activa si han avanzado.
