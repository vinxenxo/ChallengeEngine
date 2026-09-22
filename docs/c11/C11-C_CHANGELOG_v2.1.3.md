# C11-C v2.1.3 — Toolchain Consolidation

- Fixed all bulk/orchestration scripts to invoke child `.ps1` scripts directly instead of `powershell.exe -File`, preventing `[int[]]` seed argument flattening and `-Seed` binding failures.
- Fixed canonical PowerShell validator so it no longer expects a nonexistent versioned launcher.
- Fixed Godot Movie Maker invocation to use `--resolution 720 1280` as separate CLI arguments.
- Kept temporary `override.cfg` capture strategy; `project.godot` remains untouched.
- Added canonical artifact/review separation documentation.
- Added a one-time retirement helper for superseded versioned tool launchers.
- No C11-B frozen engine semantics changed.
