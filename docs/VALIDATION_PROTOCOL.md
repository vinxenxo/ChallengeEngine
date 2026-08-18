# VALIDATION_PROTOCOL.md — Protocolo de autovetting e invariantes

## 1. Formulación del Frame Ganador (`WinningFrameDetector`)
Un frame $f$ es candidato a ser ganador si cumple:

$$D(f) \le T$$

Donde $D(f)$ es la distancia semántica y $T$ es la tolerancia de la mecánica (`tolerance_threshold`).

La puntuación multivariable $S(f)$ evalúa la proximidad y la estabilidad:

$$S(f) = 0.60 \cdot \left( \frac{1}{1 + D(f)} \right) + 0.40 \cdot \left( \frac{1}{1 + V(f)} \right)$$

El cuadro ganador óptimo es:

$$f_{\text{winning}} = \arg\max_{f \in \text{CandidateFrames}} S(f)$$

---

## 2. Invariante Narrativa de Calidad (`ChallengeValidator`)
- **Umbral de Proximidad Narrativa:** $T_{\text{close}} = T \cdot 3.5$.
- **Persistencia Mínima (Histéresis):** La simulación debe permanecer por debajo de $T_{\text{close}}$ durante al menos $12\text{ frames}$ consecutivos ($\sim 0.2\text{ s}$ a $60\text{ FPS}$).
- **Criterio Aceptado:** La simulación debe registrar entre **2 y 5 pasadas cercanas** ($\text{close\_calls} \in [2, 5]$).

---

## 3. Protocolo de Aceptación End-to-End (Prueba de Fuego)
Para certificar la correcta integración, la ejecución de `python build_factory.py` sobre `CHALLENGE_001.json` debe satisfacer la siguiente lista de verificación:

1. [ ] El proceso Godot finaliza con código de salida `0`.
2. [ ] La consola emite la etiqueta `[TELEMETRY_JSON]` completa.
3. [ ] `output/CHALLENGE_001.mp4` existe.
4. [ ] `ffprobe` reporta `duration=11.000000`, `nb_frames=660` y `r_frame_rate=60/1`.
5. [ ] `output/CHALLENGE_001_manifest.json` existe y contiene valores sanitizados (sin `INF`).
6. [ ] **Invariante Temporal:** $180 \le f_{\text{winning}} < 600$ (El cuadro ganador cae dentro del bloque `GAME`).