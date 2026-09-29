[CmdletBinding()]
param(
    [ValidatePattern('^CHALLENGE_[0-9]{3}$')]
    [string]$ChallengeId = 'CHALLENGE_001',
    [ValidateRange(1,2147483646)]
    [int64]$Seed = 12345
)

$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
$ProjectRoot=[IO.Path]::GetFullPath((Resolve-Path $PSScriptRoot).Path)
Set-Location $ProjectRoot

$stamp=Get-Date -Format 'yyyyMMdd_HHmmss'
$OutputRoot=Join-Path $ProjectRoot ("artifacts\qa\c11a1_challenge\single_acceptance_{0}_{1}_{2}" -f $ChallengeId,$Seed,$stamp)
$runner=Join-Path $ProjectRoot 'tools\qa\c11\run_c11a1_challenge_bulk_qa.ps1'

if(-not(Test-Path -LiteralPath $runner -PathType Leaf)){throw "C11A.1 single acceptance: runner missing: $runner"}

Write-Host '============================================================' -ForegroundColor Cyan
Write-Host '[C11A1-SINGLE] C11-A.1 single-run acceptance' -ForegroundColor Cyan
Write-Host ("[C11A1-SINGLE] Challenge={0} Seed={1}" -f $ChallengeId,$Seed)
Write-Host ("[C11A1-SINGLE] Output={0}" -f $OutputRoot)
Write-Host '[C11A1-SINGLE] Only this Challenge/seed is executed. No 54-run matrix or finalizer is invoked.' -ForegroundColor DarkYellow
Write-Host '============================================================' -ForegroundColor Cyan

powershell.exe -NoProfile -ExecutionPolicy Bypass -File $runner `
    -ProjectRoot $ProjectRoot `
    -OutputRoot $OutputRoot `
    -ChallengeId $ChallengeId `
    -SingleSeed $Seed
$exitCode=$LASTEXITCODE
if($exitCode -ne 0){throw "C11A.1 single acceptance failed with exit code $exitCode. Inspect $OutputRoot"}

$runsRoot=Join-Path $OutputRoot 'runs'
$runDirs=@(Get-ChildItem -LiteralPath $runsRoot -Directory -ErrorAction Stop)
if($runDirs.Count -ne 1){throw "C11A.1 single acceptance: expected exactly one run, found $($runDirs.Count)"}
$runDir=$runDirs[0].FullName
$recordPath=Join-Path $runDir 'run_record.json'
$record=Get-Content -LiteralPath $recordPath -Raw -Encoding UTF8 | ConvertFrom-Json

if([string]$record.status -ne 'COMPLETE'){throw "C11A.1 single acceptance: run status=$($record.status)"}
if([string]$record.challenge_id -ne $ChallengeId){throw "C11A.1 single acceptance: challenge mismatch=$($record.challenge_id)"}
if([int64]$record.test_seed -ne $Seed){throw "C11A.1 single acceptance: seed mismatch=$($record.test_seed)"}

$manifestPath=[string]$record.factory_manifest
$manifest=Get-Content -LiteralPath $manifestPath -Raw -Encoding UTF8 | ConvertFrom-Json
if([string]$manifest.status -ne 'PASS' -or [string]$manifest.qa_id -ne 'C11-A.1'){throw "C11A.1 single acceptance: adapter manifest is not PASS: $manifestPath"}
if([string]$manifest.challenge_id -ne $ChallengeId -or [int64]$manifest.seed -ne $Seed){throw 'C11A.1 single acceptance: adapter challenge/seed mismatch.'}

$expectedFrames=[int]$record.expected_timeline.total_frames
if([int]$record.video.frames -ne $expectedFrames){throw "C11A.1 single acceptance: frames=$($record.video.frames) expected=$expectedFrames"}
$expectedFps=[int]$record.expected_timeline.fps
if([string]$record.video.fps -ne ("{0}/1" -f $expectedFps)){throw "C11A.1 single acceptance: fps=$($record.video.fps) expected=${expectedFps}/1"}
if([int]$record.video.width -ne 1080 -or [int]$record.video.height -ne 1920){throw "C11A.1 single acceptance: delivery resolution=$($record.video.width)x$($record.video.height) expected 1080x1920"}

$telemetry=$manifest.telemetry
if([int64]$telemetry.initial_seed -ne $Seed){throw "C11A.1 single acceptance: telemetry initial_seed=$($telemetry.initial_seed)"}
if([int]$telemetry.total_frames -ne $expectedFrames){throw "C11A.1 single acceptance: telemetry total_frames=$($telemetry.total_frames) expected=$expectedFrames"}
if(-not [bool]$telemetry.winning_frame_in_valid_window){throw 'C11A.1 single acceptance: winning frame outside valid window.'}

$quarantines=@(Get-ChildItem -LiteralPath $ProjectRoot -Filter '.override.challenge_quarantine_*.cfg' -File -ErrorAction SilentlyContinue)
if($quarantines.Count -gt 0){throw "C11A.1 single acceptance: leaked challenge override files: $($quarantines.Name -join ', ')"}

Write-Host ("[C11A1-SINGLE] PASS - {0} seed={1} -> {2}x{3} / {4} FPS / {5} frames" -f $ChallengeId,$Seed,$record.video.width,$record.video.height,$expectedFps,$expectedFrames) -ForegroundColor Green
Write-Host ("[C11A1-SINGLE] Evidence: {0}" -f $OutputRoot)
