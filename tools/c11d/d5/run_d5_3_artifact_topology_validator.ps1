[CmdletBinding()]
param()
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path

$predecessors = @(
    @{ Name = 'D5.0'; Path = 'artifacts\tests\c11d_d5\d5_0\d5_0_validation_receipt.json' }
    @{ Name = 'D5.1'; Path = 'artifacts\tests\c11d_d5\d5_1\d5_1_validation_receipt.json' }
    @{ Name = 'D5.2'; Path = 'artifacts\tests\c11d_d5\d5_2\d5_2_validation_receipt.json' }
)
foreach ($item in $predecessors) {
    $path = Join-Path $root $item.Path
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) { throw "$($item.Name) receipt is missing." }
    $receipt = Get-Content -LiteralPath $path -Raw | ConvertFrom-Json
    if ($receipt.result -ne 'PASS' -or $receipt.status -ne 'CLOSED') { throw "$($item.Name) must be PASS/CLOSED before D5.3." }
}

$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) { throw 'Python is required to validate artifact topology.' }
Write-Output '=================================================='
Write-Output ' C11-D D5.3 - ARTIFACT TOPOLOGY VALIDATOR'
Write-Output '=================================================='
Write-Output '[OK] D5.0, D5.1, and D5.2 PASS/CLOSED verified.'
& $python.Source (Join-Path $PSScriptRoot 'artifact_topology_validator.py') --root $root
if ($LASTEXITCODE -ne 0) { throw "D5.3 topology validator failed (exit $LASTEXITCODE)." }

$out = Join-Path $root 'artifacts\tests\c11d_d5\d5_3'
$topologyPath = Join-Path $out 'd5_3_topology_validation.json'
$matrixPath = Join-Path $out 'd5_3_consistency_matrix.json'
$receiptPath = Join-Path $out 'd5_3_validation_receipt.json'
$contractPath = Join-Path $root 'docs\current\d\D5.3_ARTIFACT_TOPOLOGY_VALIDATOR_CONTRACT.md'
$topology = Get-Content -LiteralPath $topologyPath -Raw | ConvertFrom-Json
$matrix = Get-Content -LiteralPath $matrixPath -Raw | ConvertFrom-Json
$receipt = Get-Content -LiteralPath $receiptPath -Raw | ConvertFrom-Json
if ($receipt.result -ne 'PASS' -or $receipt.status -ne 'CLOSED') { throw 'D5.3 validation receipt is not PASS/CLOSED.' }
if ($receipt.consistency_matrix_sha256 -ne (Get-FileHash -LiteralPath $matrixPath -Algorithm SHA256).Hash.ToLowerInvariant()) { throw 'D5.3 consistency matrix hash mismatch.' }
if ($topology.consistency_matrix_sha256 -ne $receipt.consistency_matrix_sha256 -or $topology.result -ne 'PASS' -or $matrix.result -ne 'PASS') { throw 'D5.3 topology layers do not agree.' }
if ($receipt.physical_locations -ne 79 -or $receipt.logical_identities -ne 75 -or $receipt.lineage_edges -ne 11) { throw 'D5.3 counts differ from the D5.1/D5.2 source records.' }
if ($receipt.missing_artifacts -ne 0 -or $receipt.hash_mismatches -ne 0 -or $receipt.identity_conflicts -ne 0 -or $receipt.lifecycle_conflicts -ne 0 -or $receipt.unknown_lineage_targets -ne 0 -or $receipt.topology_conflicts -ne 0) { throw 'D5.3 found topology or provenance conflicts.' }
if (-not $receipt.filesystem_manifest_consistent -or -not $receipt.manifest_identity_consistent -or -not $receipt.manifest_lineage_consistent -or -not $receipt.lifecycle_consistent -or -not $receipt.evidence_consistent) { throw 'D5.3 consistency gates are incomplete.' }
if (-not $receipt.d3_consistency -or -not $receipt.d4_consistency -or -not $matrix.d3.raw_master_consistency -or -not $matrix.d4.blocked_authorization_preserved) { throw 'D5.3 D3/D4 phase gate failed.' }
if ($receipt.governed_active -ne 66 -or $receipt.orphaned_nodes -ne 9 -or $receipt.global_unmanaged_candidates -ne 12304) { throw 'D5.3 governance inventory changed unexpectedly.' }
if (@($receipt.synthetic_negative_tests.PSObject.Properties | Where-Object { $_.Value -ne $true }).Count -ne 0) { throw 'One or more D5.3 synthetic negative tests failed.' }
if (-not $receipt.idempotency -or -not $receipt.frozen_c11c_preserved -or $receipt.files_moved -or $receipt.files_deleted -or $receipt.cleanup_performed) { throw 'D5.3 idempotency, frozen identity, or audit-only boundary failed.' }
if ($receipt.runtime_authority -ne 'NONE' -or $receipt.production_execution) { throw 'D5.3 exceeds its runtime authority boundary.' }
if (-not (Test-Path -LiteralPath $contractPath -PathType Leaf)) { throw 'D5.3 contract is missing.' }
$contractText = [System.IO.File]::ReadAllText($contractPath, [System.Text.Encoding]::UTF8)
if ([regex]::Matches($contractText, '(?m)^<!-- C11D_D5_3_CONTRACT_V1 -->\r?$').Count -ne 1) { throw 'D5.3 contract section marker is missing or duplicated.' }

# Advance handovers only after the generated validation, matrix, receipt, and hashes pass.
$utf8 = [System.Text.UTF8Encoding]::new($false)
$masterPath = Join-Path $root 'docs\current\d\MASTER_HANDOVER_C11D_CURRENT.md'
$master = [System.IO.File]::ReadAllText($masterPath, [System.Text.Encoding]::UTF8)
$master = [regex]::Replace($master, '(?m)^## Current state - .*$', '## Current state - D5.3 CLOSED', 1)
$master = [regex]::Replace($master, '(?m)^D5\.3:.*\r?\n', '', 1)
$master = [regex]::Replace($master, '(?m)^(D5\.2:.*)$', '$1' + "`r`nD5.3: PASS / CLOSED", 1)
$master = [regex]::Replace($master, '(?m)^NEXT =.*$', 'NEXT = D5.4 - Artifact Lifecycle / Quarantine Rules', 1)
$master = $master.Replace('- Next: **D5.3 - Artifact Topology Validator**.', '- Followed by: **D5.3 - Artifact Topology Validator**.')
$master = [regex]::Replace($master, '(?m)^## Next\r?\n\r?\nD5\.3 - Artifact Topology Validator\.\r?$', "## Next`r`n`r`nD5.4 - Artifact Lifecycle / Quarantine Rules.", 1)
$masterBlock = @'

<!-- C11D_D5_3_HANDOFF_V1 -->

## C11-D D5.3 CLOSED / PASS

- Filesystem and D5.1 manifest agree across {0} physical locations; all {1} canonical identities recompute, with no content hash or copy conflicts.
- D5.2 lineage is consistent across {2} nodes and {3} evidence-backed edges. Evidence files exist and D3/D4 gates pass; D4.8 remains BLOCKED with no authorization grant.
- Lifecycle routes are consistent: {4} governed ACTIVE artifacts and {5} ORPHANED governance records; {6} global unmanaged candidates remain outside the graph.
- Missing-file, altered-hash, identity-copy conflict, unknown-target, and lifecycle-conflict fixtures were detected. C11-C frozen identity is preserved.
- No repository files were moved or deleted; cleanup was not performed. Runtime authority is NONE and production execution is false.
- Contract: `docs/current/d/D5.3_ARTIFACT_TOPOLOGY_VALIDATOR_CONTRACT.md`.
- Validation, consistency matrix, and receipt: `artifacts/tests/c11d_d5/d5_3/`.
- Next: **D5.4 - Artifact Lifecycle / Quarantine Rules**.
'@
$values = @($receipt.physical_locations, $receipt.logical_identities, $matrix.lineage.nodes_checked, $receipt.lineage_edges, $receipt.governed_active, $receipt.orphaned_nodes, $receipt.global_unmanaged_candidates)
for ($i = 0; $i -lt $values.Count; $i++) { $masterBlock = $masterBlock.Replace("{$i}", [string]$values[$i]) }
$master = [regex]::Replace($master, '(?s)\r?\n<!-- C11D_D5_3_HANDOFF_V1 -->.*\z', '')
$master = $master.TrimEnd() + $masterBlock + "`r`n"
[System.IO.File]::WriteAllText($masterPath, $master, $utf8)

$startPath = Join-Path $root 'docs\current\d\START_PROMPT_C11D_CURRENT.md'
$start = [System.IO.File]::ReadAllText($startPath, [System.Text.Encoding]::UTF8)
$start = [regex]::Replace($start, '(?m)^Continue ChallengeEngineV01_STATELESS from .*$', 'Continue ChallengeEngineV01_STATELESS from C11-D D5.3 PASS / CLOSED.', 1)
$start = [regex]::Replace($start, '(?m)^D5\.3\s*=.*\r?\n', '', 1)
$start = [regex]::Replace($start, '(?m)^(D5\.2\s*=.*)$', '$1' + "`r`nD5.3 = PASS / CLOSED", 1)
$start = [regex]::Replace($start, '(?m)^NEXT\s*=.*$', 'NEXT = D5.4 - Artifact Lifecycle / Quarantine Rules', 1)
$start = [regex]::Replace($start, '(?m)^D5\.2 builds an evidence-backed lineage DAG.*$', 'D5.3 confirms that filesystem paths, D5.1 identities, and D5.2 lineage agree: 75 logical identities, 79 locations, and 11 evidence-backed edges. All negative fixtures passed; 66 governed ACTIVE artifacts and 9 retained ORPHANED nodes remain distinct. The 12,304 unmanaged candidates stay outside the graph. D4.8 remains BLOCKED, no repository files were moved or deleted, runtime authority is NONE, and production execution is false.', 1)
$start = [regex]::Replace($start, '(?m)^docs\\current\\d\\D5\.3_ARTIFACT_TOPOLOGY_VALIDATOR_CONTRACT\.md\r?$', '')
$start = [regex]::Replace($start, '(?m)^artifacts\\tests\\c11d_d5\\d5_3\\d5_3_validation_receipt\.json\r?$', '')
$start = [regex]::Replace($start, '(?m)^(artifacts\\tests\\c11d_d5\\d5_2\\d5_2_validation_receipt\.json)\r?$', '$1' + "`r`ndocs\current\d\D5.3_ARTIFACT_TOPOLOGY_VALIDATOR_CONTRACT.md`r`nartifacts\tests\c11d_d5\d5_3\d5_3_validation_receipt.json", 1)
$start = [regex]::Replace($start, '(?m)^D5\.3 - Artifact Topology Validator\.\r?$', 'D5.4 - Artifact Lifecycle / Quarantine Rules.', 1)
$startBlock = @'

<!-- C11D_D5_3_HANDOFF_V1 -->

D5.3 validates filesystem, D5.1 manifest, and D5.2 lineage agreement: 75 logical identities, 79 physical locations, 11 edges, 0 missing artifacts, 0 hash mismatches, and 0 topology conflicts. D3/D4 consistency and all five negative fixtures pass. The 9 ORPHANED nodes and 12,304 global unmanaged candidates remain untouched and outside cleanup authority. C11-C is preserved; runtime authority is NONE and production execution is false.
'@
$start = [regex]::Replace($start, '(?s)\r?\n<!-- C11D_D5_3_HANDOFF_V1 -->.*\z', '')
$start = $start.TrimEnd() + $startBlock + "`r`n"
[System.IO.File]::WriteAllText($startPath, $start, $utf8)

foreach ($path in @($masterPath, $startPath)) {
    $text = [System.IO.File]::ReadAllText($path, [System.Text.Encoding]::UTF8)
    $text = $text.Replace("`r`n", "`n").Replace("`r", "`n").Replace("`n", "`r`n")
    $text = [regex]::Replace($text, '(\r?\n){3,}', "`r`n`r`n")
    [System.IO.File]::WriteAllText($path, $text, $utf8)
    $text = [System.IO.File]::ReadAllText($path, [System.Text.Encoding]::UTF8)
    if ([regex]::Matches($text, '(?m)^<!-- C11D_D5_3_HANDOFF_V1 -->\r?$').Count -ne 1) { throw "D5.3 handover marker missing or duplicated: $path" }
    if ([regex]::Matches($text, '(?m)^NEXT = D5\.4 - Artifact Lifecycle / Quarantine Rules\r?$').Count -ne 1) { throw "D5.4 next marker missing or duplicated: $path" }
}

Write-Output '[OK] 79/79 manifest locations exist and declared hashes agree.'
Write-Output '[OK] 75/75 logical identities recomputed; no copy conflicts.'
Write-Output '[OK] 11/11 lineage edges resolve to manifest nodes and physical evidence.'
Write-Output '[OK] Lifecycle routes and orphan governance are consistent.'
Write-Output '[OK] D3 raw/master/QA lineage is consistent.'
Write-Output '[OK] D4 request/plan/governance/acceptance is consistent; D4.8 remains BLOCKED.'
Write-Output '[OK] All five synthetic negative fixtures were detected.'
Write-Output '[OK] 12,304 global unmanaged candidates were not promoted or cleaned.'
Write-Output '[OK] Idempotency and frozen C11-C identity verified.'
Write-Output '[OK] No files moved or deleted; runtime authority = NONE.'
Write-Output '[OK] Production execution = FALSE.'
Write-Output '=================================================='
Write-Output ' C11-D D5.3 - PASS / CLOSED'
Write-Output '=================================================='
Write-Output 'NEXT: D5.4 - Artifact Lifecycle / Quarantine Rules'
