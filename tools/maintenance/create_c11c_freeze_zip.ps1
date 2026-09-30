[CmdletBinding()]
param(
    [string]$OutputRoot = '',
    [switch]$AllowWithoutAcceptance,
    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$root = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
Set-Location $root

if ([string]::IsNullOrWhiteSpace($OutputRoot)) {
    $OutputRoot = Join-Path $root 'artifacts\releases'
} elseif (-not [IO.Path]::IsPathRooted($OutputRoot)) {
    $OutputRoot = Join-Path $root $OutputRoot
}
$OutputRoot = [IO.Path]::GetFullPath($OutputRoot)
if (-not (Test-Path -LiteralPath $OutputRoot -PathType Container)) {
    if ($DryRun) {
        Write-Host ('[C11C-FREEZE-ZIP] Dry-run output directory would be created: ' + $OutputRoot)
    } else {
        New-Item -ItemType Directory -Path $OutputRoot -Force | Out-Null
    }
}

$acceptancePath = Join-Path $root 'artifacts\tests\reports\C11C_2.19.12_ACCEPTANCE_REPORT.json'
if (-not $AllowWithoutAcceptance) {
    if (-not (Test-Path -LiteralPath $acceptancePath -PathType Leaf)) {
        throw 'C11-C freeze blocked: C11C_2.19.12 acceptance report is missing.'
    }
    $acceptance = Get-Content -Raw -LiteralPath $acceptancePath | ConvertFrom-Json
    if ([string]$acceptance.status -ne 'PASS') {
        throw 'C11-C freeze blocked: C11C_2.19.12 acceptance report is not PASS.'
    }
    if ([string]$acceptance.revision -ne '2.19.12') {
        throw 'C11-C freeze blocked: acceptance report revision is not 2.19.12.'
    }
    foreach ($checkName in @(
        'docs_consolidated','suite_self_test','producer_self_test','producer_gui',
        'launcher_audit','parallel_contract','envelope_path_contract','one_video_smoke',
        'family_coverage_smoke','retro_reference','logical','c11a1','retro',
        'physical_smoke','physical_export','video_review'
    )) {
        $prop = $acceptance.checks.PSObject.Properties[$checkName]
        if ($null -eq $prop -or $prop.Value -ne $true) {
            throw ('C11-C freeze blocked: acceptance check is not PASS: ' + $checkName)
        }
    }
}

function Assert-HistoricalBuildFactory([string]$Path) {
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) { throw 'C11-C freeze blocked: build_factory.py is missing.' }
    $item = Get-Item -LiteralPath $Path
    if ($item.Length -lt 8192) {
        throw 'C11-C freeze blocked: build_factory.py is unexpectedly small; restore the verified historical implementation before sealing.'
    }
    $text = [IO.File]::ReadAllText($Path)
    foreach ($marker in @('FACTORY_VERSION =','MANIFEST_VERSION =','argparse.ArgumentParser','def run_factory(','def run_batch(','if __name__ == "__main__":')) {
        if ($text.IndexOf($marker,[StringComparison]::Ordinal) -lt 0) {
            throw ('C11-C freeze blocked: build_factory.py does not contain expected historical implementation marker: ' + $marker)
        }
    }
    foreach ($forbidden in @('temporary compatibility wrapper','compatibility wrapper','temporary stub','stub build_factory')) {
        if ($text.IndexOf($forbidden,[StringComparison]::OrdinalIgnoreCase) -ge 0) {
            throw ('C11-C freeze blocked: build_factory.py contains a forbidden temporary-wrapper marker: ' + $forbidden)
        }
    }
}

$buildFactory = Join-Path $root 'build_factory.py'
Assert-HistoricalBuildFactory $buildFactory
$buildFactoryHash = (Get-FileHash -LiteralPath $buildFactory -Algorithm SHA256).Hash.ToLowerInvariant()

$override = Join-Path $root 'override.cfg'
if (Test-Path -LiteralPath $override -PathType Leaf) {
    throw 'C11-C freeze blocked: repository root override.cfg is present.'
}
$leaked = @(Get-ChildItem -LiteralPath $root -Filter '.override.challenge_quarantine_*.cfg' -File -ErrorAction SilentlyContinue)
if (@($leaked).Count -gt 0) { throw 'C11-C freeze blocked: override quarantine residue exists in repository root.' }

$required = @(
    'project.godot',
    'GeneradorMaestro.gd',
    'build_factory.py',
    'release_gate.py',
    'tests/run_all.py',
    'FULL_ACCEPTANCE_C11C_2.19.12.ps1',
    'docs/current/c11c/C11-C_2.19_CONSOLIDATED_STATE.md',
    'docs/current/c11c/C11-C_2.19_CONSOLIDATED_ACCEPTANCE_GATE.md',
    'docs/current/c11c/C11-C_2.19_COMPLETE_VIDEO_REVIEW_RUNBOOK.md',
    'docs/current/c11c/C11-C_2.19_COMMAND_SHEET.md',
    'docs/current/c11c/C11-C_2.19_DOCUMENTATION_INDEX.md',
    'docs/current/c11c/C11-C_MAINTENANCE_AND_FREEZE_PACKAGING.md',
    'docs/current/c11c/C11-C_2.19.12_PREFREEZE_HARDENING_REPORT.md',
    'docs/current/c11c/C11-C_2.19.12_ACCEPTANCE_EVIDENCE.md',
    'docs/current/suite/C11C_SUITE_CURRENT_RULES.md',
    'docs/current/suite/C11C_SUITE_TOOLING_MATRIX.md',
    'docs/current/producer/C11C_PRODUCER_0.9.7_CURRENT_STATE.md',
    'docs/current/d/C11-D_ROADMAP_V1.0_STATELESS.md',
    'docs/current/d/C11-D_MILESTONES_APPROVED.md',
    'docs/master-prompts/MASTER_HANDOVER_C11C_2.19_CONSOLIDATED.md',
    'docs/master-prompts/START_PROMPT_C11C_2.19_CONSOLIDATED.md',
    'docs/master-prompts/MASTER_HANDOVER_C11D_V1.0_STATELESS.md',
    'docs/master-prompts/START_PROMPT_C11D_V1.0_STATELESS.md',
    'docs/master-prompts/C11D_CONTEXT_PACK_README.md',
    'docs/master-prompts/C11C_2.19.12_PREFREEZE_CONTEXT_PACK_V34.md',
    'c11c-suite/self_test.py',
    'c11c-suite/c11c-producer/self_test.py',
    'c11c-suite/c11c-maintenance/main.py',
    'c11c-suite/c11c-maintenance/organize_repository_root.ps1',
    'c11c-suite/c11c-maintenance/test_cleanup_contract.py',
    'c11c-suite/c11c-test/main.py',
    'c11c-suite/c11c-producer/test_producer_gui_contract.py',
    'c11c-suite/c11c-maintenance/run_freeze_package.bat'
)
$missing = @($required | Where-Object { -not (Test-Path -LiteralPath (Join-Path $root $_) -PathType Leaf) })
if (@($missing).Count -gt 0) { throw ('C11-C freeze blocked: missing required files: ' + ($missing -join ', ')) }

$staleRoot = @(
    'C11C_2.19.12_CONTEXT_INDEX.md',
    'C11C_2.19.12_CONTEXT_PACK_README.md',
    'C11C_2.19.12_CANDIDATE_RECEIPT.md',
    'C11C_2.19.12_FULL_CONSOLIDATED_RECEIPT.md',
    'C11C_2.19.12_REPAIR_CANDIDATE_MANIFEST.json',
    'C11C_2.19.12_STATIC_VALIDATION_REPORT.md',
    'CHANGELOG_C11-C_2.19.12.md',
    'CONTINUE.md',
    'OVERLAY_README.md',
    'Make_zip.ps1',
    'clean-videos.ps1',
    'clean-godot.ps1',
    'prepare_c11c_acceptance_workspace.ps1'
) | Where-Object { Test-Path -LiteralPath (Join-Path $root $_) -PathType Leaf }
if (@($staleRoot).Count -gt 0) { throw ('C11-C freeze blocked: stale root documentation/tool entries remain: ' + ($staleRoot -join ', ')) }

if (Test-Path -LiteralPath (Join-Path $root 'c11c-suite\c11c-maintenace') -PathType Container) {
    throw 'C11-C freeze blocked: obsolete misspelled c11c-suite/c11c-maintenace directory remains.'
}

$staleCurrent = @(
    'docs/current/c11c/C11-C_2.19.12_PREFREEZE_REPAIR_V24.md',
    'docs/current/c11c/C11-C_2.19.12_PREFREEZE_REPAIR_V25.md',
    'docs/current/c11c/C11-C_2.19_C11A1_CANONICAL_PRODUCER_CLOSURE_V16.md',
    'docs/current/c11c/C11-C_2.19_C11A1_CANONICAL_PRODUCER_CLOSURE_V17.md',
    'docs/current/c11c/C11-C_2.19_C11A1_CANONICAL_PRODUCER_CLOSURE_V18.md',
    'docs/current/c11c/C11-C_2.19_C11A1_MANIFEST_PATH_CLOSURE.md',
    'docs/current/c11c/C11-C_2.19_CURRENT_STATE.md',
    'docs/current/c11c/C11-C_2.19_V9_CLOSURE_NOTES.md',
    'docs/current/c11c/C11C_2.19.12_PRE_FREEZE_STATUS.md',
    'docs/current/c11c/C11C_2.19.12_A1_CLOSURE_CHANGELOG_V16.md',
    'docs/current/c11c/C11C_2.19.12_A1_CLOSURE_CHANGELOG_V17.md',
    'docs/current/c11c/C11C_2.19.12_A1_CLOSURE_CHANGELOG_V18.md',
    'docs/current/c11c/C11C_2.19.12_A1_CLOSURE_CHANGELOG_V19.md',
    'docs/current/suite/C11C_SUITE_0.1.5_RULES.md',
    'c11c-suite/c11c-producer/C11C_PRODUCER_START_PROMPT_2026-09-28.md',
    'c11c-suite/c11c-producer/C11C_PRODUCER_MASTER_HANDOVER_2026-09-28.md',
    'docs/current/c11c/FULL_ACCEPTANCE_REFERENCE.md',
    'docs/current/c11c/C11-C_2.19_REPAIR_MANIFEST.json',
    'docs/master-prompts/C11C_2.19.12_V33_PREFREEZE_CONTEXT_PACK.md',
    'docs/current/producer/C11C_PRODUCER_0.8.0_AUDIT.md',
    'docs/current/producer/C11C_PRODUCER_0.8.0_CURRENT_STATE.md',
    'docs/current/producer/C11C_PRODUCER_0.8.0_RUNTIME_ACCEPTANCE.md'
) | Where-Object { Test-Path -LiteralPath (Join-Path $root $_) -PathType Leaf }
$dynamicStale = @(
    Get-ChildItem -LiteralPath (Join-Path $root 'docs\current\c11c') -File -ErrorAction SilentlyContinue |
        Where-Object { $_.Name -match '(_V\d+\.|PREFREEZE_REPAIR_|A1_CLOSURE_|REPAIR_MANIFEST|FULL_ACCEPTANCE_REFERENCE)' } |
        ForEach-Object { $_.FullName.Substring($root.Length + 1).Replace('\','/') }
)
$dynamicStale += @(
    Get-ChildItem -LiteralPath (Join-Path $root 'docs\current\producer') -File -Filter 'C11C_PRODUCER_0.8.*' -ErrorAction SilentlyContinue |
        ForEach-Object { $_.FullName.Substring($root.Length + 1).Replace('\','/') }
)
if (@($staleCurrent).Count -gt 0 -or @($dynamicStale).Count -gt 0) {
    $allStale = @($staleCurrent + $dynamicStale | Select-Object -Unique)
    throw ('C11-C freeze blocked: stale current documentation remains: ' + ($allStale -join ', '))
}

$stamp = Get-Date -Format 'yyyyMMdd_HHmmss'
$zipName = "ChallengeEngineV01_STATELESS_C11-C_2.19.12_FROZEN_$stamp.zip"
$zipPath = Join-Path $OutputRoot $zipName
$tempManifest = Join-Path ([IO.Path]::GetTempPath()) ('c11c_freeze_manifest_' + [guid]::NewGuid().ToString('N') + '.json')

$excludeDirNames = @('.git','.godot','.mono','.import','.vscode','.idea','__pycache__','.pytest_cache','.mypy_cache','.ruff_cache','.venv','venv','env','artifacts','c11c-studio','c11c-maintenace')
$excludeRelativePrefixes = @('docs/history/root_conflicts/')
$excludeFiles = @('*.pyc','*.pyo','*.pyd','*.uid','*.import','*.tmp','*.temp','*.bak','*.old','*.orig','*.swp','*.swo','*~','*.zip','*.7z','*.rar','.DS_Store','Thumbs.db','Desktop.ini','*.coverage','*.dmp','*.stackdump')

$files = @(Get-ChildItem -LiteralPath $root -Recurse -File -Force | Where-Object {
    $rel = $_.FullName.Substring($root.Length + 1).Replace('\','/')
    $parts = $rel.Split('/')
    if ($parts | Where-Object { $excludeDirNames -contains $_ }) { return $false }
    foreach ($prefix in $excludeRelativePrefixes) { if ($rel.StartsWith($prefix,[StringComparison]::OrdinalIgnoreCase)) { return $false } }
    foreach ($pattern in $excludeFiles) { if ($_.Name -like $pattern) { return $false } }
    return $true
}) | Sort-Object FullName

$entries = @($files | ForEach-Object {
    $rel = $_.FullName.Substring($root.Length + 1).Replace('\','/')
    [pscustomobject]@{ path=$rel; bytes=[int64]$_.Length; sha256=(Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash.ToLowerInvariant() }
})

$treeLines = ($entries | ForEach-Object { '{0}|{1}|{2}' -f $_.path,$_.bytes,$_.sha256 }) -join "`n"
$tmpTree = Join-Path ([IO.Path]::GetTempPath()) ('c11c_freeze_tree_' + [guid]::NewGuid().ToString('N') + '.txt')
[IO.File]::WriteAllText($tmpTree,$treeLines,(New-Object Text.UTF8Encoding($false)))
$treeSha = (Get-FileHash -LiteralPath $tmpTree -Algorithm SHA256).Hash.ToLowerInvariant()
Remove-Item -LiteralPath $tmpTree -Force

$evidence = @()
if (Test-Path -LiteralPath $acceptancePath -PathType Leaf) {
    $evidence += [pscustomobject]@{ source=$acceptancePath; entry='release/evidence/C11C_2.19.12_ACCEPTANCE_REPORT.json' }
}
$reviewReport = Join-Path $root 'artifacts\prototypes\c11c_art_direction_review\C11-C_COMPLETE_VIDEO_REVIEW_REPORT.json'
if (-not (Test-Path -LiteralPath $reviewReport -PathType Leaf)) {
    if (-not $AllowWithoutAcceptance) { throw 'C11-C freeze blocked: complete-review report is missing.' }
} else {
    $evidence += [pscustomobject]@{ source=$reviewReport; entry='release/evidence/C11-C_COMPLETE_VIDEO_REVIEW_REPORT.json' }
}

$evidenceEntries = @($evidence | ForEach-Object {
    [pscustomobject]@{ path=$_.entry; bytes=[int64](Get-Item -LiteralPath $_.source).Length; sha256=(Get-FileHash -LiteralPath $_.source -Algorithm SHA256).Hash.ToLowerInvariant() }
})

$manifest = [ordered]@{
    schema='C11-C-FROZEN-PACKAGE-V2'
    release='C11-C 2.19.12'
    source_baseline='ChallengeEngineV01_STATELESS-C11-C2.19.12-V33-STABLE.zip'
    generated_at_utc=(Get-Date).ToUniversalTime().ToString('o')
    source_root='repository root'
    acceptance_report='artifacts/tests/reports/C11C_2.19.12_ACCEPTANCE_REPORT.json'
    acceptance_enforced=(-not $AllowWithoutAcceptance)
    acceptance_status=if(Test-Path -LiteralPath $acceptancePath -PathType Leaf){'PASS'}else{$null}
    build_factory_sha256=$buildFactoryHash
    hash_algorithm='SHA-256'
    source_tree_sha256=$treeSha
    source_file_count=@($entries).Count
    evidence_files=$evidenceEntries
    excluded_directory_names=$excludeDirNames
    excluded_relative_prefixes=$excludeRelativePrefixes
    excluded_file_patterns=$excludeFiles
    source_files=$entries
}
$manifestJson = $manifest | ConvertTo-Json -Depth 10
[IO.File]::WriteAllText($tempManifest,$manifestJson,(New-Object Text.UTF8Encoding($false)))

if ($DryRun) {
    Remove-Item -LiteralPath $tempManifest -Force -ErrorAction SilentlyContinue
    Write-Host '[C11C-FREEZE-ZIP] DRY-RUN PASS - all freeze gates and package-content checks passed.'
    Write-Host ('[C11C-FREEZE-ZIP] SOURCE FILES=' + @($entries).Count)
    Write-Host ('[C11C-FREEZE-ZIP] EVIDENCE FILES=' + @($evidenceEntries).Count)
    Write-Host ('[C11C-FREEZE-ZIP] TREE SHA-256=' + $treeSha)
    Write-Host ('[C11C-FREEZE-ZIP] build_factory.py SHA-256=' + $buildFactoryHash)
    exit 0
}

Add-Type -AssemblyName System.IO.Compression
Add-Type -AssemblyName System.IO.Compression.FileSystem
if (Test-Path -LiteralPath $zipPath) { Remove-Item -LiteralPath $zipPath -Force }
$zip = [System.IO.Compression.ZipFile]::Open($zipPath,'Create')
try {
    foreach ($item in $files) {
        $entryName = $item.FullName.Substring($root.Length + 1).Replace('\','/')
        [System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile($zip,$item.FullName,$entryName) | Out-Null
    }
    foreach ($item in $evidence) {
        [System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile($zip,$item.source,$item.entry) | Out-Null
    }
    [System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile($zip,$tempManifest,'release/C11C_FREEZE_PACKAGE_MANIFEST.json') | Out-Null
} finally {
    $zip.Dispose()
}
Remove-Item -LiteralPath $tempManifest -Force -ErrorAction SilentlyContinue

$zip = [System.IO.Compression.ZipFile]::OpenRead($zipPath)
try {
    $entryNames = @($zip.Entries | ForEach-Object { $_.FullName })
    $badEntries = @($entryNames | Where-Object {
        $_.StartsWith('/') -or $_.Contains('..') -or
        $_.ToLowerInvariant().StartsWith('artifacts/') -or
        $_.ToLowerInvariant().Contains('c11c-studio') -or
        $_.ToLowerInvariant().Contains('c11c-maintenace') -or
        $_.ToLowerInvariant().Contains('/__pycache__/') -or
        $_.ToLowerInvariant().EndsWith('.pyc')
    })
    if (@($badEntries).Count -gt 0) { throw ('C11-C freeze ZIP validation failed: forbidden entries: ' + ($badEntries -join ', ')) }
    foreach ($requiredEntry in $required) {
        $normalized = $requiredEntry.Replace('\','/')
        if ($entryNames -notcontains $normalized) { throw ('C11-C freeze ZIP validation failed: missing entry: ' + $normalized) }
    }
    foreach ($evidenceEntry in $evidenceEntries) {
        if ($entryNames -notcontains $evidenceEntry.path) { throw ('C11-C freeze ZIP validation failed: missing evidence entry: ' + $evidenceEntry.path) }
    }
    if ($entryNames -notcontains 'release/C11C_FREEZE_PACKAGE_MANIFEST.json') { throw 'C11-C freeze ZIP validation failed: package manifest entry missing.' }
    if (@($entryNames).Count -lt (@($entries).Count + @($evidenceEntries).Count + 1)) { throw 'C11-C freeze ZIP validation failed: archive entry count is unexpectedly small.' }
} finally {
    $zip.Dispose()
}
$zipHash = (Get-FileHash -LiteralPath $zipPath -Algorithm SHA256).Hash.ToLowerInvariant()
$sidecar = [ordered]@{
    schema='C11-C-FROZEN-PACKAGE-RECEIPT-V2'
    release='C11-C 2.19.12'
    archive=$zipName
    archive_sha256=$zipHash
    source_tree_sha256=$treeSha
    build_factory_sha256=$buildFactoryHash
    source_file_count=@($entries).Count
    evidence_file_count=@($evidenceEntries).Count
    generated_at_utc=(Get-Date).ToUniversalTime().ToString('o')
}
$receiptPath = Join-Path $OutputRoot ('C11-C_2.19.12_FROZEN_PACKAGE_RECEIPT_' + $stamp + '.json')
$sidecar | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $receiptPath -Encoding UTF8

Write-Host ('[C11C-FREEZE-ZIP] PASS - archive=' + $zipPath)
Write-Host ('[C11C-FREEZE-ZIP] SHA-256=' + $zipHash)
Write-Host ('[C11C-FREEZE-ZIP] TREE SHA-256=' + $treeSha)
Write-Host ('[C11C-FREEZE-ZIP] build_factory.py SHA-256=' + $buildFactoryHash)
Write-Host ('[C11C-FREEZE-ZIP] SOURCE FILES=' + @($entries).Count)
Write-Host ('[C11C-FREEZE-ZIP] EVIDENCE FILES=' + @($evidenceEntries).Count)
Write-Host ('[C11C-FREEZE-ZIP] RECEIPT=' + $receiptPath)
exit 0
