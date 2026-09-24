# C11-C STUDIO — MASTER SPECIFICATION
## Especificación maestra de producto, UX, arquitectura y operación
### Proyecto: ChallengeEngineV01_STATELESS / C11-C Visual Loops
### Backend de referencia: C11-C v2.1.4
### Estado: DOCUMENTO MAESTRO PARA IMPLEMENTACIÓN FUTURA

---

## 0. PROPÓSITO DEL DOCUMENTO

Este documento define la aplicación Windows que en adelante se denominará **C11-C Studio**.

C11-C Studio será una aplicación de escritorio para operar el sistema de generación de Visual Loops C11-C sin necesidad de memorizar decenas de comandos PowerShell, manteniendo al mismo tiempo la reproducibilidad determinista, la trazabilidad de cada producto, la separación estricta entre experimentación y producción y la protección del núcleo congelado de ChallengeEngineV01_STATELESS.

Este documento está escrito para un programador que no debe necesitar conocer la historia completa de las conversaciones anteriores. La aplicación debe poder desarrollarse siguiendo esta especificación y leyendo el repositorio real como fuente de verdad operativa.

La aplicación es **frontend/orquestador**, no un nuevo motor gráfico. No debe duplicar ni reimplementar la matemática artística o de render existente cuando ésta ya exista en el backend.

Principio principal:

> **C11-C Studio controla herramientas canónicas, observa resultados y protege la trazabilidad; no reinventa la lógica del generador.**

---

# 1. CONTEXTO DEL PROYECTO

## 1.1 Proyecto raíz

Repositorio:

```text
ChallengeEngineV01_STATELESS
```

C11-C es la capa de **Visual Loops** y está separada de la simulación determinista de retos y del núcleo C11-B congelado.

## 1.2 C11-B está congelado

El núcleo C11-B es CLOSED / CERTIFIED / FROZEN.

C11-C Studio no debe modificar:

- matemáticas de simulación;
- RNG de simulación;
- `SimulationResult`;
- winning frame;
- `close_calls`;
- contratos estructurales C11-B;
- geometría lógica del frame base 540×960;
- contratos C7 de audio;
- contratos C9 de authoring;
- cualquier componente que pertenezca al núcleo congelado salvo que exista una apertura formal de alcance.

El GUI debe trabajar encima del toolchain C11-C actual.

## 1.3 Resolución de entrega actual

La captura social/productiva actual es:

```text
720 × 1280
9:16
30 FPS
```

El layout lógico histórico C11-B continúa basado en 540×960 y C11-C aplica la estrategia de captura/escala correspondiente. El GUI debe distinguir claramente entre:

- **logical canvas**;
- **delivery resolution**.

Nunca debe presentar 540×960 como resolución final de producción actual.

## 1.4 Duración actual

Baseline de trabajo vigente:

```text
18.00 s
540 frames
30 FPS
```

Esto NO debe considerarse una decisión arquitectónica definitiva para todas las futuras obras.

La futura duración variable por geometría/semilla/gramática está expresamente fuera del alcance de la primera versión de C11-C Studio, aunque el modelo de datos debe estar preparado para admitirla.

---

# 2. PRINCIPIOS DE DISEÑO

1. **Determinismo.** Una familia + seed + versión de backend + configuración equivalente debe ser reproducible.
2. **Trazabilidad.** Cada producto debe poder responder a “qué, quién, cuándo, con qué seed, con qué versión y con qué parámetros se generó”.
3. **Separación.** Prototype, Review y Production son estados/entornos distintos.
4. **Protección.** Production no se elimina mediante operaciones de limpieza de review.
5. **No duplicación.** El GUI no debe copiar lógica que ya reside en PowerShell/Python/Godot.
6. **Fail fast.** Un error de render, validación o integridad debe detener la operación correspondiente.
7. **UX operativa.** El usuario debe poder hacer las operaciones frecuentes sin consola.
8. **Transparencia técnica.** Siempre debe existir acceso al log real, comando reproducible y metadata.
9. **Auditoría.** No esconder errores bajo una simple marca roja; mostrar causa y artefacto afectado.
10. **No destructivo por defecto.** Las operaciones destructivas requieren confirmación explícita.

---

# 3. TECNOLOGÍA RECOMENDADA

## 3.1 Stack

Recomendado:

```text
Python 3.13+
PySide6 / Qt 6
```

El backend seguirá utilizando lo que actualmente use C11-C:

```text
PowerShell
Godot 4.7.1
Python
FFmpeg / FFprobe
```

No se debe sustituir Godot por Qt.

## 3.2 Arquitectura

```text
┌────────────────────────────────────────────────────┐
│                    C11-C STUDIO                    │
│                 PySide6 / Qt 6                     │
├────────────────────────────────────────────────────┤
│ UI                                                 │
│ ViewModels / State                                 │
│ Job Manager                                        │
│ Command Builder                                    │
│ Artifact Registry                                  │
│ Log Parser                                         │
│ Validation Layer                                   │
├────────────────────────────────────────────────────┤
│ Canonical Tool Adapter                             │
├────────────────────────────────────────────────────┤
│ PowerShell / Python / Godot / FFmpeg / FFprobe    │
├────────────────────────────────────────────────────┤
│ C11-C repository                                   │
└────────────────────────────────────────────────────┘
```

## 3.3 Regla de oro de arquitectura

La aplicación debe poder ejecutar una operación desde GUI y producir el mismo resultado que produciría el comando canónico equivalente desde consola.

El botón del GUI no debe tener una implementación paralela del proceso.

Ejemplo:

```text
Botón “Producir 25”
        ↓
Command Builder
        ↓
run_c11c_production_25.ps1
        ↓
Godot/Python/FFmpeg
```

No:

```text
Botón “Producir 25”
        ↓
Python reimplementa internamente el render
```

---

# 4. ESTRUCTURA DE LA APLICACIÓN

## 4.1 Navegación principal

La aplicación debe tener navegación lateral persistente:

```text
DASHBOARD
REVIEW LAB
PRODUCTION
FAMILIES
SEEDS
ARTIFACTS
LOGS
VALIDATION
SETTINGS
ABOUT / DIAGNOSTICS
```

En una versión compacta puede utilizar icono + texto.

## 4.2 Barra superior

Debe mostrar siempre:

```text
C11-C Studio
Backend: C11-C 2.1.4
Godot: detected / missing / version
FFmpeg: detected / missing
Project: path
Environment status
```

Nunca ocultar silenciosamente una dependencia ausente.

---

# 5. DASHBOARD

El dashboard debe ser el punto de entrada diario.

## 5.1 Tarjetas de estado

```text
BACKEND
C11-C 2.1.4
READY

GODOT
4.7.1
READY

DELIVERY
720×1280 · 30 FPS · 18s

FAMILIES
5

PRODUCTION PRODUCTS
N

REVIEW CORPUS
N
```

## 5.2 Acciones rápidas

```text
[ VALIDATE ENVIRONMENT ]
[ NEW 5×5 REVIEW ]
[ PRODUCE 5×5 FINAL ]
[ PRODUCE SINGLE ]
[ OPEN PRODUCTION ]
[ OPEN REVIEW ]
```

## 5.3 Actividad reciente

Mostrar últimos jobs:

- fecha/hora;
- tipo;
- familia;
- seed(s);
- resultado;
- duración;
- ruta;
- botón “open”.

---

# 6. MODELO DE DATOS DEL GUI

## 6.1 ProjectContext

```text
ProjectContext
- project_root
- backend_version
- godot_version
- ffmpeg_path
- ffprobe_path
- delivery_width
- delivery_height
- fps
- default_duration
- repository_state
```

## 6.2 Family

```text
Family
- id
- internal_name
- artistic_name
- short_description
- visual_metaphor
- engine_script_path
- shader_path
- scene_path
- launcher_path
- palette_bank
- grammar_definition
- supported_parameters
- default_duration
- loop_contract
- audio_profile
```

## 6.3 Seed

```text
SeedRecord
- seed
- source: RANDOM | MANUAL | CORPUS | REPRODUCTION
- created_at
- batch_id
- used_in_families[]
```

## 6.4 VariationProfile

El GUI debe poder mostrar parámetros efectivos sin inventarlos.

Ejemplo conceptual:

```text
VariationProfile
- palette
- grammar
- scale
- phase
- frequency
- amplitude
- density
- flow
- trace_count
- pulse_speed
- symmetry_order
- gear_ratio
- family_specific_parameters
```

No todos los campos existen en todas las familias. La UI debe ocultar campos no aplicables.

## 6.5 Job

```text
Job
- id
- job_type
- family
- seed(s)
- started_at
- finished_at
- state
- command
- exit_code
- log_path
- outputs[]
- errors[]
```

## 6.6 Product

```text
Product
- product_id
- family
- artistic_family
- seed
- version
- created_at
- status
- mp4
- gif
- wav
- social_txt
- authoring_json
- manifest_json
- ffprobe_json
- godot_log
- production_manifest
- product_txt
- reproduction_command
- sha256
```

---

# 7. FAMILIAS DE VISUAL LOOPS

Actualmente existen exactamente cinco familias.

## 7.1 Geometric Waves

Código interno:

```text
geometric
```

Familia:

```text
c11c_geometric_waves_v1
```

Nombre artístico:

```text
Geometric Waves
```

Concepto:

- harmonic loom;
- liquid architecture;
- clean vector lines;
- cyan / magenta / white;
- wave interference;
- tension / release;
- deterministic geometry.

Ejes de variación conocidos:

- polygon/order selection;
- rational frequency;
- phase;
- amplitudes;
- layer offsets;
- palette anchor;
- scale relationships;
- wave/morph values.

Header típico contiene variables efectivas, por ejemplo:

```text
<GEOMETRIC VARIANT> | WAVE x.x | MORPH x.xx
```

El GUI debe presentar la familia como **Geometric Waves** y permitir ver el nombre técnico `geometric` cuando esté activo el modo técnico.

### Subfamilias / gramáticas

La arquitectura del GUI debe soportar una lista dinámica de gramáticas. No debe codificar una lista cerrada si el backend puede crecer.

Cada grammar debe identificarse por un `grammar_id` proporcionado por backend/manifest.

---

## 7.2 Fractal Bloom

Código interno:

```text
fractal
```

Familia:

```text
c11c_fractal_bloom_v1
```

Nombre artístico:

```text
Fractal Bloom
```

Concepto:

- mycelium;
- neural synapses;
- microscopic infinite universe;
- branching filaments;
- indigo / violet / cyan;
- radial nucleus;
- controlled zoom;
- Julia-set based structure.

Ecuación central usada:

```text
z(n+1) = z(n)^2 + c
```

Mecanismos conocidos:

- seed-derived Julia constant;
- orbit traps;
- domain warp;
- depth layers;
- periodic zoom.

### Gramáticas conocidas

Actualmente deben reconocerse al menos estas identidades históricas de Fractal Bloom:

```text
RADIAL BLOOM
DENDRITIC TUNNEL
SPIRAL FRACTAL
FRACTAL FILIGREE
NESTED WORLDS
```

El GUI las debe mostrar como gramáticas/artistic modes cuando el manifest del backend las identifique.

El campo `grammar` debe permitir filtrar y comparar variaciones.

---

## 7.3 Sacred Symmetry

Código interno histórico:

```text
kaleidoscope
```

Familia:

```text
c11c_sacred_symmetry_v1
```

Nombre artístico:

```text
Sacred Symmetry
```

Concepto:

- generative astrolabe;
- celestial mechanism;
- radial symmetry;
- concentric rings;
- gold / amber / copper;
- clockwork / origami motion;
- mechanical precision.

Ejes de variación conocidos:

- symmetry order `N`;
- gear relationships;
- radial layers;
- rotation phases;
- ring relationships;
- metallic palette modes.

Header típico incluye:

```text
<VARIANT> | N=x | GEAR x:y
```

---

## 7.4 Living Particles

Código interno histórico:

```text
particle_flow
```

Familia:

```text
c11c_living_particles_v1
```

Nombre artístico:

```text
Living Particles
```

Concepto:

- magnetic dust;
- ink in fluid;
- attractors;
- eddies;
- trails;
- emerald / sea-green / turquoise.

Ejes conocidos:

- density;
- flow;
- particle count/density;
- collision/interactions;
- attractor relationships;
- trails;
- palette mode.

Header típico:

```text
<LIVING VARIANT> | DENSITY x.xx | FLOW x.xx
```

---

## 7.5 Invisible Forces

Código interno histórico:

```text
vector_field
```

Familia:

```text
c11c_invisible_forces_v1
```

Nombre artístico:

```text
Invisible Forces
```

Concepto:

- solar wind;
- gravitational topography;
- field traces;
- flow lines;
- radar/pulse energy;
- crimson / orange / yellow family.

Ejes conocidos:

- trace count;
- pulse speed;
- field configuration;
- phase;
- palette mode.

Header de referencia:

```text
TOPOGRAPHIC_BASIN | xx TRACES | PULSE x.xx
NO VES LA FUERZA, SOLO SU RASTRO
```

---

# 8. FAMILY EXPLORER

Pantalla dedicada a las familias.

Cada tarjeta debe mostrar:

```text
[Preview]
GEOMETRIC WAVES
geometric

GRAMMAR: ...
PALETTE: ...
PARAMETERS: ...
AUDIO: ...
LOOP: ...

[ GENERATE ]
[ REVIEW ]
[ OPEN FOLDER ]
```

## 8.1 Vista de comparación

Debe permitir seleccionar entre 2 y 5 familias y observar:

- preview;
- seed;
- grammar;
- palette;
- duration;
- resolution;
- audio;
- state.

---

# 9. SEEDS

La seed es un identificador de reproducción, no un simple número para rellenar un campo.

## 9.1 Modos

```text
RANDOM
MANUAL
REPRODUCE
CORPUS
PRODUCTION BANK
```

## 9.2 Random

Al seleccionar RANDOM, generar N seeds enteras válidas.

Para una review 5×5:

```text
5 unique seeds
×
5 families
```

Las mismas cinco seeds deben utilizarse en las cinco familias para facilitar comparación cruzada.

## 9.3 Manual

Entrada de seed de tipo entero.

Validar rango admitido por backend.

## 9.4 Reproduce

El usuario puede seleccionar un producto existente y pulsar:

```text
[ REPRODUCE EXACTLY ]
```

La aplicación recupera:

- family;
- seed;
- relevant version;
- manifest;
- command.

No debe reconstruir parámetros si están disponibles en el manifest.

## 9.5 Copy command

Siempre ofrecer:

```text
COPY REPRODUCTION COMMAND
```

Ejemplo conceptual:

```powershell
.\tools\prototypes\c11c_<family>\run_prototype.ps1 -Seed <seed>
```

Para producción utilizar el comando canónico de producción y no el de prototipo.

---

# 10. REVIEW LAB

Ésta es la zona de dirección de arte.

## 10.1 Modos

```text
QUICK REVIEW
5×5 ART DIRECTION REVIEW
CUSTOM CORPUS
SINGLE FAMILY REVIEW
GRAMMAR COVERAGE
```

## 10.2 5×5 Art Direction Review

Acción principal:

```text
NEW 5×5 REVIEW
```

Configuración:

```text
Families: [all 5]
Variations per family: 5
Seed mode: Random / Manual
Audio: ON/OFF
Resolution: 720×1280
FPS: 30
Duration: current backend baseline
```

Resultado:

```text
25 renders
```

La UI debe mostrar progreso:

```text
Family 2 / 5
Seed 3 / 5
Overall 8 / 25
```

## 10.3 Review asset policy

Review assets son regenerables.

Debe existir un comando/acción:

```text
RESET REVIEW ASSETS
```

que solo afecte al workspace de review.

Nunca borrar:

```text
artifacts\production
artifacts\legacy
artifacts\qa
artifacts\regression
artifacts\releases
artifacts\tests
```

## 10.4 Review gallery

Mostrar thumbnails agrupados por familia.

Ejemplo:

```text
GEOMETRIC WAVES
┌──────┬──────┬──────┬──────┬──────┐
│ seed │ seed │ seed │ seed │ seed │
└──────┴──────┴──────┴──────┴──────┘
```

Acciones:

- play;
- open file;
- open folder;
- inspect metadata;
- compare;
- promote to production.

## 10.5 Comparison mode

Seleccionar 2–5 vídeos.

Mostrar:

- video preview;
- family;
- seed;
- grammar;
- palette;
- effective parameters;
- duration;
- status.

No alterar los vídeos desde el visor.

---

# 11. PRODUCTION

Production es una zona protegida.

## 11.1 Estados

Los jobs y productos deben tener estados separados.

### Job states

```text
QUEUED
RUNNING
VALIDATING
PACKAGING
COMPLETED
FAILED
CANCELLED
```

### Product states

```text
CANDIDATE
VALIDATED
PUBLISHED
REPLACEMENT_PENDING
REPLACED
FAILED
```

### Environment states

```text
READY
DEGRADED
BLOCKED
```

## 11.2 Producto individual

Formulario:

```text
Family
Seed
Audio
Footer
```

Mostrar resolución/fps/duración como configuración efectiva.

Acción:

```text
[ PRODUCE FINAL ]
```

## 11.3 Producción 5×5

Acción principal:

```text
PRODUCE 25 FINAL PRODUCTS
```

Por defecto:

```text
5 random unique seeds
5 families
25 products
Audio ON
Footer ON
720×1280
30 FPS
current duration baseline
```

Debe ejecutarse mediante el tool canónico actual.

## 11.4 Existing product protection

Antes de empezar:

```text
Existing destination check
```

Si uno o más productos ya existen:

```text
STOP BEFORE RENDER
```

No borrar nada automáticamente.

Solo permitir reemplazo mediante acción explícita:

```text
FORCE REPLACEMENT
```

La sustitución segura debe validar primero el nuevo producto.

---

# 12. PRODUCTION CATALOG

La aplicación debe tener un catálogo central de productos.

Columnas mínimas:

```text
Product
Family
Seed
Grammar
Palette
Date
Duration
Resolution
Audio
Status
Location
```

Acciones:

```text
PLAY
OPEN
OPEN FOLDER
COPY COMMAND
COPY PATH
SHOW MANIFEST
SHOW LOG
SHOW SOCIAL TEXT
VERIFY HASH
```

---

# 13. ARTIFACTS MANAGER

## 13.1 Clasificación

El GUI debe presentar la estructura conceptual:

```text
PRODUCTION        protected
REVIEW            regenerable
PROTOTYPES        experimental
QA                protected
REGRESSION        protected
RELEASES          protected
LEGACY            protected
TESTS             protected
SCRATCH           disposable
```

## 13.2 Regla principal

El cleaner no debe considerarse una función trivial de “borrar carpeta”.

Debe presentar antes del borrado:

```text
TARGETS
FILES
SIZE
PROTECTED ITEMS
```

## 13.3 Dry run

Siempre:

```text
PREVIEW CLEANUP
```

antes del borrado real.

## 13.4 Protección

Production debe aparecer visualmente bloqueada:

```text
🔒 PROTECTED
```

Ninguna operación de limpieza general debe incluirla.

---

# 14. LOG CENTER

## 14.1 Principio

Los logs reales nunca deben ocultarse.

La aplicación debe capturar stdout/stderr y conservar el fichero generado por backend.

## 14.2 Visor

Funciones:

- seguimiento en tiempo real;
- pausa de auto-scroll;
- búsqueda;
- copy;
- open file;
- filter INFO/WARN/ERROR;
- jump to error.

## 14.3 Parsing estructurado

Reconocer eventos conocidos como:

```text
MOVIE MAKER START
RESOLUTION
FPS
FRAME COUNT
AUDIO GENERATED
FFPROBE PASS
SOCIAL GENERATED
PRODUCTION PUBLISHED
```

Si el parser no reconoce una línea, conservarla como log libre.

Nunca descartar texto desconocido.

---

# 15. VALIDATION CENTER

Antes de cualquier operación masiva se debe poder ejecutar:

```text
VALIDATE POWERSHELL
VALIDATE DELIVERY CONFIG
CHECK GODOT
CHECK FFMPEG
CHECK FFPROBE
CHECK FAMILIES
CHECK CANONICAL TOOLS
```

Resultado visual:

```text
PASS
WARN
FAIL
```

## 15.1 Preflight

Debe comprobar al menos:

- proyecto encontrado;
- cinco familias presentes;
- launchers presentes;
- toolchain canónico presente;
- Godot detectado;
- versión compatible;
- FFmpeg disponible;
- FFprobe disponible;
- delivery resolution = 720×1280;
- FPS correcto;
- herramientas PowerShell parseables;
- producción separada de review;
- rutas de artifacts existentes o creables.

## 15.2 Validación del render

Para un producto final:

```text
Width = 720
Height = 1280
FPS = 30
Frames = expected count
Duration = expected duration
Audio = expected state
```

Y comprobar que el producto tiene un único MP4 canónico.

---

# 16. AUDIO

El GUI debe exponer audio de forma explícita.

```text
Audio: ON
```

Default:

```text
ON
```

Off:

```text
NoSound / Silent
```

El GUI debe mostrar:

```text
Audio profile
Sample rate
Channels
Duration
```

No debe alterar contratos C7.

La aplicación debe distinguir entre:

```text
audio enabled
audio disabled
```

Nunca debe interpretar un WAV intermedio abandonado como producto final.

---

# 17. EDITORIAL / HEADER / FOOTER

El GUI debe poder inspeccionar la composición editorial, no editarla arbitrariamente desde la primera versión.

## Header

Conceptualmente:

```text
Línea 1: factual/paramétrica
Línea 2: hook editorial
```

La línea 2 puede presentar la transición determinista:

```text
hook
→ scramble
→ family signature
→ scramble
→ hook
```

## Footer

Telemetría y datos, sin repetir la identidad de familia si ésta ya está en la cabecera.

Debe poder mostrarse:

- technobabble;
- seed;
- body resolution;
- duration;
- parameter data;
- deterministic signature.

## Colores

La UI debe poder leer y presentar la palette efectiva de la pieza.

Las letras y líneas editoriales pertenecen a la estética y no deben presumirse siempre blancas.

---

# 18. PALETTE EXPLORER

Pantalla para explorar colorways.

Mostrar:

```text
Family
Palette ID
Primary
Secondary
Highlight
Background
Color boost
```

La palette debe presentarse como datos del backend, no como una selección GUI que sustituya silenciosamente al perfil determinista.

Modo futuro:

```text
Palette preview
```

Modo producción inicial:

```text
read-only effective palette
```

---

# 19. GRAMMAR EXPLORER

El sistema de gramáticas debe ser dinámico.

La UI debe ser capaz de representar:

```text
Grammar ID
Display Name
Family
Parameters
Supported Seeds
Coverage
```

Para Fractal Bloom se soportan al menos:

```text
RADIAL BLOOM
DENDRITIC TUNNEL
SPIRAL FRACTAL
FRACTAL FILIGREE
NESTED WORLDS
```

Para las demás familias, si el backend define otras gramáticas, se cargan desde sus definiciones/manifest sin necesidad de recompilar la aplicación.

---

# 20. REPRODUCIBILITY VIEW

Pantalla especialmente importante.

Seleccionado un producto:

```text
PRODUCT
Family: Invisible Forces
Seed: 271828
Backend: C11-C 2.1.4
Resolution: 720×1280
FPS: 30
Duration: 18.00s
Audio: ON
Grammar: ...
Palette: ...
```

Botones:

```text
[ COPY REPRODUCTION COMMAND ]
[ OPEN MANIFEST ]
[ OPEN LOG ]
[ VERIFY OUTPUT ]
[ REPRODUCE ]
```

---

# 21. SOCIAL METADATA

Cada producto de producción debe mostrar y conservar:

```text
TITLE
DESCRIPTION
FAMILY
GRAMMAR
PALETTE
SEED
DURATION
FPS
FRAMES
LOOP CYCLES
LOOP CLOSED
AUDIO
BACKGROUND
HEADER
EDITORIAL TRANSITION
TECHNOBABBLE
HASHTAGS
REPRODUCTION COMMAND
MANIFEST
```

El GUI debe incluir:

```text
[ VIEW SOCIAL TEXT ]
[ COPY SOCIAL TEXT ]
[ OPEN SOCIAL FILE ]
```

---

# 22. ESTADOS VISUALES DEL GUI

## READY

Icono verde / estado normal.

## RUNNING

Mostrar:

- family;
- seed;
- stage;
- elapsed;
- current frame si está disponible.

## VALIDATING

Mostrar checks.

## PASS

Mostrar producto y rutas.

## FAIL

Mostrar:

```text
WHAT FAILED
WHY
LOG
COMMAND
ARTIFACTS
NEXT SAFE ACTION
```

Nunca sugerir borrar el proyecto para solucionar un fallo.

---

# 23. JOB MANAGER

El generador debe utilizar un gestor de jobs asíncrono.

Cada job debe correr fuera del hilo UI.

Tecnología recomendada:

```text
QProcess
```

o wrapper equivalente de Qt para procesos externos.

## Requisitos

- cancelar jobs cuando sea seguro;
- capturar stdout;
- capturar stderr;
- capturar exit code;
- guardar timestamps;
- mantener log;
- mostrar progreso parcial;
- evitar bloquear la ventana.

## Paralelismo

No ejecutar indiscriminadamente varias instancias de Godot si el backend no lo soporta.

Por defecto:

```text
1 render at a time
```

para asegurar estabilidad y trazabilidad.

---

# 24. COMMAND BUILDER

El GUI debe tener un componente central `CommandBuilder`.

Funciones:

```text
build_review_command()
build_production_command()
build_single_family_command()
build_reproduction_command()
build_validation_command()
build_cleanup_command()
```

El resto de la aplicación no debe ensamblar strings PowerShell manualmente.

Idealmente generar un objeto estructurado:

```text
CommandSpec
- executable
- arguments[]
- working_directory
- environment
- display_command
```

La UI muestra `display_command`, pero la ejecución utiliza argumentos estructurados cuando sea posible.

Esto evita los problemas históricos de:

- strings con separadores ambiguos;
- arrays tratados como positional arguments;
- `SwitchParameter` serializados incorrectamente;
- interpolaciones `$variable:`;
- llamadas anidadas con `powershell.exe -File` que alteran binding.

Regla:

> **No lanzar un PowerShell hijo para cada script PowerShell si el script puede ejecutarse directamente desde el proceso actual o mediante una llamada controlada.**

---

# 25. ERRORES QUE C11-C STUDIO DEBE IMPEDIR

La aplicación debe prevenir de forma activa los siguientes tipos de errores que ya han ocurrido históricamente:

1. resolución 540×960 en una entrega social actual;
2. pasar `720` y `1280` como dos argumentos a `--resolution`;
3. pasar `"True"` como string a un `SwitchParameter`;
4. pasar arrays de seeds como argumentos posicionales inesperados;
5. interpolar `$family:` en strings PowerShell;
6. comas finales inválidas en `param()`;
7. renderizar un shader con símbolos no declarados;
8. generar dos MP4 finales para la misma pieza;
9. dejar `_silent.mp4` como producto aparente;
10. validar todos los MP4 de la carpeta en lugar del candidato exacto;
11. borrar producción al limpiar review;
12. mezclar review y producción;
13. perder metadata por un BOM UTF-8;
14. ocultar el log real;
15. aceptar un producto aunque FFprobe falle;
16. sobrescribir un producto válido sin autorización explícita.

Estas condiciones deben formar parte de las pruebas automatizadas del GUI.

---

# 26. FILESYSTEM CONTRACT

## Repository

```text
ChallengeEngineV01_STATELESS\\
```

## Tools

```text
tools\\prototypes\\c11c_bulk\\
tools\\prototypes\\c11c_common\\
tools\\prototypes\\c11c_<family>\\
```

## Artifacts

```text
artifacts\\
├── production\\
│   └── audiovisual\\
├── prototypes\\
│   ├── c11c_geometric_waves_v1\\
│   ├── c11c_fractal_bloom_v1\\
│   ├── c11c_sacred_symmetry_v1\\
│   ├── c11c_living_particles_v1\\
│   ├── c11c_invisible_forces_v1\\
│   ├── c11c_review_assets\\
│   └── ...
├── legacy\\
├── qa\\
├── regression\\
├── releases\\
├── scratch\\
└── tests\\
```

La aplicación debe resolver todas las rutas desde `ProjectContext.project_root`.

Nunca usar rutas absolutas hardcoded del ordenador del desarrollador.

---

# 27. PRODUCTION DIRECTORY CONTRACT

Cada producto final debe tener un directorio estable, por ejemplo:

```text
artifacts\\production\\audiovisual\\
    c11c_invisible_forces_v1\\
        InvisibleForces_v1_seed_271828\\
            InvisibleForces_v1_seed_271828.mp4
            InvisibleForces_v1_seed_271828_social.txt
            InvisibleForces_v1_seed_271828_manifest.json
            InvisibleForces_v1_seed_271828_authoring.json
            InvisibleForces_v1_seed_271828_ffprobe.json
            InvisibleForces_v1_seed_271828_godot.log
            InvisibleForces_v1_seed_271828_music.wav
            production_manifest.json
            PRODUCT.txt
```

El producto final es inmutable por defecto.

---

# 28. REVIEW VS PRODUCTION

## Review

Objetivo:

```text
explorar
comparar
iterar
```

Puede sobrescribirse/regenerarse.

## Production

Objetivo:

```text
producto distribuible
```

Debe conservar:

- MP4;
- log;
- manifest;
- authoring;
- FFprobe;
- social text;
- metadata necesaria para reproducibilidad;
- hash cuando exista.

La UI debe hacer visualmente evidente la diferencia.

---

# 29. BATCH CONTROL

La aplicación debe tener una pantalla de batch.

Columnas:

```text
#
Family
Seed
Stage
Status
Progress
Output
```

Para 25 productos:

```text
01 Geometric  seed A   PASS
02 Geometric  seed B   PASS
...
25 Invisible  seed E  PASS
```

Debe permitir abrir directamente el error asociado a un job fallido.

---

# 30. PROMOTION REVIEW → PRODUCTION

Una pieza de review no se convierte en producto por copiar manualmente un MP4.

Acción:

```text
[ PROMOTE TO PRODUCTION ]
```

La aplicación debe:

1. localizar seed/family/metadata;
2. ejecutar producción canónica;
3. validar el producto final;
4. publicar;
5. registrar la promoción.

Nunca simplemente mover el archivo de review sin validación.

---

# 31. ART DIRECTION 2.0 SUPPORT

C11-C Studio debe estar preparada para la fase de Dirección de Arte 2.0.

No debe imponer todavía decisiones artísticas nuevas.

Debe permitir observar:

- familia;
- gramática;
- palette;
- parámetros;
- densidad visual;
- intensidad;
- movimiento;
- editorial treatment;
- audio;
- duración;
- comparación entre seeds.

## Herramientas futuras

```text
STYLE BOARD
VARIATION GRID
PARAMETER HEATMAP
PALETTE BOARD
GRAMMAR COVERAGE
FAMILY COMPARISON
SEED COMPARISON
```

Estas funciones pertenecen a una evolución posterior y no deben mezclarse con el motor.

---

# 32. DURACIÓN VARIABLE FUTURA

No implementar en la primera versión.

Pero el diseño debe admitir un futuro objeto:

```text
DurationProfile
- mode: FIXED | SHORT | MEDIUM | LONG | EXPLICIT
- seconds
- frame_count
- loop_cycles
- grammar_driver
```

Futura idea artística prevista:

```text
SHORT  → 11–13 s
MEDIUM → 16–20 s
LONG   → 24–30 s
```

Los valores anteriores son conceptuales, no un contrato actual.

La duración debe depender eventualmente de la geometría/gramática/seed de forma determinista, garantizando cierre de loop y sincronización audiovisual.

---

# 33. SETTINGS

## General

- project root;
- preferred video player;
- language;
- theme;
- auto-scroll logs;
- confirm destructive actions.

## Backend

- Godot executable;
- Python executable;
- FFmpeg executable;
- FFprobe executable.

## Delivery

Read-only unless backend contract is explicitly changed:

```text
720×1280
30 FPS
18s baseline
```

## Production

- production root;
- auto-open product after completion;
- hash verification;
- preserve intermediate media in prototype only.

---

# 34. SECURITY / SAFETY

Aunque sea una herramienta local, debe evitar:

- ejecutar comandos construidos desde texto arbitrario sin validación;
- permitir rutas fuera del repository sin confirmación;
- borrar carpetas protegidas;
- seguir symlinks/reparse points de forma peligrosa durante limpieza;
- ejecutar scripts de origen desconocido sin mostrar ruta.

Las operaciones destructivas deben utilizar allowlists de raíces permitidas.

# 35. PORTABILIDAD

El GUI debe funcionar en Windows 10/11 x64 como objetivo principal.

No asumir rutas del ordenador del desarrollador.

Ejemplo incorrecto:

```text
C:\Users\vinxe\Projects\...
```

Debe funcionar igualmente en:

```text
D:\Projects\...
E:\ChallengeEngine\...
```

La raíz del proyecto debe obtenerse mediante:

1. argumento CLI opcional;
2. selector de carpeta;
3. configuración persistida.

La aplicación debe validar que la carpeta seleccionada contiene señales razonables del repositorio, como `project.godot`, `tools\` y el árbol de C11-C.

---

# 36. CLI DEL PROPIO GUI

Aunque el producto principal sea gráfico, se recomienda que C11-C Studio disponga de un CLI fino para automatización:

```text
c11c-studio.exe --project <path>
c11c-studio.exe --validate
c11c-studio.exe --review-5x5
c11c-studio.exe --production-25
```

El CLI del GUI debe reutilizar las mismas capas internas que la interfaz gráfica.

No crear un tercer backend paralelo.

---

# 37. TESTING

## 37.1 Unit tests

Probar:

- `ProjectContext`;
- `CommandBuilder`;
- path resolver;
- seed generator;
- state machine;
- artifact classification;
- log parser;
- production guard;
- manifest parser;
- family discovery;
- grammar discovery.

## 37.2 Integration tests

Usar fixtures/mock para:

- launcher success;
- launcher failure;
- fake Godot;
- fake FFprobe;
- missing executable;
- malformed JSON;
- malformed output;
- cancellation.

## 37.3 Safety tests

Intentar limpiar explícitamente:

```text
production
qa
legacy
releases
regression
```

El GUI debe negarse.

## 37.4 Regression tests heredados

Representar expresamente estos fallos históricos:

```text
540×960 rejected for current delivery
720×1280 accepted
Invalid Godot --resolution rejected
SwitchParameter string misuse rejected
Seed array transport preserved
$family: interpolation issue absent
Trailing param comma absent
Shader undefined identifier surfaces as render failure
Two final MP4s rejected
_silent.mp4 never published
Old MP4s do not contaminate exact-candidate validation
Production never deleted by review cleanup
BOM UTF-8 manifests accepted
FFprobe failure blocks publication
Existing product is not overwritten by default
```

---

# 38. ACCEPTANCE CRITERIA V1.0

La primera versión del GUI se considerará operativa cuando cumpla todos estos bloques.

## A. Environment

- abre un proyecto existente;
- detecta Godot 4.7.1;
- detecta Python;
- detecta FFmpeg;
- detecta FFprobe;
- muestra claramente READY/WARN/FAIL.

## B. Review

- genera 5×5;
- cinco seeds únicas;
- mismas cinco seeds en las cinco familias;
- no borra production;
- muestra progreso;
- muestra resultados;
- abre vídeos;
- muestra metadata.

## C. Production

- produce una familia + seed;
- produce 25 productos;
- usa 720×1280;
- valida FFprobe;
- conserva logs/metadata;
- evita overwrite accidental;
- permite Force con confirmación explícita;
- publica únicamente después de validar.

## D. Artifacts

- lista review;
- lista prototype;
- lista production;
- lista QA/evidence sin permitir su borrado desde el cleaner C11-C;
- dry-run;
- cleanup seguro.

## E. Reproducibility

- muestra seed;
- muestra manifest;
- copia command;
- reproduce producto.

## F. Logs

- live log;
- búsqueda;
- filtros;
- abrir fichero real;
- copiar contenido.

## G. UX

- ningún render bloquea la UI;
- errores legibles;
- progreso visible;
- diferencia clara entre Review / Prototype / Production.

---

# 39. DISEÑO VISUAL DEL GUI

La aplicación debe sentirse como un **creative engineering lab**.

Dirección estética:

```text
premium technical
restrained cyberpunk
mathematical
engineering laboratory
```

Debe evitar una interfaz excesivamente “gamer” o decorativa.

Recomendación:

- dark mode como default;
- tipografía limpia;
- monoespaciada solo para logs/datos;
- tarjetas sobrias;
- previews grandes;
- iconos simples;
- estados cromáticos semánticos.

Los Visual Loops deben seguir siendo el protagonista visual.

---

# 40. INFORMACIÓN MÍNIMA SIEMPRE VISIBLE

En cualquier contexto de render:

```text
FAMILY
SEED
GRAMMAR
PALETTE
RESOLUTION
FPS
DURATION
AUDIO
STATE
```

En producción añadir:

```text
PRODUCT PATH
MANIFEST
LOG
HASH
```

En review añadir:

```text
BATCH
VARIATION INDEX
```

---

# 41. ALINEACIÓN CON LA TOOLCHAIN CANÓNICA

C11-C Studio debe usar el toolchain canónico del backend v2.1.4.

La aplicación debe descubrir las herramientas actuales por su nombre canónico y no depender de archivos históricos como:

```text
run_*_v2.0.8.ps1
run_*_v2.0.9.ps1
run_*_v2.1.0.ps1
```

Los scripts versionados antiguos son historia del desarrollo y no deben aparecer como acciones normales de la UI.

---

# 42. NO HACER

El futuro programador NO debe:

- integrar la matemática de shaders en Python;
- reimplementar los variation profiles;
- convertir Qt en motor de render;
- modificar `project.godot` para resolver una necesidad cosmética del GUI;
- modificar C11-B;
- trasladar production a prototypes;
- limpiar artifacts automáticamente al iniciar el GUI;
- borrar logs para ahorrar espacio;
- ocultar los logs técnicos;
- crear un segundo sistema de seeds;
- crear una segunda lógica de duración;
- duplicar la validación del backend dentro de la UI de forma incompatible;
- permitir rutas destructivas arbitrarias;
- convertir la primera versión en editor de shaders.

---

# 43. ROADMAP RECOMENDADO

## GUI-0 — Shell

- ventana principal;
- project picker;
- dependency detector;
- Dashboard;
- logs básicos.

## GUI-1 — Review

- Seed Manager;
- Review 5×5;
- gallery;
- comparison;
- metadata.

## GUI-2 — Production

- Single Product;
- Production 5×5;
- catalog;
- promotion;
- reproducibility.

## GUI-3 — Art Direction Lab

- Style Board;
- Family Comparison;
- Grammar Explorer;
- Palette Explorer;
- Parameter Inspector;
- Seed Comparison.

## GUI-4 — Operations

- Artifact Manager;
- cleanup dry-run;
- diagnostics;
- reports.

## GUI-5 — Future

- duration profiles;
- scheduling;
- production seed banks;
- corpus analytics.

---

# 44. HANDOFF PARA EL PROGRAMADOR

El programador debe comenzar leyendo:

```text
C11-C v2.1.4 backend
MASTER_HANDOVER_C11-C_ART_DIRECTION_2.0
C11C_TOOLCHAIN_CANONICAL
C11C_PRODUCTION_POLICY
C11-C CHANGELOG
```

Después inspeccionar el repositorio real.

No asumir que todos los nombres, gramáticas o parámetros futuros existen: deben descubrirse desde definiciones/manifests cuando corresponda.

Orden de implementación:

```text
1. ProjectContext
2. ToolDiscovery
3. EnvironmentValidator
4. CommandBuilder
5. JobManager
6. ArtifactRegistry
7. LogCenter
8. SeedManager
9. Dashboard
10. Review Lab
11. Production
12. Product Catalog
13. Reproducibility
14. Family Explorer
15. Grammar Explorer
16. Palette Explorer
17. Art Direction Lab
18. Tests
19. Windows packaging
```

---


# 45. DEFINICIÓN DE ÉXITO DEL PRODUCTO

C11-C Studio debe permitir que el usuario complete las operaciones principales sin abrir PowerShell.

Caso 1:

> “Quiero cinco variaciones aleatorias de cada una de las cinco familias para revisar la Dirección de Arte.”

Acción:

```text
NEW 5×5 REVIEW
```

Caso 2:

> “Quiero producir esas cinco familias con cinco seeds nuevas como productos finales.”

Acción:

```text
PRODUCE 25 FINAL PRODUCTS
```

Caso 3:

> “Quiero volver a producir exactamente Invisible Forces seed 271828.”

Acción:

```text
REPRODUCE EXACTLY
```

El GUI debe conservar estas propiedades del backend:

```text
determinism
traceability
logs
metadata
validation
artifact safety
production protection
```

---

# 46. ESTADO DE REFERENCIA ACTUAL

El backend de referencia del GUI es:

```text
C11-C v2.1.4
```

Estado físico confirmado en Windows:

```text
PowerShell canonical parse: PASS
Delivery configuration: PASS
Godot 4.7.1 editor scan: PASS
Movie Maker capture: 720×1280
FPS: 30
Duration baseline: 18.00 s
```

La salida de Movie Maker confirmada es del tipo:

```text
Movie Maker mode enabled, recording movie in 720×1280 @ 30 FPS...
```

El backend contiene cinco familias C11-C y herramientas separadas de review y production.

C11-B permanece frozen.

---

# 47. RELACIÓN CON DIRECCIÓN DE ARTE 2.0

C11-C Studio debe preparar la evaluación artística sin imponer todavía decisiones creativas al motor.

Flujo conceptual:

```text
BACKEND CERRADO / ESTABLE
        ↓
REVIEW CORPUS
        ↓
VISUAL COMPARISON
        ↓
ART DIRECTION 2.0
        ↓
NUEVO CONTRATO ARTÍSTICO
        ↓
IMPLEMENTACIÓN
        ↓
NUEVO CORPUS
```

El laboratorio debe permitir observar preguntas como:

- qué familias ofrecen suficiente diversidad sin perder identidad;
- qué gramáticas son inmediatamente reconocibles;
- qué palettes conservan presencia en móviles;
- dónde existe exceso de densidad visual;
- qué movimiento parece orgánico y cuál parece screensaver;
- qué tratamientos editoriales ayudan y cuáles distraen;
- qué relación existe entre parámetros matemáticos y percepción;
- qué duraciones deberían estudiarse en una futura fase variable.

El GUI no debe convertir esas preguntas artísticas en reglas rígidas.

---

# 48. RESUMEN EJECUTIVO PARA IMPLEMENTACIÓN

C11-C Studio debe ser una aplicación Windows de tipo creative engineering lab.

Arquitectura:

```text
C11-C Studio
    ↓
Canonical Toolchain
    ↓
PowerShell / Python
    ↓
Godot 4.7.1 / FFmpeg / FFprobe
    ↓
Artifacts
```

Las cinco familias:

```text
Geometric Waves
Fractal Bloom
Sacred Symmetry
Living Particles
Invisible Forces
```

Operaciones fundamentales:

```text
Review 5×5
Production 5×5
Production single
Seed reproduction
Family exploration
Grammar exploration
Artifact management
Log management
Validation
```

Regla arquitectónica definitiva:

> **El GUI puede controlar el sistema; el GUI no debe convertirse en el sistema.**

---

# 49. CHECKLIST DE ENTREGA DEL FUTURO PROGRAMADOR

```text
[ ] Project detection
[ ] Dependency detection
[ ] Canonical tool discovery
[ ] Dashboard
[ ] Five families visible
[ ] Seed Manager
[ ] Random seed generation
[ ] Review 5×5
[ ] Review gallery
[ ] Video player/open
[ ] Production single
[ ] Production 5×5
[ ] Production protection
[ ] Artifact browser
[ ] Cleanup dry-run
[ ] Production catalog
[ ] Log viewer
[ ] Validation center
[ ] Reproduction command
[ ] Product manifest viewer
[ ] Social metadata viewer
[ ] FFprobe result viewer
[ ] 720×1280 validation
[ ] Audio ON/OFF
[ ] No automatic cleanup
[ ] No C11-B modification
[ ] No duplicate generation logic
[ ] Unit tests
[ ] Integration tests
[ ] Failure/safety tests
[ ] Windows packaging
```

---

# 50. DOCUMENT CONTROL

```text
Document: C11-C STUDIO — MASTER SPECIFICATION
Project: ChallengeEngineV01_STATELESS
Purpose: future GUI implementation
Target platform: Windows 10/11 x64
Recommended stack: Python + PySide6 / Qt 6
Primary renderer: Godot 4.7.1
Backend reference: C11-C v2.1.4
Current delivery: 720×1280 / 30 FPS / 18.00 s baseline
Families: 5
Review target: 5×5 = 25
Production target: 5×5 = 25
C11-B: CLOSED / CERTIFIED / FROZEN
Next creative phase: Art Direction 2.0
```

---

# APÉNDICE A — OPERACIONES CANÓNICAS QUE EL GUI DEBE ENVOLVER

El GUI debe descubrir y ejecutar las herramientas canónicas actuales, evitando depender de los nombres históricos versionados.

Operaciones de validación:

```text
validate_c11c_powershell.ps1
validate_c11c_delivery_configuration.ps1
```

Operaciones de limpieza/maintenance:

```text
clean_c11c_artifacts.ps1
reset_c11c_artifacts.ps1
```

Operaciones de review:

```text
run_c11c_art_direction_review.ps1
run_c11c_multiseed_bulk.ps1
export_review_gifs.ps1
export_review_keyframes.ps1
export_all_review_assets.ps1
```

Operaciones de producción:

```text
run_c11c_production.ps1
run_c11c_production_bulk.ps1
run_all_c11c_visual_loops.ps1
```

Launchers de familias:

```text
c11c_geometric_waves_v1\run_prototype.ps1
c11c_fractal_bloom_v1\run_prototype.ps1
c11c_sacred_symmetry_v1\run_prototype.ps1
c11c_living_particles_v1\run_prototype.ps1
c11c_invisible_forces_v1\run_prototype.ps1
```

El futuro GUI puede cambiar la forma de presentación, pero no debe inventar sustitutos incompatibles.

---

# APÉNDICE B — CONTRATO DE 5×5

Cuando el usuario selecciona 5×5:

```text
5 unique seeds
×
5 families
=
25 jobs
```

Las mismas cinco seeds cruzan las cinco familias.

Ejemplo conceptual:

```text
                 SEED A   SEED B   SEED C   SEED D   SEED E
Geometric         ✓        ✓        ✓        ✓        ✓
Fractal           ✓        ✓        ✓        ✓        ✓
Sacred            ✓        ✓        ✓        ✓        ✓
Living            ✓        ✓        ✓        ✓        ✓
Invisible         ✓        ✓        ✓        ✓        ✓
```

El batch debe tener un `batch_id` único y persistir el conjunto de seeds usado.

---

# APÉNDICE C — REQUISITOS DE LA VENTANA PRINCIPAL

La primera impresión de C11-C Studio debe permitir identificar inmediatamente:

```text
Project
Backend version
Environment health
Review count
Production count
Current batch
```

Y ofrecer:

```text
[ REVIEW 5×5 ]
[ PRODUCE 5×5 ]
[ PRODUCE SINGLE ]
[ VALIDATE ]
```

Éstas son las cuatro acciones principales del producto.

---

# APÉNDICE D — REGLAS PARA FUTURA EVOLUCIÓN

Cuando aparezca una nueva familia:

1. el backend debe definirla;
2. el GUI debe descubrirla;
3. el GUI no debe requerir cambios de arquitectura para mostrarla;
4. la familia debe aportar nombre artístico, id técnico y metadata.

Cuando aparezca una nueva gramática:

1. debe exponerse como dato;
2. debe poder filtrarse/compararse;
3. debe conservarse su relación con seed y manifest.

Cuando aparezca una nueva duración:

1. debe estar en metadata;
2. debe validarse mediante frames/duration;
3. debe seguir garantizando cierre de loop;
4. el GUI no debe asumir 18s como ley permanente.

---

# FIN DEL DOCUMENTO
C11-C STUDIO — MASTER SPECIFICATION — v2.1.4
C11-B remains frozen. Art Direction 2.0 is the next creative phase.


# 51. MASTER CONFIGURATION MATRIX — COMPLETE GUI COVERAGE

Esta sección es **normativa** para la interfaz. Ninguna pantalla del GUI debe omitir una variable que el backend actual exponga en authoring, manifest, variation profile, grammar spec, launcher o product metadata.

La regla de implementación es:

> **El backend es la fuente de verdad de las variables. La GUI debe descubrirlas y presentarlas; nunca inventarlas ni duplicarlas.**

Cada parámetro debe clasificarse en una de estas clases:

```text
USER_CONFIGURABLE   = el usuario puede elegirlo antes de generar
SEED_DERIVED        = lo determina la seed/perfil y se puede inspeccionar
BACKEND_EFFECTIVE   = valor final calculado/aplicado por backend
READ_ONLY           = informativo, no editable
PROTECTED           = no editable desde GUI
FUTURE              = reservado para una fase posterior
```

El GUI debe mostrar visualmente esa condición.

## 51.1 Project / Environment

Siempre disponibles en Settings / Environment:

```text
project_root
repository_state
backend_version
C11-C version
Godot executable/path
Godot version
FFmpeg executable/path
FFmpeg version
FFprobe executable/path
Python executable/path
Python version
PowerShell version
renderer/device
GPU
OS / architecture
```

Health checks:

```text
Godot available
FFmpeg available
FFprobe available
Python available
PowerShell parse status
canonical tools present
five families present
production path writable
review path writable
```

## 51.2 Delivery / Video Master Settings

El GUI debe exponer claramente dos conceptos separados:

```text
LOGICAL CANVAS
540 × 960   (C11-B logical baseline; protected)

DELIVERY CANVAS
720 × 1280  (current C11-C social/production delivery)
```

Configuración actual:

```text
width       = 720
height      = 1280
aspect      = 9:16
fps         = 30
frame_count = 540
length      = 18.00 s
```

Configurables actualmente:

```text
Delivery resolution       USER_CONFIGURABLE only when canonical backend permits it
FPS                       USER_CONFIGURABLE only when canonical backend permits it
Duration                  USER_CONFIGURABLE only when canonical backend permits it
Audio                     ON/OFF
Footer                    ON/OFF
```

Durante v2.1.4 el perfil canónico de entrega sigue siendo 720×1280 / 30 FPS / 18 s. La GUI debe tratar esos valores como **current canonical defaults**, no como límites universales del sistema.

El GUI debe impedir que 540×960 sea presentado como producto social actual.

## 51.3 Seed Configuration

Opciones completas:

```text
RANDOM
MANUAL
CORPUS
REPRODUCTION
PRODUCTION SEED BANK
```

Controles:

```text
seed value
seed count
unique seeds only
same seeds across families
random generation range
batch id
reproduction from product
reproduction from manifest
```

Para 5×5:

```text
5 unique seeds
×
5 families
```

Las mismas cinco seeds cruzan las cinco familias.

El GUI debe conservar:

```text
seed source
seed list
batch_id
created_at
family mapping
```

## 51.4 Batch Configuration

Campos:

```text
families selected[]
variations per family
seed mode
seed list
same seeds across families
review vs production
parallelism
continue-on-error
fail-fast
force replacement
reset review assets
```

Regla de seguridad:

```text
REVIEW
→ no production overwrite

PRODUCTION
→ existing product protection
```

## 51.5 Family Selection

La GUI debe presentar las cinco familias actuales:

```text
Geometric Waves       geometric
Fractal Bloom         fractal
Sacred Symmetry       kaleidoscope / sacred_symmetry
Living Particles      particle_flow / living_particles
Invisible Forces      vector_field / invisible_forces
```

Cada tarjeta debe mostrar:

```text
artistic name
technical id
family id
current grammar
palette
seed
status
last render
last production
```

La lista debe ser **dinámica** para soportar nuevas familias sin reescritura de la UI.

## 51.6 Grammar / Subfamily Configuration

La UI debe permitir:

```text
AUTO / SEED-DERIVED
EXPLICIT GRAMMAR (cuando el backend la permita)
```

Campos:

```text
grammar_id
grammar_name
grammar version
grammar availability
coverage status
supported parameters
```

Fractal Bloom tiene actualmente estas gramáticas conocidas:

```text
RADIAL BLOOM
DENDRITIC TUNNEL
SPIRAL FRACTAL
FRACTAL FILIGREE
NESTED WORLDS
```

Geometric Waves debe poder representar sus variantes/gramáticas dinámicamente, aunque el backend actual tenga solo una familia canónica.

Lo mismo aplica a Sacred Symmetry, Living Particles e Invisible Forces.

## 51.7 Common Visual Parameters

Cuando existan en el `VariationProfile` o manifest, el GUI debe poder inspeccionar/editar según el estado del parámetro:

```text
palette
palette anchor
palette mode
background
scale
phase
frequency
rational frequency
amplitude
amplitude set
layer count
layer offsets
optical depth
bloom / light intensity
detail
branching
symmetry order
grid/ring counts
density
particle count
flow
trace count
pulse speed
field configuration
rotation
rotation phase
gear relationship
gear ratio
attractor parameters
collision / interaction mode
trail parameters
color phase
color diversity
loop cycles
```

**No todos pertenecen a todas las familias.** El GUI debe ocultar los no aplicables y conservar los desconocidos como metadata, nunca descartarlos.

## 51.8 Geometric Waves — Complete Known Parameter Surface

Familia:

```text
family_id       = c11c_geometric_waves_v1
technical       = geometric
artistic        = Geometric Waves
```

Parámetros conocidos:

```text
polygon/order selection
rational frequency
phase
amplitudes
layer offsets
palette anchor
scale relationships
wave value
morph value
frequency relationships
Lissajous relationship / ratio
layer count
```

Datos editoriales que pueden aparecer en el render:

```text
WAVE x.x
MORPH x.xx
N / geometry order
frequency / phase terms
layer count
seed
body size
fps
duration
```

El GUI debe disponer de un inspector de estos valores efectivos, aunque algunos sean SEED_DERIVED.

## 51.9 Fractal Bloom — Complete Known Parameter Surface

Familia:

```text
family_id       = c11c_fractal_bloom_v1
technical       = fractal
artistic        = Fractal Bloom
```

Estructura matemática conocida:

```text
z_(n+1) = z_n² + c
```

Parámetros/mecanismos:

```text
Julia constant c
seed-derived Julia constant
orbit traps
domain warp
depth layer count
layer offsets
zoom amount
zoom phase
zoom cycles
branch/detail factor
color phase
color diversity
palette
optical nucleus / radial center
grammar
```

Gramáticas conocidas:

```text
RADIAL BLOOM
DENDRITIC TUNNEL
SPIRAL FRACTAL
FRACTAL FILIGREE
NESTED WORLDS
```

El GUI debe mostrar especialmente el balance entre `zoom`, `detail`, `branching`, `grammar` y `palette` porque son variables críticas de dirección visual.

## 51.10 Sacred Symmetry — Complete Known Parameter Surface

Familia:

```text
family_id       = c11c_sacred_symmetry_v1
technical       = kaleidoscope / sacred_symmetry
artistic        = Sacred Symmetry
```

Parámetros conocidos:

```text
symmetry order N
radial layers
concentric rings
rotation
rotation phase
gear count
gear relationship
gear ratio
phase offsets
ring relationships
scale relationships
metallic palette mode
background
loop cycles
```

Editorial example:

```text
N=x
GEAR x:y
```

## 51.11 Living Particles — Complete Known Parameter Surface

Familia:

```text
family_id       = c11c_living_particles_v1
technical       = particle_flow / living_particles
artistic        = Living Particles
```

Parámetros conocidos:

```text
particle density
particle count
flow magnitude
flow frequency
attractors
attractor relationships
eddies
collision / interaction behavior
trails
trail length/intensity
phase
scale
palette
palette mode
```

Editorial example:

```text
DENSITY x.xx
FLOW x.xx
PARTICLES ...
COLLISION ...
```

## 51.12 Invisible Forces — Complete Known Parameter Surface

Familia:

```text
family_id       = c11c_invisible_forces_v1
technical       = vector_field / invisible_forces
artistic        = Invisible Forces
```

Parámetros conocidos:

```text
field configuration
field / basin grammar
trace count
pulse speed
phase
flow field parameters
radial / topographic relationships
palette
palette mode
loop cycles
```

`pulse_speed` es actualmente una variable continua derivada de seed, dentro del rango implementado en la variante actual.

Editorial reference:

```text
TOPOGRAPHIC_BASIN | xx TRACES | PULSE x.xx
NO VES LA FUERZA, SOLO SU RASTRO
```

## 51.13 Palette / Color Configuration

El GUI debe conocer la paleta completa de cada familia mediante `C11CPaletteBank` y no mediante una lista duplicada manualmente.

Cada palette record debe poder exponer:

```text
palette_id
family
primary
secondary
highlight
background
accent / anchor (when present)
color phase
color diversity
color boost state / amount when exposed
```

Actualmente existe un banco ampliado de colorways por familia. La selección puede ser SEED_DERIVED.

El GUI debe permitir:

```text
preview effective palette
inspect palette
filter by family
compare palettes
```

Modo de producción actual:

```text
palette effective = backend source of truth
```

La edición manual de colores solo debe habilitarse si se implementa como un contrato nuevo y explícito; no debe alterar silenciosamente los perfiles deterministas actuales.

## 51.14 Background / Canvas / Depth

Campos visibles:

```text
logical canvas
physical delivery canvas
background color
body region
header region
footer region
optical center
safe hero radius
layer count
optical depth
bloom / glow
```

C11-B logical frame:

```text
540×960
Header = y 0..144
Body   = y 144..816
Footer = y 816..960
```

Current delivery:

```text
720×1280
Header = scaled logical region
Body   = scaled logical region
Footer = scaled logical region
```

La GUI nunca debe mover estos límites protegidos mediante controles experimentales sin un modo explícito de Art Direction Lab.

## 51.15 Editorial Configuration

### Header

Dos líneas principales:

```text
Line 1 = factual / mathematical / variant data
Line 2 = user-facing hook
```

Line 2 puede ejecutar:

```text
HOOK
→ MATRIX / airport-board scramble
→ FAMILY SIGNATURE
→ scramble
→ HOOK
```

Variables:

```text
eyebrow / line 1 text
hook text
family signature text
scramble duration
scramble charset
transition timing
text colors
line positions
alignment
```

### Decorative lines

```text
decorative line A
 decorative line B
line positions
line length
line thickness
line color
opacity
```

Deben formar parte de la composición editorial y poder activarse/desactivarse solo mediante el contrato correspondiente.

### Footer

El footer actual es telemetría. No debe repetir `VISUAL LOOP // FAMILY` si la identidad ya aparece en cabecera.

Campos:

```text
technobabble
status token
actual parameters
seed
body size
fps
duration
loop information
audio state
palette data
signature/version
```

### Typography

El GUI debe permitir inspeccionar:

```text
font family
font file/path
font size
font weight
tracking
line spacing
alignment
uppercase transform
safe margins
```

En producción inicial estos valores son read-only cuando proceden del contrato editorial.

## 51.16 Technobabble / Text Generation

El backend actual contiene vocabulario:

```text
cyberpunk
hacker
steampunk
geek
status / machine state
```

El GUI debe mostrar:

```text
generated text
category/source when available
context parameters used
status word
```

El texto puede estar relacionado con parámetros reales de la familia.

Nunca debe permitir que el texto generado declare parámetros que no existan realmente en el producto.

## 51.17 Audio Configuration

Opciones actuales:

```text
Audio ON
Audio OFF / NoSound / Silent
```

Metadata:

```text
audio profile
sample rate
channels
duration
loop state
WAV path
```

Condición actual esperada:

```text
44100 Hz
2 channels
18.00 s
```

El audio debe utilizar el perfil `C11CSafeAmbient`/equivalente vigente, orientado a reproducción móvil no intrusiva.

El GUI debe tratar las frecuencias internas, envolventes, armónicos y demás parámetros de síntesis como **backend-owned** salvo que la toolchain los exponga explícitamente.

## 51.18 Loop Configuration

Variables:

```text
loop enabled
loop cycles
total duration
cycle duration
phase closure
visual closure
audio closure
```

Actualmente el sistema utiliza ciclos enteros y la cantidad de ciclos puede ser SEED_DERIVED.

El GUI debe mostrar el valor efectivo y comprobar:

```text
closed loop = true
```

## 51.19 Output / Encoding Configuration

El GUI debe mostrar:

```text
AVI intermediate path
MP4 final path
GIF path
WAV path
manifest path
authoring path
ffprobe path
Godot log path
social metadata path
```

El usuario debe ver que el AVI es intermedio y no un producto final.

Regla actual:

```text
one canonical MP4 per seed
```

Nunca crear dos MP4 finales para ON/OFF audio.

## 51.20 Social Metadata

Cada producto final debe exponer:

```text
TITLE
DESCRIPTION
FAMILY
GRAMMAR
PALETTE
SEED
DURATION
FPS
FRAMES
LOOP CYCLES
LOOP CLOSED
AUDIO
BACKGROUND
HEADER
EDITORIAL TRANSITION
TECHNOBABBLE
HASHTAGS
REPRODUCTION COMMAND
CANONICAL MANIFEST
```

La GUI debe incluir:

```text
Preview social text
Copy social text
Open social file
```

## 51.21 Product / Artifact Configuration

Clasificación obligatoria:

```text
LEGACY
QA
REGRESSION
RELEASES
PRODUCTION
TESTS
PROTOTYPES
SCRATCH
```

La GUI debe mostrar una protección visual fuerte para:

```text
production
legacy evidence
qa evidence
regression evidence
release evidence
```

No debe existir un botón ambiguo llamado simplemente `DELETE ALL`.

Las acciones deben especificar exactamente qué raíz afectan.

## 51.22 Product States

Estados de producto:

```text
DISCOVERED
QUEUED
GENERATING
RENDERED
AUDIO_GENERATED
MUXED
VALIDATING
PASS
FAILED
PUBLISHED
PROTECTED
```

Estados de job:

```text
IDLE
QUEUED
RUNNING
VALIDATING
PASS
FAIL
CANCELLED
SKIPPED
```

Estados de environment:

```text
READY
DEGRADED
BLOCKED
```

## 51.23 Production Safety Options

Antes de publicar:

```text
existing product detected
force replacement
candidate validation
manifest validation
ffprobe validation
single-MP4 validation
resolution validation
audio validation
social metadata validation
```

`Force` nunca debe saltarse validaciones. Solo autoriza la sustitución deliberada de un producto existente **después** de validar el candidato nuevo.

## 51.24 Game / ChallengeEngine Configuration Surface

C11-C Studio debe prever una sección **Challenge Engine / Games** porque el repositorio contiene además el sistema determinista de retos y visual drills.

Esta sección debe ser inicialmente READ_ONLY para lo congelado y AUTHORING/EXPORT cuando una herramienta canónica lo permita.

Campos generales:

```text
challenge_id
challenge family/type
seed
authoring definition
profile
variant
input contract
native duration
FPS
rendered frame stream
winning frame
close calls
visual presentation profile
audio mode
video mode
output mode
```

El GUI debe mostrar, no recalcular:

```text
SimulationResult
WinningFrameDetector result
close_calls
native challenge duration
```

No debe exponer controles que permitan modificar desde la GUI las matemáticas congeladas.

### Challenge families / current repository concepts

El sistema C11 existente contiene retos numerados al menos en el rango actual `CHALLENGE_001` ... `CHALLENGE_009` y herramientas para authoring/QA/production.

El GUI debe descubrirlos desde definiciones/manifests en lugar de hardcodear sus propiedades.

Para cada challenge debe existir una ficha:

```text
Challenge ID
human name
seed
definition path
profile path
authoring status
QA status
production status
native duration
video duration
audio state
manifest
reproduction command
```

### Visual Drills

El GUI debe admitir al menos los conceptos presentes en C11-A visual QA:

```text
tracking
pursuit
saccade
peripheral scan
```

y representar sus parámetros definidos por el backend como dinámicos.

Nunca debe inventar parámetros de un visual drill que el manifest no exponga.

## 51.25 QA / Validation Options

Controles:

```text
PowerShell parse validation
Delivery configuration validation
Godot headless project scan
family launcher validation
render validation
FFprobe validation
single MP4 validation
social sidecar validation
manifest validation
seed determinism check
batch completeness
artifact path check
production protection check
```

El GUI debe permitir:

```text
run all validation
run selected validation
view failure
open implicated file
copy diagnostic output
```

## 51.26 Logs / Diagnostics

Cada job debe tener:

```text
stdout
stderr
Godot log
Python output
FFmpeg output
FFprobe JSON
structured error
exit code
start/end time
command line
```

El GUI debe soportar:

```text
live log
filter ERROR/WARN/PASS
open raw log
copy diagnostic
open output folder
```

## 51.27 Command Reproduction

Cada producto debe poder generar/copiar el comando exacto de reproducción.

Debe incluir como mínimo:

```text
family
seed
audio state
footer state
any explicit supported parameter overrides
```

No reconstruir el comando a partir de texto visual del producto si existe una orden canónica registrada en metadata.

## 51.28 Dynamic Introspection Contract

Para no perder variables futuras, C11-C Studio debe implementar introspección.

El backend puede exponer una estructura conceptual:

```json
{
  "family": "...",
  "grammar": "...",
  "parameters": {
    "name": {
      "value": 0,
      "type": "float",
      "state": "SEED_DERIVED",
      "min": 0,
      "max": 1,
      "editable": false,
      "source": "variation_profile"
    }
  }
}
```

El GUI debe generar los controles apropiados según:

```text
type
editable
min
max
step
enum/options
source
```

Si aparece un parámetro desconocido:

```text
NO FAIL
NO DROP
NO SILENT IGNORE
```

Debe aparecer en una sección `Advanced / Unknown backend parameters`.

## 51.29 Configuration Presets

La GUI debe admitir presets de alto nivel:

```text
CURRENT CANONICAL
SOCIAL DELIVERY
REVIEW 5×5
PRODUCTION 5×5
SILENT DELIVERY
SINGLE REPRODUCTION
```

Los presets son atajos de UI. No constituyen una segunda fuente de verdad.

## 51.30 Configuration Snapshot

Antes de ejecutar cualquier batch, el GUI debe poder guardar un snapshot:

```text
configuration_snapshot.json
```

Debe contener:

```text
backend version
family list
seed list
variation settings
palette/grammar effective data
delivery settings
presentation settings
audio settings
output mode
tool versions
command lines
```

Así una tanda puede reproducirse incluso después de cambiar la UI.

## 51.31 Art Direction Lab — Editable Surface

A diferencia de Production, el Art Direction Lab sí puede ofrecer controles experimentales.

Debe distinguir claramente:

```text
CANONICAL
EXPERIMENTAL
```

Superficies experimentales previstas:

```text
palette boost
saturation / luminance treatment
editorial hierarchy
header/footer placement
font scale
decorative lines
hook variants
transition timing
background treatment
bloom
layer depth
movement intensity
composition scale
visual density
grammar selection
seed comparison
```

Toda modificación experimental debe guardarse como overlay/preset y no sobreescribir silenciosamente el contrato canónico.

## 51.32 Future Duration System

Reservado:

```text
SHORT
MEDIUM
LONG
EXPLICIT
```

El GUI debe estar preparado para representar un futuro:

```text
duration profile
seconds
frame count
loop cycles
grammar driver
```

No activarlo como contrato C11-C v2.1.4.

## 51.33 UI Rule — Never Hide Effective Values

Aunque el usuario no pueda editar un valor, debe poder verlo.

Ejemplo:

```text
Pulse Speed
1.15
[SEED-DERIVED]
```

no:

```text
Pulse Speed
(hidden)
```

La GUI debe ser un observatorio completo del generador además de un controlador.

## 51.34 UI Rule — Every Product Must Explain Itself

Al seleccionar un producto, el usuario debe poder obtener sin consola:

```text
qué familia es
qué gramática usa
qué seed lo produjo
qué palette utiliza
qué parámetros efectivos tiene
qué duración tiene
qué resolución tiene
si tiene audio
si el loop está cerrado
dónde está el MP4
dónde está el manifest
dónde está el log
cómo reproducirlo
qué validaciones pasó
```

## 51.35 Acceptance Addendum — Configuration Completeness

El GUI no se considera completo hasta que:

```text
[ ] todas las cinco familias aparecen
[ ] todas las gramáticas conocidas aparecen
[ ] seed modes aparecen
[ ] 5×5 aparece
[ ] delivery settings aparecen
[ ] logical vs physical canvas aparece
[ ] audio ON/OFF aparece
[ ] footer ON/OFF aparece
[ ] header/footer effective content aparece
[ ] decorative lines aparecen
[ ] effective palette aparece
[ ] common parameters aparecen
[ ] family-specific parameters aparecen
[ ] loop information aparece
[ ] product/artifact state aparece
[ ] logs aparecen
[ ] manifests aparecen
[ ] reproduction command aparece
[ ] challenge/game metadata aparece
[ ] visual drill metadata aparece
[ ] QA/validation aparece
[ ] production protection aparece
[ ] unknown backend parameters no se pierden
[ ] future duration model está preparado
```

# 52. IMPLEMENTATION PRIORITY OF THE COMPLETE CONFIGURATION SURFACE

El programador no debe implementar todo como una única pantalla.

Orden:

```text
P0  Environment + canonical state
P0  Family selector
P0  Seed / batch
P0  Review / Production
P0  Delivery
P0  Job/logs
P0  Product/artifact explorer

P1  Variation inspector
P1  Palette explorer
P1  Grammar explorer
P1  Editorial inspector
P1  Audio inspector
P1  Reproduction view

P2  Challenge / Games viewer
P2  Visual Drill viewer
P2  QA center
P2  Production catalog

P3  Art Direction Lab
P3  advanced experimental overlays
P3  duration profiles
P3  future families/grammars
```

# 53. FINAL DESIGN RULE

El objetivo de C11-C Studio no es reducir la información del sistema para hacerla más simple.

Su objetivo es **hacer visible la complejidad real y controlarla de forma segura**.

El programador debe asumir que C11-C evolucionará en:

```text
families
subfamilies / grammars
parameters
palettes
editorial modes
audio profiles
duration profiles
output targets
challenge integrations
```

Por ello, el GUI debe ser **metadata-driven, schema-driven y backend-discoverable**.

No debe construirse alrededor de una lista fija de botones que reproduzca los comandos actuales.

# FIN DE LA AMPLIACIÓN DE CONFIGURACIÓN
