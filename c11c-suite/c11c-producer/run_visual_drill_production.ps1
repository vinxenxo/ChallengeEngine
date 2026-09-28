[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)][ValidateSet('tracking','saccade','pursuit','peripheral_scan')][string]$Family,
    [Parameter(Mandatory=$true)][ValidateRange(1,2147483646)][int]$Seed,
    [Parameter(Mandatory=$true)][ValidateRange(1,5)][int]$DifficultyTier,
    [Parameter(Mandatory=$true)][ValidateRange(0.1,3.0)][double]$SpeedMultiplier,
    [Parameter(Mandatory=$true)][ValidateSet('constant','accelerating','pulsed')][string]$PacingMode,
    [ValidateSet('MASTER_1080','REVIEW_720','MIN_540','META_REELS_FINAL_V1','LONGFORM_1080')][string]$DeliveryProfile='REVIEW_720',
    [Alias('Silent')][switch]$NoSound,
    [switch]$Force,
    [switch]$ExportGif,
    [string]$OutputRoot=''
)
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
$ProjectRoot=(Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
function Resolve-DeliveryProfileData {
    param([Parameter(Mandatory=$true)]$Config,[Parameter(Mandatory=$true)][string]$ProfileId)
    $profiles=$Config.profiles
    $current=$ProfileId
    $seen=@{}
    while($true){
        if($seen.ContainsKey($current)){throw "Delivery profile alias cycle: $ProfileId -> $current"}
        $seen[$current]=$true
        $prop=$profiles.PSObject.Properties[$current]
        if(-not $prop){throw "Unknown delivery profile in central configuration: $current"}
        $profile=$prop.Value
        if($profile.PSObject.Properties.Name -contains 'alias_of'){
            $current=[string]$profile.alias_of
            continue
        }
        return $profile
    }
}

$MovieCapture=Join-Path $ProjectRoot 'tools\prototypes\c11c_common\C11CMovieCapture.ps1'
$AudioGenerator=Join-Path $ProjectRoot 'tools\prototypes\c11c_common\C11CSafeAmbient.py'
foreach($p in @($MovieCapture,$AudioGenerator,($ProjectRoot+'\c11c-suite\c11c-producer\C11CVisualDrillProducerEnvelopeGenerator.gd'),($ProjectRoot+'\core\presentation\rendering\VisualContentPlayer.tscn'))){if(-not(Test-Path -LiteralPath $p)){throw "Required backend file missing: $p"}}
. $MovieCapture
$productionRoot=if([string]::IsNullOrWhiteSpace($OutputRoot)){Join-Path $ProjectRoot 'artifacts\production\audiovisual\visual_drills'}else{[System.IO.Path]::GetFullPath($OutputRoot)}
$familyRoot=Join-Path $productionRoot $Family
$speedTag=([math]::Round($SpeedMultiplier*100)).ToString('000')
$baseProductId="VisualDrill_${Family}_seed_${Seed}_T${DifficultyTier}_${PacingMode}_S${speedTag}"
$profileSuffix=if($DeliveryProfile -eq 'REVIEW_720'){''}else{"_$DeliveryProfile"}
$productId="$baseProductId$profileSuffix"
$productRoot=Join-Path $familyRoot $productId
if((Test-Path -LiteralPath $productRoot) -and -not $Force){throw "Production product already exists: $productRoot. Use -Force for deliberate replacement."}
$stageRoot=Join-Path $ProjectRoot 'artifacts\scratch\c11c_producer_drill'; $stage=Join-Path $stageRoot ([guid]::NewGuid().ToString('N')); New-Item -ItemType Directory -Force -Path $stage | Out-Null
$request=Join-Path $stage 'request.json'; $response=Join-Path $stage 'response.json'
[IO.File]::WriteAllText($request,([ordered]@{family=$Family;seed=$Seed;difficulty_tier=$DifficultyTier;speed_multiplier=$SpeedMultiplier;pacing_mode=$PacingMode;no_sound=[bool]$NoSound}|ConvertTo-Json -Depth 10),(New-Object Text.UTF8Encoding($false)))
function Invoke-GodotUserArgProcess{
    param(
        [Parameter(Mandatory=$true)][string]$Executable,
        [Parameter(Mandatory=$true)][string[]]$Arguments,
        [Parameter(Mandatory=$true)][string]$WorkingDirectory,
        [Parameter(Mandatory=$true)][string]$StdoutPath,
        [Parameter(Mandatory=$true)][string]$StderrPath
    )
    $psi=[Diagnostics.ProcessStartInfo]::new()
    $psi.FileName=$Executable
    $psi.WorkingDirectory=$WorkingDirectory
    $psi.UseShellExecute=$false
    $psi.CreateNoWindow=$true
    $psi.RedirectStandardOutput=$true
    $psi.RedirectStandardError=$true
    $quoted=foreach($arg in $Arguments){
        if($arg -notmatch '[\s"]'){$arg;continue}
        '"' + (($arg -replace '(\\*)"','$1$1\"') -replace '(\\+)$','$1$1') + '"'
    }
    $psi.Arguments=$quoted -join ' '
    $process=[Diagnostics.Process]::new()
    $process.StartInfo=$psi
    [void]$process.Start()
    $stdout=$process.StandardOutput.ReadToEndAsync()
    $stderr=$process.StandardError.ReadToEndAsync()
    $process.WaitForExit()
    $outText=$stdout.Result
    $errText=$stderr.Result
    [IO.File]::WriteAllText($StdoutPath,$outText,[Text.UTF8Encoding]::new($false))
    [IO.File]::WriteAllText($StderrPath,$errText,[Text.UTF8Encoding]::new($false))
    return [pscustomobject]@{ExitCode=$process.ExitCode;Stdout=$outText;Stderr=$errText}
}
function Invoke-Checked{param([string]$Exe,[string[]]$Args,[string]$Label);Write-Host "[C11-C-PRODUCER-DRILL] $Label";& $Exe @Args;if(-not $?){throw "$Label failed"}}
function Get-Probe{param([string]$Path);$raw=& ffprobe -v error -show_streams -show_format -of json $Path;if(-not $?){throw "ffprobe failed: $Path"};return (($raw -join "`n")|ConvertFrom-Json)}
function Wait-ForStableFile {
    param(
        [Parameter(Mandatory=$true)][string]$Path,
        [Parameter(Mandatory=$true)][string]$Label,
        [int]$TimeoutSeconds=90
    )
    $deadline=(Get-Date).AddSeconds($TimeoutSeconds)
    $lastSize=-1L
    $stableSamples=0
    while((Get-Date) -lt $deadline){
        if(Test-Path -LiteralPath $Path -PathType Leaf){
            $item=Get-Item -LiteralPath $Path
            $size=[int64]$item.Length
            if($size -gt 0){
                if($size -eq $lastSize){$stableSamples++}else{$stableSamples=0;$lastSize=$size}
                if($stableSamples -ge 2){return}
            }
        }
        Start-Sleep -Milliseconds 400
    }
    throw "$Label was not created/stabilized within ${TimeoutSeconds}s: $Path"
}
try{
    $generatorStdout=Join-Path $stage 'generator_stdout.log'
    $generatorStderr=Join-Path $stage 'generator_stderr.log'
    $godotExecutable = if($env:GODOT_BIN){$env:GODOT_BIN}else{'godot'}
    $generatorScript=[IO.Path]::GetFullPath((Join-Path $ProjectRoot 'c11c-suite\c11c-producer\C11CVisualDrillProducerEnvelopeGenerator.gd'))
    $generatorResult=Invoke-GodotUserArgProcess -Executable $godotExecutable -WorkingDirectory $ProjectRoot `
        -Arguments @('--headless','--path',$ProjectRoot,'--script',$generatorScript,'--',$request) `
        -StdoutPath $generatorStdout -StderrPath $generatorStderr
    if($generatorResult.ExitCode -ne 0){
        throw "Visual Drill envelope generation failed (exit=$($generatorResult.ExitCode)). See $generatorStdout and $generatorStderr."
    }
    if(-not(Test-Path -LiteralPath $response)){
        throw "Visual Drill envelope generator returned no response. See $generatorStdout and $generatorStderr."
    }
    $resp=Get-Content -Raw -LiteralPath $response|ConvertFrom-Json
    if(-not $resp.ok){throw "Visual Drill authoring failed: $($resp.error)"}
    $envelopePath=[string]$resp.envelope; $authoringPath=[string]$resp.authoring; $gameplayFrames=[int]$resp.gameplay_frames; $gameplaySeconds=[double]$resp.duration
    $totalFrames=90+$gameplayFrames+90; $totalSeconds=3.0+$gameplaySeconds+3.0

    # C11-C review capture remains the proven 720x1280 envelope. Delivery scaling happens afterwards.
    $sourceWidth=720; $sourceHeight=1280; $fps=30; $gop=90
    $state=Enter-C11CMovieOverride -ProjectRoot $ProjectRoot -Width $sourceWidth -Height $sourceHeight
    try{
        # Use the same Godot Movie Maker invocation pattern already proven by the C11-C review runner.
        # AVI is only a temporary intermediate; the Producer never exposes or retains it as a product.
        $avi=Join-Path $stage ($baseProductId+'.avi')
        $sourceSilent=Join-Path $stage ($baseProductId+'.source.silent.mp4'); $finalSource=Join-Path $stage ($baseProductId+'.source.mp4'); $finalDelivery=Join-Path $stage ($productId+'.mp4'); $stdout=Join-Path $stage 'godot_stdout.log'; $stderr=Join-Path $stage 'godot_stderr.log'
        $relativeEnvelope=$envelopePath.Substring($ProjectRoot.Length+1).Replace('\','/')
        $movieArgs=@('--path','.','--scene','core/presentation/rendering/VisualContentPlayer.tscn',"--definition=$relativeEnvelope",'--write-movie',$avi,'--fixed-fps',([string]$fps),'--quit-after',([string]$totalFrames))
        $movieProcess=Start-Process -FilePath $godotExecutable -ArgumentList $movieArgs -Wait -PassThru -NoNewWindow -RedirectStandardOutput $stdout -RedirectStandardError $stderr
        $log=(Get-Content -Raw -LiteralPath $stdout)+"`n"+(Get-Content -Raw -LiteralPath $stderr)
        foreach($bad in @('SCRIPT ERROR:','Parse Error:','Compile Error:','Failed to compile depended scripts','Invalid call. Nonexistent function')){if($log -match [regex]::Escape($bad)){throw "Godot drill reported $bad"}}
        if($movieProcess.ExitCode -ne 0){throw "Godot drill render failed: $Family seed=$Seed exit=$($movieProcess.ExitCode). See $stdout and $stderr."}
        $reportedMovie=[regex]::Match($log,'(?m)^Done recording movie at path:\s*(?<path>.+)$')
        if($reportedMovie.Success){
            $reportedPath=$reportedMovie.Groups['path'].Value.Trim()
            if((Test-Path -LiteralPath $reportedPath -PathType Leaf) -and $reportedPath -ne $avi){$avi=$reportedPath}
        }
        Wait-ForStableFile -Path $avi -Label "Godot Movie Maker AVI capture"
        # Release the project-global override immediately after Godot capture.
        Exit-C11CMovieOverride -State $state
        $state = $null
        & ffmpeg -y -hide_banner -loglevel error -i $avi -an -c:v libx264 -preset fast -crf 21 -profile:v high -pix_fmt yuv420p -r 30 -g 90 -keyint_min 90 -sc_threshold 0 -flags +cgop -x264-params 'open_gop=0:keyint=90:min-keyint=90:scenecut=0' $sourceSilent
        if($LASTEXITCODE -ne 0){throw 'Drill source video encode from AVI failed.'}
        if($NoSound){Move-Item -LiteralPath $sourceSilent -Destination $finalSource -Force}else{
            $audio=Join-Path $stage ($baseProductId+'_music.wav'); & python $AudioGenerator $audio $Seed 1 $totalSeconds $Family 'drill'; if($LASTEXITCODE -ne 0){throw 'Drill audio generation failed.'}
            & ffmpeg -y -hide_banner -loglevel error -i $sourceSilent -i $audio -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -profile:a aac_low -b:a 192k -ar 48000 -ac 2 -shortest -movflags +faststart $finalSource
            if($LASTEXITCODE -ne 0){throw 'Drill source audio mux failed.'}
        }

        $deliveryConfigPath=Join-Path $ProjectRoot 'profiles\delivery\c11c_video_delivery_profiles.json'
        if(-not(Test-Path -LiteralPath $deliveryConfigPath)){throw "Delivery profile configuration missing: $deliveryConfigPath"}
        $deliveryConfig=Get-Content -Raw -LiteralPath $deliveryConfigPath|ConvertFrom-Json
        $deliveryProfileData=Resolve-DeliveryProfileData -Config $deliveryConfig -ProfileId $DeliveryProfile
        if(-not $deliveryProfileData.width -or -not $deliveryProfileData.height){throw "Delivery profile lacks dimensions: $DeliveryProfile"}
        $deliveryWidth=[int]$deliveryProfileData.width; $deliveryHeight=[int]$deliveryProfileData.height; $deliveryRate=[int]$deliveryProfileData.audio_sample_rate_hz; $deliveryFps=if($deliveryProfileData.PSObject.Properties.Name -contains 'fps'){[int]$deliveryProfileData.fps}else{30}
        $deliveryEncoder=if($deliveryProfileData.PSObject.Properties.Name -contains 'encoder'){[string]$deliveryProfileData.encoder}else{'libx264'}
        $deliveryPreset=if($deliveryProfileData.PSObject.Properties.Name -contains 'preset'){[string]$deliveryProfileData.preset}else{'fast'}
        $deliveryCrf=if($deliveryProfileData.PSObject.Properties.Name -contains 'crf'){[int]$deliveryProfileData.crf}else{18}
        $deliveryGopFrames=if($deliveryProfileData.PSObject.Properties.Name -contains 'gop_frames'){[int]$deliveryProfileData.gop_frames}else{[int]([math]::Round($deliveryFps*3))}
        if($deliveryFps -lt 24 -or $deliveryFps -gt 60){throw "Delivery profile FPS outside 24..60: $DeliveryProfile fps=$deliveryFps"}
        if($DeliveryProfile -eq 'REVIEW_720'){Copy-Item -LiteralPath $finalSource -Destination $finalDelivery -Force}
        else{
            $ff=@('-y','-hide_banner','-loglevel','error','-i',$finalSource,'-vf',"scale=${deliveryWidth}:${deliveryHeight}:flags=lanczos",'-c:v',$deliveryEncoder,'-preset',$deliveryPreset,'-crf',[string]$deliveryCrf,'-pix_fmt','yuv420p','-r',[string]$deliveryFps,'-g',[string]$deliveryGopFrames,'-keyint_min',[string]$deliveryGopFrames,'-sc_threshold','0','-flags','+cgop','-x264-params',('open_gop=0:keyint={0}:min-keyint={0}:scenecut=0' -f $deliveryGopFrames))
            if($NoSound){$ff+=@('-an')}else{$ff+=@('-c:a','aac','-profile:a','aac_low','-b:a','192k','-ar',[string]$deliveryRate,'-ac','2')}
            $ff += $finalDelivery
            & ffmpeg @ff
            if($LASTEXITCODE -ne 0){throw "Drill delivery encode failed: $DeliveryProfile"}
        }
        $probe=Get-Probe $finalDelivery; $v=@($probe.streams|Where-Object{$_.codec_type -eq 'video'})|Select-Object -First 1
        if([int]$v.width -ne $deliveryWidth -or [int]$v.height -ne $deliveryHeight){throw "Drill output resolution mismatch: $($v.width)x$($v.height)"}
        if([math]::Abs([double]$probe.format.duration-$totalSeconds) -gt 0.15){throw "Drill duration mismatch."}
        if($Force -and(Test-Path -LiteralPath $productRoot)){Remove-Item -LiteralPath $productRoot -Recurse -Force}
        New-Item -ItemType Directory -Force -Path $productRoot|Out-Null
        Copy-Item -LiteralPath $finalDelivery -Destination (Join-Path $productRoot ($productId+'.mp4')) -Force
        Copy-Item -LiteralPath $envelopePath -Destination (Join-Path $productRoot 'envelope.json') -Force
        Copy-Item -LiteralPath $authoringPath -Destination (Join-Path $productRoot 'authoring.json') -Force
        Copy-Item -LiteralPath $stdout -Destination (Join-Path $productRoot 'godot_stdout.log') -Force
        Copy-Item -LiteralPath $stderr -Destination (Join-Path $productRoot 'godot_stderr.log') -Force
        if($ExportGif){& ffmpeg -y -hide_banner -loglevel error -i (Join-Path $productRoot ($productId+'.mp4')) -vf 'fps=24,scale=360:640:flags=lanczos,pad=360:640:(ow-iw)/2:(oh-ih)/2' -loop 0 (Join-Path $productRoot ($productId+'.gif'));if($LASTEXITCODE -ne 0){throw 'GIF export failed.'}}
        $manifest=[ordered]@{schema='C11-C-PRODUCER-VISUAL-DRILL-PRODUCT-V3';revision='2.19.1';backend='2.16.9';product_id=$productId;family=$Family;seed=$Seed;difficulty_tier=$DifficultyTier;speed_multiplier=$SpeedMultiplier;pacing_mode_requested=$PacingMode;delivery_profile=$DeliveryProfile;source_capture_resolution="${sourceWidth}x${sourceHeight}";source_capture_format='temporary_avi';resolution="${deliveryWidth}x${deliveryHeight}";fps=30;pre_roll_seconds=3.0;gameplay_seconds=$gameplaySeconds;end_cta_seconds=3.0;total_duration_seconds=$totalSeconds;total_frames=$totalFrames;audio_enabled=(-not $NoSound);audio_mode=$(if($NoSound){'OFF'}else{'FAMILY_MUSIC_V4'});audio_sample_rate_hz=$(if($NoSound){0}else{$deliveryRate});audio_channels=$(if($NoSound){0}else{2});mp4=(Join-Path $productRoot ($productId+'.mp4'));envelope=(Join-Path $productRoot 'envelope.json');authoring=(Join-Path $productRoot 'authoring.json');ffprobe=$probe}
        [IO.File]::WriteAllText((Join-Path $productRoot 'production_manifest.json'),($manifest|ConvertTo-Json -Depth 20),(New-Object Text.UTF8Encoding($false)))
        $hookDataPath=Join-Path $ProjectRoot 'profiles\presentation\c11c_visual_hooks.json'; if(-not(Test-Path -LiteralPath $hookDataPath)){throw "Visual hook bank missing: $hookDataPath"}; $hookData=Get-Content -Raw -LiteralPath $hookDataPath|ConvertFrom-Json; $hookEntry=$hookData.visual_drills.$Family; if($null -eq $hookEntry){throw "No Visual Drill hook bank for family: $Family"}; $hooks=@($hookEntry.hooks); if($hooks.Count -ne 10){throw "Visual Drill hook bank for $Family must contain exactly 10 hooks: got $($hooks.Count)"}; $hookIndex=(($Seed+[int]$hookEntry.family_offset)%$hooks.Count+$hooks.Count)%$hooks.Count; $hook=[string]$hooks[$hookIndex]; $tags=if($Family -eq 'tracking'){'#VisualDrill #Tracking #VisualChallenge #GenerativeArt #GodotEngine'}elseif($Family -eq 'saccade'){'#VisualDrill #Saccade #VisualChallenge #GenerativeArt #GodotEngine'}elseif($Family -eq 'pursuit'){'#VisualDrill #Pursuit #VisualChallenge #GenerativeArt #GodotEngine'}else{'#VisualDrill #PeripheralScan #VisualChallenge #GenerativeArt #GodotEngine'}
        $copy="$hook`n`n$Family - ejercicio visual procedural determinista.`n`n$tags"; $social=@('COPY_PASTE_READY:',$copy,'','TITLE:',"VISUAL DRILL // $Family",'','DESCRIPTION:',$copy,'',"HASHTAGS: $tags",''); [IO.File]::WriteAllText((Join-Path $productRoot ($productId+'_social.txt')),(($social -join "`n")+"`n"),(New-Object Text.UTF8Encoding($false)))
        Write-Host "[C11-C-PRODUCER-DRILL] FINAL PRODUCT PASS: $productRoot"
    }finally{if($null -ne $state){Exit-C11CMovieOverride -State $state}}
}finally{if(Test-Path -LiteralPath $stage){Remove-Item -LiteralPath $stage -Recurse -Force -ErrorAction SilentlyContinue}}
