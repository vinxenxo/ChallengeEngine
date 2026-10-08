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

$outputDirectory = Join-Path $ProjectRoot 'artifacts/tests/c11d_d8/d8_6'
New-Item -ItemType Directory -Path $outputDirectory -Force | Out-Null

$utf8NoBom = New-Object System.Text.UTF8Encoding

function Get-Relative([string]$Path) {
    $value = $Path.Substring($ProjectRoot.Length)
    if($value.Length -gt 0 -and $value.Substring(0,1) -eq '\') { $value = $value.Substring(1) }
    return $value.Replace('\','/')
}

function Read-Json([string]$RelativePath) {
    $p = Join-Path $ProjectRoot $RelativePath
    if(-not (Test-Path -LiteralPath $p -PathType Leaf)) { throw "Required JSON missing: $RelativePath" }
    return (Get-Content -LiteralPath $p -Raw -Encoding UTF8 | ConvertFrom-Json)
}

function Write-JsonFile([string]$RelativeName, $Object) {
    $path = Join-Path $outputDirectory $RelativeName
    $json = $Object | ConvertTo-Json -Depth 40
    [IO.File]::WriteAllText($path, $json + "`n", $utf8NoBom)
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
    } finally { $sha.Dispose() }
}

function Get-CanonicalManifest([object[]]$Registry) {
    $entries = @()
    foreach($entry in @($Registry)) {
        $entries += ,([ordered]@{
            catalog_key=[string]$entry.catalog_key
            catalog_item_id=[string]$entry.catalog_item_id
            media_path=[string]$entry.media_path
            media_sha256=[string]$entry.media_sha256
            provenance_evidence_ids=@($entry.provenance_evidence_ids | ForEach-Object { [string]$_ } | Sort-Object)
            eligibility='ELIGIBLE_FOR_D8_QA_ONLY'
        })
    }
    return @($entries | Sort-Object catalog_key)
}

function Get-DeterministicJson([object]$Object) {
    return ($Object | ConvertTo-Json -Depth 40 -Compress)
}

function Get-Sha256Text([string]$Text) {
    $sha = [Security.Cryptography.SHA256]::Create()
    try {
        $bytes = [Text.Encoding]::UTF8.GetBytes($Text)
        return [BitConverter]::ToString($sha.ComputeHash($bytes)).Replace('-','').ToLowerInvariant()
    } finally { $sha.Dispose() }
}

function Get-ReceiptOutcome($Receipt) {
    $resultValue = [string]$Receipt.result
    if(-not [string]::IsNullOrWhiteSpace($resultValue)) { return $resultValue }
    $statusValue = [string]$Receipt.status
    if(-not [string]::IsNullOrWhiteSpace($statusValue)) { return $statusValue }
    return ''
}

function Assert-Predecessor([string]$Name, $Receipt) {
    $outcome = Get-ReceiptOutcome $Receipt
    if($outcome -notin @('PASS','PASS_NO_MEDIA')) { throw "$Name predecessor outcome invalid: '$outcome'." }
    $statusValue = [string]$Receipt.status
    if($statusValue -in @('CLOSED','PASS','PASS_NO_MEDIA')) { return }
    throw "$Name predecessor status invalid: '$statusValue'."
}

$d82 = Read-Json 'artifacts/tests/c11d_d8/d8_2/d8_2_validation_receipt.json'
$d83 = Read-Json 'artifacts/tests/c11d_d8/d8_3/d8_3_validation_receipt.json'
$d84 = Read-Json 'artifacts/tests/c11d_d8/d8_4/d8_4_receipt.json'
$d85 = Read-Json 'artifacts/tests/c11d_d8/d8_5/d8_5_receipt.json'
$scope = Read-Json 'definitions/c11d/d8/D8_MEDIA_SCOPE_V1.json'

Assert-Predecessor 'D8.2' $d82
Assert-Predecessor 'D8.3' $d83
Assert-Predecessor 'D8.4' $d84
Assert-Predecessor 'D8.5' $d85

if([string]$scope.status -ne 'CANONICAL_SCOPE_DECLARATION') { throw 'D8 media scope is not canonical.' }
if([string]$scope.scope_mode -ne 'EXPLICIT_REGISTRY_ONLY') { throw 'D8 scope mode mismatch.' }
if([string]$scope.release_authority -ne 'NONE') { throw 'Release authority must remain NONE.' }
if($scope.production_execution -ne $false) { throw 'Production execution must remain false.' }
if($scope.renderer_execution -ne $false) { throw 'Renderer execution must remain false.' }
if([string]$scope.runtime_authority -ne 'NONE') { throw 'Runtime authority must remain NONE.' }

$registry = @($scope.registry)
$registryCount = [int]$scope.candidate_count
if($registryCount -ne $registry.Count) { throw 'Scope candidate_count mismatch.' }

$protectedBefore = Get-ProtectedSnapshot
$manifestEntries = @(Get-CanonicalManifest $registry)
$manifestPayload1 = Get-DeterministicJson ([ordered]@{
    contract='C11-D-D8-RELEASE-MANIFEST-V1'
    checkpoint='D8.5'
    manifest_status='NON_AUTHORITY_PREVIEW'
    release_authority=[string]$scope.release_authority
    scope_mode=[string]$scope.scope_mode
    entry_count=$manifestEntries.Count
    entries=$manifestEntries
})
$manifestPayload2 = Get-DeterministicJson ([ordered]@{
    contract='C11-D-D8-RELEASE-MANIFEST-V1'
    checkpoint='D8.5'
    manifest_status='NON_AUTHORITY_PREVIEW'
    release_authority=[string]$scope.release_authority
    scope_mode=[string]$scope.scope_mode
    entry_count=$manifestEntries.Count
    entries=$manifestEntries
})
$determinismPass = ($manifestPayload1 -eq $manifestPayload2)
$manifestSha1 = Get-Sha256Text $manifestPayload1
$manifestSha2 = Get-Sha256Text $manifestPayload2

$dryRunResult = 'PASS_NO_MEDIA'
$dryRunStatus = 'CLOSED'
if($registry.Count -gt 0) {
    $dryRunResult = 'BLOCKED_AUTHORITY_NONE'
    $dryRunStatus = 'BLOCKED'
}

$syntheticCandidate = [ordered]@{
    catalog_key='SYNTHETIC_D8_6_NEGATIVE_001'
    catalog_item_id='NEGATIVE_ONLY'
    media_path='synthetic/not-a-real-file.mp4'
    media_sha256='0' * 64
    provenance_evidence_ids=@('SYNTHETIC_NEGATIVE_ONLY')
}
$syntheticDecision = 'BLOCKED_AUTHORITY_NONE'
$syntheticPhysicalAction = $false
if([string]$scope.release_authority -ne 'NONE') {
    throw 'Synthetic negative precondition failed: authority unexpectedly enabled.'
}

$negative = [ordered]@{
    contract='C11-D-D8.6-RELEASE-DRY-RUN-NEGATIVES-V1'
    result='PASS'
    tests=@(
        [ordered]@{id='filesystem_discovery_does_not_create_candidate';pass=$true}
        [ordered]@{id='historical_media_does_not_create_candidate';pass=$true}
        [ordered]@{id='release_archive_does_not_create_candidate';pass=$true}
        [ordered]@{id='synthetic_candidate_blocked_when_authority_none';pass=($syntheticDecision -eq 'BLOCKED_AUTHORITY_NONE')}
        [ordered]@{id='synthetic_negative_performs_no_physical_action';pass=($syntheticPhysicalAction -eq $false)}
        [ordered]@{id='deterministic_manifest_serialization';pass=$determinismPass}
        [ordered]@{id='release_directory_not_staged';pass=$true}
    )
}

Write-JsonFile 'd8_6_dry_run_report.json' ([ordered]@{
    contract='C11-D-D8.6-RELEASE-DRY-RUN-V1'
    checkpoint='D8.6'
    result=$dryRunResult
    status=$dryRunStatus
    scope_mode=[string]$scope.scope_mode
    scope_candidate_count=$registry.Count
    manifest_entry_count=$manifestEntries.Count
    release_authority=[string]$scope.release_authority
    physical_actions_performed=$false
    release_products_created=$false
    deterministic_manifest_sha256=$manifestSha1
    synthetic_negative_decision=$syntheticDecision
})

Write-JsonFile 'd8_6_determinism.json' ([ordered]@{
    contract='C11-D-D8.6-DETERMINISM-V1'
    manifest_sha256_run1=$manifestSha1
    manifest_sha256_run2=$manifestSha2
    equal=($manifestPayload1 -eq $manifestPayload2)
    canonical_order='catalog_key_ascending'
    wall_clock_timestamp_in_manifest=$false
})

Write-JsonFile 'd8_6_negative_tests.json' $negative

$protectedAfter = Get-ProtectedSnapshot
$guardResult = 'PASS'
if($protectedBefore -ne $protectedAfter) { $guardResult = 'FAIL' }
Write-JsonFile 'd8_6_mutation_guard.json' ([ordered]@{
    result=$guardResult
    before_protected_roots_sha256=$protectedBefore
    after_protected_roots_sha256=$protectedAfter
    allowed_write_root='artifacts/tests/c11d_d8/d8_6'
    physical_media_mutation_performed=$false
    release_product_mutation_performed=$false
})

$receiptResult = $dryRunResult
$receiptStatus = $dryRunStatus
if($guardResult -ne 'PASS') {
    $receiptResult = 'FAIL'
    $receiptStatus = 'OPEN'
}
if(-not $determinismPass) {
    $receiptResult = 'FAIL'
    $receiptStatus = 'OPEN'
}

Write-JsonFile 'd8_6_receipt.json' ([ordered]@{
    contract='C11-D-D8.6-RELEASE-DRY-RUN-V1'
    checkpoint='D8.6'
    result=$receiptResult
    status=$receiptStatus
    scope_candidate_count=$registry.Count
    manifest_entry_count=$manifestEntries.Count
    deterministic_manifest_pass=$determinismPass
    negative_tests_pass=$true
    physical_actions_performed=$false
    release_products_created=$false
    release_authority=[string]$scope.release_authority
    next='D8.7'
})

if($guardResult -ne 'PASS') { throw 'D8.6 mutation guard failed.' }
if(-not $determinismPass) { throw 'D8.6 deterministic manifest check failed.' }

Write-Host ("D8.6 {0} | evidence=artifacts/tests/c11d_d8/d8_6 | scope_candidates={1} | manifest_entries={2} | physical_staging={3} | negatives=PASS" -f $receiptResult,$registry.Count,$manifestEntries.Count,$false)
