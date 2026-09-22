param(
    [switch]$Apply
)

$ErrorActionPreference = 'Stop'
$ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$ArtifactsRoot = Join-Path $ProjectRoot 'artifacts'
$PrototypeRoot = Join-Path $ArtifactsRoot 'prototypes'
$ScratchRoot = Join-Path $ArtifactsRoot 'scratch'

Write-Host '[C11C-RESET] =========================================='
Write-Host "[C11C-RESET] ProjectRoot: $ProjectRoot"
Write-Host "[C11C-RESET] Mode: $(if ($Apply) { 'APPLY' } else { 'DRY-RUN' })"
Write-Host '[C11C-RESET] This command is intentionally separate from every render/review launcher.'
Write-Host '[C11C-RESET] Protected evidence roots: legacy / qa / regression / releases / production / tests'
Write-Host ''

$targets = @()
if (Test-Path -LiteralPath $PrototypeRoot) {
    $targets += @(Get-ChildItem -LiteralPath $PrototypeRoot -Directory -Force | Where-Object { $_.Name -like 'c11c_*' })
}
if (Test-Path -LiteralPath $ScratchRoot) {
    $targets += @(Get-ChildItem -LiteralPath $ScratchRoot -Force)
}

$totalBytes = [int64]0
function Get-TreeBytes([string]$Path) {
    if (-not (Test-Path -LiteralPath $Path)) { return [int64]0 }
    $sum = (Get-ChildItem -LiteralPath $Path -Recurse -File -Force -ErrorAction SilentlyContinue |
        Measure-Object -Property Length -Sum).Sum
    if ($null -eq $sum) { return [int64]0 }
    return [int64]$sum
}

foreach ($item in $targets) {
    $bytes = if ($item.PSIsContainer) { Get-TreeBytes $item.FullName } else { [int64]$item.Length }
    $totalBytes += $bytes
    if ($Apply) {
        Remove-Item -LiteralPath $item.FullName -Recurse -Force
        Write-Host "[C11C-RESET] REMOVED  $($item.FullName)"
    } else {
        Write-Host "[C11C-RESET] WOULD REMOVE  $($item.FullName)"
    }
}

if ($Apply) {
    New-Item -ItemType Directory -Force -Path $PrototypeRoot | Out-Null
    New-Item -ItemType Directory -Force -Path $ScratchRoot | Out-Null
}

$totalMB = [math]::Round($totalBytes / 1MB, 2)
Write-Host ''
Write-Host "[C11C-RESET] Targets: $($targets.Count)"
Write-Host "[C11C-RESET] Reclaimable: $totalMB MB"
if ($Apply) {
    Write-Host '[C11C-RESET] C11-C RESET COMPLETE. Protected evidence roots were not touched.'
} else {
    Write-Host '[C11C-RESET] DRY-RUN ONLY. Rerun with -Apply to delete.'
}
return
