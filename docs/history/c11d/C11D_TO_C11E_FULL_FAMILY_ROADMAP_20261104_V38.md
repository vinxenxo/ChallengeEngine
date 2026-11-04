# C11-D to C11-E full-family roadmap — V38

**Date:** 2026-11-04. The destination remains one shared D+E service for Challenge, Visual Loop and Visual Drill, preserving each family's binder, timeline and music ownership.

## Ordered milestones

1. **E0/E1:** shared intent foundation; Challenge-only request `show_hook_countdown` remains accepted.
2. **E2/E3:** D3 Music V5 Challenge path, independent `music_seed`, mux/FFprobe; prior A/V work remains test-only accepted evidence.
3. **E4A Challenge:** shared-layer D consumer applied; the first real-frame pass showed baked-hook overlap. V1 recomposition then failed to parse on Godot 4.7.1 because it called `PackedStringArray.join`. V2 fixes the API direction to `String.join(PackedStringArray)` and adds a static regression assertion. The Godot pixel rerun and operator review remain open. No production dispatch path is inferred.
4. **E4B Loop:** adapt approved common presentation into the existing Loop binder; preserve C11-C Loop music and timeline.
5. **E4C Drill:** adapt approved common presentation into the existing Drill binder; preserve C11-C Drill music and timeline.
6. **E5:** converge GUI/CLI through one service; enforce deterministic repeats and independent gameplay/music seed domains.
7. **E6 Smoke18:** six audiovisual scenarios per family.
8. **E7 Matrix101:** 54 Challenges + 27 Loop grammars + 20 Drill variants. CH_008/009 remain held while the 11s declared duration conflicts with 12s phase sum.
9. **E8:** independent acceptance, immutable freeze and explicit promotion; only then may C11-E replace C11-C.

## Architecture and authority

Canonical request/catalog/profile → optional effective editorial and family options → unchanged C family generator/mechanics/timeline → family-specific D consumer → family-owned music → mux/QC. GUI and CLI converge on one E1 service. No parallel renderer or sixth GUI surface.

C11-C 2.19.12 remains sole production authority; frozen manifest `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`. Production renderer/dispatch/media OFF; D4.8 blocked; D9.10 PREPARE_ONLY; D9.17 NO-GO; D10 blocked; `release_authority=NONE`.
