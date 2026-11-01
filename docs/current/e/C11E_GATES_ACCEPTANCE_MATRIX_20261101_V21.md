# C11-E gates and acceptance matrix â€” V21

**Date:** 2026-11-01. Do not conflate preflight, partial render, and gate acceptance.

| Gate | Status | Evidence / next action |
|---|---|---|
| E0 restart | PASS / retained | Prior accepted E0 receipt. |
| E1 shared service | Automated PASS 2/2; GUI observation pending | Shared service remains the sole CLI/GUI production path. |
| E2 V9 install reconciliation | PASS | 16 operations: 12 applied, 4 already present. |
| E2 Godot JSON numeric | PASS 30/30 | Godot 4.7.1 Mono; float seed types; complete sidecar valid. |
| E2 Python pair contract | PASS 9/9 | Corrected V9 contract test, including revised test 09. |
| E2 runner source pin | PASS | Corrected test SHA pinned in runner. |
| E2 FFmpeg range normalization | PASS on retained R3 A AVI | Installed FFmpeg 9.0 QA transcode probes as H.264 High, yuv420p, tv, 720Ã—1280, 30 FPS, 270 frames, no audio; V21 V3 repeats this check before writing. |
| V21 V2 applicator | FAILED / rolled back | PowerShell 5.1 treated successful Python unittest stderr as terminating `RemoteException`; no V21 docs/receipt accepted. V21 V3 uses `System.Diagnostics.ProcessStartInfo` async stream capture. |
| E2 physical A/B R3 | FAILED / partial | A rendered and MP4 created; B not invoked; runner rejected yuvj420p/pc. Failure ZIP SHA `cff29f245a1c8cf97ac02cd7bed3455a0a2ac364248f7cf257a2b148f2e0f6ab`. |
| E2 physical A/B R4 | PENDING | Run with new ID; two renders; both MP4 metadata and frame comparisons must pass. |
| E2 visual and independent acceptance | PENDING | Inspect complete A and B videos and record separate decision. |
| E3 D3 Music V5 | BLOCKED | After E2 acceptance only; independent music seed, deterministic generation, FFmpeg mux, FFprobe A/V validation. |
| E4A Challenge | NOT STARTED | Family presentation/editorial adapter. |
| E4B Visual Loop | NOT STARTED | Loop binder and family adapter. |
| E4C Visual Drill | NOT STARTED | Drill binder and family adapter. |
| E5 determinism and parity | NOT STARTED | Seed isolation, repeatability, GUI/CLI parity. |
| E6 Smoke18 | NOT STARTED | Six cases per family. |
| E7 Matrix101 | NOT STARTED / qualified | 54 Challenge + 27 Loop + 20 Drill planned; currently runnable population 99 because CH_008/009 remain held. |
| E8 independent acceptance/freeze/promotion | BLOCKED | Explicit independent decision and release authority required. |

C11-C 2.19.12 remains the production authority until E8. R1, R2 and R3 are immutable failed attempts and their request IDs must not be reused.