# START PROMPT
## ChallengeEngineV01_STATELESS
### Continuación posterior a C7-A3 — FROZEN / CERTIFIED

Estás continuando el proyecto `ChallengeEngineV01_STATELESS` en una nueva ventana de contexto.

Debes asumir como baseline vinculante el siguiente estado:

```text
C6-A1  FROZEN / CERTIFIED
C7-A1  FROZEN / CERTIFIED
C7-A2  FROZEN / CERTIFIED
C7-A3  FROZEN / CERTIFIED
```

El subsistema audiovisual completo está cerrado.

---

## 1. REGLA PRINCIPAL

NO reabras C7-A1.

NO reabras C7-A2.

NO reabras C7-A3.

NO modifiques por iniciativa propia:

- RNG;
- simulación;
- `SimulationResult`;
- `VideoTimeline`;
- `winning_frame`;
- `AudioExportBridge`;
- PCM;
- multiplexado FFmpeg;
- auditoría FFprobe;
- contrato fail-closed.

Solo pueden tocarse mediante una regresión explícitamente demostrada o una instrucción expresa.

---

## 2. EVIDENCIA CERTIFICADA

C7-A1 certificó:

```text
PCM determinista
AudioTimeline
AudioExportBridge
AAC
MP4
FFprobe
non-silence audit
ffplay playback
```

C7-A2 certificó:

```text
mixed batch
1 audio-on
1 audio-off
2/2 PASS
audio_summary
0 unauthorized audio streams en OFF
```

C7-A3 certificó:

```text
9 challenges
4 workers
9/9 PASS
audio C7 habilitado
shadow audit C6 ↔ C7
18 variables deterministas
0/9 discrepancies
```

Por tanto:

> El audio C7 está certificado como capa ortogonal al conjunto completo de telemetría determinista declarado en la auditoría shadow.

---

## 3. CORPUS

Baseline histórico:

```text
./challenges/
CHALLENGE_001.json
...
CHALLENGE_009.json
```

Debe permanecer intacto como regresión C6.

Suite C7 paralela:

```text
./challenges_c7/
```

representa la evolución audiovisual.

No mezclar arbitrariamente ambas suites.

---

## 4. OBSERVACIÓN CONOCIDA

Existe una observación visual:

> El cuadrado verde / winning highlight puede parecer adelantado respecto al momento en que el objeto llega visualmente a su objetivo.

Esta observación NO está declarada como regresión del núcleo determinista.

No modificarla todavía.

Si una fase posterior necesita investigarla, hacerlo como auditoría independiente:

```text
SimulationResult
→ winning_frame
→ Timeline
→ Presentation
→ Rendered frame
```

sin alterar primero la simulación.

---

## 5. FILOSOFÍA DE TRABAJO

Trabajar exactamente como en los checkpoints anteriores:

```text
AUDIT
→ DEFINE CONTRACT
→ IMPLEMENT MINIMAL DELTA
→ UNIT TEST
→ INTEGRATION TEST
→ REGRESSION
→ BATCH
→ CERTIFY
→ FREEZE
```

No implementar código antes de determinar:

- objetivo;
- contrato;
- inputs;
- outputs;
- invariantes;
- gates de fallo;
- pruebas de aceptación.

---

## 6. PROHIBICIONES

No:

- reescribir módulos certificados;
- duplicar arquitectura existente;
- introducir fallback silencioso;
- inferir información autoritativa;
- modificar el corpus C6 histórico;
- mezclar audio C7 con lógica de simulación;
- cambiar seeds para ocultar una regresión;
- declarar PASS basándose únicamente en ausencia de excepciones;
- declarar CERTIFIED sin evidencia reproducible.

---

## 7. SIGUIENTE FASE

No asumas automáticamente cuál es el siguiente bloque.

Primero:

1. inspecciona el roadmap C7 disponible en el repositorio;
2. identifica el siguiente checkpoint después de A3;
3. contrasta ese checkpoint con el estado real del código;
4. determina qué está realmente pendiente;
5. presenta el contrato y los gates de aceptación;
6. solo después propone o aplica el cambio mínimo necesario.

La prioridad es:

> **continuidad arquitectónica + determinismo + trazabilidad + mínima superficie de cambio.**

---

## 8. CONTEXTO DE EJECUCIÓN

Entorno utilizado:

```text
Godot 4.7.1-stable (official)
Python 3.x
FFmpeg 9.0
Windows / PowerShell
```

El usuario ejecuta las pruebas localmente.

Nunca afirmar que una prueba ha sido ejecutada por el asistente.

El usuario proporciona logs reales de PowerShell como evidencia.

---

## 9. RESPUESTA ESPERADA AL ARRANQUE

Al comenzar la nueva ventana:

- reconocer C7-A3 como checkpoint congelado;
- no volver a explicar toda la implementación audiovisual;
- identificar el siguiente bloque real del roadmap;
- señalar cualquier ambigüedad o dependencia;
- proponer el siguiente gate de aceptación.

No asumir que la siguiente tarea es “más audio”.

El objetivo ahora es avanzar el motor funcionalmente manteniendo intactos los checkpoints certificados.

## CONTINUIDAD

Fuente maestra:

`MASTER HANDOVER — ChallengeEngineV01_STATELESS — C7-A3 FROZEN / CERTIFIED`

Este START PROMPT debe interpretarse conjuntamente con ese documento.