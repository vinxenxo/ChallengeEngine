param(
    [string]$InputRoot = '.\artifacts\prototypes',
    [string]$OutputRoot = '.\artifacts\prototypes\c11c_review_assets',
    [double[]]$Times = @(0.0,2.25,4.5,6.75,9.0,11.25,13.5,15.75),
    [int]$Width = 720,
    [int]$Height = 1280,
    [int[]]$Seeds = @()
)
$ErrorActionPreference='Stop'
New-Item -ItemType Directory -Force -Path $OutputRoot | Out-Null
$mp4s=@(Get-ChildItem -Path $InputRoot -Recurse -Filter '*.mp4' | Where-Object {
    $_.Name -match '_seed_[0-9]+\.mp4$' -and
    $_.FullName -notlike '*c11c_review_assets*' -and
    ($Seeds.Count -eq 0 -or ($Seeds | ForEach-Object { $_.ToString() }) -contains ([regex]::Match($_.Name,'_seed_([0-9]+)\.mp4$').Groups[1].Value))
} | Sort-Object FullName)
if ($mp4s.Count -eq 0) { throw "No canonical C11-C seed MP4 files found under $InputRoot" }
foreach ($mp4 in $mp4s) {
    $stem=[IO.Path]::GetFileNameWithoutExtension($mp4.Name)
    $familyOut=Join-Path $OutputRoot $mp4.Directory.Name
    $keyOut=Join-Path $familyOut ($stem+'_keyframes')
    New-Item -ItemType Directory -Force -Path $keyOut | Out-Null
    $index=1
    foreach ($sec in $Times) {
        $png=Join-Path $keyOut ('{0}_kf_{1:D2}.png' -f $stem,$index)
        & ffmpeg -hide_banner -loglevel error -y -ss $sec -i $mp4.FullName -frames:v 1 -vf "scale=${Width}:${Height}:flags=lanczos" -an $png
        if ($LASTEXITCODE -ne 0) { throw "Keyframe extraction failed for ${stem} at ${sec}s" }
        $index++
    }
}
Write-Host "[C11-C-REVIEW] Keyframes complete: $($mp4s.Count) videos x $($Times.Count) frames"
return
