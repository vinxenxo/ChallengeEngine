# DISTRIBUTION_SPEC_V0.1 — Especificaciones de Distribución Social

## 1. Desacoplamiento de Perfiles de Distribución
El Motor de Simulación (`Engine`) es completamente independiente de las plataformas de redes sociales. La configuración de formato se define a nivel de perfil de salida o datos del challenge.

   CORE ENGINE (Agnóstico)
          │
          ▼
DISTRIBUTION PROFILE (Perfil de Formato)
│
┌──────┴──────┐
▼             ▼
Vertical       Square / Horizontal
(9:16 Short)     (Post Clásico)


---

## 2. Master Interno Estándar (Short-Form Vertical)

| Parámetro | Especificación |
| :--- | :--- |
| **Resolución Master** | $1080 \times 1920$ píxeles |
| **Relación de Aspecto** | 9:16 (Vertical Estricto) |
| **Framerate Target** | 60 FPS (o 30 FPS según perfil) |
| **Formato de Píxel** | YUV420p |
| **Códec de Vídeo** | H.264 / MP4 |
| **Códec de Audio** | AAC (192 kbps) |

---

## 3. Estructura Cronológica Master ("Pause Challenge")

La duración estándar para desafíos de pausa en redes sociales se establece en **duración declarativa por challenge (frames derivados a partir de sus cuatro fases)**:

$$\begin{aligned}
\text{HOOK (Cuenta Atrás):} \quad & 0.0\text{ s} - 3.0\text{ s} \quad (180\text{ frames}) \\
\text{GAMEPLAY (Juego):} \quad & 3.0\text{ s} - 10.0\text{ s} \quad (420\text{ frames}) \\
\text{CTA / FREEZE (Cierre):} \quad & 10.0\text{ s} - 11.0\text{ s} \quad (60\text{ frames}) \\
\hline
\mathbf{DURACIÓN\ TOTAL:} \quad & \mathbf{11.0\text{ s}} \quad \mathbf{(660\text{ frames})}
\end{aligned}$$

- **Ventaja Narrativa:** Combina **3 segundos de cuenta atrás (HOOK)** para enganchar la atención del usuario con los **8 segundos recomendados de juego continuo y cierre**, optimizando la retención y la probabilidad de pausa en plataformas como Instagram Reels, TikTok, YouTube Shorts y Facebook Reels.

---

## 4. Zonas Seguras (Safe Areas)
La capa de presentación debe respetar los márgenes superiores (15%) e inferiores (20%) para evitar

## Current Live Distribution Timing

The distribution architecture remains platform-agnostic. The historical 11.0-second profile is a reference fixture; production duration is derived per challenge from HOOK/GAME/REVEAL/CTA:

```text
HOOK = 2.0 s / 120 frames
GAME = 7.0 s / 420 frames
CTA  = 2.0 s / 120 frames
```

This supersedes older timing examples in this historical document for current engine work. No social platform API is part of the Simulation Core.

---

## Current Live Distribution Contract — CHECKPOINT 0.9.0

The distribution layer remains platform-agnostic. The current production master is:

```text
1080 × 1920
9:16
60 FPS
declarativa por challenge
H.264 / MP4
YUV420p
```

The live timeline is 2 s HOOK + 7 s GAME + 2 s CTA. Older 3+7+1 timing in this historical document is retained as historical reference only and must not override the live JSON contract.

Production artifacts are isolated under the challenge output directory; the root output directory contains only the batch manifest and non-challenge placeholders such as `.gitkeep`.
