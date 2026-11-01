# C11-E gates and acceptance matrix â€” V20

**Date:** 2026-11-01. Statuses below distinguish tests passed from gates still awaiting physical and independent acceptance.

| Gate | Status | Evidence / boundary |
|---|---|---|
| E0 restart | PASS / retained | V2 restart receipt accepted. |
| E1 shared service | PASS automated 2/2; GUI observation pending | Shared service remains the single CLI/GUI production path. |
| E2 V9 reconciliation | PASS | 16 operations: 12 applied + 4 already present. |
| E2 Godot numeric contract | PASS 30/30 | Native Godot 4.7.1 Mono; gameplay/music JSON float; full sidecar validation. |
| E2 Python pair contract | PASS 9/9 | Corrected test 09 verifies V9 shared-validator delegation and title source. |
| E2 runner source pin | PASS after V20 correction | Runner pins corrected test SHA; new runner SHA `c5d6bc26c70151238f60466fa401e1fd14ef9b0a25b34aa45d98ebce2ba5c763`. |
| E2 physical A/B | PENDING R3 | R1/R2 failed before renderer (zero renders and media). R3 is next; no audio. |
| E2 human visual/independent acceptance | PENDING | Requires actual A/B videos, receipt, ZIP, FFprobe and separate review decision. |
| E3 D3 Music V5 | BLOCKED | No E3 until E2 automated + human acceptance. |
| E4A Challenge | BLOCKED | Presentation/editorial adapter integration. |
| E4B Visual Loop | BLOCKED | Loop binder/adapter integration. |
| E4C Visual Drill | BLOCKED | Drill binder/adapter integration. |
| E5 determinism/parity | NOT STARTED | Gameplay/music seed isolation, deterministic repeatability and GUI/CLI parity. |
| E6 Smoke18 | NOT STARTED | Six scenarios per family. |
| E7 Matrix101 | NOT STARTED / qualified | 54 Challenge + 27 Loop + 20 Drill planned; currently runnable population is 99 because CH_008/009 are held. |
| E8 independent acceptance/freeze/promotion | BLOCKED | Requires independent decision and explicit authority. |

R1 and R2 remain immutable failed pre-render attempts. No source repair may reuse their request IDs. C11-C remains the production authority until E8.