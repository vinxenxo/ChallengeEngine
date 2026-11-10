# C11-E E4C Visual Drill Execution Plan — V4 (2026-11-10)

## Current verified state

The V1.1 integration overlay and V2 discovery hotfix both installed successfully. The Windows attempt `DRILLV2_20261110T101456Z_f7658bde` passed Python 3.13, py_compile, E1 32/32, Drill V2 source-chain 7/7, V1 dynamic binding 12/12, request-scoped 51/51 negatives, editorial review 28/28 negatives, frozen manifest and seven source pins. These are completed and reusable only while the exact original logs and current source pins validate.

The real-Godot matrix did **not** pass. Discovery chose `PATH:godot.exe` in the WinGet Mono directory after checking its version but before finding the dedicated Windows console executable. The first live Godot process exited `3228369023` / `0xC06D007F`, emitted only the engine banner and returned no summary. No matrix receipt was produced. This is a process startup/native delay-load failure, not a selector assertion failure.

## V3 required behavior

- Accept only Windows console executables; reject generic GUI/editor binaries even when their version check succeeds.
- For a configured or PATH `godot.exe`, inspect the same directory for `Godot_v4.7.1-stable_mono_win64_console.exe` and console aliases.
- Search Downloads, `C:\Godot`, `%LOCALAPPDATA%\Programs\Godot`, and `%LOCALAPPDATA%\Microsoft\WinGet\Packages\GodotEngine.GodotEngine.Mono_*`.
- Require exact `4.7.1.stable.mono.official.a13da4feb` and a separate temporary-project `--headless --script` smoke with an explicit success marker.
- Record the 32-bit exit code in hex; on failure save Application Error/WER event records when available.
- Reuse the previous static preflight logs only after verifying every log, all pass markers, current source pins and the frozen manifest. If reuse validation fails, run the normal ordered suites rather than skipping them.

## Next action

Run the package's V3 one-shot entrypoint. It replaces the V2 runner transactionally and runs the acceptance runner only if installation succeeds. The prior evidence directory is `artifacts/tests/c11e/e4c_drill_binder_v2_acceptance/DRILLV2_20261110T101456Z_f7658bde`.

Require:
- `GODOT_DISCOVERY_SOURCE` identifies a console binary (not the GUI `PATH:godot.exe`).
- `GODOT_HEADLESS_SCRIPT_SMOKE=PASS`.
- static preflight reuse receipt `PASS_SOURCE_PINS_REVALIDATED` (or a complete new preflight if the logs are not reusable).
- 20/20 selector receipts; two independent Godot runs per selector; 20/20 request manifests; 20/20 lineage closure; 67/67 pins.

## Selector and family invariants

Four families × five tiers: tracking, pursuit, saccade, peripheral_scan; tiers 1–5. Reuse D9 Dynamic Request Payload Binding V2. Preserve PRE_ROLL 3s, GAME canonical frame count, END_CTA 3s, DONE; native END_CTA owns the CTA/header. Preserve native `FAMILY_MUSIC_V4` mapping and independent gameplay/music seeds.

## Explicit downstream gates

A.3 stale manifest lineage remains BLOCKED pending a new hash-bound approval. The visual consumer, Drill-native A/V, Qt GUI runtime observation and operator A/V review remain separate gates. A dynamic-binding PASS does not close E4C overall or authorize renderer/media.

Frozen C11-C manifest remains 796,318 bytes / `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`. Renderer OFF; D4.8 BLOCKED; D9.10 PREPARE_ONLY; D9.14/D9.16 BLOCKED; D9.17 NO-GO; D10 BLOCKED; release NONE.
