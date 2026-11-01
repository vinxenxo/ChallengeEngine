# C11-E Gates and Acceptance Matrix — V22

**Date:** 2026-11-02
**Authority:** `C11E_CURRENT_AUTHORITY_20261102_V22.md`

| Gate | Required outcome | Current evidence | State | Next permitted action |
|---|---|---|---|---|
| E0 | Foundation/re-entry established without changing frozen C | E0 V2 receipt SHA `869a099c6d73e9b9230db954e68707e3b079db82c368dd151806f8e10a9c8315` | PASS / installed | Reuse only |
| E1 | Shared service, one path for CLI and GUI; automated contract | 2/2 automated tests PASS; prior manual GUI observation status remains as recorded in V21 | AUTOMATED PASS; MANUAL STATUS UNCHANGED | Do not build parallel adapters |
| E2-A | Numeric and Python contracts | Godot 30/30; Python 9/9 | PASS | No rerun |
| E2-B | Two physical A/B title-only renders | R4, runner exit 0, two AVIs + two MP4s | PASS | Preserve immutable artifacts |
| E2-C | Pixel invariance/difference assertions | Gameplay body 540/540 same; title slot 540/540 different; surrounding header regions same; full MP4 270/270 different | PASS | No source edits required |
| E2-D | Delivery/FFprobe metadata | Both MP4s H.264 High, 720×1280, 30 fps, 270 frames, 9 s, yuv420p, TV range, no audio | PASS | E2 audio remains disabled |
| E2-E | Independent visual inspection and operator approval | Assistant sampled 18 decoded frames plus six receipt PNGs; no obvious visual defect. Full operator playback not yet attested in receipt. | SAMPLED REVIEW PASS; OPERATOR SIGN-OFF PENDING | Operator watches both full MP4s and records decision |
| E3 | D3 Music V5 independent seed, deterministic audio selection/output, FFmpeg mux, FFprobe A/V validation | No E3 execution evidence yet | PREPARE_ONLY / BLOCKED ON E2 SIGN-OFF | Source/contract preflight only after E2 sign-off |
| E4A | Challenge family adapter | Not started | BLOCKED | After E3 |
| E4B | Visual Loop family adapter | Not started | BLOCKED | After E3 |
| E4C | Visual Drill family adapter | Not started | BLOCKED | After E3 |
| E5 | Seed isolation, determinism, GUI-CLI parity across all families | Not started | BLOCKED | After E4A/B/C |
| E6 | Smoke18: six tests per family | Not started | BLOCKED | After E5 |
| E7 | Matrix101: 54 Challenge, 27 Loop, 20 Drill | Not started; CH_008/CH_009 held | BLOCKED | After E6 and resolution of duration discrepancy |
| E8 | Independent acceptance, immutable freeze and formal promotion | No decision record | BLOCKED | Only after all gates and independent review |

## E2 R4 acceptance record

- RequestId: `C11E-E2-CH001-AB-20261101-V9-R4`
- R4 receipt SHA-256: `2f8c355453d8558c6af42aa5da35f603b767726d64ba04f842dc799a2cadef7f`
- Evidence ZIP SHA-256: `f33431bb131697baf9dc3df6ed1ed8e4ca14ecb40d7b9ef07c812a5bca67a3de`
- R4 checkout HEAD: `7fbdf8529d2af6ba7089eacd8fd9b38682466d84` (branch `main`)
- Runner pin: `158325324626085ebf319f68906ca8778f9a08eb39c6e8441da146c12ee4f953`
- Python contract pin: `ab4ed3fd421ef0cac86d4ef25167f0161a186ef5bd90373414abed7bea17d2a9`
- Governance from receipt: `release_authority=NONE`, `baseline_promotion=false`, `d_governance_mutated=false`, `human_visual_review=PENDING`.

**Gate decision:** E2 automated execution and technical assertions PASS. The overall formal E2 gate is not declared closed until the operator's full playback review is positively recorded. E3 remains prepare-only.
