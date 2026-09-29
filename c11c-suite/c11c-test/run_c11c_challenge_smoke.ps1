[CmdletBinding()]
param(
    [ValidatePattern('^CHALLENGE_[0-9]{3}$')][string]$ChallengeId='CHALLENGE_001',
    [ValidateRange(1,2147483646)][int]$Seed=24681357,
    [ValidateSet('MASTER_1080','REVIEW_720','MIN_540')][string]$DeliveryProfile='REVIEW_720',
    [switch]$AllCanonical
)
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
$ProjectRoot=(Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
Set-Location $ProjectRoot

function Read-Json([string]$Path){
    Get-Content -Raw -LiteralPath $Path -Encoding UTF8 | ConvertFrom-Json
}
function Assert-Equal([object]$Actual,[object]$Expected,[string]$Label){
    if($Actual -ne $Expected){throw "${Label}: actual=$Actual expected=$Expected"}
}
function Probe-Video([string]$Path){
    $raw=& ffprobe -v error -count_frames -show_streams -show_format -of json -- $Path 2>&1
    if($LASTEXITCODE -ne 0){throw "ffprobe failed: $Path`n$($raw -join "`n")"}
    (($raw -join "`n")|ConvertFrom-Json)
}
function Test-OverrideIntegrity([string]$Path,[bool]$WasPresent,[string]$BeforeHash,[string]$Label){
    $afterPresent=Test-Path -LiteralPath $Path -PathType Leaf
    if($WasPresent -ne $afterPresent){throw "${Label} override.cfg presence changed."}
    if($WasPresent){
        $afterHash=(Get-FileHash -Algorithm SHA256 -LiteralPath $Path).Hash
        if($afterHash -ne $BeforeHash){throw "${Label} override.cfg hash changed: before=$BeforeHash after=$afterHash"}
    }
    $leaks=@(Get-ChildItem -LiteralPath $ProjectRoot -Filter '.override.challenge_quarantine_*.cfg' -File -ErrorAction SilentlyContinue)
    if($leaks.Count -ne 0){throw "${Label} override quarantine leak detected: $($leaks.Name -join ', ')"}
}

$overridePath=Join-Path $ProjectRoot 'override.cfg'
$overrideWasPresent=Test-Path -LiteralPath $overridePath -PathType Leaf
$overrideBeforeHash=if($overrideWasPresent){(Get-FileHash -Algorithm SHA256 -LiteralPath $overridePath).Hash}else{''}

if($AllCanonical){
    $ids=@(Get-ChildItem -LiteralPath (Join-Path $ProjectRoot 'challenges') -File -ErrorAction Stop |
        Where-Object { $_.Extension -ieq '.json' -and $_.BaseName -match '^CHALLENGE_[0-9]{3}$' } |
        Sort-Object Name |
        Select-Object -ExpandProperty BaseName)
}else{
    $ids=@($ChallengeId)
}
if($ids.Count -lt 1){throw 'No challenge selected.'}

$stamp=Get-Date -Format 'yyyyMMdd_HHmmss'
$runRoot=Join-Path $ProjectRoot "artifacts\qa\c11c_challenge_smoke\$stamp"
New-Item -ItemType Directory -Force -Path $runRoot | Out-Null
$runner=Join-Path $ProjectRoot 'tools\prototypes\c11c_bulk\run_c11c_challenge_production.ps1'
$results=@()

try{
    foreach($id in $ids){
        Write-Host "[C11C-CHALLENGE-SMOKE] START $id seed=$Seed profile=$DeliveryProfile"
        $cfg=Read-Json (Join-Path $ProjectRoot "challenges\$id.json")
        Assert-Equal ([string]$cfg.challenge_id) $id "${id} challenge_id"
        $fps=[int]$cfg.video.fps
        $totalSeconds=0.0
        foreach($key in @('hook_duration','game_duration','cta_duration')){$totalSeconds += [double]$cfg.video.$key}
        $revealProperty=$cfg.video.PSObject.Properties['reveal_duration']
        if($null -ne $revealProperty){$totalSeconds += [double]$revealProperty.Value}
        $expectedFrames=[int][math]::Round($totalSeconds*$fps)
        $outputRoot=Join-Path $runRoot $id

        & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $runner -ChallengeId $id -Seed $Seed -DeliveryProfile $DeliveryProfile -OutputRoot $outputRoot -NoSound -Force
        if($LASTEXITCODE -ne 0){throw "${id} production failed with exit code $LASTEXITCODE"}

        $productRoot=Join-Path $outputRoot $id
        $mp4=Join-Path $productRoot "${id}_seed_${Seed}.mp4"
        $manifestPath=Join-Path $productRoot 'production_manifest.json'
        if(-not(Test-Path -LiteralPath $mp4 -PathType Leaf)){throw "${id} final MP4 missing: $mp4"}
        if(-not(Test-Path -LiteralPath $manifestPath -PathType Leaf)){throw "${id} production manifest missing: $manifestPath"}
        $manifest=Read-Json $manifestPath

        $deliveryWidth=if($DeliveryProfile -eq 'REVIEW_720'){720}elseif($DeliveryProfile -eq 'MIN_540'){540}else{1080}
        $deliveryHeight=if($DeliveryProfile -eq 'REVIEW_720'){1280}elseif($DeliveryProfile -eq 'MIN_540'){960}else{1920}
        Assert-Equal ([string]$manifest.source_movie_resolution) '540x960' "${id} source movie resolution"
        Assert-Equal ([string]$manifest.delivery_resolution) "${deliveryWidth}x${deliveryHeight}" "${id} delivery resolution"
        Assert-Equal ([int]$manifest.fps) $fps "${id} manifest FPS"
        Assert-Equal ([bool]$manifest.audio_present) $false "${id} manifest audio_present"

        $probe=Probe-Video $mp4
        $video=@($probe.streams|Where-Object{$_.codec_type -eq 'video'})|Select-Object -First 1
        $audio=@($probe.streams|Where-Object{$_.codec_type -eq 'audio'})
        if($null -eq $video){throw "${id} final MP4 has no video stream."}
        Assert-Equal ([int]$video.width) $deliveryWidth "${id} width"
        Assert-Equal ([int]$video.height) $deliveryHeight "${id} height"
        Assert-Equal ([string]$video.r_frame_rate) ("{0}/1" -f $fps) "${id} FPS"
        Assert-Equal ([int]$video.nb_read_frames) $expectedFrames "${id} frame count"
        if([math]::Abs([double]$video.duration-$totalSeconds) -gt 0.10){throw "${id} duration: actual=$($video.duration) expected=$totalSeconds"}
        if($audio.Count -ne 0){throw "${id} must remain video-only; final audio streams=$($audio.Count)"}
        if([string]$video.codec_name -ne 'h264'){throw "${id} codec mismatch: $($video.codec_name)"}
        if([string]$video.pix_fmt -notin @('yuv420p','yuvj420p')){throw "${id} pixel format mismatch: $($video.pix_fmt)"}

        $results += [pscustomobject]@{challenge_id=$id;seed=$Seed;fps=$fps;frames=$expectedFrames;duration_seconds=$totalSeconds;mp4=$mp4;status='PASS'}
        Write-Host "[C11C-CHALLENGE-SMOKE] PASS $id -> ${deliveryWidth}x${deliveryHeight} / $fps FPS / $expectedFrames frames / video-only"
    }
    $report=[ordered]@{schema='C11-C-CHALLENGE-SMOKE-V1';revision='2.19.12';seed=$Seed;delivery_profile=$DeliveryProfile;all_canonical=$AllCanonical.IsPresent;count=$results.Count;results=$results;generated_at_utc=[DateTimeOffset]::UtcNow.ToString('o')}
    $reportPath=Join-Path $runRoot 'C11C_CHALLENGE_SMOKE_REPORT.json'
    [IO.File]::WriteAllText($reportPath,($report|ConvertTo-Json -Depth 10),(New-Object Text.UTF8Encoding($false)))
    Test-OverrideIntegrity $overridePath $overrideWasPresent $overrideBeforeHash 'C11C Challenge Smoke'
    Write-Host "[C11C-CHALLENGE-SMOKE] COMPLETE PASS - $($results.Count) challenge product(s)"
    Write-Host "[C11C-CHALLENGE-SMOKE] REPORT: $reportPath"
}catch{
    try{Test-OverrideIntegrity $overridePath $overrideWasPresent $overrideBeforeHash 'C11C Challenge Smoke'}catch{Write-Error $_}
    throw
}
