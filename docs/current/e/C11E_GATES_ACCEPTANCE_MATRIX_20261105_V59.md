# C11-E Gates and Acceptance Matrix — V59

**Date:** 2026-11-05. Supersedes V58 for V3/V4 postprocess disposition.

| Gate | Status | Boundary / next action |
|---|---|---|
| E0–E3 | Accepted in previously recorded scopes | Do not repeat without concrete pin drift/defect. |
| E4A.2 | PASS test-only | Accepted Challenge 004 source/body base. |
| E4A.3D.1 | PASS test-only | Isolated D compositor proof; no generic layout approval. |
| E4A.4 | PASS isolated audio/mux test-only | D3 V5/D3.3/AAC/FFprobe on C11-C review MP4; not D-composited video. |
| E4A.5B | PASS read-only source closure | 88-member reconciliation and live root/launcher review recorded. |
| E4A.6 root consumer | PASS_TEST_ONLY | 17/17 tests; Godot live root; 900 frames; mount=1; header=180; footer=120; native CTA=0. |
| E4A.6 Movie Maker | PASS_TEST_ONLY_CAPTURED | Existing AVI: 900 frames/60 FPS; configured marker, telemetry and completion marker present. No rerun. |
| E4A.6 postprocess V1 | BLOCKED_BEFORE_WORK | Wrong 63-character manifest SHA constant; no processing. |
| E4A.6 postprocess V2 | BLOCKED_AT_SOURCE_FFPROBE | Wrapper exposed empty `ExitCode`; stderr empty; FFprobe failure not established. |
| E4A.6 postprocess V3 | BLOCKED_AT_BOUNDARY_STILLS | FFmpeg rejected `-vsync`; V3 had already created and FFprobe-validated the silent MP4. A later rerun refused to overwrite it. No complete receipt. |
| E4A.6 postprocess V4 | READY_TO_RUN | Revalidates/reuses V3 MP4 when valid; otherwise encodes and verifies a temporary candidate. Uses `-fps_mode vfr`; no `-vsync`; idempotent still extraction. |
| E4A visual/layout review | PARTIAL | Operator reported no obvious defects; formal geometry/safe-area approval NOT_GRANTED. |
| E4A final D-composited A/V | PENDING | D-composited Challenge video + D3 V5, D3.3 mastering, approved mux/FFprobe; A/B/C music-seed isolation and human listening/sync review. |
| E4B Loop | HELD | Preserve Loop grammar/variant timeline, binder and existing family music. |
| E4C Drill | HELD | Preserve Drill phase/END_CTA precedence, binder and existing family music. |
| E5 | PENDING | Cross-family determinism, seed isolation, adapter/profile non-leakage, GUI/CLI parity. |
| E6 | PENDING | Smoke18: six audiovisual scenarios per family. |
| E7 | PENDING | Matrix101: 54 Challenge + 27 Loop + 20 Drill; CH_008/009 held for 11s/12s discrepancy. |
| E8 | BLOCKED | Full historical C-to-E map, independent acceptance, immutable freeze and explicit separate promotion. |

## Source/baseline note

The C11-C frozen manifest remains 796,318 bytes / SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`. Its `GeneradorMaestro.gd` entry pins original SHA `4f10144c62c7bc149bd46aa37494b1df40c7185544b8477153150eec71c1aaf9`; the active D-only postimage is `d42782e8f5bb94ff0ede653a1c4624dc91541cc8203abf136b09a8fc288a7d82`. The frozen artifact/manifest remain unchanged; no further writes to this active path until D/E source isolation is resolved.

## Governance

Production renderer OFF, dispatch OFF, media OFF. `release_authority=NONE`. C11-C remains production authority. No release, freeze or promotion authority.
