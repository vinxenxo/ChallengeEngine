# C11-E Execution Backlog — V27

**Date:** 2026-11-05.

1. **E4A.5B — Source closure.** Read-only source review completed against the latest supplied snapshot. Preserve the 88-member handoff reconciliation (83 exact + 5 authorized), current snapshot pin for the adapter test, source seam, launcher, QA and A/V findings. No Godot/FFmpeg/media was run. Git metadata is unavailable in the ZIP.
2. **E4A.6 — Minimum D-only Challenge consumer.** Implement only after review of the V1 design. Add a D-owned Challenge consumer and fail-closed D envelope transport. Insert after the four existing `SocialUIBinder.bind_render_model(rm)` calls; retain exactly one whole binder apply per frame. Do not run `PresentationUI.apply_render_model` a second time. Apply only Hook/Countdown/CTA visibility after native binding. Mount `C11CVisualEditorialLayer` once and update it without remounting. Preserve timeline, phase names, native state offsets and source frame count.
3. **E4A.6 tests.** Static checks for four insertion seams / one binder per phase / one timeline advance; adapter immutability; half-open ranges; absent-envelope no-op; fail-closed invalid envelope; hook/countdown ON/OFF; title/subtitle combinations; D/native CTA ownership transitions; RevealManager/WinningHighlight one-pass; no Loop/Drill leakage. Then isolated Godot proof with stderr/exit/frame checks, only after separate test-run authorization.
4. **E4A audio/mux completion.** Connect and test D3 V5 Challenge music engine using independent `music_seed`; verify actual audio creation, FFmpeg mux and FFprobe A/V duration/codec/rate. Existing C7 PCM path is not evidence of D3. Keep renderer/production dispatch disabled.
5. **E4A final gate.** Challenge live visual, D3 audio/mux, source-time correctness, separate human visual/listening review and GUI/CLI prepare parity. No release promotion.
6. **E4B — Visual Loop.** 27 grammar identities; retain five Loop families, grammar timing, existing family/grammar music and Loop binder. Do not reuse Challenge phase ranges or D3 Challenge music.
7. **E4C — Visual Drill.** 20 variants; retain four Drill types, phase semantics, END_CTA precedence, current Drill binder and Drill music.
8. **E5:** cross-family determinism, seed-domain isolation, adapter/profile non-leakage and GUI/CLI parity.
9. **E6:** Smoke18, six complete A/V scenarios per family.
10. **E7:** Matrix101: 54 Challenge + 27 Loop + 20 Drill; CH_008/009 held pending authoritative timing reconciliation.
11. **E8:** independent acceptance, immutable freeze and explicit promotion decision.

Always-on invariants: C11-C 2.19.12 and its freeze manifest remain untouched; `request.seed` and `request.music_seed` remain separate; no automatic seed generation; no mutation of simulation truth; no `FrameSnapshot.custom_data` serialization; no renderer dispatch or media creation until separately authorized; no new GUI surface or parallel producer/renderer.
