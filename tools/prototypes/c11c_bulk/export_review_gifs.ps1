param(
    [string]$InputRoot = '.\artifacts\prototypes',
    [string]$OutputRoot = '.\artifacts\prototypes\c11c_review_assets',
    [int]$GifWidth = 360,
    [int]$GifHeight = 640,
    [int]$GifFps = 12,
    [int]$GifColors = 96,
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
    New-Item -ItemType Directory -Force -Path $familyOut | Out-Null
    $gifOut=Join-Path $familyOut ($stem+'_review.gif')
    $palette=Join-Path $familyOut ($stem+'_palette.png')
    & ffmpeg -hide_banner -loglevel error -y -i $mp4.FullName -vf ("fps={0},scale={1}:{2}:flags=lanczos,palettegen=max_colors={3}:stats_mode=diff" -f $GifFps,$GifWidth,$GifHeight,$GifColors) $palette
    if ($LASTEXITCODE -ne 0) { throw "palettegen failed for $stem" }
    & ffmpeg -hide_banner -loglevel error -y -i $mp4.FullName -i $palette -filter_complex ("[0:v]fps={0},scale={1}:{2}:flags=lanczos[x];[x][1:v]paletteuse=dither=sierra2_4a" -f $GifFps,$GifWidth,$GifHeight) -an $gifOut
    if ($LASTEXITCODE -ne 0) { throw "GIF encode failed for $stem" }
    Remove-Item -LiteralPath $palette -Force
}
Write-Host "[C11-C-REVIEW] GIFs complete: $($mp4s.Count)"
return
