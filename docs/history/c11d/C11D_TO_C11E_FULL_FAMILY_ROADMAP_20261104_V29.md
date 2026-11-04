# C11-D → C11-E full-family roadmap — V29

**Date:** 2026-11-04. This is the current engineering sequence; the product target remains the same.

## Product outcome

One coherent on-demand audiovisual service for Challenge, Visual Loop and Visual Drill. Keep all C11-C gameplay generators/mechanics and existing family audio behavior intact. Add D-owned layout/presentation, approved family-scoped editorial, independent gameplay/music seeds, correct family music, FFmpeg mux, FFprobe/audio QA and GUI/CLI parity through the existing shared E1 service and five suite modules. The GUI is the primary operation surface; CLI supports CI/compatibility and invokes the same business path.

## Accepted gates and present position

E0/E1, bounded E2 R4, E3.2, Challenge D3 V5/audio mux pilot and E3 negative controls 50/50 are accepted within scope. E4A discovery, GUI contract, Gate A and Policy V1 are accepted within their scope. E4A.1 fixture-only is accepted. E4A.2 is accepted for six-sample real-gameplay BODY identity/region confinement only.

E4A.3 V1 has 46/46 Python tests but runtime was stalled by using Godot `--headless` while waiting for RenderingServer rendering. This is a harness failure, no Godot PASS. V2 corrects the process to run with rendering enabled, adds a 90s timeout/heartbeat/progress logs and has 50/50 preparation tests. Next action is the single V2 Windows run against the accepted E4A.2 MP4, not a new C11-C capture.

## Ordered gates

1. E4A.3 V2: six-frame D-owned Godot SubViewport alpha-composition over real Challenge video. Must prove Godot actual render, pixel comparisons and unchanged body/source evidence.
2. E4A.4: test-only A/V exercise with accepted E3 D3 V5/music seed path, FFmpeg mux and FFprobe; inspect full result and perform operator visual review.
3. E4A layout: reconcile current/root README instructions, D1.1/D1.5/D1.7 and historical C11-B/C presentation contracts. Do not infer generic Challenge safe area or text typography from region topology or unrelated family styles. Approve placement only on authoritative evidence; otherwise keep affected fields blocked.
4. Close E4A only after actual D consumer proof, accepted layout/explicit blocked field disposition and test-only A/V review.
5. E4B: Loop family grammar/timeline/editorial/layout integration; preserve C11-C Loop mechanics and music.
6. E4C: Drill family/type/tier/phase/END_CTA/editorial/layout integration; preserve C11-C Drill mechanics and music.
7. E5: deterministic reruns, independent gameplay/music seed domains, family/profile leakage controls, GUI/CLI parity.
8. E6 Smoke18: six full audiovisual cases per family.
9. E7 Matrix101: 54 Challenges + 27 Loop grammars + 20 Drill variants. CH_008/009 remain held for declared 11s vs 12s phase-sum discrepancy; 99 provisional runnable.
10. E8: row-by-row historical C11-C corpus reconciliation, independent acceptance, immutable freeze and separate explicit promotion.

## Frozen governance

C11-C 2.19.12 remains sole production authority; manifest SHA `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`. No changes to C generators, mechanics, RNG, simulation truth, `FrameSnapshot.custom_data`, `core/audio`, D3 V5, E1 service or manifest. No second producer/binder, sixth module or `c11d-control`. Production D renderer OFF; D9.10 PREPARE_ONLY; D4.8 BLOCKED; D9.14/D9.16 blocked; D9.17 NO-GO; D10 blocked; release authority NONE.
