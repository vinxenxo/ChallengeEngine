param(
    [switch]$Apply
)

$ErrorActionPreference = 'Stop'

# c11c_bulk -> prototypes -> tools -> project root
$ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$ArtifactsRoot = Join-Path $ProjectRoot 'artifacts'
$PrototypeRoot = Join-Path $ArtifactsRoot 'prototypes'
$ScratchRoot = Join-Path $ArtifactsRoot 'scratch'

# Never remove any historical/certification evidence from these roots.
$ProtectedRoots = @(
    (Join-Path $ArtifactsRoot 'legacy'),
    (Join-Path $ArtifactsRoot 'qa'),
    (Join-Path $ArtifactsRoot 'regression'),
    (Join-Path $ArtifactsRoot 'releases'),
    (Join-Path $ArtifactsRoot 'production'),
    (Join-Path $ArtifactsRoot 'tests')
)

# Review keyframes are intentionally retained: they are active visual-review evidence.
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

function Is-Protected([string]$Path) {
    foreach ($root in $ProtectedRoots) {
        if (Is-UnderRoot $Path $root) { return $true }
    }
    foreach ($root in $ProtectedPrototypeRoots) {
        if (Is-UnderRoot $Path $root) { return $true }
    }
    return $false
}

$Candidates = @()

if (Test-Path -LiteralPath $PrototypeRoot) {
    Get-ChildItem -LiteralPath $PrototypeRoot -Recurse -File -Force | ForEach-Object {
        if ($_.Extension.ToLowerInvariant() -in $DisposableExtensions -and -not (Is-Protected $_.FullName)) {
            $Candidates += $_
        }
    }
}

$ScratchItems = @()
if (Test-Path -LiteralPath $ScratchRoot) {
    $ScratchItems = @(Get-ChildItem -LiteralPath $ScratchRoot -Force)
}

Write-Host '[C11C-CLEAN] =========================================='
Write-Host "[C11C-CLEAN] ProjectRoot: $ProjectRoot"
Write-Host "[C11C-CLEAN] Mode: $(if ($Apply) { 'APPLY' } else { 'DRY-RUN' })"
Write-Host '[C11C-CLEAN] Protected roots: legacy / qa / regression / releases / production / tests'
Write-Host '[C11C-CLEAN] Protected prototype root: c11c_review_assets'
Write-Host '[C11C-CLEAN] Disposable prototype media: MP4/GIF/AVI/WAV/PNG/JPEG/WebP/BMP/MOV/MKV/WebM'
Write-Host '[C11C-CLEAN] Prototype metadata (*.json/*.txt/*.md/*.sha256 etc.) is retained.'
Write-Host ''

$totalBytes = [int64]0
foreach ($file in $Candidates) {
    $totalBytes += [int64]$file.Length
    if ($Apply) {
        Remove-Item -LiteralPath $file.FullName -Force
        Write-Host "[C11C-CLEAN] REMOVED  $($file.FullName)"
    } else {
        Write-Host "[C11C-CLEAN] WOULD REMOVE  $($file.FullName)"
    }
}

$scratchBytes = [int64]0
foreach ($item in $ScratchItems) {
    if ($item.PSIsContainer) {
        $sum = (Get-ChildItem -LiteralPath $item.FullName -Recurse -File -ErrorAction SilentlyContinue |
            Measure-Object -Property Length -Sum).Sum
        if ($null -ne $sum) { $scratchBytes += [int64]$sum }
    } else {
        $scratchBytes += [int64]$item.Length
    }

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
                Where-Object {
                    -not (Is-Protected $_.FullName) -and
                    @(Get-ChildItem -LiteralPath $_.FullName -Force -ErrorAction SilentlyContinue).Count -eq 0
                } |
                ForEach-Object { Remove-Item -LiteralPath $_.FullName -Force -ErrorAction SilentlyContinue }
        }
    }
}

$totalMB = [math]::Round(($totalBytes + $scratchBytes) / 1MB, 2)
Write-Host ''
Write-Host "[C11C-CLEAN] Prototype media files: $($Candidates.Count)"
Write-Host "[C11C-CLEAN] Scratch top-level entries: $($ScratchItems.Count)"
Write-Host "[C11C-CLEAN] Reclaimable: $totalMB MB"

if ($Apply) {
    Write-Host '[C11C-CLEAN] CLEANUP COMPLETE. Protected evidence/review assets were not touched.'
} else {
    Write-Host '[C11C-CLEAN] DRY-RUN ONLY. Review the list, then rerun with -Apply to delete.'
}
