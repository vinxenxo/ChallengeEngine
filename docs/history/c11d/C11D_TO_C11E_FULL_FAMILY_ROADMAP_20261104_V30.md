# C11-D to C11-E Full-Family Roadmap — V30

**Date:** 2026-11-04. Supersedes the preceding roadmap as an execution-status update only; it does not override authority or governance locks.

## Product outcome

One C11-E shared service and family adapters that produce validated audiovisual output for Challenge, Visual Loop and Visual Drill. Preserve C11-C mechanics/generators and existing family audio routes. Add D-owned presentation, enabled family-scoped editorial, independent gameplay/music seeds, D3 V5 Challenge audio, FFmpeg mux, FFprobe/audio QA and immutable receipts. GUI and CLI use the same shared E1 service; GUI remains the existing operator surface.

## Ordered gates and current checkpoint

- E0, E1, E2, E3.2 and E3 negative-control gate: accepted; reuse.
- E4A.2: accepted bounded real C11-C BODY pixel reference for CHALLENGE_004.
- E4A.3 V2: accepted bounded D-owned Godot SubViewport compositor over real C11-C sample frames. 6/6 real frames, 18/18 PNGs, 12/12 pixel comparisons; body identity preserved; Godot ran with rendering enabled and exited 0. This is not a full MP4 or production layout acceptance.
- E4A layout: blocked/not approved. The test title/subtitle overlapped existing hook headline; CTA overlapped existing footer CTA. D1.5 safe-area/typography/CTA geometry remain unknown. `player_name` and `challenge_label` remain blocked; language metadata-only.
- E4A.4 next: D3 V5 audio, D3.3 mastering, FFmpeg stream-copy mux and FFprobe on the immutable E4A.2 normalized CHALLENGE_004 15-second test video. A/B music seed 840001, C changed seed 840002; gameplay seed 314159 is constant. This is not a D overlay composite; operator playback/listening review remains required.
- E4A closure after both bounded A/V and separate layout disposition. Do not infer layout approval from audio/mux success.
- E4B Visual Loop: prove grammar/variant timeline and editorial/layout binding; preserve existing C11-C Loop music.
- E4C Visual Drill: prove phase/END_CTA precedence and editorial/layout binding; preserve existing C11-C Drill music.
- E5: determinism, independent seed domains, no profile/adapter leakage and GUI/CLI parity.
- E6: Smoke18, six audiovisual scenarios per family.
- E7: Matrix101 target = 54 Challenge + 27 Loop + 20 Drill. CH_008/009 held due declared 11s vs phase sum 12s; 99 cases provisional until authoritative reconciliation.
- E8: map the entire historical C11-C corpus row by row, including the 27 review cases, 9 Challenge cases and all applicable visual/review categories; independent acceptance, immutable freeze and explicit promotion.

## Critical visual interpretation

D1.1 is mapping evidence only. D1.5 logical canvas is 540x960 with Header 0..144, Body 144..816 and Footer 816..960; generic safe-area insets, typography, CTA geometry and asset fit/crop are not specified. D1.7 inherits the canonical layout and forbids converting UNKNOWN into invented values. The next layout work must inspect live `AGENTS.md`, `.continue/rules/CONTINUE.md` and historical C11-B/C contracts before proposing changes.

## Governance

C11-C 2.19.12 remains the sole production baseline. Manifest 796,318 bytes / SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`. No protected C generator/mechanic, core/audio, D3 V5 engine, E1 service, frozen manifest, D4.8/D9.10 locks or release authority changes. No E4 gate grants production renderer, dispatch, freeze or promotion. `release_authority=NONE` until E8 and explicit approval.
