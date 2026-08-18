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