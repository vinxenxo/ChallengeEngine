# VIDEO_SPECIFICATION.md — ESPECIFICACIONES DE VÍDEO Y PIPELINE

## 1. Especificaciones Técnicas del Master

| Parámetro | Valor Máster / Regla |
| :--- | :--- |
| **Resolución** | $1080 	imes 1920$ píxeles |
| **Relación de Aspecto** | 9:16 (Vertical Estricto) |
| **Framerate Target** | 60 FPS (configurable por JSON) |
| **Formato de Píxel** | YUV420p (obligatorio para compatibilidad móvil) |
| **Códec de Vídeo** | H.264 / MP4 |
| **Códec de Audio** | AAC (192 kbps) |

---

## 2. Invocación de Renderizado Offline

La factoría calcula `--quit-after` desde el timeline declarativo de cada challenge. El valor no debe fijarse manualmente a 660 frames cuando el challenge utiliza otra composición temporal.

Ejemplo conceptual:

```text
godot [renderer de producción] \
  --write-movie output/CHALLENGE_XXX_raw.avi \
  --fixed-fps <fps> \
  --quit-after <total_frames_calculado> \
  --path . \
  -- \
  --config=challenges/CHALLENGE_XXX.json
```

## 3. Pipeline de Transcodificación FFmpeg

```bash
ffmpeg -y -i output/CHALLENGE_XXX_raw.avi \
  -vcodec libx264 \
  -crf 18 \
  -pix_fmt yuv420p \
  -acodec aac \
  -b:a 192k \
  output/CHALLENGE_XXX.mp4
```

---

## 4. Contrato Temporal Vivo — C6-D4

La composición temporal es **declarativa por challenge** y se define mediante cuatro duraciones: `hook_duration`, `game_duration`, `reveal_duration` y `cta_duration`.

### Regla de activación de fases

| Duración | Comportamiento |
|---:|---|
| `0` | La fase queda omitida del vídeo efectivo. |
| `> 0` | La fase forma parte del timeline y se renderiza. |
| `< 0` | JSON inválido; bloqueado por Capa 0. |

`GAME` es obligatorio y debe cumplir `game_duration > 0`.

El orden de las fases sigue siendo fijo:

```text
HOOK → GAME → REVEAL → CTA
```

Las fases desactivadas no generan frames ni estados visuales propios.

### Cálculo canónico

```text
hook_frames   = round(hook_duration   × fps)
game_frames   = round(game_duration   × fps)
reveal_frames = round(reveal_duration × fps)
cta_frames    = round(cta_duration    × fps)

total_frames = hook_frames + game_frames + reveal_frames + cta_frames
```

La factoría Python y `VideoTimeline.gd` deben producir el mismo resultado determinista. FFprobe es la autoridad física sobre el artefacto renderizado.

### Ejemplos oficiales C6-D4

```text
HOOK=0, GAME=7, REVEAL=0, CTA=2
→ GAME → CTA
→ 9.0 s / 540 frames @ 60 FPS

HOOK=3, GAME=7, REVEAL=0, CTA=0
→ HOOK → GAME
→ 10.0 s / 600 frames @ 60 FPS

HOOK=0, GAME=7, REVEAL=0, CTA=0
→ GAME
→ 7.0 s / 420 frames @ 60 FPS

HOOK=3, GAME=7, REVEAL=3, CTA=2
→ HOOK → GAME → REVEAL → CTA
→ 15.0 s / 900 frames @ 60 FPS
```

El antiguo perfil 11 s (`2 + 7 + 2`) queda como **perfil de referencia histórico**, no como límite global del motor.

---

## 5. Integridad de Simulación vs Presentación

El control de fases pertenece exclusivamente a la capa temporal/presentación. No puede modificar:

- RNG o seeds.
- `SimulationResult.frames`.
- `winning_frame_game`.
- métricas de validación.
- trayectorias o matemáticas de las mecánicas.

Cuando `hook_duration=0`, por ejemplo, el primer frame visual es `GAME[0]`; no se recalcula la simulación para compensar la ausencia del HOOK.

---

## 6. Artefactos Canónicos

```text
output/CHALLENGE_XXX/CHALLENGE_XXX_raw.avi
output/CHALLENGE_XXX/CHALLENGE_XXX.mp4
output/CHALLENGE_XXX/CHALLENGE_XXX_manifest.json
output/BATCH_MANIFEST.json
```

Cada manifest debe reflejar exactamente las duraciones y frame counts efectivos del challenge que lo generó.
