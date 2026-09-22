param(
    [switch]$Apply,
    [switch]$ResetC11C
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
Write-Host '[C11C-CLEAN] Ordinary mode: only regenerable prototype media is removed; metadata is retained.'
Write-Host '[C11C-CLEAN] Reset mode (-ResetC11C): removes the complete C11-C prototype workspace and scratch, then recreates them.'
Write-Host ''

if ($ResetC11C) {
    $targets = @()
    if (Test-Path -LiteralPath $PrototypeRoot) {
        $targets += @(Get-ChildItem -LiteralPath $PrototypeRoot -Directory -Force | Where-Object { $_.Name -like 'c11c_*' })
    }
    if (Test-Path -LiteralPath $ScratchRoot) {
        $targets += @(Get-ChildItem -LiteralPath $ScratchRoot -Force)
    }

    $totalBytes = [int64]0
    foreach ($item in $targets) {
        $bytes = if ($item.PSIsContainer) { Get-TreeBytes $item.FullName } else { [int64]$item.Length }
        $totalBytes += $bytes
        if ($Apply) {
            Remove-Item -LiteralPath $item.FullName -Recurse -Force
            Write-Host "[C11C-CLEAN] RESET REMOVED  $($item.FullName)"
        } else {
            Write-Host "[C11C-CLEAN] RESET WOULD REMOVE  $($item.FullName)"
        }
    }

    if ($Apply) {
        New-Item -ItemType Directory -Force -Path $PrototypeRoot | Out-Null
        New-Item -ItemType Directory -Force -Path $ScratchRoot | Out-Null
    }

    $totalMB = [math]::Round($totalBytes / 1MB, 2)
    Write-Host ''
    Write-Host "[C11C-CLEAN] Reset targets: $($targets.Count)"
    Write-Host "[C11C-CLEAN] Reset reclaimable: $totalMB MB"
    if ($Apply) {
        Write-Host '[C11C-CLEAN] C11-C RESET COMPLETE. Protected evidence roots were not touched.'
    } else {
        Write-Host '[C11C-CLEAN] C11-C RESET DRY-RUN ONLY. Rerun with -Apply to delete.'
    }
    return
}

$candidates = @()
if (Test-Path -LiteralPath $PrototypeRoot) {
    Get-ChildItem -LiteralPath $PrototypeRoot -Recurse -File -Force | ForEach-Object {
        $isProtected = $false
        foreach ($root in $ProtectedRoots) {
            if (Is-UnderRoot $_.FullName $root) { $isProtected = $true; break }
        }
        if (-not $isProtected -and $_.Extension.ToLowerInvariant() -in $DisposableExtensions) {
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

if ($Apply) {
    foreach ($root in @($PrototypeRoot, $ScratchRoot)) {
        if (Test-Path -LiteralPath $root) {
            Get-ChildItem -LiteralPath $root -Recurse -Directory -Force |
                Sort-Object FullName -Descending |
                Where-Object { @(Get-ChildItem -LiteralPath $_.FullName -Force -ErrorAction SilentlyContinue).Count -eq 0 } |
                ForEach-Object { Remove-Item -LiteralPath $_.FullName -Force -ErrorAction SilentlyContinue }
        }
    }
}

$totalMB = [math]::Round(($totalBytes + $scratchBytes) / 1MB, 2)
Write-Host ''
Write-Host "[C11C-CLEAN] Prototype media files: $($candidates.Count)"
Write-Host "[C11C-CLEAN] Scratch top-level entries: $($scratchItems.Count)"
Write-Host "[C11C-CLEAN] Reclaimable: $totalMB MB"
if ($Apply) {
    Write-Host '[C11C-CLEAN] CLEANUP COMPLETE. Protected evidence roots were not touched.'
} else {
    Write-Host '[C11C-CLEAN] DRY-RUN ONLY. Review the list, then rerun with -Apply to delete.'
}
