[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$pythonScript = Join-Path $PSScriptRoot 'seed_governance_audit.py'
$outputDirectory = Join-Path $repoRoot 'artifacts\tests\c11d_d6\d6_0'

function Get-TreeSnapshot {
    param([string]$Root)
    $snapshotOutput = & python $pythonScript --root $Root --snapshot-only
    if ($LASTEXITCODE -ne 0) { throw 'Unable to capture D6.0 repository worktree snapshot.' }
    return ($snapshotOutput | ConvertFrom-Json)
}

Write-Host '=================================================='
Write-Host ' C11-D D6.0 - SEED GOVERNANCE AUDIT'
Write-Host '=================================================='

$d55ReceiptPath = Join-Path $repoRoot 'artifacts\tests\c11d_d5\d5_5\d5_5_acceptance_receipt.json'
if (-not (Test-Path -LiteralPath $d55ReceiptPath -PathType Leaf)) { throw 'D5.5 acceptance receipt is missing.' }
$d55Receipt = Get-Content -LiteralPath $d55ReceiptPath -Raw | ConvertFrom-Json
if ($d55Receipt.result -ne 'PASS' -or $d55Receipt.status -ne 'CLOSED') { throw 'D5.5 must be PASS/CLOSED before D6.0.' }
Write-Host '[OK] D5.5 PASS/CLOSED verified.'

$before = Get-TreeSnapshot -Root $repoRoot
Write-Host ('[OK] Mutation guard baseline captured: {0} worktree files.' -f $before.files)

Push-Location $repoRoot
try {
    & python $pythonScript --root $repoRoot
    if ($LASTEXITCODE -ne 0) { throw 'D6.0 audit did not pass its evidence gates.' }
}
finally {
    Pop-Location
}

$after = Get-TreeSnapshot -Root $repoRoot
if ($before.files -ne $after.files -or $before.tree_sha256 -ne $after.tree_sha256) {
    throw ('FILESYSTEM_MUTATION_FAILURE: before={0}/{1}; after={2}/{3}' -f $before.files, $before.tree_sha256, $after.files, $after.tree_sha256)
}
Write-Host '[OK] Mutation guard PASS; only files under artifacts/tests/c11d_d6/d6_0/ may change.'

$receiptPath = Join-Path $outputDirectory 'd6_0_audit_receipt.json'
$receipt = Get-Content -LiteralPath $receiptPath -Raw | ConvertFrom-Json
if ($receipt.result -ne 'PASS' -or $receipt.status -ne 'CLOSED' -or $receipt.audit_complete -ne $true) { throw 'D6.0 receipt is not PASS/CLOSED/AUDIT COMPLETE.' }
if ($receipt.runtime_authority -ne 'NONE' -or $receipt.production_execution -ne $false) { throw 'D6.0 runtime fence failed.' }

Write-Host ('[OK] Seed/RNG findings: {0}; blocking={1}; warnings={2}; unknown={3}.' -f $receipt.seed_rng_findings, $receipt.blocking_findings, $receipt.warning_findings, $receipt.unknown_findings)
Write-Host ('[OK] Domains: {0}' -f (($receipt.domain_counts | ConvertTo-Json -Compress)))
Write-Host ('[OK] Classifications: {0}' -f (($receipt.classification_counts | ConvertTo-Json -Compress)))
Write-Host ('[OK] Shared/global RNG found={0}; active runtime nondeterminism={1}; Producer nondeterministic selections={2}.' -f $receipt.shared_rng_state_found, $receipt.active_nondeterministic_source_found, $receipt.producer_nondeterministic_seed_selection_count)
Write-Host ('[OK] D3 music isolation={0}; D4 seed/music_seed separation={1}; D4.8 blocked={2}.' -f $receipt.d3_music_isolation, $receipt.d4_seed_music_seed_separation, $receipt.d4_8_blocked_no_seed_authority)
Write-Host ('[OK] C11-C preserved={0}; deterministic={1}; idempotent={2}.' -f $receipt.frozen_c11c_preserved, $receipt.deterministic, $receipt.idempotent)
Write-Host ('[OK] Runtime authority={0}; production execution={1}.' -f $receipt.runtime_authority, $receipt.production_execution)
Write-Host '=================================================='
Write-Host ' C11-D D6.0 - PASS / CLOSED'
Write-Host '=================================================='
Write-Host 'NEXT: D6.1 - Canonical Seed Registry + Governance Policy'
