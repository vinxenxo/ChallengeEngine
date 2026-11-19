# C11-C → D+E: arquitectura de sustitución de la factoría audiovisual — V1

**Fecha:** 2026-11-19  
**Objeto:** consolidar el modelo real de producción C11-C 2.19.12 y definir el alcance correcto de su sustitución por D+E.  
**Estado:** documento de arquitectura y reconciliación histórica; no concede autoridad de producción.

## 1. Base documental inspeccionada

Se inspeccionó el snapshot de referencia `ChallengeEngineV01_STATELESS-LATEST.zip` (74,572,127 bytes, SHA-256 `5514652fd5b140cf126b80c7de82379eb0081c4797e4b311111a964f0b7d8a96`). No se extrajo sobre el checkout. Su miembro `release/C11C_FREEZE_PACKAGE_MANIFEST.json` mide 796,318 bytes y su SHA-256 coincide exactamente con el manifiesto congelado activo: `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`. Por tanto, los documentos y scripts históricos citados abajo se contrastaron contra el manifiesto congelado, sin convertir el ZIP en autoridad sobre el checkout.

Documentos principales revisados:

| Documento C11-C | SHA-256 | Aportación |
|---|---|---|
| `docs/c11/C11C_TOOLCHAIN_CANONICAL_v2.1.4.md` | `770b3ab9c001ae9ed75803d894c7aef33fe9c1f3d04f03ba3b92ddece0472cc2` | Toolchain, producción, captura, audio, sidecar y almacenamiento |
| `docs/c11/C11-C_EDITORIAL_AUDIO_LOOP_CONTRACT_v2.1.1.md` | `07f54f8b3eced5c3d14b6d059a010e438a91e17e8deef6d6b12197a94ef4f448` | Canvas lógico, viewport de captura, editorial y audio |
| `docs/c11/C11-C_CHANGELOG_v2.0.1_to_v2.1.4.md` | `f085baa72c0643c857aafdb35a54258834002d668b676d35c29283f6c6b73208` | Evolución editorial/audio/producción y reparaciones del toolchain |
| `docs/current/c11c/C11-C_2.19_COMMAND_SHEET.md` | `8b65ba3f0d9c892128600ad5e0203f83af954a92364f29fe4b053cd0afb1d19a` | Comandos canónicos y límites de mantenimiento |
| `docs/current/c11c/C11-C_2.19_COMPLETE_VIDEO_REVIEW_RUNBOOK.md` | `927cff979a2eda2b787602bc41d0069462da830057352c094ead322ae5768002` | Corpus 52, aislamiento de workers y validación |
| `docs/current/c11c/C11-C_2.19_CONSOLIDATED_STATE.md` | `a142675cdd25277ac586b4fed18afed790d0d63fa08ce382e3ef248622203175` | Baseline final, cobertura y límites congelados |
| `docs/current/c11c/C11-C_2.19_CONSOLIDATION_AND_FAILURE_PREVENTION.md` | `a6b357d84f40704fed480ca73d20a9749677cc75b714bd3c68b74b94c08092d7` | Reglas históricas de prevención de fallos |
| `docs/current/challenges/CHALLENGE_PRODUCTION_CURRENT.md` | `715035d0c9de897ac5c6d07c480ad2cc2df2ee64d21f5ed85dff20b886af8f79` | Ruta específica Challenge |

También se inspeccionaron los launchers de Loop, el helper `C11CMovieCapture.ps1`, el productor de Drill, el QA de Challenge y el verificador de revisión completa. Sus hashes se registran en el archivo de evidencias del paquete.

## 2. Qué hace realmente la factoría C

C11-C no es un único renderer ni un único comando. Es una factoría con tres rutas familiares de generación/captura, servicios transversales de editorial/audio y una capa independiente de empaquetado, validación y preservación de productos.

### 2.1 Challenge

Ruta confirmada por `CHALLENGE_PRODUCTION_CURRENT.md` y `run_c11c_challenge_bulk_qa.ps1`:

```text
Challenge JSON canónico
  → definición efectiva temporal por seed (sin reescribir el JSON original)
  → timeline derivado de las fases y FPS de la definición
  → Godot Movie Maker: fuente 540×960
  → FFmpeg delivery profile
       REVIEW_720  → 720×1280
       MASTER_1080 → 1080×1920
       MIN_540     → 540×960
  → MP4 + production manifest + telemetry/logs + metadata de review
  → FFprobe/framemd5 y QA de contrato
```

La duración se deriva de las fases canónicas; un `video.total_duration` obsoleto no sustituye el timeline calculado. Solo la definición temporal efectiva recibe el seed de ejecución. La QA histórica incluye 9 Challenges × 6 casos = 54 ejecuciones, con repetición A/B para determinismo; no se confunde con la matriz completa de revisión C.

### 2.2 Visual Loop

La ruta de cada familia parte del launcher existente `tools/prototypes/<family>/run_prototype.ps1`. La revisión histórica del launcher Geometric Waves confirma el patrón compartido:

```text
familia + grammar + seed
  → authoring/variation determinista
  → binder y renderer específicos de familia
  → capa editorial/social común
  → override.cfg temporal para viewport/window 720×1280
  → Godot Movie Maker, fixed-fps 30, captura AVI
  → audio WAV determinista de familia (según authoring)
  → FFmpeg H.264/yuv420p y mux AAC (video copy en el mux de música)
  → FFprobe + manifest + authoring + social sidecar + Godot log
  → stage de prototypes / posterior empaquetado en production
```

La composición lógica 540×960 se entrega mediante el canvas social 720×1280 (factor 4/3 según el contrato editorial). `override.cfg` es temporal: se preserva el fichero previo cuando existe y se restaura o elimina al salir. El helper de música `C11CSafeAmbient.py` es una entrada de compatibilidad que delega en el generador determinista `generate_c11c_family_music.py`; los parámetros de authoring seleccionan perfil, gramática, duración/ciclos y seed. El producto normal es un único MP4. AVI y MP4 silencioso son intermedios, no productos persistentes ordinarios.

### 2.3 Visual Drill

La ruta de revisión de Drill no es una simple variante de Loop:

```text
familia Drill + seed
  → generación de review envelope por familia/seed
  → timeline de fases + countdown + precedencia END_CTA/CTA terminal
  → binder y renderer de Drill
  → editorial/social compartida
  → C11CMovieCapture / override.cfg temporal 720×1280
  → Godot Movie Maker AVI a 30 FPS
  → FFmpeg H.264 silencioso
  → música ambiental de familia/seed
  → mux AAC (video copy) + FFprobe
  → MP4 + manifest + social sidecar + logs
  → keyframes/contact sheet/GIF de review
```

La música, el perfil y el semantic key se registran por familia/seed. Los artefactos de review se conservan separados de production.

### 2.4 Capa transversal y QA

- `C11CVisualEditorialLayer.gd`, `UnifiedSocialFrame`, los binders por familia, palettes, hooks y roles tipográficos forman la presentación social compartida; no sustituyen los renderers/binders de cada familia.
- Los Loop y Drill mantienen identidad, grammar/timeline, seed y música propios; Challenge conserva su productor y cronología específicos.
- El `Complete Video Review` de C11-C valida **52 vídeos**: 27 Visual Loops + 20 Visual Drills + 5 Longforms. Usa 7 workers aislados, cada uno con proyecto Godot y caché `.godot` privados; no se permite compartir `override.cfg` ni un fallback serial presentado como paralelismo.
- La salida final conserva MP4, manifests, authoring, FFprobe, logs, social sidecar y `PRODUCT.txt`/production manifest según ruta.
- `artifacts/prototypes` es regenerable; `artifacts/production/audiovisual` es persistente. Review no limpia automáticamente. “Los launchers generan; los cleaners limpian; production conserva”. Reemplazo exige operación explícita y se hace después de render y validación correctos.

## 3. Consecuencia de arquitectura para D+E

La sustitución debe reemplazar el ciclo de factoría completo, no solo colocar una cabecera/pie sobre un vídeo. El target D+E se ordena así:

```text
GUI actual / CLI compatibility adapter
  → mismo E1 Production Service (request normalizado)
  → resolver de familia + contrato/timeline original de Challenge / Loop / Drill
  → D9.9 plan + D9.10 bridge + D9.8 editorial model
  → layout D aprobado + compositor D-owned en el seam Option C
  → salida visual D separada y recibo de consumo de campos
  → audio por ruta familiar, con request.seed y request.music_seed separados
  → FFmpeg encode/mux según ejecución TEST_ONLY autorizada
  → FFprobe + QA de streams/timing/loudness/no-silence
  → manifests + social/authoring + recibos hash-pinned + review humano
```

### 3.1 Responsabilidades no intercambiables

| Dominio | C11-C histórico | D+E sucesor requerido |
|---|---|---|
| Mecánica/verdad determinista | C11-B/C congelada | Consumir sin modificar; no reimplementar ni reinterpretar |
| Familia/grammar/timeline | Binders y contratos específicos por familia | Mantener un resolver/servicio E común, sin aplanar contratos de familia |
| Editorial | C11CVisualEditorialLayer + hooks/telemetry | D9.8/D9.9: field allowlist, planes y copy por idioma/ámbito autorizado |
| Layout | Canvas social y binders históricos 540×960→720×1280 | D layout por familia, safe areas, clipping, jerarquía, campo y receipts de consumo |
| Música | Generador de familia/seed de C para Loop/Drill y ruta histórica Challenge | Challenge usa D3 Music V5; Loop/Drill conservan temporalmente música familiar ya aceptada hasta que exista una migración propia validada. No mezclar seeds |
| Captura/composición | Godot Movie Maker, rutas de captura específicas | D-owned consumer sobre seam existente; no crear segundo Producer, binder ni renderer paralelo |
| Entrega | FFmpeg, AAC, FFprobe, sidecars/manifests | E3 mux/QC + FFprobe y receipts reproducibles, gated por política de ejecución |
| Review/provenance | corpus físico, workers aislados, reportes | Smoke18 → Matrix101 + mapa regresivo C→E completo + E8 independiente |

**Aclaración musical:** “sustituir C” no significa borrar de golpe las rutas de música familiar que E4B/E4C han aceptado preservar. El primer target D+E debe mantener los contratos Loop/Drill estables mientras Challenge usa D3 V5; cualquier reemplazo posterior de música Loop/Drill necesita su propia cualificación y recibos. Así se evita que una mejora editorial introduzca una regresión de identidad sonora.

## 4. Option C y el estado real del compositor

Option C está aprobado como arquitectura: un único consumidor D-owned, en el seam existente, produce un artefacto D separado a partir de una fuente C inmutable y sus pruebas de identidad. La decisión arquitectónica no habilita dispatch/render/media.

Para el scope geométrico Loop E6 se aprobó el canvas 720×1280 con contenido 504×896 en `(108,192)`, header/footer negros de 192 px y gutters laterales de 108 px. Esta aprobación es de **geometría**, no de calidad del resampler ni del pipeline completo.

El compositor Python V4 pasó sus 37 tests funcionales de implementación, pero el benchmark Windows midió P95 2050.1467 ms (~0.488 fps): queda descartado como hot path a 30 FPS. El probe QImage V1 no ejecutó ningún test Qt: abortó en preflight por el error del adjudicador A3 documentado en el siguiente apartado. La variante QImage `SmoothTransformation` aún requiere runtime PASS, benchmark y revisión visual del resampler. No está integrada en E1/family-stage y no recibe aceptación E6.

La secuencia técnica es L1 sintético → L2 un selector/frame real copiado y verificado → L3 revisión visual/negative controls → L4 seis Loop Smoke18 selectores → L5 integrar filas Smoke18 después de política y manifiesto TEST_ONLY. La geometría aprobada no reemplaza las autorizaciones D4.8/D9.10.

## 5. Cierre de límites y criterio de sustitución

- C11-C 2.19.12 continúa siendo la única autoridad de producción hasta E8 y promoción separada.
- No alterar `release/C11C_FREEZE_PACKAGE_MANIFEST.json`, generadores/mecánicas C protegidos, RNG, `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector`, `RenderedFrameStream`, audio core ni definiciones canónicas.
- No renderer, launcher, dispatch ni media hasta que exista una política sucesora D4.8 acotada y un manifiesto de ejecución TEST_ONLY exacto.
- D4.8 V2 continúa BLOCKED; D9.10 PREPARE_ONLY; D9.14/D9.16 BLOCKED; D9.17 BLOCKED_NO_GO; D10 BLOCKED_FOR_PROMOTION.
- E6 accepted = 0; Smoke18 reutiliza evidencia elegible pero no la acepta por sí sola; Matrix101 no está congelada; CH_008/009 permanecen retenidos por la discrepancia 11 s/12 s.
- La sustitución de C por D+E solo será demostrable cuando la factoría nueva cubra las tres rutas, sus pipelines de música, layout/editorial, reproducibilidad, QA/receipts, GUI/CLI parity y regresión histórica completa; E8 independiente y decisión de promoción son obligatorios.
