# C11-C CHANGELOG — v2.0.1 → v2.1.4

## Resumen

Esta etapa evolucionó C11-C desde el primer paquete editorial/audio hasta un toolchain estable para entrega social, revisión visual y producción protegida.

> Nota: el nombre solicitado históricamente `v2.0.1 → v2.1.2` queda superseded por esta edición consolidada, que incorpora además las correcciones posteriores imprescindibles hasta **v2.1.4**.

## v2.0.1 — Editorial + audio + sidecar

- Header editorial con datos reales de variación.
- Hook de línea 2 con transición determinista.
- Footer de telemetría.
- Technobabble cyberpunk/geek/steampunk.
- Parámetros reales incrustados en textos.
- Audio ambiental determinista, inicialmente a 18 s.
- `-NoSound`.
- Social sidecar con metadatos y comando de reproducción.
- 20 colorways por familia.
- Invisible Forces con `pulse_speed` continuo.
- Loop baseline: 18 s / 540 frames.

## v2.0.2 — Editorial animator hotfix + cleaner

- Corrección de referencia `C11CEditorialAnimatorClass` mediante preload directo.
- Cleaner de artifacts para medios regenerables.
- Protección de evidencia C11.

## v2.0.3 — Shader + cleaner hotfix

- Corrección de identificador `C11C_TAU` → constante local de shader.
- Corrección de sintaxis del cleaner.

## v2.0.4 — Social delivery/editorial polish

- Líneas decorativas recuperadas conceptualmente para el sistema editorial.
- Color editorial ligado a paleta.
- Footer deja de repetir la identidad de familia.
- MP4 único con audio / MP4 único sin audio.
- Manejo UTF-8 BOM en social metadata.
- Base de entrega social preparada para 720x1280.

## v2.0.5 — Bulk + artifact reset

- Corrección de variables de Fractal Bloom (`color_phase`, `color_diversity`).
- Reset separado del workspace regenerable.
- Intento inicial de desacoplar review de cleanup automático.

## v2.0.6 — Mobile/social hotfix

- Resolución social objetivo 720x1280.
- Color más vivo/saturado para móvil.
- Audio ambiental de menor riesgo de resonancia en altavoces móviles.
- 12 posts de redes sociales.

## v2.0.7–v2.0.9 — Toolchain repair

- Corrección de errores de scripts PowerShell.
- Separación cleaner/review.
- Corrección de paso de switches.
- Corrección de cierres prematuros mediante `exit`/`return`.
- Reducción progresiva de lanzadores versionados.

## v2.1.0–v2.1.2 — Workspace / production separation

- Validación estática de PowerShell.
- Workspace regenerable C11-C separado de producción.
- Producción persistente bajo `artifacts/production/audiovisual`.
- Protección frente a sobrescritura accidental.
- Documentación de toolchain y handover.

## v2.1.3 — Consolidation

- Eliminación de invocaciones frágiles de `powershell.exe -File` entre scripts.
- Transporte directo/tipado de arrays de seeds.
- Canonicalización de comandos de review y production.
- Retirada de launchers versionados obsoletos.

## v2.1.4 — Toolchain final fix

- Corrección definitiva del argumento Godot `--resolution` a formato único `720x1280`.
- Revisión de todas las referencias de resolución en las cinco familias.
- Revisión de parámetros PowerShell entre orchestrators.
- Validación de toolchain canónico.
- Review preparado para 25 renders reales.

## Estado final de esta rama

### Arte

C11-C tiene cinco familias diferenciadas y una identidad común de mathematical generative art.

### Vídeo

Entrega objetivo: 720x1280, 30 FPS, 9:16. Baseline temporal de revisión: 18 s.

### Audio

Ambiental, determinista, suave y opcional.

### Metadata

Cada pieza puede conservar manifest, authoring, FFprobe, Godot log y social sidecar.

### Artifacts

Review/prototype es regenerable. Production queda fuera de las limpiezas de review.

## Próximo checkpoint

**C11-C ART DIRECTION 2.0**

Entrada: corpus de 25 vídeos, 5 seeds × 5 familias.  
Salida esperada: contrato DA 2.0 antes de nuevas modificaciones de implementación.
