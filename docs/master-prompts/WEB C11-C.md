He preparado un **prompt maestro para Lovable** pensado no como una landing genérica, sino como la web oficial de un proyecto técnico/visual que explique qué es Challenge Engine, por qué existe, cómo funciona, qué familias contiene y hacia dónde va C11-D. La prioridad es que Lovable construya una identidad propia y no una típica web SaaS.

# MASTER PROMPT — CHALLENGE ENGINE

## Official Project Website — Lovable Build Specification

Construye la web oficial de **Challenge Engine**, un proyecto de ingeniería audiovisual procedural orientado a la generación determinista, reproducible y escalable de vídeos cortos de challenges para formatos sociales verticales.

No quiero una landing SaaS genérica, ni una página corporativa convencional, ni una web de “startup AI”. Quiero una experiencia digital premium que combine:

* ingeniería procedural;
* visuales matemáticos;
* estética retro-futurista;
* cultura arcade;
* precisión técnica;
* documentación viva;
* sensación de laboratorio de software audiovisual.

La web debe comunicar que **Challenge Engine no es simplemente un generador de vídeos**: es una arquitectura de producción que busca convertir mecánicas de juegos/challenges en una cadena de generación audiovisual determinista, declarativa, reproducible y trazable.

El visitante debe entender rápidamente:

1. qué es Challenge Engine;
2. qué problema resuelve;
3. cómo se generan los vídeos;
4. qué diferencia existe entre Simulation, Presentation, Audio y Delivery;
5. por qué la determinidad y la trazabilidad son importantes;
6. qué son Visual Loops, Visual Drills y Challenges;
7. cómo C11-C aporta las lecciones de producción maduras;
8. cómo C11-D está normalizando esas capacidades para los Challenges recuperados de C11-A/C11-B;
9. por qué los assets, seeds, música y provenance forman parte del sistema;
10. que el proyecto está construido con una filosofía de ingeniería rigurosa y no mediante hacks audiovisuales aislados.

---

# 1. CONTEXTO Y PROPÓSITO

## Nombre del proyecto

**Challenge Engine**

Submarca técnica:

**CHALLENGE ENGINE / PROCEDURAL VIDEO SYSTEM**

Descriptor principal:

**Deterministic procedural video generation for games, challenges and social formats.**

Descriptor alternativo:

**From gameplay truth to reproducible audiovisual content.**

## Propósito

Challenge Engine fabrica vídeos verticales de challenges mediante una arquitectura procedural.

La idea fundamental es separar:

**Simulation Truth**

de:

**Presentation**

de:

**Audio**

de:

**Delivery**

y mantener además:

**Seed + Provenance**

como información trazable de cada artefacto generado.

El sistema nació alrededor de challenges y mecánicas recuperadas de ramas anteriores del proyecto, pero evolucionó hasta incorporar una infraestructura mucho más madura de producción visual, editorial y audiovisual.

La rama C11-C consolidó una infraestructura de producción visual para:

* Visual Loops;
* Visual Drills;
* production/review workflows;
* layouts sociales;
* procedural visuals;
* editorial presentation;
* deterministic generation;
* QA;
* provenance;
* delivery.

La rama C11-D tiene como objetivo llevar esas capacidades maduras a la familia **Challenge**, recuperando y normalizando el contenido proveniente de C11-A/C11-B.

La web debe explicar esta evolución como una **convergencia arquitectónica**, no como una migración improvisada.

## Mensaje estratégico

La frase conceptual que debe recorrer toda la web:

> **Build once. Simulate deterministically. Present consistently. Generate reproducibly.**

Otra frase clave:

> **One production architecture. Many visual identities.**

Y otra:

> **The mechanic defines the truth. The presentation defines the experience.**

---

# 2. VIBRA GENERAL

La sensación general debe ser:

**premium procedural laboratory + arcade engineering + retro-futuristic audiovisual system**

No debe parecer:

* una web de una agencia;
* una consultora;
* una startup de IA;
* una plantilla SaaS;
* una web de videojuegos infantil;
* un portfolio de diseñador;
* una dashboard empresarial aburrida.

Debe transmitir:

* precisión;
* profundidad;
* control;
* experimentación;
* tecnología;
* matemáticas;
* movimiento;
* arcade;
* sonido;
* sistemas;
* reproducibilidad.

La web debe sentirse como el sitio oficial de una tecnología audiovisual interna que podría convertirse en una plataforma.

---

# 3. DIRECCIÓN DE ARTE

## Tema

**Dark mode estricto.**

No implementar Light Mode.

El fondo no debe ser negro puro.

Debe ser un dark blue-black / graphite tecnológico.

## Paleta

Usar variables CSS, no colores hardcoded repetidos.

### Background

```text
--background: #080B10
--background-soft: #0D121A
```

### Surfaces

```text
--surface-1: #101722
--surface-2: #151D29
--surface-3: #1B2533
```

### Primary

```text
--cyan: #6EE7FF
```

### Secondary

```text
--violet: #9A8CFF
```

### Accent

```text
--acid: #B9FF5C
```

### Warm accent

```text
--amber: #FFB84D
```

### Error / warning

```text
--red: #FF647C
```

### Text

```text
--text-primary: #F4F7FA
--text-secondary: #A5AFBC
--text-muted: #667180
```

No pastel palette.

No gradients pastel.

No rainbow gradients.

No excessive neon.

Neon should be used as an **instrument highlight**, not as the whole interface.

---

# 4. VISUAL LANGUAGE

El lenguaje visual debe inspirarse en:

* CRT;
* arcade hardware;
* mathematical visualization;
* procedural graphics;
* terminal interfaces;
* industrial control systems;
* generative art;
* technical documentation;
* motion design;
* retro computing.

Pero con acabado contemporáneo.

No crear una estética “cyberpunk cliché”.

Nada de:

* hackers con capucha;
* código cayendo por la pantalla;
* robots genéricos;
* ciudad futurista;
* circuit boards de stock;
* AI brains;
* manos humanas con tecnología;
* hologramas genéricos;
* astronautas;
* ilustraciones corporativas.

La sofisticación debe venir de:

* geometría;
* movimiento;
* datos;
* tipografía;
* partículas;
* grids;
* líneas;
* seeds;
* diagramas;
* visualización matemática;
* animación procedural.

---

# 5. TIPOGRAFÍA

Usar:

### Headlines

**Space Grotesk**

Peso:

600 / 700

### Body

**Inter**

Peso:

400 / 500 / 600

### Technical / Data

**IBM Plex Mono**

Usarla para:

* seeds;
* IDs;
* versiones;
* hashes;
* estados;
* etiquetas;
* metadata;
* números;
* pequeños elementos técnicos.

No utilizar demasiadas fuentes.

---

# 6. FORMAS Y COMPONENTES

Usar:

* cards con border sutil;
* radios moderados;
* 10–14 px;
* superficies oscuras;
* bordes de 1px;
* glow muy limitado;
* sombras profundas pero suaves.

No utilizar:

* tarjetas gigantes con esquinas exageradamente redondas;
* glassmorphism extremo;
* blobs;
* neumorphism;
* botones “pill” para absolutamente todo.

Los elementos técnicos pueden tener esquinas más rectas.

Los elementos editorial/CTA pueden tener radios moderados.

## Bordes

Bordes ligeramente visibles:

```text
rgba(255,255,255,0.08)
```

Hover:

```text
rgba(110,231,255,0.35)
```

---

# 7. STACK TECNOLÓGICO

Usar:

* React;
* TypeScript;
* Tailwind CSS;
* shadcn/ui;
* Lucide React;
* Framer Motion.

Usar CSS variables para el Design System.

Usar componentes reutilizables.

No construir toda la web como un único componente gigantesco.

Crear componentes independientes para:

* Navbar;
* Hero;
* StatusStrip;
* ArchitectureDiagram;
* FamilyCard;
* ChallengeCard;
* PipelineStep;
* MetricCard;
* Roadmap;
* TechnicalPanel;
* Footer.

Usar animaciones GPU-friendly.

Evitar animaciones excesivamente pesadas.

No utilizar Three.js salvo que Lovable demuestre que el efecto resulta realmente mejor que una solución CSS/SVG/canvas mucho más ligera.

Para esta primera versión prefiero:

**CSS + SVG + Canvas + Framer Motion**

antes que un 3D complejo.

---

# 8. ESTRUCTURA GENERAL

Crear una web **single-page vertical premium**, con navegación anclada.

Navbar sticky.

Secciones:

1. Navbar
2. Hero
3. System Status
4. What is Challenge Engine?
5. Architecture
6. Three Content Worlds
7. Challenges
8. Visual Loops
9. Visual Drills
10. Determinism
11. Asset Families
12. Music / Audio
13. C11-D Roadmap
14. Engineering Principles
15. Technical Status
16. Final CTA
17. Footer

---

# 9. NAVBAR

Navbar fija en la parte superior.

Izquierda:

```text
CHALLENGE ENGINE
```

Pequeño descriptor:

```text
PROCEDURAL VIDEO SYSTEM
```

Centro:

```text
SYSTEM
ARCHITECTURE
CONTENT
ROADMAP
```

Derecha:

Botón:

```text
ENTER THE LAB
```

El botón puede llevar al final de la página o a una sección “Lab”.

Navbar sobre fondo oscuro semitransparente.

Border inferior mínimo.

---

# 10. HERO

El Hero debe ser espectacular.

No utilizar una imagen de stock.

No utilizar una ilustración prefabricada.

Crear un fondo procedural propio mediante:

* grid;
* líneas;
* pequeños puntos;
* ondas geométricas;
* partículas;
* trayectorias;
* números;
* semillas;
* pequeños labels técnicos.

La composición debe sentirse como una simulación viva.

### Eyebrow

```text
C11-D / PROCEDURAL VIDEO SYSTEM
```

### H1

```text
TURN GAMEPLAY
INTO REPRODUCIBLE
VIDEO.
```

“VIDEO.” puede tener un tratamiento visual diferente.

### Subheadline

```text
Challenge Engine is a deterministic audiovisual production system built to turn game mechanics into reproducible, presentation-ready vertical videos.
```

### Secondary text

```text
Simulation truth stays immutable.
Everything around it becomes programmable, declarative and traceable.
```

### Primary CTA

```text
EXPLORE THE SYSTEM
```

### Secondary CTA

```text
VIEW THE ROADMAP
```

Debajo del CTA, añadir una micro metadata line:

```text
720 × 1280 • 30 FPS • DETERMINISTIC • PROCEDURAL
```

Nota:

La referencia histórica de Challenge internamente conserva una lógica de render/captura nativa de 540×960 con delivery 720×1280. La web debe presentar 720×1280 como **social delivery target**, no afirmar que toda la simulación se calcula nativamente a 720×1280.

---

# 11. HERO INTERACTIVE ENGINE PANEL

A la derecha del Hero, mostrar un “live engine panel”.

Ejemplo:

```text
ENGINE / PREVIEW

CHALLENGE_001
KEY

SEED
12345

FRAME
0540

FPS
30

STATUS
DETERMINISTIC

PRESENTATION
LOCKED

AUDIO
READY
```

Los valores pueden animarse ligeramente.

Pero debe ser una **visualización conceptual**, claramente etiquetada como:

```text
SYSTEM PREVIEW
```

No fingir que se está ejecutando el engine real en navegador.

Cada cierto tiempo cambiar visualmente el seed mostrado entre valores conocidos:

```text
12345
314159
54321
7770001
998877
```

Mantenerlos como ejemplos históricos de determinismo, no como “live generation”.

---

# 12. SYSTEM STATUS STRIP

Debajo del hero:

Una línea horizontal de estado.

Mostrar:

```text
C11-C
FROZEN

C11-D
ACTIVE

D0
CLOSED

D1
CLOSED

D2
CLOSED

D3
NEXT
```

Cada estado con pequeño indicador.

Usar:

* verde ácido para CLOSED/PASS;
* cyan para ACTIVE;
* amber para NEXT.

No usar rojo salvo errores reales.

---

# 13. WHAT IS CHALLENGE ENGINE?

Título:

```text
A VIDEO ENGINE,
NOT A VIDEO TEMPLATE.
```

Texto:

```text
Challenge Engine does not simply place graphics around a prerecorded animation.

It separates gameplay truth from presentation, audio and delivery so every generated video can be reproduced, inspected and evolved without rewriting the underlying mechanic.
```

Mostrar cuatro bloques:

### SIMULATION

```text
The game decides what happened.
```

### PRESENTATION

```text
The system decides how it is shown.
```

### AUDIO

```text
Music and sound become deterministic production layers.
```

### DELIVERY

```text
The same content becomes platform-ready media.
```

Debajo:

```text
SEED + PROVENANCE
```

Texto:

```text
Every important generation decision should remain traceable.
```

---

# 14. ARCHITECTURE

Esta debe ser una de las secciones principales de la web.

Título:

```text
ONE TRUTH.
MULTIPLE LAYERS.
```

Crear diagrama visual:

```text
                 ┌─────────────────────┐
                 │   GAMEPLAY TRUTH    │
                 │ Simulation / Rules  │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │   RESULT / FRAMES   │
                 │ winning_frame etc.  │
                 └──────────┬──────────┘
                            │
               ┌────────────┼────────────┐
               ▼            ▼            ▼
        PRESENTATION      AUDIO       PROVENANCE
               │            │            │
               └────────────┼────────────┘
                            ▼
                 ┌─────────────────────┐
                 │   DELIVERY LAYER    │
                 │ Social / Review /   │
                 │ Production Profiles │
                 └─────────────────────┘
```

No presentar esto como código ejecutable.

Es una arquitectura conceptual.

Animación:

La línea de conexión viaja suavemente de izquierda a derecha.

---

# 15. PRESENTATION CONTRACT

Crear una pequeña sección técnica:

### TITLE

```text
PRESENTATION IS NOT SIMULATION.
```

Copy:

```text
The presentation layer consumes simulation results.
It does not redefine them.
```

Mostrar:

```text
540 × 960
LOGICAL CANVAS
```

↓

```text
720 × 1280
SOCIAL DELIVERY
```

Mostrar además:

```text
HEADER
0 — 144

BODY
144 — 816

FOOTER
816 — 960
```

Añadir etiqueta:

```text
CANONICAL CHALLENGE SOCIAL GEOMETRY
```

Esto debe presentarse como contrato técnico, no como simple diseño.

---

# 16. THE THREE CONTENT WORLDS

Título:

```text
THREE WAYS TO GENERATE MOTION.
```

Tres grandes cards.

## CHALLENGE

Tag:

```text
MECHANIC-DRIVEN
```

Descripción:

```text
Interactive-looking visual challenges generated from deterministic gameplay mechanics.
```

Ejemplos:

```text
KEY
PARKING
PILOT
HIT
CATCH
FIND
CHOOSE
COUNT
```

## VISUAL LOOPS

Tag:

```text
PURE PROCEDURAL MOTION
```

Descripción:

```text
Continuous generative visual systems designed around mathematical motion, rhythm and visual grammar.
```

Familias:

```text
GEOMETRIC WAVES
FRACTAL BLOOM
SACRED SYMMETRY
LIVING PARTICLES
INVISIBLE FORCES
```

## VISUAL DRILLS

Tag:

```text
ATTENTION / TRACKING
```

Descripción:

```text
Motion-driven visual drills designed around tracking, saccades, pursuit and peripheral attention.
```

Familias:

```text
TRACKING
SACCADE
PURSUIT
PERIPHERAL
```

No decir que estas tres familias son la misma cosa.

La web debe dejar claro:

```text
Different content.
Shared production philosophy.
```

---

# 17. CHALLENGE SECTION

Título:

```text
NINE CHALLENGES.
ONE ENGINE.
```

Mostrar una grid 3×3 en desktop.

Cards:

### CHALLENGE_001

```text
KEY
v1.0
```

### CHALLENGE_002

```text
PARKING
v1.0
```

### CHALLENGE_003

```text
PILOT
v2.0
```

### CHALLENGE_004

```text
PARKING V2
v2.0
```

### CHALLENGE_005

```text
HIT
v1.0
```

### CHALLENGE_006

```text
CATCH
```

### CHALLENGE_007

```text
FIND
```

### CHALLENGE_008

```text
CHOOSE
```

### CHALLENGE_009

```text
COUNT
```

En cada card mostrar metadata:

```text
MECHANIC
ASSET FAMILY
VERSION
STATUS
```

Cuando no exista información explícita:

```text
UNKNOWN
```

Nunca inventar una familia.

---

# 18. CHALLENGE ASSET FAMILIES

Título:

```text
ASSETS ARE DATA.
NOT DECORATION.
```

Copy:

```text
Reusable assets are represented declaratively so visual identity can evolve without rewriting the mechanics.

Identity, family, role and provenance remain separate.
```

Mostrar dos familias explícitas actuales:

```text
fam_001
```

asociada a:

```text
CHALLENGE_001
CHALLENGE_003
```

y:

```text
fam_garage_01
```

asociada a:

```text
CHALLENGE_002
CHALLENGE_004
```

Mostrar las otras cinco como:

```text
FAMILY UNKNOWN
```

y explicar:

```text
UNKNOWN is not a bug.
It is an evidence state.
```

Importante:

No presentar UNKNOWN como “error”.

---

# 19. CROSS-FAMILY REUSE

Crear un pequeño bloque técnico.

Título:

```text
REUSE WITHOUT COLLAPSE.
```

Mostrar:

```text
CROSS-FAMILY REUSE
1
```

Texto:

```text
An asset can legitimately be reused across families.

Shared assets do not automatically become the same family.

Identity is preserved.
Reuse is declared.
Evidence remains traceable.
```

Esto es importante porque forma parte del diseño de C11-D.

---

# 20. VISUAL LOOPS

Título:

```text
PROCEDURAL WORLDS.
```

Mostrar las cinco familias como cinco grandes panels.

### GEOMETRIC WAVES

Visual conceptual:

* ondas;
* líneas;
* campos matemáticos.

### FRACTAL BLOOM

Visual:

* fractales;
* expansión;
* simetría.

### SACRED SYMMETRY

Visual:

* radial symmetry;
* kaleidoscopic structures;
* controlled clipping.

### LIVING PARTICLES

Visual:

* partículas;
* trayectoria;
* grid tipo Tron muy sutil.

### INVISIBLE FORCES

Visual:

* campos vectoriales;
* partículas;
* fuerzas invisibles representadas mediante trayectorias.

No usar imágenes externas.

Crear estos visuales con SVG/CSS/canvas procedural.

---

# 21. VISUAL DRILLS

Título:

```text
MOTION WITH INTENT.
```

Mostrar:

```text
TRACKING
SACCADE
PURSUIT
PERIPHERAL
```

Explicar:

```text
Visual Drills turn motion into attention mechanics.

The point is not simply movement.
The point is controlled perceptual behavior.
```

Añadir pequeños indicadores:

```text
TIMING
TRAJECTORY
FIXATION
SACCADE
PERIPHERAL FIELD
```

No afirmar que estos elementos son simulación gameplay.

---

# 22. DETERMINISM

Esta sección debe ser visualmente importante.

Título:

```text
SAME SEED.
SAME TRUTH.
```

Mostrar una comparación:

```text
SEED
12345

RUN A
✓

RUN B
✓

RESULT
IDENTICAL STRUCTURAL OUTPUT
```

Después:

```text
SEED
314159

RUN A
✓

RUN B
✓
```

Explicación:

```text
Determinism is not a visual trick.

It is the foundation that lets the engine reproduce, inspect, QA and deliver the same underlying result reliably.
```

Mostrar una línea:

```text
STRUCTURAL RNG
      ≠
MUSIC RNG
      ≠
PRESENTATION STATE
```

Texto:

```text
Randomness must be separated by responsibility.
```

No afirmar que D3 musical ya está implementado; esta parte debe marcar la arquitectura objetivo cuando corresponda.

---

# 23. PROVENANCE

Título:

```text
EVERY ARTIFACT LEAVES A TRACE.
```

Mostrar una tarjeta metadata:

```text
CHALLENGE_ID
CHALLENGE_001

MECHANIC
KEY

VERSION
1.0

SEED
12345

ASSET_FAMILY
fam_001

PROFILE
REVIEW_720

SOURCE_REV
C11-D

STATUS
DETERMINISTIC
```

Añadir:

```text
PROVENANCE
```

y explicar:

```text
The goal is not merely to generate a video.

The goal is to know how that video was generated.
```

---

# 24. AUDIO / MUSIC

Título:

```text
SOUND SHOULD BELONG TO THE SYSTEM.
```

Explicar que la arquitectura musical está evolucionando hacia una pipeline procedural compartida.

Copy:

```text
Music is treated as a production layer, not as an isolated soundtrack file.

The architecture is designed around deterministic generation with separate control over:
```

Mostrar seis elementos:

```text
TIMBRE
HARMONY
RHYTHM
MOTIF
TEXTURE
SPATIAL
```

Después:

```text
STYLE PROFILE
```

Mostrar:

```text
CHALLENGE
8-BIT / CHiPTUNE
```

pero marcarlo:

```text
PLANNED STYLE PROFILE
```

No afirmar que ya está implementado.

Explicar:

```text
The future Challenge sound identity is 8-bit/chiptune.

The generation process itself should remain shared.

Style changes.
Pipeline stays.
```

Y añadir una pequeña frase:

```text
Visual Loops and Visual Drills keep their existing behavior.
Challenge gets a style profile, not a duplicated music engine.
```

---

# 25. C11-C → C11-D

Crear una sección narrativa muy visual.

Título:

```text
FROM VISUAL PROTOTYPES
TO PRODUCTION SYSTEM.
```

Timeline horizontal:

```text
C11-A / C11-B
CHALLENGE ORIGINS
        ↓
C11-C
VISUAL PRODUCTION MATURITY
        ↓
C11-D
NORMALIZATION
        ↓
UNIFIED PRODUCTION PIPELINE
```

Explicar:

### C11-A / C11-B

```text
Recovered challenge mechanics and historical content.
```

### C11-C

```text
Mature visual loops, drills, social presentation and production workflows.
```

### C11-D

```text
Bring the lessons together without changing gameplay truth.
```

### Final target

```text
A stronger, declarative, reproducible Challenge production architecture.
```

---

# 26. ROADMAP

Título:

```text
THE ROAD TO PRODUCTION.
```

Crear timeline.

## D0

```text
BASELINE
INVENTORY
CHALLENGE RECOVERY
```

Estado:

```text
CLOSED
```

## D1

```text
VISUAL / EDITORIAL NORMALIZATION
LAYOUT
PRESENTATION
```

Estado:

```text
CLOSED
```

## D2

```text
DECLARATIVE ASSET FAMILIES
ROLE EVIDENCE
CANONICAL BINDING
```

Estado:

```text
CLOSED
```

## D3

```text
PROCEDURAL MUSIC V5
```

Estado:

```text
NEXT
```

## D4

```text
PRODUCTION REQUEST
PERSONALIZATION
GUI / CLI PARITY
```

Estado:

```text
PLANNED
```

## D5

```text
ARTIFACT TOPOLOGY
PROVENANCE
```

## D6

```text
SEED REGISTRY
GOVERNANCE
```

## D7

```text
CHALLENGE PRODUCTION MATRIX
CATALOG
```

## D8

```text
MEDIA QA
RELEASE PIPELINE
```

## D9

```text
SUITE
PRODUCER
MAINTENANCE
CATALOG / CONFIG
```

## D10

```text
NEW MECHANICS
```

Nota visual:

D10 debe aparecer deliberadamente al final.

Texto:

```text
New mechanics come last.

Production robustness comes first.
```

---

# 27. ENGINEERING PRINCIPLES

Título:

```text
BUILT AROUND CONSTRAINTS.
```

Crear seis grandes principios:

### 01 — DETERMINISTIC

```text
Same inputs.
Same structural result.
```

### 02 — DECLARATIVE

```text
Configuration should describe the system.
```

### 03 — SEPARATED

```text
Simulation truth stays isolated from presentation.
```

### 04 — REUSABLE

```text
One capability should not become three duplicated pipelines.
```

### 05 — TRACEABLE

```text
Every generated artifact should have a lineage.
```

### 06 — FROZEN WHEN CERTIFIED

```text
Stable contracts stay stable until evidence justifies change.
```

---

# 28. FROZEN BASELINE

Crear una sección técnica discreta.

Título:

```text
REFERENCE BUILD
```

Mostrar:

```text
C11-C
2.19.12
FROZEN
```

Subline:

```text
IMMUTABLE REFERENCE BASELINE
```

No mostrar rutas locales de Windows.

Mostrar solo fingerprints técnicos, si resulta visualmente adecuado:

```text
ZIP SHA-256
D85425CF18C5211C8497574F4FC66202D613EACC0EC14CD4E2FEF0B24F634A32
```

```text
TREE SHA-256
2D39B7B923B42CDC6647A4D25493B75023CDD19CEE18214BBDE1FDD295B8F256
```

Si mostrar hashes completos hace la sección demasiado pesada, utilizar un botón:

```text
VIEW BUILD FINGERPRINTS
```

abrir modal técnico.

No inventar otros hashes.

---

# 29. CURRENT SYSTEM STATUS

Crear una especie de terminal visual.

Título:

```text
SYSTEM / CURRENT STATE
```

Contenido conceptual:

```text
ENGINE
CHALLENGE ENGINE

BRANCH
C11-D

C11-C
FROZEN / 2.19.12

D0
CLOSED / PASS

D1
CLOSED

D2
CLOSED

D3
NEXT

RUNTIME
DETERMINISTIC

PRESENTATION
DECLARATIVE

ASSETS
EVIDENCE-BACKED

PROVENANCE
ENABLED BY DESIGN
```

Importante:

No hacer pasar esta interfaz por una consola real del engine.

Etiquetar:

```text
PROJECT STATUS
```

---

# 30. TECHNICAL PHILOSOPHY

Título:

```text
THE HARD PART IS NOT RENDERING.
```

Texto grande:

```text
The hard part is making the entire production chain predictable.
```

Después:

```text
Simulation.
Presentation.
Assets.
Audio.
Seeds.
Profiles.
Delivery.
QA.
Provenance.
```

Y cerrar:

```text
Challenge Engine is being built as a system of contracts.
Not a pile of render scripts.
```

---

# 31. FINAL CTA

Crear una sección final muy visual.

Fondo con una visual procedural lenta.

H1:

```text
MAKE EVERY FRAME
COUNT.
```

Subheadline:

```text
A deterministic engine for challenge-driven audiovisual systems.
```

CTA:

```text
ENTER THE LAB
```

Segundo CTA:

```text
READ THE ARCHITECTURE
```

Pequeña metadata:

```text
CHALLENGE ENGINE
C11-D
PROCEDURAL VIDEO SYSTEM
```

---

# 32. FOOTER

Footer minimalista.

Logo textual:

```text
CHALLENGE ENGINE
```

Subtext:

```text
PROCEDURAL VIDEO SYSTEM
```

Links:

```text
SYSTEM
ARCHITECTURE
CONTENT
ROADMAP
STATUS
```

Pequeña línea:

```text
Built around deterministic simulation, declarative production and traceable audiovisual generation.
```

Añadir discretamente:

```text
LAB
```

y, cuando resulte apropiado:

```text
CIBERPUNK.ES / LAB
```

No convertir esto en la marca principal.

---

# 33. INTERACTIVIDAD

La web debe sentirse viva.

## Hover

Challenge cards:

* pequeño desplazamiento vertical;
* borde cyan;
* metadata aparece ligeramente;
* icono se desplaza.

Visual family cards:

* background procedural aumenta ligeramente su velocidad;
* aparecer una etiqueta técnica;
* glow muy sutil.

Architecture diagram:

* hover de cada layer resalta las conexiones relacionadas.

Roadmap:

* al pasar por cada checkpoint, expandir una descripción.

---

# 34. SCROLL ANIMATIONS

Usar Framer Motion.

Elementos deben aparecer:

```text
opacity 0 → 1
translateY 20 → 0
```

Duración:

```text
0.45 — 0.7s
```

Easing suave.

No usar animaciones de “reveal” demasiado lentas.

No animar absolutamente todos los elementos.

Mantener jerarquía.

---

# 35. PROCEDURAL BACKGROUNDS

Crear visuales procedurales ligeros.

Opciones:

* grid dinámico;
* wave field;
* moving dots;
* vector lines;
* radial symmetry;
* particle trails.

Cada sección puede tener su propia variante.

Pero todas deben mantener la misma dirección artística.

No repetir exactamente el mismo canvas en toda la página.

---

# 36. INTERACTIVE SEED CONTROL

Crear una pequeña interacción opcional en la sección Determinism.

UI:

```text
SEED
[ 12345 ]

REGENERATE
```

Al pulsar:

```text
314159
54321
7770001
998877
```

debe cambiar el “preview state” visual.

Pero debe quedar claramente entendido como:

```text
DEMO / VISUALIZATION
```

No llamar al engine real ni fingir que la web está ejecutando Challenge Engine.

---

# 37. RESPONSIVIDAD

Desktop:

Diseño editorial con mucho espacio.

Tablet:

Reducir grids.

Mobile:

Todo debe convertirse en una secuencia vertical.

Hero:

1 columna.

Architecture:

diagrama vertical.

Challenge cards:

1 columna o 2 columnas pequeñas.

Visual family panels:

1 columna.

Roadmap:

timeline vertical.

Navbar:

hamburger funcional.

No permitir overflow horizontal.

---

# 38. MOBILE PRIORITY

Esta web debe verse extraordinariamente bien en:

```text
390 × 844
```

y:

```text
430 × 932
```

El sistema es para vídeo vertical y social content, así que mobile no puede ser una adaptación secundaria.

Los números técnicos deben seguir siendo legibles.

Los diagramas deben simplificarse sin perder significado.

---

# 39. ACCESSIBILITY

Implementar:

* semantic HTML;
* keyboard navigation;
* visible focus;
* aria labels;
* suficiente contraste;
* reduced-motion support;
* no information communicated only through color.

Con:

```css
prefers-reduced-motion: reduce
```

reducir animaciones.

---

# 40. SEO

Title:

```text
Challenge Engine — Deterministic Procedural Video System
```

Meta description:

```text
Challenge Engine is a deterministic procedural video system for reproducible game challenges, visual loops, drills and scalable audiovisual production.
```

Keywords conceptuales:

```text
procedural video
deterministic video generation
challenge engine
procedural graphics
generative video
game challenge automation
motion systems
visual loops
visual drills
reproducible media
```

Open Graph title:

```text
Challenge Engine — Build Once. Generate Reproducibly.
```

Open Graph description:

```text
A deterministic audiovisual production system built around simulation truth, declarative presentation and traceable generation.
```

---

# 41. DESIGN SYSTEM COMPONENTS

Crear componentes reutilizables:

```text
<SectionHeader />
<StatusBadge />
<TechnicalLabel />
<MetricCard />
<ChallengeCard />
<FamilyCard />
<ArchitectureNode />
<ArchitectureConnection />
<RoadmapItem />
<SeedPanel />
<CodeLikePanel />
<GlowDivider />
<ProceduralCanvas />
```

No repetir HTML equivalente.

---

# 42. ICONOGRAPHY

Usar Lucide React.

Preferir:

```text
Play
Cpu
Layers
Workflow
Database
GitBranch
Sparkles
Volume2
ShieldCheck
Boxes
Activity
Hash
Route
Gauge
Code2
Terminal
```

No usar iconos demasiado grandes.

Icons deben funcionar como señales visuales, no como decoración excesiva.

---

# 43. DATA MODEL INTERNO DE LA WEB

Crear datos estáticos en estructuras TypeScript.

Ejemplo conceptual:

```ts
type Challenge = {
  id: string;
  name: string;
  version?: string;
  assetFamily?: string;
  status: string;
};
```

No hardcodear todos los cards directamente dentro del JSX.

Lo mismo para:

* visual loop families;
* drill families;
* roadmap;
* technical principles;
* architecture layers.

---

# 44. IMPORTANT DATA ACCURACY RULE

La web no puede inventar información.

Cuando un dato técnico no esté confirmado:

```text
UNKNOWN
```

Nunca sustituir UNKNOWN con una suposición.

Esto es especialmente importante para:

* asset family;
* asset role;
* version;
* provenance;
* historical data.

No inventar estadísticas de producción.

No decir:

```text
10,000 videos generated
```

si no existe esa evidencia.

No decir:

```text
AI-powered
```

como marketing genérico.

No decir:

```text
100% bug free
```

ni:

```text
production ready
```

si el estado real no lo demuestra.

---

# 45. DO NOT MAKE IT A FAKE SAAS DASHBOARD

La web no es:

```text
Pricing
Features
Customers
Testimonials
Login
Enterprise
```

No incluir:

* pricing;
* fake customer logos;
* testimonials inventados;
* fake graphs;
* fake users;
* fake revenue metrics;
* fake AI benchmark numbers.

Este proyecto debe presentarse como un **engineering / audiovisual lab**, no como un SaaS comercial ficticio.

---

# 46. DO NOT USE GENERIC AI VISUALS

No utilizar:

* Midjourney-like imagery;
* stock images;
* humanoids;
* generic gaming artwork;
* fake dashboards;
* generic 3D renders.

Todos los elementos visuales principales deben ser:

* CSS;
* SVG;
* Canvas;
* procedural.

El objetivo estético es que incluso sin conocer el proyecto el visitante piense:

> “Esto parece generado por el propio engine.”

---

# 47. VISUAL RELATION TO THE PROJECT

La web debe utilizar como lenguaje visual los principios artísticos del proyecto:

* dark non-black backgrounds;
* mathematical geometry;
* mobile-first composition;
* deterministic procedural patterns;
* contrasting data-driven palettes;
* premium motion;
* precise alignment;
* strong safe areas;
* no screensaver-like movement.

Las animaciones deben tener propósito.

No llenar toda la pantalla de partículas simplemente porque “queda tecnológico”.

---

# 48. PERFORMANCE

Priorizar:

* CSS transforms;
* opacity;
* requestAnimationFrame solo cuando sea necesario;
* lazy loading;
* code splitting;
* lightweight SVG;
* small canvas effects.

No mantener múltiples canvas pesados simultáneamente.

No crear partículas con miles de objetos DOM.

Objetivo:

```text
smooth 60fps interactions
```

en desktop moderno y experiencia sólida en mobile.

---

# 49. PAGE RHYTHM

La página debe alternar:

```text
BIG STATEMENT
↓
TECHNICAL DETAIL
↓
VISUAL EXPERIENCE
↓
DATA
↓
NARRATIVE
↓
TECHNICAL DETAIL
```

No hacer 12 grids consecutivas.

Usar:

* espacios grandes;
* líneas;
* divisores;
* cambios sutiles de surface;
* diagramas;
* visualizaciones.

La página tiene que sentirse editorial.

---

# 50. COPYWRITING STYLE

El lenguaje debe ser:

* técnico;
* seguro;
* sobrio;
* corto;
* preciso.

No utilizar frases de startup como:

```text
Revolutionize your workflow.
Unlock your potential.
Next-generation AI platform.
Game-changing technology.
```

Evitar exageraciones.

La voz debe sonar como alguien que ha construido el sistema.

Preferir:

```text
Separate truth from presentation.
```

en lugar de:

```text
Revolutionize your media workflow.
```

Preferir:

```text
Determinism makes production inspectable.
```

en lugar de:

```text
Experience the future of video.
```

---

# 51. MICRO COPY SYSTEM

Pequeñas etiquetas recurrentes:

```text
C11-D
PROCEDURAL
DETERMINISTIC
DECLARATIVE
EVIDENCE-BACKED
FROZEN
ACTIVE
NEXT
UNKNOWN
TRACEABLE
REUSABLE
```

Usarlas como un lenguaje visual coherente.

---

# 52. BRAND SIGNATURE

Crear una pequeña marca gráfica basada en:

```text
CE
```

o:

```text
C•
E
```

pero evitar logotipos complejos.

El logo puede ser tipográfico.

La identidad debe poder funcionar únicamente con:

```text
CHALLENGE ENGINE
```

y una línea cyan.

---

# 53. OPTIONAL “LAB MODE”

Crear una interacción discreta:

Botón:

```text
LAB MODE
```

Cuando se activa:

* aparecen grid lines;
* labels técnicos;
* coordenadas;
* pequeñas líneas de debug;
* metadata;
* seed values.

Debe ser puramente visual.

No alterar el contenido.

Puede funcionar como una Easter Egg elegante.

---

# 54. FINAL UX PRINCIPLE

La web debe responder visualmente a esta jerarquía:

```text
WHY
↓
WHAT
↓
HOW
↓
WHAT EXISTS
↓
HOW IT EVOLVES
↓
WHY IT MATTERS
```

El usuario debe entender primero el proyecto, luego la arquitectura, luego las familias y finalmente el roadmap.

---

# 55. IMPLEMENTATION ORDER IN LOVABLE

Construye en este orden:

### STEP 1

Design system.

### STEP 2

Navbar + Hero.

### STEP 3

Status strip.

### STEP 4

Architecture.

### STEP 5

Content families.

### STEP 6

Challenges.

### STEP 7

Determinism / Provenance.

### STEP 8

Audio.

### STEP 9

Roadmap.

### STEP 10

Responsive + accessibility.

### STEP 11

Performance optimization.

### STEP 12

Final visual polish.

No generar toda la web con contenido placeholder y luego intentar arreglarla.

El contenido anterior es el contenido base real.

---

# 56. LOVABLE ACCEPTANCE CRITERIA

Considera la implementación correcta solamente si:

## Visual

* Dark non-black theme.
* No generic SaaS appearance.
* No generic AI imagery.
* Procedural visuals coherent with Challenge Engine.
* Premium typography.
* Strong information hierarchy.
* Good mobile experience.

## Technical

* React + TypeScript.
* Tailwind.
* shadcn/ui.
* Lucide.
* Framer Motion.
* Reusable components.
* Responsive.
* Accessible.

## Content

La web debe explicar correctamente:

```text
Challenge Engine
C11-A / C11-B
C11-C
C11-D
Challenges
Visual Loops
Visual Drills
Determinism
Presentation
Assets
Audio
Provenance
Roadmap
```

## Accuracy

No inventar:

* asset families;
* versions;
* production counts;
* generated video counts;
* performance figures;
* users;
* business metrics.

## Architecture

Debe quedar clarísimo:

```text
Simulation Truth
        ↓
Presentation
        ↓
Audio
        ↓
Delivery
        ↓
Provenance
```

pero Audio/Provenance pueden evolucionar como capas de producción sin alterar la verdad de simulación.

---

# 57. MOST IMPORTANT PRODUCT MESSAGE

La web completa debe terminar transmitiendo una idea:

> **Challenge Engine is an audiovisual production architecture where gameplay truth stays deterministic, presentation stays reusable, assets stay declarative, and generated media stays traceable.**

Y una segunda idea:

> **C11-D is not rebuilding the engine. It is normalizing how the engine produces content.**

Y una tercera:

> **Visual identity can change without changing gameplay truth.**

---

# 58. FINAL DESIGN CHECK BEFORE SUBMITTING

Antes de considerar terminada la web, revisa mentalmente:

```text
¿Parece una plataforma SaaS genérica?
→ NO

¿Parece una web de IA?
→ NO

¿Parece un videojuego infantil?
→ NO

¿Parece una instalación de laboratorio procedural?
→ YES

¿Los visuales parecen pertenecer al proyecto?
→ YES

¿Se entiende Challenge vs Visual Loop vs Visual Drill?
→ YES

¿Se entiende C11-C → C11-D?
→ YES

¿La determinidad tiene protagonismo?
→ YES

¿Assets / roles / provenance aparecen como conceptos de ingeniería?
→ YES

¿UNKNOWN se trata correctamente como estado de evidencia?
→ YES

¿La web deja claro que D3 musical es arquitectura futura y no una funcionalidad ya certificada?
→ YES

¿Mobile funciona como experiencia principal?
→ YES

¿Los textos parecen escritos por un ingeniero del sistema y no por un generador de marketing?
→ YES
```

# 59. FINAL LOVABLE INSTRUCTION

No simplifiques el concepto para hacerlo parecer una startup.

No sustituyas la arquitectura por marketing.

No elimines detalles técnicos para “hacerlo más accesible”.

La web tiene que ser accesible, pero también tiene que dejar claro que detrás existe una arquitectura real.

Quiero que el resultado final se sienta como:

**a living technical showcase of a procedural audiovisual engine.**

No como una plantilla.

No como un portfolio.

No como una landing SaaS.

**Como Challenge Engine.**

Este prompt ya deja a Lovable con una dirección bastante cerrada: **identidad visual propia, arquitectura real, datos actuales sin inventar y espacio para que C11-D siga evolucionando sin que la web tenga que rehacerse**.
