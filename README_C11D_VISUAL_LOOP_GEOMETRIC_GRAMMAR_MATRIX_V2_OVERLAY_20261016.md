# C11-D Visual Loop Geometric Grammar Matrix V2 Overlay — 2026-10-16

Additive-only D-owned preparation overlay. It introduces a read-only Godot probe for the **five grammar IDs in the frozen C11-C Geometric Waves prototype**, each tested against four explicit gameplay seeds (20 grammar/seed cases). It does not replace or alter any existing file.

## What this increment establishes

- The local parameter-projection stage maps `harmonic_membrane`, `interference_plane`, `parametric_ribbon`, `lattice_wave`, and `orbital_wave` to indices 0–4 and their shader branch identifiers.
- Each of the 20 grammar/seed pairs projects exactly 20 style values and repeats the same projection deterministically in memory.
- The runner and schemas are source-pinned, including the frozen C11-C manifest, producer registry, geometric variation profile, prototype, renderer, shader, and probe/runner implementations.
- The audit never instantiates a renderer/material, executes the shader, writes payload/receipt files, emits renderer input, or creates media.

## Mandatory boundary

This is **parameter-mapping evidence only**. It does **not** admit the four non-harmonic grammar IDs through the canonical D9.9/D9.10 request-binding chain; that chain remains pinned to `harmonic_membrane`. It does not prove a canonical request-bound payload, editorial consumption, presentation geometry, timeline/audio compliance, renderer input admission, or production readiness. The renderer stays OFF; media creation is false; D4.8 remains BLOCKED; release authority remains NONE; D9.14/D9.16/D9.17/D10 remain blocked.

## Apply from the repository root

Extract the ZIP into the existing repository root **without `-Force`**. All paths in this overlay are new additions; an existing-path conflict should stop the operation rather than be overwritten. Verify the ZIP SHA-256 using the sidecar delivered with it.

## Run the contract tests first

```powershell
$pythonPath = (Get-Command python.exe -ErrorAction Stop).Source
$testOut = Join-Path $env:TEMP 'C11D_GEOMETRIC_GRAMMAR_MATRIX_V2_TEST.stdout.txt'
$testErr = Join-Path $env:TEMP 'C11D_GEOMETRIC_GRAMMAR_MATRIX_V2_TEST.stderr.txt'
$p = Start-Process -FilePath $pythonPath -ArgumentList @('-B', '.\tools\c11d\d9\test_d_renderer_visual_loop_geometric_grammar_matrix_v2.py') -WorkingDirectory (Get-Location).Path -RedirectStandardOutput $testOut -RedirectStandardError $testErr -Wait -PassThru
Get-Content $testOut; Get-Content $testErr
if ($p.ExitCode -ne 0 -or (Get-Content $testErr -Raw) -notmatch '(?m)^OK\s*$') { throw 'Contract tests failed; runtime not started.' }
```

The expected preparation result is `Ran 11 tests` / `OK`. These tests use a mocked process boundary and are **not** evidence of a real Godot run.

## Run the real Godot probe

Use the exact executable confirmed by the successful cross-type runtime audit; do not guess another installation path:

```powershell
$godotPath = 'C:\Users\vinxe\AppData\Local\Microsoft\WinGet\Packages\GodotEngine.GodotEngine.Mono_Microsoft.Winget.Source_8wekyb3d8bbwe\Godot_v4.7.1-stable_mono_win64\godot.exe'
if (-not (Test-Path -LiteralPath $godotPath -PathType Leaf)) { throw 'The previously verified Godot path is unavailable; do not launch with a guessed path.' }
$pythonPath = (Get-Command python.exe -ErrorAction Stop).Source
$repoRoot = (Get-Location).Path
$runtimeOut = Join-Path $env:TEMP 'C11D_GEOMETRIC_GRAMMAR_MATRIX_V2_RUNTIME.stdout.txt'
$runtimeErr = Join-Path $env:TEMP 'C11D_GEOMETRIC_GRAMMAR_MATRIX_V2_RUNTIME.stderr.txt'
$runtimeArgs = '-B .\tools\c11d\d9\d_renderer_visual_loop_geometric_grammar_matrix_v2.py --godot "' + $godotPath + '" --root "' + $repoRoot + '" --timeout 120'
$p = Start-Process -FilePath $pythonPath -ArgumentList $runtimeArgs -WorkingDirectory $repoRoot -RedirectStandardOutput $runtimeOut -RedirectStandardError $runtimeErr -Wait -PassThru
$runtimeText = if (Test-Path -LiteralPath $runtimeOut) { Get-Content -LiteralPath $runtimeOut -Raw } else { '' }
$runtimeErrors = if (Test-Path -LiteralPath $runtimeErr) { Get-Content -LiteralPath $runtimeErr -Raw } else { '' }
Write-Output $runtimeText
if ($runtimeErrors) { Write-Output $runtimeErrors }
if ($p.ExitCode -ne 0 -or $runtimeText -notmatch 'C11-D VISUAL LOOP GEOMETRIC GRAMMAR MATRIX V2 AUDIT PASS' -or $runtimeText -notmatch 'source_pins=12/12' -or $runtimeText -notmatch '"godot_version"\s*:\s*"4\.7\.1\.stable\.mono\.official\.a13da4feb"' -or $runtimeText -notmatch 'renderer=OFF' -or $runtimeText -notmatch 'release_authority=NONE') { throw 'Real Godot matrix not proven PASS; inspect captured output and do not advance the gate.' }
Write-Output 'REAL GODOT MATRIX V2: PASS'
```

The runner checks the exact version string and all 12 pinned source hashes before launching its one headless probe. It emits a self-hashed audit receipt to stdout and does not write any evidence or payload file to the repository.

## Preparation-tree validation in this delivery

- Python contract/negative tests: **11/11 PASS**.
- Contract load, exact 12-source lineage, and five-entry/four-seed input schema: PASS.
- Real Godot execution of the new V2 probe: **not run in this preparation environment**. It must pass in the active Windows checkout before this checkpoint can be described as runtime-verified.

## Next engineering gate

After the real V2 probe passes, the next increment is a separately versioned request-chain extension that admits each supported geometric grammar through D9.9 → D9.10 → request-scoped binding and then proves exact selector payload identity. Do not loosen the V1/V2 pinned contracts in place. Only after that should the family matrix be expanded to the other four Visual Loop families. The independent candidate-I/O gaps for presentation, timeline, audio, editorial field consumption, and authorization remain open.
