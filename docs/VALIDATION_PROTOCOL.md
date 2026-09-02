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

## Current V2.0 Validation Addendum

The original validation section is historical. The current live temporal contract is:

```text
FPS   = 60
HOOK  = 120 frames
GAME  = 420 frames
CTA   = 120 frames
TOTAL = suma de frames declarados por fase
```

Therefore the valid absolute winning-frame interval is:

```text
120 <= absolute_winning_frame < 540
```

For V2.0 mechanics, RNG-context errors must be detected before `WinningFrameDetector` or `ChallengeValidator` process a truncated simulation. A failed RNG operation returns a sentinel at the lower layer, bubbles `error_state` to the mechanic context, and is converted into `[ERROR_JSON]` by the Composition Root.

V2.0 validation also distinguishes:

- **mechanical determinism:** output depends only on declared structural inputs;
- **presentation/cosmetic isolation:** cosmetic RNG consumption cannot alter `SimulationResult`;
- **capability authorization:** a mechanic can consume only the streams granted by its context and the Registry.

---

## Current Live Validation Contract — CHECKPOINT 1.1.0-C6-D4

The global temporal window is:

```text
120 <= absolute_winning_frame < 540
```

The modern validator accepts mechanic-owned `close_calls` supplied through `SimulationResult.metadata` and no longer requires the historical 3.5× fallback for mechanics that own their metric. Historical formulas in the document above are retained as historical reference and do not override sovereign HIT/CATCH contracts.

### Production validation

Canonical E2E acceptance:

```text
duración física = total_frames configurado ± tolerancia FFprobe
frame count físico = total_frames configurado
60/1 FPS
```

Canonical artifact tree:

```text
output/CHALLENGE_XXX/...
output/BATCH_MANIFEST.json
```

The external Python test runner remains mandatory for suite certification.
