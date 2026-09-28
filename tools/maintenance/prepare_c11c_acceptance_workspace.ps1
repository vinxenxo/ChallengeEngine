[CmdletBinding()]
param(
    [switch]$RotateAcceptanceRoots,
    [switch]$QuarantineCaches,
    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$stamp = Get-Date -Format 'yyyyMMdd_HHmmss'
$QuarantineRoot = Join-Path $ProjectRoot ("artifacts\maintenance\quarantine\c11c_acceptance_$stamp")

function Ensure-Dir([string]$Path) {
    if (-not (Test-Path -LiteralPath $Path -PathType Container)) {
        if (-not $DryRun) { New-Item -ItemType Directory -Path $Path -Force | Out-Null }
    }
}

function Move-Safely([string]$Source, [string]$Label) {
    if (-not (Test-Path -LiteralPath $Source)) { return }
    $leaf = Split-Path -Leaf $Source
    $destination = Join-Path $QuarantineRoot (Join-Path $Label $leaf)
    Write-Host "[C11C-MAINT] QUARANTINE: $Source -> $destination"
    if ($DryRun) { return }
    Ensure-Dir (Split-Path -Parent $destination)
    Move-Item -LiteralPath $Source -Destination $destination -Force
}

if ($RotateAcceptanceRoots) {
    foreach ($entry in @(
        @{ Path = Join-Path $ProjectRoot 'artifacts\qa\c11a1_challenge'; Label = 'qa' },
        @{ Path = Join-Path $ProjectRoot 'artifacts\qa\physical_smoke\c10c_e2e'; Label = 'qa' },
        @{ Path = Join-Path $ProjectRoot 'artifacts\prototypes\c11c_art_direction_review'; Label = 'prototypes' },
        @{ Path = Join-Path $ProjectRoot 'artifacts\prototypes\c11c_visual_drills_review'; Label = 'prototypes' }
    )) {
        Move-Safely ([string]$entry.Path) ([string]$entry.Label)
    }
}

# Accidental extracted overlay folders are never part of the source tree.
foreach ($name in @(
    'C11C_2.19.3_PRODUCER_TEST_REPAIR_OVERLAY',
    'C11C_2.19.3_PRODUCER_TEST_REPAIR_OVERLAY_ROOT'
)) {
    Move-Safely (Join-Path $ProjectRoot $name) 'accidental_overlay'
}

# Known typo directory: quarantine only if both variants exist; never merge blindly.
$typo = Join-Path $ProjectRoot 'c11c-suite\c11c-maintenace'
$canonical = Join-Path $ProjectRoot 'c11c-suite\c11c-maintenance'
if ((Test-Path -LiteralPath $typo -PathType Container) -and (Test-Path -LiteralPath $canonical -PathType Container)) {
    Write-Host '[C11C-MAINT] Both c11c-maintenace and c11c-maintenance exist. They are NOT auto-merged.'
    Write-Host '[C11C-MAINT] Review both trees; use -DryRun to inspect quarantine actions.'
}

if ($QuarantineCaches) {
    $cacheRoots = @(
        (Join-Path $ProjectRoot '.pytest_cache'),
        (Join-Path $ProjectRoot 'c11c-suite\.pytest_cache'),
        (Join-Path $ProjectRoot 'c11c-suite\c11c-producer\__pycache__')
    )
    foreach ($path in $cacheRoots) { Move-Safely $path 'caches' }
}

Write-Host '[C11C-MAINT] Workspace preparation complete.'
Write-Host "[C11C-MAINT] Quarantine root: $QuarantineRoot"
