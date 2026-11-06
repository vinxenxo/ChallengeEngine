# C11-E Gates and Acceptance Matrix — V65

**Date:** 2026-11-05. V65 records V1.1 Git-check removal and the two subsequent documentation-preflight failures; V1.2 is the standalone self-hydrating correction. Production governance is unchanged.

| Gate | Status | Acceptance / next action |
|---|---|---|
| E0–E3 | Accepted in recorded scopes | Do not repeat without concrete source drift or a new defect. |
| E4A.2 | PASS_TEST_ONLY | Challenge 004 base. |
| E4A.3D.1 | PASS_TEST_ONLY | Isolated D compositor proof; no generalized layout approval. |
| E4A.4 | PASS_TEST_ONLY | D3 V5/D3.3/mux/FFprobe on C11-C review video; not D-composited. |
| E4A.5B | PASS_READ_ONLY | 88-source closure. |
| E4A.6 runtime V3 | PASS_TEST_ONLY | 17/17; Godot 4.7.1; 900 frames; one mount. |
| E4A.6 postprocess V4 | PASS_TEST_ONLY_VISUAL_POSTPROCESS (superseded for final visual requirement) | Pre-correction output; grey inactive bands did not meet the later operator requirement. |
| E4A.6 reserved bands V1 | BLOCKED_BEFORE_EXECUTION | PS 5.1 parser rejected two `$i:` expressions; no V1 execution. |
| E4A.6 reserved bands V2 source/runtime/capture | PASS_TEST_ONLY_COMPONENTS | AST PASS; 22/22 Python; Godot import; live-root 900/900; Movie Maker AVI 900/900 with matching configure and phase telemetry. |
| E4A.6 V2 wrapper completion | BLOCKED_RUNNER_FALSE_NEGATIVE | Path-based `Test-CaptureLog` received `$movie.Stdout` text. It returned false before validating markers; not a renderer or consumer failure. |
| E4A.6 recovery V1 | BLOCKED_PREFLIGHT_ONLY | Invalid fixed `HEAD` pin; operator-managed commit advanced to `d5589fde1e5132c653c1ac5604a34a524c02a47a`. No media/evidence processing or writes occurred. |
| E4A.6 recovery V1.1 | BLOCKED_DOCUMENTATION_PREFLIGHT_ONLY | First run: packaged doc manifest missing beside runner. Second run: manifest copied alone; 15 relative docs/prompts were absent. Both stopped before FFmpeg/media/source/doc writes. |
| E4A.6 recovery V1.2 | READY_STANDALONE_RUNNER | No Git checks; exact source pins remain. Documentation manifest and all 15 payloads are embedded as a compressed, SHA-pinned package and self-extracted inside the unique recovery evidence root. Only runner `.ps1` is required in Downloads. Reuses AVI; no rerender/test rerun. Awaiting Windows run. |
| E4A final audiovisual | PENDING | Corrected D MP4 + actual D3 V5/D3.3; A/B/C music-seed isolation; AAC mux/FFprobe; sync/listening review and E1 GUI/CLI parity. |
| E4B Loop | HELD | Opens only after full E4A acceptance. |
| E4C Drill | HELD | Opens after E4B integration/acceptance. |
| E5 | PENDING | Determinism, seed domains, family/profile isolation and GUI/CLI parity. |
| E6 Smoke18 | PENDING | Six A/V scenarios per family. |
| E7 Matrix101 | PENDING | 54 + 27 + 20; CH_008/009 held for 11 s/12 s discrepancy. |
| E8 | BLOCKED | Historical regression map, independent acceptance, freeze and separately authorized promotion. |

## Recovery invariants

The uploaded AVI SHA-256 is `2f6d0c73cb09571584db68e37760c933706473a07e559fc93113f26eabb89f45`. Its video stream is MJPEG 540x960, 60/1 FPS, 900 frames, 15 s. FFprobe also detects PCM S16LE 48 kHz stereo; ignore it with `-map 0:v:0 -an`. Delivery MP4 must be H.264 High, 720x1280, 30/1 FPS, 450 frames, 15 s, yuv420p, color_range `tv`, zero audio streams. Extract frames 0, 89, 90, 299, 300, 389, 390, 449. Audit inactive HEADER/FOOTER bands at RGB threshold <=8 and <=0.1% non-black samples; verify active HOOK header and CTA footer each have at least 100 non-black samples.

## Source and governance boundary

The recovery runner does not write source. Consumer SHA `eba81fff4c24ca75033c8f963665df1961136046c41fee0e88681fe55a631203`; focused test SHA `9845eda094037f8748493171755b32d3479ddf6548612e9a6ecebba187cbc512`. C11-C manifest remains 796,318 bytes / `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`. Active `GeneradorMaestro.gd` remains `d42782e8f5bb94ff0ede653a1c4624dc91541cc8203abf136b09a8fc288a7d82`; no write. Frozen shared layer remains read-only.

Per-iteration runners must not consult Git; the operator commits each iteration. Production renderer/dispatch/media remain OFF; `release_authority=NONE`.
