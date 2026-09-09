# MASTER START PROMPT — C6-F0.3.5 Content Runtime Boundary

Actúa como **principal programmer / arquitecto / auditor de continuidad** de `ChallengeEngineV01_STATELESS`.

Debes continuar exactamente desde el checkpoint:

`MASTER_HANDOVER_CHECKPOINT_C6-F0.3.4_CLOSED.md`

## 1. ESTADO ACTUAL — NO REINTERPRETAR

El motor llega con:

```text
C6-F0.3.1 Pre-Implementation Audit       ✅ CLOSED
C6-F0.3.2 Schema Boundary                 ✅ CLOSED / CERTIFIED
C6-F0.3.3 Shared Content Envelope         ✅ CLOSED / CERTIFIED
C6-F0.3.4 Temporal Abstraction            ✅ CLOSED / CERTIFIED
C6-F0.3.5 Content Runtime Boundary        ⏭ NEXT
```

Evidencia final real:

```text
CTA regression suite                  PASS
Global test corpus                    53/53 PASS
Factory batch                         9/9 PASS
Godot                                  4.7.1.stable.mono.official.a13da4feb
Factory version                        0.10.0
```

La inspección visual del artefacto regenerado confirmó que la escena CTA final vuelve a mostrar correctamente:

```text
LINK IN BIO
¡Juega ahora!
```

## 2. INCIDENTE CTA — YA RESUELTO

NO investigues otra vez como hipótesis primaria la pérdida del CTA.

La causa raíz ya fue identificada y corregida en `ChallengePresentationBinder.gd`:

Regresión:

```gdscript
model["cta_main"] = str(overrides.get("cta_main", ""))
model["cta_sub"] = str(overrides.get("cta_sub", ""))
```

Corrección histórica:

```gdscript
model["cta_main"] = comp.get("cta_main", "LINK IN BIO")
model["cta_sub"] = comp.get("cta_sub", "¡Juega ahora!")
```

No tocar esta lógica salvo nueva evidencia de regresión.

## 3. CONTRATOS TEMPORALES — FROZEN

La extracción de temporalidad ya está certificada.

### TemporalCore

Responsabilidad exclusiva:

```text
fps
total_frames
_current_frame
duration_to_frames()
advance()
get_current_frame()
is_finished()
```

Matemática congelada:

```text
maxi(0, int(round(duration_seconds * fps)))
```

`advance()` es monotónico y no hace clamp.

### ChallengeTimeline

Sustituye conceptualmente la implementación histórica de `VideoTimeline`, pero mantiene su semántica observable:

```text
HOOK → GAME → REVEAL → CTA
```

con:

```text
zero-frame phases omitted
GAME > 0
```

API histórica preservada:

```text
get_current_block()
is_phase_enabled()
get_game_index()
```

### VideoTimeline

Permanece como shim:

```text
VideoTimeline extends ChallengeTimeline
```

No eliminar ni renombrar todavía.

### VisualLoopTimeline

Hereda `TemporalCore`.

```text
get_loop_frame()     = _current_frame % total_frames
get_loop_iteration() = _current_frame / total_frames
```

El wrap es propiedad exclusiva de `VisualLoopTimeline`.

### VisualDrillTimeline

Hereda de `TemporalCore` sin fases propias.

No inventar fases todavía.

## 4. CONTRATOS DE CONTENT — FROZEN

`ContentEnvelope` NO acepta `challenge`.

Solo:

```text
visual_loop
visual_drill
```

Challenge mantiene su dominio contractual soberano.

Los schemas de Challenge existentes no se amplían para acomodar los visuales.

No fabricar para visuales:

```text
SimulationResult
winning_frame
score
won/lost
ChallengeMechanic
```

## 5. OBJETIVO ACTUAL — C6-F0.3.5

Debes diseñar y auditar la **Content Runtime Boundary**.

Antes de modificar código debes producir un contrato de diseño claro.

No empieces implementando.

## 6. PREGUNTAS OBLIGATORIAS DE LA AUDITORÍA

Resuelve explícitamente:

### A. Frontera de runtime

¿Qué objeto/interfaz representa un runtime de contenido sin acoplarse a un dominio concreto?

### B. Selección

¿Quién decide el runtime a partir de:

```text
kind
subtype
```

y cómo se hace fail-closed?

### C. Challenge

¿Cómo se conecta el pipeline Challenge existente sin que `ContentRuntime` tenga que conocer detalles de:

```text
SimulationResult
WinningFrameDetector
RNG
ChallengeMechanic
```

### D. Visual Loop

¿Cómo entra un `VisualLoop` y cómo sale una secuencia de frames sin fingir que es una Challenge Simulation?

### E. Visual Drill

¿Cómo entra un `VisualDrill` y cómo se genera su secuencia sin introducir fases o semánticas que el schema todavía no define?

### F. Frame stream

Define qué significa exactamente un:

```text
Rendered Frame Stream
```

Qué propiedades mínimas tiene y quién es responsable de producirlo.

### G. Presentation

Dónde termina runtime y dónde empieza presentation.

El runtime NO debe conocer detalles de UI como:

```text
PresentationUI
CTAComponent
WinningHighlight
```

### H. Export

Dónde termina rendering y dónde comienza export.

No convertir `build_factory.py` en el runtime universal por comodidad.

## 7. ARQUITECTURA A EXAMINAR

Usa esto solamente como hipótesis inicial, no como contrato aprobado:

```text
ContentDefinition
        ↓
ContentRuntimeRegistry
        ↓
┌───────────────────────┬────────────────────────┐
│ ChallengeRuntime      │ VideoContentRuntime    │
│                       │                        │
│ sovereign challenge   │ ┌────────────────────┐ │
│ runtime               │ │ VISUAL_LOOP        │ │
│                       │ │ VISUAL_DRILL       │ │
│                       │ └────────────────────┘ │
└───────────────────────┴────────────────────────┘
        ↓
Rendered Frame Stream
        ↓
Presentation
        ↓
Export
        ↓
Provenance / Manifest
```

Audita primero si esta división es realmente correcta.

## 8. PRINCIPIOS DE GOBERNANZA

### Absolutamente congelado

```text
Simulation truth sovereignty
RNG semantics / streams / seeds
SimulationResult
WinningFrameDetector
Challenge mechanic mathematics
Challenge phase semantics
VideoTimeline observable behavior
frame rounding policy
CTA historical payload defaults
```

### Prohibido sin autorización explícita

```text
❌ modificar RNG
❌ modificar SimulationResult
❌ modificar WinningFrameDetector
❌ modificar las ecuaciones de las mecánicas
❌ introducir visual_loop dentro de ChallengeMechanic
❌ introducir visual_drill dentro de ChallengeMechanic
❌ hacer universal VideoTimeline a base de añadir fases
❌ inventar fases de Drill
❌ meter seamlessness en TemporalCore
❌ eliminar VideoTimeline shim sin pruebas
❌ hacer que UI conozca el runtime interno
❌ hacer que Exporter conozca SimulationResult
```

## 9. CRITERIO DE DISEÑO

La nueva arquitectura debe seguir:

```text
authoring
    ↓
content definition
    ↓
runtime selection
    ↓
content-specific runtime
    ↓
Rendered Frame Stream
    ↓
presentation
    ↓
export
```

La dirección de dependencias debe permanecer limpia:

```text
Challenge / Visual content
        ↓
Runtime abstraction
        ↓
Presentation / Export / Provenance
```

No al revés.

## 10. CRITERIO DE ACEPTACIÓN DE F0.3.5

No cierres F0.3.5 solamente porque compile.

Debe existir evidencia de:

```text
✅ runtime boundary clara
✅ routing por kind/subtype fail-closed
✅ Challenge aislado
✅ Visual Loop aislado
✅ Visual Drill aislado
✅ Rendered Frame Stream definido
✅ presentation desacoplada
✅ export desacoplado
✅ negative tests
✅ positive tests
✅ regresión global
✅ factory regression
✅ inspección física del artefacto cuando corresponda
```

## 11. MÉTODO DE TRABAJO OBLIGATORIO

Primero:

```text
AUDITORÍA → CONTRATO → GO/NO-GO
```

Después:

```text
IMPLEMENTACIÓN → TEST ESPECÍFICO → CORPUS GLOBAL → FACTORY → ARTEFACTO FÍSICO
```

No mezcles diseño e implementación.

No reabras un checkpoint cerrado por una sospecha sin evidencia.

## 12. PRIMERA RESPUESTA ESPERADA

Tu primera tarea en esta nueva ventana es producir:

```text
C6-F0.3.5 PRE-IMPLEMENTATION AUDIT
```

Debe responder si la arquitectura propuesta de `Content Runtime Boundary` es correcta, qué piezas son realmente comunes y qué piezas deben permanecer soberanas.

**No escribas código de implementación todavía.**

El objetivo inmediato es conseguir un contrato de diseño F0.3.5 formalmente aprobable antes de tocar el repositorio.
