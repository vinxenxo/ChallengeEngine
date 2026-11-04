# C11-E Gates & Acceptance Matrix — V40

**Date:** 2026-11-04. Active checkout remains the source of truth. C11-C 2.19.12 remains the production baseline.

| Gate | State | Accepted scope / next condition |
|---|---|---|
| E0 | PASS / CLOSED | Preserve accepted evidence; do not repeat |
| E1 | PASS / CLOSED | Shared production-intent service; it only prepares sealed intents and never dispatches |
| E2 | PASS / CLOSED | Bounded CHALLENGE_001 title-to-pixels R4 control only |
| E3.2 | PASS / CLOSED | D3 V5 ↔ E1 planning binding |
| E3 audiovisual pilot | PASS bounded | Existing Producer GUI/QProcess pilot; D3.3, mux and FFprobe; negative controls V1.5 accepted |
| E3 negative controls V1.5 | PASS / CLOSED | 50/50 Windows tests; do not repeat absent source change |
| E4A.1 | PASS / CLOSED | Fixture-only / source audit increments as previously recorded |
| E4A.2 | PASS bounded | Six real C11-C BODY sample points; real-body identity proof |
| E4A.3 V1 | FAILED / CONSUMED | Godot headless prevented rendering; do not rerun |
| E4A.3 V2 | PASS bounded | Godot 4.7.1 rendering enabled; 6/6 real frames, 18/18 PNG, 12/12 comparisons; BODY identity retained |
| E4A visual layout | BLOCKED / NOT APPROVED | Existing hook and CTA overlaps; D1.5 safe area / type unknown; player_name/challenge_label blocked |
| E4A.4 audio/mux | PREPARED / NOT RUN | Apply/run the V1 overlay; D3 V5 + D3.3 + FFmpeg mux + FFprobe on immutable E4A.2 video; no D overlay in MP4 |
| E4A closure | PENDING | Requires E4A.4 Windows PASS, operator A/V listening review, and layout issue disposition |
| E4B Loop | NOT STARTED | After E4A bounded closure; preserve existing C11-C Loop music |
| E4C Drill | NOT STARTED | After E4B; preserve existing C11-C Drill music |
| E5 | NOT STARTED | Cross-family determinism, seed domains, adapter/profile isolation, GUI/CLI parity |
| E6 Smoke18 | NOT STARTED | Six audiovisual cases per family |
| E7 Matrix101 | NOT STARTED | 54+27+20 target; 99 provisional runnable; CH_008/009 held |
| E8 | NOT STARTED | Historical corpus matrix, independent acceptance, freeze and explicit promotion |

## E4A.3 evidence identity

Evidence ZIP SHA-256: `75c5b37426eea6e40a41d3daa821fc74a08f69590e569b1080cbc9305ae5db91`  
Receipt SHA-256: `3670428feae3b34766677b4cdba3985babecbda9ee781eebe4cc57c318cd9f1c`  
Report SHA-256: `ee1be803f4d0433347778793aab12228301aea5108f426011836c27dc268dc08`

## Global governance

Frozen C11-C manifest SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`; 796,318 bytes. `renderer=OFF`; D4.8 BLOCKED; D9.10 PREPARE_ONLY; D9.14/D9.16 BLOCKED; D9.17 BLOCKED_NO_GO; D10 BLOCKED_FOR_PROMOTION; `release_authority=NONE`. No E gate by itself promotes a production baseline.
