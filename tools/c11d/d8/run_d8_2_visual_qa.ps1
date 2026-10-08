[CmdletBinding()]
param(
    [string]$ProjectRoot = '',
    [string]$D81Receipt = 'artifacts/tests/c11d_d8/d8_1/d8_1_validation_receipt.json'
)
Set-StrictMode -Version Latest
$ErrorActionPreference='Stop'
if([string]::IsNullOrWhiteSpace($ProjectRoot)){$ProjectRoot=(Get-Location).Path}
$ProjectRoot=(Resolve-Path -LiteralPath $ProjectRoot).Path
if(-not(Test-Path -LiteralPath (Join-Path $ProjectRoot 'tools/c11d/d8') -PathType Container)){throw "ProjectRoot does not look like ChallengeEngineV01_STATELESS: $ProjectRoot"}
$EvidenceRoot=Join-Path $ProjectRoot 'artifacts/tests/c11d_d8/d8_2'
$ScopePath=Join-Path $ProjectRoot 'definitions/c11d/d8/D8_MEDIA_SCOPE_V1.json'
$D81Path=Join-Path $ProjectRoot ($D81Receipt.Replace('\','/').TrimStart('./') -replace '/', '\')
function Write-Utf8NoBom([string]$Path,[string]$Text){$enc=New-Object System.Text.UTF8Encoding($false);[IO.File]::WriteAllText($Path,$Text,$enc)}
function CanonicalJson($Value){return ($Value|ConvertTo-Json -Depth 50 -Compress)}
function Sha256([string]$Path){return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()}
if(-not(Test-Path -LiteralPath $ScopePath -PathType Leaf)){throw "Canonical D8 media scope missing: $ScopePath"}
if(-not(Test-Path -LiteralPath $D81Path -PathType Leaf)){throw "D8.1 receipt missing: $D81Receipt"}
$d81=Get-Content -LiteralPath $D81Path -Raw -Encoding UTF8|ConvertFrom-Json
$scope=Get-Content -LiteralPath $ScopePath -Raw -Encoding UTF8|ConvertFrom-Json
if($d81.status -notin @('PASS','PASS_NO_MEDIA')){throw "D8.1 is not closed successfully: $($d81.status)"}
if($scope.scope_mode -ne 'EXPLICIT_REGISTRY_ONLY'){throw "Unsupported visual QA scope mode: $($scope.scope_mode)"}
$targets=@($scope.registry)
if(-not(Test-Path -LiteralPath $EvidenceRoot -PathType Container)){New-Item -ItemType Directory -Path $EvidenceRoot -Force|Out-Null}
$status=if($targets.Count -eq 0){'PASS_NO_MEDIA'}else{'BLOCKED'}
$reason=if($targets.Count -eq 0){$null}else{'D8_2_VISUAL_EXECUTION_DEFERRED_TO_REGISTERED_MEDIA_IMPLEMENTATION'}
$report=[ordered]@{contract='C11-D-D8.2-VISUAL-QA-REPORT-V1';phase='D8.2';status=$status;scope_mode=$scope.scope_mode;candidate_count=$targets.Count;visual_targets=@($targets);source_d8_1_receipt=$D81Receipt;source_d8_1_receipt_sha256=(Sha256 $D81Path);release_authority='NONE';production_execution=$false;renderer_execution=$false;media_source_modified=$false;derived_visual_evidence_created=$false;reason=$reason}
Write-Utf8NoBom (Join-Path $EvidenceRoot 'd8_2_visual_qa_report.json') (CanonicalJson $report)
$receipt=[ordered]@{contract='C11-D-D8.2-VALIDATION-RECEIPT-V1';phase='D8.2';status=$status;next=if($status-eq'PASS_NO_MEDIA'){'D8.3'}else{'D8.2_MEDIA_IMPLEMENTATION'};scope_sha256=(Sha256 $ScopePath);visual_report_sha256=(Sha256 (Join-Path $EvidenceRoot 'd8_2_visual_qa_report.json'));governance=[ordered]@{d4_8='BLOCKED';runtime_authority='NONE';production_execution=$false;renderer_execution=$false;master_seed='NOT_ADOPTED';cross_domain_seed_sharing='FORBIDDEN';release_authority='NONE'}}
Write-Utf8NoBom (Join-Path $EvidenceRoot 'd8_2_validation_receipt.json') (CanonicalJson $receipt)
Write-Host "D8.2 $status | evidence=artifacts/tests/c11d_d8/d8_2 | scope_candidates=$($targets.Count)"
if($status-eq'PASS_NO_MEDIA'){exit 0}else{exit 1}
