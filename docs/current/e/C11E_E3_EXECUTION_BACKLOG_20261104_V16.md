# C11-E Execution Backlog — V16

**Date:** 2026-11-04. Supersedes V15's V1 E4A.3 runtime-pending instructions after the real launch-mode hang was diagnosed.

## Current execution position

- E0/E1, E2 R4, E3.2, E3 audio/mux pilot and 50/50 negative controls: accepted within recorded bounds; do not repeat.
- E4A source/GUI/Gate A and Policy V1: accepted within scope.
- E4A.1: fixture-only pixel test accepted.
- E4A.2: bounded real-gameplay BODY pixel proof accepted, six delivery samples, 33/33 focused tests, 18 images, 12 comparisons.
- E4A.3 V1: 46/46 Python tests passed; Godot then hung because the runner used `--headless` while the GDScript awaited `RenderingServer.frame_post_draw`. No Godot PASS/receipt exists. Preserve partial evidence and do not rerun V1.
- E4A.3 V2: prepared with no-headless renderer-enabled Godot launch, 90-second timeout, heartbeat, persistent logs and per-viewport progress markers. 50/50 focused tests and `py_compile` pass in preparation. Windows runtime still open.

## Immediate task — execute E4A.3 V2

1. Stop the old V1 foreground run with Ctrl+C if still active.
2. Apply the V2 overlay in one PowerShell 5.1 transaction; verify ZIP/sidecar, all payload hashes, exact source preimages and C11-C manifest before any write.
3. Run 50 focused Python tests.
4. Run the compositor against the existing accepted E4A.2 RUN directory. Godot must launch **without `--headless`** because it must render SubViewport textures. The runner reports a heartbeat every 5 seconds and stops the child after 90 seconds.
5. Review exact stdout/stderr, exit code, Godot stage markers, six extracted base frame hashes, 18 Godot PNG hashes, 12 comparisons, report, receipt, FFprobe and SHA256SUMS. A timeout or nonzero exit is FAIL; preserve logs, no manual PASS.

## After E4A.3

- E4A.4: test-only audiovisual integration with accepted E3 D3 V5, independent music seed, FFmpeg mux, FFprobe and operator visual review.
- E4A layout disposition and closure: only after historical/root README reconciliation and explicit resolution of D1.5 safe area/typography. Keep `player_name`/`challenge_label` blocked absent approved geometry.
- E4B Loop → E4C Drill → E5 cross-family determinism/seed isolation/profile non-leakage/GUI-CLI parity → E6 Smoke18 → E7 Matrix101 (99 runnable while CH_008/009 timing blocked) → E8 historic C11-C corpus, independent acceptance, freeze, explicit promotion.

## Product invariants

One coherent Challenge + Visual Loop + Visual Drill audiovisual service. Retain C11-C generators/mechanics and current family audio. Use the existing E1 shared service and five suite modules; no parallel producer/binder or sixth module. GUI is the operation path; CLI supports CI/parity. Keep gameplay `seed` and `music_seed` independent.

C11-C frozen manifest SHA `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953` is unchanged. C11-C code/mechanics/RNG, `FrameSnapshot.custom_data`, `core/audio`, D3 V5 and E1 service remain protected. Production renderer OFF; D9.10 PREPARE_ONLY; D4.8 BLOCKED; D9.14/D9.16 blocked; D9.17 NO-GO; D10 blocked; release authority NONE.
