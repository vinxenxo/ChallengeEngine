# MASTER HANDOVER
## ChallengeEngineV01_STATELESS
### Checkpoint: C7-A3 — AUDIOVISUAL CORPUS INTEGRATION
### STATUS: FROZEN / CERTIFIED

---

## 0. PROPÓSITO DE ESTE DOCUMENTO

Este documento constituye el estado maestro de continuidad del proyecto `ChallengeEngineV01_STATELESS` al cierre de C7-A3.

La siguiente ventana de contexto DEBE tomar este documento como fuente primaria de continuidad y NO debe reabrir, rediseñar ni reinterpretar checkpoints certificados salvo que exista una instrucción explícita del usuario para hacerlo.

El proyecto trabaja bajo un principio estricto de evolución incremental:

> **NO REGRESAR A CHECKPOINTS CERRADOS.  
> NO REIMPLEMENTAR COMPONENTES CERTIFICADOS.  
> NO INTRODUCIR CAMBIOS LATERALES EN FASES CONGELADAS.**

---

# 1. ESTADO OFICIAL ACTUAL

## C6-A1
**FROZEN / CERTIFIED ✅**

Baseline C6 histórico preservado.

## C7-A1
**FROZEN / CERTIFIED ✅**

Infraestructura audiovisual física completa:

- determinismo de audio;
- RNG de audio;
- timeline acústico;
- generación PCM;
- `AudioExportBridge`;
- fail-closed;
- integración en `GeneradorMaestro`;
- multiplexado AAC;
- auditoría FFprobe;
- auditoría de contenido acústico;
- validación práctica mediante `ffplay`.

## C7-A2
**FROZEN / CERTIFIED ✅**

Batch mixto de fixtures:

- audio-on;
- audio-off;
- validación concurrente;
- ausencia estricta de stream `a:0` en audio-off;
- contenido acústico certificado en audio-on;
- A/V sync certificado;
- agregación `audio_summary`;
- `mixed_batch=true`.

Fixture de integración:

```text
tests/fixtures/C7_AUDIO_CHALLENGE_002.json
tests/fixtures/C7_VIDEO_ONLY_CHALLENGE_001.json
```

## C7-A3
**FROZEN / CERTIFIED ✅**

Escalado al corpus C7 paralelo:

- 9 challenges;
- ejecución concurrente con `--workers 4`;
- 9/9 PASS;
- audio habilitado en la suite C7;
- auditoría de contenido acústico;
- auditoría A/V;
- manifiestos individuales;
- `BATCH_MANIFEST`;
- comparación shadow C6 ↔ C7.

Auditoría shadow ampliada:

```text
CHALLENGE_001  MATCH
CHALLENGE_002  MATCH
CHALLENGE_003  MATCH
CHALLENGE_004  MATCH
CHALLENGE_005  MATCH
CHALLENGE_006  MATCH
CHALLENGE_007  MATCH
CHALLENGE_008  MATCH
CHALLENGE_009  MATCH

Discrepancias: 0/9
```

Se compararon 18 variables deterministas:

```text
rng_version
initial_seed
final_seed
seed_used
attempts
close_calls
hook_frames
game_frames
reveal_frames
cta_frames
total_frames
winning_frame
winning_frame_game
winning_frame_in_valid_window
winning_time
winning_time_game
score
minimum_distance
```

Resultado:

```text
0/9 discrepancies
```

Conclusión:

> La introducción del subsistema de audio no modifica ninguno de los invariantes deterministas observables incluidos en la auditoría shadow ampliada.

La afirmación correcta es:

> **Orthogonality verified for the complete declared deterministic telemetry set.**

No extender esta afirmación automáticamente a variables que no hayan sido comparadas.

---

# 2. ARQUITECTURA CONSOLIDADA

Pipeline de producción:

```text
Challenge JSON
    ↓
Godot validation
    ↓
Canonical V2
    ↓
Simulation
    ↓
SimulationResult
    ↓
VideoTimeline
    ↓
Visual rendering
    ↓
RAW AVI

Audio authoring
    ↓
AudioProfile
    ↓
AudioTimelineResolver
    ↓
AudioExportBridge
    ↓
PCM s16le 44.1 kHz mono
    ↓
SHA-256

RAW AVI + PCM
    ↓
FFmpeg
    ↓
H.264 + AAC
    ↓
MP4 Master
    ↓
FFprobe
    ↓
Audio content audit
    ↓
Manifest
```

Principio operativo:

```text
GODOT     = calcula + renderiza
PYTHON    = orquesta + valida
FFMPEG    = empaqueta / codifica
FFPROBE   = certifica
```

---

# 3. CONTRATO DE AUDIO C7

## Audio OFF

Ausencia de:

```text
canonical_v2.audio
```

produce:

```text
audio_enabled = false
```

y posteriormente:

```text
MP4
→ 0 streams de audio
```

La rama OFF DEBE mantener:

```text
-map 0:v:0
```

para impedir selección automática de audio desde el RAW.

## Audio ON

`canonical_v2.audio` es la única autoridad.

El flujo esperado es:

```text
canonical_v2.audio
    ↓
profile resolution
    ↓
AudioProfileRegistry
    ↓
AudioProfileValidator
    ↓
AudioExportBridge
    ↓
PCM
    ↓
AAC
```

No introducir fallback inferido.

---

# 4. FAIL-CLOSED

Regla obligatoria:

```text
[AUDIO_EXPORT_JSON] ausente
→ ERROR
→ no fallback implícito
```

Nunca convertir ausencia de telemetry en:

```text
audio_enabled = false
```

El OFF debe estar explícitamente declarado por el runtime mediante:

```json
{
  "audio_enabled": false
}
```

---

# 5. AUDITORÍAS AUDIOVISUALES

## A1.3

Valida:

### Video
- H.264
- 1080x1920
- yuv420p-compatible
- framerate esperado
- número de frames esperado
- duración esperada

### Audio ON
- AAC
- 44100 Hz
- mono
- duración compatible

### Audio OFF
- cero streams de audio

### A/V
```text
abs(video_duration - audio_duration) <= 0.05
```

## A1.4

### PCM
Calcula:

```text
total_samples
non_zero_samples
non_zero_ratio
peak_amplitude
peak_normalized
rms_amplitude
is_silent
```

Gate:

```text
peak > 100
non_zero_samples > 0
```

### AAC

`volumedetect` sobre el MP4.

Comprueba:

```text
max_volume_db
mean_volume_db
```

Gate:

```text
max_volume_db > -90 dB
```

La reproducción práctica mediante `ffplay` confirmó que la señal acústica es físicamente audible.

---

# 6. BATCH C7

`run_batch()` descubre fixtures C7 mediante:

```python
challenges_dir.glob("*CHALLENGE*.json")
```

El batch devuelve métricas:

```json
"audio_summary": {
  "total_challenges": ...,
  "audited_challenges": ...,
  "audio_enabled": ...,
  "audio_disabled": ...,
  "audio_content_valid": ...,
  "av_sync_valid": ...,
  "mixed_batch": ...
}
```

### Regla importante

`mixed_batch` es una propiedad de la suite/contexto de integración.

NO debe convertirse en un requisito universal del batch de producción.

El corpus C6 oficial puede ser:

```text
9 audio-off
mixed_batch = false
```

y sigue siendo un batch válido.

---

# 7. CORPUS Y TRAZABILIDAD

El corpus histórico:

```text
./challenges/
CHALLENGE_001.json
...
CHALLENGE_009.json
```

debe considerarse baseline C6 congelado.

NO modificar esos JSON para introducir audio experimental.

La estrategia C7 adoptada consiste en un corpus paralelo derivado:

```text
./challenges_c7/
```

manteniendo comportamiento mecánico determinista equivalente y añadiendo únicamente la dimensión audiovisual C7.

La comparación C6 ↔ C7 garantiza que el audio es una capa ortogonal respecto al resultado determinista.

---

# 8. SHADOW AUDIT

Script:

```text
audit_shadow.py
```

Compara los manifiestos de:

```text
./output
./output_c7
```

Para los 9 challenges.

Variables comparadas:

18 campos deterministas documentados en este handover.

Resultado certificado actual:

```text
0/9 discrepancies
```

No ampliar verbalmente la garantía más allá del conjunto realmente comparado.

---

# 9. INCIDENTE VISUAL CONOCIDO

Existe una observación durante la reproducción de algunos fixtures:

> El `WinningHighlightComponent` / cuadrado verde puede parecer visualmente adelantado respecto a la posición visible del objeto.

Esta cuestión está registrada como:

```text
PRESENTATION TEMPORAL OBSERVATION
```

No constituye un fallo certificado de C7-A1/C7-A2/C7-A3.

No modificar:

```text
winning_frame
SimulationResult
RNG
mecánica Key
timeline
```

para resolverla sin una auditoría específica.

Debe tratarse como problema potencial de presentación/render temporal independiente.

---

# 10. REGLAS DE CONTINUIDAD

La siguiente ventana DEBE:

1. Tratar C7-A1, C7-A2 y C7-A3 como cerrados.
2. No repetir sus pruebas salvo regresión real.
3. No modificar el `AudioExportBridge` por razones no demostradas.
4. No alterar RNG.
5. No alterar simulación.
6. No alterar `SimulationResult`.
7. No introducir nuevas abstracciones sin necesidad.
8. No contaminar `./challenges/`.
9. Diferenciar claramente:
   - simulación;
   - presentación;
   - audio;
   - packaging;
   - auditoría.
10. No afirmar que algo está certificado sin evidencia de ejecución correspondiente.
11. Mantener fail-closed.
12. Preferir cambios mínimos y localizados.
13. Antes de modificar una pieza congelada, justificar primero la necesidad con evidencia reproducible.
14. No inventar APIs de Godot ni contratos inexistentes.
15. No afirmar ejecución de pruebas que no haya realizado el usuario.

---

# 11. CHECKPOINT DE REANUDACIÓN

Estado:

```text
C6-A1  FROZEN / CERTIFIED
C7-A1  FROZEN / CERTIFIED
C7-A2  FROZEN / CERTIFIED
C7-A3  FROZEN / CERTIFIED
```

El pipeline audiovisual C7 queda cerrado.

El siguiente trabajo debe comenzar en el **siguiente bloque funcional de C7**, no en otra iteración de A1/A2/A3.

La siguiente tarea NO está fijada por este documento.

La nueva ventana debe auditar primero el roadmap disponible y determinar cuál es el siguiente checkpoint lógico antes de modificar código.

---

# 12. REGLA FINAL DE CONTINUIDAD

No asumir que “audio funciona” significa que las siguientes fases deben centrarse obligatoriamente en más audio.

El objetivo del subsistema audiovisual ya se ha alcanzado.

A partir de aquí:

> **C7 debe avanzar funcionalmente sin degradar el núcleo determinista ni reabrir la infraestructura audiovisual certificada.**