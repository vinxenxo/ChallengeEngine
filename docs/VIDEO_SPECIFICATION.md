# VIDEO_SPECIFICATION.md — ESPECIFICACIONES DE VÍDEO Y PIPELINE

## 1. Especificaciones Técnicas del Master

| Parámetro | Valor Máster por Defecto |
| :--- | :--- |
| **Resolución** | $1080 \times 1920$ píxeles |
| **Relación de Aspecto** | 9:16 (Vertical Estricto) |
| **Framerate Target** | 60 FPS (Configurable por JSON) |
| **Formato de Píxel** | YUV420p (Obligatorio para compatibilidad móvil) |
| **Códec de Vídeo** | H.264 / MP4 |
| **Códec de Audio** | AAC (192 kbps) |

---

## 2. Invocación de Renderizado Offline (Godot Movie Maker)

godot --headless \
  --write-movie output/CHALLENGE_001_raw.avi \
  --fixed-fps 60 \
  --quit-after 660 \
  --path . \
  -- \
  --config=challenges/CHALLENGE_001.json

## 3. Pipeline de Transcodificación FFmpeg
Bash
ffmpeg -y -i output/CHALLENGE_001_raw.avi \
  -vcodec libx264 \
  -crf 18 \
  -pix_fmt yuv420p \
  -acodec aac \
  -b:a 192k \
  output/CHALLENGE_001.mp4

## Current Live Temporal Contract — CHECKPOINT 0.3.x

The current challenge master profile used by the frozen baseline and current V2 fixtures is:

| Block | Duration | Frames @ 60 FPS |
|---|---:|---:|
| HOOK | 2.0 s | 120 |
| GAME | 7.0 s | 420 |
| CTA | 2.0 s | 120 |
| TOTAL | 11.0 s | 660 |

The original document's technical rendering pipeline remains valid. Older timing examples with 3.0 s HOOK + 1.0 s CTA are historical and must not override the live challenge JSON contract.

---

## Current Live Video Contract — CHECKPOINT 0.9.0

Production video uses the graphical Godot Compatibility renderer for Movie Maker. The unsupported/unsafe combination of `--headless` with `--write-movie` is not part of the production contract.

### Live timeline

```text
HOOK = 2.0 s / 120 frames
GAME = 7.0 s / 420 frames
CTA  = 2.0 s / 120 frames
TOTAL = 11.0 s / 660 frames
```

### Canonical artifact paths

```text
output/CHALLENGE_XXX/CHALLENGE_XXX_raw.avi
output/CHALLENGE_XXX/CHALLENGE_XXX.mp4
output/CHALLENGE_XXX/CHALLENGE_XXX_manifest.json
output/BATCH_MANIFEST.json
```

FFprobe is the physical output authority for duration, frame count and frame rate.
