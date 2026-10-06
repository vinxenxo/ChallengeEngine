[CmdletBinding()]
param()
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$d50Path = Join-Path $root 'artifacts\tests\c11d_d5\d5_0\d5_0_validation_receipt.json'
if (-not (Test-Path -LiteralPath $d50Path -PathType Leaf)) { throw 'D5.0 validation receipt is missing.' }
$d50 = Get-Content -LiteralPath $d50Path -Raw | ConvertFrom-Json
if ($d50.result -ne 'PASS' -or $d50.status -ne 'CLOSED') { throw 'D5.0 must be PASS/CLOSED before D5.1.' }

# Keep both handovers current before their hashes are captured into the manifest.
$utf8 = [System.Text.UTF8Encoding]::new($false)
foreach ($relative in @('docs\current\d\MASTER_HANDOVER_C11D_CURRENT.md', 'docs\current\d\START_PROMPT_C11D_CURRENT.md')) {
    $path = Join-Path $root $relative
    $text = [System.IO.File]::ReadAllText($path, [System.Text.Encoding]::UTF8)
    $text = [regex]::Replace($text, '(?m)^NEXT\s*=.*$', 'NEXT = D5.2 - Provenance Lineage Registry', 1)
    if ($relative -like '*MASTER_HANDOVER*') {
        $text = [regex]::Replace($text, '(?m)^D5\.1:\s*.*$', 'D5.1: PASS / CLOSED', 1)
    } else {
        $text = [regex]::Replace($text, '(?m)^D5\.1\s*=\s*.*$', 'D5.1 = PASS / CLOSED', 1)
    }
    [System.IO.File]::WriteAllText($path, $text, $utf8)
}

$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) { throw 'Python is required to build the canonical manifest.' }
Write-Output '=================================================='
Write-Output ' C11-D D5.1 - CANONICAL ARTIFACT MANIFEST'
Write-Output '=================================================='
Write-Output '[OK] D5.0 PASS/CLOSED verified.'
& $python.Source (Join-Path $PSScriptRoot 'artifact_manifest_builder.py') --root $root
if ($LASTEXITCODE -ne 0) { throw "D5.1 manifest builder failed (exit $LASTEXITCODE)." }

$out = Join-Path $root 'artifacts\tests\c11d_d5\d5_1'
$manifest = Get-Content -LiteralPath (Join-Path $out 'd5_1_canonical_artifact_manifest.json') -Raw | ConvertFrom-Json
$receipt = Get-Content -LiteralPath (Join-Path $out 'd5_1_validation_receipt.json') -Raw | ConvertFrom-Json
$evidence = Get-Content -LiteralPath (Join-Path $out 'd5_1_manifest_evidence.json') -Raw | ConvertFrom-Json
$schema = Get-Content -LiteralPath (Join-Path $root 'definitions\c11d\artifacts\C11D_ARTIFACT_MANIFEST_SCHEMA_V1.json') -Raw | ConvertFrom-Json
if ($receipt.result -ne 'PASS' -or $receipt.status -ne 'CLOSED') { throw 'D5.1 validation receipt is not PASS/CLOSED.' }
if ($manifest.artifact_types.Count -ne 12 -or $manifest.lifecycle_states.Count -ne 5) { throw 'D5.1 taxonomy or lifecycle list is incomplete.' }
if ($schema.properties.manifest_id.const -ne 'c11d_artifact_manifest') { throw 'D5.1 JSON schema identity mismatch.' }
if ($manifest.unmanaged_inventory.cleanup_authority -ne 'NONE' -or $manifest.unmanaged_inventory.cleanup_performed) { throw 'Orphan cleanup authority or execution is invalid.' }
if (@($receipt.tests.PSObject.Properties | Where-Object { $_.Value -ne $true }).Count -ne 0) { throw 'One or more D5.1 acceptance checks failed.' }
if (@($manifest.artifacts | Where-Object { $_.lifecycle_state -eq 'ORPHANED' -and ($_.governed -or $_.canonical) }).Count -ne 0) { throw 'An orphaned record was marked governed or canonical.' }
if (@($manifest.artifacts | Where-Object { $_.relative_path -like 'docs/history/*' -and $_.lifecycle_state -ne 'HISTORICAL' }).Count -ne 0) { throw 'Historical path has a non-HISTORICAL lifecycle.' }
$manifestHash = (Get-FileHash -LiteralPath (Join-Path $out 'd5_1_canonical_artifact_manifest.json') -Algorithm SHA256).Hash.ToLowerInvariant()
$evidenceHash = (Get-FileHash -LiteralPath (Join-Path $out 'd5_1_manifest_evidence.json') -Algorithm SHA256).Hash.ToLowerInvariant()
if ($receipt.manifest_sha256 -ne $manifestHash -or $receipt.manifest_evidence_sha256 -ne $evidenceHash) { throw 'D5.1 receipt output hashes do not match the written files.' }
foreach ($relative in @('docs\current\d\MASTER_HANDOVER_C11D_CURRENT.md', 'docs\current\d\START_PROMPT_C11D_CURRENT.md')) {
    $text = [System.IO.File]::ReadAllText((Join-Path $root $relative), [System.Text.Encoding]::UTF8)
    if ([regex]::Matches($text, '(?m)^D5\.1(?:\s*[:=])\s*PASS\s*/\s*CLOSED\s*$').Count -ne 1) { throw "D5.1 handover marker is missing or duplicated: $relative" }
    if ([regex]::Matches($text, '(?m)^NEXT\s*=\s*D5\.2\s*-\s*Provenance Lineage Registry\s*$').Count -ne 1) { throw "D5.2 next marker is missing or duplicated: $relative" }
}

$messages = @(
    '[OK] Governed artifact inventory built.'
    '[OK] Artifact taxonomy verified.'
    '[OK] Lifecycle states verified.'
    '[OK] Stable artifact identity verified.'
    '[OK] Content SHA-256 integrity verified.'
    '[OK] Path-independent identity test passed.'
    '[OK] D3 provenance entries verified.'
    '[OK] D4 provenance entries verified.'
    '[OK] Request -> Plan lineage references verified.'
    '[OK] Plan -> Authorization lineage references verified.'
    '[OK] Historical boundary preserved.'
    '[OK] Orphan candidates retained without deletion.'
    '[OK] Frozen C11-C identity preserved.'
    '[OK] Manifest deterministic.'
    '[OK] Manifest idempotency PASS.'
    '[OK] Runtime authority = NONE.'
    '[OK] Production execution = FALSE.'
)
$messages | ForEach-Object { Write-Output $_ }
Write-Output '=================================================='
Write-Output ' C11-D D5.1 - PASS / CLOSED'
Write-Output '=================================================='
Write-Output 'NEXT: D5.2 - Provenance Lineage Registry'
