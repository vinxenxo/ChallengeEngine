# C11-E E6 — Registro de evidencia aceptada y reutilización candidata

**Fecha:** 2026-11-17 · **Estado:** `EVIDENCE_LINEAGE_REGISTER / E6_REUSE_NOT_YET_ACCEPTED`

## Cierres históricos que deben conservarse

| Área | Evidencia existente | Disposición |
|---|---|---|
| E4A/B/C | Alcances E4 aceptados; E4C 20/20 | Cerrados; no repetir |
| E5 | `PASS_CLOSED_TEST_ONLY`; tres pruebas Qt visibles 3/3 | Cerrado; no repetir canary/Qt |
| R1V | 10/10 técnico A/V y 10/10 visual/audio humano | Cerrado; no repetir |
| Loop22 | 44/44 A/V y 22/22 A/B; 44/44 revisión humana | Cerrado; no repetir |
| Challenge CH004 | E4A.7 A/V receipt `102cf07a0b8920318c3ba211a3bd4374c3e080018486363d701f81e65613aaa0` | Reutilización E6 candidata, no aceptada aún |

## Candidatos Loop (6/6)

| Grammar / variant | Gameplay seed | Music seed | Timebase | Evidencia indicada |
|---|---:|---:|---:|---|
| `fractal_bloom / radial_bloom` | 100006 | 500006 | 22 s @ 30 fps | R1V aceptado |
| `geometric_waves / harmonic_membrane` | 100001 | 500001 | 23 s @ 30 fps | Par GEOAVR2 de reemplazo + cierre R1V |
| `invisible_forces / dipole_field` | 100021 | 500021 | 22 s @ 30 fps | R1V aceptado |
| `living_particles / swarm` | 100016 | 500016 | 20 s @ 30 fps | R1V aceptado |
| `sacred_symmetry / astrolabe` | 100011 | 500011 | 23 s @ 30 fps | R1V aceptado |
| `geometric_waves / interference_plane` | 100002 | 500002 | 23 s @ 30 fps | Loop22 aceptado |

La tabla identifica candidatos, no sustituye los recibos. Para cada selector hay que vincular recibo exacto y SHA de MP4/AAC/WAV/streams que existan, junto con FFprobe, QA, seed/profile/timebase, revisión humana y source pins. El resumen actual no expone todos los media hashes por selector. No se deben propagar hashes de un selector a los demás.

## Candidatos Drill (6/6)

| Drill selector | Receipt SHA-256 |
|---|---|
| `tracking / tier-2` | `f95e9b4e787f1b4f7db79b92428324f6de662ade55b260c7692d4440e2967ee7` |
| `pursuit / tier-1` | `57206b45…acc6eee7` |
| `saccade / tier-1` | `930ba103…1282e606` |
| `peripheral_scan / tier-1` | `eb290666…19964083b` |
| `tracking / tier-5` | `6e55dc3f…690c3c61` |
| `peripheral_scan / tier-5` | `5644ffa386c2d1388e7dd657cb566c796a87de93b22c28db84197dbb8ad3a224` |

Las tres entradas con puntos suspensivos son abreviaturas de visualización que deben sustituirse por valores completos extraídos del ledger/recibo original antes de congelar E6. No son SHA válidos para pinning. Las seis rutas y los hashes completos figuran en el recibo del audit E6 Drill. No volver a ejecutar E4C para reconstruirlos.

## Challenge CH004

- Recibo E4A.7: SHA `102cf07a0b8920318c3ba211a3bd4374c3e080018486363d701f81e65613aaa0`.
- Fuente MP4 silenciosa normalizada: SHA `841b03531301c7e70c0e09ce3e9f536241d2072a87792e099ed7a955bef8c52f`.
- Metadata conocida: 720×1280, 30 fps, 450 frames, 15 s, H.264 High, yuv420p, rango TV.
- A/B/C y sus medios anidados deben ser verificados íntegramente contra las predicates E6 antes de marcar `REUSE_ACCEPTED`.

## Regla E6 de aceptación de reuse

Cada fila permanece `REUSE_CANDIDATE_NOT_ACCEPTED` hasta que el ledger final contiene: fuente/receipt hash, hashes de todos los archivos anidados, selector/familia/gramática/tier, seeds, perfil, timebase, metadatos FFprobe, resultados audio QA, stream identity/repeatability aplicable, aprobación visual/audio del operador y source-pin lineage. Un artefacto previamente aceptado por E4/E5 no es automáticamente aceptado por E6, pero tampoco se vuelve a generar por faltar metadatos en un resumen.
