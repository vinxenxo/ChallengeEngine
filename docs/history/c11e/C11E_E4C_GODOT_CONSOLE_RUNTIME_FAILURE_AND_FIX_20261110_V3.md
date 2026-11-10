# E4C Godot console-runtime failure and V3 correction — 2026-11-10

## Observed evidence

Run `DRILLV2_20261110T101456Z_f7658bde` selected:

`C:\Users\vinxe\AppData\Local\Microsoft\WinGet\Packages\GodotEngine.GodotEngine.Mono_Microsoft.Winget.Source_8wekyb3d8bbwe\Godot_v4.7.1-stable_mono_win64\godot.exe`

Discovery source was `PATH:godot.exe`. `--version` returned exact `4.7.1.stable.mono.official.a13da4feb`. The first actual V2 harness process exited `3228369023` (`0xC06D007F`); stdout/stderr exposed only the engine banner, and Python correctly stopped the matrix. No harness summary, receipt or selector runtime PASS was produced.

## Diagnosis

The runner's candidate ordering treated a successful `--version` response as sufficient. It inserted PATH `godot.exe` before searching console binaries and did not inspect the PATH executable's own directory for its sibling console exe. It therefore selected an editor GUI binary rather than the console variant intended for Windows CLI/headless automation.

Windows defines `0xC06D007F` as an MSVC delay-load exception associated with a missing procedure import (`ERROR_PROC_NOT_FOUND`). The exact failing DLL/export is not inferable from the supplied logs and remains unknown without a corresponding Application Error/WER event or dump. The code is evidence of native process initialization failure, not a GDScript selector assertion.

## V3 changes

Runner V3 postimage SHA-256: `2a039de904e4b6cf97e8f4e848a86b95c6ce8fa6a60a0b4b893c5430dcf9f6da` (28374 bytes); exact V2 preimage SHA-256: `342398d6e75a458e46478df225df99f36241cdb7a65a8f33d644478c27c575e7` (17460 bytes).

- Strict console-only candidate discovery; sibling scan for `Godot_v4.7.1-stable_mono_win64_console.exe` and console aliases.
- Targeted WinGet Mono cache search, in addition to Downloads, `C:\Godot` and LocalAppData Programs.
- Exact version and isolated temporary-project headless-script smoke required before Python matrix execution.
- Failed candidate exit codes rendered as 8-digit hex; Windows Application Error / WER events saved when available.
- Reuse of the exact prior Python/static preflight evidence, only after required log files and all pass markers validate and current source pins/frozen manifest are rechecked.
- Transactional runner replacement with pinned V2 preimage, V3 postimage and add-only docs; no binder/service/C11-C changes.

## Current status

The V3 package has been prepared and statically audited. Windows PowerShell 5.1 AST/transaction and actual Godot console smoke are intentionally verified on the operator workstation by the installer/runner; they are not represented as completed in this preparation environment. E4C dynamic runtime remains pending until V3 reports the 20/20 acceptance markers.

## Boundaries

Renderer OFF; media false; D4.8 BLOCKED; release authority NONE. A.3 policy lineage, visual consumer, native A/V and GUI runtime remain independent downstream blockers. No accepted E4A/E4B or Drill authoring tests are repeated.
