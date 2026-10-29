# C11-D — Phase Q: revisión read-only de dependencias semánticas y de política

**Fecha:** 29-10-2026  
**Estado:** `PREPARED_READ_ONLY_POLICY_DEPENDENCY_REVIEW_NOT_OPERATOR_POLICY_APPROVAL`  
**Entrada:** Phase P aceptada exclusivamente para procedencia source-frame.  
**Modo:** read-only; sin runtime, sin producción, sin payload y sin media.

## 1. Decisión de alcance

Phase P ha demostrado relaciones `source-value` ↔ `frame-value` para seis candidatos y estabilidad de los recibos en procesos independientes. No ha decidido qué debe verse, cómo se mapea al canvas, cuándo es visible, cómo se muestrea para entrega ni si el campo merece un binding. Phase Q organiza esas dependencias sin cambiar las decisiones semánticas previas ni aprobar una política de renderer.

La propuesta previa y el registro de decisión semántica V2B siguen siendo autoridad de lo que se aceptó/bloqueó semánticamente: `CHALLENGE_003.target_x`, `CHALLENGE_005.target_position`, `CHALLENGE_006.target_position` y `CHALLENGE_007.target_position` tienen definición semántica aceptada **para una futura especificación de binding**; `CHALLENGE_008.active_selection` y `CHALLENGE_009.displayed_count` siguen bloqueados. Ninguno tiene binding autorizado.

## 2. Evidencia de entrada verificada por el operador

| Evidencia | Resultado |
|---|---|
| Manifiesto canónico C11-C | 796.318 bytes; SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953` |
| Informe runtime Phase P | SHA-256 `9686240a0e2caa46f05cea4ca2c8fcaaa1499d006ac6ac75d128137693fc2ef7` |
| Godot | `4.7.1.stable.mono.official.a13da4feb` |
| Pins Phase P / V2C parent | `95/95` / `PASS` |
| Selectores / planner / procesos Godot | `6/6` / `6/6` / `12/12` |
| Hashes de repetición | concordancia para los seis selectores |
| Serialización de valores candidatos / mapa custom_data completo | `false` / `false` |
| Cierre documental Phase P | siete hashes de continuidad verificados; aceptación limitada a procedencia |

La aceptación de procedencia no es evidencia de consumo visual, de dibujo de texto, de píxeles ni de vídeo.

## 3. Matriz por candidato

| Candidato | Semántica establecida por fuentes/decisión previa | Situación de Phase P | Dependencias abiertas antes de cualquier especificación de consumidor |
|---|---|---|---|
| `CHALLENGE_003.target_x` | `float` escalar por frame en `PILOT_0X100`; la decisión previa acepta solo el eje X derivado de `target_start + target_velocity * frame_index`. No contiene Y. | Procedencia aceptada. | Aprobar/rechazar el mapeo de X; decidir explícitamente si se permite un Y de presentación `480` que no proviene de la simulación; fijar dominio, tamaño intrínseco del SVG, ancla, recorte y rounding de píxel; definir sampling de fuente 60 FPS a entrega 30 FPS. La propuesta `x=(target_x/100)*540`, `y=480` es propuesta, no política aprobada. |
| `CHALLENGE_005.target_position` | `Vector2` del objetivo de Hit; un punto por ejecución repetido en los registros por frame. No es una trayectoria móvil. | Procedencia aceptada. | Resolver transformación espacial propuesta, propiedad del marcador, tamaño/ancla, borde/recorte, rounding, visibilidad y muestreo de entrega. No sustituirlo por `snapshot.position` ni por telemetría de scoring. |
| `CHALLENGE_006.target_position` | `Vector2` por frame para el objetivo móvil; el track principal `snapshot.position` corresponde al catcher. | Procedencia aceptada. | Aprobar transformación espacial y región/ventana de visibilidad; cardinalidad exacta por frame; finiteza y dominio; sampling 60→30 sin interpolación ni extrapolación no autorizadas; rounding y crop. |
| `CHALLENGE_007.target_position` | `Vector2` por frame para el objetivo; `snapshot.position` corresponde al scanner. El objetivo está separado de distractores y telemetría. | Procedencia aceptada. | Las mismas dependencias espaciales y temporales que el track `Vector2` de CH_006; excluir topología/distancias de distractores, scoring y `close_calls`. No inferir visibilidad desde el nombre de una fase. |
| `CHALLENGE_008.active_selection` | `int` con índice de opción; `ChooseMechanic` ya mapea `selection` a `options_positions[selection]` en `snapshot.position` (con fallback central para índice inválido). La semántica visual adicional puede ser redundante. | Procedencia source-frame aceptada; decisión semántica completa bloqueada. | Decisión explícita sobre `total_duration=11s` frente a suma de fases `12s`; determinar si el índice aporta información visual independiente de `snapshot.position`; definir propiedad/estilo de selección antes de decidir sampling o visibilidad. Está fuera de la propuesta de transformación espacial de los cuatro campos aceptados. |
| `CHALLENGE_009.displayed_count` | `int` del valor presentado por frame, distinto de `target_count`; el source ya usa el valor presentado para calcular `snapshot.position.x = start_pos.x + offset_index * step_x`. No existe autorización de emitir texto/layout. | Procedencia source-frame aceptada; decisión semántica completa bloqueada. | Decisión explícita 11s frente a 12s; determinar si la presentación existente vía posición es suficiente, qué objeto/área sería dueño del recuento y si se necesitaría texto/layout. Mantener `displayed_count` distinto de `target_count`; ningún consumer/transform está autorizado. |

### Restricciones transversales

- `winning_frame` es el único anclaje temporal de Challenge. `close_calls` cuenta episodios y no puede usarse como frame, duración o regla de visibilidad.
- Mantener `CHALLENGE_003.target_x` como escalar. No inventar Y ni convertirlo silenciosamente en `Vector2`.
- `CHALLENGE_005.target_position` es constante por ejecución aunque se repita en frames; no declararlo una trayectoria móvil.
- Las tracks de CH_006 y CH_007 no se fusionan con `snapshot.position`.
- No leer ni serializar campos no allowlisted, no volcar todo `FrameSnapshot.custom_data` y no emitir valores reales en recibos.
- Para datos ausentes, tipo incorrecto, `NaN`/infinito, cardinalidad incorrecta o fuera de dominio, el diseño futuro debe definir fallo cerrado. No se autoriza clamping, fallback desde la posición primaria, interpolación ni extrapolación.

## 4. Dependencias de política que siguen sin aprobar

| Dominio | Estado real | Decisiones requeridas | Evidencia negativa/determinista futura |
|---|---|---|---|
| Timebase y sampling | Propuesta solamente. La propuesta half-open/nearest-half-up existente es de un caso concreto; no se extiende por inferencia a los seis selectores. | Mapeo explícito de índices de fuente a 30 FPS de entrega; límites inclusivos/exclusivos; duración preservada; desempate; regla para FPS no soportados. Resolver 008/009 antes de incluirlos. | Mapeo de índices y cardinalidad exacta; pruebas de frontera; repeat hash; rechazo cerrado de perfiles no soportados; cero muestras sintéticas. |
| Coordenadas y proyección | Propuesta para 003/005/006/007; 008/009 excluidos. No aprobada. | Transformaciones por espacio, dominio, Y de presentación del piloto, límites y política de valores fuera de dominio. | Puntos conocidos, dominio y finitud; rechazo sin clamp; escalar sin Y inferida; preservación de precisión. |
| Región y visibilidad | Propuesta de span completo para los cuatro candidatos anteriores; no aprobada. | Dueño del target, región, ventana exacta y cardinalidad; la fase de Challenge por sí sola no otorga visibilidad editorial. | Límites de aparición/desaparición, cardinalidad y fallo cerrado ante muestras ausentes; `close_calls` no afecta visibilidad. |
| Tamaño, ancla, crop y rounding | Tamaño SVG intrínseco como unidades de canvas y ancla central son propuestas; rounding de píxel sigue sin resolver. | Confirmar dimensiones, ancla, recorte fuera del canvas y rounding determinista. | Geometría reproducible del ancla, clipping sin mover origen, SVG inválido/missing falla cerrado y pixel rounding determinista. |
| Propiedad semántica / redundancia | Cuatro definiciones semánticas aceptadas para especificación futura; dos bloqueadas. Ningún binding aprobado. | Decidir quién es dueño del significado visual, si un campo añade significado respecto a la track primaria y qué campos quedan excluidos. | Allowlist estricta, sin fallback a posición/scoring, sin serialización de mapa completo, sin texto/layout hasta autorización explícita. |
| Datos inválidos y determinismo | La procedencia hash-only es reproducible; no garantiza corrección visual. | Fijar tipos, finitud, límites, cardinalidad y manejo de ausencia para cada futura especificación. | Missing, tipo incorrecto, NaN/Infinity, fuera de dominio, cardinalidad incorrecta, procesos independientes y recibos sin valores crudos. |

### Políticas previas que no se deben elevar por inferencia

- La propuesta de coordenadas V2B (`44c1ec65…`) sigue `PROPOSED_NOT_APPROVED` y cubre los cuatro campos 003/005/006/007; no incluye 008/009.
- La propuesta de región/visibilidad V2B (`f3afe4d7…`) tampoco está aprobada y limita su scope a esos mismos cuatro campos.
- La propuesta temporal de alineación (`39f6f979…`) es específica de un caso de revisión y no autoriza generalizar automáticamente su regla de sampling.
- La proyección de timebase de entrega (`4a76bc96…`) está en preparación; no emite instrucciones de renderer ni media.
- El docket de políticas continúa en preparación y conserva decisiones de operador pendientes.

## 5. Criterio de salida de Phase Q

Phase Q podrá quedar aceptada como **inventario read-only de dependencias de política**, no como aceptación de políticas, únicamente cuando su test estático confirme el orden de seis candidatos, el estado aceptado/bloqueado de decisiones anteriores, los cinco dominios de política pendientes, los pins declarados y todos los locks. No requiere ejecutar Godot ni repetir Phase P.

Para autorizar un consumidor futuro hacen falta decisiones separadas —y, en su caso, aprobaciones explícitas del operador— para timebase/sampling, coordenadas/proyección, región/visibilidad, tamaño/ancla/crop, pixel rounding, validez/cardinalidad y propiedad semántica. Cualquier binding posterior necesitará su propio decision record y tests negativos/deterministas.

`CHALLENGE_008` y `CHALLENGE_009` quedan fuera de cualquier especificación de binding/coordinate consumer hasta resolver expresamente la discrepancia 11s/12s. No elegir una corrección por inferencia.

## 6. Siguiente puerta

**Phase R — paquete de decisiones de política y adjudicación de dependencias, read-only.** Preparar un paquete por decisión que enlace las propuestas existentes, identifique opciones y consecuencias, haga explícita la autoridad requerida y registre una decisión sin traducirla automáticamente a código. Esta puerta no concede binding ni autorización de render.

## 7. Locks de gobernanza

`renderer=OFF`; `media_created=false`; `payload_materialized=false`; `candidate_input_admissible=false`; `seed_domains_complete_for_candidate_input=false`; `automatic_seed_generation=false`; `master_seed=NOT_ADOPTED`; `approved_bindings=0`; `approved_custom_data_bindings=0`; `approved_renderer_projection_bindings=0`; `D4.8=BLOCKED`; `D9.10=PREPARE_ONLY`; `D9.14=BLOCKED`; `D9.16=BLOCKED`; `D9.17=BLOCKED_NO_GO`; `D10=BLOCKED_FOR_PROMOTION`; `baseline_approval=MISSING`; `freeze_eligible=false`; `release_authority=NONE`.

C11-C 2.19.12 permanece como baseline autoritativo e inmutable. Phase Q no cambia el manifiesto, no actualiza fuentes de Challenge, no toca el harness CH_004 V1, no crea un renderer ni llama a Godot.
