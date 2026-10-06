[CmdletBinding()]
param()
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$d51Path = Join-Path $root 'artifacts\tests\c11d_d5\d5_1\d5_1_validation_receipt.json'
if (-not (Test-Path -LiteralPath $d51Path -PathType Leaf)) { throw 'D5.1 validation receipt is missing.' }
$d51 = Get-Content -LiteralPath $d51Path -Raw | ConvertFrom-Json
if ($d51.result -ne 'PASS' -or $d51.status -ne 'CLOSED') { throw 'D5.1 must be PASS/CLOSED before D5.2.' }

$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) { throw 'Python is required to build the lineage registry.' }
Write-Output '=================================================='
Write-Output ' C11-D D5.2 - PROVENANCE LINEAGE REGISTRY'
Write-Output '=================================================='
Write-Output '[OK] D5.1 PASS/CLOSED verified.'
& $python.Source (Join-Path $PSScriptRoot 'provenance_lineage_registry.py') --root $root
if ($LASTEXITCODE -ne 0) { throw "D5.2 lineage registry builder failed (exit $LASTEXITCODE)." }

$out = Join-Path $root 'artifacts\tests\c11d_d5\d5_2'
$registryPath = Join-Path $out 'd5_2_lineage_registry.json'
$evidencePath = Join-Path $out 'd5_2_lineage_evidence.json'
$receiptPath = Join-Path $out 'd5_2_validation_receipt.json'
$registry = Get-Content -LiteralPath $registryPath -Raw | ConvertFrom-Json
$evidence = Get-Content -LiteralPath $evidencePath -Raw | ConvertFrom-Json
$receipt = Get-Content -LiteralPath $receiptPath -Raw | ConvertFrom-Json
if ($receipt.result -ne 'PASS' -or $receipt.status -ne 'CLOSED') { throw 'D5.2 receipt is not PASS/CLOSED.' }
if ($receipt.registry_sha256 -ne (Get-FileHash -LiteralPath $registryPath -Algorithm SHA256).Hash.ToLowerInvariant()) { throw 'D5.2 registry hash mismatch.' }
if ($receipt.evidence_sha256 -ne (Get-FileHash -LiteralPath $evidencePath -Algorithm SHA256).Hash.ToLowerInvariant()) { throw 'D5.2 evidence hash mismatch.' }
if ($registry.nodes.Count -ne 75 -or $receipt.physical_locations_referenced -ne 79 -or $receipt.orphan_nodes -ne 9) { throw 'D5.2 logical identity/location/orphan counts differ from the D5.1 source manifest.' }
if ($receipt.edges -ne $receipt.evidence_backed_edges -or $registry.invalid_edges_rejected.Count -ne 0) { throw 'D5.2 contains an unbacked or invalid edge.' }
if (@($registry.edges | Where-Object { $_.confidence -ne 'EVIDENCE_BACKED' -or $_.evidence.source_type -notin @('manifest', 'receipt', 'contract', 'audit', 'evidence') }).Count -ne 0) { throw 'D5.2 edge evidence source type is invalid.' }
if (-not $receipt.dag_valid -or -not $receipt.duplicate_identity_collapsed -or -not $receipt.missing_parent_rejected -or -not $receipt.synthetic_cycle_detected) { throw 'D5.2 graph acceptance checks failed.' }
if (-not $receipt.d3_lineage_valid -or -not $receipt.d4_lineage_valid -or -not $receipt.deterministic_registry -or -not $receipt.idempotency) { throw 'D5.2 D3/D4 lineage or determinism checks failed.' }
if ($receipt.global_unmanaged_candidates -ne 12304 -or $receipt.cleanup_performed -or $receipt.files_moved -or $receipt.files_deleted) { throw 'D5.2 orphan inventory or audit-only boundary failed.' }
if (-not $receipt.frozen_c11c_preserved -or $receipt.runtime_authority -ne 'NONE' -or $receipt.production_execution) { throw 'D5.2 frozen/runtime boundary failed.' }
if (-not (Test-Path -LiteralPath (Join-Path $root 'docs\current\d\D5.2_PROVENANCE_LINEAGE_REGISTRY_CONTRACT.md') -PathType Leaf)) { throw 'D5.2 contract is missing.' }

# Advance handovers only after all generated outputs pass receipt/hash validation.
$utf8 = [System.Text.UTF8Encoding]::new($false)
$masterPath = Join-Path $root 'docs\current\d\MASTER_HANDOVER_C11D_CURRENT.md'
$master = [System.IO.File]::ReadAllText($masterPath, [System.Text.Encoding]::UTF8)
$master = [regex]::Replace($master, '(?m)^## Current state - .*$', '## Current state - D5.2 CLOSED', 1)
$master = [regex]::Replace($master, '(?m)^D5\.2:.*\r?\n', '', 1)
$master = [regex]::Replace($master, '(?m)^(D5\.1:.*)$', '$1' + "`r`nD5.2: PASS / CLOSED", 1)
$master = [regex]::Replace($master, '(?m)^D5 = ACTIVE$', 'D5 = ACTIVE', 1)
$master = [regex]::Replace($master, '(?m)^NEXT =.*$', 'NEXT = D5.3 - Artifact Topology Validator', 1)
$master = $master.Replace('- Next: **D5.2 - Provenance Lineage Registry**.', '- Followed by: **D5.2 - Provenance Lineage Registry**.')
$master = [regex]::Replace($master, '(?m)^## Next\r?\n\r?\nD5\.2 - Provenance Lineage Registry\.$', "## Next`r`n`r`nD5.3 - Artifact Topology Validator.", 1)
$masterBlock = @'

<!-- C11D_D5_2_HANDOFF_V1 -->

## C11-D D5.2 CLOSED / PASS

- The registry consumes the D5.1 manifest as the sole node source: 75 logical nodes retain 79 physical locations; 9 ORPHANED nodes remain governed as non-cleanup records.
- Evidence-backed graph contains {0} accepted edges; D3 raw-to-master and QA lineage and D4 request/plan/governance/acceptance evidence are validated. Blocked D4.8 governance is recorded as BLOCKED, not as a grant.
- The 12,304 global unmanaged candidates remain external inventory; no files were moved or deleted.
- Synthetic cycle and missing-parent rejection checks passed; registry is deterministic/idempotent and C11-C frozen SHA-256 is preserved.
- Runtime authority is NONE; production execution is false.
- Contract: `docs/current/d/D5.2_PROVENANCE_LINEAGE_REGISTRY_CONTRACT.md`.
- Registry, evidence, and receipt: `artifacts/tests/c11d_d5/d5_2/`.
- Next: **D5.3 - Artifact Topology Validator**.
'@
$masterBlock = $masterBlock.Replace('{0}', [string]$receipt.edges)
$master = [regex]::Replace($master, '(?s)\r?\n<!-- C11D_D5_2_HANDOFF_V1 -->.*\z', '')
$master = $master.TrimEnd() + $masterBlock + "`r`n"
[System.IO.File]::WriteAllText($masterPath, $master, $utf8)

$startPath = Join-Path $root 'docs\current\d\START_PROMPT_C11D_CURRENT.md'
$start = [System.IO.File]::ReadAllText($startPath, [System.Text.Encoding]::UTF8)
$start = [regex]::Replace($start, '(?m)^Continue ChallengeEngineV01_STATELESS from .*$', 'Continue ChallengeEngineV01_STATELESS from C11-D D5.2 PASS / CLOSED.', 1)
$start = [regex]::Replace($start, '(?m)^D5\.2\s*=.*\r?\n', '', 1)
$start = [regex]::Replace($start, '(?m)^(D5\.1\s*=.*)$', '$1' + "`r`nD5.2 = PASS / CLOSED", 1)
$start = [regex]::Replace($start, '(?m)^D5 = ACTIVE$', 'D5 = ACTIVE', 1)
$start = [regex]::Replace($start, '(?m)^NEXT\s*=.*$', 'NEXT = D5.3 - Artifact Topology Validator', 1)
$start = [regex]::Replace($start, '(?m)^D5\.1 publishes.*$', 'D5.2 builds an evidence-backed lineage DAG from the D5.1 canonical manifest. It records 75 logical nodes across 79 physical locations, 11 evidence-backed edges, and 9 retained ORPHANED nodes; the 12,304 global candidates remain outside the governed graph. D4.8 governance is recorded as BLOCKED, not as an authorization grant. No files were moved or deleted; runtime authority is NONE and production execution is false.', 1)
$start = [regex]::Replace($start, '(?m)^artifacts\\tests\\c11d_d5\\d5_1\\d5_1_validation_receipt\.json$', '$0' + "`r`ndocs\current\d\D5.2_PROVENANCE_LINEAGE_REGISTRY_CONTRACT.md`r`ndefinitions\c11d\provenance\C11D_PROVENANCE_LINEAGE_REGISTRY_V1.json`r`nartifacts\tests\c11d_d5\d5_2\d5_2_validation_receipt.json", 1)
$start = [regex]::Replace($start, '(?m)^D5\.2 - Provenance Lineage Registry\.$', 'D5.3 - Artifact Topology Validator.', 1)
$start = [regex]::Replace($start, '(?s)\r?\n<!-- C11D_D5_2_HANDOFF_V1 -->.*\z', '')
$startBlock = @'

<!-- C11D_D5_2_HANDOFF_V1 -->

D5.2 builds a deterministic evidence-backed lineage DAG from the D5.1 manifest: 75 logical nodes, 79 referenced locations, {0} edges, and 9 retained ORPHANED nodes. D3/D4 lineage, duplicate identity collapse, synthetic cycle detection, and invalid-parent rejection passed. The 12,304 global unmanaged candidates remain outside the registry; no files were moved or deleted. D4.8 remains a blocked authorization decision. Runtime authority is NONE and production execution is false.
'@
$startBlock = $startBlock.Replace('{0}', [string]$receipt.edges)
$start = $start.TrimEnd() + $startBlock + "`r`n"
[System.IO.File]::WriteAllText($startPath, $start, $utf8)

foreach ($path in @($masterPath, $startPath)) {
    $text = [System.IO.File]::ReadAllText($path, [System.Text.Encoding]::UTF8)
    $text = $text.Replace("`r`n", "`n").Replace("`r", "`n").Replace("`n", "`r`n")
    [System.IO.File]::WriteAllText($path, $text, $utf8)
}

foreach ($path in @($masterPath, $startPath)) {
    $text = [System.IO.File]::ReadAllText($path, [System.Text.Encoding]::UTF8)
    if ([regex]::Matches($text, '(?m)^<!-- C11D_D5_2_HANDOFF_V1 -->\r?$').Count -ne 1) { throw "D5.2 handover marker missing or duplicated: $path" }
    if ([regex]::Matches($text, '(?m)^NEXT = D5\.3 - Artifact Topology Validator\r?$').Count -ne 1) { throw "D5.3 next marker missing or duplicated: $path" }
}

Write-Output '[OK] D5.1 manifest is the sole graph node source.'
Write-Output '[OK] Duplicate logical identities collapse; physical locations remain indexed.'
Write-Output '[OK] Every accepted edge is evidence-backed; invalid parent fixture rejected.'
Write-Output '[OK] Synthetic cycle detected; real lineage remains a DAG.'
Write-Output '[OK] D3 and D4 evidence lineage verified.'
Write-Output '[OK] Orphan nodes and 12,304 global candidates retained without cleanup.'
Write-Output '[OK] Frozen C11-C identity preserved.'
Write-Output '[OK] Determinism and idempotency passed.'
Write-Output '[OK] Runtime authority = NONE.'
Write-Output '[OK] Production execution = FALSE.'
Write-Output '=================================================='
Write-Output ' C11-D D5.2 - PASS / CLOSED'
Write-Output '=================================================='
Write-Output 'NEXT: D5.3 - Artifact Topology Validator'
