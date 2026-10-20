# C11-D V2-C — Godot Mono Version Guard Correction (2026-10-17)

## Cause

The first runtime process correctly resolved the Godot 4.7.1 Mono executable. The Python runner's `--version` probe returned `4.7.1.stable.mono.official.a13da4feb`, but `Engine.get_version_info().string` returned `4.7.1-stable (official)`, which does not encode the `.mono` build suffix. V2-C's GDScript harness incorrectly demanded `mono` in that engine display string and blocked `CHALLENGE_001` before entering `ChallengeRuntimeBridge.run_effective_pipeline`.

The initial report hash marker was in fact correct. The earlier PowerShell regex check was too strict for CRLF output lines; use `ReadAllLines()` plus exact prefix matching or `TrimEnd()` when validating a hash marker.

## Guarded correction

- The parent Python runner continues to require Godot 4.7.1 and `mono` in the exact executable's external `--version` output.
- The runner passes that already-verified version string to each isolated Godot process.
- The GDScript harness validates the engine's numeric major/minor/patch fields as 4.7.1 and records the launcher version separately from `Engine.get_version_info()`.
- The receipt's `runtime.godot_version` retains the externally verified Mono launcher identity, while `runtime.engine_version_info` preserves the actual engine dictionary.
- A Python static regression test asserts the split; contract tests are now 27.

## Scope / governance

This is a guarded replacement of the V2-C harness, runner and Python test file. The overlay manifest records exact before-SHA256 preconditions and after-SHA256 pins. The application block must save and verify backups before replacement. The canonical V1 CHALLENGE_004 harnesses are not touched. No simulation, seed, custom_data, payload, media, renderer, temporal policy or release authority behavior is changed.

Runtime acceptance is still NOT established. Run the updated 27 Python tests and then a focused CHALLENGE_001 single-process smoke receipt. Only after the smoke passes should the full V2-C runner proceed. A smoke receipt proves only that one source-frame harness process reaches receipt validation; it does not close V2-C's nine-selector, eighteen-process gate.
