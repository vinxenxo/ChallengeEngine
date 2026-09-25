param(
    [Parameter(Mandatory=$false)]
    [ValidateRange(1,2147483646)]
    [int]$Seed=314159,
    [Parameter(Mandatory=$false)]
    [string]$OutputRoot='',
    [switch]$Force
)
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
$ProjectRoot=(Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$composer=Join-Path $PSScriptRoot 'run_c11c_visual_loop_longform_production.ps1'
$families=@('c11c_geometric_waves_v1','c11c_fractal_bloom_v1','c11c_sacred_symmetry_v1','c11c_living_particles_v1','c11c_invisible_forces_v1')
if([string]::IsNullOrWhiteSpace($OutputRoot)){ $OutputRoot=Join-Path $ProjectRoot 'artifacts\production\audiovisual_longform' }
$results=@()
foreach($family in $families){
    Write-Host "[C11-C-LONGFORM-BULK] $family seed=$Seed"
    $params=@{Family=$family;Seed=$Seed;OutputRoot=$OutputRoot}
    if($Force){$params.Force=$true}
    & $composer @params
    if($LASTEXITCODE -ne 0){throw "Longform production failed for $family"}
    $key = switch ($family) {
        'c11c_geometric_waves_v1' { 'geometric' }
        'c11c_fractal_bloom_v1' { 'fractal' }
        'c11c_sacred_symmetry_v1' { 'sacred_symmetry' }
        'c11c_living_particles_v1' { 'living_particles' }
        'c11c_invisible_forces_v1' { 'invisible_forces' }
    }
    $dir=Join-Path $OutputRoot $family
    $product=Get-ChildItem -LiteralPath $dir -Filter '*_Longform_seed_*.mp4' -File | Sort-Object LastWriteTime -Descending | Select-Object -First 1
    if($null -eq $product){throw "Longform output MP4 not found for $family"}
    $results += [pscustomobject]@{family=$key;seed=$Seed;mp4=$product.FullName;status='PASS'}
}
Write-Host "[C11-C-LONGFORM-BULK] COMPLETE families=$($results.Count) seed=$Seed root=$OutputRoot"
$results | Format-Table -AutoSize
