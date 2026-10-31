# C11-E — autoridad y continuación vigentes (V4)

**Fecha:** 2026-10-30 · **Rama local:** `main` · **HEAD reconciliado:** `bc8330e794fe37efe0c4f9c2bb0c0bd389f28f2c`.

C11-E integra la solicitud editorial universal con la producción física existente de C11-C y la música D3, manteniendo C11-C 2.19.12 como baseline de producción hasta aceptación E8.

## Lectura obligatoria

1. `C11E_CURRENT_AUTHORITY_20261030_V4.md`.
2. `C11E_GATES_ACCEPTANCE_MATRIX_20261030_V4.md`.
3. `C11E_E0_REVIEW_AND_E1_SOURCE_ARCHITECTURE_20261030_V1.md`.
4. `C11E_DOCUMENTATION_RECONCILIATION_20261030_V4.md`.
5. `C11E_PROGRAM_CHARTER_20261030_V3.md` y `C11E_ARCHITECTURE_CONTRACT_20261030_V3.md`.
6. `C11E_OPEN_DECISIONS_AND_RISK_REGISTER_20261030_V3.md`.
7. `../history/c11d/C11D_TO_C11E_ROADMAP_TRANSITION_20261030_V1.md` (ruta relativa desde `docs/current/e`: `../../history/c11d/C11D_TO_C11E_ROADMAP_TRANSITION_20261030_V1.md`).
8. `prompts/C11E_CONTINUATION_MASTER_PROMPT_20261030_V4.md` en la raíz del repositorio.

## Estado

- E0: PASS; instalación y recibo revisados independientemente.
- E1: IN_PROGRESS; inspección de arquitectura realizada, servicio canónico compartido GUI/CLI pendiente de implementación y contract tests.
- E2: NOT_STARTED; primer objetivo visible `title`-to-pixels en `CHALLENGE_001`.

Los documentos V3 de planificación se conservan. Las referencias V3 que dicen que E0 no se aplicó o que sigue pendiente quedan supersedidas por este README y los documentos V4/V1 de revisión.

## Objetivo funcional

Primero demostrar dos MP4 `CHALLENGE_001` con igual gameplay/seed/duración/frames y distinto texto `title` visible en un slot propio. `title` no es `hook` ni CTA. Después: D3+audio/mux, Loop/Drill, regresión, Smoke 18, Matrix 101 y decisión E8.

## Límites

No cambiar el manifiesto C11-C (`e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`, 796318 bytes), simulación, RNG, `winning_frame`, `close_calls` ni mecánicas. No convertir D9.10/fachada D en dispatcher E. No cambiar rama ni refs. `request.seed` y `request.music_seed` son independientes. CHALLENGE_008/009 siguen excluidos por la discrepancia 11 s/12 s.
