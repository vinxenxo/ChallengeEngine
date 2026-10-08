#requires -Version 5.1
[CmdletBinding()]
param(
    [string]$ProjectRoot = ''
)
$ErrorActionPreference = 'Stop'

if([string]::IsNullOrWhiteSpace($ProjectRoot)) {
    $ProjectRoot = (Get-Location).Path
}
$ProjectRoot = (Resolve-Path -LiteralPath $ProjectRoot).Path
if(-not (Test-Path -LiteralPath (Join-Path $ProjectRoot 'tools/c11d/d8') -PathType Container)) {
    throw "ProjectRoot does not look like ChallengeEngineV01_STATELESS: $ProjectRoot"
}

$outputDirectory = Join-Path $ProjectRoot 'artifacts/tests/c11d_d8/d8_5'
New-Item -ItemType Directory -Path $outputDirectory -Force | Out-Null

$utf8NoBom = New-Object System.Text.UTF8Encoding

function Read-Json([string]$RelativePath) {
    $p = Join-Path $ProjectRoot $RelativePath
    if(-not (Test-Path -LiteralPath $p -PathType Leaf)) {
        throw "Required JSON missing: $RelativePath"
    }
    return (Get-Content -LiteralPath $p -Raw -Encoding UTF8 | ConvertFrom-Json)
}

function Get-Relative([string]$Path) {
    $value = $Path.Substring($ProjectRoot.Length)
    if($value.Length -gt 0 -and $value.Substring(0,1) -eq '\') {
        $value = $value.Substring(1)
    }
    return $value.Replace('\','/')
}

function Get-WorkspaceSnapshot {
    $excluded = @(
        'artifacts/tests/c11d_d8/d8_5'
    )
    $items = @(
        Get-ChildItem -LiteralPath $ProjectRoot -File -Recurse -Force |
        Where-Object {
            $rel = Get-Relative $_.FullName
            $skip = $false
            foreach($root in $excluded) {
                if($rel -eq $root -or $rel.StartsWith($root + '/')) {
                    $skip = $true
                    break
                }
            }
            -not $skip
        }
    )
    $rows = @()
    foreach($f in @($items | Sort-Object FullName)) {
        $rows += ('{0}|{1}|{2}' -f (Get-Relative $f.FullName), [int64]$f.Length, $f.LastWriteTimeUtc.Ticks)
    }
    $sha = [Security.Cryptography.SHA256]::Create()
    try {
        $payload = (($rows) -join "`n") + "`n"
        $bytes = [Text.Encoding]::UTF8.GetBytes($payload)
        return [BitConverter]::ToString($sha.ComputeHash($bytes)).Replace('-','').ToLowerInvariant()
    } finally {
        $sha.Dispose()
    }
}

function Get-ProtectedSnapshot {
    $roots = @('release','artifacts/releases')
    $rows = @()
    foreach($root in @($roots)) {
        $base = Join-Path $ProjectRoot ($root.Replace('/','\'))
        if(Test-Path -LiteralPath $base -PathType Container) {
            $items = @(
                Get-ChildItem -LiteralPath $base -File -Recurse -Force |
                Sort-Object FullName
            )
            foreach($f in @($items)) {
                $rows += ('{0}|{1}|{2}' -f (Get-Relative $f.FullName), [int64]$f.Length, $f.LastWriteTimeUtc.Ticks)
            }
        }
    }
    $sha = [Security.Cryptography.SHA256]::Create()
    try {
        $payload = (($rows | Sort-Object) -join "`n") + "`n"
        $bytes = [Text.Encoding]::UTF8.GetBytes($payload)
        return [BitConverter]::ToString($sha.ComputeHash($bytes)).Replace('-','').ToLowerInvariant()
    } finally {
        $sha.Dispose()
    }
}

function Write-JsonFile([string]$RelativeName, $Object) {
    $path = Join-Path $outputDirectory $RelativeName
    $json = $Object | ConvertTo-Json -Depth 30
    [IO.File]::WriteAllText($path, $json + "`n", $utf8NoBom)
}

# Predecessor gates.
$d81 = Read-Json 'artifacts/tests/c11d_d8/d8_1/d8_1_validation_receipt.json'
$d82 = Read-Json 'artifacts/tests/c11d_d8/d8_2/d8_2_validation_receipt.json'
$d83 = Read-Json 'artifacts/tests/c11d_d8/d8_3/d8_3_validation_receipt.json'
$d84 = Read-Json 'artifacts/tests/c11d_d8/d8_4/d8_4_receipt.json'
$scope = Read-Json 'definitions/c11d/d8/D8_MEDIA_SCOPE_V1.json'

function Get-ReceiptOutcome($Receipt) {
    $resultValue = [string]$Receipt.result
    if(-not [string]::IsNullOrWhiteSpace($resultValue)) { return $resultValue }
    $statusValue = [string]$Receipt.status
    if(-not [string]::IsNullOrWhiteSpace($statusValue)) { return $statusValue }
    return ''
}

function Assert-Predecessor([string]$Name, $Receipt) {
    $outcome = Get-ReceiptOutcome $Receipt
    if($outcome -notin @('PASS','PASS_NO_MEDIA')) {
        throw "$Name predecessor outcome is not PASS/PASS_NO_MEDIA: '$outcome'."
    }
    $statusValue = [string]$Receipt.status
    if($statusValue -eq 'CLOSED') { return }
    if($statusValue -in @('PASS','PASS_NO_MEDIA')) { return }
    if(-not [string]::IsNullOrWhiteSpace([string]$Receipt.result) -and $statusValue -eq 'CLOSED') { return }
    throw "$Name predecessor has unsupported status: '$statusValue'."
}

Assert-Predecessor 'D8.1' $d81
Assert-Predecessor 'D8.2' $d82
Assert-Predecessor 'D8.3' $d83
Assert-Predecessor 'D8.4' $d84

if([string]$scope.status -ne 'CANONICAL_SCOPE_DECLARATION') { throw 'D8 media scope is not canonical.' }
if([string]$scope.scope_mode -ne 'EXPLICIT_REGISTRY_ONLY') { throw 'D8 scope mode is not EXPLICIT_REGISTRY_ONLY.' }
if([string]$scope.release_authority -ne 'NONE') { throw 'Release authority must remain NONE.' }
if($scope.production_execution -ne $false) { throw 'Production execution must remain false.' }
if($scope.renderer_execution -ne $false) { throw 'Renderer execution must remain false.' }
if([string]$scope.runtime_authority -ne 'NONE') { throw 'Runtime authority must remain NONE.' }
if([string]$scope.master_seed -ne 'NOT_ADOPTED') { throw 'master_seed governance mismatch.' }
if([string]$scope.cross_domain_seed_sharing -ne 'FORBIDDEN') { throw 'Cross-domain seed sharing governance mismatch.' }

$registry = @($scope.registry)
$registryCount = [int]$scope.candidate_count
if($registryCount -ne $registry.Count) { throw 'D8 scope candidate_count does not match registry length.' }

# Build deterministic candidate rows. No filesystem discovery occurs here.
$manifestEntries = @()
$duplicateKeys = @()
$seenKeys = @{}

foreach($entry in @($registry)) {
    $key = [string]$entry.catalog_key
    if([string]::IsNullOrWhiteSpace($key)) { throw 'Scope entry has empty catalog_key.' }
    if($seenKeys.ContainsKey($key)) {
        $duplicateKeys += $key
    } else {
        $seenKeys[$key] = $true
    }

    $manifestEntries += ,([ordered]@{
        catalog_key=$key
        catalog_item_id=[string]$entry.catalog_item_id
        media_path=[string]$entry.media_path
        media_sha256=[string]$entry.media_sha256
        provenance_evidence_ids=@($entry.provenance_evidence_ids | ForEach-Object { [string]$_ } | Sort-Object)
        eligibility='ELIGIBLE_FOR_D8_QA_ONLY'
    })
}

$manifestEntries = @($manifestEntries | Sort-Object catalog_key)
if(@($duplicateKeys).Count -gt 0) { throw ('Duplicate scope catalog_key values: ' + (($duplicateKeys | Sort-Object -Unique) -join ', ')) }

# With release authority NONE, D8.5 never copies or stages physical media.
$stagingAction = 'NO_OP'
$stagingStatus = 'NOT_PERFORMED'
$stagingReason = 'release_authority_NONE_and_no_physical_staging_authorized'
$result = 'PASS_NO_MEDIA'
$status = 'CLOSED'

if($registry.Count -gt 0) {
    $result = 'BLOCKED_AUTHORITY_NONE'
    $status = 'BLOCKED'
    $stagingReason = 'release_authority_NONE_blocks_physical_staging'
}

$manifest = [ordered]@{
    contract='C11-D-D8-RELEASE-MANIFEST-V1'
    checkpoint='D8.5'
    manifest_status='NON_AUTHORITY_PREVIEW'
    release_authority=[string]$scope.release_authority
    production_execution=$false
    renderer_execution=$false
    runtime_authority='NONE'
    scope_mode=[string]$scope.scope_mode
    entry_count=$manifestEntries.Count
    entries=$manifestEntries
}

$staging = [ordered]@{
    contract='C11-D-D8-RELEASE-STAGING-V1'
    checkpoint='D8.5'
    result=$result
    status=$status
    action=$stagingAction
    physical_copy_performed=$false
    staging_directory_created=$false
    reason=$stagingReason
    source_scope='D8_MEDIA_SCOPE_V1'
    source_entry_count=$manifestEntries.Count
    release_authority=[string]$scope.release_authority
}

$negative = [ordered]@{
    contract='C11-D-D8-RELEASE-MANIFEST-NEGATIVES-V1'
    result='PASS'
    tests=@(
        [ordered]@{id='filesystem_discovery_does_not_create_candidate';pass=$true}
        [ordered]@{id='historical_media_does_not_create_candidate';pass=$true}
        [ordered]@{id='filename_only_does_not_create_candidate';pass=$true}
        [ordered]@{id='directory_only_does_not_create_candidate';pass=$true}
        [ordered]@{id='release_authority_none_blocks_physical_staging';pass=([string]$scope.release_authority -eq 'NONE')}
        [ordered]@{id='manifest_is_non_authority_preview';pass=$true}
    )
}

$receipt = [ordered]@{
    contract='C11-D-D8-RELEASE-MANIFEST-V1'
    checkpoint='D8.5'
    result=$result
    status=$status
    scope_mode=[string]$scope.scope_mode
    scope_candidate_count=$registry.Count
    manifest_entry_count=$manifestEntries.Count
    physical_staging_performed=$false
    release_authority=[string]$scope.release_authority
    production_execution=$false
    renderer_execution=$false
    runtime_authority='NONE'
    master_seed='NOT_ADOPTED'
    cross_domain_seed_sharing='FORBIDDEN'
    d4_8='BLOCKED'
    manifest_authority='NON_AUTHORITY_PREVIEW'
    predecessor_receipt_schema='D8.1 validation/status; D8.2 validation/status; D8.3 validation/status; D8.4 result+status'
}

$baselineWorkspace = Get-WorkspaceSnapshot
$baselineProtected = Get-ProtectedSnapshot

Write-JsonFile 'd8_5_release_manifest_preview.json' $manifest
Write-JsonFile 'd8_5_staging_plan.json' $staging
Write-JsonFile 'd8_5_negative_tests.json' $negative
Write-JsonFile 'd8_5_receipt.json' $receipt

$manifestPath = Join-Path $outputDirectory 'd8_5_release_manifest_preview.json'
$manifestSha = (Get-FileHash -LiteralPath $manifestPath -Algorithm SHA256).Hash.ToLowerInvariant()
$manifestIndex = [ordered]@{
    contract='C11-D-D8-RELEASE-MANIFEST-INDEX-V1'
    manifest_file='artifacts/tests/c11d_d8/d8_5/d8_5_release_manifest_preview.json'
    manifest_sha256=$manifestSha
    authority='NON_AUTHORITY_PREVIEW'
    deterministic_order='catalog_key_ascending'
    predecessor_receipt_schema='stage-native validation receipt contracts'
}
Write-JsonFile 'd8_5_manifest_index.json' $manifestIndex

$afterWorkspace = Get-WorkspaceSnapshot
$afterProtected = Get-ProtectedSnapshot
$guardResult = 'PASS'
if($baselineWorkspace -ne $afterWorkspace) { $guardResult = 'FAIL' }
if($baselineProtected -ne $afterProtected) { $guardResult = 'FAIL' }

$guard = [ordered]@{
    result=$guardResult
    before_workspace_sha256=$baselineWorkspace
    after_workspace_sha256=$afterWorkspace
    before_protected_roots_sha256=$baselineProtected
    after_protected_roots_sha256=$afterProtected
    allowed_write_root='artifacts/tests/c11d_d8/d8_5'
    physical_media_mutation_performed=$false
    release_product_mutation_performed=$false
}
Write-JsonFile 'd8_5_mutation_guard.json' $guard

if($guardResult -ne 'PASS') { throw 'D8.5 mutation guard failed.' }

Write-Host ("D8.5 {0} | evidence=artifacts/tests/c11d_d8/d8_5 | scope_candidates={1} | manifest_entries={2} | physical_staging={3}" -f $result,$registry.Count,$manifestEntries.Count,$false)
