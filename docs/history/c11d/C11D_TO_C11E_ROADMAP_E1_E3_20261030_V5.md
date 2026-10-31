# Transición C11-D → C11-E: roadmap E1–E3 (V5)

## Propósito

C11-C 2.19.12 sigue siendo el motor productivo congelado. C11-E construye una capa unificada de request, presentación editorial y música que reutiliza el motor físico y los componentes D sin duplicar la simulación.

## Hitos y evidencias

- E0: instrucciones E y jerarquía documental desplegadas, histórico D archivado y reconciliación confirmada.
- E1: servicio compartido de preparación GUI/CLI en `c11c-producer`; 8/8 archivos aplicados y dos pruebas Windows 2/2 PASS. Observación manual GUI pendiente.
- E2: first real visual proof, two `CHALLENGE_001` MP4s, only `production_override.title` differs; gameplay and both seed domains remain invariant. V2 HEAD mismatch and V3 Windows path-guard bug both failed before writes/render; V4 fixes the path guard and is pending execution.
- E3: D3 music generation and FFmpeg mux only after E2 visual acceptance; independent `music_seed`.

## Resto del plan

E4 one physical video per family Challenge/Loop/Drill; E5 determinism/regression; E6 Smoke18; E7 Matrix101; E8 formal acceptance/promotion. CH_008/009 remain excluded until explicit resolution of 11s versus 12s declared duration. No gate implies release authority unless E8 records approval.

## Guardrails

No mutation of C simulation/mechanics/RNG or frozen manifest; no changes to `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector`, `RenderedFrameStream`. Preserve `main` and all existing refs. Do not turn D9.10 `PREPARE_ONLY` into an executor. Do not bypass the C11-D governance record. Keep source-level, runtime, media, pixel and human-review evidence separate.
