# C11-E Gates and Acceptance Matrix — V25

**Date:** 2026-11-03
**Checkpoint:** E3 V1.3 patch applied; V1.4 Windows tests 31/31 PASS.

| Gate | Status | Evidence / outstanding acceptance |
|---|---|---|
| E0 | PASS / retained | Foundation restart accepted. |
| E1 shared service | PASS automated; GUI runtime still pending | GUI must remain primary operator workflow; CLI same-service parity only. |
| E2 CH001 A/B | FORMALLY CLOSED (bounded) | R4 receipt `2f8c3554...cadef7f`; R4 evidence ZIP `f33431bb...67a3de`; visual board reviewed. No audio. |
| E3.2 V5/E1 binding | PASS / committed | Contract and deterministic tests previously accepted. |
| E3 V1.3 patch | APPLIED 10/10 | One main.py replacement plus nine add-only payloads; hashes verified. |
| E3 Windows V1.4 suite | PASS 31/31 | Python 3.13.14; compile PASS; PySide6 6.11.2; test mux temporary-only; no renderer/GUI/production media. Receipt SHA `84fc86c96ca237c7dd16837666882e80afe6dda8292a04527d19fcbd3579e30b`. |
| E3 GUI runtime | PENDING | Real Windows Producer GUI launch/action/progress/error/result observation. |
| E3 raw audio/master/mux/FFprobe pilot | PENDING | GUI-triggered, test-only CH001 using immutable R4 input; preserve video frames. |
| E3 repeatability/seed isolation | Unit tests PASS; physical run confirmation pending | Same seed same audio; changed music seed changed audio; video unchanged. |
| E3 formal exit | BLOCKED | All ten exit evidence categories in backlog V2 required. |
| E4A Challenge | NOT STARTED | Full Challenge family editorial/presentation. |
| E4B Loop | NOT STARTED | Family binder and existing C11-C grammar/music adapter. |
| E4C Drill | NOT STARTED | Family binder and phase/END_CTA precedence. |
| E5 cross-family QA | NOT STARTED | Determinism, seed separation, no leakage, GUI-first and CLI parity. |
| E6 Smoke18 | NOT STARTED | 6 Challenge + 6 Loop + 6 Drill. |
| E7 Matrix101 | NOT STARTED / bounded | 54 + 27 + 20; CH_008/009 withheld (declared 11s vs phase sum 12s); provisional runnable population 99. |
| E8 independent acceptance/freeze/promotion | NOT STARTED | Explicit separate authority required. |

## Hard locks

`release_authority=NONE`; `baseline_promotion=false`; `freeze_eligible=false`; C11-C 2.19.12 remains authoritative. No core/audio or protected C generator/mechanics changes, no C11-C manifest edits, no additional suite module, no second producer, no manual CLI operator workflow.

## Immediate next gate

`E3-GUI-01`: launch the existing Producer GUI using the actual checkout entry point; confirm the E3 control is surfaced and invokes the E1 shared service; run one controlled CH001 audio-only attach pilot against the R4 fixture, test-only output, no gameplay render. Collect GUI observation, audio provenance, mastering QA, FFmpeg/FFprobe and receipt. Do not rerun V1.4's already-passing 31 tests.
