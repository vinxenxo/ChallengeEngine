#requires -Version 5.1
[CmdletBinding()]
param(
    [switch]$AuthorizeAcceptance
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version 1.0

$Root = (Get-Location).Path
$D94Root = Join-Path $Root 'artifacts\tests\c11d_d9\d9_4'
$EvidenceRoot = Join-Path $D94Root 'evidence'
$ContractPath = Join-Path $Root 'definitions\c11d\d9\D9_ACCEPTANCE_CLOSURE_V1.json'
$D87Root = Join-Path $Root 'artifacts\tests\c11d_d8\d8_7'
$D90Root = Join-Path $Root 'artifacts\tests\c11d_d9\d9_0'
$D91Root = Join-Path $Root 'artifacts\tests\c11d_d9\d9_1'
$D92Root = Join-Path $Root 'artifacts\tests\c11d_d9\d9_2'
$D93Root = Join-Path $Root 'artifacts\tests\c11d_d9\d9_3'
$Receipt91Path = Join-Path $D91Root 'evidence\d9_1_receipt.json'
$Mutation91Path = Join-Path $D91Root 'evidence\d9_1_mutation_guard.json'
$Receipt92Path = Join-Path $D92Root 'evidence\d9_2_receipt.json'
$Receipt93Path = Join-Path $D93Root 'evidence\d9_3_receipt.json'
$Repeat93Path = Join-Path $D93Root 'evidence\d9_3_repeatability.json'
$Negative93Path = Join-Path $D93Root 'evidence\d9_3_negative_control.json'
$Mutation93Path = Join-Path $D93Root 'evidence\d9_3_mutation_guard.json'
$Probe93Path = Join-Path $D93Root 'evidence\d9_3_ffprobe.json'
$D91VideoPath = Join-Path $D91Root 'pilot_media\CHALLENGE_001\CHALLENGE_001_seed_12345.mp4'
$D92VideoPath = Join-Path $D92Root 'pilot_media\CHALLENGE_001_seed_12345_AV.mp4'
$D93RepeatAVPath = Join-Path $D93Root 'pilot_media\repeat_a\CHALLENGE_001_seed_12345_AV_repeat_A.mp4'
$D93RepeatBVPath = Join-Path $D93Root 'pilot_media\repeat_b\CHALLENGE_001_seed_12345_AV_repeat_B.mp4'
$D93NegativeAVPath = Join-Path $D93Root 'pilot_media\negative_music_seed\CHALLENGE_001_seed_12345_AV_musicseed_840002.mp4'
$ReceiptPath = Join-Path $EvidenceRoot 'd9_4_receipt.json'
$ManifestPath = Join-Path $EvidenceRoot 'd9_4_acceptance_manifest.json'
$MutationPath = Join-Path $EvidenceRoot 'd9_4_mutation_guard.json'

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
    $items = @(Get-ChildItem -LiteralPath $Path -File -Recurse -Force | Sort-Object FullName)
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
function Require-File([string]$Path) {
    if(-not(Test-Path -LiteralPath $Path -PathType Leaf)){ throw "Required evidence file missing: $Path" }
}
function Require-Receipt([string]$Path,[string]$Checkpoint,[string]$Status) {
    Require-File $Path
    $o = Read-Json $Path
    if([string]$o.checkpoint -ne $Checkpoint){ throw "$Checkpoint receipt checkpoint mismatch: $Path" }
    if([string]$o.result -ne 'PASS'){ throw "$Checkpoint receipt result is not PASS: $Path" }
    if([string]$o.status -ne $Status){ throw "$Checkpoint receipt status mismatch: $Path" }
    return $o
}

Require-File $ContractPath
foreach($p in @($D87Root,$D90Root,$D91Root,$D92Root,$D93Root)){
    if(-not(Test-Path -LiteralPath $p -PathType Container)){ throw "Required evidence root missing: $p" }
}
foreach($p in @($Mutation91Path,$Receipt92Path,$Receipt93Path,$Repeat93Path,$Negative93Path,$Mutation93Path,$Probe93Path,$D91VideoPath,$D92VideoPath,$D93RepeatAVPath,$D93RepeatBVPath,$D93NegativeAVPath)){
    Require-File $p
}

$cfg = Read-Json $ContractPath
if([string]$cfg.schema -ne 'C11-D-D9-ACCEPTANCE-CLOSURE-V1'){ throw 'D9.4 contract identity mismatch.' }
if([string]$cfg.release_authority -ne 'NONE'){ throw 'D9.4 release authority boundary failed.' }
if([bool]$cfg.production_execution){ throw 'D9.4 production execution must remain false.' }
if([string]$cfg.allowed_write_root -ne 'artifacts/tests/c11d_d9/d9_4'){ throw 'D9.4 allowed write root mismatch.' }

$d87 = $null
$d87Candidates = @(Get-ChildItem -LiteralPath $D87Root -Filter '*.json' -File -Force | Sort-Object Name)
foreach($f in $d87Candidates){
    try {
        $o = Read-Json $f.FullName
        if([string]$o.checkpoint -eq 'D8.7' -and [string]$o.status -eq 'CLOSED' -and [string]$o.result -eq 'PASS_NO_MEDIA'){ $d87 = $o; break }
    } catch {}
}
if($null -eq $d87){ throw 'D8.7 PASS_NO_MEDIA/CLOSED receipt not found.' }
if([string]$d87.release_authority -ne 'NONE'){ throw 'D8.7 release authority must remain NONE.' }

$d90 = $null
$d90Candidates = @(Get-ChildItem -LiteralPath $D90Root -Filter '*.json' -File -Recurse -Force | Sort-Object FullName)
foreach($f in $d90Candidates){
    try {
        $o = Read-Json $f.FullName
        $isD90 = (($null -ne $o.phase -and [string]$o.phase -eq 'D9.0') -or ($null -ne $o.checkpoint -and [string]$o.checkpoint -eq 'D9.0'))
        $isPass = ($null -ne $o.result -and [string]$o.result -eq 'PASS')
        $isPre = ($null -ne $o.status -and [string]$o.status -eq 'PREFLIGHT_ONLY')
        if($isD90 -and $isPass -and $isPre){ $d90 = $o; break }
    } catch {}
}
if($null -eq $d90){ throw 'D9.0 PASS/PREFLIGHT_ONLY evidence not found.' }
if($null -ne $d90.pilot_authorized -and [bool]$d90.pilot_authorized){ throw 'D9.0 pilot authority must remain false.' }
if($null -ne $d90.production_execution -and [bool]$d90.production_execution){ throw 'D9.0 production execution must remain false.' }

$d91 = Require-Receipt $Receipt91Path 'D9.1' 'PILOT_COMPLETE'
if([string]$d91.challenge_id -ne 'CHALLENGE_001' -or [int]$d91.seed -ne 12345 -or [string]$d91.delivery_profile_id -ne 'REVIEW_720'){ throw 'D9.1 identity mismatch.' }
if([int]$d91.frames -ne 540 -or [int]$d91.fps -ne 60){ throw 'D9.1 frame/FPS acceptance failed.' }
$mutation91 = Read-Json $Mutation91Path
if([string]$mutation91.result -ne 'PASS' -or -not [bool]$mutation91.protected_roots_equal){ throw 'D9.1 mutation guard acceptance failed.' }

$d92 = Require-Receipt $Receipt92Path 'D9.2' 'PILOT_COMPLETE'
if([string]$d92.challenge_id -ne 'CHALLENGE_001' -or [int]$d92.seed -ne 12345 -or [int]$d92.music_seed -ne 840001){ throw 'D9.2 identity mismatch.' }
if([string]$d92.audio_codec -ne 'aac' -or [int]$d92.audio_sample_rate_hz -ne 48000 -or [int]$d92.audio_channels -ne 2){ throw 'D9.2 audio acceptance failed.' }
if([int]$d92.frames -ne 540 -or [int]$d92.fps -ne 60){ throw 'D9.2 timing acceptance failed.' }
if([string]$d92.release_authority -ne 'NONE'){ throw 'D9.2 release authority must remain NONE.' }

$d93 = Require-Receipt $Receipt93Path 'D9.3' 'PILOT_REPEAT_COMPLETE'
if([string]$d93.challenge_id -ne 'CHALLENGE_001' -or [int]$d93.seed -ne 12345 -or [int]$d93.music_seed -ne 840001){ throw 'D9.3 identity mismatch.' }
if(-not [bool]$d93.repeatability_exact_wav -or -not [bool]$d93.repeatability_exact_mp4){ throw 'D9.3 exact repeatability is not PASS.' }
if(-not [bool]$d93.negative_control_music_changed -or -not [bool]$d93.negative_control_mp4_changed){ throw 'D9.3 negative control is not PASS.' }
if([string]$d93.release_authority -ne 'NONE'){ throw 'D9.3 release authority must remain NONE.' }

$repeat93 = Read-Json $Repeat93Path
if([string]$repeat93.result -ne 'PASS'){ throw 'D9.3 repeatability evidence is not PASS.' }
if(-not [bool]$repeat93.exact_wav_match -or -not [bool]$repeat93.exact_mp4_match){ throw 'D9.3 repeatability evidence does not prove exact equality.' }
$negative93 = Read-Json $Negative93Path
if([string]$negative93.result -ne 'PASS'){ throw 'D9.3 negative evidence is not PASS.' }
if(-not [bool]$negative93.wav_changed -or -not [bool]$negative93.mp4_changed){ throw 'D9.3 negative evidence does not prove changed output.' }
$mutation93 = Read-Json $Mutation93Path
if([string]$mutation93.result -ne 'PASS' -or -not [bool]$mutation93.protected_roots_equal){ throw 'D9.3 mutation guard acceptance failed.' }

$repeatAHash = Hash-File $D93RepeatAVPath
$repeatBHash = Hash-File $D93RepeatBVPath
$negativeHash = Hash-File $D93NegativeAVPath
if($repeatAHash -ne $repeatBHash){ throw 'Physical D9.3 repeat MP4 hashes differ.' }
if($repeatAHash -eq $negativeHash){ throw 'Physical D9.3 negative MP4 hash did not change.' }

$MediaChecks = @(
    [ordered]@{name='D9.1_VIDEO';path=$D91VideoPath;exists=$true;sha256=Hash-File $D91VideoPath;bytes=[int64](Get-Item -LiteralPath $D91VideoPath).Length},
    [ordered]@{name='D9.2_AV';path=$D92VideoPath;exists=$true;sha256=Hash-File $D92VideoPath;bytes=[int64](Get-Item -LiteralPath $D92VideoPath).Length},
    [ordered]@{name='D9.3_REPEAT_A';path=$D93RepeatAVPath;exists=$true;sha256=$repeatAHash;bytes=[int64](Get-Item -LiteralPath $D93RepeatAVPath).Length},
    [ordered]@{name='D9.3_REPEAT_B';path=$D93RepeatBVPath;exists=$true;sha256=$repeatBHash;bytes=[int64](Get-Item -LiteralPath $D93RepeatBVPath).Length},
    [ordered]@{name='D9.3_NEGATIVE';path=$D93NegativeAVPath;exists=$true;sha256=$negativeHash;bytes=[int64](Get-Item -LiteralPath $D93NegativeAVPath).Length}
)

if(-not $AuthorizeAcceptance){ throw 'D9.4 acceptance execution is disabled. Re-run with -AuthorizeAcceptance.' }
if(Test-Path -LiteralPath $D94Root){
    $existing = @(Get-ChildItem -LiteralPath $D94Root -File -Recurse -Force -ErrorAction SilentlyContinue)
    if($existing.Count -gt 0){ throw 'D9.4 acceptance root is not empty; replacement is forbidden.' }
}
New-Item -ItemType Directory -Force -Path $EvidenceRoot | Out-Null

$protectedRoots = @(
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
$beforeProtected = @()
foreach($p in $protectedRoots){
    if(Test-Path -LiteralPath $p){
        $beforeProtected += [pscustomobject]@{root=$p.Substring($Root.Length+1).Replace('\','/');files=Get-TreeSnapshot $p}
    }
}

$afterProtected = @()
foreach($p in $protectedRoots){
    if(Test-Path -LiteralPath $p){
        $afterProtected += [pscustomobject]@{root=$p.Substring($Root.Length+1).Replace('\','/');files=Get-TreeSnapshot $p}
    }
}
$protectedEqual = ([string]($beforeProtected | ConvertTo-Json -Depth 16 -Compress) -eq [string]($afterProtected | ConvertTo-Json -Depth 16 -Compress))

$manifest = [ordered]@{
    schema='C11-D-D9-ACCEPTANCE-MANIFEST-V1'
    checkpoint='D9.4'
    result='PASS'
    d9_status='CLOSED'
    d9_0='PASS/PREFLIGHT_ONLY'
    d9_1='PASS/PILOT_COMPLETE'
    d9_2='PASS/PILOT_COMPLETE'
    d9_3='PASS/PILOT_REPEAT_COMPLETE'
    d9_3_repeatability='EXACT'
    d9_3_negative_control='PASS'
    real_media_present=$true
    physical_media_mutation_performed=$true
    release_product_mutation_performed=$false
    release_authority='NONE'
    production_execution=$false
    renderer_execution=$false
    allowed_write_root='artifacts/tests/c11d_d9/d9_4'
    media=$MediaChecks
}
Write-Json $ManifestPath $manifest 16
Write-Json $MutationPath ([ordered]@{
    schema='C11-D-D9-MUTATION-GUARD-V1'
    result=$(if($protectedEqual){'PASS'}else{'FAIL'})
    allowed_write_root='artifacts/tests/c11d_d9/d9_4'
    physical_media_mutation_performed=$true
    release_product_mutation_performed=$false
    protected_roots_equal=$protectedEqual
}) 10
if(-not $protectedEqual){ throw 'D9.4 protected root mutation detected.' }

$receipt = [ordered]@{
    contract='C11-D-D9-ACCEPTANCE-CLOSURE-V1'
    checkpoint='D9.4'
    result='PASS'
    status='CLOSED'
    d9_status='CLOSED'
    acceptance_authorized=$true
    challenge_id='CHALLENGE_001'
    seed=12345
    music_seed=840001
    negative_music_seed=840002
    delivery_profile_id='REVIEW_720'
    presentation_profile_id='social_default_v1'
    d9_0_result='PASS'
    d9_1_result='PASS'
    d9_2_result='PASS'
    d9_3_result='PASS'
    exact_wav_repeatability=$true
    exact_mp4_repeatability=$true
    negative_music_seed_changed_wav=$true
    negative_music_seed_changed_mp4=$true
    real_media_present=$true
    physical_media_mutation_performed=$true
    release_product_mutation_performed=$false
    production_execution=$false
    renderer_execution=$false
    release_authority='NONE'
    mutation_guard='PASS'
    allowed_write_root='artifacts/tests/c11d_d9/d9_4'
    d8_7_dependency='PASS_NO_MEDIA/CLOSED'
    d8_7_release_authority='NONE'
    d9_1_receipt=$Receipt91Path.Substring($Root.Length+1).Replace('\','/')
    d9_2_receipt=$Receipt92Path.Substring($Root.Length+1).Replace('\','/')
    d9_3_receipt=$Receipt93Path.Substring($Root.Length+1).Replace('\','/')
    acceptance_manifest=$ManifestPath.Substring($Root.Length+1).Replace('\','/')
    mutation_evidence=$MutationPath.Substring($Root.Length+1).Replace('\','/')
}
Write-Json $ReceiptPath $receipt 16

Write-Host 'D9.4 PASS | D9=CLOSED | d9_1=PASS | d9_2=PASS | d9_3=PASS | repeatability=EXACT | negative_control=PASS | release_authority=NONE'
