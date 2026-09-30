[CmdletBinding()]
param(
    [string]$OutputRoot = '',
    [switch]$AllowWithoutAcceptance
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
New-Item -ItemType Directory -Path $OutputRoot -Force | Out-Null

$acceptancePath = Join-Path $root 'artifacts\tests\reports\C11C_2.19.12_ACCEPTANCE_REPORT.json'
if (-not $AllowWithoutAcceptance) {
    if (-not (Test-Path -LiteralPath $acceptancePath -PathType Leaf)) {
        throw 'C11-C freeze blocked: C11C_2.19.12 acceptance report is missing.'
    }
    $acceptance = Get-Content -Raw -LiteralPath $acceptancePath | ConvertFrom-Json
    if ([string]$acceptance.status -ne 'PASS') {
        throw 'C11-C freeze blocked: C11C_2.19.12 acceptance report is not PASS.'
    }
    foreach ($checkName in @('docs_consolidated','suite_self_test','producer_self_test','producer_gui','launcher_audit','parallel_contract','envelope_path_contract','one_video_smoke','retro_reference','logical','c11a1','retro','physical_smoke','physical_export','video_review')) {
        $prop = $acceptance.checks.PSObject.Properties[$checkName]
        if ($null -eq $prop -or $prop.Value -ne $true) {
            throw ('C11-C freeze blocked: acceptance check is not PASS: ' + $checkName)
        }
    }
}

$buildFactory = Join-Path $root 'build_factory.py'
if (-not (Test-Path -LiteralPath $buildFactory -PathType Leaf)) { throw 'C11-C freeze blocked: build_factory.py is missing.' }
if ((Get-Item -LiteralPath $buildFactory).Length -eq 0) {
    throw 'C11-C freeze blocked: build_factory.py is empty. Restore the last historical copy before sealing the release.'
}

$override = Join-Path $root 'override.cfg'
if (Test-Path -LiteralPath $override -PathType Leaf) {
    throw 'C11-C freeze blocked: repository root override.cfg is present.'
}
$leaked = @(Get-ChildItem -LiteralPath $root -Filter '.override.challenge_quarantine_*.cfg' -File -ErrorAction SilentlyContinue)
if ($leaked.Count -gt 0) { throw 'C11-C freeze blocked: override quarantine residue exists in repository root.' }

$required = @(
    'project.godot',
    'GeneradorMaestro.gd',
    'build_factory.py',
    'release_gate.py',
    'tests/run_all.py',
    'FULL_ACCEPTANCE_C11C_2.19.12.ps1',
    'docs/current/c11c/C11-C_2.19_CONSOLIDATED_STATE.md',
    'docs/current/c11c/C11-C_2.19_CONSOLIDATED_ACCEPTANCE_GATE.md',
    'docs/current/d/C11-D_ROADMAP_V1.0_STATELESS.md',
    'docs/master-prompts/MASTER_HANDOVER_C11D_V1.0_STATELESS.md',
    'docs/master-prompts/START_PROMPT_C11D_V1.0_STATELESS.md',
    'c11c-suite/self_test.py',
    'c11c-suite/c11c-producer/self_test.py',
    'c11c-suite/c11c-maintenance/main.py'
)
$missing = @($required | Where-Object { -not (Test-Path -LiteralPath (Join-Path $root $_) -PathType Leaf) })
if ($missing.Count -gt 0) { throw ('C11-C freeze blocked: missing required files: ' + ($missing -join ', ')) }

$stamp = Get-Date -Format 'yyyyMMdd_HHmmss'
$zipName = "ChallengeEngineV01_STATELESS_C11-C_2.19.12_FROZEN_$stamp.zip"
$zipPath = Join-Path $OutputRoot $zipName
$tempManifest = Join-Path ([IO.Path]::GetTempPath()) ('c11c_freeze_manifest_' + [guid]::NewGuid().ToString('N') + '.json')

$excludeDirNames = @('.git','.godot','.mono','.import','.vscode','.idea','__pycache__','.pytest_cache','.mypy_cache','.ruff_cache','.venv','venv','env','artifacts','c11c-studio')
$excludeFiles = @('*.pyc','*.pyo','*.pyd','*.uid','*.import','*.tmp','*.temp','*.bak','*.old','*.orig','*.swp','*.swo','*~','*.zip','*.7z','*.rar','.DS_Store','Thumbs.db','Desktop.ini')

$files = @(Get-ChildItem -LiteralPath $root -Recurse -File -Force | Where-Object {
    $rel = $_.FullName.Substring($root.Length + 1).Replace('\','/')
    $parts = $rel.Split('/')
    if ($parts | Where-Object { $excludeDirNames -contains $_ }) { return $false }
    foreach ($pattern in $excludeFiles) { if ($_.Name -like $pattern) { return $false } }
    return $true
}) | Sort-Object FullName

$entries = @($files | ForEach-Object {
    $rel = $_.FullName.Substring($root.Length + 1).Replace('\','/')
    [pscustomobject]@{
        path = $rel
        bytes = [int64]$_.Length
        sha256 = (Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
    }
})

$treeLines = ($entries | ForEach-Object { '{0}|{1}|{2}' -f $_.path,$_.bytes,$_.sha256 }) -join "`n"
$tmpTree = Join-Path ([IO.Path]::GetTempPath()) ('c11c_freeze_tree_' + [guid]::NewGuid().ToString('N') + '.txt')
[IO.File]::WriteAllText($tmpTree,$treeLines,(New-Object Text.UTF8Encoding($false)))
$treeSha = (Get-FileHash -LiteralPath $tmpTree -Algorithm SHA256).Hash.ToLowerInvariant()
Remove-Item -LiteralPath $tmpTree -Force

$manifest = [ordered]@{
    schema='C11-C-FROZEN-PACKAGE-V1'
    release='C11-C 2.19.12'
    generated_at_utc=(Get-Date).ToUniversalTime().ToString('o')
    source_root='repository root'
    acceptance_report=if(Test-Path -LiteralPath $acceptancePath -PathType Leaf){'artifacts/tests/reports/C11C_2.19.12_ACCEPTANCE_REPORT.json'}else{$null}
    acceptance_enforced=(-not $AllowWithoutAcceptance)
    hash_algorithm='SHA-256'
    tree_sha256=$treeSha
    file_count=$entries.Count
    excluded_directory_names=$excludeDirNames
    excluded_file_patterns=$excludeFiles
    files=$entries
}
$manifestJson = $manifest | ConvertTo-Json -Depth 8
[IO.File]::WriteAllText($tempManifest,$manifestJson,(New-Object Text.UTF8Encoding($false)))

Add-Type -AssemblyName System.IO.Compression
Add-Type -AssemblyName System.IO.Compression.FileSystem
if (Test-Path -LiteralPath $zipPath) { Remove-Item -LiteralPath $zipPath -Force }
$zip = [System.IO.Compression.ZipFile]::Open($zipPath,'Create')
try {
    foreach ($item in $files) {
        $entryName = $item.FullName.Substring($root.Length + 1).Replace('\','/')
        [System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile($zip,$item.FullName,$entryName) | Out-Null
    }
    [System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile($zip,$tempManifest,'release/C11C_FREEZE_PACKAGE_MANIFEST.json') | Out-Null
} finally {
    $zip.Dispose()
}
Remove-Item -LiteralPath $tempManifest -Force -ErrorAction SilentlyContinue

$zip = [System.IO.Compression.ZipFile]::OpenRead($zipPath)
try {
    $entryNames = @($zip.Entries | ForEach-Object { $_.FullName })
    $badEntries = @($entryNames | Where-Object { $_.StartsWith('/') -or $_.Contains('..') -or $_.ToLowerInvariant().StartsWith('artifacts/') -or $_.ToLowerInvariant().Contains('c11c-studio') -or $_.ToLowerInvariant().Contains('/__pycache__/') -or $_.ToLowerInvariant().EndsWith('.pyc') })
    if ($badEntries.Count -gt 0) { throw ('C11-C freeze ZIP validation failed: forbidden entries: ' + ($badEntries -join ', ')) }
    foreach ($requiredEntry in $required) {
        $normalized = $requiredEntry.Replace('\','/')
        if ($entryNames -notcontains $normalized) { throw ('C11-C freeze ZIP validation failed: missing entry: ' + $normalized) }
    }
    if ($entryNames -notcontains 'release/C11C_FREEZE_PACKAGE_MANIFEST.json') { throw 'C11-C freeze ZIP validation failed: package manifest entry missing.' }
    if ($entryNames.Count -lt $entries.Count + 1) { throw 'C11-C freeze ZIP validation failed: archive entry count is unexpectedly small.' }
} finally {
    $zip.Dispose()
}
$zipHash = (Get-FileHash -LiteralPath $zipPath -Algorithm SHA256).Hash.ToLowerInvariant()
$sidecar = [ordered]@{ schema='C11-C-FROZEN-PACKAGE-RECEIPT-V1'; release='C11-C 2.19.12'; archive=$zipName; archive_sha256=$zipHash; tree_sha256=$treeSha; file_count=$entries.Count; generated_at_utc=(Get-Date).ToUniversalTime().ToString('o') }
$receiptPath = Join-Path $OutputRoot ('C11-C_2.19.12_FROZEN_PACKAGE_RECEIPT_' + $stamp + '.json')
$sidecar | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $receiptPath -Encoding UTF8

Write-Host ('[C11C-FREEZE-ZIP] PASS - archive=' + $zipPath)
Write-Host ('[C11C-FREEZE-ZIP] SHA-256=' + $zipHash)
Write-Host ('[C11C-FREEZE-ZIP] TREE SHA-256=' + $treeSha)
Write-Host ('[C11C-FREEZE-ZIP] FILES=' + $entries.Count)
Write-Host ('[C11C-FREEZE-ZIP] RECEIPT=' + $receiptPath)
exit 0
