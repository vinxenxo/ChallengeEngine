# C11-E E6 Smoke18 — Evidence Requalification V2

**Status:** `REQUALIFICATION_CANDIDATE_LEDGER_PREPARED_NOT_FROZEN_NOT_E6_ACCEPTED`  
**Date:** 2026-11-18  
**Scope:** read-only evidence reconciliation and add-only ledger documentation. No media execution.

## V2 installer/runner correction

V1 failed at the Python version check because Windows PowerShell 5.1 altered the nested quotation marks in an inline `python -c` argument. The operator's log shows that failure occurred before payload preflight and before checkout copies. V2 removes inline Python source from the PowerShell native-command argument path entirely.

Both installer and runner now:

- read the Python version through `.NET System.Diagnostics.ProcessStartInfo` using the simple `--version` argument;
- redirect and asynchronously consume stdout and stderr, so stderr cannot be promoted by `$ErrorActionPreference='Stop'` into a false test failure;
- explicitly set `$global:LASTEXITCODE` to `1` on entry and `0` only after complete success; non-zero Python test/audit codes are propagated;
- use versioned V2 runner, validator and test destinations, leaving any V1 tool files untouched;
- verify all payload sizes and SHA-256 values, validate all destinations before writing, refuse differing destinations, and install only by `ADD_ONLY`.

The ledger retains the exact V1 bytes and same destination. If it is already present with the same SHA-256 it is skipped; a differing file is a hard stop, never overwritten.

## Evidence requalification state

The ledger contains 18 top-level scenarios: 6 Challenge, 6 Loop and 6 Drill. Thirteen are reuse candidates with reconciled evidence references: CH004, six Loop and six Drill. Five Challenge scenarios still require fresh A/V qualification. The rows remain candidates; `e6_accepted_scenarios=0` and the matrix is not frozen.

Hydration V2's historical report remains unchanged at 1,801/1,803 checks, with the two original historical source-pin divergence checks retained. The D9 pin reconciliation V2 and CH004 semantic review V4 provide the separate adjudication evidence; this V2 runner verifies their pinned reports and sidecars rather than rewriting the historical result.

Loop22 `interference_plane` A/B was independently rehashed in the active checkout by the operator: both MP4 files are 10,500,987 bytes and SHA-256 `a2fdb135a201a5ce9f91c19b51c65be53ab0d0aaeced6829633958195d7f0131`. The family-specific Loop profile (`yuvj420p`, full range) is preserved; it is not normalized to CH004's `yuv420p`, TV-range profile.

## Install V2

1. Verify the package ZIP against its external `.sha256` sidecar.
2. Extract to a new, empty Downloads folder; do not extract over the active checkout or the previous V1 package extraction.
3. Run from Windows PowerShell 5.1:

```powershell
$ErrorActionPreference = 'Stop'
$ProjectRoot = 'C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS'
$PackageRoot = Join-Path $env:USERPROFILE 'Downloads\C11E_E6_SMOKE18_REUSE_REQUALIFICATION_V2'
$PythonExe = Join-Path $env:LOCALAPPDATA 'Programs\Python\Python313\python.exe'
$Installer = Join-Path $PackageRoot 'INSTALL_C11E_E6_SMOKE18_REUSE_REQUALIFICATION_V2.ps1'
Unblock-File -LiteralPath $Installer
& $Installer -ProjectRoot $ProjectRoot -PackageRoot $PackageRoot -PythonExe $PythonExe
if ($LASTEXITCODE -ne 0) { throw "E6_REQUALIFICATION_INSTALL_FAILED:$LASTEXITCODE" }
```

Expected installation status: `PASS_ADD_ONLY_E6_SMOKE18_REUSE_REQUALIFICATION_INSTALL`, five payloads, two unchanged governance anchors, 32/32 focused tests. The installer writes `INSTALL_RECEIPT_V2.json` and its SHA-256 sidecar.

## Run the read-only requalification

Only after install PASS:

```powershell
$Runner = Join-Path $ProjectRoot 'tools\c11d\d9\RUN_C11E_E6_SMOKE18_REUSE_REQUALIFICATION_V2.ps1'
& $Runner -ProjectRoot $ProjectRoot -PythonExe $PythonExe
if ($LASTEXITCODE -ne 0) { throw "E6_REQUALIFICATION_BLOCKED:$LASTEXITCODE; preserve the report." }
```

A complete result is `PASS_REUSE_EVIDENCE_LINKAGE_REQUALIFIED_NOT_E6_ACCEPTANCE`. A blocked report is preserved and returns a non-zero exit code.

## Governance remains unchanged

- D4.8 remains `BLOCKED`; no override is claimed.
- E1 remains `PREPARE_ONLY`; family adapter `NOT_CONNECTED_E1`; renderer OFF; production dispatch/media false.
- No Godot, Movie Maker, D3/D3.3, FFmpeg, FFprobe, audio, mux, media creation or BatchId reservation/consumption.
- `release_authority=NONE`.
- No Git checks; commits operator-managed; source-file SHA-256 pins enforced.
- C11-C frozen manifest SHA-256 remains `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.
