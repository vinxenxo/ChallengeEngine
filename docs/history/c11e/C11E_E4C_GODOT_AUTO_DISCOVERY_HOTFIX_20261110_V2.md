# E4C Godot auto-discovery hotfix — V2 (2026-11-10)

## Root cause and V1 package failure

The installed E4C runner originally required `$env:C11D_GODOT_EXECUTABLE` and did not resolve Godot from PATH or standard install folders. The first runner invocation therefore stopped before the Python preflight, Godot version probe, or any dynamic matrix execution. A prior D9 runner already provided PATH and standard-folder discovery.

The first package attempt (hotfix package V1) then repeated a previously diagnosed installer defect: its expected frozen C11-C SHA was misspelled as a 63-character value. The active manifest was unchanged and correct. The installer stopped at its first frozen-manifest preflight, before source replacement, documentation additions, staging or evidence transaction. The operator's output confirms no V1 hotfix writes. The V2 installer defines the canonical 64-character SHA once and reuses that value for all semantic checks and the receipt.

## V2 correction

- Explicit valid `$env:C11D_GODOT_EXECUTABLE` wins.
- Otherwise resolve `godot4.exe`, `godot.exe`, `godot4`, or `godot` from PATH.
- Otherwise search Downloads, `C:\Godot`, and `%LOCALAPPDATA%\Programs\Godot` for the Godot 4.7.1 Mono console executable.
- Probe candidates through `System.Diagnostics.ProcessStartInfo` with stdout/stderr capture; accept only exact `4.7.1.stable.mono.official.a13da4feb`.
- Set the resolved environment variable and pass the exact path to the Python runtime matrix.
- Installer validates its complete package contents manifest, frozen C11-C manifest (796,318 bytes and canonical SHA), runner preimage/postimage, all eight documentation payloads, and PowerShell AST before repository writes.
- Transaction uses a unique backup for `[IO.File]::Replace`, add-only moves, postimage checks and rollback.

## Scope and boundary

One pinned replacement: `tools/c11d/d9/RUN_C11E_E4C_DRILL_BINDER_V2_ACCEPTANCE_V1.ps1`, plus eight versioned documentation additions. No service, binder, GUI, C11-C source, frozen manifest, test fixture, or media behavior changes. This hotfix executes no Godot test or renderer. Actual Windows PowerShell 5.1 installation and E4C runtime acceptance remain pending operator execution.
