param(
    [int[]]$Seeds = @(314159, 271828, 161803, 112358, 577215, 8675309, 424242, 990001),
    [switch]$Production
)

$ErrorActionPreference = 'Stop'
$ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$families = @(
    'c11c_geometric_waves_v1',
    'c11c_fractal_bloom_v1',
    'c11c_sacred_symmetry_v1',
    'c11c_living_particles_v1',
    'c11c_invisible_forces_v1'
)
$root = Join-Path $ProjectRoot 'artifacts\prototypes\c11c_bulk_multiseed'
New-Item -ItemType Directory -Force -Path $root | Out-Null
$results = @()
foreach ($seed in $Seeds) {
    foreach ($family in $families) {
        $launcher = Join-Path $ProjectRoot ("tools\prototypes\$family\run_prototype.ps1")
        if (-not (Test-Path -LiteralPath $launcher)) { throw "Missing launcher: $launcher" }
        Write-Host "[C11-C-MULTISEED] START family=${family} seed=${seed}"
        $launcherArgs = @('-Seed', $seed)
        if ($Production) { $launcherArgs += '-NoFooter' }
        & powershell -NoProfile -ExecutionPolicy Bypass -File $launcher @launcherArgs
        $exit = [int]$LASTEXITCODE
        if ($exit -ne 0) {
            $results += [ordered]@{ family=$family; seed=$seed; status='FAIL'; exit=$exit }
            throw "Multi-seed run failed for ${family} seed=${seed}: exit=${exit}"
        }
        $artifactDir = Join-Path $ProjectRoot ("artifacts\prototypes\$family")
        $literalSeedFiles = Get-ChildItem -LiteralPath $artifactDir -File -ErrorAction SilentlyContinue | Where-Object { $_.Name -match '\$Seed' }
        if ($literalSeedFiles) {
            Write-Warning "Legacy literal `$Seed artifacts detected in ${family}; they are retained as historical evidence and excluded from the current seed validation."
        }
        $seedToken = "seed_${seed}"
        $seedFiles = Get-ChildItem -LiteralPath $artifactDir -File -ErrorAction SilentlyContinue | Where-Object { $_.Name -like "*$seedToken*" }
        if (-not $seedFiles) { throw "No seed-specific artifacts found in ${family} for seed=${seed}." }
        $seedSpecific = $seedFiles | Where-Object { $_.Name -notmatch '\$Seed' }
        if (-not $seedSpecific) { throw "Seed ${seed} produced no non-literal seed artifacts in ${family}." }
        $results += [ordered]@{ family=$family; seed=$seed; status='PASS'; exit=0; artifact_count=$seedSpecific.Count; footer_mode=($(if ($Production) { 'OFF' } else { 'ON' })) }
        Write-Host "[C11-C-MULTISEED] PASS family=$family seed=$seed artifacts=$($seedSpecific.Count)"
    }
}
$manifest = [ordered]@{
    schema='C11-C-MULTISEED-BULK-V1'; status='COMPLETE'; revision='2.0.9'; seeds=@($Seeds); family_count=$families.Count; seed_count=$Seeds.Count; render_count=$families.Count*$Seeds.Count; results=$results; visual_contract=[ordered]@{canvas='720x1280'; body='y=192..1088'; fps=30; duration_seconds=18.0; frames=540; audio='stereo 44.1kHz, deterministic prototype bed'}; footer_mode=$(if ($Production) { 'OFF' } else { 'ON' }); variation_profile_revision='1.0.0'; frozen_boundaries_modified=$false
}
$manifestPath=Join-Path $root 'C11-C_MULTISEED_BULK_MANIFEST.json'
$manifest | ConvertTo-Json -Depth 8 | Set-Content -Encoding UTF8 $manifestPath
Write-Host "[C11-C-MULTISEED] COMPLETE renders=$($families.Count*$Seeds.Count) manifest=$manifestPath"
