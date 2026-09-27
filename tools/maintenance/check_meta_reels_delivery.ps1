param(
    [Parameter(Mandatory=$true)][string]$InputMp4,
    [ValidateSet('PROJECT_TARGET','META_REELS_FINAL_V1')][string]$Profile='META_REELS_FINAL_V1',
    [switch]$Strict,
    [switch]$RequireAudio
)
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
$Path=(Resolve-Path -LiteralPath $InputMp4).Path
$raw=& ffprobe -v error -show_streams -show_format -of json $Path 2>&1
$exit=$LASTEXITCODE
if($exit -ne 0){throw "ffprobe failed for $Path"}
$data=($raw -join "`n") | ConvertFrom-Json
$v=@($data.streams|Where-Object{$_.codec_type -eq 'video'})|Select-Object -First 1
$a=@($data.streams|Where-Object{$_.codec_type -eq 'audio'})|Select-Object -First 1
if($null -eq $v){throw 'No video stream found.'}
$w=[int]$v.width; $h=[int]$v.height
$fps=[string]$v.r_frame_rate; $afps=[string]$v.avg_frame_rate
$checks=[ordered]@{}
if($Profile -eq 'META_REELS_FINAL_V1'){
    $checks.container=([string]$data.format.format_name -match 'mp4')
    $checks.aspect=([double]$w/[double]$h -gt 0.555 -and [double]$w/[double]$h -lt 0.565)
    $checks.resolution=($w -eq 1080 -and $h -eq 1920)
    $checks.fps=($fps -eq '30/1' -and $afps -eq '30/1')
    $checks.progressive=([string]$v.field_order -in @('unknown','progressive','') -or [int]$v.field_order -eq 0)
    $checks.h264=([string]$v.codec_name -eq 'h264')
    $checks.yuv420p=([string]$v.pix_fmt -eq 'yuv420p')
    if($null -eq $a){$checks.audio=$false;$checks.audio_bitrate=$false;$checks.stereo=$false;$checks.aac_lc=$false;$checks.sample_rate_48k=$false}
    else{$checks.audio=$true;$checks.audio_bitrate=([int64]$a.bit_rate -ge 128000);$checks.stereo=([int]$a.channels -eq 2);$checks.aac_lc=([string]$a.codec_name -eq 'aac' -and ([string]$a.profile -match '(?i)LC|Low Complexity'));$checks.sample_rate_48k=([int]$a.sample_rate -eq 48000)}
    Write-Host '[META-REELS] Closed GOP: must be proven by the encoder contract (3 seconds at fixed 30 FPS = 90 frames); ffprobe stream metadata alone is insufficient.'
}
else{
    $checks.container=([string]$data.format.format_name -match 'mp4')
    $checks.aspect=([double]$w/[double]$h -gt 0.555 -and [double]$w/[double]$h -lt 0.565)
    $checks.minimum_resolution=($w -ge 540 -and $h -ge 960)
    $checks.fps=($afps -ne '' -and $fps -eq $afps)
    $checks.h264=([string]$v.codec_name -eq 'h264')
    $checks.yuv420p=([string]$v.pix_fmt -eq 'yuv420p')
}
Write-Host '[META-REELS] =========================================='
Write-Host "[META-REELS] Profile=$Profile"
Write-Host "[META-REELS] File=$Path"
Write-Host "[META-REELS] Video=${w}x${h} codec=$($v.codec_name) pix_fmt=$($v.pix_fmt) fps=$fps"
if($null -ne $a){Write-Host "[META-REELS] Audio codec=$($a.codec_name) profile=$($a.profile) bitrate=$($a.bit_rate) sample_rate=$($a.sample_rate) channels=$($a.channels)"}else{Write-Host '[META-REELS] Audio: none'}
foreach($k in $checks.Keys){Write-Host ('[META-REELS] {0} = {1}' -f $k,$checks[$k])}
$failed=@($checks.Keys|Where-Object{-not[bool]$checks[$_]})
if($RequireAudio -and $null -eq $a){$failed += 'audio'}
if($Profile -eq 'META_REELS_FINAL_V1'){
    $checks.duration_range='manual/manifest check: 3..90 s for Facebook Reels target'
    $failed=$failed|Where-Object{$_ -ne 'duration_range'}
}
if($failed.Count -gt 0){Write-Host "[META-REELS] RESULT = FAIL: $($failed -join ', ')"; if($Strict){exit 1}}
else{Write-Host '[META-REELS] RESULT = PASS'}
