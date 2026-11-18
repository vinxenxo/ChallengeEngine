# C11-E E6 Render Gate Preflight V1

**Purpose:** advance Smoke18 toward a controlled TEST_ONLY render by reconciling the active checkout's source pins, exact predecessor receipts and previously accepted external tool binary hashes. This package is strictly read-only except for its own report under `artifacts/tests/c11e/e6_render_gate_preflight/`.

## What it checks

- 20 source pins, including the immutable C11-C manifest, D4.8 V2, Challenge/Drill consumers, the Loop boundary and the three Loop proposal hashes.
- Eight predecessor receipts, including Composition Readiness V2, Challenge PREPARE_ONLY, reuse requalification, family-editorial install/plan/audit and the prior D9 pin / reuse hydration reports.
- Five runtime binaries by exact path, SHA-256 and byte size using file reads only: Godot 4.7.1 Mono, FFmpeg 9.0, FFprobe 9.0, Python 3.13.14 and Windows PowerShell 5.1. **No executable is invoked to discover a version.**
- The 18-row / 30-editorial-target contract and all known open gates.

## Important interpretation

A successful preflight does **not** mean the render is authorized. The output deliberately preserves these blockers: CH004 historical D9 model drift; five fresh Challenge A/V rows; six missing/unadmitted Loop D pixel compositions; six Drill and 18 Challenge editorial runtime readbacks; Loop policy decision reconciliation; global D renderer I/O baseline (0/10 complete, 6 partial, 4 blocked); D4.8 successor approval; and the separate E6 TEST_ONLY execution authorization.

The historical E6 hydration V2 report is expected to retain its two CH004 source drift failures. The service change was later superseded by the accepted 33-pin source baseline, but this does not waive the D9 editorial-model preimage divergence. The preflight will not auto-waive either condition.

The package contains a draft successor policy V2. It is a proposal only and does not mutate D4.8 V2. The prior operator-approved Challenge music fixture (840001/840002, 104 BPM) and family editorial copy remain test-only; E1 tempo/duration remain null.

## Install

Extract the ZIP to a fresh temporary folder (do not extract over the checkout). Verify the ZIP SHA-256 from its `.sha256` sidecar. The installer is at archive root:

```powershell
$ErrorActionPreference = 'Stop'
$ProjectRoot = 'C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS'
$PackageRoot = 'C:\Path\To\Fresh\Extracted\C11E_E6_RENDER_GATE_PREFLIGHT_V1'
$Installer = Join-Path $PackageRoot 'INSTALL_C11E_E6_RENDER_GATE_PREFLIGHT_V1.ps1'
if (-not (Test-Path -LiteralPath $Installer -PathType Leaf)) { throw "INSTALLER_NOT_FOUND:$Installer" }
Unblock-File -LiteralPath $Installer
powershell.exe -NoProfile -ExecutionPolicy Bypass -File $Installer -ProjectRoot $ProjectRoot -PackageRoot $PackageRoot
if ($LASTEXITCODE -ne 0) { throw 'RENDER_GATE_PREFLIGHT_INSTALL_FAILED; preserve all evidence' }
```

## Run

Only after `INSTALL_STATUS=PASS`:

```powershell
$PythonExe = Join-Path $env:LOCALAPPDATA 'Programs\Python\Python313\python.exe'
$Runner = Join-Path $ProjectRoot 'tools\c11d\d9\RUN_C11E_E6_RENDER_GATE_PREFLIGHT_V1.ps1'
if (-not (Test-Path -LiteralPath $Runner -PathType Leaf)) { throw "RUNNER_NOT_INSTALLED:$Runner" }
powershell.exe -NoProfile -ExecutionPolicy Bypass -File $Runner -ProjectRoot $ProjectRoot -PythonExe $PythonExe
if ($LASTEXITCODE -ne 0) { throw 'RENDER_GATE_PREFLIGHT_AUDIT_DID_NOT_COMPLETE; preserve report and logs' }
```

The runner verifies Windows PowerShell 5.1 AST parsing, Python 3.13.14 and focused unit tests. It writes a JSON receipt and sidecar. Source/receipt/tool mismatches are recorded as blockers; the audit exits successfully if the report is written, even when the render gate remains blocked.

## Forbidden operations

This package does not invoke Godot/Movie Maker, FFmpeg, FFprobe, D3, audio generation, mux, render, dispatch or any production process; it does not reserve/consume a BatchId, create media, mutate protected source, modify D4.8 V2, freeze the E6 matrix, or grant release authority. Git checks are skipped and commits remain operator-managed.
