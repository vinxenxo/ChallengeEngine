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

$outputDirectory = Join-Path $ProjectRoot 'artifacts/tests/c11d_d8/d8_7'
New-Item -ItemType Directory -Path $outputDirectory -Force | Out-Null
$utf8NoBom = New-Object System.Text.UTF8Encoding

function Read-Json([string]$RelativePath) {
    $p = Join-Path $ProjectRoot $RelativePath
    if(-not (Test-Path -LiteralPath $p -PathType Leaf)) { throw "Required JSON missing: $RelativePath" }
    return (Get-Content -LiteralPath $p -Raw -Encoding UTF8 | ConvertFrom-Json)
}

function Write-JsonFile([string]$RelativeName, $Object) {
    $path = Join-Path $outputDirectory $RelativeName
    $json = $Object | ConvertTo-Json -Depth 50
    [IO.File]::WriteAllText($path, $json + "`n", $utf8NoBom)
}

function Get-ProtectedSnapshot {
    $roots = @('release','artifacts/releases')
    $rows = @()
    foreach($root in @($roots)) {
        $base = Join-Path $ProjectRoot ($root.Replace('/','\'))
        if(Test-Path -LiteralPath $base -PathType Container) {
            $items = @(Get-ChildItem -LiteralPath $base -File -Recurse -Force | Sort-Object FullName)
            foreach($f in @($items)) {
                $rel = $f.FullName.Substring($ProjectRoot.Length)
                if($rel.Length -gt 0 -and $rel.Substring(0,1) -eq '\') { $rel = $rel.Substring(1) }
                $rows += ('{0}|{1}|{2}' -f $rel.Replace('\','/'), [int64]$f.Length, $f.LastWriteTimeUtc.Ticks)
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

function Get-Outcome($Receipt) {
    $resultValue = [string]$Receipt.result
    if(-not [string]::IsNullOrWhiteSpace($resultValue)) { return $resultValue }
    $statusValue = [string]$Receipt.status
    if(-not [string]::IsNullOrWhiteSpace($statusValue)) { return $statusValue }
    return ''
}

function Assert-ClosedPass([string]$Name, $Receipt) {
    $outcome = Get-Outcome $Receipt
    $status = [string]$Receipt.status
    if($outcome -notin @('PASS','PASS_NO_MEDIA')) { throw "$Name outcome invalid: '$outcome'." }
    if($status -notin @('PASS','PASS_NO_MEDIA','CLOSED')) { throw "$Name status invalid: '$status'." }
}

$d80 = Read-Json 'artifacts/tests/c11d_d8/d8_0/d8_0_receipt.json'
$d81 = Read-Json 'artifacts/tests/c11d_d8/d8_1/d8_1_validation_receipt.json'
$d82 = Read-Json 'artifacts/tests/c11d_d8/d8_2/d8_2_validation_receipt.json'
$d83 = Read-Json 'artifacts/tests/c11d_d8/d8_3/d8_3_validation_receipt.json'
$d84 = Read-Json 'artifacts/tests/c11d_d8/d8_4/d8_4_receipt.json'
$d85 = Read-Json 'artifacts/tests/c11d_d8/d8_5/d8_5_receipt.json'
$d86 = Read-Json 'artifacts/tests/c11d_d8/d8_6/d8_6_receipt.json'
$scope = Read-Json 'definitions/c11d/d8/D8_MEDIA_SCOPE_V1.json'

Assert-ClosedPass 'D8.0' $d80
Assert-ClosedPass 'D8.1' $d81
Assert-ClosedPass 'D8.2' $d82
Assert-ClosedPass 'D8.3' $d83
Assert-ClosedPass 'D8.4' $d84
Assert-ClosedPass 'D8.5' $d85
Assert-ClosedPass 'D8.6' $d86

if([string]$scope.scope_mode -ne 'EXPLICIT_REGISTRY_ONLY') { throw 'Canonical D8 scope mode mismatch.' }
if([string]$scope.release_authority -ne 'NONE') { throw 'Release authority is not NONE.' }
if($scope.production_execution -ne $false) { throw 'Production execution is not false.' }
if($scope.renderer_execution -ne $false) { throw 'Renderer execution is not false.' }
if([string]$scope.runtime_authority -ne 'NONE') { throw 'Runtime authority is not NONE.' }
if([string]$scope.master_seed -ne 'NOT_ADOPTED') { throw 'master_seed state mismatch.' }
if([string]$scope.cross_domain_seed_sharing -ne 'FORBIDDEN') { throw 'cross-domain seed sharing state mismatch.' }

$registry = @($scope.registry)
$registryCount = [int]$scope.candidate_count
if($registryCount -ne $registry.Count) { throw 'Scope candidate count mismatch.' }

$protectedBefore = Get-ProtectedSnapshot

$predecessors = @(
    [ordered]@{phase='D8.0';result=(Get-Outcome $d80);status=[string]$d80.status},
    [ordered]@{phase='D8.1';result=(Get-Outcome $d81);status=[string]$d81.status},
    [ordered]@{phase='D8.2';result=(Get-Outcome $d82);status=[string]$d82.status},
    [ordered]@{phase='D8.3';result=(Get-Outcome $d83);status=[string]$d83.status},
    [ordered]@{phase='D8.4';result=(Get-Outcome $d84);status=[string]$d84.status},
    [ordered]@{phase='D8.5';result=(Get-Outcome $d85);status=[string]$d85.status},
    [ordered]@{phase='D8.6';result=(Get-Outcome $d86);status=[string]$d86.status}
)

$mediaDependentState = 'PASS_NO_MEDIA'
if($registry.Count -gt 0) { $mediaDependentState = 'PASS' }

$acceptance = [ordered]@{
    contract='C11-D-D8-ACCEPTANCE-FREEZE-V1'
    checkpoint='D8.7'
    result=$mediaDependentState
    status='CLOSED'
    d8_control_plane='ACCEPTED'
    d8_freeze='AUTHORIZED_BY_D8_7_ACCEPTANCE_ONLY'
    scope_mode=[string]$scope.scope_mode
    scope_candidate_count=$registry.Count
    media_dependent_acceptance=$mediaDependentState
    release_authority=[string]$scope.release_authority
    production_execution=$false
    renderer_execution=$false
    runtime_authority=[string]$scope.runtime_authority
    master_seed=[string]$scope.master_seed
    cross_domain_seed_sharing=[string]$scope.cross_domain_seed_sharing
    predecessors=$predecessors
    no_media_actions_performed=$true
}

Write-JsonFile 'd8_7_acceptance_report.json' $acceptance
Write-JsonFile 'd8_7_predecessor_matrix.json' ([ordered]@{contract='C11-D-D8.7-PREDECESSOR-MATRIX-V1';phases=$predecessors;all_pass=$true})

$protectedAfter = Get-ProtectedSnapshot
$guard = 'PASS'
if($protectedBefore -ne $protectedAfter) { $guard = 'FAIL' }
Write-JsonFile 'd8_7_mutation_guard.json' ([ordered]@{
    result=$guard
    before_protected_roots_sha256=$protectedBefore
    after_protected_roots_sha256=$protectedAfter
    allowed_write_root='artifacts/tests/c11d_d8/d8_7'
    physical_media_mutation_performed=$false
    release_product_mutation_performed=$false
})

$receiptResult = $mediaDependentState
if($guard -ne 'PASS') { $receiptResult='FAIL' }
Write-JsonFile 'd8_7_receipt.json' ([ordered]@{
    contract='C11-D-D8-ACCEPTANCE-FREEZE-V1'
    checkpoint='D8.7'
    result=$receiptResult
    status=($(if($receiptResult -eq 'FAIL'){'OPEN'}else{'CLOSED'}))
    d8_control_plane='ACCEPTED'
    scope_candidate_count=$registry.Count
    release_authority=[string]$scope.release_authority
    physical_media_mutation_performed=$false
    release_product_mutation_performed=$false
    mutation_guard=$guard
    next='POST_D8_MEDIA_QUALIFICATION'
})

if($guard -ne 'PASS') { throw 'D8.7 mutation guard failed.' }
Write-Host ("D8.7 {0} | evidence=artifacts/tests/c11d_d8/d8_7 | scope_candidates={1} | control_plane=ACCEPTED | media_state={0}" -f $receiptResult,$registry.Count)
