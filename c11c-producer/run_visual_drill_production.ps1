param(
    [Parameter(Mandatory=$true)][ValidateSet('tracking','saccade','pursuit','peripheral_scan')][string]$Family,
    [Parameter(Mandatory=$true)][ValidateRange(1,2147483646)][int]$Seed,
    [Parameter(Mandatory=$true)][ValidateRange(1,5)][int]$DifficultyTier,
    [Parameter(Mandatory=$true)][ValidateRange(0.1,3.0)][double]$SpeedMultiplier,
    [Parameter(Mandatory=$true)][ValidateSet('constant','accelerating','pulsed')][string]$PacingMode,
    [ValidateSet('REVIEW_720','META_REELS_FINAL_V1')][string]$DeliveryProfile='REVIEW_720',
    [Alias('Silent')][switch]$NoSound,
    [switch]$Force,
    [switch]$ExportGif,
    [switch]$KeepAvi,
    [string]$OutputRoot=''
)
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
$ProjectRoot=(Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$MovieCapture=Join-Path $ProjectRoot 'tools\prototypes\c11c_common\C11CMovieCapture.ps1'
$AudioGenerator=Join-Path $ProjectRoot 'tools\prototypes\c11c_common\C11CSafeAmbient.py'
foreach($p in @($MovieCapture,$AudioGenerator,($ProjectRoot+'\c11c-producer\C11CVisualDrillProducerEnvelopeGenerator.gd'),($ProjectRoot+'\core\presentation\rendering\VisualContentPlayer.tscn'))){if(-not(Test-Path -LiteralPath $p)){throw "Required backend file missing: $p"}}
. $MovieCapture
$productionRoot=if([string]::IsNullOrWhiteSpace($OutputRoot)){Join-Path $ProjectRoot 'artifacts\production\audiovisual\visual_drills'}else{[System.IO.Path]::GetFullPath($OutputRoot)}
$familyRoot=Join-Path $productionRoot $Family
$speedTag=([math]::Round($SpeedMultiplier*100)).ToString('000')
$productId="VisualDrill_${Family}_seed_${Seed}_T${DifficultyTier}_${PacingMode}_S${speedTag}"
$productRoot=Join-Path $familyRoot $productId
if((Test-Path -LiteralPath $productRoot) -and -not $Force){throw "Production product already exists: $productRoot. Use -Force for deliberate replacement."}
$stageRoot=Join-Path $ProjectRoot 'artifacts\scratch\c11c_producer_drill'; $stage=Join-Path $stageRoot ([guid]::NewGuid().ToString('N')); New-Item -ItemType Directory -Force -Path $stage | Out-Null
$request=Join-Path $stage 'request.json'; $response=Join-Path $stage 'response.json'
[IO.File]::WriteAllText($request,([ordered]@{family=$Family;seed=$Seed;difficulty_tier=$DifficultyTier;speed_multiplier=$SpeedMultiplier;pacing_mode=$PacingMode;no_sound=[bool]$NoSound}|ConvertTo-Json -Depth 10),(New-Object Text.UTF8Encoding($false)))
function Invoke-Checked{param([string]$Exe,[string[]]$Args,[string]$Label);Write-Host "[C11-C-PRODUCER-DRILL] $Label";& $Exe @Args;if(-not $?){throw "$Label failed"}}
function Get-Probe{param([string]$Path);$raw=& ffprobe -v error -show_streams -show_format -of json $Path;if(-not $?){throw "ffprobe failed: $Path"};return (($raw -join "`n")|ConvertFrom-Json)}
try{
    & godot --headless --path $ProjectRoot --script 'c11c-producer/C11CVisualDrillProducerEnvelopeGenerator.gd' -- $request
    if(-not $?){throw 'Visual Drill envelope generation failed.'}
    if(-not(Test-Path -LiteralPath $response)){throw 'Visual Drill envelope generator returned no response.'}
    $resp=Get-Content -Raw -LiteralPath $response|ConvertFrom-Json
    if(-not $resp.ok){throw "Visual Drill authoring failed: $($resp.error)"}
    $envelopePath=[string]$resp.envelope; $authoringPath=[string]$resp.authoring; $gameplayFrames=[int]$resp.gameplay_frames; $gameplaySeconds=[double]$resp.duration
    $totalFrames=90+$gameplayFrames+90; $totalSeconds=3.0+$gameplaySeconds+3.0
    if([string]::IsNullOrWhiteSpace($OutputRoot)){}else{ }
    $width=if($DeliveryProfile -eq 'META_REELS_FINAL_V1'){1080}else{720}; $height=if($DeliveryProfile -eq 'META_REELS_FINAL_V1'){1920}else{1280}; $fps=30; $gop=90
    $state=Enter-C11CMovieOverride -ProjectRoot $ProjectRoot -Width $width -Height $height
    try{
        $avi=if($KeepAvi){Join-Path $stage ($productId+'.avi')}else{Join-Path ([IO.Path]::GetTempPath()) ($productId+'_'+[guid]::NewGuid().ToString('N')+'.avi')}
        $silent=Join-Path $stage ($productId+'.silent.mp4'); $final=Join-Path $stage ($productId+'.mp4'); $stdout=Join-Path $stage 'godot_stdout.log'; $stderr=Join-Path $stage 'godot_stderr.log'
        $relativeEnvelope=$envelopePath.Substring($ProjectRoot.Length+1).Replace('\','/')
        $args=@('--path',$ProjectRoot,'--scene','core/presentation/rendering/VisualContentPlayer.tscn',"--definition=$relativeEnvelope",'--write-movie',$avi,'--fixed-fps',([string]$fps),'--resolution',("${width}x${height}"),'--quit-after',([string]$totalFrames))
        & godot @args > $stdout 2> $stderr; if(-not $?){throw "Godot drill render failed: $Family seed=$Seed"}
        $log=(Get-Content -Raw -LiteralPath $stdout)+"`n"+(Get-Content -Raw -LiteralPath $stderr)
        foreach($bad in @('SCRIPT ERROR:','Parse Error:','Compile Error:','Failed to compile depended scripts','Invalid call. Nonexistent function')){if($log -match [regex]::Escape($bad)){throw "Godot drill reported $bad"}}
        if(-not(Test-Path -LiteralPath $avi)){throw "Godot did not create AVI: $avi"}
        & ffmpeg -y -hide_banner -loglevel error -i $avi -an -c:v libx264 -preset fast -crf 21 -profile:v high -pix_fmt yuv420p -r 30 -g 90 -keyint_min 90 -sc_threshold 0 -flags +cgop -x264-params 'open_gop=0:keyint=90:min-keyint=90:scenecut=0' -movflags +faststart $silent
        if($LASTEXITCODE -ne 0){throw 'Drill video encode failed.'}
        if($NoSound){Move-Item -LiteralPath $silent -Destination $final -Force}else{
            $audio=Join-Path $stage ($productId+'_music.wav'); & python $AudioGenerator $audio $Seed 1 $totalSeconds $Family 'drill'; if($LASTEXITCODE -ne 0){throw 'Drill audio generation failed.'}
            $bitrate=if($DeliveryProfile -eq 'META_REELS_FINAL_V1'){'192k'}else{'192k'}; $rate=if($DeliveryProfile -eq 'META_REELS_FINAL_V1'){'48000'}else{'44100'}
            & ffmpeg -y -hide_banner -loglevel error -i $silent -i $audio -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -profile:a aac_low -b:a $bitrate -ar $rate -ac 2 -shortest -movflags +faststart $final
            if($LASTEXITCODE -ne 0){throw 'Drill audio mux failed.'}
        }
        $probe=Get-Probe $final; $v=@($probe.streams|Where-Object{$_.codec_type -eq 'video'})|Select-Object -First 1
        if([int]$v.width -ne $width -or [int]$v.height -ne $height){throw "Drill output resolution mismatch: $($v.width)x$($v.height)"}
        if([math]::Abs([double]$probe.format.duration-$totalSeconds) -gt 0.15){throw "Drill duration mismatch."}
        if($Force -and(Test-Path -LiteralPath $productRoot)){Remove-Item -LiteralPath $productRoot -Recurse -Force}
        New-Item -ItemType Directory -Force -Path $productRoot|Out-Null
        Copy-Item -LiteralPath $final -Destination (Join-Path $productRoot ($productId+'.mp4')) -Force
        Copy-Item -LiteralPath $envelopePath -Destination (Join-Path $productRoot 'envelope.json') -Force
        Copy-Item -LiteralPath $authoringPath -Destination (Join-Path $productRoot 'authoring.json') -Force
        Copy-Item -LiteralPath $stdout -Destination (Join-Path $productRoot 'godot_stdout.log') -Force
        Copy-Item -LiteralPath $stderr -Destination (Join-Path $productRoot 'godot_stderr.log') -Force
        if($KeepAvi){Copy-Item -LiteralPath $avi -Destination (Join-Path $productRoot ($productId+'.avi')) -Force}
        if($ExportGif){& ffmpeg -y -hide_banner -loglevel error -i (Join-Path $productRoot ($productId+'.mp4')) -vf 'fps=24,scale=360:640:flags=lanczos,pad=360:640:(ow-iw)/2:(oh-ih)/2' -loop 0 (Join-Path $productRoot ($productId+'.gif'));if($LASTEXITCODE -ne 0){throw 'GIF export failed.'}}
        $manifest=[ordered]@{schema='C11-C-PRODUCER-VISUAL-DRILL-PRODUCT-V2';revision='2.17.0';backend='2.16.9';product_id=$productId;family=$Family;seed=$Seed;difficulty_tier=$DifficultyTier;speed_multiplier=$SpeedMultiplier;pacing_mode_requested=$PacingMode;delivery_profile=$DeliveryProfile;resolution="${width}x${height}";fps=30;pre_roll_seconds=3.0;gameplay_seconds=$gameplaySeconds;end_cta_seconds=3.0;total_duration_seconds=$totalSeconds;total_frames=$totalFrames;audio_enabled=(-not $NoSound);audio_mode=$(if($NoSound){'OFF'}else{'FAMILY_MUSIC_V4'});mp4=(Join-Path $productRoot ($productId+'.mp4'));envelope=(Join-Path $productRoot 'envelope.json');authoring=(Join-Path $productRoot 'authoring.json');ffprobe=$probe}
        [IO.File]::WriteAllText((Join-Path $productRoot 'production_manifest.json'),($manifest|ConvertTo-Json -Depth 20),(New-Object Text.UTF8Encoding($false)))
        $hook=(Get-Content -Raw $authoringPath|ConvertFrom-Json).content.hook; $tags=if($Family -eq 'tracking'){'#VisualDrill #Tracking #VisualChallenge #GenerativeArt #GodotEngine'}elseif($Family -eq 'saccade'){'#VisualDrill #Saccade #VisualChallenge #GenerativeArt #GodotEngine'}elseif($Family -eq 'pursuit'){'#VisualDrill #Pursuit #VisualChallenge #GenerativeArt #GodotEngine'}else{'#VisualDrill #PeripheralScan #VisualChallenge #GenerativeArt #GodotEngine'}
        $copy="$hook`n`n$Family - ejercicio visual procedural determinista.`n`n$tags"; $social=@('COPY_PASTE_READY:',$copy,'','TITLE:',"VISUAL DRILL // $Family",'','DESCRIPTION:',$copy,'',"HASHTAGS: $tags",''); [IO.File]::WriteAllText((Join-Path $productRoot ($productId+'_social.txt')),(($social -join "`n")+"`n"),(New-Object Text.UTF8Encoding($false)))
        Write-Host "[C11-C-PRODUCER-DRILL] FINAL PRODUCT PASS: $productRoot"
    }finally{Exit-C11CMovieOverride -State $state}
}finally{if(Test-Path -LiteralPath $stage){Remove-Item -LiteralPath $stage -Recurse -Force -ErrorAction SilentlyContinue}}
