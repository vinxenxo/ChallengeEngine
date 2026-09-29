[CmdletBinding()]
param(
    [ValidatePattern('^CHALLENGE_[0-9]{3}$')][string]$ChallengeId='CHALLENGE_003',
    [ValidateRange(1,2147483646)][int]$Seed=24681357,
    [ValidateSet('MIN_540','REVIEW_720','MASTER_1080')][string]$DeliveryProfile='MIN_540',
    [switch]$AllCanonical
)
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
$ProjectRoot=(Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
Set-Location $ProjectRoot
$smoke=Join-Path $ProjectRoot 'c11c-suite\c11c-test\run_c11c_challenge_smoke.ps1'
if(-not(Test-Path -LiteralPath $smoke -PathType Leaf)){throw "Challenge smoke launcher missing: $smoke"}
$args=@('-Seed',[string]$Seed,'-DeliveryProfile',$DeliveryProfile)
if($AllCanonical){
    Write-Host "[C11C-CHALLENGE-FAMILY] START all 9 Challenges seed=$Seed profile=$DeliveryProfile"
    $args += '-AllCanonical'
}else{
    Write-Host "[C11C-CHALLENGE-FAMILY] START $ChallengeId seed=$Seed profile=$DeliveryProfile"
    $args += @('-ChallengeId',$ChallengeId)
}
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File $smoke @args
$exit=$LASTEXITCODE
if($exit -ne 0){throw "[C11C-CHALLENGE-FAMILY] failed with exit code $exit"}
if($AllCanonical){Write-Host '[C11C-CHALLENGE-FAMILY] COMPLETE PASS - 9 challenge products'}else{Write-Host "[C11C-CHALLENGE-FAMILY] COMPLETE PASS - $ChallengeId"}
