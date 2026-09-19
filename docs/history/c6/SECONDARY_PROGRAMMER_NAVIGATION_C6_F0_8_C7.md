# ChallengeEngineV01_STATELESS — Guía de Navegación para Programador Secundario
## Baseline: C6-F0.8-F2/F3 → C7-A0.1-F1

**Estado:** guía operativa de navegación y nomenclatura  
**Baseline físico:** `ChallengeEngineV01.2-C6-LATEST.zip`  
**Checkpoint congelado de partida:** `C6-F0.8-F2/F3`  
**Checkpoint activo:** `C7-A0.1-F1 — Procedural Audio Foundation & Deterministic Stream Integration`

> Esta guía existe para que un programador secundario pueda localizar correctamente código, documentación, perfiles, definiciones y tests sin confundir infraestructura histórica, authoring, runtime, presentación o artefactos de producción.

---

# 1. REGLA DE AUTORIDAD

No utilizar nombres de versión de archivos como prueba de cronología.

La autoridad se interpreta así:

1. **ZIP baseline real**: `ChallengeEngineV01.2-C6-LATEST.zip`.
2. **Master Handover del checkpoint activo**: C6-F0.8-F2/F3.
3. **Código ejecutable actual** de la ruta que se vaya a modificar.
4. **Documentación marcada como current/live**.
5. **Tests y contratos automatizados**.
6. Documentación histórica únicamente para entender decisiones anteriores.

Un archivo con `1.1.0`, `C6-D4`, `F4.4`, etc. no sustituye al baseline simplemente por tener un número mayor.

---

# 2. IDENTIDAD DEL PRODUCTO

`ChallengeEngineV01_STATELESS` es una fábrica determinista de contenido audiovisual para redes sociales.

No es un videojuego interactivo en runtime.

El espectador está fuera del motor:

```text
Challenge / Visual Content
        ↓
Deterministic generation
        ↓
Presentation
        ↓
Movie Maker / export
        ↓
Reel / Short / TikTok
        ↓
Viewer
```

En un Pause Challenge, el espectador intenta pausar el vídeo en el frame ganador usando la plataforma. El motor no captura ese input del espectador.

**No introducir `InteractionEvent`, `IInputMapper`, replay del input físico ni control de gameplay del usuario salvo que un futuro checkpoint cambie explícitamente el producto.**

---

# 3. CAPAS PRINCIPALES

```text
Capa 0 — Declarativa / Authoring
        JSON, perfiles, schema, migración

Capa 1 — Simulación determinista
        Mecánicas, RNG estructural, SimulationResult

Capa 2 — Presentación
        Bindings, RenderedFrameStream, renderers, Movie Maker

Capa 3 — Producción
        Python, FFmpeg, FFprobe, manifests, artefactos

Capa audiovisual C7
        Audio semántico y determinista → futura salida física
```

La adición de Audio no debe convertir Presentación en autoridad de la simulación ni introducir input del espectador en el motor.

---

# 4. MAPA DEL ÁRBOL ACTUAL

## Raíz

| Ruta | Responsabilidad |
|---|---|
| `project.godot` | Configuración del proyecto Godot |
| `Main.tscn` | Escena principal |
| `GeneradorMaestro.gd` | Composition Root / flujo principal histórico-live |
| `build_factory.py` | Orquestador de producción |
| `run_batch_export.py` | Batch export |
| `audit_export_pipeline.py` | Auditoría de pipeline |
| `challenge_schema.json` | Schema declarativo C6-F |
| `MASTER_HANDOVER_C6_F0_8_FROZEN.md` | Handover del baseline congelado |
| `START_PROMPT_C6_F0_8_CONTINUATION.md` | Continuidad del checkpoint |
| `AGENTS.md` | Guía histórica; está marcada como desactualizada |

### Importante sobre `AGENTS.md`

`AGENTS.md` **no es la autoridad de continuidad actual**. Contiene reglas útiles de navegación, pero declara explícitamente que está desactualizada. Esta guía complementa y actualiza la navegación para C6-F0.8/C7.

---

# 5. `core/` — NÚCLEO DEL MOTOR

## `core/authoring/`

Responsabilidad: **authoring, validación, migración y registries declarativos**.

Ejemplos:

```text
AssetFamilyRegistry.gd
AssetFamilyValidator.gd
AudioProfileRegistry.gd
AudioProfileValidator.gd
AuthoringMechanicRegistry.gd
ChallengeMigrationAdapter.gd
ContentEnvelope.gd
DifficultyProfileRegistry.gd
PresentationBindingValidator.gd
VideoProfileRegistry.gd
```

### Audio ya existente aquí

`core/authoring/AudioProfileRegistry.gd` y `core/authoring/AudioProfileValidator.gd` **ya existen en el baseline**.

No significan que C7 Procedural Audio Runtime ya exista.

Su función actual es cargar/validar **perfiles declarativos de authoring**.

No convertirlos silenciosamente en:

- `AudioRuntime`
- `AudioRNGContext`
- generadores DSP
- runtime de reproducción

C7 debe mantener la frontera authoring/runtime.

---

## `core/data/`

Modelos de datos compartidos.

Ejemplo actual:

```text
FrameSnapshot.gd
```

Las clases de datos puras siguen el patrón `RefCounted` y tipado estático.

---

## `core/deterministic/`

Base de determinismo y RNG.

```text
DeterministicLCG.gd
RNGStreamDefinition.gd
RNGStreamRegistry.gd
StructuralRNG.gd
CosmeticRNG.gd
MechanicRNGContext.gd
PresentationRNGContext.gd
```

### Regla fundamental

Toda nueva fuente de aleatoriedad debe tener:

```text
stream registrado
+ dominio propietario
+ consumidor autorizado
+ semántica de consumo explícita
```

No introducir RNG globales.

### C7 Audio

`AudioRNGContext` es específico del dominio Audio. Su implementación puede reutilizar la infraestructura determinista existente, pero no debe duplicar una segunda implementación del LCG ni apropiarse de streams visuales/simulación.

La derivación de seeds debe apoyarse en el mecanismo determinista real existente en el baseline, no en `hash()` nativo como contrato de portabilidad.

---

## `core/execution/`

Flujos de ejecución / Canonical V2.

```text
ChallengeExecutionPipeline.gd
ChallengeLegacyRuntimeOracle.gd
ChallengeRuntimeBridge.gd
ChallengeRuntimeContext.gd
ChallengeTimelineBuilder.gd
```

Modificar aquí puede afectar a mecánicas, authoring y ejecución efectiva. Revisar callers y tests antes de tocarlo.

---

# 6. `core/mechanics/` — MECÁNICAS

Árbol actual:

```text
core/mechanics/
├── ChallengeMechanic.gd
├── MechanicRegistry.gd
├── catch/
├── choose/
├── count/
├── find/
├── hit/
├── key/
├── parking/
└── pilot/
```

Familias actuales:

`key`, `parking`, `pilot`, `hit`, `catch`, `find`, `choose`, `count`.

### Regla

Una nueva mecánica es una **familia matemática determinista**, no una interacción física del espectador.

Debe seguir:

```text
AUDIT
→ CONTRACT
→ ISOLATION
→ INTEGRATION
→ REGRESSION
→ BATCH
→ FREEZE
```

---

# 7. `core/presentation/`

Responsabilidad: representación pasiva.

```text
ChallengePresentationBinder.gd
CoordinateMapper.gd
PresentationBinderRegistry.gd
PresentationBindingResult.gd
PresentationProfile.gd
PresentationTheme.gd
PresentationUI.gd
ReferenceFrameResolver.gd
VisualDrillPresentationBinder.gd
VisualLoopPresentationBinder.gd
```

## `core/presentation/components/`

Componentes visuales:

```text
CountdownComponent.gd
CTAComponent.gd
HookComponent.gd
RevealManager.gd
SafeAreaLayout.gd
TypographyLabel.gd
WinningHighlightComponent.gd
```

## `core/presentation/rendering/`

Hosts y renderers pasivos:

```text
ContentRendererHost.gd
VisualContentPlayer.gd
VisualLoopRenderer.gd
VisualDrillRenderer.gd
FractalRenderer.gd
GeometricRenderer.gd
KaleidoscopeRenderer.gd
ParticleFlowRenderer.gd
VectorFieldRenderer.gd
TrackingRenderer.gd
PursuitRenderer.gd
SaccadeRenderer.gd
PeripheralScanRenderer.gd
```

### Regla congelada

Los renderers:

- no calculan mecánicas;
- no llaman generadores;
- no consumen RNG;
- no avanzan el tiempo semántico;
- no deciden qué ocurrió;
- no utilizan `payload.domain` como router.

El routing autorizado es:

```text
RenderedFrameStream(kind, subtype)
```

---

# 8. `core/runtime/` — RUNTIMES DE CONTENIDO

```text
ChallengeRuntime.gd
ContentRuntime.gd
ContentRuntimeRegistry.gd
RenderedFrameStream.gd
VisualDrillRuntime.gd
VisualLoopRuntime.gd
```

Subdominios:

```text
core/runtime/visual/
core/runtime/visual_drill/
```

## Visual Loop

Generadores:

```text
FractalGenerator.gd
GeometricGenerator.gd
KaleidoscopeGenerator.gd
ParticleFlowGenerator.gd
VectorFieldGenerator.gd
```

Streams congelados: `2001–2005`.

## Visual Drill

Generadores:

```text
PeripheralScanGenerator.gd
PursuitGenerator.gd
SaccadeGenerator.gd
TrackingGenerator.gd
```

Streams congelados: `2011–2014`.

**No tocar estos streams para Audio.**

---

# 9. `core/simulation/`

```text
SimulationMetricsResolver.gd
SimulationResult.gd
```

Aquí vive la salida semántica de la simulación.

`SimulationResult` es contrato interno público.

Audio debe consumir hechos derivados del estado semántico, pero **no alterar `SimulationResult`**.

---

# 10. `core/timeline/`

```text
VideoTimeline.gd
```

Fuente efectiva de temporalidad en Godot.

Fases:

```text
HOOK → GAME → REVEAL → CTA
```

`winning_frame` de simulación es relativo a GAME. El frame absoluto se deriva con `hook_frames`.

Audio debe respetar esta temporalidad; no inventar su propio reloj de gameplay.

---

# 11. `core/validation/`

Validadores y contratos:

```text
C6FChallengeSchemaValidator.gd
ChallengeDefinitionValidator.gd
ChallengeValidator.gd
ContentSchemaValidator.gd
FamilyAssets.gd
PresentationProfileValidator.gd
ValidationResult.gd
WinningFrameDetector.gd
```

Regla: validar primero, ejecutar después.

No convertir un problema de Audio en una modificación de estos validadores salvo que el contrato de authoring cambie explícitamente.

---

# 12. `challenges/`

Definiciones de challenges históricos/actuales:

```text
CHALLENGE_001.json ... CHALLENGE_009.json
```

No confundir con `definitions/`.

- `challenges/` = corpus de challenges.
- `definitions/` = corpus canónico de Visual Content.

---

# 13. `definitions/` — VISUAL CONTENT CANÓNICO

Exactamente nueve definiciones certificadas:

```text
visual_loop_fractal_canonical.json
visual_loop_vector_field_canonical.json
visual_loop_particle_flow_canonical.json
visual_loop_kaleidoscope_canonical.json
visual_loop_geometric_canonical.json

visual_drill_tracking_canonical.json
visual_drill_pursuit_canonical.json
visual_drill_saccade_canonical.json
visual_drill_peripheral_scan_canonical.json
```

Este conjunto está congelado por C6-F0.8.

No añadir Audio a estas definiciones por conveniencia sin contrato C7 explícito.

---

# 14. `profiles/`

Separación actual:

```text
profiles/assets/
profiles/audio/
profiles/difficulty/
profiles/video/
```

## `profiles/audio/`

Perfiles declarativos actualmente existentes:

```text
default_asset_music.json
default_procedural_music.json
fake_identity.json
```

Estos son **authoring data** consumidos por `AudioProfileRegistry`/`AudioProfileValidator`.

No confundir:

```text
profiles/audio/*.json
```

con la futura clase runtime:

```text
AudioProfile.gd
```

El primero es configuración declarativa; el segundo sería un modelo tipado runtime del nuevo subsistema C7.

---

# 15. C7 — DÓNDE DEBE CRECER PROCEDURAL AUDIO

El baseline **no contiene todavía `core/audio/`**.

Para C7-A0.1-F1, la ubicación prevista del nuevo dominio es:

```text
core/audio/
```

con una estructura inicial mínima:

```text
core/audio/
├── AudioRNGContext.gd
├── AudioEvent.gd
├── AudioProfile.gd
├── AudioGenerationResult.gd
└── generators/
    └── ToneBurstGenerator.gd
```

Esta ruta es una extensión nueva del dominio C7; no debe reutilizar `core/authoring/` como cajón de runtime.

### Futuras piezas posibles, todavía fuera de F1

```text
core/audio/AudioEventStream.gd
core/audio/AudioRuntime.gd
core/audio/AudioProfileResolver.gd
```

Solo crear cuando el contrato correspondiente haya sido aprobado.

---

# 16. C7 — TESTS

Los tests actuales viven principalmente en `tests/`, con subdirectorios por dominio cuando existe una familia suficientemente grande.

Para C7 se recomienda:

```text
tests/audio/
```

Ejemplos de nomenclatura futura:

```text
C7A01AudioRNGContextTest.gd
C7A01AudioEventContractTest.gd
C7A01AudioProfileContractTest.gd
C7A01ToneBurstGeneratorTest.gd
```

Cada nuevo `*Test.gd` debe registrarse en:

```text
tests/run_all.py
```

y debe emitir exactamente el marcador PASS esperado por el runner.

No dejar tests ejecutables pero no registrados.

---

# 17. `tests/` — MAPA MENTAL

Hay tres grandes familias de pruebas:

### C6-E / Presentation

```text
C6E*
```

### C6-F / Visual Content

```text
C6F0*
C6F08*
C6F2*
C6F3*
C6F4*
```

### RNG / Core

```text
RNGArchitectureTest.gd
DeterministicLCGStatelessTest.gd
```

No modificar estos tests para acomodar C7. Añadir suites C7 independientes, salvo una dependencia contractual demostrable.

---

# 18. DOCUMENTACIÓN — QUÉ LEER Y CUÁNDO

## Primero para continuidad

```text
MASTER_HANDOVER_C6_F0_8_FROZEN.md
START_PROMPT_C6_F0_8_CONTINUATION.md
```

## Arquitectura general

```text
docs/ARCHITECTURE_V0.1.md
docs/DATA_MODEL_V0.1.md
docs/DOMAIN_MODEL_V0.1.md
docs/GOVERNANCE.md
```

## Contratos de contenido

```text
docs/CONTENT_SCHEMA_V0.1.md
docs/VIDEO_SPECIFICATION.md
docs/DISTRIBUTION_SPEC_V0.1.md
docs/PRODUCTION_PROVENANCE_CONTRACT_V1.0.md
```

## Testing / validación

```text
docs/TESTING_STRATEGY_V0.1.md
docs/VALIDATION_PROTOCOL.md
```

## Roadmap

```text
docs/ROADMAP_PHASES.md
```

### Documentos históricos

Todo documento con nombres como:

```text
MASTER_HANDOVER_CHECKPOINT_0.x
MASTER_HANDOVER_CHECKPOINT_1.0.0
MASTER_HANDOVER_CHECKPOINT_1.1.0-C6-D4
C6-D4_*
C6-F4.*
```

puede contener decisiones importantes, pero **no debe interpretarse automáticamente como estado actual**.

Nunca sustituir el baseline actual por una conclusión obtenida solo del nombre de un documento histórico.

---

# 19. PRODUCCIÓN Y ARTEFACTOS

## `scripts/`

Scripts de aplicación de patches, auditorías, validadores auxiliares y herramientas históricas.

No ejecutar/aplicar un patch histórico como si fuera parte del workflow normal sin identificar primero su propósito y target.

## `output/`

Artefactos por challenge:

```text
output/CHALLENGE_XXX/
```

Contiene AVI, MP4, GIF y manifest cuando están presentes.

## `output_batch_audit/`

Evidencia física de las pruebas de determinismo visual, además de artefactos auxiliares como `pilot.avi` y `smoke.avi`.

Los archivos de `output/` y `output_batch_audit/` no son código fuente.

## `__pycache__/` y `tests/__pycache__/`

Artefactos de Python. No son parte de la arquitectura.

---

# 20. REGLAS DE NOMENCLATURA

## GDScript

Clases / archivos:

```text
PascalCase.gd
```

Ejemplo:

```text
AudioRNGContext.gd
ToneBurstGenerator.gd
```

Funciones y variables:

```text
snake_case
```

Constantes:

```text
UPPER_SNAKE_CASE
```

## JSON

Perfiles y definiciones usan identificadores `snake_case` cuando forman parte del contrato declarativo.

## Tests

```text
<Checkpoint><Domain><Purpose>Test.gd
```

Ejemplo:

```text
C7A01AudioRNGContextTest.gd
```

## Checkpoints

El checkpoint es una identidad de trabajo, no una prueba de cronología global.

Ejemplo actual:

```text
C7-A0.1-F1
```

---

# 21. C7-A0.1-F1 — ALCANCE ACTUAL

El objetivo actual es **fundación semántica y determinista de Audio Procedural**.

Dentro de F1:

```text
AudioRNGContext
AudioEvent
AudioProfile
AudioGenerationResult
ToneBurstGenerator
Determinism / isolation tests
```

Fuera de F1:

```text
PCM
Godot AudioStream
AudioServer
mezcla física
threads de audio
callbacks realtime
backend nativo
DSP complejo
reproducción final
Movie Maker audio export
```

### Principio

```text
AudioGenerationResult
```

es un **plan acústico determinista**, no un buffer PCM.

---

# 22. REGLAS DE AUDIO CONGELADAS PARA F1

### Audio no recibe input del espectador

No existe interacción runtime del usuario en este producto.

### Audio no modifica simulación

Debe cumplirse:

```text
SimulationResult antes de Audio
==
SimulationResult después de Audio
```

### Audio RNG está aislado

```text
Simulation RNG
≠ Visual / Cosmetic RNG
≠ Audio RNG
```

### El evento no sabe cómo suena

`AudioEvent` expresa:

```text
qué ocurrió + cuándo ocurrió
```

No contiene lógica del generador.

### El perfil no sabe por qué fue invocado

`AudioProfile` expresa:

```text
cómo debe configurarse el generador
```

No contiene conocimiento de mecánicas concretas.

### El generador no emite PCM en F1

Produce `AudioGenerationResult`.

---

# 23. WORKFLOW OBLIGATORIO PARA EL SEGUNDO PROGRAMADOR

Antes de editar:

```text
1. Identificar checkpoint.
2. Identificar ruta exacta afectada.
3. Leer contrato correspondiente.
4. Leer el test más cercano.
5. Confirmar si la pieza pertenece a authoring, simulation, runtime, presentation o production.
6. No reutilizar un nombre existente con otra semántica.
```

Después:

```text
CONTRACT
→ IMPLEMENTATION
→ FOCUSED TEST
→ REGISTER TEST
→ FULL RELEVANT SUITE
→ EVIDENCE
→ FREEZE
```

No hacer:

```text
refactor global
renombrado masivo
migración de carpetas por estética
reutilización de clases con semántica diferente
modificación de C6-F0.8 para facilitar C7
```

---

# 24. ERRORES CONCRETOS QUE DEBEN EVITARSE

## Error 1 — Confundir Audio Authoring con Audio Runtime

Incorrecto:

```text
core/authoring/AudioProfileRegistry.gd
→ convertirlo en AudioRuntime
```

Correcto:

```text
core/authoring/
    declarative profiles

core/audio/
    C7 semantic runtime
```

## Error 2 — Crear input del espectador

Incorrecto:

```text
InteractionEvent
IInputMapper
ACTION_TAP
```

No pertenecen al producto actual.

## Error 3 — Meter Audio dentro de Presentation

Incorrecto:

```text
renderer -> genera sonido
```

Correcto:

```text
semantic engine state
        ↓
Audio event
        ↓
Audio runtime
```

## Error 4 — Reutilizar RNG visual

Nunca utilizar `2001–2005` o `2011–2014` para Audio.

## Error 5 — Tratar `hash()` nativo como contrato de seed derivation

La derivación debe utilizar una primitive determinista explícita y estable del core.

## Error 6 — Convertir `AudioGenerationResult` en PCM demasiado pronto

F1 es semántico.

---

# 25. CHECKPOINT ACTUAL DE NAVEGACIÓN

```text
C6-F0.8-F2/F3
    ↓
FROZEN / CLOSED / CERTIFIED
    ↓
C7-A0.1-F1
    ↓
Procedural Audio Foundation
```

El trabajo C6-F0.8 queda cerrado salvo evidencia explícita de defecto.

La siguiente implementación pertenece al dominio:

```text
core/audio/
```

y sus tests a:

```text
tests/audio/
```

La infraestructura C6 existente de perfiles de audio permanece en:

```text
core/authoring/AudioProfileRegistry.gd
core/authoring/AudioProfileValidator.gd
profiles/audio/*.json
```

y debe mantenerse conceptualmente separada.

---

# 26. REGLA FINAL

Cuando exista duda entre dos rutas, no improvisar.

Responder primero:

```text
¿Esto es declarativo?
¿Esto es simulación?
¿Esto es runtime?
¿Esto es presentación?
¿Esto es producción?
¿Esto pertenece al nuevo dominio Audio?
```

Después localizar la ruta correspondiente.

**Nunca usar una carpeta solo porque contiene una clase con un nombre parecido.**

**El nombre no define la capa; el contrato y los callers reales definen la capa.**
