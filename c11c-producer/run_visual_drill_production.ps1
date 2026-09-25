param(
    [Parameter(Mandatory=$true)][ValidateSet('tracking','saccade','pursuit','peripheral_scan')][string]$Family,
    [Parameter(Mandatory=$true)][ValidateRange(1,2147483646)][int]$Seed,
    [Parameter(Mandatory=$true)][ValidateRange(1,5)][int]$DifficultyTier,
    [Parameter(Mandatory=$true)][ValidateRange(0.1,3.0)][double]$SpeedMultiplier,
    [Parameter(Mandatory=$true)][ValidateSet('constant','accelerating','pulsed')][string]$PacingMode,
    [Alias('Silent')][switch]$NoSound,
    [switch]$Force
)
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest

$ProjectRoot=(Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$CaptureScript=Join-Path $ProjectRoot 'tools\prototypes\c11c_common\C11CMovieCapture.ps1'
$AudioGenerator=Join-Path $ProjectRoot 'tools\prototypes\c11c_common\C11CSafeAmbient.py'
$PlayerScene=Join-Path $ProjectRoot 'core\presentation\rendering\VisualContentPlayer.tscn'
$VariationScript=Join-Path $ProjectRoot 'core\authoring\VisualDrillSeedVariation.gd'
$AuthoringScript=Join-Path $ProjectRoot 'core\authoring\VisualAuthoringGenerator.gd'
foreach($path in @($CaptureScript,$AudioGenerator,$PlayerScene,$VariationScript,$AuthoringScript)){ if(-not(Test-Path -LiteralPath $path)){ throw "Required backend file missing: $path" } }
. $CaptureScript

$productionRoot=Join-Path $ProjectRoot 'artifacts\production\audiovisual\visual_drills'
$familyRoot=Join-Path $productionRoot $Family
$speedTag=([math]::Round($SpeedMultiplier*100)).ToString('000')
$productId="VisualDrill_${Family}_seed_${Seed}_T${DifficultyTier}_${PacingMode}_S${speedTag}"
$productRoot=Join-Path $familyRoot $productId
if((Test-Path -LiteralPath $productRoot) -and -not $Force){ throw "Production product already exists: $productRoot. Use -Force only for deliberate replacement." }

$stageRoot=Join-Path $ProjectRoot 'artifacts\scratch\c11c_producer_drill'
$stage=Join-Path $stageRoot ([guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Force -Path $stage | Out-Null
$request=Join-Path $stage 'request.json'
$response=Join-Path $stage 'response.json'
$requestData=[ordered]@{ family=$Family; seed=$Seed; difficulty_tier=$DifficultyTier; speed_multiplier=$SpeedMultiplier; pacing_mode=$PacingMode; no_sound=[bool]$NoSound }
[System.IO.File]::WriteAllText($request,($requestData|ConvertTo-Json -Depth 8),(New-Object System.Text.UTF8Encoding($false)))

function Invoke-Checked {
    param([string]$Exe,[string[]]$Args,[string]$Label)
    Write-Host "[C11-C-PRODUCER-DRILL] $Label"
    & $Exe @Args
    $exitCode=$LASTEXITCODE
    if($exitCode -ne 0){ throw "$Label failed with exit code $exitCode" }
}
function Get-Probe {
    param([string]$Path)
    $raw=& ffprobe -v error -show_streams -show_format -of json $Path
    if($LASTEXITCODE -ne 0){ throw "ffprobe failed: $Path" }
    return (($raw -join "`n")|ConvertFrom-Json)
}
function Invoke-GodotMovieChecked {
    param([string[]]$Args,[string]$RunDir)
    $stdoutPath=Join-Path $RunDir 'godot_stdout.log'
    $stderrPath=Join-Path $RunDir 'godot_stderr.log'
    & godot @Args > $stdoutPath 2> $stderrPath
    $exitCode=$LASTEXITCODE
    $stdout=if(Test-Path -LiteralPath $stdoutPath){Get-Content -Raw -LiteralPath $stdoutPath}else{''}
    $stderr=if(Test-Path -LiteralPath $stderrPath){Get-Content -Raw -LiteralPath $stderrPath}else{''}
    $log=$stdout+"`n"+$stderr
    foreach($bad in @('SCRIPT ERROR:','Parse Error:','Compile Error:','Failed to compile depended scripts','Invalid call. Nonexistent function')){ if($log -match [regex]::Escape($bad)){ throw "Godot drill render reported $bad. See $stdoutPath / $stderrPath" } }
    if($exitCode -ne 0){ throw "Godot drill render failed: $Family seed=$Seed. See $stdoutPath / $stderrPath" }
    if($log -notmatch '\[VISUAL_CONTENT_PLAYER\] Ready \[visual_drill/'){ throw "VisualContentPlayer did not reach READY for $Family seed=$Seed. See $stdoutPath / $stderrPath" }
}
function Get-Sha { param([string]$Path); return (Get-FileHash -Algorithm SHA256 -LiteralPath $Path).Hash.ToLowerInvariant() }

$state=$null
try {
    Write-Host "[C11-C-PRODUCER-DRILL] Authoring envelope $Family seed=$Seed T$DifficultyTier speed=$SpeedMultiplier pacing=$PacingMode"
    & godot --headless --path $ProjectRoot --script 'c11c-producer/C11CVisualDrillProducerEnvelopeGenerator.gd' -- $request
    if($LASTEXITCODE -ne 0){ throw 'Visual Drill envelope generation failed.' }
    if(-not(Test-Path -LiteralPath $response)){ throw 'Visual Drill envelope generator returned no response.' }
    $resp=Get-Content -Raw -LiteralPath $response | ConvertFrom-Json
    if(-not $resp.ok){ throw "Visual Drill authoring failed: $($resp.error)" }

    $envelopePath=[string]$resp.envelope
    $authoringPath=[string]$resp.authoring
    $gameplayFrames=[int]$resp.gameplay_frames
    $gameplaySeconds=[double]$resp.duration
    $countdownFrames=90
    $ctaFrames=90
    $totalFrames=$countdownFrames+$gameplayFrames+$ctaFrames
    $totalSeconds=3.0+$gameplaySeconds+3.0

    $state=Enter-C11CMovieOverride -ProjectRoot $ProjectRoot -Width 720 -Height 1280
    $avi=Join-Path $stage "$productId.avi"
    $silent=Join-Path $stage "$productId.silent.mp4"
    $final=Join-Path $stage "$productId.mp4"
    $relativeEnvelope=$envelopePath.Substring($ProjectRoot.Length+1).Replace('\','/')

    Invoke-GodotMovieChecked @('--path','.', '--scene','core/presentation/rendering/VisualContentPlayer.tscn',"--definition=$relativeEnvelope",'--write-movie',$avi,'--fixed-fps','30','--quit-after',([string]$totalFrames)) $stage
    if(-not(Test-Path -LiteralPath $avi)){ throw "Godot did not create AVI: $avi" }
    Invoke-Checked 'ffmpeg' @('-y','-hide_banner','-loglevel','error','-i',$avi,'-an','-c:v','libx264','-preset','fast','-crf','21','-pix_fmt','yuv420p','-movflags','+faststart',$silent) 'Encode drill MP4'

    $audioProfile = switch ($Family) {
        'tracking' { 'FLOWING_VECTOR' }
        'saccade' { 'CIRCUIT_PULSE' }
        'pursuit' { 'ORGANIC_BLOOM' }
        'peripheral_scan' { 'ORBITAL_RITUAL' }
        default { throw "No FAMILY_MUSIC_V3 profile defined for $Family" }
    }
    if($NoSound){
        Move-Item -LiteralPath $silent -Destination $final -Force
    } else {
        $audio=Join-Path $stage "${productId}_music.wav"
        & python $AudioGenerator $audio $Seed 1 $totalSeconds $Family 'drill'
        $audioExitCode=$LASTEXITCODE
        if($audioExitCode -ne 0){ throw "Drill audio generation failed: exit=$audioExitCode" }
        if(-not(Test-Path -LiteralPath $audio)){ throw "Drill music WAV missing: $audio" }
        Invoke-Checked 'ffmpeg' @('-y','-hide_banner','-loglevel','error','-i',$silent,'-i',$audio,'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','128k','-ar','44100','-ac','2','-shortest','-movflags','+faststart',$final) 'Mux drill audio'
        Remove-Item -LiteralPath $silent -Force
    }

    $probe=Get-Probe $final
    $video=@($probe.streams|Where-Object {$_.codec_type -eq 'video'})|Select-Object -First 1
    if($null -eq $video){ throw "No video stream in $final" }
    if([int]$video.width -ne 720 -or [int]$video.height -ne 1280){ throw "Visual Drill delivery is not 720x1280: $($video.width)x$($video.height)" }
    if([double]$probe.format.duration -lt ($totalSeconds-0.15) -or [double]$probe.format.duration -gt ($totalSeconds+0.15)){ throw "Visual Drill duration mismatch: expected ~$totalSeconds s, got $($probe.format.duration) s" }

    if($Force -and (Test-Path -LiteralPath $productRoot)){ Remove-Item -LiteralPath $productRoot -Recurse -Force }
    New-Item -ItemType Directory -Force -Path $productRoot | Out-Null
    $finalProduct=Join-Path $productRoot "$productId.mp4"
    Copy-Item -LiteralPath $final -Destination $finalProduct -Force
    Copy-Item -LiteralPath $envelopePath -Destination (Join-Path $productRoot 'envelope.json') -Force
    Copy-Item -LiteralPath $authoringPath -Destination (Join-Path $productRoot 'authoring.json') -Force
    Copy-Item -LiteralPath (Join-Path $stage 'godot_stdout.log') -Destination (Join-Path $productRoot 'godot_stdout.log') -Force
    Copy-Item -LiteralPath (Join-Path $stage 'godot_stderr.log') -Destination (Join-Path $productRoot 'godot_stderr.log') -Force

    $sidecar=@"
TITLE: VISUAL DRILL // $Family
FAMILY: $Family
SEED: $Seed
DIFFICULTY TIER: $DifficultyTier
SPEED MULTIPLIER: $SpeedMultiplier
PACING REQUESTED: $PacingMode
RESOLUTION: 720x1280
FPS: 30
PRE_ROLL: 3.00 s
GAMEPLAY: $([math]::Round($gameplaySeconds,2)) s / $gameplayFrames frames
END CTA: 3.00 s
TOTAL: $([math]::Round($totalSeconds,2)) s / $totalFrames frames
AUDIO: $(-not $NoSound)
AUDIO MODE: $(if($NoSound){'OFF'}else{'FAMILY_MUSIC_V3'})
"@
    $social=Join-Path $productRoot "${productId}_social.txt"
    [System.IO.File]::WriteAllText($social,$sidecar,(New-Object System.Text.UTF8Encoding($false)))

    $manifest=[ordered]@{
        schema='C11-C-PRODUCER-VISUAL-DRILL-PRODUCT-V1'
        revision='0.1.1'
        backend='2.10.1'
        product_id=$productId
        family=$Family
        seed=$Seed
        difficulty_tier=$DifficultyTier
        speed_multiplier=$SpeedMultiplier
        pacing_mode_requested=$PacingMode
        resolution='720x1280'
        fps=30
        pre_roll_seconds=3.0
        gameplay_seconds=$gameplaySeconds
        end_cta_seconds=3.0
        total_duration_seconds=$totalSeconds
        total_frames=$totalFrames
        audio_enabled=(-not $NoSound)
        audio_mode=$(if($NoSound){'OFF'}else{'FAMILY_MUSIC_V3'})
        mp4=$finalProduct
        envelope=(Join-Path $productRoot 'envelope.json')
        authoring=(Join-Path $productRoot 'authoring.json')
        social=$social
        ffprobe=$probe
        mp4_sha256=(Get-Sha $finalProduct)
        variation_source=$VariationScript
        authoring_source=$AuthoringScript
    }
    [System.IO.File]::WriteAllText((Join-Path $productRoot 'production_manifest.json'),($manifest|ConvertTo-Json -Depth 14),(New-Object System.Text.UTF8Encoding($false)))

    $productText=@"
C11-C VISUAL DRILL FINAL PRODUCT
===============================
Product ID: $productId
Family: $Family
Seed: $Seed
Difficulty Tier: $DifficultyTier
Speed Multiplier: $SpeedMultiplier
Pacing Mode Requested: $PacingMode

Authoritative generation path:
VisualAuthoringGenerator.gd + VisualDrillSeedVariation.gd (C11-C 2.10.1)

Exact Producer reproduction:
.\c11c-producer\run_visual_drill_production.ps1 -Family $Family -Seed $Seed -DifficultyTier $DifficultyTier -SpeedMultiplier $SpeedMultiplier -PacingMode $PacingMode$(if($NoSound){' -NoSound'}else{''})
"@
    [System.IO.File]::WriteAllText((Join-Path $productRoot 'PRODUCT.txt'),$productText,(New-Object System.Text.UTF8Encoding($false)))
    Write-Host "[C11-C-PRODUCER-DRILL] FINAL PRODUCT PASS: $productRoot"
} finally {
    if($null -ne $state){ Exit-C11CMovieOverride -State $state }
    if(Test-Path -LiteralPath $stage){ Remove-Item -LiteralPath $stage -Recurse -Force -ErrorAction SilentlyContinue }
}
