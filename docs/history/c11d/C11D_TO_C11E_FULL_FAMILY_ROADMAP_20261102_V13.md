# C11-D to C11-E Full-Family Production Roadmap — V13

**Date:** 2026-11-02
**Authority:** E2 R4 formal closure decision V1; C11-C 2.19.12 remains production authority until E8.

## Product definition

Deliver all three production families—Challenge, Visual Loop and Visual Drill—preserving existing C11-C generators and mechanics. Add the D presentation layer, enabled editorial fields, and D3 Music V5. CLI and GUI must use one shared production service. Final MP4s carry editorial content and an independently seeded soundtrack assembled with FFmpeg and validated by FFprobe. CHALLENGE_001 A/B is an integration control, not the product boundary.

## Gate sequence

| Gate | Scope | Exit evidence |
|---|---|---|
| E0 | Foundation and immutable baseline | Accepted V2 receipt; do not rerun |
| E1 | Shared CLI/GUI production service | Existing automated 2/2 PASS; preserve manual GUI observation as its own status |
| E2 | Title-to-pixels A/B control | R4 automation, hashes, FFprobe, 540-frame full decoded visual audit and user-directed formal closure V1: ACCEPTED |
| E3 | D3 Music V5 | Source-contract discovery, independent seed, deterministic soundtrack, music/gameplay isolation, FFmpeg mux, FFprobe A/V and negative cases |
| E4A | Challenge adapter | Challenge-specific presentation/editorial binder through shared service |
| E4B | Visual Loop adapter | Loop-specific projection and editorial mapping |
| E4C | Visual Drill adapter | Drill-specific projection and editorial mapping |
| E5 | Cross-family determinism and parity | Gameplay/music seed isolation, repeatability, GUI/CLI parity across all families |
| E6 | Smoke18 | Six representative audiovisual cases per family |
| E7 | Matrix101 | 54 Challenge + 27 Visual Loop + 20 Visual Drill |
| E8 | Independent acceptance/freeze/promotion | Separate acceptance records, source pins, package/tree hashes and formal promotion authority |

## Current position

- E2: formally closed by a separate add-only decision based on R4 automation, read-only reconciliation and the user-directed 540-frame visual audit. Original R4 receipt is immutable; its `human_visual_review` field stays `PENDING` as captured at physical-run time.
- E3: open for read-only D3 Music V5 source discovery/preflight. No audio renderer or mux has been invoked.
- E4A/B/C, E5, E6, E7, E8 remain blocked behind E3 and subsequent evidence.

## Matrix qualification

CH_008 and CH_009 remain held because each declares 11 seconds while its phase sum is 12 seconds (`3+7+0+2`). The currently valid runnable set remains 99 (54+27+18), not 101. Do not modify either source definition without explicit authority.

## Permanent governance

- C11-C 2.19.12 frozen manifest is 796,318 bytes, SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`; immutable.
- `release_authority=NONE`, `baseline_promotion=false`, `freeze_eligible=false` until E8.
- No protected C11-C mechanics/generators edits; no `c11d-control` path.
- One shared service for CLI and GUI; no parallel producer path.
- `request.seed` and `request.music_seed` are independent domains; no automatic seed generation or cross-domain RNG consumption.
- Each physical E3 attempt gets a fresh RequestId; preserve receipts, failed evidence and exact hashes.
- Do not invent music asset formats, codec, sample rate, bit rate, fades, duration policy or sync tolerance before reading D3 Music V5.
