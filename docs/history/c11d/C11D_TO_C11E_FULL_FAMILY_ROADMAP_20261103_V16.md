# C11-D to C11-E Full-Family Roadmap — V16

**Date:** 2026-11-03. Supersedes V15's E3 pre-GUI/pre-pilot status and clarifies the development CLI/GUI sequence. Does not supersede governance locks.

## Product outcome

One C11-E service and set of family adapters producing validated audiovisual outputs for Challenge, Visual Loop and Visual Drill. Preserve the C11-C visual mechanics/generators and existing family audio implementations. Add the approved D presentation/layout and family-scoped editorial values, orchestrate the correct audio route, mux with FFmpeg, validate with FFprobe/audio QA and issue immutable run receipts.

## Development workflow

Implement reusable scripts/service through CLI first where practical; then connect the same scripts to the current low-fidelity Producer GUI. Both CLI and GUI execution/testing remain required in this engineering phase. The GUI is a dispatcher, not a second business-logic implementation. The future all-generation-through-GUI target begins after D/E replaces C and a new GUI is built. CLI remains for CI/compatibility.

## E gates

- **E0:** accepted; do not repeat.
- **E1:** shared GUI/CLI intent service accepted; separate-process CLI adapter test exists.
- **E2:** bounded CH001 R4 title-to-pixels control formally closed only for its declared scope.
- **E3.2:** D3 V5 contract binding to E1 accepted.
- **E3 GUI/audio pilot:** PASS. Existing Producer GUI launched and invoked the E3 worker via QProcess. Test-only CH001 R4 pilot passed raw WAV repeatability, music-seed isolation, D3.3 mastering, FFmpeg mux, FFprobe and unchanged H.264 stream. User confirmed A and C are expected and defect-free. Receipt SHA `910d600e06dcdb2356f9f787fd0c82d45db203e35b471cd5c7cdba10d6ec5aab`.
- **E3 negative controls:** next overlay V1.5; add final mux cardinality/codec/rate/layout/non-silence/timing checks and 19 explicit tests. Full 50-test Windows suite required because pipeline source changes. E3 closes only after PASS.
- **E4A:** full Challenge presentation/layout/editorial consumer and D3 V5 audio.
- **E4B:** Loop grammar/variant timeline and editorial/layout binding; preserve existing C11-C Loop music.
- **E4C:** Drill phase/END_CTA precedence and editorial/layout binding; preserve existing C11-C Drill music.
- **E5:** cross-family determinism, gameplay/music seed isolation, adapter/profile non-leakage, CLI and GUI execution parity.
- **E6:** Smoke18 — six audiovisual scenarios per family.
- **E7:** Matrix101 — 54 Challenge + 27 Loop + 20 Drill. CH_008/009 held pending reconciliation of 11-second declared duration against 12-second phase sum (3+7+0+2); 99 provisional runnable cases.
- **E8:** independent acceptance, immutable freeze and explicit promotion.

## Complete visual test obligation

Before E8, reconcile the full historical C11-C corpus, including the known 27 review cases, 9 Challenge cases and all other visual/review categories, into a row-by-row C-to-E regression map. Each applicable Challenge, Loop and Drill case must test the D presentation/layout, editorial and correct family music layers, seed domains, visual identity, determinism, mux/FFprobe/audio QA and receipts. Smoke18 is a sample gate, not a substitute for complete family coverage.

## Hard governance

C11-C 2.19.12 remains the only production baseline. Frozen manifest: 796,318 bytes / SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`. No core/audio, protected C11-C mechanics/generators, canonical definitions, D4.8/D9.10 locks or manifest changes. No second producer, sixth suite module or `c11d-control`. `release_authority=NONE` until independent E8 and explicit governance approval.

## Immediate handoff

Apply and execute `C11E_E3_NEGATIVE_CONTROLS_OVERLAY_V1_5.zip` using its hash-gated Windows scripts. If 50/50 PASS, formally close E3 and begin E4A Challenge.
