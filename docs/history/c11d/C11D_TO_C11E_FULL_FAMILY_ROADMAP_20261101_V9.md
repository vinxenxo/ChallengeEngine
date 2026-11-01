# C11-D â†’ C11-E full-family roadmap â€” V9

**Date:** 2026-11-01. This roadmap preserves the complete delivery scope; E2 is only the first technical control.

## Product target

Deliver on-demand final MP4 production for **Challenge, Visual Loop and Visual Drill**, retaining the C11-C generators and mechanics. E adds the D presentation layer, editable/enabled editorial, and D3 Music V5 integration. CLI and GUI must call the same shared production service; no parallel producer implementations.

Every final family flow must support final editorial data, deterministic gameplay seed isolation from independent `request.music_seed`, audio generation/mix, FFmpeg mux and FFprobe verification of video and audio streams. Challenge-specific data must not leak into Loop/Drill contracts.

## Gates

1. **E0/E1:** restart baseline and shared CLI/GUI service; automated E1 acceptance retained, GUI observation pending.
2. **E2:** physical Challenge 001 A/B proof that the title reaches its own header pixel slot while gameplay body remains invariant. No audio. Current pre-render native JSON test passed 30/30; corrected Python contract is 9/9; physical attempt R1 stopped at stale test 09 before rendering. Next attempt is R2.
3. **E3:** D3 Music V5 with independent music seed, FFmpeg mux and FFprobe A/V verification. Enter only after E2 physical and human acceptance.
4. **E4A:** Challenge full presentation/editorial adapter integration.
5. **E4B:** Visual Loop presentation/editorial binder and adapter integration.
6. **E4C:** Visual Drill presentation/editorial binder and adapter integration.
7. **E5:** determinism, independent seed-domain checks and CLI/GUI parity across all families.
8. **E6:** Smoke18 (six per family).
9. **E7:** Matrix101 planned composition: 54 Challenges, 27 Loops and 20 Drills. CH_008/009 remain excluded until the declared 11-second duration vs 12-second phase-sum discrepancy is resolved by explicit authority; presently runnable scope is 99.
10. **E8:** independent acceptance, frozen package and explicit promotion decision.

## Non-negotiable boundaries

C11-C 2.19.12 and its frozen manifest remain the production authority until E8. Do not mutate C generators/mechanics or protected release sources. E2 has no audio; no gate grants release authority or promotion implicitly. No stale PASS, stale receipt variables or reused request IDs.