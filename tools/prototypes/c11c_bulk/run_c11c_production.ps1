[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)]
    [ValidateSet('c11c_geometric_waves_v1','c11c_fractal_bloom_v1','c11c_sacred_symmetry_v1','c11c_living_particles_v1','c11c_invisible_forces_v1')]
    [string]$Family,
    [Parameter(Mandatory=$true)]
    [ValidateRange(1,2147483646)]
    [int]$Seed,
    [Parameter(Mandatory=$false)]
    [string]$Grammar = '',
    [ValidateRange(20.0,23.0)]
    [double]$Duration = 0.0,
    [Alias('Silent')][switch]$NoSound,
    [switch]$NoFooter,
    [switch]$ExportGif,
    [switch]$KeepAvi,
    [ValidateSet('MASTER_1080','REVIEW_720','MIN_540','META_REELS_FINAL_V1','LONGFORM_1080')]
    [string]$DeliveryProfile = 'REVIEW_720',
    [switch]$Force
)
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
$ProjectRoot=(Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
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

$launcher=Join-Path $ProjectRoot ("tools\prototypes\$Family\run_prototype.ps1")
if (-not (Test-Path -LiteralPath $launcher)) { throw "Prototype launcher not found: $launcher" }
$prefixMap=@{
    c11c_geometric_waves_v1='GeometricWaves_v1'
    c11c_fractal_bloom_v1='FractalBloom_v1'
    c11c_sacred_symmetry_v1='SacredSymmetry_v1'
    c11c_living_particles_v1='LivingParticles_v1'
    c11c_invisible_forces_v1='InvisibleForces_v1'
}
$baseProductId="$($prefixMap[$Family])_seed_$Seed"
$profileSuffix=if($DeliveryProfile -eq 'REVIEW_720'){''}else{"_$DeliveryProfile"}
$productId="$baseProductId$profileSuffix"
$productionRoot=Join-Path $ProjectRoot 'artifacts\production\audiovisual'
$productRoot=Join-Path (Join-Path $productionRoot $Family) $productId
if ((Test-Path -LiteralPath $productRoot) -and -not $Force) {
    throw "Production product already exists: $productRoot. Use -Force only for deliberate replacement."
}
Write-Host '[C11-C-PRODUCTION] =========================================='
Write-Host "[C11-C-PRODUCTION] Family=$Family Seed=$Seed Product=$productId Delivery=$DeliveryProfile"

$launcherParams=@{Seed=[int]$Seed}
if(-not [string]::IsNullOrWhiteSpace($Grammar)){$launcherParams.Grammar=$Grammar}
if($NoSound){$launcherParams.NoSound=$true}
if($NoFooter){$launcherParams.NoFooter=$true}
if($ExportGif){$launcherParams.ExportGif=$true}
if($KeepAvi){$launcherParams.KeepAvi=$true}
if($Duration -gt 0){$launcherParams.Duration=$Duration}
& $launcher @launcherParams
if (-not $?) { throw 'Prototype generation failed.' }

$stage=Join-Path $ProjectRoot ("artifacts\prototypes\$Family")
$requiredBase=@(
    "$baseProductId.mp4",
    "${baseProductId}_social.txt",
    "${baseProductId}_manifest.json",
    "${baseProductId}_authoring.json",
    "${baseProductId}_ffprobe.json",
    "${baseProductId}_godot.log"
)
foreach ($name in $requiredBase) {
    if (-not (Test-Path -LiteralPath (Join-Path $stage $name))) { throw "Required production artifact missing: $name" }
}
$sourceMp4=Join-Path $stage "$baseProductId.mp4"
$finalMp4=Join-Path $stage "$productId.mp4"
$deliveryConfigPath=Join-Path $ProjectRoot 'profiles\delivery\c11c_video_delivery_profiles.json'
if(-not (Test-Path -LiteralPath $deliveryConfigPath)){throw "Delivery profile configuration missing: $deliveryConfigPath"}
$deliveryConfig=Get-Content -Raw -LiteralPath $deliveryConfigPath|ConvertFrom-Json
$deliveryProfileData=Resolve-DeliveryProfileData -Config $deliveryConfig -ProfileId $DeliveryProfile
if(-not $deliveryProfileData.width -or -not $deliveryProfileData.height){throw "Delivery profile lacks dimensions: $DeliveryProfile"}
$deliveryWidth=[int]$deliveryProfileData.width
$deliveryHeight=[int]$deliveryProfileData.height
$deliveryAudioRate=[int]$deliveryProfileData.audio_sample_rate_hz
$deliveryFps=if($deliveryProfileData.PSObject.Properties.Name -contains 'fps'){[int]$deliveryProfileData.fps}else{30}
$deliveryEncoder=if($deliveryProfileData.PSObject.Properties.Name -contains 'encoder'){[string]$deliveryProfileData.encoder}else{'libx264'}
$deliveryPreset=if($deliveryProfileData.PSObject.Properties.Name -contains 'preset'){[string]$deliveryProfileData.preset}else{'fast'}
$deliveryCrf=if($deliveryProfileData.PSObject.Properties.Name -contains 'crf'){[int]$deliveryProfileData.crf}else{18}
$deliveryGopFrames=if($deliveryProfileData.PSObject.Properties.Name -contains 'gop_frames'){[int]$deliveryProfileData.gop_frames}else{[int]([math]::Round($deliveryFps*3))}
if($deliveryFps -lt 24 -or $deliveryFps -gt 60){throw "Delivery profile FPS outside 24..60: $DeliveryProfile fps=$deliveryFps"}
if($DeliveryProfile -eq 'REVIEW_720'){
    # REVIEW_720 is the native review delivery. Its final path is intentionally
    # identical to the source MP4 path; do not ask Copy-Item to copy a file onto itself.
    $sourceFull=[System.IO.Path]::GetFullPath($sourceMp4)
    $finalFull=[System.IO.Path]::GetFullPath($finalMp4)
    if(-not [string]::Equals($sourceFull,$finalFull,[System.StringComparison]::OrdinalIgnoreCase)){
        Copy-Item -LiteralPath $sourceMp4 -Destination $finalMp4 -Force
    }
} else {
    $ffArgs=@('-y','-hide_banner','-loglevel','error','-i',$sourceMp4,'-vf',"scale=${deliveryWidth}:${deliveryHeight}:flags=lanczos",'-c:v',$deliveryEncoder,'-preset',$deliveryPreset,'-crf',[string]$deliveryCrf,'-pix_fmt','yuv420p','-r',[string]$deliveryFps,'-g',[string]$deliveryGopFrames,'-keyint_min',[string]$deliveryGopFrames,'-sc_threshold','0','-flags','+cgop','-x264-params',('open_gop=0:keyint={0}:min-keyint={0}:scenecut=0' -f $deliveryGopFrames))
    if($NoSound){$ffArgs+=@('-an')}else{$ffArgs+=@('-c:a','aac','-profile:a','aac_low','-b:a','192k','-ar',[string]$deliveryAudioRate,'-ac','2')}
    $ffArgs+=$finalMp4
    & ffmpeg @ffArgs
    if($LASTEXITCODE -ne 0){throw "Delivery profile encode failed: $DeliveryProfile"}
}
if(-not(Test-Path -LiteralPath $finalMp4)){throw "Final delivery MP4 missing: $finalMp4"}

$sourceManifest=Get-Content -Raw (Join-Path $stage "${baseProductId}_manifest.json") | ConvertFrom-Json
$videoProbeRaw=& ffprobe -v error -show_streams -show_format -of json $finalMp4
if($LASTEXITCODE -ne 0){throw "FFprobe validation failed: $finalMp4"}
$videoProbe=$videoProbeRaw -join "`n" | ConvertFrom-Json
$video=@($videoProbe.streams|Where-Object{$_.codec_type -eq 'video'})|Select-Object -First 1
if(-not $video){throw 'Final delivery has no video stream.'}
if([int]$video.width -ne $deliveryWidth -or [int]$video.height -ne $deliveryHeight){throw "Delivery resolution mismatch: $($video.width)x$($video.height), expected ${deliveryWidth}x${deliveryHeight}"}
if([string]$video.r_frame_rate -ne '30/1'){throw "Delivery FPS mismatch: $($video.r_frame_rate)"}
if([int]$video.nb_frames -ne [int]$sourceManifest.visual.frame_count){throw "Delivery frame-count mismatch: $($video.nb_frames) vs $($sourceManifest.visual.frame_count)"}
if([math]::Abs([double]$video.duration-[double]$sourceManifest.visual.duration_seconds)-gt 0.08){throw "Delivery duration mismatch."}

if ($Force -and (Test-Path -LiteralPath $productRoot)) { Remove-Item -LiteralPath $productRoot -Recurse -Force }
New-Item -ItemType Directory -Force -Path $productRoot | Out-Null
Copy-Item -LiteralPath $finalMp4 -Destination (Join-Path $productRoot "$productId.mp4") -Force
foreach($name in @("${baseProductId}_social.txt","${baseProductId}_authoring.json","${baseProductId}_ffprobe.json","${baseProductId}_godot.log")){
    Copy-Item -LiteralPath (Join-Path $stage $name) -Destination (Join-Path $productRoot $name) -Force
}
if($KeepAvi){
    $aviSource=Join-Path $stage "$baseProductId.avi"
    if(-not(Test-Path -LiteralPath $aviSource)){throw "KeepAvi was requested but the retained AVI is missing: $aviSource"}
    Copy-Item -LiteralPath $aviSource -Destination (Join-Path $productRoot "$productId.avi") -Force
}
if($ExportGif){
    & ffmpeg -y -hide_banner -loglevel error -i (Join-Path $productRoot "$productId.mp4") -vf 'fps=24,scale=360:640:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=96:stats_mode=diff[p];[s1][p]paletteuse=dither=sierra2_4a' -loop 0 (Join-Path $productRoot "$productId.gif")
    if($LASTEXITCODE -ne 0){throw 'GIF packaging failed.'}
}
$repro=".\tools\prototypes\c11c_bulk\run_c11c_production.ps1 -Family $Family -Seed $Seed -DeliveryProfile $DeliveryProfile"
if($Duration -gt 0){$repro+=" -Duration $($Duration.ToString([System.Globalization.CultureInfo]::InvariantCulture))"}
if(-not [string]::IsNullOrWhiteSpace($Grammar)){$repro+=" -Grammar $Grammar"}
if($NoSound){$repro+=' -NoSound'}
if($NoFooter){$repro+=' -NoFooter'}
if($ExportGif){$repro+=' -ExportGif'}
if($KeepAvi){$repro+=' -KeepAvi'}
$prodManifest=[ordered]@{
    schema='C11-C-PRODUCTION-PRODUCT-V3'; revision='2.18.0'; status='FINAL_PRODUCT'; product_id=$productId; family=$Family; seed=$Seed
    grammar_id=if([string]::IsNullOrWhiteSpace($Grammar)){[string]$sourceManifest.grammar_id}else{$Grammar}
    grammar_name=if([string]::IsNullOrWhiteSpace($Grammar)){[string]$sourceManifest.grammar}else{$Grammar}
    created_utc=[DateTime]::UtcNow.ToString('o'); source_canvas='720x1280'; canvas="${deliveryWidth}x${deliveryHeight}"; delivery_profile=$DeliveryProfile
    fps=$deliveryFps; duration_seconds=[double]$sourceManifest.visual.duration_seconds; frames=[int]$sourceManifest.visual.frame_count
    sound_enabled=(-not $NoSound); export_gif=[bool]$ExportGif; keep_avi=[bool]$KeepAvi; footer_enabled=(-not $NoFooter)
    production_path=$productRoot; source_stage=$stage; reproduction_command=$repro
    files=@(Get-ChildItem -LiteralPath $productRoot -File|Select-Object -ExpandProperty Name)
}
[IO.File]::WriteAllText((Join-Path $productRoot 'production_manifest.json'),($prodManifest|ConvertTo-Json -Depth 15),(New-Object Text.UTF8Encoding($false)))
$productText=@"
C11-C FINAL PRODUCT
===================
Product ID: $productId
Family: $Family
Seed: $Seed
Grammar technical id: $(if([string]::IsNullOrWhiteSpace($Grammar)){[string]$sourceManifest.grammar_id}else{$Grammar})
Source capture: 720x1280
Delivery: ${deliveryWidth}x${deliveryHeight}
Delivery profile: $DeliveryProfile
FPS: $deliveryFps
Duration: $([double]$sourceManifest.visual.duration_seconds) s
Sound: $(-not $NoSound)
Footer: $(-not $NoFooter)

Reproduction command:
$repro
"@
[IO.File]::WriteAllText((Join-Path $productRoot 'PRODUCT.txt'),$productText,(New-Object Text.UTF8Encoding($false)))
Write-Host "[C11-C-PRODUCTION] FINAL PRODUCT PASS - $productId -> ${deliveryWidth}x${deliveryHeight}"
