#requires -Version 5.1
[CmdletBinding()]
param()
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version 1.0

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$builderPath = Join-Path $PSScriptRoot 'd7_5_full_acceptance_builder.py'
$outputDirectory = Join-Path $repoRoot 'artifacts\tests\c11d_d7\d7_5'

if(-not(Test-Path -LiteralPath $builderPath -PathType Leaf)){
    throw ('D7.5 builder not found: {0}' -f $builderPath)
}
New-Item -ItemType Directory -Path $outputDirectory -Force | Out-Null

# Do not permit Python to create bytecode anywhere in the repository.
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:PYTHONHASHSEED = '0'

function Get-DiagnosticTree {
    param([string]$Root)
    $map = @{}
    Get-ChildItem -LiteralPath $Root -Recurse -File -Force -ErrorAction SilentlyContinue |
        Where-Object {
            $_.FullName -notlike ((Join-Path $Root 'artifacts\tests\c11d_d7\d7_5') + '\*')
        } |
        ForEach-Object {
            $relative = $_.FullName.Substring($Root.Length).TrimStart([char]92,[char]47) -replace '\\','/'
            try {
                $hash = (Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
                $map[$relative] = ('{0}|{1}' -f $_.Length,$hash)
            } catch {
                $map[$relative] = ('ERROR|{0}' -f $_.Length)
            }
        }
    return $map
}

function Get-DiagnosticDelta {
    param(
        [hashtable]$Before,
        [hashtable]$After
    )
    $paths = @($Before.Keys + $After.Keys | Sort-Object -Unique)
    $delta = @()
    foreach($path in $paths){
        $beforeValue = $null
        $afterValue = $null
        if($Before.ContainsKey($path)){ $beforeValue = [string]$Before[$path] }
        if($After.ContainsKey($path)){ $afterValue = [string]$After[$path] }
        if($beforeValue -ne $afterValue){
            $kind = 'MODIFIED'
            if($null -eq $beforeValue){ $kind = 'ADDED' }
            elseif($null -eq $afterValue){ $kind = 'DELETED' }
            $delta += ('{0}: {1}' -f $kind,$path)
        }
    }
    return @($delta)
}

function Invoke-Builder {
    param(
        [string]$TempBuilder,
        [string]$Root,
        [string]$Label
    )
    & python.exe -B $TempBuilder --root $Root
    if($LASTEXITCODE -ne 0){
        throw ('D7.5 full acceptance builder {0} failed.' -f $Label)
    }
}

# Run the builder from a temporary copy outside the repository.
# This eliminates repository-local __pycache__ and makes the mutation guard authoritative.
$tempDir = Join-Path ([System.IO.Path]::GetTempPath()) ('c11d_d75_' + [Guid]::NewGuid().ToString('N'))
$tempBuilder = Join-Path $tempDir 'd7_5_full_acceptance_builder.py'
try {
    New-Item -ItemType Directory -Path $tempDir -Force | Out-Null
    Copy-Item -LiteralPath $builderPath -Destination $tempBuilder -Force

    $baseline = (& python.exe -B $tempBuilder --root $repoRoot --snapshot-only | ConvertFrom-Json)
    if($LASTEXITCODE -ne 0){ throw 'Unable to capture D7.5 repository snapshot.' }
    $diagnosticBefore = Get-DiagnosticTree -Root $repoRoot

    Write-Host ('[OK] Mutation guard baseline captured: {0} worktree files outside d7_5 evidence.' -f $baseline.files)

    for($runIndex = 1; $runIndex -le 2; $runIndex++){
        Invoke-Builder -TempBuilder $tempBuilder -Root $repoRoot -Label ('run {0}' -f $runIndex)
    }

    $after = (& python.exe -B $tempBuilder --root $repoRoot --snapshot-only | ConvertFrom-Json)
    if($LASTEXITCODE -ne 0){ throw 'Unable to capture final D7.5 repository snapshot.' }
    $diagnosticAfter = Get-DiagnosticTree -Root $repoRoot

    if($baseline.files -ne $after.files -or $baseline.sha256 -ne $after.sha256){
        $delta = Get-DiagnosticDelta -Before $diagnosticBefore -After $diagnosticAfter
        if(@($delta).Count -eq 0){
            $delta = @('Mutation hash/count changed but path-level diagnostic found no delta; inspect concurrent filesystem activity.')
        }
        $deltaText = ($delta -join '; ')
        throw ('FILESYSTEM_MUTATION_FAILURE: before={0}/{1}; after={2}/{3}; DELTA=[{4}]' -f $baseline.files,$baseline.sha256,$after.files,$after.sha256,$deltaText)
    }

    Write-Host '[OK] Mutation guard PASS; only artifacts/tests/c11d_d7/d7_5/ evidence may change.'

    $expected = @(
        'd7_5_full_acceptance.json',
        'd7_5_governance_validation.json',
        'd7_5_negative_tests.json',
        'd7_5_acceptance_receipt.json'
    )
    $actual = @(Get-ChildItem -LiteralPath $outputDirectory -File | Select-Object -ExpandProperty Name | Sort-Object)
    if(@($actual).Count -ne $expected.Count -or (Compare-Object $actual $expected)){
        throw 'D7.5 evidence scope failure: expected exactly four evidence JSON files.'
    }
    Write-Host '[OK] Four D7.5 evidence files present and exactly scoped.'

    $hashesA = @()
    foreach($expectedName in $expected){
        $hashesA += (Get-FileHash -LiteralPath (Join-Path $outputDirectory $expectedName) -Algorithm SHA256).Hash
    }
    $hashTextA = $hashesA -join '|'

    Invoke-Builder -TempBuilder $tempBuilder -Root $repoRoot -Label 'final idempotency run'

    $hashesB = @()
    foreach($expectedName in $expected){
        $hashesB += (Get-FileHash -LiteralPath (Join-Path $outputDirectory $expectedName) -Algorithm SHA256).Hash
    }
    $hashTextB = $hashesB -join '|'
    if($hashTextA -ne $hashTextB){
        throw 'D7.5 evidence SHA-256 mismatch across runs.'
    }
    Write-Host '[OK] Evidence SHA-256 values stable across repeated runs.'

    $receipt = Get-Content -LiteralPath (Join-Path $outputDirectory 'd7_5_acceptance_receipt.json') -Raw | ConvertFrom-Json
    if([string]$receipt.result -ne 'PASS' -or [string]$receipt.status -ne 'CLOSED'){
        $gov = Get-Content -LiteralPath (Join-Path $outputDirectory 'd7_5_governance_validation.json') -Raw | ConvertFrom-Json
        $govErrors = (($gov.errors | ForEach-Object { [string]$_ }) -join ', ')
        $full = Get-Content -LiteralPath (Join-Path $outputDirectory 'd7_5_full_acceptance.json') -Raw | ConvertFrom-Json
        $fullErrors = (($full.errors | ForEach-Object { [string]$_ }) -join ', ')
        throw ('D7.5 receipt is not PASS/CLOSED. GovernanceErrors=[{0}] FullErrors=[{1}]' -f $govErrors,$fullErrors)
    }

    Write-Host ('[OK] D7.0-D7.4 predecessors PASS/CLOSED; challenges={0}; matrix rows={1}; catalog items={2}; core cases={3}.' -f $receipt.challenge_count,$receipt.matrix_rows,$receipt.catalog_items,$receipt.core_cases)
    Write-Host ('[OK] C11-C build_factory.py identity={0}; frozen SHA={1}.' -f $receipt.c11c_build_factory_path,$receipt.c11c_build_factory_sha256)
    Write-Host ('[OK] Authorities: matrix={0}; catalog={1}; identity/provenance={2}.' -f $receipt.canonical_authorities.matrix,$receipt.canonical_authorities.catalog,$receipt.canonical_authorities.identity_provenance)
    Write-Host ('[OK] Governance pass={0}; negative tests={1}; D4.8={2}; runtime={3}; production={4}; renderer={5}; release present={6}.' -f $receipt.governance_pass,$receipt.negative_tests_pass,$receipt.d4_8_status,$receipt.runtime_authority,$receipt.production_execution,$receipt.renderer_execution,$receipt.release_directory_present)
    Write-Host '=================================================='
    Write-Host ' C11-D D7.5 - PASS / CLOSED'
    Write-Host '=================================================='
    Write-Host 'NEXT: D8 - Media QA + Release Pipeline'
}
finally {
    if(Test-Path -LiteralPath $tempDir){
        Remove-Item -LiteralPath $tempDir -Recurse -Force -ErrorAction SilentlyContinue
    }
}
