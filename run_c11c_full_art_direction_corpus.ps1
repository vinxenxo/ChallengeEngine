<#
C11-C — FULL ART DIRECTION CORPUS RUNNER

Runs the complete review/production corpus sequentially:
1) C11-C preflight validation
2) 27 Visual Loop production products (all current subtypes, weekly schedule)
3) 5 Visual Loop long-form products (one per family, 180s each)
4) 20 Visual Drill physical review renders (4 families x 5 high-spread seeds)

The script is intentionally sequential and fail-fast.
It does not modify C11-B, C7, C9, simulation truth, or frozen contracts.
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory = $false)]
    [ValidatePattern('^\d{4}$')]
    [string]$WeekId = '',

    [Parameter(Mandatory = $false)]
    [switch]$Force,

    [Parameter(Mandatory = $false)]
    [ValidateRange(1, 2147483646)]
    [int]$LongformSeedBase = 0,

    [Parameter(Mandatory = $false)]
    [switch]$SkipPreflight
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$ProjectRoot = (Resolve-Path $PSScriptRoot).Path
$BulkRoot = Join-Path $ProjectRoot 'tools\prototypes\c11c_bulk'
$Common = Join-Path $BulkRoot 'C11CProductionBatchCommon.ps1'

$Preflight = Join-Path $BulkRoot 'validate_c11c_preflight.ps1'
$Weekly = Join-Path $BulkRoot 'run_c11c_weekly_production_batch.ps1'
$Longform = Join-Path $BulkRoot 'run_c11c_visual_loop_longform_production.ps1'
$DrillReview = Join-Path $BulkRoot 'run_c11c_visual_drill_review.ps1'

foreach ($required in @($Common, $Preflight, $Weekly, $Longform, $DrillReview)) {
    if (-not (Test-Path -LiteralPath $required)) {
        throw "Required C11-C launcher missing: $required"
    }
}

. $Common

if ([string]::IsNullOrWhiteSpace($WeekId)) {
    $WeekId = (Get-Random -Minimum 1000 -Maximum 10000).ToString()
}

# Full run gets its own audit directory. Production artifacts remain in the
# canonical production tree; only the run manifest/log live here.
$RunStamp = Get-Date -Format 'yyyyMMdd_HHmmss'
$RunRoot = Join-Path $ProjectRoot "artifacts\batch\full_art_direction\${RunStamp}_week_${WeekId}"
New-Item -ItemType Directory -Force -Path $RunRoot | Out-Null
$LogPath = Join-Path $RunRoot 'full_run.log'
$ManifestPath = Join-Path $RunRoot 'full_run_manifest.json'

function Write-RunLog {
    param([Parameter(Mandatory = $true)][string]$Message)
    $line = "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') $Message"
    Write-Host $line
    Add-Content -LiteralPath $LogPath -Value $line -Encoding UTF8
}

function Invoke-C11CStep {
    param(
        [Parameter(Mandatory = $true)][string]$Label,
        [Parameter(Mandatory = $true)][string]$ScriptPath,
        [Parameter(Mandatory = $true)][hashtable]$Parameters
    )

    Write-RunLog "START $Label"
    try {
        & $ScriptPath @Parameters
        Write-RunLog "PASS  $Label"
    }
    catch {
        Write-RunLog "FAIL  $Label :: $($_.Exception.Message)"
        throw
    }
}

$drillSeeds = @(New-C11CUniqueSeeds -Count 5)
if ($drillSeeds.Count -ne 5) { throw 'Failed to allocate 5 high-spread Drill review seeds.' }
Assert-C11CSeedSpacing -Seeds $drillSeeds

if ($LongformSeedBase -eq 0) {
    $longformSeeds = @(New-C11CUniqueSeeds -Count 5)
} else {
    $longformSeeds = @(
        [int]$LongformSeedBase,
        [int][math]::Min(2147483646, $LongformSeedBase + 321456789),
        [int][math]::Min(2147483646, $LongformSeedBase + 654321987),
        [int][math]::Min(2147483646, $LongformSeedBase + 987654321),
        [int][math]::Min(2147483646, $LongformSeedBase + 1234567123)
    )
    $longformSeeds = @($longformSeeds | Select-Object -Unique)
    if ($longformSeeds.Count -ne 5) {
        $longformSeeds = @(New-C11CUniqueSeeds -Count 5)
    }
}
Assert-C11CSeedSpacing -Seeds $longformSeeds

$familyRows = @(
    @{ Key='geometric';       Production='c11c_geometric_waves_v1'; LongformSeed=[int]$longformSeeds[0] },
    @{ Key='fractal';         Production='c11c_fractal_bloom_v1'; LongformSeed=[int]$longformSeeds[1] },
    @{ Key='sacred_symmetry'; Production='c11c_sacred_symmetry_v1'; LongformSeed=[int]$longformSeeds[2] },
    @{ Key='living_particles';Production='c11c_living_particles_v1'; LongformSeed=[int]$longformSeeds[3] },
    @{ Key='invisible_forces';Production='c11c_invisible_forces_v1'; LongformSeed=[int]$longformSeeds[4] }
)

$runManifest = [ordered]@{
    schema = 'C11-C-FULL-ART-DIRECTION-CORPUS-V1'
    script = 'run_c11c_full_art_direction_corpus.ps1'
    week_id = $WeekId
    generated_at = (Get-Date).ToString('o')
    preflight = -not [bool]$SkipPreflight
    visual_loop_production = [ordered]@{
        count = 27
        output = "artifacts\batch\week\$WeekId"
    }
    longform = [ordered]@{
        count = 5
        duration_seconds = 180
        seeds = $longformSeeds
        output = 'artifacts\production\audiovisual_longform'
    }
    visual_drill_review = [ordered]@{
        count = 20
        seeds = $drillSeeds
        families = @('tracking','saccade','pursuit','peripheral_scan')
        output = 'artifacts\prototypes\c11c_visual_drills_review'
    }
}

[System.IO.File]::WriteAllText(
    $ManifestPath,
    ($runManifest | ConvertTo-Json -Depth 10),
    (New-Object System.Text.UTF8Encoding($false))
)

Write-RunLog '============================================================'
Write-RunLog 'C11-C FULL ART DIRECTION CORPUS'
Write-RunLog "WeekId=$WeekId"
Write-RunLog 'Corpus: 27 Visual Loops + 5 Long-form + 20 Visual Drills = 52 videos'
Write-RunLog "Drill review seeds: $($drillSeeds -join ', ')"
Write-RunLog "Longform seeds: $($longformSeeds -join ', ')"
Write-RunLog "Run root: $RunRoot"
Write-RunLog '============================================================'

if (-not $SkipPreflight) {
    Invoke-C11CStep -Label 'C11-C PREFLIGHT' -ScriptPath $Preflight -Parameters @{}
}

$weeklyParams = @{ WeekId = $WeekId }
if ($Force) { $weeklyParams.Force = $true }
Invoke-C11CStep -Label "27 VISUAL LOOP PRODUCTION / WEEK $WeekId" -ScriptPath $Weekly -Parameters $weeklyParams

for ($i = 0; $i -lt $familyRows.Count; $i++) {
    $row = $familyRows[$i]
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

Write-RunLog '============================================================'
Write-RunLog 'FULL ART DIRECTION CORPUS COMPLETE'
Write-RunLog '27 production Visual Loops: PASS'
Write-RunLog '5 production Long-form Visual Loops: PASS'
Write-RunLog '20 Visual Drill physical review renders: PASS'
Write-RunLog 'TOTAL: 52 videos'
Write-RunLog "Manifest: $ManifestPath"
Write-RunLog '============================================================'

Write-Host ""
Write-Host "C11-C COMPLETE CORPUS GENERATED SUCCESSFULLY"
Write-Host "WeekId: $WeekId"
Write-Host "Run manifest: $ManifestPath"