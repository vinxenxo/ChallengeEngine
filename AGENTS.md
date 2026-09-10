# Guía para agentes (DESACTUALIZADA)

## Propósito y alcance

Este archivo es la guía operativa para agentes que trabajen en `ChallengeEngineV01_STATELESS`. Resume la arquitectura, los contratos que deben preservarse, los puntos de extensión y el flujo de validación. No sustituye las especificaciones del proyecto ni convierte documentos históricos en estado actual.

La autoridad se consulta en este orden:

1. Código fuente ejecutable, especialmente la ruta que se esté modificando.
2. Documentación marcada como estado live.
3. Tests y contratos automatizados.
4. Checkpoints históricos, solo como contexto de decisiones anteriores.

La documentación de estado principal es `docs/DOCUMENTATION_STATUS_1.1.0-C6-D4.md`. Para gobierno y contratos de ingeniería, consultar `docs/GOVERNANCE.md`, `docs/MASTER_HANDOVER_CHECKPOINT_1.1.0-C6-D4.md` y `docs/ROADMAP_PHASES.md`. `.continue/rules/CONTINUE.md` contiene reglas útiles, pero es parcial y no refleja todos los subsistemas actuales.

## Identidad del proyecto

Es un generador determinista de challenges y vídeos para Godot 4.7. La ejecución está dividida en cuatro capas:

```text
JSON declarativo
    -> simulación determinista y validación
    -> presentación Godot / Movie Maker
    -> orquestación Python + FFmpeg + FFprobe
```

El proyecto declara Godot `4.7` y renderizado Compatibility en `project.godot`. La escena principal es `Main.tscn`, con `GeneradorMaestro.gd` como raíz de composición del runtime live. El viewport fuente es `540x960`; la salida de producción esperada se transcodifica a `1080x1920` cuando corresponde.

La arquitectura distingue:

- **Capa declarativa:** JSON de entrada con intención del creador: mecánica, semilla, dificultad, tiempos, assets y perfiles.
- **Simulación:** cálculo determinista en CPU. Produce historia de frames, métricas y resultado verificado sin depender de nodos gráficos.
- **Presentación:** consume el resultado verificado y lo representa siguiendo la línea temporal, perfiles, bindings y componentes visuales.
- **Producción:** Python coordina Godot, recoge telemetría, ejecuta FFmpeg/FFprobe y construye manifiestos.

`core/execution/ChallengeExecutionPipeline.gd` y `ChallengeTimelineBuilder.gd` representan una vía de ejecución/canonical V2 distinta del flujo de composición visible en `GeneradorMaestro.gd`. Antes de cambiar uno, confirmar mediante sus callers y tests si la modificación afecta al runtime live, al flujo de authoring o a ambos.

## Mapa del código

### Entrada y composición

- `Main.tscn`: escena de entrada configurada en `project.godot`.
- `GeneradorMaestro.gd`: procesa argumentos de usuario tras `--`, carga la definición, crea la línea temporal, valida, inicializa RNG, ejecuta simulación y validación, presenta `verified_history` y emite `[TELEMETRY_JSON]` o `[ERROR_JSON]`.
- `build_factory.py`: orquestador de producción. Lanza Godot, captura resultados, transcodifica y genera manifiestos.

### `core/deterministic/`

Contiene la base de reproducibilidad:

- `DeterministicLCG.gd`: primitiva matemática stateless; no debe acumular estado de secuencia mutable.
- `RNGStreamRegistry.gd` y `RNGStreamDefinition.gd`: registran streams, dominios y consumidores autorizados.
- `StructuralRNG.gd` y `CosmeticRNG.gd`: separan decisiones que alteran la simulación de variaciones visuales.
- `MechanicRNGContext.gd` y `PresentationRNGContext.gd`: inyectan capacidades limitadas a cada capa.

Toda nueva fuente de aleatoriedad debe tener stream registrado, dominio propietario y consumidor explícito. No usar singletons RNG globales ni permitir que el RNG cosmético altere `SimulationResult` o `verified_history`.

### `core/mechanics/`

- `ChallengeMechanic.gd`: contrato base de las mecánicas.
- `MechanicRegistry.gd`: resuelve identificadores de mecánica.
- Familias actuales: `key`, `parking`, `pilot`, `hit`, `catch`, `find`, `choose` y `count`.
- `ParkingMechanicV2.gd` coexiste con la implementación legacy; no integrar ni retirar una variante sin evidencia en sus tests y documentación live.

Una nueva mecánica debe definir su contrato matemático, recibir capacidades RNG por inyección, aislarse en tests y registrarse solo cuando la integración esté validada.

### `core/authoring/`

Implementa authoring y migración de challenges: requests, validadores, resolutores, registries y adapters por mecánica. Los perfiles de dificultad, vídeo, audio, assets y presentation binding deben validarse antes de llegar a producción. `ChallengeMigrationAdapter.gd` es el punto a revisar cuando se traduzcan definiciones legacy al contrato canonical.

### `core/simulation/`, `core/timeline/` y `core/validation/`

- `SimulationResult.gd`: resultado de simulación; sus campos y semántica son contrato público interno.
- `SimulationMetricsResolver.gd`: métricas derivadas del resultado.
- `VideoTimeline.gd`: fuente efectiva de fases y conteo de frames.
- `ChallengeDefinitionValidator.gd`, `C6FChallengeSchemaValidator.gd` y `ChallengeValidator.gd`: validan distintos límites del contrato.
- `WinningFrameDetector.gd`: localiza el frame ganador.
- `ValidationResult.gd` y `FamilyAssets.gd`: transportan resultados y assets validados.

La simulación debe mantenerse libre de presentación. Los detectores y validadores deben detectar y transportar errores; la raíz de composición decide la salida de proceso y la telemetría.

### `core/presentation/`

Contiene perfiles, coordinate mapping, binding, UI y componentes como hook, countdown, reveal, CTA y winning highlight. `ReferenceFrameResolver.gd` y `ChallengePresentationBinder.gd` conectan la simulación validada con la presentación. Esta capa debe leer el resultado verificado, no recalcular la verdad del challenge ni cambiar el resultado por decisiones cosméticas.

### `core/data/`

Contiene modelos de datos compartidos, incluido `FrameSnapshot.gd`. Las clases de datos puros deben conservar el patrón existente de `RefCounted` y tipado estático salvo una razón documentada y validada.

### `challenges/`, schema y assets

Las fixtures actuales `CHALLENGE_001` a `CHALLENGE_009` no son homogéneas:

- `CHALLENGE_001` y `CHALLENGE_002` usan RNG 1.0 y son fixtures legacy congeladas.
- `CHALLENGE_003` a `CHALLENGE_009` usan RNG 2.0.
- `CHALLENGE_007`, `CHALLENGE_008` y `CHALLENGE_009` ejercitan, respectivamente, `find_v1`, `choose_v1` y `count_v1`.

`challenge_schema.json` define el contrato C6-F con `schema_version: "2.0"`, secciones como `simulation` y `presentation`. Algunas fixtures live usan `generation`, schema 1.0 o carecen de `schema_version`; no asumir que todas cumplen directamente el schema C6-F. Tratarlo como frontera de authoring/migración hasta que el código y la documentación establezcan una convergencia.

Los assets obligatorios deben resolverse con rutas `res://`. No introducir rutas absolutas ni dependencias de una máquina local en challenges o perfiles.

## Contratos que no deben romperse

### RNG y determinismo

- Misma semilla, configuración, algoritmo y versión de motor deben producir la misma secuencia lógica.
- `DeterministicLCG` permanece stateless.
- Los streams deben registrarse antes de consumirse.
- `StructuralRNG` controla decisiones que afectan a la simulación.
- `CosmeticRNG` solo controla variación de presentación.
- Añadir presentación, cambiar orden de render o consumir RNG cosmético no puede cambiar la simulación ni el frame ganador.
- `CHALLENGE_001` y `CHALLENGE_002` deben conservar compatibilidad RNG 1.0.

### Tiempo y frames

La secuencia de fases es:

```text
HOOK -> GAME -> REVEAL -> CTA
```

- Una fase con duración `0` se omite.
- `GAME > 0` siempre debe cumplirse.
- `total_frames` es la suma de las fases efectivas.
- `SimulationResult.winning_frame` es relativo a `GAME`.
- Para obtener el frame absoluto de vídeo se suma `hook_frames` al frame ganador relativo.
- `VideoTimeline.gd` es la fuente efectiva de la temporalidad en Godot.
- No cambiar matemáticas de simulación o winning-frame como solución a un problema puramente visual o temporal.

### Manifiestos y metadata

La factoría separa metadata declarativa, telemetría runtime, mediciones físicas y valores derivados. No inventar campos declarativos que no existan en la definición de entrada. `factory_version` y `manifest_version` son identidades distintas.

Los artefactos esperados se aíslan por challenge, por ejemplo:

```text
output/CHALLENGE_XXX/CHALLENGE_XXX_raw.avi
output/CHALLENGE_XXX/CHALLENGE_XXX.mp4
output/CHALLENGE_XXX/CHALLENGE_XXX.gif
output/CHALLENGE_XXX/CHALLENGE_XXX_manifest.json
output/BATCH_MANIFEST.json
```

Los archivos existentes en `output/` o manifests históricos no prueban el estado actual. Para certificar una versión, regenerar y validar los artefactos.

## Workflow de desarrollo

Antes de editar:

1. Identificar la ruta ejecutable que decide el comportamiento, no solo el archivo que lo reexporta o registra.
2. Leer el test más cercano y el contrato/documento live asociado.
3. Confirmar si el cambio afecta a simulación, presentación, authoring, producción o más de una capa.
4. Mantener los cambios pequeños y no reformatar archivos no relacionados.

Al añadir una mecánica o stream:

1. Congelar primero el contrato matemático y sus invariantes.
2. Implementar aislamiento con capacidades RNG inyectadas.
3. Añadir o actualizar el registry correspondiente.
4. Añadir tests con marcadores PASS.
5. Integrar solo después de comprobar equivalencia y regresión.

Al modificar una suite GDScript:

- Cada archivo `*Test.gd` descubierto bajo `tests/` debe estar registrado en `KNOWN_SUITES` dentro de `tests/run_all.py`.
- Debe emitir exactamente el marcador PASS que el registro espera.
- Evitar entradas duplicadas: las claves repetidas en el diccionario Python se sobrescriben silenciosamente.

No usar una ejecución parcial como sustituto de la regresión completa. No declarar una release certificada basándose solo en tests estáticos o Python.

## Validación y comandos

Ejecutar primero los checks baratos disponibles desde la raíz del proyecto:

```powershell
python .\tests\phase_duration_contract_test.py
python .\tests\c6e_output_contract_test.py
python -m py_compile .\build_factory.py
python .\audit_c3_e.py
```

Regresión GDScript completa:

```powershell
python .\tests\run_all.py
```

El runner descubre todas las suites `*Test.gd`, exige registro explícito, detecta errores fatales, comprueba exit code y exige el marcador PASS. `tests/run_suite.py` es un runner parcial para un subconjunto de mecánicas y no reemplaza a `run_all.py`.

Validación del proyecto y suite individual:

```powershell
godot --headless --path . --editor --quit
godot --headless --path . --script .\tests\RNGArchitectureTest.gd
```

Para la factoría:

```powershell
python build_factory.py --config .\challenges\CHALLENGE_001.json --output .\output
python build_factory.py --config .\challenges\CHALLENGE_001.json --output .\output --validate-only
python build_factory.py --batch .\challenges --output .\output --workers 2
python build_factory.py --batch .\challenges --output .\output --workers 2 --no-gif
```

La certificación física completa requiere Godot 4.7.1, FFmpeg y FFprobe, además de la ejecución del corpus, el batch de los nueve challenges y la inspección de frames, duración, framerate, resolución, codec y pixel format. Si una herramienta no está disponible, informar el bloqueo; nunca convertirlo en PASS.

## Estado y riesgos conocidos

- La certificación E2E física de C6-D4 depende de Godot 4.7.1, FFmpeg y FFprobe y no debe inferirse de artefactos históricos.
- Existe una diferencia entre el schema C6-F y las fixtures live legacy; investigarla antes de cambiar validadores o migración.
- `ChallengeExecutionPipeline.gd` debe considerarse una vía distinta hasta confirmar sus callers y cobertura.
- `tests/run_all.py` contiene históricamente entradas repetidas en `KNOWN_SUITES`; no asumir que cada línea representa una suite adicional.
- Algunos documentos y README pueden contener conflictos o estados de checkpoints anteriores. No usarlos como autoridad sin contrastarlos con código y documentación live.
- `.continue/rules/CONTINUE.md` no es un inventario completo del proyecto y puede quedar desactualizado.

Estos puntos son riesgos de mantenimiento, no instrucciones para corregirlos automáticamente durante una tarea no relacionada.

## Checklist antes de terminar

- El cambio respeta la separación de capas.
- No se alteró el determinismo estructural ni la semántica del frame ganador sin una regresión explícita.
- Los nuevos streams y tests están registrados.
- Las fixtures legacy que correspondan siguen siendo compatibles.
- Se ejecutaron los checks disponibles y se distinguieron los bloqueos de las pruebas exitosas.
- Las rutas, assets y comandos documentados funcionan en el entorno indicado.
- No se presentó como certificación evidencia histórica o incompleta.
- La documentación live se actualizó si cambió un contrato, comando o estado de release.
