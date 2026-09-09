# MASTER HANDOVER CHECKPOINT — ChallengeEngineV01_STATELESS

## Estado congelado

**Checkpoint:** C6-F0.3.4 CLOSED / CERTIFIED
**Fecha de checkpoint:** 2026-09-09
**Baseline funcional:** C6-F0.3.3 + C6-F0.3.4 corrigida
**Godot:** 4.7.1.stable.mono.official.a13da4feb
**Factory:** 0.10.0

---

## 1. Propósito de este checkpoint

Este documento congela el estado alcanzado antes de abrir **C6-F0.3.5 — Content Runtime Boundary**.

El objetivo es que otra ventana/chat pueda continuar sin reinterpretar decisiones ya cerradas, sin reabrir contratos históricos y sin volver a investigar problemas ya resueltos.

**Regla principal:** este checkpoint es fuente de continuidad. Las decisiones marcadas como FROZEN/CLOSED no deben modificarse salvo que exista una regresión demostrada y una orden explícita de reapertura/versionado.

---

## 2. Arquitectura global vigente

```text
CONTENT ENGINE
├── CHALLENGE
│   └── ChallengeMechanic
│       └── SimulationResult / WinningFrameDetector / VideoTimeline semantics
│
└── VIDEO_CONTENT
    ├── VISUAL_LOOP
    │   └── procedural visual sequence → loop → video
    │
    └── VISUAL_DRILL
        └── visual exercise sequence → video
```

La nueva rama de contenido visual **no se implementa como ChallengeMechanic**.

No se fabrican para visuales:
- SimulationResult
- winning_frame
- score
- won/lost
- mecánicas de challenge

---

## 3. C6-F0.3 — estado oficial

```text
C6-F0.3.1 Pre-Implementation Audit       ✅ CLOSED
C6-F0.3.2 Schema Boundary                 ✅ CLOSED / CERTIFIED
C6-F0.3.3 Shared Content Envelope         ✅ CLOSED / CERTIFIED
C6-F0.3.4 Temporal Abstraction            ✅ CLOSED / CERTIFIED
C6-F0.3.5 Content Runtime Boundary        ⏭ NEXT
```

### Evidencia real de F0.3.2/F0.3.3

- `C6F0_3MultiContentFoundationTest.gd` PASS.
- Corpus global anterior: 52/52 PASS.
- Tras incorporar la regresión CTA: corpus global 53/53 PASS.
- `build_factory.py --batch ./challenges --output ./output --workers 9`: 9/9 PASS.
- Factory manifest:
  - `manifest_version: 1.0`
  - `factory_version: 0.10.0`
  - Godot `4.7.1-stable (official)`
  - RNG `1.0`, `2.0`
  - status `PASSED`

### Evidencia real de F0.3.4

- Editor headless carga correctamente las nuevas clases globales:
  - `TemporalCore`
  - `ChallengeTimeline`
  - `VisualLoopTimeline`
  - `VisualDrillTimeline`
  - `VideoTimeline`
- Corpus E2E: **53/53 PASS**.
- Factory: **9/9 PASS**.
- Suite específica CTA: **PASS**.
- Inspección visual de los artefactos regenerados: **CTA final restaurado y correcto**.

**Importante:** 53/53 y 9/9 son evidencia de ejecución real aportada en la conversación; no inferir resultados adicionales no mostrados.

---

## 4. C6-F0.3.2 — contratos congelados

### Content Envelope

Ruta:
`res://core/authoring/schemas/content_envelope_schema.json`

Contrato vigente:

```text
schema_version = "2.0"
content_id     = non-empty, ^[A-Z0-9_]+$
content_version = non-empty string
kind           = visual_loop | visual_drill
subtype        = non-empty string
engine_version = non-empty string
authoring_version = non-empty string
```

Envelope anidado:

```text
presentation
├── profile_id           required string non-empty
├── coordinate_space     required string non-empty
└── theme                optional string

assets
├── family_id            required string non-empty
└── background_path      optional string

audio
├── profile_id           required string non-empty
└── enabled              required boolean

provenance
├── author               required string non-empty
└── timestamp_ms         required integer >= 0
```

Todas estas estructuras usan `additionalProperties: false`.

### Frontera Challenge

**FROZEN:** `challenge` NO pertenece al `ContentEnvelope` multipropósito.

Challenge conserva:
- sus schemas soberanos
- su orquestación soberana
- su semántica histórica

No introducir Challenge dentro de `ContentEnvelope` en F0.3.5.

---

## 5. Payload contracts congelados

### VISUAL_LOOP

Ruta normativa:
`res://core/authoring/schemas/visual_loop_schema.json`

Campos:

```text
duration >= 0.1
fps ∈ {30, 60}
frame_count >= 1
loop
visual_parameters
```

`loop`:

```text
seamless: boolean
boundary_tolerance: number, 0.0 <= x <= 0.01
transition_window_frames: optional integer >= 0
```

`visual_parameters`:

```text
generator ∈ {
  fractal,
  vector_field,
  particle_flow,
  kaleidoscope,
  geometric
}
layers: non-empty array
```

Cada layer:

```text
blend_mode: required string
speed: required number
complexity: required integer
color_palette: optional string
```

### VISUAL_DRILL

Ruta normativa:
`res://core/authoring/schemas/visual_drill_schema.json`

Campos:

```text
duration >= 0.1
fps ∈ {30, 60}
frame_count >= 1
exercise_parameters
stimulus
targets
distractors
trajectory
task
```

`exercise_parameters`:

```text
difficulty_tier: integer 1..5
speed_multiplier: number
pacing_mode: optional {constant, accelerating, pulsed}
```

`stimulus`:

```text
shape ∈ {dot, ring, target, polygon}
size: number
color: string
```

`targets.count >= 1`

`distractors.count >= 0`

`trajectory`:

```text
pattern ∈ {linear, lissajous, random_walk, orbital}
speed: number
```

`task`:

```text
type ∈ {pursuit, saccade, tracking, peripheral_scan}
target_switch_interval: optional number
```

---

## 6. `ContentSchemaValidator` — contrato vigente

Ruta:
`res://core/validation/ContentSchemaValidator.gd`

Responsabilidades:

```text
1. Validar documento root.
2. Aplicar additionalProperties:false a root.
3. Validar ContentEnvelope.
4. Despachar exclusivamente por kind:
   visual_loop / visual_drill
5. Validar estructura completa de cada payload.
6. Aplicar restricciones numéricas y enums.
7. Aplicar invariantes cross-field.
```

Invariante temporal:

```text
frame_count == round(duration * fps)
```

`frame_count` es una declaración verificable, no una autoridad runtime independiente.

### Seamless

`seamless` es actualmente **declarativo**.

No afirmar que un loop es perceptualmente seamless solamente porque el campo sea `true`.
La validación física/visual de continuidad pertenece a una futura capa runtime/render.

---

## 7. C6-F0.3.4 — Temporal Abstraction congelada

### `TemporalCore.gd`

Ruta:
`res://core/authoring/TemporalCore.gd`

Responsabilidad única:

```text
fps
total_frames
_current_frame

duration_to_frames()
advance()
get_current_frame()
is_finished()
```

Comportamiento congelado:

```text
fps <= 0 → fallback histórico 60
advance() → _current_frame += 1
sin clamp
sin wrap
is_finished() → _current_frame >= total_frames
```

Única matemática temporal reutilizable:

```text
maxi(0, int(round(duration_seconds * fps)))
```

**NO cambiar esta fórmula durante F0.3.5.**

---

## 8. `ChallengeTimeline` — semántica Challenge congelada

Ruta:
`res://core/authoring/ChallengeTimeline.gd`

Hereda de `TemporalCore`.

Conserva:

```text
hook_frames
game_frames
reveal_frames
cta_frames
```

Y la semántica:

```text
HOOK → GAME → REVEAL → CTA
```

Las fases de 0 frames se omiten efectivamente.

API congelada:

```text
get_current_block()
is_phase_enabled()
get_game_index()
```

`total_frames`:

```text
hook_frames + game_frames + reveal_frames + cta_frames
```

No tocar:
- RNG
- SimulationResult
- WinningFrameDetector
- matemáticas de las mecánicas
- lógica de winning frame

---

## 9. `VideoTimeline` — shim de compatibilidad

Ruta:
`res://core/authoring/VideoTimeline.gd`

Actualmente:

```text
VideoTimeline extends ChallengeTimeline
```

Su finalidad es mantener el `class_name VideoTimeline` y evitar migraciones indiscriminadas de consumidores históricos.

**No eliminar ni renombrar durante F0.3.5 sin evidencia de que ya no sea necesario.**

---

## 10. `VisualLoopTimeline` — contrato congelado

Ruta:
`res://core/authoring/VisualLoopTimeline.gd`

Hereda de `TemporalCore`.

Construye:

```text
total_frames = duration_to_frames(duration)
```

Semántica:

```text
absolute cursor:
0 1 2 3 ... N N+1 N+2 ...

loop frame:
_current_frame % total_frames

loop iteration:
_current_frame / total_frames
```

API:

```text
get_loop_frame()
get_loop_iteration()
```

**TemporalCore NO hace wrap.**

El wrap es responsabilidad exclusiva del timeline de loop.

---

## 11. `VisualDrillTimeline` — contrato congelado

Ruta:
`res://core/authoring/VisualDrillTimeline.gd`

Hereda estrictamente de `TemporalCore`.

Actualmente no tiene semántica de fases.

**NO inventar**:
- instruction
- exercise
- closing
- otras fases

hasta que el contrato/schema lo declare formalmente.

---

## 12. Regresión audiovisual CTA — incidente cerrado

### Síntoma

Tras la primera extracción temporal, el timeline conservaba el CTA pero los vídeos finales mostraban la escena CTA sin textos.

### Causa raíz

La regresión estaba en `ChallengePresentationBinder.gd`.

Histórico correcto:

```gdscript
model["cta_main"] = comp.get("cta_main", "LINK IN BIO")
model["cta_sub"] = comp.get("cta_sub", "¡Juega ahora!")
```

Regresión introducida:

```gdscript
model["cta_main"] = str(overrides.get("cta_main", ""))
model["cta_sub"] = str(overrides.get("cta_sub", ""))
```

Esto vaciaba los textos cuando no existían overrides.

### Corrección

Se restauraron los defaults históricos:

```text
LINK IN BIO
¡Juega ahora!
```

No se modificó el contenido para crear un nuevo texto "LINK TO THE BIO".

### Suite dedicada

`C6F0_3_4CTARenderRegressionTest.gd`

Verificó:

```text
✅ timeline llega a CTA
✅ RenderModel recupera payload CTA
✅ PresentationUI muestra textos CTA
```

Resultado real:

```text
[C6F0_3_4_CTA_RENDER_REGRESSION_SUITE] PASS
```

Y después:

```text
[BATCH-RUNNER] PASS — 53 suite(s) superaron la auditoría E2E.
```

Factoría posterior:

```text
9 total
9 passed
0 failed
```

La inspección visual aportada por el usuario confirmó que el CTA final vuelve a estar presente correctamente.

---

## 13. Artefactos audiovisuales y autoridad física

Para Challenge, la salida de producción mantiene el contrato histórico:

```text
logical/simulation canvas: 1080x1920
Godot source movie:       540x960
master MP4:               1080x1920
codec:                    H.264
pixel format:             YUV420-compatible
upscale:                  FFmpeg Lanczos 2x
FFprobe:                  autoridad física final
```

La pipeline de vídeo no debe considerarse validada exclusivamente por suites lógicas.

**El artefacto físico debe inspeccionarse cuando una modificación afecta render/export.**

---

## 14. Invariantes de gobernanza

### Absolutamente congelado salvo reapertura explícita

```text
Simulation truth sovereignty
RNG semantics, streams and seeds
SimulationResult
WinningFrameDetector
Challenge mechanic mathematics
Challenge phase semantics
VideoTimeline historical observable behavior
VideoTimeline / ChallengeTimeline compatibility
frame rounding policy
```

### No permitido en F0.3.5 por iniciativa propia

```text
❌ refactorizar RNG
❌ modificar mecánicas
❌ cambiar winning-frame math
❌ convertir Challenge en un ContentDocument visual
❌ inventar fases Drill
❌ introducir visuales dentro de ChallengeMechanic
❌ meter seamlessness en TemporalCore
❌ cambiar build_factory por motivos cosméticos
❌ eliminar VideoTimeline shim sin corpus específico que lo justifique
```

---

## 15. Punto exacto de continuación: C6-F0.3.5

### Objetivo

Definir la frontera de runtime entre:

```text
CHALLENGE
VISUAL_LOOP
VISUAL_DRILL
```

sin que `ContentEngine` conozca detalles internos indebidos ni que las ramas visuales entren en el dominio Challenge.

### Preguntas que deben resolver la siguiente ventana

```text
1. ¿Cuál es el contrato mínimo de un Content Runtime?
2. ¿Cuál es la interfaz común de entrada/salida?
3. ¿Quién selecciona el runtime por kind/subtype?
4. ¿Cómo se evita que Content Runtime conozca SimulationResult?
5. ¿Cómo se representa una secuencia de frames sin inventar una nueva simulación universal?
6. ¿Qué parte corresponde a authoring, runtime, rendering y export?
7. ¿Cómo se prueba el aislamiento Challenge/VideoContent?
```

### Arquitectura objetivo a estudiar

```text
ContentDefinition
        ↓
ContentRuntimeRegistry
        ↓
┌───────────────────────┬────────────────────────┐
│ ChallengeRuntime      │ VideoContentRuntime    │
│                       │                        │
│ existing challenge    │ ┌────────────────────┐ │
│ sovereign pipeline    │ │ VISUAL_LOOP        │ │
│                       │ │ VISUAL_DRILL       │ │
│                       │ └────────────────────┘ │
└───────────────────────┴────────────────────────┘
        ↓
Rendered Frame Stream
        ↓
Presentation / Export / Provenance
```

Esto es una **dirección de auditoría/diseño**, no un contrato ya aprobado.

---

## 16. Criterio de entrada de F0.3.5

La siguiente ventana debe comenzar con este dictamen ya establecido:

```text
C6-F0.3.1  CLOSED
C6-F0.3.2  CLOSED / CERTIFIED
C6-F0.3.3  CLOSED / CERTIFIED
C6-F0.3.4  CLOSED / CERTIFIED

NEXT: C6-F0.3.5 Content Runtime Boundary
```

No repetir desde cero la auditoría temporal ni la investigación CTA salvo que aparezca una regresión nueva.

---

## 17. Nota sobre el baseline entregado

El baseline de continuidad aportado en la conversación fue:

`ChallengeEngineV01_STATELESS_C6_F.0_3_3.zip`

Contiene la versión congelada de F0.3.3 junto con la implementación posterior de la abstracción temporal y los artefactos generados utilizados para detectar/corregir la regresión CTA.

La última evidencia de ejecución corresponde a la versión corregida:

```text
53/53 global PASS
9/9 factory PASS
CTA regression PASS
visual output inspected and CTA restored
```

**Estado de esta checkpoint: CONGELADO.**
