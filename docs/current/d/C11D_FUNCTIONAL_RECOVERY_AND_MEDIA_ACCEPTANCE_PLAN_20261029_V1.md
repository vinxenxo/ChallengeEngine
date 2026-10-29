# C11-D — Plan de recuperación funcional y aceptación de vídeo físico V1

**Fecha:** 2026-10-29  
**Prioridad:** ingeniería funcional y producción de medios, no más preparación documental genérica.  
**Objetivo final:** que la suite operativa `c11c-suite` genere bajo demanda con el baseline D, y no siga exponiendo C como la versión de generación por defecto, incorporando música, presentación y editorial modificable.

## 1. Objetivo de producto

La rama D no debe reimplementar las mecánicas ni reabrir el motor congelado de C. Debe conservar el camino de generación existente que funciona y añadir una capa D encima/alrededor de su frontera de producción: selección/solicitud universal, configuración editorial efectiva, composición/presentación, música y delivery. CLI y GUI deben llamar al mismo servicio canónico, recibir resultados equivalentes y producir artefactos comprobables.

Las tres familias del alcance D son:

1. **Challenge**: nueve selectores (`CHALLENGE_001` a `CHALLENGE_009`), con identidad de variante y semántica/campos específicos.
2. **Visual Loops**: cinco familias y 27 gramáticas concretas; `auto` es un selector, no una gramática concreta.
3. **Visual Drills**: cuatro tipos y 20 variantes tipo/tier.

Longform queda fuera de D hasta que el contrato lo soporte explícitamente. `CHALLENGE_008` y `CHALLENGE_009` no entran en el primer render de integración si sigue activa la discrepancia 11 s declarados frente a 12 s en la suma de fases.

## 2. Baseline C: conducta que debemos reproducir

La aceptación C de referencia combinaba pruebas lógicas, producción física, cobertura de familias, determinismo, revisión A/V y controles del repositorio. No se consideraba un vídeo correcto solo porque `self_test.py` estuviera verde.

- La geometría social lógica C es 540×960; la entrega de revisión habitual es 720×1280 a 30 FPS. La estructura conocida de Header/Body/Footer es 0–144 / 144–816 / 816–960 en el marco lógico, pero la integración D debe verificar los contratos vivos y no recalcularla a partir de un screenshot.
- Challenge tiene una matriz física heredada de 54 ejecuciones (9 retos × 6 casos de semilla, según `tools/qa/c11/run_c11c_challenge_bulk_qa.ps1`). No cambiar los seeds, orden ni los controles A/B sin revisar ese runner y su contrato.
- El corpus de revisión histórico C contiene 27 Loops + 20 Drills + 5 Longforms = 52 vídeos y usaba workers Godot aislados; para la matriz D de scope soportado se conservan solo las 27 gramáticas de Loop y las 20 variantes de Drill.
- El humo de cobertura que se documentó en el trabajo C usa 23 productos. Para D el equivalente útil es 9 Challenge + 5 Loops representativos + 4 tipos de Drill = 18 productos. No es el gate final.

Runners históricos que se deben inspeccionar antes de ejecutar (leer parámetros y salidas primero; no asumir opciones):

- `python -u .\c11c-suite\self_test.py`
- `python .\tests\run_all.py`
- `python .\c11c-suite\c11c-test\self_test.py` y rutas del manifest de Test
- `tools\qa\c11\run_c11c_challenge_bulk_qa.ps1`
- `tools\qa\c11\run_c11c_complete_video_review.ps1`
- `c11c-suite\c11c-test\run_c11c_complete_video_review.bat`

Se reutilizan los runners que correspondan en una copia de trabajo y con salidas aisladas. No se debe disparar por defecto la batería C completa en el mismo directorio de salida que el smoke D.

## 3. Estado D demostrado y brecha funcional

### D ya existe dentro de su alcance

- D9.8: Universal Editorial Model y resolver con herencia `global → content_type → family → subtype → variant → production_override`.
- D9.9: creación canónica de solicitudes/planes para Challenge, Loop y Drill; paridad GUI/CLI en las pruebas registradas.
- D9.10: bridge/adapter de planificación, pero el adapter sigue siendo `PREPARE_ONLY` y **no es un dispatcher**.
- D3/V5 y las rutas D de audio contienen motor musical y evidencias audiovisuales acotadas; `request.seed` y `request.music_seed` deben seguir separados.
- Los contratos de request-scoped binding, payload preview, logical composition, frame program y candidate I/O son activos que hay que inspeccionar y reutilizar antes de inventar otro binder.

### Aún no demostrado

- La identidad del inventario histórico del renderer declara `renderer_implementation=NOT_IMPLEMENTED` y `renderer_build_artifact=NONE`.
- Auditoría editorial: cadena de revisión 14/14 pero payload visual consume 0/14 campos; el sidecar no prueba que el texto se dibuje.
- El registro V2.2 del 27-10-2026 valida joins de requests/payload/sidecar para tres fixtures, pero vuelve a declarar `visual_payload_consumed=0/14`, `candidate_input_admissible=false` y `renderer=OFF`.
- La cualificación D9.14 histórica produjo cuatro MP4 A/V bajo una autorización acotada para generadores existentes de C; no certifica renderer D universal ni aceptación de las tres familias completas con la nueva editorial visual.
- Un test de contrato o un harness Godot de frames fuente no es un MP4 final aceptado.

Por eso, la primera tarea no es crear otro contrato de auditoría: es localizar el punto de integración real y conectar ahí las capas D, conservando las implementaciones protegidas de C.

## 4. Arquitectura objetivo

```text
CLI ───────────┐
               ├── D canonical production service ── D request/catalog/profile resolution
GUI Producer ──┘                                   ├─ effective editable editorial values
                                                   ├─ existing C generator/mechanics (unchanged)
                                                   ├─ D-owned presentation/visual consumer
                                                   ├─ D3 music engine (independent music seed)
                                                   └─ delivery/mux/validation ── MP4 + evidence manifest
```

El esquema describe la dirección, no afirma que todos los módulos estén ya conectados. El primer análisis de código debe identificar los entrypoints, las interfaces reales y las fronteras protegidas. La solución preferida es añadir/consumir componentes D fuera del conjunto congelado de C y reutilizar el backend existente allí donde el contrato de C siga siendo el esperado. No modificar `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector`, `RenderedFrameStream`, RNG, mecánicas, `core/`, `assets/`, `scenes/`, `scripts/`, `challenges/` o contratos protegidos sin una justificación/versionado y las reglas del repositorio.

Superficies operativas únicas: `c11c-test`, `c11c-producer`, `c11c-catalog`, `c11c-config`, `c11c-maintenance`. La GUI y la CLI deben invocar el mismo adaptador/servicio. No crear `c11d-control`, `c11c-studio` ni otra suite.

## 5. Fases funcionales y puertas de salida

### Fase 0 — Verificar el checkout activo (una vez)

- Comprobar que el directorio es el repositorio indicado.
- Verificar los hashes pinneados de `AGENTS.md`, `CONTINUE.md`, manifiesto C, ledger V18, checkpoint V41 y prompts V41. El script exporter también debe comprobar el manifiesto C.
- Revisar el cierre de AD instalado y anotar que sus 60/60 tests no se repiten mientras las fuentes permanezcan idénticas.
- Tomar un inventario del código de producción, perfiles/selector, generadores, servicios compartidos, escenas/renderer, música/mux, manifest de Test y launchers QA.
- Confirmar que todo output de trabajo va a carpeta temporal aislada y que no se escribe en un directorio de release.

**Salida:** inventario de entrypoints y mapa de flujo C→D con rutas y hashes. Esto debe formar parte del mismo expediente técnico de integración, no una fase de gobierno nueva.

### Fase 1 — Revisar la frontera real C→D y cerrar la especificación mínima

Inspeccionar en código y contratos existentes:

1. Cómo crea el productor C una unidad Challenge/Loop/Drill y cuál es su identidad completa (selector, variante, grammar o tipo/tier, profile/duration/FPS).
2. Cómo D9.9 obtiene solicitud/plan canónico y cómo D9.10 prepara el envelope.
3. Dónde ocurre la composición visual final en el renderer C existente, qué campos recibe y qué punto D puede consumir sin mutar el motor congelado.
4. Cómo `title`, `subtitle`, `call_to_action`, `language` y los campos Challenge `player_name`, `challenge_label` deben llegar desde el modelo editorial a la salida visual.
5. Cómo se genera música, se crea el audio, se muxea al MP4 y se valida su presencia/sonoridad. Gameplay seed y music seed tienen propietarios separados.
6. Qué reglas de timebase, layout, visibilidad y crop ya están fijadas por un contrato C existente y pueden heredarse tal cual. Si hay delta D real, registrar solo ese delta y elegir un valor basándose en un contrato/decisión explícitos; no inventar números por conveniencia.

El objetivo es el **mínimo contrato de integración que permita construir y probar**, extendiendo el contrato canónico existente. No crear un binder paralelo. La semántica registrada para cuatro campos Challenge permite especificación futura, no aprueba por sí sola bindings de ejecución. En el primer scope evitar 008/009 y cualquier campo cuya semántica no tenga una fuente válida.

### Fase 2 — Implementar el consumer/compositor visual D

- Añadir una implementación de capa D con ruta/identidad propias, fuera de los archivos C protegidos.
- Convertir los valores editoriales ya resueltos en elementos visuales consumidos por el compositor, siguiendo regiones y comportamiento existentes y verificados.
- Los valores deben ser modificables por el modelo editorial y el override de producción; los cambios de texto deben ser observables en frames, no solo en request/sidecar hashes.
- No permitir que valores editoriales muten mecánica, telemetry, provenance, seeds o simulation truth.
- Añadir tests del consumer: campo permitido, alcance por tipo/variante, ventana de aparición/ocultación, ausencia o invalidación, escaping/encoding de texto, longitud extrema y paridad canonical request→render props.
- Si la interfaz existente no permite una integración sin tocar una zona protegida, documentar el archivo y la frontera exactos, proponer un wrapper D-only y detenerse solo en ese bloqueo específico.

**Criterio:** el consumer recibe los valores correctos y los expone al renderer real, con tests focalizados. No basta con sidecar parity.

### Fase 3 — Integración audiovisual D del primer MP4

- Usar un run ID único bajo `artifacts/tests/c11d_d_render/<run_id>/` o un directorio temporal equivalente; no utilizar release ni producción final.
- Generar un Challenge no bloqueado (empezar por `CHALLENGE_001`; extender luego el caso de target a `CHALLENGE_003` tras revisar su mapping).
- Generar un Visual Loop representativo: fixture existente `c11c_geometric_waves_v1 / harmonic_membrane`.
- Generar un Visual Drill representativo: `tracking / tier-2`.
- Para cada fixture, generar al menos dos salidas con datos de editorial diferentes y verificar mediante frames muestreados que los cambios esperados aparecen en la capa D.
- Exigir MP4 legible, resolución/FPS/duración dentro del perfil declarado, audio estéreo real cuando el perfil lo requiere, WAV/receipt y fuente/música con hashes correctos, mux final y manifiesto de output completo.
- Guardar logs stdout/stderr separados, exit code real, toolchain exacta, hashes de source, input/request/editorial/music/audio/video y resultado del auditor. Nunca emitir PASS si falta un artefacto requerido.

**Criterio:** 3 tipos físicos aceptados; la variación editorial aparece visiblemente; música y seeds están separadas; la ejecución es reproducible.

### Fase 4 — Smoke de cobertura D (18 salidas)

| Familia | Cobertura | Vídeos |
|---|---|---:|
| Challenge | Cada uno de los 9 selectores una vez | 9 |
| Visual Loop | 5 familias, una gramática canónica por familia | 5 |
| Visual Drill | 4 tipos, un tier canónico por tipo | 4 |
| **Total** | **Cobertura de catálogo, no matriz completa** | **18** |

Para cada salida exigir un archivo real, un informe de validación, salida audiovisual consistente con el manifest, y una revisión visual de forma/region/overlays. Esto es el smoke rápido de la suite D, equivalente funcional a la cobertura de familias, no la puerta final.

### Fase 5 — Matriz completa de productos soportados (101 salidas base)

| Familia | Matriz | Vídeos |
|---|---|---:|
| Challenge | 9 selectores × 6 casos heredados de semilla | 54 |
| Visual Loop | 27 gramáticas concretas | 27 |
| Visual Drill | 4 tipos × 5 tiers | 20 |
| **Total** | Longform excluido; 008/009 solo cuando su conflicto haya sido resuelto | **101** |

Reutilizar la matriz de semillas/variantes del runner canónico C exactamente, sin reordenar ni asignar significados a los sufijos de caso sin leer el contrato. La tabla indica los tamaños de la matriz, no garantiza que todas las combinaciones sean admisibles con el contrato D actual. Si el gate activo excluye una combinación, registrar `BLOCKED` con causa y continuar las filas permitidas; no cambiar el selector/catálogo para forzarla.

Pruebas añadidas a la matriz:

- Repetición bit-a-bit o equivalencia visual/audio según el contrato y el nivel de determinismo de cada tipo.
- Gameplay seed cambia la simulación/payload esperado; music seed cambia solo el dominio musical y no contamina gameplay/visual state.
- Reproducción desde Catalog y lineage/provenance.
- Duración, frames, FPS, dimensiones, audio presente/ausente según perfil, loudness no silencioso, integridad del MP4 y outputs únicos.
- Rechazo de selector/variante/tier inválido y de seeds inválidas/colisiones entre dominios.
- Revisión visual de todas las 101 salidas, con selección/golden comparisons automáticas donde los contratos definan tolerancia y revisión humana para texto/layout.

### Fase 6 — Paridad CLI/GUI y aceptación de las cinco superficies

- CLI y GUI pasan por el mismo servicio de producción. No duplicar la cadena de render o composición en callbacks Qt.
- Ejecutar una generación equivalente por CLI y GUI de cada familia y comparar request identity, effective editorial values, content/catalog/profile identity, music configuration, seed ownership, artefactos y reportes.
- Registrar la aceptación operativa de Producer/Test/Catalog/Config/Maintenance con evidencia observable apropiada; un test offscreen no demuestra que un operador haya visto la GUI.
- Ejecutar las pruebas focalizadas afectadas por los cambios y después las regresiones agregadas `python -u .\c11c-suite\self_test.py`, `python .\tests\run_all.py`, los checks de Producer/Test GUI y baseline candidate.
- Incluir el test de render en el test registry/run manifest por la forma definida por `c11c-test/BUILD_MANIFEST.json`, sin crear una superficie nueva.

### Fase 7 — Baseline D, freeze y cambio de default

El cutover funcional es que los comandos normales del Producer generen mediante D. El freeze/promotion es un evento independiente, solo cuando las puertas obligatorias hayan sido aceptadas. Antes de cambiar el default: ejecutar candidate preflight completo, confirmar fuentes protegidas C, validar los 101 medios, GUI/CLI parity, D9.14, D9.15, D9.16, D9.17 y D10, crear una identidad/manifest exactos del código D aceptado y emitir una decisión de baseline separada. C11-C permanece disponible e inmutable como referencia, no se sobrescribe.

## 6. Cómo tratar los gates sin convertirlos en un bucle documental

El usuario declaró explícitamente autorización de operador para seguir probando renders en esta conversación. Esto autoriza avanzar en el trabajo de prueba como objetivo de ingeniería; no convierte en aprobado un campo de estado del checkout ni autoriza release/promoción.

Mantener cada gate fiel a su alcance:

- **Contrato PASS** significa que el contrato pasa sus tests.
- **Harness Godot PASS** significa que ese harness y sus fuentes se comportan según su prueba.
- **MP4 físico PASS** requiere un output real inspeccionado/probado.
- **D9.14** tiene una cualificación histórica limitada para generadores existentes de C; no se debe presentar como la aceptación del renderer D universal.
- **D4.8/D9.17/D10** no pueden autoaprobarse por un test o por este plan. Si una puerta técnicamente impide ejecutar el test físico, comprobar si el contrato autoriza un modo de prueba aislado. No desactivar el gate mediante patch ni editar booleans. Si no existe esa ruta, producir la mínima evidencia concreta del bloqueo y resolver ese gate exacto, no crear fases genéricas adicionales.
- Las decisiones R-01..R-07 deben heredar las decisiones C explícitas cuando la conducta sea exactamente la misma; registrar y resolver solo diferencias introducidas por D. R-08/009 siguen apartadas mientras exista la discrepancia temporal conocida.

## 7. Evidencia y logs que cada ejecución debe guardar

Bajo un `run_id` único, en directorio temporal o `artifacts/tests/c11d_d_render/`:

- `run_manifest.json` con selector/variant/grammar/type-tier, seeds separados, perfil, duración/FPS, identidad de request, campos editoriales efectivos, source pins, versión del código y fecha.
- `stdout.txt`, `stderr.txt`, exit code y comando exacto.
- MP4 final y sidecars de audio/receipt necesarios para la auditoría (solo en la carpeta de test).
- salida de `ffprobe`/FFmpeg para codec, dimensiones, frame rate, duración, canales y sonoridad.
- `sampled_frames/` o un manifiesto de frames revisados, con hashes; no es necesario duplicar el vídeo dentro de la carpeta de reportes.
- hashes SHA-256 de todos los artefactos y un JSON de resultado por fila.
- comparaciones de repetición/variación editorial y resultados de negativos.

Los logs se capturan desde el proceso real con stdout/stderr separados y `exit code`; no inferirlos desde un resumen, ni crear recibos de un PASS que no haya sucedido.

## 8. Primera tarea tras aplicar el overlay

1. Ejecutar el `VERIFY` del overlay de documentación.
2. Crear el snapshot con una sola orden: `tools/c11d/packaging/New-C11DWorkingSnapshot.ps1`. El script localiza el checkout a partir de su propia ruta, verifica el manifiesto C, filtra rutas no aptas y deja el ZIP, `.sha256` e informe `.report.json` fuera del repositorio. El modo `-PreflightOnly` es opcional si antes se quieren inspeccionar los conteos sin escribir archivos. No subir el ZIP histórico del 28-10.
3. Con el informe del snapshot, revisar primero los entrypoints C que el bulk QA llama y el entrypoint D/Producer existente. Capturar el diagrama real C→D con caminos y source hashes.
4. Revisar los contratos ya existentes de payload/request/editorial y escoger el seam de composición. No volver a ejecutar auditorías de todo el catálogo sin cambios.
5. Implementar un pequeño incremento D-only sobre ese seam y pasar de inmediato a los tres MP4 del smoke de integración.

La salida esperada de la siguiente fase es una diferencia de código D, tests de consumer y tres vídeos reales inspeccionados; no otro paquete cuyo único resultado sea `PREPARATION_ONLY`.

## 9. Límites que no cambian

- C11-C 2.19.12 y el manifiesto congelado permanecen byte-for-byte inmutables hasta la aceptación formal y eventual promoción de D.
- No materializar dentro de `SimulationResult` ni serializar entero `FrameSnapshot.custom_data`.
- `winning_frame` es ancla temporal; `close_calls` es conteo de episodios, no tiempo ni identidad del primer impacto.
- Los dominios `request.seed` (juego) y `request.music_seed` (música) son independientes; no compartir estado.
- No crear `c11d-control`, `c11c-studio` ni una sexta suite.
- Longform fuera de alcance. CHALLENGE_008/009 mantienen bloqueo si la discrepancia 11s/12s no se resuelve con fuente válida.
- Sin release, promoción ni freeze por el hecho de que se genere un MP4 de test.
