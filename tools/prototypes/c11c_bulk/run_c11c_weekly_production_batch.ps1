param(
    [Parameter(Mandatory=$false)][ValidatePattern('^\d{4}$')][string]$WeekId = '',
    [Parameter(Mandatory=$false)][int[]]$Seeds = @(),
    [switch]$Force
)
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
. (Join-Path $PSScriptRoot 'C11CProductionBatchCommon.ps1')
$Schedule=Get-C11CProductionSchedule
if($Seeds.Count -eq 0){ $Seeds=New-C11CUniqueSeeds -Count $Schedule.Count }
elseif($Seeds.Count -ne $Schedule.Count){ throw "Weekly batch requires exactly $($Schedule.Count) seeds when -Seeds is supplied." }
if([string]::IsNullOrWhiteSpace($WeekId)){ $WeekId=(Get-Random -Minimum 1000 -Maximum 10000).ToString() }
$OutputRoot=Join-Path $ProjectRoot "artifacts\batch\week\$WeekId"
Write-Host '[C11-C-BATCH] WEEKLY PRODUCTION BATCH'
Write-Host "[C11-C-BATCH] WeekId=$WeekId | videos=$($Schedule.Count) | output=$OutputRoot"
Invoke-C11CProductionBatch -Schedule $Schedule -Seeds $Seeds -OutputRoot $OutputRoot -BatchKind 'week' -BatchId $WeekId -Force:$Force

# C11-C 2.13.0 batch seeds use stratified_spread_random_v1 through C11CProductionBatchCommon.
