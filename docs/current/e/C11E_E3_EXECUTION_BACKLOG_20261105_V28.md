# C11-E Execution Backlog — V28

**Date:** 2026-11-05.

1. **E4A.5B — Challenge source closure.** PASS read-only review of the latest supplied snapshot. Preserve the 88-member handoff reconciliation (83 exact + 5 authorized), V4 stale-pin disposition, four phase seams, root/scene/resources, launcher, QA and A/V findings.
2. **E4A.6 — D-only live Challenge consumer.** Implementation prepared: optional `--c11e-editorial-envelope=<path>`; lazy-loaded consumer; four post-native-bind call sites; one full native binder apply per frame; exactly one native timeline advance; one shared layer mount; targeted Hook/Countdown/CTA visibility only. Do not call the full binder or `PresentationUI.apply_render_model` again.
3. **E4A.6 — Windows runtime acceptance.** Run flat PS5.1 runner against the reviewed snapshot with Godot 4.7.1. Require py_compile, 16 focused Python tests, Godot clean stderr/exit 0 and summary `900 frames / one mount / 180 header / 120 footer / zero native CTA owner frames`. Record source pre/post SHA and stdout/stderr receipts. Repair only proven D-only defects.
4. **E4A.6 — Negative/variant coverage.** After initial live-root proof, add isolated cases for absent envelope no-op, corrupt/missing SHA sidecar, wrong Challenge identity, FPS/frame mismatch, altered phase ranges, Hook/Countdown OFF, empty title/subtitle/CTA, CTA owner transitions, and proof that RevealManager/WinningHighlight remain single-pass.
5. **E4A final — D3 V5.** Connect and test the actual Challenge music engine using independent `music_seed`; verify audio creation, FFmpeg mux and FFprobe A/V duration/codec/rate. Existing C7 PCM is not D3 evidence. Production dispatch remains off.
6. **E4A final gate.** Challenge live visual, D3 A/V, source-time correctness, human visual/listening review and GUI/CLI prepare parity. No release promotion.
7. **E4B Loop.** 27 grammar identities; preserve five Loop families, timing, family/grammar music and Loop binder. Do not reuse Challenge phase ranges or D3 Challenge music.
8. **E4C Drill.** 20 variants; preserve four Drill types, phase semantics, END_CTA precedence, Drill binder and Drill music.
9. **E5.** Cross-family determinism, gameplay/music seed isolation, profile non-leakage and GUI/CLI parity.
10. **E6.** Smoke18: six complete A/V cases per family.
11. **E7.** Matrix101: 54 Challenge + 27 Loop + 20 Drill; CH_008/009 held pending authoritative timing reconciliation.
12. **E8.** Independent acceptance, immutable freeze and explicit promotion.

**Always-on invariants:** C11-C 2.19.12 and its freeze manifest untouched; no mutation of simulation truth or protected C APIs; `request.seed` / `request.music_seed` independent; no automatic seeds; no `FrameSnapshot.custom_data` serialization; no renderer dispatch/media creation before explicit authority; no sixth GUI surface or parallel producer/renderer.
