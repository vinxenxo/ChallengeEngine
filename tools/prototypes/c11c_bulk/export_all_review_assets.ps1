param(
    [string]$InputRoot = '.\artifacts\prototypes',
    [string]$OutputRoot = '.\artifacts\prototypes\c11c_review_assets',
    [int[]]$Seeds = @()
)
$ErrorActionPreference='Stop'
$gif=Join-Path $PSScriptRoot 'export_review_gifs.ps1'
$key=Join-Path $PSScriptRoot 'export_review_keyframes.ps1'
$gifArgs=@('-NoProfile','-ExecutionPolicy','Bypass','-File',$gif,'-InputRoot',$InputRoot,'-OutputRoot',$OutputRoot)
if($Seeds.Count -gt 0){$gifArgs += '-Seeds'; $gifArgs += @($Seeds | ForEach-Object {[string]$_})}
& powershell.exe @gifArgs
$exit=$LASTEXITCODE
if ($exit -ne 0) { throw "Review GIF export failed: exit=$exit" }
$keyArgs=@('-NoProfile','-ExecutionPolicy','Bypass','-File',$key,'-InputRoot',$InputRoot,'-OutputRoot',$OutputRoot)
if($Seeds.Count -gt 0){$keyArgs += '-Seeds'; $keyArgs += @($Seeds | ForEach-Object {[string]$_})}
& powershell.exe @keyArgs
$exit=$LASTEXITCODE
if ($exit -ne 0) { throw "Review keyframe export failed: exit=$exit" }
Write-Host '[C11-C-REVIEW] ALL REVIEW ASSETS COMPLETE'
return
