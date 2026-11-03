# C11-E Continuation Master Prompt — V36

Continue the project in the active Windows checkout `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`; that checkout is the only source of truth. Never extract an old snapshot over it. Use PowerShell 5.1. Do not repeat accepted gates absent relevant source drift.

## Accepted milestones

E0/E1, bounded E2 R4, E3.2, E3 Challenge A/V pilot and E3 negative controls 50/50 remain accepted within scope. E4A discovery, GUI contract successor, Gate A and operator-approved Policy V1 remain accepted within scope. E4A.1 is accepted only as a Godot 4.7.1 neutral-body pixel fixture: 23/23 focused tests, 18 PNGs 540×960, 12 comparisons; receipt `d90394548ae9dc5ac7b75199c96d423605e9c645dedf0616b8bdfbd1b165ea53`; report `adefba7fe65400efa30d422e0547499c60b79a400eed8e4d90cf1dc9a5d7597f`; ZIP `ecd2b141603e004d00a9d814f9ca670dbca2ea611de4b32d76dcbcd13c70c7c2`. It did not rasterize actual gameplay.

## Current E4A.2 prepared increment

Runner `tools/c11d/d9/c11e_e4a_challenge_real_body_pixel_review.py` SHA `a852e5f4238f14b30a887f579bad3e4284c420c427dc625667a0ec60190fff1a`; tests `tools/c11d/d9/test_c11e_e4a_challenge_real_body_pixel_review.py` SHA `5e967ec3b8fd87cc9effe079356912e8f6b69f8994a368dc8f1c15cfb95dcb0c`. Tests 25/25 and compilation pass. A final local synthetic FFmpeg testsrc2 simulation yielded 18 PNGs / 12 comparisons, but it is not a C11-C runtime run.

The runner prepares A/B/C using the existing E1 service and D9.9 resolver, then calls the existing C11-C challenge script once for CHALLENGE_004 / seed 314159 / REVIEW_720 / NoSound into a fresh `artifacts/tests` root. It validates a single H.264 yuv420p 720×1280 30fps 450-frame 15s MP4, with no audio and `production_manifest.json` profile REVIEW_720. Six sampled frames (0,89,90,300,390,449) yield 18 PNGs and 12 pixel comparisons. A/B BODY must be identical at all six. Only title/subtitle HEADER/HOOK and CTA FOOTER/CTA can change. Challenge-only overlay fields remain blocked. Test-only text placement is not production typography.

**Windows execution is still pending.** Install the add-only overlay and execute the runner once. Inspect its resulting evidence ZIP (MP4, production manifest, ffprobe, generator logs, intents, PNGs, body hashes, report, receipt and SHA256SUMS) before accepting E4A.2. A run failure is not a PASS; retain raw failure evidence and diagnose its actual error.

## Next work after E4A.2

E4A.3 integrate the D-owned composition result into the actual D Challenge visual consumer (no parallel binder/producer; no C11-C `hook_text`/`cta_main` aliases). E4A.4 perform test-only A/V qualification using the already accepted E3 D3 V5/FFmpeg/FFprobe route, then operator visual review and formal E4A closeout. Afterwards E4B Loop, E4C Drill, E5 determinism/seed isolation/profile leakage/GUI-CLI parity, E6 Smoke18, E7 Matrix101 (99 provisional while CH_008/009 have 11s/12s discrepancy), and E8 historic C11-C corpus reconciliation, independent acceptance, freeze and explicit promotion.

## Immutable constraints

C11-C 2.19.12 and its manifest `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953` remain immutable. Do not modify mechanics/RNG, generators, `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector`, `RenderedFrameStream`, `FrameSnapshot.custom_data`, protected presentation binders, `core/audio`, D3 V5 or E1 service. No sixth module, parallel producer or binder. Keep production D renderer OFF; D9.10 PREPARE_ONLY; D4.8 BLOCKED; D9.14/D9.16 BLOCKED; D9.17 BLOCKED_NO_GO; D10 BLOCKED_FOR_PROMOTION; `release_authority=NONE`; no freeze/promotion.
