# C11-D Request-Scoped Payload Materialization/Binding Overlay V1

## Purpose and state

This is a small, D-owned, preparation-only overlay. It joins three exact fixed canonical D9.9 review request chains to digests produced by the existing bounded in-memory Godot payload harnesses, then emits a hash-sealed review receipt to stdout only.

**State:** `PREPARATION_ONLY_FIXED_REVIEW_FIXTURES_REQUEST_BOUND_NOT_RENDERER_INPUT`.
It is not a renderer implementation, does not create renderer-native input, does not invoke renderer dispatch, does not persist payload/receipt files, and does not authorize production or release. `candidate_input_admissible=false`, `video_render_ready=false`, `renderer=OFF`, `media_created=false`, `D4.8=BLOCKED`, `release_authority=NONE`, `D9.14/D9.16=BLOCKED`, `D9.17=NO-GO`, and `D10=BLOCKED` remain mandatory.

The binding scope is intentionally limited to three exact review fixtures: Challenge `CHALLENGE_004`, Loop `harmonic_membrane`, and Drill `tracking/tier-2`. Dynamic arbitrary request transport and full consumption of all editorial values are not implemented. The receipt's Challenge payload identifier is a derived alias, not a native runtime identifier. Do not treat the receipt as a video-ready product.

## Exact overlay contents

### New files (6)

- `definitions/c11d/production/D_RENDERER_REQUEST_SCOPED_PAYLOAD_MATERIALIZATION_BINDING_SCHEMA_V1.json`
- `definitions/c11d/production/D_RENDERER_REQUEST_SCOPED_PAYLOAD_MATERIALIZATION_BINDING_V1.json`
- `tools/c11d/d9/d_renderer_request_scoped_payload_materialization_binding.py`
- `tools/c11d/d9/test_d_renderer_request_scoped_payload_materialization_binding.py`
- `docs/current/d/D_RENDERER_REQUEST_SCOPED_PAYLOAD_MATERIALIZATION_BINDING_CHECKPOINT_V1.md`
- `README_C11D_RENDERER_REQUEST_SCOPED_PAYLOAD_MATERIALIZATION_BINDING_OVERLAY_V1.md`

### Updated files (6)

- `docs/current/d/D_RENDERER_BASELINE_PREPARATION_PLAN_V1.md`
- `docs/current/d/D_RENDERER_CANDIDATE_IO_CONTRACT_CHECKPOINT_V1.md`
- `docs/current/d/C11D_CONTEXT_CHECKPOINT_D10_20261011.md`
- `docs/current/d/MASTER_HANDOVER_C11D_CURRENT.md`
- `docs/current/d/START_PROMPT_C11D_CURRENT.md`
- `docs/current/d/C11-D_ROADMAP_V1.0_STATELESS.md`

Exactly 12 archive entries are expected. No source under the frozen C11-C roots, no freeze manifest, no operator evidence/maintenance ledger and no cache/test output is included.

## Preflight and application (Windows PowerShell)

Run at the repository root. The SHA-256 is provided as a constant so a missing optional `.sha256` sidecar does not interrupt the check. Do not extract the source-context ZIP over the active checkout.

```powershell
$ErrorActionPreference = 'Stop'
$Root = 'C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS'
Set-Location $Root
$Overlay = Join-Path $env:USERPROFILE 'Downloads\C11D_RENDERER_REQUEST_SCOPED_PAYLOAD_MATERIALIZATION_BINDING_OVERLAY_V1.zip'
if (-not (Test-Path -LiteralPath $Overlay)) { throw "HARD STOP: overlay not found: $Overlay" }
$ExpectedZip = (Read-Host 'Paste the expected SHA-256 from the delivery message').Trim().ToLowerInvariant()
$ActualZip = (Get-FileHash -LiteralPath $Overlay -Algorithm SHA256).Hash.ToLowerInvariant()
Write-Host "Computed overlay SHA-256: $ActualZip"
if ($ActualZip -ne $ExpectedZip) { throw "HARD STOP: overlay SHA-256 mismatch: $ActualZip" }

$ExpectedManifest = 'e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953'
$Manifest = (Get-FileHash '.\release\C11C_FREEZE_PACKAGE_MANIFEST.json' -Algorithm SHA256).Hash.ToLowerInvariant()
if ($Manifest -ne $ExpectedManifest) { throw 'HARD STOP: frozen C11-C manifest precondition failed.' }
$ExpectedTimebase = '251b2384aabfe975b55938bc4a6696aba81b8dc817aa6902bf1f60f3894ad019'
$Timebase = (Get-FileHash '.\definitions\c11d\production\D_RENDERER_UNIFIED_DELIVERY_TIMEBASE_POLICY_PROPOSAL_V1.json' -Algorithm SHA256).Hash.ToLowerInvariant()
if ($Timebase -ne $ExpectedTimebase) { throw 'HARD STOP: timebase bytes differ from pinned baseline.' }

$ExpectedBefore = @{
  'docs/current/d/D_RENDERER_BASELINE_PREPARATION_PLAN_V1.md' = '93ee0aa844bcbc5ba35bdb0a9a072a708cb232ef62d3f8301db5413b08736c34'
  'docs/current/d/D_RENDERER_CANDIDATE_IO_CONTRACT_CHECKPOINT_V1.md' = '00bf251cc1f0aafd4c4cedd9e2b03c3ef38a1b9e1f532d375e3005e9789c2b43'
  'docs/current/d/C11D_CONTEXT_CHECKPOINT_D10_20261011.md' = '2523af73c008f5a4c4aaf0b685b37212c8668f76a439df981d3c890f4a54eb7b'
  'docs/current/d/MASTER_HANDOVER_C11D_CURRENT.md' = '85f2bc3de2401659025a5641071c6319801acd9a23e43711cdff49ec888ddd4b'
  'docs/current/d/START_PROMPT_C11D_CURRENT.md' = '598b8812407af571b37b1f25b68f72c2d1b5de287065e19ad02b905f201f8f26'
  'docs/current/d/C11-D_ROADMAP_V1.0_STATELESS.md' = '39620255b1270cda05cb3386b81a91bd91fee5e2b4405ca7c25b49d77ed6bb05'
}
foreach ($Rel in $ExpectedBefore.Keys) {
  if (-not (Test-Path -LiteralPath $Rel)) { throw "HARD STOP: required documentation file missing: $Rel" }
  $Got = (Get-FileHash -LiteralPath $Rel -Algorithm SHA256).Hash.ToLowerInvariant()
  if ($Got -ne $ExpectedBefore[$Rel]) { throw "HARD STOP: documentation base mismatch: $Rel ($Got). Reconcile; do not overwrite." }
}

$NewExpected = @{
  'definitions/c11d/production/D_RENDERER_REQUEST_SCOPED_PAYLOAD_MATERIALIZATION_BINDING_SCHEMA_V1.json' = '45b1df4af2861bd23641cdaca6e4a2b7e2872bcedd1e36b590b132fd09195ff0'
  'definitions/c11d/production/D_RENDERER_REQUEST_SCOPED_PAYLOAD_MATERIALIZATION_BINDING_V1.json' = '3ca013cb1f798b03ef0b595072429e038bd98054b5c10cd694b3ac9c3c225a76'
  'tools/c11d/d9/d_renderer_request_scoped_payload_materialization_binding.py' = '244426e8f742e221f1fbb6885103135bd01d202cb6c8b641f877bd089e81ab9d'
  'tools/c11d/d9/test_d_renderer_request_scoped_payload_materialization_binding.py' = '6407fc1cf7b6560b83362445452c79204233e9bb39e261b7042d12acdb6219f6'
  'docs/current/d/D_RENDERER_REQUEST_SCOPED_PAYLOAD_MATERIALIZATION_BINDING_CHECKPOINT_V1.md' = '9a60a3c0ae018dfc99ac91303913ff1a71ab7b126069fdbe003e5c3316531aa8'
}
foreach ($Rel in $NewExpected.Keys) {
  if (Test-Path -LiteralPath $Rel) {
    $Got = (Get-FileHash -LiteralPath $Rel -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($Got -ne $NewExpected[$Rel]) { throw "HARD STOP: destination exists with unexpected bytes: $Rel ($Got)" }
    throw "HARD STOP: this overlay appears partly/already applied ($Rel). Inspect and skip reapplication rather than force-overwrite."
  }
}
$OverlayReadmePath = '.\README_C11D_RENDERER_REQUEST_SCOPED_PAYLOAD_MATERIALIZATION_BINDING_OVERLAY_V1.md'
if (Test-Path -LiteralPath $OverlayReadmePath) { throw 'HARD STOP: overlay README already exists in destination; inspect before applying.' }

Add-Type -AssemblyName System.IO.Compression.FileSystem
$Zip = [System.IO.Compression.ZipFile]::OpenRead($Overlay)
try {
  $ExpectedEntries = @(
    'definitions/c11d/production/D_RENDERER_REQUEST_SCOPED_PAYLOAD_MATERIALIZATION_BINDING_SCHEMA_V1.json',
    'definitions/c11d/production/D_RENDERER_REQUEST_SCOPED_PAYLOAD_MATERIALIZATION_BINDING_V1.json',
    'tools/c11d/d9/d_renderer_request_scoped_payload_materialization_binding.py',
    'tools/c11d/d9/test_d_renderer_request_scoped_payload_materialization_binding.py',
    'docs/current/d/D_RENDERER_REQUEST_SCOPED_PAYLOAD_MATERIALIZATION_BINDING_CHECKPOINT_V1.md',
    'docs/current/d/D_RENDERER_BASELINE_PREPARATION_PLAN_V1.md',
    'docs/current/d/D_RENDERER_CANDIDATE_IO_CONTRACT_CHECKPOINT_V1.md',
    'docs/current/d/C11D_CONTEXT_CHECKPOINT_D10_20261011.md',
    'docs/current/d/MASTER_HANDOVER_C11D_CURRENT.md',
    'docs/current/d/START_PROMPT_C11D_CURRENT.md',
    'docs/current/d/C11-D_ROADMAP_V1.0_STATELESS.md',
    'README_C11D_RENDERER_REQUEST_SCOPED_PAYLOAD_MATERIALIZATION_BINDING_OVERLAY_V1.md'
  )
  $ActualEntries = @($Zip.Entries | ForEach-Object { $_.FullName.Replace('\\','/') } | Sort-Object)
  $WantEntries = @($ExpectedEntries | Sort-Object)
  if (($ActualEntries -join "`n") -ne ($WantEntries -join "`n")) { throw 'HARD STOP: archive entry list differs from the 12-file allowlist.' }
} finally { $Zip.Dispose() }

Expand-Archive -LiteralPath $Overlay -DestinationPath $Root -Force
if ((Get-FileHash '.\release\C11C_FREEZE_PACKAGE_MANIFEST.json' -Algorithm SHA256).Hash.ToLowerInvariant() -ne $ExpectedManifest) { throw 'HARD STOP: frozen manifest changed after apply.' }
if ((Get-FileHash '.\definitions\c11d\production\D_RENDERER_UNIFIED_DELIVERY_TIMEBASE_POLICY_PROPOSAL_V1.json' -Algorithm SHA256).Hash.ToLowerInvariant() -ne $ExpectedTimebase) { throw 'HARD STOP: timebase bytes changed after apply.' }
Write-Host 'Overlay applied; C11-C manifest and timebase bytes are unchanged.'
```

Paste the exact 64-character SHA-256 from the delivery message when prompted. This avoids requiring that the separate `.sha256` sidecar also be downloaded. The script is intentionally fail-closed and will stop if the docs differ from the expected base. Do not remove those checks to force application.

## Validation after application

```powershell
python -B .\tools\c11d\d9\test_d_renderer_request_scoped_payload_materialization_binding.py
# The next command invokes both existing headless Godot harnesses for real. Supply the installed Godot 4.7.1 console path.
python -B .\tools\c11d\d9\d_renderer_request_scoped_payload_materialization_binding.py --godot 'C:\PATH\TO\Godot_v4.7.1-stable_win64_console.exe'
python -B .\tools\c11d\d9\test_d_renderer_request_scoped_payload_binding.py
python -B .\tools\c11d\d9\test_d_renderer_visual_payload_materialization_preview.py
python -B .\tools\c11d\d9\test_d_renderer_challenge_visual_payload_preview.py
python -B .\tools\c11d\d9\test_d_renderer_candidate_io_contract.py
python -B .\tools\c11d\d9\test_d_renderer_unified_content_review.py
python -B .\tools\c11d\d9\test_cross_suite_lifecycle.py
python -B .\tools\c11d\baseline_candidate\test_d_baseline_candidate.py
```

Use the real Godot 4.7.1 console binary in place of the example path, or omit `--godot` if `godot` resolves on `PATH`. Do not redirect the runner output to a file: its receipt is intentionally console-only. The Python unit test uses mocked harness stdout and is not a substitute for the real runner command.

## Scope after a PASS

A PASS establishes only that those fixed fixtures are source-bound to the observed in-memory payload digests under the listed inputs. It does not establish dynamic request transport, arbitrary editorial-value consumption, a D renderer baseline, field approval, D4.8 authorization, D9 closure, media creation or release readiness. Keep all gates closed.
