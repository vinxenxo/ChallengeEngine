param(
    [switch]$Apply
)

$ErrorActionPreference = 'Stop'
$ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$ArtifactsRoot = Join-Path $ProjectRoot 'artifacts'
$PrototypeRoot = Join-Path $ArtifactsRoot 'prototypes'
$ScratchRoot = Join-Path $ArtifactsRoot 'scratch'

$ProtectedRoots = @(
    (Join-Path $ArtifactsRoot 'legacy'),
    (Join-Path $ArtifactsRoot 'qa'),
    (Join-Path $ArtifactsRoot 'regression'),
    (Join-Path $ArtifactsRoot 'releases'),
    (Join-Path $ArtifactsRoot 'production'),
    (Join-Path $ArtifactsRoot 'tests')
)

$ProtectedPrototypeRoots = @(
    (Join-Path $PrototypeRoot 'c11c_review_assets')
)

$DisposableExtensions = @(
    '.mp4', '.gif', '.avi', '.wav',
    '.png', '.jpg', '.jpeg', '.webp', '.bmp',
    '.mov', '.mkv', '.webm'
)

function Normalize-Path([string]$Path) {
    return [System.IO.Path]::GetFullPath($Path).TrimEnd('\')
}

function Is-UnderRoot([string]$Path, [string]$Root) {
    $full = Normalize-Path $Path
    $base = Normalize-Path $Root
    return $full.Equals($base, [System.StringComparison]::OrdinalIgnoreCase) -or
           $full.StartsWith($base + '\', [System.StringComparison]::OrdinalIgnoreCase)
}

function Get-TreeBytes([string]$Path) {
    if (-not (Test-Path -LiteralPath $Path)) { return [int64]0 }
    $sum = (Get-ChildItem -LiteralPath $Path -Recurse -File -Force -ErrorAction SilentlyContinue |
        Measure-Object -Property Length -Sum).Sum
    if ($null -eq $sum) { return [int64]0 }
    return [int64]$sum
}

Write-Host '[C11C-CLEAN] =========================================='
Write-Host "[C11C-CLEAN] ProjectRoot: $ProjectRoot"
Write-Host "[C11C-CLEAN] Mode: $(if ($Apply) { 'APPLY' } else { 'DRY-RUN' })"
Write-Host '[C11C-CLEAN] Protected roots: legacy / qa / regression / releases / production / tests'
Write-Host '[C11C-CLEAN] Protected prototype root: c11c_review_assets'
Write-Host '[C11C-CLEAN] Ordinary cleanup only: regenerable prototype media + scratch.'
Write-Host '[C11C-CLEAN] Full C11-C reset is a separate command: reset_c11c_artifacts.ps1'
Write-Host '[C11C-CLEAN] Prototype metadata (*.json/*.txt/*.md/*.sha256 etc.) is retained.'
Write-Host ''

$candidates = @()
if (Test-Path -LiteralPath $PrototypeRoot) {
    Get-ChildItem -LiteralPath $PrototypeRoot -Recurse -File -Force | ForEach-Object {
        $protected = $false
        foreach ($root in ($ProtectedRoots + $ProtectedPrototypeRoots)) {
            if (Is-UnderRoot $_.FullName $root) { $protected = $true; break }
        }
        if (-not $protected -and $_.Extension.ToLowerInvariant() -in $DisposableExtensions) {
            $candidates += $_
        }
    }
}

$scratchItems = @()
if (Test-Path -LiteralPath $ScratchRoot) {
    $scratchItems = @(Get-ChildItem -LiteralPath $ScratchRoot -Force)
}

$totalBytes = [int64]0
foreach ($file in $candidates) {
    $totalBytes += [int64]$file.Length
    if ($Apply) {
        Remove-Item -LiteralPath $file.FullName -Force
        Write-Host "[C11C-CLEAN] REMOVED  $($file.FullName)"
    } else {
        Write-Host "[C11C-CLEAN] WOULD REMOVE  $($file.FullName)"
    }
}

$scratchBytes = [int64]0
foreach ($item in $scratchItems) {
    $bytes = if ($item.PSIsContainer) { Get-TreeBytes $item.FullName } else { [int64]$item.Length }
    $scratchBytes += $bytes
    if ($Apply) {
        Remove-Item -LiteralPath $item.FullName -Recurse -Force
        Write-Host "[C11C-CLEAN] REMOVED SCRATCH  $($item.FullName)"
    } else {
        Write-Host "[C11C-CLEAN] WOULD REMOVE SCRATCH  $($item.FullName)"
    }
}

$totalMB = [math]::Round(($totalBytes + $scratchBytes) / 1MB, 2)
Write-Host ''
Write-Host "[C11C-CLEAN] Prototype media files: $($candidates.Count)"
Write-Host "[C11C-CLEAN] Scratch top-level entries: $($scratchItems.Count)"
Write-Host "[C11C-CLEAN] Reclaimable: $totalMB MB"
if ($Apply) {
    Write-Host '[C11C-CLEAN] CLEANUP COMPLETE. Protected evidence/review assets were not touched.'
} else {
    Write-Host '[C11C-CLEAN] DRY-RUN ONLY. Review the list, then rerun with -Apply to delete.'
}
return
