#requires -Version 5.1
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version 1.0

$ProjectRoot = (Get-Location).Path
$EvidenceDir = Join-Path $ProjectRoot 'artifacts\tests\c11d_d9\d9_0'
New-Item -ItemType Directory -Force -Path $EvidenceDir | Out-Null

function Read-JsonFile([string]$Path) {
    if(-not (Test-Path -LiteralPath $Path -PathType Leaf)) { throw "Required JSON missing: $Path" }
    return (Get-Content -LiteralPath $Path -Raw -Encoding UTF8 | ConvertFrom-Json)
}
function Write-Json([string]$Path,[object]$Object) {
    $json = $Object | ConvertTo-Json -Depth 20
    [System.IO.File]::WriteAllBytes($Path,[System.Text.Encoding]::UTF8.GetBytes($json + [Environment]::NewLine))
}

$d87 = Read-JsonFile (Join-Path $ProjectRoot 'artifacts\tests\c11d_d8\d8_7\d8_7_acceptance_receipt.json')
if([string]$d87.result -notin @('PASS_NO_MEDIA','PASS')) { throw 'D8.7 acceptance is not PASS.' }
if([string]$d87.status -ne 'CLOSED') { throw 'D8.7 acceptance is not CLOSED.' }

$scopePath = Join-Path $ProjectRoot 'definitions\c11d\d8\D8_MEDIA_SCOPE_V1.json'
$scope = Read-JsonFile $scopePath
if([string]$scope.scope_mode -ne 'EXPLICIT_REGISTRY_ONLY') { throw 'D8 media scope mode is not EXPLICIT_REGISTRY_ONLY.' }

$orchestrator = Join-Path $ProjectRoot 'tools\c11d\d4\canonical_production_orchestrator.py'
if(-not (Test-Path -LiteralPath $orchestrator -PathType Leaf)) { throw "Canonical production orchestrator missing: $orchestrator" }

$pilotRequestPath = Join-Path $ProjectRoot 'definitions\c11d\d9\D9_MEDIA_PILOT_REQUEST_V1.json'
$pilot = Read-JsonFile $pilotRequestPath
if([bool]$pilot.authorized) { throw 'D9.0 pilot request must remain unauthorized.' }
if([bool]$pilot.execution) { throw 'D9.0 pilot execution must remain disabled.' }
if([string]$pilot.release_authority -ne 'NONE') { throw 'D9.0 release authority must remain NONE.' }

$evidence = [ordered]@{
    contract='C11-D-D9.0-MEDIA-PILOT-PREFLIGHT-V1'
    phase='D9.0'
    result='PASS'
    status='PREFLIGHT_ONLY'
    d8_7=[ordered]@{result=[string]$d87.result;status=[string]$d87.status}
    media_scope=[ordered]@{scope_mode=[string]$scope.scope_mode;candidate_count=[int]$scope.candidate_count}
    producer=[ordered]@{canonical_orchestrator_present=$true;path='tools/c11d/d4/canonical_production_orchestrator.py'}
    authorization=[ordered]@{pilot_authorized=[bool]$pilot.authorized;production_execution=[bool]$pilot.execution;renderer_execution=[bool]$pilot.renderer_execution;release_authority=[string]$pilot.release_authority}
    forbidden_actions_performed=$false
}
Write-Json (Join-Path $EvidenceDir 'd9_0_preflight_evidence.json') $evidence

$receipt = [ordered]@{
    contract='C11-D-D9.0-VALIDATION-RECEIPT-V1'
    checkpoint='D9.0'
    result='PASS'
    status='PREFLIGHT_ONLY'
    media_scope_candidates=[int]$scope.candidate_count
    pilot_authorized=[bool]$pilot.authorized
    production_execution=[bool]$pilot.execution
    renderer_execution=[bool]$pilot.renderer_execution
    release_authority=[string]$pilot.release_authority
    next='D9.1 - Single-case real media render'
}
Write-Json (Join-Path $EvidenceDir 'd9_0_validation_receipt.json') $receipt

Write-Host 'D9.0 PASS | preflight_only=True | scope_candidates=0 | pilot_authorized=False | production_execution=False | renderer_execution=False'
