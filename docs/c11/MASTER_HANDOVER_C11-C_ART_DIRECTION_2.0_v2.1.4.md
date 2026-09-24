# MASTER HANDOVER — C11-C ART DIRECTION 2.0

**Estado:** READY FOR ART DIRECTION 2.0  
**Toolchain consolidado:** C11-C v2.1.4  
**Fecha:** 2026-09-22  
**Baseline de ingeniería:** C11-B CLOSED / CERTIFIED / FROZEN

## 1. Objetivo de este handover

Este documento fija el punto de entrada de la siguiente ventana de contexto. La infraestructura C11-C queda fuera de la dirección artística salvo que aparezca un bug real de ejecución.

La siguiente fase debe trabajar sobre un corpus físico de **25 Visual Loops**: 5 variaciones por familia, con las mismas 5 seeds compartidas entre las cinco familias cuando se utilice una tanda comparativa.

## 2. Frontera de ingeniería

No reabrir C11-B ni modificar:

- matemática de mecánicas y simulación;
- RNG estructural o ownership determinista;
- `SimulationResult`;
- `winning_frame`;
- `close_calls`;
- contratos C7 de audio;
- contratos C9 de authoring;
- geometría C11-B Header / Body / Footer como contrato lógico.

C11-C es presentación/art generative sobre ese baseline.

## 3. Estado visual actual

Existen exactamente cinco familias:

| Familia técnica | Nombre artístico | Núcleo visual |
|---|---|---|
| `geometric` | **Geometric Waves** | ondas, interferencia, geometría armónica |
| `fractal` | **Fractal Bloom** | fractales, ramificación, zoom, universo microscópico |
| `kaleidoscope` | **Sacred Symmetry** | simetría radial, anillos, mecanismo astronómico |
| `particle_flow` | **Living Particles** | partículas, atractores, flujos y remolinos |
| `vector_field` | **Invisible Forces** | trazas, campos, cuencas y fuerzas invisibles |

ADN común: matemática generativa premium, fondo oscuro/abyssal, trazos de luz, color controlado, movimiento elegante, determinismo y ausencia de aspecto de screensaver.

## 4. Cambios consolidados hasta v2.1.4

### Editorial

- Header con línea factual grande y hook grande.
- Hook con transición determinista tipo Matrix / airport split-flap alrededor del centro temporal.
- Footer reducido a telemetría/generación; no repite `VISUAL LOOP // FAMILY`.
- Recuperadas las líneas decorativas de Header y Footer.
- Tipografía y elementos editoriales vuelven a utilizar los colores de la paleta efectiva de cada seed/familia.
- Technobabble ampliado con vocabulario cyberpunk/geek/steampunk y parámetros reales de la variación.

### Color

Se aplica un aumento editorial de viveza/saturación/luminancia manteniendo la identidad cromática de cada colorway. La finalidad es conservar legibilidad y presencia en pantallas móviles.

### Audio

El audio por defecto es un ambiente determinista de baja intrusión. Se sustituyó la sensación de beep/test por drones, armónicos suaves y movimiento lento. Se evita el efecto de resonancia/acople molesto percibido en altavoces móviles.

`-NoSound` y `-Silent` producen un único MP4 sin audio. El modo normal produce un único MP4 con audio. No debe quedar `_silent.mp4` como producto adicional.

### Entrega social

- Resolución física de entrega: **720x1280**.
- Formato: 9:16.
- 30 FPS.
- Baseline temporal de review: 18.00 s / 540 frames.
- Se genera sidecar social con descripción, hashtags, seed y comando exacto de reproducción.

### Producción

Los productos finales están separados de review/prototype bajo:

`artifacts/production/audiovisual/<family>/<product>/`

La limpieza de review/prototypes no debe tocar producción.

### Toolchain

Se consolidó el flujo para evitar cadenas frágiles de `powershell.exe -File` y transporte incorrecto de arrays/switches. Los parámetros entre scripts PowerShell se mantienen tipados/directos.

Se añadió validación de parseo PowerShell y validación específica de entrega 720x1280.

## 5. Validación física cerrada antes de esta fase

En Windows con Godot 4.7.1:

- `godot --headless --path . --editor --quit` completó el escaneo/carga.
- `validate_c11c_powershell.ps1` completó **17/17 scripts canónicos**.
- `validate_c11c_delivery_configuration.ps1` dio PASS.
- El launcher canónico de review ya llegó al punto correcto de captura y el problema anterior de resolución quedó corregido con formato `720x1280`.

## 6. Corpus de revisión para Art Direction 2.0

Objetivo inmediato:

**25 vídeos = 5 seeds × 5 familias.**

Cada seed se aplica a todas las familias para permitir comparación transversal.

El corpus debe contener:

- MP4;
- GIF/review assets cuando corresponda;
- keyframes;
- manifest/metadata;
- social sidecar;
- logs de render.

No hacer limpieza automática durante la generación.

## 7. Criterios de Art Direction 2.0

La revisión debe centrarse en:

1. impacto inmediato en móvil;
2. viveza y contraste real de color;
3. jerarquía Header / Body / Footer;
4. calidad y discreción del hook animado;
5. sensación premium y diferenciación entre familias;
6. ausencia de aspecto de screensaver;
7. riqueza de variación entre seeds;
8. coherencia entre metáfora artística y matemática real;
9. legibilidad de telemetría sin competir con el protagonista visual;
10. comportamiento del audio como capa ambiental, no protagonista.

No convertir estas observaciones en cambios de ingeniería hasta haber agrupado los hallazgos por familia.

## 8. Duración — fuera de esta revisión

El corpus actual usa 18 s como baseline común para estabilizar la revisión. La duración variable **NO** debe implementarse ahora.

Trabajo futuro separado: asociar determinísticamente una duración corta/media/larga a gramática/seed/estructura, garantizando siempre ciclos enteros y cierre perfecto del loop, sincronización audiovisual y telemetría correcta.

## 9. Ruta de trabajo en la siguiente ventana

**PASO A —** revisar los 25 vídeos físicos.  
**PASO B —** registrar hallazgos por familia y por seed.  
**PASO C —** separar problemas universales de problemas específicos de familia.  
**PASO D —** definir Dirección de Arte 2.0 como contrato, no como colección de parches.  
**PASO E —** implementar solo después de aprobar el contrato.  
**PASO F —** regenerar un corpus de validación y comparar contra esta baseline.

## 10. Regla de estabilidad

A partir de este punto, un cambio que no sea necesario para corregir un fallo demostrado no debe entrar en el toolchain durante la revisión artística.

**Punto de entrada oficial de la siguiente ventana: C11-C v2.1.4 + corpus de 25 renders de Art Direction 2.0.**
