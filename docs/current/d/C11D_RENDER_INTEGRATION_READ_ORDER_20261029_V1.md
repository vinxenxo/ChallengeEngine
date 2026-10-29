# C11-D render integration — mapa de lectura por tarea V1

Este mapa reduce la relectura histórica de todos los prompts/checkpoints. Las rutas se deben confirmar en el checkout activo.

| Necesidad | Leer primero | Abrir solo si hace falta |
|---|---|---|
| Reglas de repositorio | `AGENTS.md`, `.continue/rules/CONTINUE.md` | Changelog si una regla contradice un historial antiguo |
| Estado actual / pins | `C11D_ENGINEERING_PHASE_LEDGER_20261029_V18.md`, `C11D_FULL_CONTEXT_CONTINUITY_CHECKPOINT_20261029_V41.md`, `C11D_PHASE_AD_EXECUTION_CLOSEOUT_20261029_V1.md` | Recibos y paquetes X–AD si se precisa verificar un dato puntual |
| Objetivo de producto y próxima tarea | `C11D_FUNCTIONAL_RECOVERY_AND_MEDIA_ACCEPTANCE_PLAN_20261029_V1.md` | Este mapa y master prompt |
| Qué protege C | `docs/current/c11c/C11-C_2.19.12_ACCEPTANCE_EVIDENCE.md`, `C11-C_2.19_CONSOLIDATED_ACCEPTANCE_GATE.md` | `C11-C_2.19.12_CLOSURE_AND_FREEZE_READINESS.md`; scripts de QA C |
| Familia/selector y plan | Universal Editorial Model D9.8, Producer/request plan D9.9, `c11c-suite` manifests | Visual Loop/Drill selector inventories |
| Música | D3 Music Engine V5, unified audio/music policy, mux and seed audits | D9.14 Challenge audio-mux verification |
| Input/output visual | Candidate I/O gap audit, request-scoped payload binding/materialization, logical composition/frame program, candidate identity | V2B semantic/crosswalk/runtime receipts |
| Texto editable visible | editorial model, shared production context/view model, field-consumption audit, region/visibility and temporal contracts | historical sidecar/visibility proposals |
| Vídeo físico | D9.14 runbook; existing C launchers; Godot/FFmpeg actual logs | old bounded qualification logs/results |
| GUI operation | `c11c-producer`, `c11c-test`, GUI contracts/runtime tests and five-surface operational checkpoint | Qt offscreen logs and operator evidence ledger |
| Final acceptance | C acceptance scripts plus D9.14/15/16/17 and candidate evaluator | Historical freeze/promotion docs only after all candidate gates pass |

## Entry points inherited from C

Review, do not blindly run, these canonical examples:

```powershell
python -u .\c11c-suite\self_test.py
python .\tests\run_all.py
python .\c11c-suite\c11c-test\self_test.py
.\tools\qa\c11\run_c11c_challenge_bulk_qa.ps1
.\tools\qa\c11\run_c11c_complete_video_review.ps1
```

Read each runner's parameters, output root and acceptance markers before invoking. For D media tests, set a unique test output root and preserve stdout/stderr/exit code. Do not point a QA runner at a production/release folder.

## Why older “next task” sections are not all current

A historical prompt may say the next phase is a seed collision audit; a later checkpoint can close it. Phase X–AD then devoted many turns to source-corpus and authority-intake records. Those records remain immutable evidence, but their old `NEXT` text does not supersede this functional recovery sequence. The new working sequence is the D-owned presentation/editorial consumer, real A/V pilot and family coverage, followed by full acceptance.
