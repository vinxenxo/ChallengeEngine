# C11-E E4A.6 Live Challenge Consumer — Runtime Diagnostic V2

**Date:** 2026-11-05. Status: `BLOCKED_RUNTIME_IMPORT_NOT_COMPLETED`; this record supersedes no accepted C11-C or E4A evidence.

## User-run V1 evidence

Evidence archive: `C11E_E4A6_LIVE_CONSUMER_20261105_132212.zip`, SHA-256 `be5362e677f234c541d780a43f138a1e4e1e97a60c4d5a18541ec24cdbdbe596`. ZIP CRC passed; 17 entries. `py_compile` passed, all 16 focused Python tests passed, E1 envelope preparation passed, and Godot version was 4.7.1.

The run did **not** produce a live-root summary or V1 apply receipt. The user interrupted with Ctrl+C. Godot stderr contains GDScript parse errors for unresolved global class names/types (`VideoTimeline`, `FrameSnapshot`, `SimulationResult`, `ChallengeRuntimeContext`, `PresentationProfile`, `CoordinateMapper`, etc.); stdout contains only the engine version. Therefore no GDScript runtime pass, no 900-frame completion, and no E4A.6 closure can be claimed.

## Root cause hypothesis supported by source evidence

The source snapshot ZIP has no `.godot/` entries. Godot global script class names are cached in the generated project cache. V1 launched `--headless --path <project> --scene Main.tscn` directly, without first running the editor import/class-scan pass. The unresolved global classes are consistent with a missing generated global script class cache. V2 adds an explicit `--headless --editor --path <original-checkout> --import` pass and verifies `.godot/global_script_class_cache.cfg` before starting the scene. This is a diagnostic correction, not proof that no further GDScript defects exist.

## Working-tree correction

V1's default `ProjectRoot` was `Projects\ChallengeEngineV01_STATELESS_C11E_E4A5B_REVIEWED_20261105`, not the active `Projects\ChallengeEngineV01_STATELESS` checkout. The user invoked V1 without `-ProjectRoot`, so the V1 source transaction ran against the reviewed side directory. Treat that directory as a disposable diagnostic copy; do not copy its files back or use it as authority. V2 defaults explicitly to the original active checkout and records Git HEAD/status. All future source changes and add-only documentation are applied directly there.

## V2 execution contract

- Verify exact source pins before any mutation; drift blocks without repair or exclusion.
- Apply one exact `GeneradorMaestro.gd` preimage/postimage transaction and add-only D consumer, E1 envelope builder, tests and versioned records.
- Run `py_compile`, 16 focused tests and real E1 envelope preparation.
- Run Godot 4.7.1 editor import/class scan first; require exit 0, empty stderr and a generated global class cache.
- Run the Challenge root with the sealed envelope, with a bounded timeout; require exit 0, empty stderr, startup marker and `C11E_E4A6_LIVE_CONSUMER_SUMMARY` matching 900 frames / one mount / 180 header / 120 footer / zero native CTA ownership.
- Write progress markers and a PASS/BLOCKED receipt; no Movie Maker, FFmpeg, audio, media, production dispatch, staging or commit.

## Governance

C11-C 2.19.12 remains immutable. Renderer/dispatch/media remain OFF; D4.8 BLOCKED; D9.10 PREPARE_ONLY; release authority NONE. E4A.6 remains open until the V2 runtime receipt is independently reviewed. D3 V5 actual music generation/mux/FFprobe and visual review remain separate gates. E4B/E4C remain held.
