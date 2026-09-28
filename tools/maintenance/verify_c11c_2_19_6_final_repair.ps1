[CmdletBinding()]
param()
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest

$ProjectRoot=(Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$TestPath=Join-Path $ProjectRoot 'tests\C11CParallelReviewWorkerIsolationContractTest.gd'
$BatchPath=Join-Path $ProjectRoot 'tools\prototypes\c11c_bulk\run_c11c_art_direction_batch_v4.ps1'
$WorkerPath=Join-Path $ProjectRoot 'tools\prototypes\c11c_bulk\C11CReviewWorkerIsolation.ps1'
$MoviePath=Join-Path $ProjectRoot 'tools\prototypes\c11c_common\C11CMovieCapture.ps1'
$RunAllPath=Join-Path $ProjectRoot 'tests\run_all.py'

function Read-CleanUtf8([string]$Path){
    $bytes=[System.IO.File]::ReadAllBytes($Path)
    if($bytes.Length -ge 3 -and $bytes[0] -eq 0xEF -and $bytes[1] -eq 0xBB -and $bytes[2] -eq 0xBF){throw "UTF-8 BOM is not allowed in final-repair text files: $Path"}
    $utf8=New-Object System.Text.UTF8Encoding($false,$true)
    return $utf8.GetString($bytes)
}

$test=Read-CleanUtf8 $TestPath
$batch=Read-CleanUtf8 $BatchPath
$worker=Read-CleanUtf8 $WorkerPath
$movie=Read-CleanUtf8 $MoviePath
$runall=Read-CleanUtf8 $RunAllPath

$poolPos=$batch.IndexOf('$workerPool=New-C11CReviewWorkerPool',[System.StringComparison]::Ordinal)
$capturePos=$batch.IndexOf('Start-LoopReviewJob -FamilyId',[System.StringComparison]::Ordinal)
if($poolPos -lt 0 -or $capturePos -lt 0 -or $poolPos -ge $capturePos){throw 'Worker-pool preparation ordering contract is invalid.'}

if($test.Contains('New-C11CReviewWorkerPool") < batch.find("Start-LoopReviewJob")')){throw 'Obsolete declaration-order assertion remains in the worker contract test.'}
if(-not $test.Contains('var pool_call := batch.find("$workerPool=New-C11CReviewWorkerPool")')){throw 'Final repair test must locate the pool creation call site.'}
if(-not $test.Contains('var capture_call := batch.find("Start-LoopReviewJob -FamilyId")')){throw 'Final repair test must locate the capture call site.'}
if(-not $test.Contains('_assert(pool_call < capture_call')){throw 'Final repair test must compare actual call-site positions.'}

if(-not $runall.Contains('C11CParallelReviewWorkerIsolationContractTest.gd')){throw 'Worker contract is not registered in tests/run_all.py.'}
foreach($token in @('Initialize-C11CReviewWorkerProject','global_script_class_cache.cfg','PresentationProfile','GODOT_BIN')){if(-not $worker.Contains($token)){throw "Worker bootstrap marker missing: $token"}}
if(-not $batch.Contains('MAX_OBSERVED_CONCURRENCY')){throw 'Batch concurrency telemetry contract is missing.'}
if($batch.Contains('Mutex')){throw 'Global mutex remains in Art Direction batch.'}
if($movie.Contains('System.Threading.Mutex')){throw 'Global mutex remains in Movie Maker helper.'}

$launcherFiles=Get-ChildItem -LiteralPath (Join-Path $ProjectRoot 'c11c-suite') -Recurse -File | Where-Object {$_.Extension.ToLowerInvariant() -in @('.bat','.cmd','.ps1')}
foreach($file in $launcherFiles){
    $bytes=[System.IO.File]::ReadAllBytes($file.FullName)
    if($bytes.Length -ge 3 -and $bytes[0] -eq 0xEF -and $bytes[1] -eq 0xBB -and $bytes[2] -eq 0xBF){throw "UTF-8 BOM remains in active Suite launcher: $($file.FullName)"}
    $text=[System.IO.File]::ReadAllText($file.FullName)
    if($text -match '(?i)c11c-studio' -and $file.Name -ne 'self_test.py'){throw "Active Suite launcher/dependency references retired c11c-studio: $($file.FullName)"}
}

Write-Host '[C11-C-2.19.6-FINAL-REPAIR] STATIC VERIFICATION PASS'
Write-Host "[C11-C-2.19.6-FINAL-REPAIR] pool_call=$poolPos capture_call=$capturePos"
Write-Host '[C11-C-2.19.6-FINAL-REPAIR] active c11c-suite .BAT/.CMD/.PS1: no c11c-studio dependency'
