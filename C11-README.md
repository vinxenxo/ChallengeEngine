Sí. **Oficializaría C11**, pero con una corrección importante respecto al planteamiento anterior:

> **C11 no debe empezar mejorando los renderers. Debe empezar midiendo el producto visual real a escala.**

La propia visión del proyecto es precisamente una fábrica reproducible y escalable que parte de reto + parámetros + semilla y termina en vídeo terminado.  Además, la arquitectura ya establece claramente que Godot calcula/renderiza y que Python orquesta la producción. 

Y tenemos una razón técnica muy concreta para hacerlo así: **el C10 smoke físico demuestra que el pipeline funciona para dos rutas concretas, pero no demuestra todavía que las nueve familias visuales mantengan una calidad visual aceptable al cambiar sistemáticamente de seed.**

## C11 — VISUAL QUALIFICATION, POLISH & PRODUCTION

**Estado: OPEN**

Yo lo estructuraría así:

```text
C11-A  Visual Seed Qualification
       ↓
C11-B  Visual Art Direction / Polish
       ↓
C11-C  Production Export Qualification
       ↓
C11-D  Distribution Metadata / Social Packaging
       ↓
C11 FREEZE
```

Y el orden es deliberado.

### C11-A — Visual Seed Qualification & Bulk Render

Este debe ser el primer checkpoint.

No modifica:

```text
C6-F0.8
C10
Visual Loop mathematics
Visual Drill mathematics
RNG ownership
RenderedFrameStream
ContentRuntimeRegistry
Binder architecture
passive-renderer contract
```

Su misión es exclusivamente responder:

> **¿Qué aspecto tienen realmente nuestras nueve familias cuando las sometemos a semillas distintas y se renderizan físicamente?**

### Qué haría C11-A

Un nuevo orquestador específico para Visual Content, por encima de C10:

```text
Seed Matrix
    ↓
VisualAuthoringRequest
    ↓
VisualAuthoringGenerator
    ↓
Content Envelope V2
    ↓
ContentRuntimeRegistry
    ↓
RenderedFrameStream
    ↓
VisualContentPlayer
    ↓
Movie Maker
    ↓
AVI
    ↓
FFmpeg
    ↓
MP4
    ↓
ffprobe
    ↓
Visual QA artifacts
```

Esto es importante porque **no reutilizaría ciegamente el viejo `run_batch_export.py`**. Ese mecanismo histórico modifica el `F0_8MovieMakerPilot.tscn` durante las ejecuciones y trabaja sobre definiciones temporales; para C11 necesitamos que la entrada sea el contrato C10 de authoring y que el proceso sea completamente externo y no mutante.

## Primera matriz

Yo empezaría con las **9 rutas canónicas × 6 casos de seed**:

```text
12345
54321
314159
7770001
998877
12345  ← repetición A/B
```

Por tanto:

```text
9 × 6 = 54 renders físicos
```

No estamos intentando “demostrar aleatoriedad” estadísticamente. Estamos construyendo un **corpus visual de producción**.

El `12345` repetido tiene una función especialmente importante:

```text
same request
same seed
same route
        ↓
A
B
```

y nos permite comprobar que la cadena completa sigue siendo reproducible.

Los otros cinco seeds sirven para estudiar:

```text
variación
composición
legibilidad
posición
densidad
movimiento
color
casos extremos
```

### Muy importante: no empezaría cambiando tiers

El primer barrido debe ser:

```text
tier = 2
```

porque necesitamos separar dos variables.

Primero:

> **¿El mismo producto visual se comporta bien al variar la seed?**

Después:

> ¿Cómo se comporta al cambiar dificultad?

Así evitamos mezclar inmediatamente:

```text
seed
+
tier
+
assets
+
export profile
```

y no saber qué está provocando un problema.

---

# Artefactos que debe producir C11-A

No quiero simplemente 54 MP4.

Cada caso debería generar algo equivalente a:

```text
run/
├── envelope.json
├── render.avi
├── render.mp4
├── metadata.json
├── frame_000.png
├── frame_025.png
├── frame_050.png
├── frame_075.png
├── frame_100.png
└── contact_sheet.png
```

Y a nivel de lote:

```text
C11_VISUAL_BULK_MANIFEST.json
```

con una entrada por ejecución:

```json
{
  "route": "visual_loop/fractal",
  "seed": 314159,
  "tier": 2,
  "authoring_hash": "...",
  "envelope_hash": "...",
  "avi_sha256": "...",
  "mp4_sha256": "...",
  "width": 540,
  "height": 960,
  "fps": 30,
  "frames": 60,
  "duration_seconds": 2.0,
  "technical_status": "PASS",
  "visual_review": "PENDING"
}
```

Ese último punto es deliberado.

## No quiero un `VISUAL_PASS` automático

Una máquina puede decir:

```text
54/54 exportados
54/54 ffprobe correcto
54/54 hashes correctos
```

pero no puede afirmar por sí sola:

> “este vídeo tiene una buena dirección de arte”.

La salida del primer checkpoint debe separar:

```text
TECHNICAL PASS
```

de:

```text
VISUAL REVIEW REQUIRED
```

---

# La revisión visual sí debe ser sistemática

Para cada familia revisaremos al menos:

| Criterio       | Qué buscamos                                         |
| -------------- | ---------------------------------------------------- |
| Legibilidad    | Se entiende qué está ocurriendo                      |
| Composición    | No parece una escena vacía o accidental              |
| Contraste      | Elementos principales destacan                       |
| Safe area      | Nada importante queda mal colocado                   |
| Escala         | Objetos suficientemente grandes                      |
| Movimiento     | Se percibe con claridad                              |
| Temporalidad   | El momento ganador resulta visualmente identificable |
| Seed variation | Las semillas producen variedad real                  |
| Seed collapse  | Las semillas no parecen prácticamente iguales        |
| Artefactos     | No hay clipping, aliasing o glitches                 |
| Jerarquía      | Hook / juego / objetivo / CTA están claros           |
| Calidad        | No parece una demo técnica                           |

Y aquí creo que está **exactamente el problema que has detectado tú**.

Por la inspección física del C10 smoke actual, hay indicios claros de que algunas rutas siguen teniendo una presentación muy básica: el fractal tiene una apariencia extremadamente simple y el tracking deja una cantidad importante de espacio visual sin utilizar. Eso no es un fallo de arquitectura matemática; es precisamente el tipo de problema que C11 debe convertir en evidencia cuantificable antes de empezar a “embellecer”.

---

# C11-B — Visual Art Direction / Polish

**No lo abriría todavía.**

Primero necesitamos que C11-A nos diga:

```text
FRACTAL
→ problema de densidad

TRACKING
→ problema de composición

PURSUIT
→ ...

SACCADE
→ ...

...
```

Entonces sí podemos modificar:

```text
shader
material
palette
background
particle appearance
glow
stroke
line weight
visual hierarchy
assets
post-processing
```

pero con una regla absolutamente estricta:

```text
RenderedFrameStream
        ↓
     renderer
        ↓
      pixels
```

El renderer puede cambiar radicalmente de aspecto.

No puede cambiar:

```text
mechanics
timing
RNG
winning_frame
routing
simulation
```

Eso encaja perfectamente con la arquitectura existente, donde los temas visuales son contenido/presentación y no nuevas familias matemáticas. 

---

# C11-C — aquí tenemos otro asunto importante

Hay una cuestión que **no debemos esconder dentro del bulk runner**.

El C10 smoke actual utiliza:

```text
540 × 960
30 FPS
60 frames
2 s
```

mientras que el producto de distribución tiene objetivos de publicación más amplios.

Por tanto yo **no cambiaría todavía resolución ni FPS**.

C11-A debe utilizar el contrato físico actualmente probado:

```text
540 × 960
30 FPS
60 frames
```

y producir evidencia.

Después abriremos C11-C para decidir explícitamente:

```text
¿Render nativo 1080×1920 @ 60?
```

o

```text
¿Render base + transformación/export profile?
```

o cualquier tercera solución que resulte técnicamente correcta.

No debemos convertir una cuestión de exportación en una modificación accidental del contrato de authoring.

---

# C11-D — Social Metadata

Aquí también estoy de acuerdo contigo, pero **después**.

Una vez que tengamos:

```text
vídeo técnicamente correcto
+
vídeo visualmente aceptable
+
export final estabilizado
```

entonces el manifest puede evolucionar hacia:

```json
{
  "video": {},
  "challenge": {},
  "provenance": {},
  "distribution": {
    "description": "...",
    "hashtags": [],
    "title": "...",
    "language": "es"
  }
}
```

Eso sigue manteniendo la capa social fuera del núcleo determinista, que es justamente la separación que queremos.

---

# Contrato propuesto para C11-A

Yo congelaría ahora este contrato conceptual:

```text
C11-A
VISUAL SEED QUALIFICATION & BULK RENDER HARNESS
```

### Entrada

```text
canonical_visual_routes
seed_matrix
difficulty_tier
export_profile
```

### Obligaciones

```text
1. Generar mediante C10 Authoring.
2. No modificar definiciones canónicas.
3. No modificar C10 tests.
4. No modificar frozen visual runtime.
5. No inyectar RNG-level parameters.
6. Exportar físicamente cada caso.
7. Validar AVI/MP4 con ffprobe.
8. Registrar hashes.
9. Registrar seed y route.
10. Crear muestras visuales.
11. Crear manifest agregado.
12. Detectar fallos técnicos.
13. Marcar revisión visual humana como pendiente.
```

### Salida

```text
C11_VISUAL_BULK_MANIFEST.json
+
54 physical renders
+
270 sampled frames
+
54 contact sheets
```

Los 270 frames salen de:

```text
54 renders × 5 frames
```

y nos darán una primera visión bastante potente del estado real.

---

# Y el punto arquitectónico más importante

**No tocaría `build_factory.py` todavía.**

Tenemos ya una factoría de producción para el pipeline general. El problema de C11 es distinto: necesitamos una **Visual Bulk QA Factory**.

Así evitamos convertir una herramienta de producción existente en una herramienta que empiece a acumular responsabilidades de:

```text
Challenge production
+
Visual authoring
+
Visual QA
+
Social distribution
```

Eso sería exactamente el tipo de contaminación arquitectónica que hemos evitado hasta C10.

---

## CHECKPOINT C11-A

```text
C11 — VISUAL QUALIFICATION, POLISH & PRODUCTION
STATUS: OPEN

C11-A — Visual Seed Qualification & Bulk Render Harness
STATUS: CONTRACT DEFINITION

OBJECTIVE:
Validar físicamente la variabilidad visual de las 9 rutas canónicas
mediante múltiples seeds y un corpus reproducible de exportación.

INPUT:
Visual Authoring Request + external seed matrix

OUTPUT:
Physical render corpus + technical manifest + visual QA corpus

FROZEN DEPENDENCIES:
C6-F0.8
C10
RNG 2001–2005 / 2011–2014
RenderedFrameStream
ContentRuntimeRegistry
Passive renderers

OUT OF SCOPE:
Math
RNG
Routing
Authoring contract
Social APIs
New visual families
Production resolution redesign

GO / NO-GO:

GO — abrir C11-A y pasar a implementación
NO-GO — tocar renderers/policies/export profile antes de obtener el corpus
```

**Mi recomendación concreta es que el siguiente paso sea ya el contrato técnico exacto del runner C11-A — archivos, CLI, estructura de directorios, seed matrix, manifest schema y gates de validación— y solo después escribir el código.**

La razón es que ahora sí estamos atacando la carencia que señalas: **no nos falta otra capa arquitectónica; nos falta demostrar qué producto visual estamos produciendo realmente cuando la fábrica deja de usar un par de semillas de demostración.**
