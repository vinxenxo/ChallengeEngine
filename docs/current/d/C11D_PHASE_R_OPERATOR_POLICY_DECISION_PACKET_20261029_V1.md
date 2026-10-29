# C11-D Phase R — Operator Policy Decision Packet V1

**Estado:** `PREPARED_READ_ONLY_DECISION_PACKET_NOT_ADJUDICATED`  
**Modo:** `READ_ONLY_DECISION_PREPARATION`  
**Fecha:** 2026-10-29

## 1. Finalidad y alcance

Phase R transforma el inventario read-only de Phase Q en un expediente de decisiones explícitas. Identifica las opciones, sus consecuencias, la autoridad requerida y las pruebas que deberán ejecutarse después de que se adopte una decisión válida. **Este expediente no selecciona ninguna opción, no aprueba políticas y no autoriza bindings.**

Solo se preparan los seis selectores ya inventariados: `CHALLENGE_003.target_x`, `CHALLENGE_005.target_position`, `CHALLENGE_006.target_position`, `CHALLENGE_007.target_position`, `CHALLENGE_008.active_selection` y `CHALLENGE_009.displayed_count`.

Phase Q se cerró con estado `PASS_READ_ONLY_INVENTORY`; el registro add-only indicado en la matriz JSON es parte de la autoridad de esta fase. Phase P continúa aceptada **solo** para procedencia source-frame, no para consumo visual.

## 2. Regla de decisión y autoridad

La autoridad de producto/contrato correspondiente debe resolver cada decisión dentro de su ámbito. Una preparación hecha por el asistente no sustituye esa autoridad. Toda decisión adoptada deberá constar en un registro separado e inmutable que incluya, como mínimo: identificador, opción exacta, alcance por selector, autoridad responsable, justificación, pins de fuentes, consecuencias, pruebas de aceptación y fecha.

Hasta que exista dicho registro, la posición operativa es `KEEP_BLOCKED_NO_POLICY_ADOPTION`. No se usarán nombres de fases, plausibilidad visual o conveniencia para inferir decisiones. El cierre de Phase R no autoriza renderer, payload, media, bindings, accesos nuevos a `custom_data` ni promoción.

## 3. Expediente de decisiones

El JSON compañero enumera nueve IDs (`R-01` a `R-09`). La siguiente síntesis destaca el objeto de cada decisión; las opciones completas y sus consecuencias están en el JSON para que puedan ser validadas sin interpretación del texto narrativo.

### R-01-TIMEBASE-SAMPLING — Muestreo temporal 60 FPS → 30 FPS

Debe seleccionarse una regla exacta de índices de origen o una política de límites temporales, incluyendo duración, cardinalidad, extremos y empates. No hay una regla blanket 2:1 aprobada. No se permite interpolación/extrapolación ni muestras sintéticas sin una política nueva y separadamente aprobada.

### R-02-SPATIAL-MAPPING — Transformación espacial de vectores

Para los tres candidatos Vector2 de CHALLENGE_005/006/007, debe aprobarse, rechazarse o reemplazarse explícitamente la propuesta de escala source 1080×1920 → logical 540×960 (0,5) → delivery 720×1280 (4/3). Las dos etapas no se convierten en política aprobada por estar documentadas. CHALLENGE_008/009 quedan fuera de este alcance mientras estén bloqueados.

### R-03-PILOT-SCALAR-X-AND-PRESENTATION-Y — Escalar X y Y de presentación del piloto

`CHALLENGE_003.target_x` permanece un `float` escalar por frame. La propuesta `x_logical=(target_x/100)*540` y el posible `y_logical=480` son dos decisiones independientes; Y sería presentación, no dato de origen. No se puede transformar el candidato en `Vector2` ni inferir Y desde `snapshot.position`.

### R-04-VISIBILITY-AND-REGION-OWNERSHIP — Visibilidad y propiedad de región

Debe definirse por selector quién posee el objetivo visual y el intervalo exacto de visibilidad. La propuesta de visibilidad durante todo el span de origen no está aprobada. Los nombres de fases no prueban ventanas visuales y `close_calls` no sirve para derivar visibilidad.

### R-05-ASSET-GEOMETRY-ANCHOR-CROP-ROUNDING — Dimensiones, ancla, recorte y redondeo

Debe resolverse si el tamaño intrínseco SVG 100×100 es una unidad de escala, si el ancla es el centro y cómo se recorta la geometría en el borde lógico. También debe elegirse un modo de redondeo de píxel determinista; dejarlo implícito no es una resolución válida. La posición de origen no se moverá silenciosamente para evitar clipping.

### R-06-INVALID-DATA-AND-TRACK-INTEGRITY — Datos inválidos e integridad del track

Debe adoptarse una política por candidato para valores ausentes, tipos incorrectos, `NaN`, `Infinity`, valores fuera de dominio y cardinalidades incoherentes. La propuesta conservadora es fallar cerrado para todo el track, sin clamping. Cualquier política menos estricta necesitaría un contrato de huecos separado y prohibir la interpolación/extrapolación no autorizada.

### R-07-SEMANTIC-VISUAL-OWNERSHIP — Propiedad semántica y consumo visual

Debe declararse si cada selector representa un elemento visual distinto, qué actor/región lo posee y qué información añade respecto a `snapshot.position`. CHALLENGE_007 excluye distractores, telemetría de éxito/puntuación y `close_calls`. CHALLENGE_008 puede ser redundante con la posición primaria. En CHALLENGE_009, `displayed_count` es el estado mostrado actual, no `target_count`, y no autoriza texto ni layout.

### R-08-CHALLENGE-008-DURATION-CONFLICT — Conflicto de duración de CHALLENGE_008

El valor declarado es 11 s y la suma de fases es 12 s. El bloqueo permanece. Solo el propietario explícito del contrato temporal puede autorizar una corrección gobernada o una excepción documentada. Este paquete no determina cuál valor es correcto.

### R-09-CHALLENGE-009-DURATION-AND-COUNT-ROLE — Conflicto temporal y papel visual de CHALLENGE_009

Se conserva el mismo conflicto 11 s/12 s, sin inferencia. Además, debe resolverse si `displayed_count` tiene un papel visual separado y cómo se distingue de `target_count`. Una decisión de duración no habilita texto/layout ni binding.

## 4. Pruebas futuras requeridas

Las pruebas no se ejecutan en Phase R. Tras decisiones válidas, los contratos específicos deberán cubrir: índices y cardinalidad temporal; límites y empates; transforms de puntos conocidos; dominio y rechazo de límites; independencia de Y de presentación; span y ownership de visibilidad; geometría/anchor/clip/redondeo exactos; datos ausentes, tipos y valores no finitos; integridad de cardinalidad; determinismo entre procesos; y serialización limitada a campos expresamente autorizados sin valores candidatos raw ni mapas completos de `custom_data`.

## 5. Invariantes

- `renderer=OFF`; Godot no se invoca en Phase R.
- `media_created=false`; `payload_materialized=false`.
- `approved_bindings=0`; `approved_custom_data_bindings=0`; `approved_renderer_projection_bindings=0`.
- `candidate_input_admissible=false`; `master_seed=NOT_ADOPTED`; generación automática de seeds desactivada.
- `D4.8=BLOCKED`; `D9.10=PREPARE_ONLY`; `D9.14=BLOCKED`; `D9.16=BLOCKED`; `D9.17=BLOCKED_NO_GO`; `D10=BLOCKED_FOR_PROMOTION`.
- `baseline_approval=MISSING`; `freeze_eligible=false`; `release_authority=NONE`.
- C11-C 2.19.12 sigue siendo el baseline autoritativo e inmutable hasta la aceptación, freeze y promoción formales de C11-D.
- CHALLENGE_008/009 continúan bloqueados por el conflicto 11 s/12 s hasta decisión de autoridad explícita.

## 6. Condición de salida y siguiente gate

Phase R puede cerrarse cuando el expediente, schema y test estático son coherentes, los pins actuales concuerdan y todos los bloqueos permanecen intactos. Cerrar Phase R significa **packet de decisiones preparado**, no políticas adoptadas. El siguiente gate propuesto es Phase S, para registrar y adjudicar únicamente decisiones explícitas que se hayan proporcionado con autoridad y alcance verificables.
