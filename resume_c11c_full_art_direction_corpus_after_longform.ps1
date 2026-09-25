<# C11-C - RESUME AFTER LONGFORM PARSER FAILURE

Resumes a failed FULL ART DIRECTION CORPUS run after the 27 Visual Loop
production products have already completed.

Reads the latest full_run_manifest.json so the exact Drill and Longform
seeds from the interrupted run are reused. Does not rerun the 27 loops.
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory=$false)]
    [switch]$Force
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$ProjectRoot = (Resolve-Path $PSScriptRoot).Path
$BulkRoot = Join-Path $ProjectRoot 'tools\prototypes\c11c_bulk'
$Common = Join-Path $BulkRoot 'C11CProductionBatchCommon.ps1'
$Preflight = Join-Path $BulkRoot 'validate_c11c_preflight.ps1'
$Longform = Join-Path $BulkRoot 'run_c11c_visual_loop_longform_production.ps1'
$DrillReview = Join-Path $BulkRoot 'run_c11c_visual_drill_review.ps1'

foreach ($required in @($Common,$Preflight,$Longform,$DrillReview)) {
    if (-not (Test-Path -LiteralPath $required)) { throw "Required C11-C launcher missing: $required" }
}

$manifestFiles = @(Get-ChildItem -LiteralPath (Join-Path $ProjectRoot 'artifacts\batch\full_art_direction') -Filter 'full_run_manifest.json' -File -Recurse -ErrorAction Stop | Sort-Object LastWriteTime -Descending)
if ($manifestFiles.Count -lt 1) { throw 'No full_run_manifest.json found under artifacts\batch\full_art_direction.' }

$manifestPath = $manifestFiles[0].FullName
$manifest = Get-Content -Raw -LiteralPath $manifestPath | ConvertFrom-Json

if ([string]$manifest.schema -ne 'C11-C-FULL-ART-DIRECTION-CORPUS-V1') {
    throw "Unsupported corpus manifest schema: $($manifest.schema)"
}

$longformSeeds = @($manifest.longform.seeds | ForEach-Object { [int]$_ })
$drillSeeds = @($manifest.visual_drill_review.seeds | ForEach-Object { [int]$_ })
if ($longformSeeds.Count -ne 5) { throw "Expected 5 longform seeds in manifest; found $($longformSeeds.Count)." }
if ($drillSeeds.Count -ne 5) { throw "Expected 5 Drill review seeds in manifest; found $($drillSeeds.Count)." }

. $Common
Assert-C11CSeedSpacing -Seeds $longformSeeds
Assert-C11CSeedSpacing -Seeds $drillSeeds

function Invoke-C11CStep {
    param(
        [Parameter(Mandatory=$true)][string]$Label,
        [Parameter(Mandatory=$true)][string]$ScriptPath,
        [Parameter(Mandatory=$true)][hashtable]$Parameters
    )
    Write-Host "START $Label"
    try {
        & $ScriptPath @Parameters
        Write-Host "PASS  $Label"
    }
    catch {
        Write-Host "FAIL  $Label :: $($_.Exception.Message)" -ForegroundColor Red
        throw
    }
}

Invoke-C11CStep -Label 'C11-C PREFLIGHT / RESUME' -ScriptPath $Preflight -Parameters @{}

$familyRows = @(
    @{ Key='geometric';        Production='c11c_geometric_waves_v1'; LongformSeed=[int]$longformSeeds[0] },
    @{ Key='fractal';          Production='c11c_fractal_bloom_v1'; LongformSeed=[int]$longformSeeds[1] },
    @{ Key='sacred_symmetry';  Production='c11c_sacred_symmetry_v1'; LongformSeed=[int]$longformSeeds[2] },
    @{ Key='living_particles'; Production='c11c_living_particles_v1'; LongformSeed=[int]$longformSeeds[3] },
    @{ Key='invisible_forces'; Production='c11c_invisible_forces_v1'; LongformSeed=[int]$longformSeeds[4] }
)

foreach ($row in $familyRows) {
    $params = @{
        Family     = $row.Production
        Seed       = [int]$row.LongformSeed
        OutputRoot = (Join-Path $ProjectRoot 'artifacts\production\audiovisual_longform')
    }
    if ($Force) { $params.Force = $true }
    Invoke-C11CStep -Label "LONGFORM $($row.Key) 180s" -ScriptPath $Longform -Parameters $params
}

$drillParams = @{
    Seeds = $drillSeeds
    Families = @('tracking','saccade','pursuit','peripheral_scan')
    ResetReviewAssets = $true
}
Invoke-C11CStep -Label '20 VISUAL DRILL PHYSICAL REVIEW RENDERS' -ScriptPath $DrillReview -Parameters $drillParams

Write-Host ''
Write-Host 'C11-C RESUME COMPLETE'
Write-Host '27 Visual Loop production products: already completed; not rerun.'
Write-Host '5 production Long-form Visual Loops: PASS'
Write-Host '20 Visual Drill physical review renders: PASS'
Write-Host "Source manifest: $manifestPath"
