param(
    [string]$InputRoot = '.\artifacts\prototypes',
    [string]$OutputRoot = '.\artifacts\prototypes\c11c_review_assets',
    [int[]]$Seeds = @()
)
$ErrorActionPreference='Stop'
$gif=Join-Path $PSScriptRoot 'export_review_gifs.ps1'
$key=Join-Path $PSScriptRoot 'export_review_keyframes.ps1'
New-Item -ItemType Directory -Force -Path $OutputRoot | Out-Null
if($Seeds.Count -gt 0){
    & $gif -InputRoot $InputRoot -OutputRoot $OutputRoot -Seeds $Seeds
    if(-not $?){throw 'Review GIF export failed.'}
    & $key -InputRoot $InputRoot -OutputRoot $OutputRoot -Seeds $Seeds
    if(-not $?){throw 'Review keyframe export failed.'}
} else {
    & $gif -InputRoot $InputRoot -OutputRoot $OutputRoot
    if(-not $?){throw 'Review GIF export failed.'}
    & $key -InputRoot $InputRoot -OutputRoot $OutputRoot
    if(-not $?){throw 'Review keyframe export failed.'}
}
Write-Host '[C11-C-REVIEW] ALL REVIEW ASSETS COMPLETE'
return
