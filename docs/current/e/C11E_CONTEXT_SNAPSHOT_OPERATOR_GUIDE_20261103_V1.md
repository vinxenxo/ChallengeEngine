# C11-E Context Snapshot Operator Guide — V1

## Purpose

Create a filtered context ZIP to attach to the next ChatGPT window. Use the repository's existing C11-D snapshot utility; do not create ad-hoc ZIPs in the checkout and do not place the archive in `release`.

## Canonical tool

`tools\c11d\packaging\New-C11DWorkingSnapshot.ps1`

The utility derives the active repository root from its own location. Do not pass `-Root`. The supported parameters used here are `-OutputDirectory`, `-ArchiveName` and `-PreflightOnly`.

## PowerShell 5.1 command

```powershell
$ErrorActionPreference = 'Stop'
$Root = 'C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS'
$SnapshotTool = Join-Path $Root 'tools\c11d\packaging\New-C11DWorkingSnapshot.ps1'
$Documents = [Environment]::GetFolderPath('MyDocuments')
$SnapshotDirectory = Join-Path $Documents 'C11E_CONTEXT_SNAPSHOTS'
$ArchiveName = 'C11E_WORKING_CONTEXT_' + (Get-Date -Format 'yyyyMMdd_HHmmss') + '.zip'

if (-not (Test-Path -LiteralPath $SnapshotTool -PathType Leaf)) {
    throw "Snapshot generator missing: $SnapshotTool"
}
if (-not (Test-Path -LiteralPath $SnapshotDirectory -PathType Container)) {
    New-Item -ItemType Directory -Path $SnapshotDirectory -Force | Out-Null
}

Write-Host '========== SNAPSHOT PREFLIGHT =========='
& $SnapshotTool -OutputDirectory $SnapshotDirectory -ArchiveName $ArchiveName -PreflightOnly
if (-not $?) { throw 'SNAPSHOT PREFLIGHT FAILED.' }

Write-Host '========== SNAPSHOT GENERATION =========='
& $SnapshotTool -OutputDirectory $SnapshotDirectory -ArchiveName $ArchiveName
if (-not $?) { throw 'SNAPSHOT GENERATION FAILED.' }

$SnapshotZip = Join-Path $SnapshotDirectory $ArchiveName
$SnapshotSidecar = $SnapshotZip + '.sha256'
$SnapshotReport = $SnapshotZip + '.report.json'
foreach ($File in @($SnapshotZip, $SnapshotSidecar, $SnapshotReport)) {
    if (-not (Test-Path -LiteralPath $File -PathType Leaf)) {
        throw "Snapshot output missing: $File"
    }
}
$SnapshotSha = (Get-FileHash -LiteralPath $SnapshotZip -Algorithm SHA256).Hash.ToLowerInvariant()
$SnapshotBytes = (Get-Item -LiteralPath $SnapshotZip).Length
Write-Host 'C11-E SNAPSHOT GENERATED'
Write-Host "ZIP=$SnapshotZip"
Write-Host "BYTES=$SnapshotBytes"
Write-Host "SHA256=$SnapshotSha"
Write-Host "SIDECAR=$SnapshotSidecar"
Write-Host "REPORT=$SnapshotReport"
```

## Why this does not change the repository or C11-C manifest

The archive, sidecar and report are written under `%USERPROFILE%\Documents\C11E_CONTEXT_SNAPSHOTS`, outside the repository. Do not change `$SnapshotDirectory` to `$Root\release` or any directory under the checkout. Writing outside the checkout cannot add a Git working-tree path or change the Git tree hash. The tool copies, but does not rebuild, `release\C11C_FREEZE_PACKAGE_MANIFEST.json`; its required identity remains 796,318 bytes and SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`. It must appear exactly once in the ZIP.

The ZIP is a filtered context snapshot, not a release, freeze, backup or evidence package. It excludes the `artifacts` tree except compact allowlisted evidence, caches/build outputs, nested archives, temp files and selected local evidence. Therefore upload the latest E3 run receipt/logs and any media evidence ZIP separately if they are needed in the next window.

## Attach to the next window

Upload these three snapshot outputs:

1. `C11E_WORKING_CONTEXT_*.zip`
2. `C11E_WORKING_CONTEXT_*.zip.sha256`
3. `C11E_WORKING_CONTEXT_*.zip.report.json`

Also attach the E3 Windows test receipt/logs from `Documents\C11E_E3_TEST_EVIDENCE\C11E_E3_TESTS_V14_f371a0bfdccf407aba5e3e4cbf6c5f4b` when needed. Never extract the snapshot over the active Windows checkout.
