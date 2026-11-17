# C11-E E6 — Estado de admisión y ruta segura al primer render

**Revisión:** 2026-11-17 · **Versión:** V1  
**Checkout autoritativo:** `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`  
**Disposición:** `E6_READINESS_PASS_STATIC / MEDIA_ADMISSION_HELD`

## 1. Decisión ejecutiva

E6 ha avanzado de un inventario general a una auditoría estática de la ruta Challenge con sus dependencias de escena/timebase verificadas. El resultado permite continuar cerrando el contrato y la evidencia, pero todavía **no autoriza Godot, Movie Maker, D3, FFmpeg, FFprobe, audio, mux ni render**.

La aprobación general del operador para continuar el proyecto se registra como `CONTINUATION_APPROVAL_RECEIVED_NOT_POLICY_ADOPTION`. No se interpreta como aceptación automática de nueve pins candidatos, adopción de políticas, autorización de medios ni resolución del conflicto D4.8.

## 2. Evidencia actual confirmada

| Evidencia | Resultado | Límite exacto |
|---|---|---|
| E6 read-only audit V3 | PASS, 15 tests, 50/50 pins según el recibo aceptado | Auditoría estática; no render |
| Challenge plan-only | 18/18 E1 intents y 18/18 D envelopes | Seis escenarios × probes A/B/C; no 18 escenarios Challenge |
| Challenge consumer contract V3 | 36/36 tests; 24/24 pins | `PASS_STATIC_CONSUMER_CONTRACT_18_OF_18_EXECUTION_HELD` |
| Capture-route audit V2 | 24/24 pins; 6/6 definiciones; 18/18 checks | `PASS_STATIC_ROUTE_AUDIT_EXECUTION_HELD`; siete bloqueos siguen abiertos |
| Runtime dependency audit V1 | 33/33 huellas coincidentes: 24 previas + 9 nuevas | Las nueve adicionales siguen `CANDIDATE_ONLY_NOT_ACCEPTED` |
| E5 | `PASS_CLOSED_TEST_ONLY` | No repetir E5, D99 Qt ni el canary |
| E4A/B/C | Cerrados en los alcances ya aceptados | No regenerar evidencia aceptada |

### Identidades y hashes que deben conservarse

- Capture-route audit: `E6ROUTEAUDIT_20261117T125614Z_54A34DBA`; recibo SHA-256 `8deb1c23022ecde3f0b66e7ff07778172adecbd6e6a7f6ec045f6698657b4190`.
- Runtime dependency audit: `E6DEPPINAUDIT_20261117T130110Z_A1CCE574`; recibo SHA-256 `bff36af655abba65aa7ddb2e59c108c57593b6ca19aad586aafe7077b7428f3d`.
- Manifiesto candidato de nueve dependencias: SHA-256 `6f607d0a59202a23673905ea69542c07d1f43b2cf405e379b30257bba281483a`; estado `CANDIDATE_ONLY_NOT_ACCEPTED`.
- Manifiesto congelado C11-C: SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`; 796,318 bytes.
- Política D4.8 R1V V2: SHA-256 `0866b53ad4fcdebe74d01f66864b2dfb00eb644ca28dcd59301c8f3208239c07`; 12,996 bytes.

El instalador de este overlay vuelve a verificar los recibos de ambos audits y las 33 huellas de fuente. Esa comprobación es una precondición de instalación, **no** una nueva aceptación de política ni una repetición de la cualificación.

## 3. Nueve dependencias runtime observadas

Los nueve archivos adicionales que coincidieron en el audit son:

1. `project.godot` — selección de escena principal y settings.
2. `Main.tscn` — escena principal existente.
3. `core/authoring/ChallengeMigrationAdapter.gd` — migración de timebase Challenge.
4. `core/execution/ChallengeTimelineBuilder.gd` — construcción de timeline.
5. `core/authoring/ChallengeTimeLiine.gd` — aritmética de duración de fases.
6. `core/authoring/TemporalCore.gd` — redondeo duración→frames.
7. `core/validation/ChallengeDefinitionValidator.gd` — validación de definición.
8. `core/presentation/PresentationProfile.gd` — dependencia de perfil de presentación.
9. `core/validation/PresentationProfileValidator.gd` — validación del perfil.

Sus SHA-256 y tamaños están en `E6_RUNTIME_ROUTE_DEPENDENCY_PIN_CANDIDATE_V1.json`. El audit comprobó los nueve, pero dejó explícito `acceptance=NOT_GRANTED_BY_THIS_AUDIT`. No se deben copiar manualmente a un manifest aceptado ni cambiar ese estado por edición documental.

## 4. Bloqueos E6 que permanecen

El recibo de ruta registra exactamente estos siete bloqueos:

1. `E4A6_ENVELOPE_BUILDER_IS_CHALLENGE_004_ONLY`.
2. `E4A7_AUDIO_MUX_REVIEW_WORKER_IS_CHALLENGE_004_ONLY`.
3. `E3_D3_V5_PIPELINE_IS_CHALLENGE_001_ONLY`.
4. `CHALLENGE_E6_D9_MOVIE_MAKER_ORCHESTRATOR_NOT_FOUND`.
5. `D4_8_R1V_V2_STILL_FORBIDS_SMOKE18_D3_AUDIO_PCM_AND_FFMPEG_MUX`.
6. `E6_TEST_ONLY_GOVERNANCE_AUTHORIZATION_NOT_PRESENT`.
7. `E1_TEMPO_BPM_AND_DURATION_SECONDS_REMAIN_UNRESOLVED`.

Estos bloqueos son verificaciones pendientes, no defectos que deban “arreglarse” extendiendo workers CH004/CH001 por simple cambio de parámetros.

## 5. Contabilidad correcta de Smoke18

El objetivo E6 es **18 escenarios principales**: seis Challenge, seis Visual Loop y seis Visual Drill. Los 18 Challenge E1 intents y 18 envelopes son tres sub-probes por cada uno de los seis Challenge escenarios: A, B_REPEAT y C_CHANGED_MUSIC_SEED. No deben sumarse como 18 escenarios principales adicionales.

### Challenge — seis candidatos de trabajo, todavía no congelados

`CHALLENGE_001`, `002`, `004`, `005`, `006`, `007` es la selección candidata de trabajo, no una selección formalmente congelada. `CHALLENGE_003` permanece excluido de esta propuesta por ser el piloto RNG y compartir gameplay seed 314159 con CH004. `CHALLENGE_008/009` siguen excluidos por discrepancia declarada de 11 s frente a suma de fases de 12 s.

| Selector | Gameplay seed candidato | Timebase nativo |
|---|---:|---|
| CHALLENGE_001 | 193847 | 540 frames / 9 s @ 60 fps |
| CHALLENGE_002 | 987654 | 600 frames / 10 s @ 60 fps |
| CHALLENGE_004 | 314159 | 900 frames / 15 s @ 60 fps |
| CHALLENGE_005 | 998877 | 420 frames / 7 s @ 60 fps |
| CHALLENGE_006 | 884422 | 540 frames / 9 s @ 60 fps |
| CHALLENGE_007 | 7770001 | 600 frames / 10 s @ 60 fps |

Los valores de música 840001/840002, perfil `challenge_8bit_v1`, variación 0 y 104 BPM provienen de fixtures/propuestas E6; no son defaults de producto ni valores autorizados para ejecución. `E1.tempo_bpm` y `E1.duration_seconds` siguen sin resolver.

## 6. Evidencia reutilizable — no regenerar

- **R1V:** cierre técnico y revisión humana/audio 10/10 aceptados. No repetir.
- **Loop22:** 44/44 salidas A/V y 22/22 pares A/B; cierre humano posterior 44/44 aceptado. No repetir Loop22, R1P ni R1V.
- **Drill:** E4C `ACCEPTED_20_OF_20`; seis recibos elegibles como candidatos de reutilización. No repetir lotes aceptados.
- **Challenge CH004:** E4A.7 recibo SHA-256 `102cf07a0b8920318c3ba211a3bd4374c3e080018486363d701f81e65613aaa0`; fuente silenciosa normalizada SHA-256 `841b03531301c7e70c0e09ce3e9f536241d2072a87792e099ed7a955bef8c52f`. La reutilización en E6 sigue condicionada a validar el recibo completo y todos los medios anidados con las reglas E6.

El ledger E6 no convierte los 13 candidatos de reutilización (seis Loop + seis Drill + CH004 potencial) en 13 aceptaciones automáticas. Se deben asociar los recibos exactos y SHA-256 de cada salida, validar seeds, perfil, timebase, FFprobe, audio, aprobación humana y fuente de procedencia. Los medios aceptados nunca se regeneran para rellenar un ledger.

## 7. Puerta de gobernanza y primer render

### D4.8 permanece intacta

La política D4.8 R1V V2 con SHA `0866b53ad4fcdebe74d01f66864b2dfb00eb644ca28dcd59301c8f3208239c07` autoriza su alcance histórico acotado y prohíbe Smoke18/Matrix101, D3/música/PCM y FFmpeg filters/mux. No se modifica, no se sustituye y no se evade cambiando nombres de runner.

La propuesta E6 TEST_ONLY V2 sigue `NOT_READY_FOR_APPROVAL / NO_MEDIA_AUTHORITY`. Antes de cualquier herramienta multimedia se necesita una resolución de gobernanza separada y explícita que documente cómo se resuelve el conflicto de alcance con D4.8 y liste exactamente procesos, binarios/versiones/hashes, argumentos, recuentos, destinos, límites, parada al primer fallo y revisión humana. Una nueva nota E6 por sí sola no anula D4.8.

### Phase AD — no confundir aprobación de continuidad con política

El último registro de gobernanza localizado en la evidencia documental (Phase AD, 2026-10-29) indica `PENDING_OPERATOR_CHOICE_NO_APPLICABLE_AUTHORITY_SUBMITTED`; el gate exige completar el expediente existente R-01…R-09, con autoridad verificable y procedencia o decisión explícita `KEEP_BLOCKED_NO_POLICY_ADOPTION` por fila. Ese estado **debe revalidarse contra el archivo del checkout activo antes de modificarlo**, porque la copia localizada es de octubre y no es prueba de su versión viva actual.

La aprobación general recibida el 2026-11-17 permite continuar el trabajo de ingeniería dentro de los límites actuales; no contiene por sí sola rol/delegación, política, ámbito, fecha, fuente inmutable o aprobación verificable para adoptar una política de render.

### Umbral mínimo antes del primer render E6

- Las nueve dependencias incorporadas formalmente al conjunto de pins tras revisión/decisión explícita; no solo `PASS` del audit candidato.
- Reutilización de Loop/Drill/CH004 probada a nivel de cada recibo y cada medio; ledger final vinculado a hashes exactos.
- Seis filas Challenge seleccionadas formalmente; seeds/timebases canónicos; mapa de música y duración aprobado por request, sin defaults inventados.
- Ruta Challenge multi-selector existente verificada y un único orquestador D9 `PREPARE_ONLY` probado; sin Producer, binder, renderer, módulo o compositor paralelo.
- Matriz final de 18 escenarios principales congelada y 18 grupos de probes Challenge A/B/C reconciliados.
- Phase AD y cualquier otra política D aplicable reconciliadas en el checkout activo.
- Resolución explícita del conflicto D4.8 + autorización E6 TEST_ONLY aprobada para el ámbito exacto.
- Recién entonces, un runner de ejecución de un solo uso con rutas/argv exactos, salida aislada, parada al primer error, evidencia completa y aceptación visual/audio humana.

## 8. Invariantes no negociables

- C11-C 2.19.12 sigue siendo la única autoridad de producción; manifest SHA `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.
- No cambiar C11-C, su manifest, mecánicas, RNG, generadores, audio core ni contratos protegidos.
- E1 `PREPARE_ONLY`; `family_adapter=NOT_CONNECTED_E1`.
- `D4.8=BLOCKED`; `renderer=OFF`; `production_dispatch=false`; `media=false`.
- `D9.10=PREPARE_ONLY`; `D9.14/D9.16=BLOCKED`; `D9.17=BLOCKED_NO_GO`; `D10=BLOCKED_FOR_PROMOTION`.
- `release_authority=NONE`; no promotion, freeze ni cutover.
- `GIT_CHECKS=SKIPPED`; `COMMITS=OPERATOR_MANAGED`; `SOURCE_FILE_PINS=ENFORCED`.
- No repetir cualificaciones aceptadas, no consumir BatchId en preparación, no extraer ZIP sobre checkout.

## 9. Orden operativo actualizado

1. Confirmar versión/hash/estado del expediente Phase AD directamente en el checkout activo; no restaurarlo desde snapshots.
2. Obtener las decisiones del operador en el expediente existente, o documentar por fila que se mantiene bloqueado. No escribir decisiones en nombre del operador.
3. Revisar y aceptar/rechazar formalmente el candidato de nueve pins. El audit de 33/33 no hace esa elección.
4. Hidratar la evidencia original de Loop/Drill/CH004 de forma read-only y terminar el ledger E6 sin reruns.
5. Cerrar selección/semillas Challenge y el contrato E1 de tempo/duración usando autoridad canónica.
6. Solo tras cerrar esas entradas, finalizar la matriz E6 y el D9 `PREPARE_ONLY` multi-selector.
7. Presentar la autorización E6 TEST_ONLY y la resolución de conflicto D4.8 para aprobación separada.
8. Ejecutar el primer render solo con todos los gates anteriores y la autorización exacta vigente.
