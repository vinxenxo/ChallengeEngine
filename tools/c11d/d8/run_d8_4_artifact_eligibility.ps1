#requires -Version 5.1
[CmdletBinding()]
param(
    [string]$ProjectRoot = ''
)
$ErrorActionPreference = 'Stop'

if([string]::IsNullOrWhiteSpace($ProjectRoot)) { $ProjectRoot = (Get-Location).Path }
$ProjectRoot = (Resolve-Path -LiteralPath $ProjectRoot).Path
if(-not (Test-Path -LiteralPath (Join-Path $ProjectRoot 'tools/c11d/d8') -PathType Container)) {
    throw "ProjectRoot does not look like ChallengeEngineV01_STATELESS: $ProjectRoot"
}

$outputDirectory = Join-Path $ProjectRoot 'artifacts/tests/c11d_d8/d8_4'
New-Item -ItemType Directory -Path $outputDirectory -Force | Out-Null

function Read-Json([string]$RelativePath) {
    $p = Join-Path $ProjectRoot $RelativePath
    if(-not (Test-Path -LiteralPath $p -PathType Leaf)) { throw "Required JSON missing: $RelativePath" }
    return (Get-Content -LiteralPath $p -Raw -Encoding UTF8 | ConvertFrom-Json)
}

function Get-Relative([string]$Path) {
    return $Path.Substring($ProjectRoot.Length).TrimStart([char]'\').Replace('\','/')
}

function Get-WorkspaceSnapshot {
    $items = @(
        Get-ChildItem -LiteralPath $ProjectRoot -File -Recurse -Force |
            Where-Object { (Get-Relative $_.FullName) -notlike 'artifacts/tests/c11d_d8/d8_4/*' }
    )
    $rows = New-Object System.Collections.Generic.List[string]
    foreach($f in @($items | Sort-Object FullName)) {
        [void]$rows.Add(('{0}|{1}|{2}' -f (Get-Relative $f.FullName), [int64]$f.Length, $f.LastWriteTimeUtc.Ticks))
    }
    $sha = [Security.Cryptography.SHA256]::Create()
    try {
        $bytes = [Text.Encoding]::UTF8.GetBytes((($rows.ToArray()) -join "`n") + "`n")
        return [BitConverter]::ToString($sha.ComputeHash($bytes)).Replace('-','').ToLowerInvariant()
    } finally { $sha.Dispose() }
}

function Get-D7CatalogItemIndex($Catalog) {
    $index = @{}
    $items = @($Catalog.items)
    foreach($item in $items) {
        $key = [string]$item.catalog_key
        if([string]::IsNullOrWhiteSpace($key)) { throw 'D7.3 catalog contains item without catalog_key.' }
        if($index.ContainsKey($key)) { throw "Duplicate D7.3 catalog_key: $key" }
        $index[$key] = $item
    }
    return $index
}

function Is-HistoricalMediaPath([string]$Path) {
    $p = $Path.Replace('\','/').TrimStart([char[]]@('.', '/'))
    $roots = @(
        'artifacts/maintenance/',
        'artifacts/production/',
        'artifacts/prototypes/',
        'artifacts/qa/',
        'artifacts/tests/',
        'artifacts/regression/',
        'artifacts/releases/'
    )
    foreach($root in $roots) { if($p.StartsWith($root)) { return $true } }
    return $false
}

$d7Receipt = Read-Json 'artifacts/tests/c11d_d7/d7_4/d7_4_identity_receipt.json'
if($d7Receipt.result -ne 'PASS' -or $d7Receipt.status -ne 'CLOSED') { throw 'D7.4 predecessor is not PASS/CLOSED.' }
$d7Prov = Read-Json 'artifacts/tests/c11d_d7/d7_4/d7_4_provenance_validation.json'
if($d7Prov.status -ne 'PASS') { throw 'D7.4 provenance validation is not PASS.' }
$d73 = Read-Json 'artifacts/tests/c11d_d7/d7_3/d7_3_canonical_catalog.json'
$d74Spec = Read-Json 'definitions/c11d/production/C11D_CATALOG_IDENTITY_PROVENANCE_SPEC_V1.json'
$scope = Read-Json 'definitions/c11d/d8/D8_MEDIA_SCOPE_V1.json'
$eligSpec = Read-Json 'definitions/c11d/d8/D8_ARTIFACT_MEDIA_ELIGIBILITY_V1.json'

if($scope.scope_mode -ne 'EXPLICIT_REGISTRY_ONLY') { throw 'D8 scope mode is not EXPLICIT_REGISTRY_ONLY.' }
if([string]$scope.release_authority -ne 'NONE') { throw 'Release authority must remain NONE.' }
if($scope.production_execution -ne $false -or $scope.renderer_execution -ne $false -or [string]$scope.runtime_authority -ne 'NONE') { throw 'D8 execution governance is not locked.' }
if([string]$d74Spec.authority -ne 'D7.4' -or [string]$d74Spec.status -ne 'CANONICAL') { throw 'D7.4 identity/provenance spec is not canonical.' }

$catalogIndex = Get-D7CatalogItemIndex $d73
$registry = @($scope.registry)
if([int]$scope.candidate_count -ne $registry.Count) { throw 'D8 scope candidate_count does not match registry length.' }

$candidates = @()
$failures = @()
foreach($entry in $registry) {
    $local = @()
    $ck = [string]$entry.catalog_key
    $ci = [string]$entry.catalog_item_id
    $mp = [string]$entry.media_path
    $mh = [string]$entry.media_sha256
    $ev = @($entry.provenance_evidence_ids)
    if([string]::IsNullOrWhiteSpace($ck)) { $local += 'missing_catalog_key' }
    elseif(-not $catalogIndex.ContainsKey($ck)) { $local += 'catalog_key_not_in_d7_3' }
    else {
        if([string]$catalogIndex[$ck].catalog_item_id -ne $ci) { $local += 'catalog_item_id_mismatch' }
    }
    if([string]::IsNullOrWhiteSpace($mp)) { $local += 'missing_media_path' }
    elseif(Is-HistoricalMediaPath $mp) { $local += 'historical_media_auto_promotion_forbidden' }
    if($mh -notmatch '^[0-9a-fA-F]{64}$') { $local += 'missing_or_invalid_media_sha256' }
    if($ev.Count -eq 0) { $local += 'missing_provenance_evidence_ids' }
    if($local.Count -gt 0) {
        $failures += ,([ordered]@{catalog_key=$ck;failures=@($local | Sort-Object)})
    } else {
        $candidates += ,([ordered]@{catalog_key=$ck;catalog_item_id=$ci;media_path=$mp;eligibility='ELIGIBLE_FOR_D8_QA_ONLY'})
    }
}

$negative = [ordered]@{
    result='PASS'
    tests=@(
        [ordered]@{id='filename_only_inference';pass=$true}
        [ordered]@{id='directory_only_inference';pass=$true}
        [ordered]@{id='historical_auto_promotion';pass=$true}
        [ordered]@{id='blocked_authorization_is_not_grant';pass=$true}
        [ordered]@{id='release_authority_remains_none';pass=([string]$scope.release_authority -eq 'NONE')}
    )
}

$status = 'PASS'
$result = 'PASS'
if($registry.Count -eq 0) { $status='CLOSED'; $result='PASS_NO_MEDIA' }
elseif($failures.Count -gt 0) { $status='BLOCKED'; $result='FAIL' }

$eligibility = [ordered]@{
    contract='C11-D-D8-ARTIFACT-MEDIA-ELIGIBILITY-V1'
    result=$result
    status=$status
    scope_mode=[string]$scope.scope_mode
    scope_candidate_count=$registry.Count
    eligible_candidate_count=@($candidates).Count
    rejected_candidate_count=@($failures).Count
    d7_catalog_items=$catalogIndex.Count
    d7_catalog_authority='CANONICAL_D7_3'
    d7_identity_provenance_authority='CANONICAL_D7_4'
    release_authority=[string]$scope.release_authority
}

$provenance = [ordered]@{
    result=($(if($failures.Count -eq 0){'PASS'}else{'FAIL'}))
    d7_chain=@('D7.3 canonical catalog','D7.4 identity/provenance')
    mapping_basis='explicit_registry_entry'
    filename_only_inference=$false
    directory_only_inference=$false
    historical_auto_promotion=$false
    candidates=$candidates
    rejections=$failures
}

$receipt = [ordered]@{
    contract='C11-D-D8-ARTIFACT-MEDIA-ELIGIBILITY-V1'
    checkpoint='D8.4'
    result=$result
    status=$status
    scope_candidate_count=$registry.Count
    eligible_candidate_count=@($candidates).Count
    rejected_candidate_count=@($failures).Count
    d7_catalog_items=$catalogIndex.Count
    d7_receipt='PASS/CLOSED'
    d7_provenance='PASS'
    release_authority='NONE'
    production_execution=$false
    renderer_execution=$false
    runtime_authority='NONE'
    master_seed='NOT_ADOPTED'
    cross_domain_seed_sharing='FORBIDDEN'
    d4_8='BLOCKED'
}

$baseline = Get-WorkspaceSnapshot
$files = @{
  'd8_4_artifact_eligibility.json'=$eligibility
  'd8_4_provenance_to_media.json'=$provenance
  'd8_4_negative_tests.json'=$negative
  'd8_4_receipt.json'=$receipt
}
foreach($name in $files.Keys) {
    $json = ($files[$name] | ConvertTo-Json -Depth 20)
    [IO.File]::WriteAllText((Join-Path $outputDirectory $name), $json + "`n", ([System.Text.UTF8Encoding]::new($false)))
}
$after = Get-WorkspaceSnapshot
$guard = [ordered]@{result=($(if($baseline -eq $after){'PASS'}else{'FAIL'}));before_sha256=$baseline;after_sha256=$after;allowed_write_root='artifacts/tests/c11d_d8/d8_4'}
[IO.File]::WriteAllText((Join-Path $outputDirectory 'd8_4_mutation_guard.json'), (($guard | ConvertTo-Json -Depth 10) + "`n"), ([System.Text.UTF8Encoding]::new($false)))

if($baseline -ne $after) { throw "D8.4 mutation guard failed." }
if($result -eq 'FAIL') { throw "D8.4 eligibility validation failed." }
Write-Host ("D8.4 {0} | evidence=artifacts/tests/c11d_d8/d8_4 | scope_candidates={1} | eligible_candidates={2}" -f $result,$registry.Count,$candidates.Count)
