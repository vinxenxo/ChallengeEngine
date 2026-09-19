# ChallengeEngineV01 — ¿Qué estamos construyendo?

Estamos construyendo una **fábrica automática de vídeos de retos de precisión**: el vídeo ejecuta una situación matemática y el espectador intenta pausar en el frame ganador.

No es un videojuego tradicional. La lógica del reto, la presentación y la producción están separadas para poder generar situaciones repetibles y escalables.

## Familias matemáticas actuales

```text
HIT
CATCH
DODGE / SAVE / CONTROL
FIND
CHOOSE / COUNT (fixtures/pipeline C6)
```

El motor también contiene fixtures de laboratorio como `pilot` y `key`, que sirven para preservar y validar contratos históricos.

## RNG y determinismo

El motor usa RNG sin estado y streams semánticos. Las fixtures históricas mantienen sus contratos de RNG versionados. Los cambios de presentación o temporalidad no pueden alterar la verdad estructural de la simulación.

## C6-F0.3 — Foundation branch

La rama C6-F0.3 establece la frontera común de contenido sin convertir Challenge en un tipo de contenido visual.

```text
C6-F0.3.1  Pre-Implementation Audit       CLOSED
C6-F0.3.2  Schema Boundary                CLOSED / CERTIFIED
C6-F0.3.3  Shared Content Envelope        CLOSED / CERTIFIED
C6-F0.3.4  Temporal Abstraction + CTA     CLOSED / CERTIFIED
C6-F0.3.5  Content Runtime Boundary       IMPLEMENTED / RUNTIME PENDING
```

### Authoring boundary

`ContentEnvelope` acepta únicamente:

```text
visual_loop
visual_drill
```

Challenge conserva sus schemas y orquestación soberanos.

### Temporal boundary

```text
TemporalCore
├── ChallengeTimeline
│   └── VideoTimeline compatibility shim
├── VisualLoopTimeline
└── VisualDrillTimeline
```

La fórmula histórica es:

```text
maxi(0, int(round(duration_seconds * fps)))
```

`VisualLoopTimeline` es el único propietario del wrapping de loop. `VisualDrillTimeline` no define fases.

### Runtime boundary

```text
Domain definition
      ↓
ContentRuntimeRegistry
      ↓
exact (kind, subtype) / fail-closed
      ↓
ChallengeRuntime | VisualLoopRuntime | VisualDrillRuntime
      ↓
RenderedFrameStream
      ↓
Presentation / Rendering
      ↓
Export
```

El runtime común no conoce `SimulationResult`, `WinningFrameDetector`, RNG, `ChallengeMechanic`, `PresentationUI` ni FFmpeg.

## CTA histórico

La extracción temporal provocó una regresión temporalmente acotada en los textos CTA. Los defaults históricos fueron restaurados y la suite específica verificó:

```text
LINK IN BIO
¡Juega ahora!
```

La corrección se considera parte del baseline congelado.

## Producción

La factoría continúa en versión `0.10.0` con contrato de manifest `1.0`. `build_factory.py` sigue siendo orquestación de producción, no el runtime universal.

## Certificación pendiente de F0.3.5

La implementación está presente y ha pasado las comprobaciones estáticas del paquete. La certificación real de Godot/factoría debe ejecutarse en una máquina con el Godot objetivo disponible.

## Documentación viva

La referencia acumulativa de esta rama es:

```text
docs/C6-F0.3_MULTI-CONTENT-TEMPORAL-RUNTIME-FOUNDATION.md
```

La continuidad exacta es:

```text
docs/MASTER_HANDOVER_CHECKPOINT_C6-F0.3.5_IMPLEMENTED_PENDING_EXECUTION.md
```

La regla de desarrollo sigue siendo:

```text
AUDIT → CONTRACT → IMPLEMENTATION → TEST → REGRESSION → BATCH → PHYSICAL ARTIFACT → FREEZE
```
