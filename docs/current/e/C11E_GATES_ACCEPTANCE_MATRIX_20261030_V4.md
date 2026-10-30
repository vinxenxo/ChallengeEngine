# C11-E — gates y matriz de aceptación (V4)

**Fecha:** 2026-10-30 · **Rama:** `main` · **Estado:** E0 verificado; E1 en curso.

| Gate | Estado | Alcance y criterio de salida |
|---|---|---|
| E0 — Foundation/bootstrap | `PASS` | V3 aplicado en `main`; receipt inspeccionado; 12/12 ficheros y 2/2 archivos históricos verificados; pin del manifiesto C exacto; refs y HEAD preservados; sin código, render ni media. |
| E1 — Servicio canónico GUI/CLI | `IN_PROGRESS` | Diseñar/implementar un único servicio de producción E dentro de `c11c-producer`; usar request canónico/resolver D9.9 sin reutilizar su bridge/adapter plan-only. Contract tests de paridad GUI/CLI, hashes, validación y errores. Aún sin dispatch físico. |
| E2 — Challenge title-to-pixels | `NOT_STARTED` | Un consumidor editorial E aditivo con slot `title` dedicado y dos MP4 aislados de `CHALLENGE_001`. Mismo gameplay seed/config/mecánica/duración/frame count; solo cambia `title`; fuera del slot visual, los frames deben coincidir o las diferencias deben explicarse. |
| E3 — D3 audio + mux | `NOT_STARTED` | Integrar D3 usando solo `music_seed`; WAV/receipt, FFmpeg mux, FFprobe y determinismo. No altera vídeo base. |
| E4 — Loop/Drill físicos | `NOT_STARTED` | Un render aislado de cada familia tras certificar sus adaptadores/slots. Reutilizar compositores C; no duplicar motores. |
| E5 — Determinismo/regresión C | `NOT_STARTED` | Repeticiones, seeds cruzadas, suite C pertinente, paridad GUI/CLI y auditoría de ausencia de cambios mecánicos. |
| E6 — Smoke 18 | `NOT_STARTED` | Casos declarados individualmente, sin ocultar fallos ni skips. |
| E7 — Matrix 101 | `NOT_STARTED` | 54 Challenge + 27 Loop grammar + 20 Drill variants; exclusiones 008/009 visibles y denominador recalculado cuando corresponda. |
| E8 — Aceptación/promoción | `NOT_STARTED` | Decisión independiente, manifest/tree/ZIP hash, freeze E y migración reversible; C11-C sigue en producción hasta aceptación explícita. |

## Reglas de transición

- E0 PASS no significa E1 completado ni autoriza render.
- E1 solo demuestra contrato/paridad de servicio; no emite MP4.
- E2 habilita exactamente la pareja A/B Challenge aislada, no una corrida masiva.
- E3 audio y mux no forman parte de E2.
- E4 requiere aprobación del propio gate E y no deriva de un PASS Challenge.
- E6/E7 no pueden ampliar la autorización de producción o release.
- Los bloqueos D (`D4.8`, `D9.10`, `D9.14`, `D9.17`, `D10`) conservan su valor histórico D; no se reescriben ni cambian por los gates E.

## Condiciones permanentes

Manifiesto C11-C: SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`, 796318 bytes. No modificar ni regenerar. `request.seed` y `request.music_seed` son dominios separados. No mutar simulación, timeline, `winning_frame`, `close_calls`, RNG, mecánicas ni frames fuente de C.
