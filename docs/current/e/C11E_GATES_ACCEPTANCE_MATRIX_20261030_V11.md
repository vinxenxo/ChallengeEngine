# C11-E — gates and acceptance (V11)

| Gate | Functional deliverable | Acceptance evidence | State at restart |
|---|---|---|---|
| E0 | Reconcile active checkout, immutable C manifest, E1/E2 receipts, live source pins, tools and incidents; archive pre-E instructions before updating authority | Readable E0 receipt, hash-verified archives, source/toolchain inventory, no render | Re-entry package prepared; Windows application pending |
| E1 | One service for GUI and CLI, preserving request/editorial/seed/provenance parity | Existing Windows Producer tests 2/2 PASS; manual GUI runtime still pending | Automated PASS; partial gate |
| E2 | Challenge `title` visibly affects its own presentation slot without changing gameplay | Two physical MP4s; frame-level body identity; title-slot differences; receipt and human review | V4 install PASS; render not started; V5 executable resolver pending Windows execution |
| E3 | Challenge D3 music generation and final mux | WAV generated from `music_seed`, muxed MP4, FFprobe A/V stream checks; music-seed A/B leaves gameplay frames unchanged | Not started |
| E4A | One complete Challenge output | Real C Challenge generator/binder + allowed editorial fields + selected C presentation + D3 music + mux | Not started |
| E4B | One complete Visual Loop output | Real Loop generator/binder/grammar + allowed editorial fields + C presentation + D3 music + mux | Not started |
| E4C | One complete Visual Drill output | Real Drill generator/binder/type/tier + allowed editorial fields + C presentation + D3 music + mux | Not started |
| E5 | Determinism/replay, independent seed domains, editorial pixel isolation, 3-family regression and GUI/CLI parity | Repeat/hash/frame/stream comparisons and source-bound receipts | Not started |
| E6 | Smoke 18: six per family | 18 physical, reviewed A/V outputs and receipts | Not started |
| E7 | Matrix 101: 54 Challenges + 27 Loop grammars + 20 Drill variants | Full 101-case results; each family A/V/provenance gates retained | Not started; CH_008/009 timing issue remains |
| E8 | Independent formal acceptance, baseline freeze/promotion decision | Separate reviewer/operator decision package and immutable source/media evidence | Not started |

## Family acceptance contract

Each E4 family must execute the actual family-specific C generator and binder, with original mechanics and profile; resolve enabled D9.8 fields into the correct distinct visual slots; render physical source media; generate a D3 soundtrack from the independent `request.music_seed`; mux with FFmpeg; and verify final MP4 with FFprobe. Receipts bind canonical request, family/variant identity, profile, source pins, gameplay and music seeds, editorial values/hashes, WAV, mux command, final media hashes and review outcome. Sidecar-only or plan-only does not count.

## Current enabled editorial fields

Common to Challenge/Loop/Drill: `title`, `subtitle`, `call_to_action`, `language`. Challenge-only: `player_name`, `challenge_label`. Reserved fields remain disabled. `title` must not be routed to C hook or CTA. The exact visual region is family-specific and must be grounded in that family's binder/model.

## Limits and authority

CHALLENGE_008/009 remain held until the 11-second declared duration vs 12-second phase sum is resolved. Runnable present family matrix is 52 Challenge + 27 Loop + 20 Drill = 99, while E7 remains Matrix101 and cannot be marked complete by omission. Longform disabled. E2/E3/E4 PASS never changes D9.10 `PREPARE_ONLY`, D4.8, D9.14/D9.16/D9.17/D10, C11-C baseline authority or release authorization.
