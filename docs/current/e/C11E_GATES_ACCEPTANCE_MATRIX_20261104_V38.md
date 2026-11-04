# C11-E Gates Acceptance Matrix — V38

| Gate | Status | Evidence / next action |
|---|---|---|
| E0/E1 | PASS retained | Shared service; do not repeat without source drift |
| E2 | PASS bounded | CHALLENGE_001 R4 title-to-pixels only |
| E3/E3.2 | PASS test-only | Accepted D3 V5 / mux pilot and 50/50 negative controls |
| E4A discovery + GUI contract | PASS within scope | Source audit and GUI contract successor retained |
| E4A Gate A | CLOSED_WITH_BLOCKERS | Editorial sidecar 14/14; I/O 0/10 complete, 6 partial, 4 blocked |
| E4A policy V1 | APPROVED | Operator-approved exact semantic field-to-region/phase mapping |
| E4A.1 | PASS — FIXTURE ONLY | Neutral body; does not test gameplay pixel identity |
| E4A.2 | PASS — REAL BODY, SIX SAMPLES | Windows Godot source video reused; 33/33 tests; 18 PNG; 12 comparisons; BODY identity across A/B/C; report/receipt hashes recorded in V38 |
| E4A.2 visual layout | NOT ACCEPTED | Placeholder text overlaps C11-C HOOK; D1.5 safe area and generic typography unknown |
| E4A.3 preparation | 46/46 PYTHON PASS | D-owned Godot SubViewport real-background test branch prepared; exact pins; Windows Godot execution pending |
| E4A.3 Windows runtime | OPEN | Apply V1 overlay; reuse E4A.2 normalized MP4; expect 18 Godot PNGs / 12 comparisons; inspect complete evidence ZIP |
| E4A.3 production consumer | NOT ACCEPTED | Test-only materializer branch is not yet production Producer/renderer integration or full-duration composition |
| E4A.4 | PENDING | Test-only A/V using accepted E3 D3 V5/mux/FFprobe; operator visual review; do not bypass layout disposition |
| E4A closure | OPEN | Requires actual D consumer/layout decision, A/V evidence and operator review |
| E4B Loop | BLOCKED_BY_SEQUENCE | Start after E4A close; preserve C11-C Loop music and family contract |
| E4C Drill | BLOCKED_BY_SEQUENCE | Start after E4B; preserve phase/END_CTA and family music |
| E5 | OPEN | Determinism, separate seed domains, adapter/profile isolation, GUI/CLI parity |
| E6 Smoke18 | OPEN | Six actual audiovisual cases per family |
| E7 Matrix101 | OPEN / 99 PROVISIONAL | CH_008/009 held: 11s declared vs 12s phase sum |
| E8 | BLOCKED | Historical C11-C corpus, independent acceptance, freeze and separate explicit promotion |

## E4A.2 accepted evidence

`RUN_20261104_002559_542bcf60.zip`; 7,751,764 bytes; SHA-256 `49736fb268af00bb92868a29b819ad54cc6a4dc011000cae20505ee56e496893`; valid CRC; 85 entries. C11-C base MP4 `fdd0598e20ddc6201e54cc2dad7fd3362c2ef80961df44f3ef4676fb97a765de` (`yuvj420p/pc`, 60fps/900, 720×1280, 15s). Test-only normalized derivative `edbd446d67142d20e138e55563f16cbae8d9a4c39469fd2bebcb3c9d5723fb9e` (`yuv420p/tv`, 30fps/450, 720×1280, 15s). Report `e940f0a150d7dcea8ab34003b2f053d4be614f602ee6ea3ff04cd8bfa2b71159`; receipt `b23a5f0c1557b52b724c99ac90a671e0a8d8457dcd5e605f8d097c517f366308`.

## E4A.3 exact preparation pins

- Materializer: `e925cc319852e9fe79c26f9dd791ff1f43a0d3465ae30159819be5f57fb001e1`.
- Runner: `9d00faf38213ade848f722a72bf0ba6ef102975f43bd9e960648780bf3d2c629`.
- Tests: `b33a158ddd29f1581f86a7d6ceabef4a66a1a5a8a51aaada9b8489c730876973`.
- 46/46 preparation tests; `py_compile` PASS. No Godot runtime PASS is claimed until the Windows output and receipt are reviewed.

## Governance

C11-C 2.19.12 remains sole production baseline; frozen manifest SHA `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953` (796,318 bytes). Production D renderer OFF; D9.10 PREPARE_ONLY; D4.8 BLOCKED; D9.14/D9.16 BLOCKED; D9.17 BLOCKED_NO_GO; D10 BLOCKED_FOR_PROMOTION; `release_authority=NONE`; no freeze/promotion.
