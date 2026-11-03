# C11-E Gates Acceptance Matrix — V37

| Gate | Status | Evidence / next action |
|---|---|---|
| E0/E1 | PASS retained | Shared production service; no repeat absent source drift |
| E2 | PASS bounded | CHALLENGE_001 R4 title-to-pixels only |
| E3/E3.2 | PASS test-only | Accepted D3 V5 audio/mux pilot and 50/50 negative controls |
| E4A discovery + GUI contract | PASS within scope | Source audit / GUI contract successor retained |
| E4A Gate A | CLOSED_WITH_BLOCKERS | Editorial sidecar 14/14; I/O 0/10 complete, 6 partial, 4 blocked |
| E4A policy V1 | APPROVED | Operator-approved exact Challenge semantic mapping |
| E4A.1 | PASS — FIXTURE ONLY | Godot 4.7.1; 23/23; 18 PNG @ 540×960; 12 comparisons; neutral BODY |
| E4A.2 first Windows execution | FAIL — HARNESS ASSUMPTION | C11-C source render completed; runner failed before PNGs due raw source 60fps/900 + yuvj420p/pc vs assumed 30fps/450 + yuv420p; manifest unchanged |
| E4A.2 corrected V2 | PREPARED / WINDOWS REPLAY REQUIRED | Runner `5c0e8765bb29b58ddefc1b9593be188227e77725431c3dc959c1ce6866529a9b`; tests `657f459ce11621a2dde133da5234ea27754c56b3acb5a10c8b37ff952a48d07b`; 33/33 tests; exact uploaded MP4 replay 18 PNG / 12 comparisons; reuse prior MP4, no Godot rerun |
| E4A.2 visual placement | NOT ACCEPTED | Placeholder title/subtitle overlap C11-C hook headline in test montage; D1.5 safe area/typography unknown |
| E4A.3 actual D consumer | NOT YET IMPLEMENTED | D-owned composition/layout consumption; no C aliases or parallel binder |
| E4A.4 A/V + review | PENDING | Reuse accepted E3 D3 V5/mux/FFprobe; operator visual acceptance |
| E4A closure | OPEN | Requires actual D consumer, layout, A/V and review |
| E4B Loop | BLOCKED_BY_SEQUENCE | Begin after E4A close |
| E4C Drill | BLOCKED_BY_SEQUENCE | Begin after E4B; retain END_CTA/music contracts |
| E5 | OPEN | Determinism, independent seeds, family/profile non-leakage, GUI/CLI parity |
| E6 Smoke18 | OPEN | Six actual A/V cases per family |
| E7 Matrix101 | OPEN / 99 PROVISIONAL | CH_008/009 held for 11s declared vs 12s phase sum |
| E8 | BLOCKED | Historic C11-C corpus map, independent acceptance, immutable freeze and separate promotion |

## Evidence notes

E4A.2 failed archive `RUN_20261103_235800_fd6fb07c.zip`: SHA `2430588990a6d82aad68082fab000b71b5218af42f27cce75633b7153e06a53d`; source MP4 SHA `fdd0598e20ddc6201e54cc2dad7fd3362c2ef80961df44f3ef4676fb97a765de`. The source stream is H.264 `yuvj420p` full-range `pc`, 720×1280, 60fps, 900 frames, 15s, no audio. The C11-C production manifest declares `yuv420p`; discrepancy is retained and disclosed. The failure was the runner's incorrect raw-source precondition, not an accepted pixel result.

Corrected V2 local replay used the exact supplied MP4 bytes, generated a separate test-only limited-range 30fps/450-frame derivative, and passed 18/18 PNGs and 12/12 comparisons with zero A/B BODY changes and B/C pixel identity. It is preparation evidence only until the corrected runner executes on Windows and its full receipt is reviewed.

The fixture's test-only text coordinates are not production layout values. A montage shows overlap with the current C11-C HOOK headline. D1.5 safe-area and generic typography values are UNKNOWN; no visual placement acceptance is given.

## Governance

C11-C 2.19.12 remains sole production authority; frozen manifest SHA `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953` (796,318 bytes). D production renderer OFF; D9.10 PREPARE_ONLY; D4.8 BLOCKED; D9.14/D9.16 BLOCKED; D9.17 BLOCKED_NO_GO; D10 BLOCKED_FOR_PROMOTION; `release_authority=NONE`; no freeze/promotion.
