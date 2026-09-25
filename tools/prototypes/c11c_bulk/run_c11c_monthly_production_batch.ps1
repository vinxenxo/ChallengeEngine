param(
    [Parameter(Mandatory=$false)][ValidatePattern('^\d{4}-\d{2}$')][string]$MonthId = '',
    [Parameter(Mandatory=$false)][ValidateRange(1,5)][int]$Weeks = 4,
    [Parameter(Mandatory=$false)][int[]]$Seeds = @(),
    [switch]$Force
)
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
. (Join-Path $PSScriptRoot 'C11CProductionBatchCommon.ps1')
if([string]::IsNullOrWhiteSpace($MonthId)){ $MonthId=(Get-Date).ToString('yyyy-MM') }
$WeeklySchedule=Get-C11CProductionSchedule
$Total=$WeeklySchedule.Count * $Weeks
if($Seeds.Count -eq 0){ $Seeds=New-C11CUniqueSeeds -Count $Total }
elseif($Seeds.Count -ne $Total){ throw "Monthly batch requires exactly $Total seeds when -Seeds is supplied (weeks=$Weeks)." }
if(@($Seeds|Sort-Object -Unique).Count -ne $Seeds.Count){ throw 'Monthly batch seeds must all be unique across every week.' }
Assert-C11CSeedSpacing -Seeds $Seeds
$MonthRoot=Join-Path $ProjectRoot "artifacts\batch\month\$MonthId"
if((Test-Path -LiteralPath $MonthRoot) -and -not $Force){ throw "Monthly batch already exists: $MonthRoot. Use -Force for deliberate replacement." }
if($Force -and (Test-Path -LiteralPath $MonthRoot)){ Remove-Item -LiteralPath $MonthRoot -Recurse -Force }
New-Item -ItemType Directory -Force -Path $MonthRoot | Out-Null
$allResults=@()
for($week=1;$week -le $Weeks;$week++){
    $start=($week-1)*$WeeklySchedule.Count
    $weekSeeds=@($Seeds[$start..($start+$WeeklySchedule.Count-1)])
    $weekRoot=Join-Path $MonthRoot "week$week"
    Invoke-C11CProductionBatch -Schedule $WeeklySchedule -Seeds $weekSeeds -OutputRoot $weekRoot -BatchKind 'month_week' -BatchId ("{0}/week{1}" -f $MonthId,$week)
    $weekManifest=Get-Content -Raw -LiteralPath (Join-Path $weekRoot 'batch_manifest.json') | ConvertFrom-Json
    $allResults += @($weekManifest.results)
}
$monthManifest=[ordered]@{
    schema='C11-C-MONTHLY-BATCH-MANIFEST-V1'
    revision='2.13.0'
    status='COMPLETE'
    month_id=$MonthId
    weeks=$Weeks
    products=$allResults.Count
    unique_seeds=@($Seeds|Select-Object -Unique).Count
    unique_video_keys=@($allResults | ForEach-Object { "$($_.family)|$($_.grammar)|$($_.seed)" } | Select-Object -Unique).Count
    seed_strategy='stratified_spread_random_v1'
    minimum_seed_gap=(Get-C11CMinimumSeedGap -Count $Seeds.Count)
    schedule='same 27-slot weekly pattern repeated with unique seeds per slot'
    output_root=$MonthRoot
    results=$allResults
}
[System.IO.File]::WriteAllText((Join-Path $MonthRoot 'month_manifest.json'),($monthManifest|ConvertTo-Json -Depth 12),(New-Object System.Text.UTF8Encoding($false)))
Write-Host "[C11-C-BATCH] COMPLETE MONTH $MonthId | weeks=$Weeks | products=$($allResults.Count) | root=$MonthRoot"

# C11-C 2.13.0 batch seeds use stratified_spread_random_v1 through C11CProductionBatchCommon.
