[CmdletBinding()]
param(
    [int]$Seed = 314159,
    [string]$OutputRoot = ''
)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
Set-Location $ProjectRoot
if ($Seed -lt 1 -or $Seed -gt 2147483646) { throw "Seed out of range: $Seed" }
if ([string]::IsNullOrWhiteSpace($OutputRoot)) {
    $stamp = Get-Date -Format 'yyyyMMdd_HHmmss'
    $OutputRoot = Join-Path $ProjectRoot "artifacts\qa\c11c_one_video_each_type\$stamp"
}
$OutputRoot = [System.IO.Path]::GetFullPath($OutputRoot)
New-Item -ItemType Directory -Force -Path $OutputRoot | Out-Null

function Invoke-C11CChild {
    param([Parameter(Mandatory=$true)][string]$Label,[Parameter(Mandatory=$true)][string]$ScriptPath,[Parameter(Mandatory=$true)][string[]]$Arguments)
    Write-Host "[C11C-SMOKE] START $Label"
    & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $ScriptPath @Arguments
    if ($LASTEXITCODE -ne 0) { throw "$Label failed with exit code $LASTEXITCODE" }
    Write-Host "[C11C-SMOKE] PASS $Label"
}

function Get-FinalMp4 {
    param([Parameter(Mandatory=$true)][string]$Root,[Parameter(Mandatory=$true)][string]$Label)
    $files = @(Get-ChildItem -LiteralPath $Root -Recurse -File -Filter '*.mp4' -ErrorAction SilentlyContinue | Where-Object { $_.Name -notlike '*_silent.mp4' })
    if ($files.Count -ne 1) { throw "$Label expected exactly 1 final MP4 under $Root; found $($files.Count)." }
    return $files[0].FullName
}

function Assert-Video {
    param([Parameter(Mandatory=$true)][string]$Path,[Parameter(Mandatory=$true)][string]$Label,[Parameter(Mandatory=$true)][double]$MinSeconds)
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) { throw "$Label output missing: $Path" }
    $ffprobe = (Get-Command ffprobe.exe -ErrorAction SilentlyContinue).Source
    if ([string]::IsNullOrWhiteSpace($ffprobe)) {
        $ffprobe = (Get-Command ffprobe -ErrorAction SilentlyContinue).Source
    }
    if ([string]::IsNullOrWhiteSpace($ffprobe)) { throw 'ffprobe is required for C11-C one-video smoke validation.' }
    $json = & $ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate -show_entries format=duration -of json -i $Path | ConvertFrom-Json
    $stream = $json.streams[0]
    if ([int]$stream.width -ne 720 -or [int]$stream.height -ne 1280) { throw "$Label resolution mismatch: $($stream.width)x$($stream.height); expected 720x1280." }
    $duration = [double]$json.format.duration
    if ($duration + 0.05 -lt $MinSeconds) { throw "$Label duration $duration is below expected minimum $MinSeconds seconds." }
    Write-Host "[C11C-SMOKE] VERIFIED $Label -> $($stream.width)x$($stream.height) / $duration s"
}

$loopRoot = Join-Path $OutputRoot '01_visual_loop'
$drillRoot = Join-Path $OutputRoot '02_visual_drill'
$longRoot = Join-Path $OutputRoot '03_longform'
New-Item -ItemType Directory -Force -Path $loopRoot,$drillRoot,$longRoot | Out-Null

Invoke-C11CChild 'Visual Loop / geometric / lattice_wave' (Join-Path $ProjectRoot 'tools\prototypes\c11c_geometric_waves_v1\run_prototype.ps1') @(
    '-Seed', [string]$Seed, '-Grammar', 'lattice_wave', '-Duration', '23', '-OutputRoot', $loopRoot, '-OutputTag', 'lattice_wave'
)
$loopMp4 = Get-FinalMp4 -Root $loopRoot -Label 'Visual Loop'
Assert-Video -Path $loopMp4 -Label 'Visual Loop' -MinSeconds 22.5

Invoke-C11CChild 'Visual Drill / tracking' (Join-Path $ProjectRoot 'tools\prototypes\c11c_bulk\run_c11c_visual_drill_review.ps1') @(
    '-Seeds', [string]$Seed, '-Families', 'tracking', '-Smoke', '-ResetReviewAssets', '-ReviewRootOverride', $drillRoot
)
$drillMp4 = Get-FinalMp4 -Root $drillRoot -Label 'Visual Drill'
Assert-Video -Path $drillMp4 -Label 'Visual Drill' -MinSeconds 26.5

Invoke-C11CChild 'Visual Longform / geometric' (Join-Path $ProjectRoot 'tools\prototypes\c11c_bulk\run_c11c_visual_loop_longform_production.ps1') @(
    '-Family', 'c11c_geometric_waves_v1', '-Seed', [string]$Seed, '-OutputRoot', $longRoot, '-Force'
)
$longMp4 = Get-FinalMp4 -Root $longRoot -Label 'Visual Longform'
Assert-Video -Path $longMp4 -Label 'Visual Longform' -MinSeconds 179.0

$report = [ordered]@{
    schema = 'C11-C-ONE-VIDEO-EACH-TYPE-SMOKE-V1'
    revision = '2.19.12'
    seed = $Seed
    status = 'PASS'
    physical_profile = '720x1280@30'
    outputs = [ordered]@{
        visual_loop = $loopMp4
        visual_drill = $drillMp4
        longform = $longMp4
    }
    generated_at = (Get-Date).ToUniversalTime().ToString('o')
}
$report | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $OutputRoot 'C11C_ONE_VIDEO_EACH_TYPE_SMOKE_REPORT.json') -Encoding UTF8
Write-Host "[C11C-SMOKE] COMPLETE PASS - 3 independent C11-C video types under $OutputRoot"
