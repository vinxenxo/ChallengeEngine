#requires -Version 5.1
[CmdletBinding()]
param(
    [switch]$AuthorizePilot
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version 1.0

$Root = (Get-Location).Path
$D9Root = Join-Path $Root 'artifacts\tests\c11d_d9\d9_1'
$PilotOutputRoot = Join-Path $D9Root 'pilot_media'
$D9EvidenceRoot = Join-Path $D9Root 'evidence'
$ContractPath = Join-Path $Root 'definitions\c11d\d9\D9_REAL_MEDIA_PILOT_V1.json'
$D90Root = Join-Path $Root 'artifacts\tests\c11d_d9\d9_0'
$D87Root = Join-Path $Root 'artifacts\tests\c11d_d8\d8_7'
$SchemaPath = Join-Path $Root 'definitions\c11d\production\C11D_PRODUCTION_REQUEST_SCHEMA_V1.json'
$CliPath = Join-Path $Root 'tools\c11d\d4\production_cli.py'
$ProducerPath = Join-Path $Root 'tools\prototypes\c11c_bulk\run_c11c_challenge_production.ps1'
$ChallengePath = Join-Path $Root 'challenges\CHALLENGE_001.json'
$RequestPath = Join-Path $D9EvidenceRoot 'd9_1_canonical_request.json'
$PlanPath = Join-Path $D9EvidenceRoot 'd9_1_production_plan.json'
$RequestCliLog = Join-Path $D9EvidenceRoot 'd9_1_d4_5_cli.log'
$PilotReceiptPath = Join-Path $D9EvidenceRoot 'd9_1_receipt.json'
$ProbePath = Join-Path $D9EvidenceRoot 'd9_1_ffprobe.json'
$MutationPath = Join-Path $D9EvidenceRoot 'd9_1_mutation_guard.json'
$RenderLogPath = Join-Path $D9EvidenceRoot 'd9_1_renderer.log'
$ShaPath = Join-Path $D9EvidenceRoot 'd9_1_media_sha256.json'

foreach($p in @($ContractPath,$SchemaPath,$CliPath,$ProducerPath,$ChallengePath)) {
    if(-not (Test-Path -LiteralPath $p -PathType Leaf)){ throw "Required path missing: $p" }
}
if(-not(Test-Path -LiteralPath $D87Root -PathType Container)){ throw 'D8.7 evidence root missing.' }
if(-not(Test-Path -LiteralPath $D90Root -PathType Container)){ throw 'D9.0 evidence root missing.' }

function Read-Json([string]$Path) {
    return ([System.IO.File]::ReadAllText($Path) | ConvertFrom-Json)
}
function Write-Json([string]$Path,[object]$Value,[int]$Depth) {
    $text = [string]($Value | ConvertTo-Json -Depth $Depth)
    [System.IO.File]::WriteAllBytes($Path,[System.Text.Encoding]::UTF8.GetBytes($text))
}
function Hash-File([string]$Path) {
    return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
}
function Get-TreeSnapshot([string]$Path) {
    if(-not(Test-Path -LiteralPath $Path)){ return @() }
    $items = @(
        Get-ChildItem -LiteralPath $Path -File -Recurse -Force |
        Sort-Object FullName
    )
    $rows = @()
    foreach($f in $items){
        $rows += [pscustomobject]@{
            path = $f.FullName.Substring($Root.Length + 1).Replace('\','/')
            length = [int64]$f.Length
            sha256 = Hash-File $f.FullName
        }
    }
    return @($rows)
}
function Get-DeterministicSnapshotHash([object[]]$Rows) {
    $json = [string](@($Rows) | ConvertTo-Json -Depth 8 -Compress)
    return (Hash-Bytes ([System.Text.Encoding]::UTF8.GetBytes($json)))
}
function Hash-Bytes([byte[]]$Bytes) {
    $sha = [System.Security.Cryptography.SHA256]::Create()
    try { return ([BitConverter]::ToString($sha.ComputeHash($Bytes)) -replace '-','').ToLowerInvariant() }
    finally { $sha.Dispose() }
}

$D87Receipt = $null
$d87ReceiptCandidates = @(
    Get-ChildItem -LiteralPath $D87Root -Filter '*.json' -File -Force |
    Sort-Object Name
)
foreach($f in $d87ReceiptCandidates){
    try {
        $o=Read-Json $f.FullName
        if([string]$o.checkpoint -eq 'D8.7' -and [string]$o.status -eq 'CLOSED'){ $D87Receipt=$o; break }
    } catch {}
}
if($null -eq $D87Receipt){ throw 'No D8.7 PASS/CLOSED receipt found.' }
if([string]$D87Receipt.result -ne 'PASS_NO_MEDIA'){ throw 'D8.7 is not PASS_NO_MEDIA.' }
if([string]$D87Receipt.release_authority -ne 'NONE'){ throw 'D8.7 release_authority is not NONE.' }

$D90Preflight = $null
$D90PreflightPath = $null
$d90Candidates = @(
    Get-ChildItem -LiteralPath $D90Root -Filter '*.json' -File -Recurse -Force |
    Sort-Object FullName
)
foreach($f in $d90Candidates){
    try {
        $o=Read-Json $f.FullName
        $isD90 = ($null -ne $o.phase -and [string]$o.phase -eq 'D9.0') -or ($null -ne $o.checkpoint -and [string]$o.checkpoint -eq 'D9.0')
        $isPreflight = (($null -ne $o.status -and [string]$o.status -eq 'PREFLIGHT_ONLY') -or ($null -ne $o.preflight_only -and [bool]$o.preflight_only -eq $true))
        $isPass = ($null -ne $o.result -and [string]$o.result -in @('PASS','PASS_NO_MEDIA'))
        if($isD90 -and $isPreflight -and $isPass){
            $D90Preflight=$o
            $D90PreflightPath=$f.FullName
            break
        }
    } catch {}
}
if($null -eq $D90Preflight){
    $names = @($d90Candidates | Select-Object -ExpandProperty Name)
    throw ('No valid D9.0 preflight evidence found. JSON files inspected: ' + (($names -join ', ')))
}
if($null -ne $D90Preflight.pilot_authorized -and [bool]$D90Preflight.pilot_authorized){ throw 'D9.0 pilot authority must still be false before D9.1.' }

if(-not $AuthorizePilot){
    throw 'D9.1 physical execution is disabled. Re-run with -AuthorizePilot for the explicit single-case pilot.'
}

$cfg = Read-Json $ChallengePath
if([string]$cfg.challenge_id -ne 'CHALLENGE_001'){ throw 'CHALLENGE_001 identity mismatch.' }
if([string]$cfg.mechanic_version -ne '1.0'){ throw 'Unexpected CHALLENGE_001 mechanic_version.' }
$fps=[int]$cfg.video.fps
$hook=[double]$cfg.video.hook_duration
$game=[double]$cfg.video.game_duration
$reveal=[double]0
$revealProp=$cfg.video.PSObject.Properties['reveal_duration']
if($null -ne $revealProp){$reveal=[double]$revealProp.Value}
$cta=[double]$cfg.video.cta_duration
$frames=[int][Math]::Floor((($hook+$game+$reveal+$cta)*$fps)+0.5)
$duration=($frames/[double]$fps)

New-Item -ItemType Directory -Force -Path $D9EvidenceRoot,$PilotOutputRoot | Out-Null
$existing=@(Get-ChildItem -LiteralPath $PilotOutputRoot -File -Recurse -Force -ErrorAction SilentlyContinue)
if($existing.Count -gt 0){ throw 'Pilot output root is not empty; no replacement is allowed.' }

$request=[ordered]@{
    request_id='D9.1-PILOT-001'
    schema_version='1.0'
    mode='REVIEW'
    challenge_id='CHALLENGE_001'
    challenge_version='1.0'
    seed=12345
    music_seed=840001
    delivery_profile_id='REVIEW_720'
    presentation_profile_id='social_default_v1'
    duration_seconds=$duration
    variation_index=0
    personalization=[ordered]@{enabled=$false;profile_id='none_v1';values=@{}}
    editorial=[ordered]@{title='CHALLENGE_001 · key';subtitle='D9.1 REAL MEDIA PILOT';language='es';call_to_action='¡INTÉNTALO TÚ TAMBIÉN!'}
    output=[ordered]@{container='mp4';width=720;height=1280;fps=$fps;audio_enabled=$false}
    provenance=[ordered]@{source_revision='D7-FROZEN';request_origin='TEST';parent_request_id='UNKNOWN'}
}
Write-Json $RequestPath $request 20

# Canonical D4.5 plan. The plan stays non-executing.
$cliRaw = & python.exe $CliPath --request $RequestPath --output $PlanPath --print-json 2>&1
$cliExit=$LASTEXITCODE
[System.IO.File]::WriteAllText($RequestCliLog,(($cliRaw -join [Environment]::NewLine)),[System.Text.Encoding]::UTF8)
if($cliExit -ne 0){ throw 'D9.1 D4.5 canonical request/plan failed.' }
$plan=Read-Json $PlanPath
if([string]$plan.challenge_id -ne 'CHALLENGE_001'){ throw 'D4.4 plan challenge mismatch.' }
if([string]$plan.delivery_profile_id -ne 'REVIEW_720'){ throw 'D4.4 plan delivery profile mismatch.' }
if([int]$plan.seed -ne 12345){ throw 'D4.4 plan gameplay seed mismatch.' }
if([int]$plan.music_seed -ne 840001){ throw 'D4.4 plan music seed mismatch.' }
if([string]$plan.runtime_authority -ne 'NONE'){ throw 'D4.4 plan runtime authority crossed boundary.' }
if([bool]$plan.renderer_activation){ throw 'D4.4 plan renderer activation is true.' }
if([bool]$plan.orchestrator_execution){ throw 'D4.4 plan orchestrator execution is true.' }

$protectedPaths=@(
    (Join-Path $Root 'c11c-suite'),
    (Join-Path $Root 'challenges'),
    (Join-Path $Root 'core'),
    (Join-Path $Root 'tests'),
    (Join-Path $Root 'tools\c11c'),
    (Join-Path $Root 'tools\c11d\d0'),
    (Join-Path $Root 'tools\c11d\d1'),
    (Join-Path $Root 'tools\c11d\d2'),
    (Join-Path $Root 'tools\c11d\d3'),
    (Join-Path $Root 'tools\c11d\d4'),
    (Join-Path $Root 'tools\c11d\d5'),
    (Join-Path $Root 'tools\c11d\d6'),
    (Join-Path $Root 'tools\c11d\d7'),
    (Join-Path $Root 'definitions\c11d\production'),
    (Join-Path $Root 'definitions\c11d\seeds'),
    (Join-Path $Root 'artifacts\releases'),
    (Join-Path $Root 'release')
)
$beforeProtected=@()
foreach($p in $protectedPaths){
    if(Test-Path -LiteralPath $p){
        $beforeProtected += [pscustomobject]@{root=$p.Substring($Root.Length+1).Replace('\','/');files=Get-TreeSnapshot $p}
    }
}

$renderArgs=@(
    '-NoProfile','-ExecutionPolicy','Bypass','-File',$ProducerPath,
    '-ChallengeId','CHALLENGE_001',
    '-Seed','12345',
    '-DeliveryProfile','REVIEW_720',
    '-OutputRoot',$PilotOutputRoot,
    '-KeepAvi',
    '-NoSound'
)
$renderOutput = & powershell.exe @renderArgs 2>&1
$renderExit=$LASTEXITCODE
[System.IO.File]::WriteAllText($RenderLogPath,(($renderOutput -join [Environment]::NewLine)),[System.Text.Encoding]::UTF8)
if($renderExit -ne 0){ throw "Physical producer failed with exit=$renderExit. See $RenderLogPath" }

$mp4s=@(Get-ChildItem -LiteralPath $PilotOutputRoot -Filter '*.mp4' -File -Recurse -Force)
$avis=@(Get-ChildItem -LiteralPath $PilotOutputRoot -Filter '*_source.avi' -File -Recurse -Force)
if($mp4s.Count -ne 1){ throw "Expected exactly one pilot MP4; found $($mp4s.Count)." }
if($avis.Count -ne 1){ throw "Expected exactly one pilot source AVI; found $($avis.Count)." }
$mp4=$mp4s[0]
$avi=$avis[0]

$probeRaw=& ffprobe -v error -count_frames -show_streams -show_format -of json -- $mp4.FullName 2>&1
if($LASTEXITCODE -ne 0){ throw 'ffprobe failed on pilot MP4.' }
$probeText=$probeRaw -join [Environment]::NewLine
[System.IO.File]::WriteAllText($ProbePath,$probeText,[System.Text.Encoding]::UTF8)
$probe=$probeText|ConvertFrom-Json
$v=@($probe.streams|Where-Object{$_.codec_type -eq 'video'})|Select-Object -First 1
if($null -eq $v){ throw 'Pilot MP4 has no video stream.' }
if([int]$v.width -ne 720 -or [int]$v.height -ne 1280){ throw "Pilot delivery resolution mismatch: $($v.width)x$($v.height)" }
if([string]$v.r_frame_rate -ne ("{0}/1" -f $fps)){ throw "Pilot FPS mismatch: $($v.r_frame_rate), expected $fps/1" }
if([int]$v.nb_read_frames -ne $frames){ throw "Pilot frame mismatch: $($v.nb_read_frames), expected $frames" }
if(@($probe.streams|Where-Object{$_.codec_type -eq 'audio'}).Count -ne 0){ throw 'Visual pilot unexpectedly contains an audio stream.' }

$afterProtected=@()
foreach($p in $protectedPaths){
    if(Test-Path -LiteralPath $p){
        $afterProtected += [pscustomobject]@{root=$p.Substring($Root.Length+1).Replace('\','/');files=Get-TreeSnapshot $p}
    }
}
$beforeJson=[string]($beforeProtected|ConvertTo-Json -Depth 16 -Compress)
$afterJson=[string]($afterProtected|ConvertTo-Json -Depth 16 -Compress)
$protectedEqual=($beforeJson -eq $afterJson)
Write-Json $MutationPath ([ordered]@{result=$(if($protectedEqual){'PASS'}else{'FAIL'});allowed_write_root='artifacts/tests/c11d_d9/d9_1';physical_media_mutation_performed=$true;release_product_mutation_performed=$false;protected_roots_equal=$protectedEqual}) 10
if(-not $protectedEqual){ throw 'Protected root mutation detected.' }

$mediaSha=@(
    [ordered]@{path=$mp4.FullName.Substring($Root.Length+1).Replace('\','/');sha256=Hash-File $mp4.FullName;bytes=[int64]$mp4.Length},
    [ordered]@{path=$avi.FullName.Substring($Root.Length+1).Replace('\','/');sha256=Hash-File $avi.FullName;bytes=[int64]$avi.Length}
)
Write-Json $ShaPath $mediaSha 8

$receipt=[ordered]@{
    contract='C11-D-D9-REAL-MEDIA-PILOT-V1'
    checkpoint='D9.1'
    result='PASS'
    status='PILOT_COMPLETE'
    pilot_authorized=$true
    challenge_id='CHALLENGE_001'
    challenge_version='1.0'
    mode='REVIEW'
    seed=12345
    music_seed=840001
    delivery_profile_id='REVIEW_720'
    presentation_profile_id='social_default_v1'
    audio_enabled=$false
    source_resolution='540x960'
    delivery_resolution='720x1280'
    fps=$fps
    frames=$frames
    duration_seconds=$duration
    source_avi=$avi.FullName.Substring($Root.Length+1).Replace('\','/')
    delivery_mp4=$mp4.FullName.Substring($Root.Length+1).Replace('\','/')
    d4_plan_sha256=(Hash-File $PlanPath)
    d9_0_preflight_evidence=$(if($null -ne $D90PreflightPath){$D90PreflightPath.Substring($Root.Length+1).Replace('\','/')}else{$null})
    release_authority='NONE'
    global_production_execution=$false
    bulk_execution=$false
    release_product_created=$false
    protected_roots_unchanged=$protectedEqual
    next='D9.2 - Audio-enabled real media pilot'
}
Write-Json $PilotReceiptPath $receipt 12

Write-Host "D9.1 PASS | challenge=CHALLENGE_001 | profile=REVIEW_720 | frames=$frames | video=$($mp4.FullName) | audio=OFF | release_authority=NONE"
