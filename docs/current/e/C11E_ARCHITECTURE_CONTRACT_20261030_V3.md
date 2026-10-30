# C11-E — contrato de arquitectura e integración

**Versión:** V3 · **Fecha:** 2026-10-30 · **Base técnica:** snapshot `C11D_WORKING_CONTEXT_20261029_203557.zip` y slice de checkout activo 2026-10-29.

## 1. Pipeline objetivo

```text
Producer GUI ─┐
              ├─> C11E Production Service ─> Canonical Request / Resolver
Producer CLI ─┘                                  │
                                                 ├─> Challenge Adapter ─> C Challenge Generator/Frames
                                                 ├─> Loop Adapter ──────> C Loop Generator/Frames
                                                 └─> Drill Adapter ────> C Drill Generator/Frames
                                                                  │
                                             E Editorial Presentation Context
                                                                  │
                                              Existing C family visual consumer
                                                                  │
                                                  Godot Movie Maker capture
                                                                  │
                                    optional D3 music ─> FFmpeg A/V mux/encode
                                                                  │
                                              FFprobe + semantic validation
                                                                  │
                                                   E Run Receipt / Output MP4
```

El servicio único normaliza/valida, resuelve editorial y selecciona un adaptador. No debe convertirse en un segundo productor paralelo: es la fachada común sobre runners C existentes y módulos D reutilizables.

## 2. Fuentes y puntos de integración ya identificados

### Productor y solicitud

- `c11c-suite/c11c-producer/main.py`: mantiene rutas físicas C (`_run_challenge_job()` / `_run_content_job()`) y la pestaña de planificación D. La revisión detectó que el flujo D no llama a los launchers físicos.
- `c11c-suite/c11c-producer/c11d_gui_request.py`: adaptador de request GUI D.
- `tools/c11d/d9/universal_producer.py`: normalización y resolución de request editorial universal.
- `tools/c11d/d9/universal_editorial_model.py`: modelo universal y resolución de valores.
- `tools/c11d/d9/shared_production_context_service.py` más adapters GUI/CLI: infraestructura compartida preexistente; contrato y comportamiento actuales son preparation-only, no equivalen a dispatch.
- `tools/c11d/d9/editorial_render_bridge.py` y `d_render_adapter.py`: D9.10 prepara registros/envelopes y hashes, con `renderer_input_emitted=false`, `renderer_dispatch_invoked=false` y `PREPARE_ONLY`. E no debe fingir que ya producen media.

### Challenge

- Launcher físico: `tools/prototypes/c11c_bulk/run_c11c_challenge_production.ps1`.
- QA wrapper: `tools/qa/c11/run_c11c_challenge_bulk_qa.ps1`.
- Consumidor visual: `core/presentation/ChallengePresentationBinder.gd`, con `build_frame_render_model(...)`; el binder construye claves como `hook_text`, reveal y CTA a partir del contenido/estado C.
- E debe pasar su contexto editorial por un adaptador explícito al consumidor Challenge. No mutar la definición canónica del challenge en disco, ni contaminar la copia efectiva usada para la mecánica.

### Loop y Drill

- Producer Loop/Content launchers y sus generadores se localizan en `tools/prototypes/c11c_bulk/`.
- Drill launcher: `c11c-suite/c11c-producer/run_visual_drill_production.ps1`.
- Consumidores: `VisualLoopPresentationBinder.gd`, `VisualDrillPresentationBinder.gd`, `VisualContentPlayer.gd` y `C11CVisualEditorialLayer.gd`.
- Loop y Drill tienen modelos editoriales distintos. El código de Drill construye editorial context, header/footer, CTA, intro y estado propio; se debe preservar su precedencia temporal (por ejemplo END_CTA) y no sobrescribir textos de fase accidentalmente.

## 3. Regla del consumidor visual

El flujo correcto es `request.editorial` validado → `EEditorialPresentationContext` con identidad/hash → adapter de familia → slot/propiedad del modelo visual → frame capturado. El contexto no se serializa dentro de `custom_data` ni se propaga como metadatos no consumidos.

El primer caso de prueba propuesto es `CHALLENGE_001` + `title`, por reducir superficie de integración y evitar los IDs 008/009. Antes de modificar código se inspeccionarán en el checkout activo el launcher, escena y binder realmente utilizados por ese challenge. Se fijará el punto exacto de composición y se determinará si el título se muestra en HOOK, GAME, REVEAL o una región común. No se asumirá que `title` equivale semánticamente a `hook`, `reveal` o `cta`.

La presentación lógica C conocida es 540×960, con HEADER y=0..144, BODY y=144..816 y FOOTER y=816..960; entrega social típica 720×1280, 30 FPS (escala 4/3). Se hereda cuando el perfil de salida seleccionado lo establece. No se cambia geometría, tipografía, safe areas ni timing para conseguir que una prueba pase.

## 4. Contrato de request

El request canónico E debe contener, como mínimo:

- `request_id` estable y único.
- `family` y selector exacto (Challenge ID / Loop ID + grammar / Drill subtype + variant).
- `seed` de gameplay explícita, sin coerción ni generación automática.
- `music_seed` separada y usada únicamente por la música D3.
- `delivery_profile` y `editorial_profile` resueltos de fuentes autorizadas.
- `editorial` con campos allowlisted, normalizados, longitud y charset validados.
- `source_identity` (commit, contrato/model version, hash del editorial efectivo).
- `output_root` aislado y política de overwrite explícita (por defecto, no overwrite).

El resolver debe conservar `raw_request`, valores normalizados, defaults efectivos, campos omitidos y hashes. El recibo debe permitir reproducir exactamente la entrada.

## 5. Campos editoriales y compatibilidad

Los campos del modelo universal no se proyectan en todos los targets por similitud de nombres. Se crea una matriz `field × family × phase × visual slot` y cada celda tiene estado `SUPPORTED`, `UNSUPPORTED`, `CONDITIONAL` o `NOT_YET_VERIFIED`. Los campos no soportados se rechazan o se marcan explícitamente como no consumidos; nunca se ignoran silenciosamente.

`language` puede permanecer como metadata según el modelo D existente; no se trata como texto visible a menos que una política E lo habilite. `title` es el primer campo candidato de prueba. `subtitle`, `call_to_action`, `player_name` y `challenge_label` se habilitan después de mapear y validar sus semánticas por familia.

## 6. Semillas y determinismo

- C recibe `seed` como dominio mecánico; E no altera el RNG de C ni deriva semillas a partir de `music_seed`.
- D3 recibe `music_seed`; el audio no cambia frames, duración ni resultado del juego.
- Las semillas se guardan explícitamente en request y receipt.
- Prueba visual editorial: mismo Challenge, mismo seed, mismo profile, mismo request excepto por `title`. La expectativa es gameplay idéntico y únicamente los píxeles del slot editorial difieren.
- Prueba A/V: mismo vídeo fuente y mismo `music_seed` debe generar/muxear el mismo resultado cuando la toolchain sea determinista; el receipt declara versiones y cualquier fuente de nondeterminism.

## 7. Render y audio

El launcher C continúa siendo responsable de ejecutar la familia y capturar frames. E añade contexto editorial por una interfaz explícita y no intrusiva. En audio, reutilizar `tools/c11d/d3/c11d_music_engine_v5.py` solo tras comprobar su API y entradas reales en el checkout; los pilotos D9.2 prueban que hubo un camino D3+FFmpeg en otro contexto, no que el formulario universal controle hoy el audio.

Orden recomendado de output:

1. Render temporal sin audio o con audio desactivado para aislar el transporte editorial.
2. Validación del vídeo intermedio (resolución, FPS, duración, conteo de frames, stream de vídeo).
3. Generación de audio mediante `music_seed` y mux/encode FFmpeg.
4. Validación final FFprobe (streams, codecs, duración, sample rate/canales si aplica, timestamps, tamaño no nulo) y checks de integridad.

La evidencia debe preservar video intermedio, WAV cuando corresponda, MP4 final, logs y hashes. Limpieza no elimina evidencia aprobada.

## 8. Suite y APIs

Se conservan exactamente cinco superficies. El usuario opera Producer; Test ejecuta preflights/regresión; Catalog consulta receipts/media validados; Config inspecciona perfiles/contratos; Maintenance gestiona documentación/artefactos. No se crea módulo adicional ni ruta paralela fuera de `c11c-suite`.

CLI y GUI llaman al mismo `C11EProductionService` (nombre provisional de diseño, a fijar según convenciones del repo). La lógica de normalización, resolución, seeds, selección de runner, salida y receipt reside en el servicio y sus adaptadores, no en handlers GUI/CLI duplicados.

## 9. Compatibilidad con C

No modificar: `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector`, `RenderedFrameStream`, gameplay RNG, definición canónica o timeline de mecánica, catálogo de mecánicas ni geometría congelada. No modificar el paquete congelado ni su manifest.

Cambios permitidos en E: nuevos módulos `tools/c11e/` (si la convención del repositorio lo permite), tipos/validators/receipts nuevos, adaptadores de request a los slots visuales ya existentes, wrapper/dispatcher compartido y tests. Los cambios a consumidores visuales compartidos se harán como cambios aditivos compatibles, con pruebas C previas/posteriores y sin alterar la salida cuando el contexto E está ausente.

## 10. Evidencia requerida por render

Por cada render: commit y branch; request original + normalizado; perfiles/contratos/hashes; semillas separadas; familia/selector; command line; exit codes; stdout/stderr separados y sus hashes; source/intermediate/final hashes; Godot/FFmpeg/FFprobe versions; resolución/FPS/frame count/duración; audio streams; resultado del diff editorial; regresión mecánica; path aislado; review visual humana documentada.
