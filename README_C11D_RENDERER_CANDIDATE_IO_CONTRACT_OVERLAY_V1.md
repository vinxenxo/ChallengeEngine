# C11-D — Renderer Candidate I/O Contract V1 Overlay

## Purpose

This incremental overlay defines the first complete, D-owned prospective input/output interface for a future renderer candidate. It closes a contract-design gap; it **does not implement or activate a renderer**.

The I/O contract is `PREPARATION_ONLY_INTERFACE_PROPOSAL_NOT_IMPLEMENTED_NOT_APPROVED`. Its strict schemas describe what a future approved input instance and QA-bound output manifest must contain. A current input remains inadmissible: no request-specific payload instance is materialized for all three content types, shared policy proposals remain unapproved, the renderer baseline is not approved/frozen, and D4.8 remains blocked.

This overlay also aligns the existing byte-level hash chain for timebase → audio/music → unified review, and changes the timebase negative test to restore exact saved bytes instead of text-normalizing source line endings. It does not modify the timebase proposal bytes themselves.

## Exact contents

### New files (6)

- `definitions/c11d/production/D_RENDERER_CANDIDATE_IO_CONTRACT_V1.json`
- `definitions/c11d/production/D_RENDERER_CANDIDATE_IO_CONTRACT_SCHEMA_V1.json`
- `definitions/c11d/production/D_RENDERER_CANDIDATE_INPUT_SCHEMA_V1.json`
- `definitions/c11d/production/D_RENDERER_CANDIDATE_OUTPUT_MANIFEST_SCHEMA_V1.json`
- `tools/c11d/d9/test_d_renderer_candidate_io_contract.py`
- `docs/current/d/D_RENDERER_CANDIDATE_IO_CONTRACT_CHECKPOINT_V1.md`

### Modified files (12)

- `definitions/c11d/production/D_RENDERER_UNIFIED_AUDIO_MUSIC_DELIVERY_POLICY_PROPOSAL_SCHEMA_V1.json`
- `definitions/c11d/production/D_RENDERER_UNIFIED_AUDIO_MUSIC_DELIVERY_POLICY_PROPOSAL_V1.json`
- `definitions/c11d/production/D_RENDERER_UNIFIED_CONTENT_REVIEW_SCHEMA_V1.json`
- `definitions/c11d/production/D_RENDERER_UNIFIED_CONTENT_REVIEW_V1.json`
- `tools/c11d/d9/d_renderer_unified_audio_music_delivery_policy.py`
- `tools/c11d/d9/d_renderer_unified_content_review.py`
- `tools/c11d/d9/test_d_renderer_unified_delivery_timebase_policy.py`
- `docs/current/d/C11D_CONTEXT_CHECKPOINT_D10_20261011.md`
- `docs/current/d/C11-D_ROADMAP_V1.0_STATELESS.md`
- `docs/current/d/D_RENDERER_BASELINE_PREPARATION_PLAN_V1.md`
- `docs/current/d/MASTER_HANDOVER_C11D_CURRENT.md`
- `docs/current/d/START_PROMPT_C11D_CURRENT.md`

This overlay includes the prior D10 reconciliation content in its current checkpoint/roadmap/handover/prompt versions. It is a cumulative replacement of those five documentation files; it does not include any runtime ledger or C11-C freeze artifact.

## Integrity preconditions — do not skip

The overlay is based on the inspected first-entry/canonical-manifest view of `ChallengeEngineV01_STATELESS_C11-D10_LATEST_20261011_203730.zip` (archive SHA-256 `8fd1957adaee0a0380048c9f789da661454dff22e662aba5fc6327cac4d622e8`). That export contains a duplicate historical freeze-manifest path and omits operator-runtime ledgers confirmed present in the user's Windows checkout. **Never extract the full context ZIP over the active checkout.**

Before applying this overlay, the active checkout must meet these byte-level preconditions:

- Frozen manifest SHA-256: `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.
- Timebase proposal SHA-256: `251b2384aabfe975b55938bc4a6696aba81b8dc817aa6902bf1f60f3894ad019`.
- The seven existing code/policy files being replaced must match the baseline SHA-256 values encoded in the PowerShell preflight below.
- The five documentation targets may match either the original context ZIP version or the earlier `C11D_D10_RECONCILIATION_OVERLAY_V1` version. Any other hash means stop and reconcile before overwriting local work.

The first command below is read-only and refuses to continue on any mismatch. Do not remove the guard just to force the extraction through.

## Apply from Windows PowerShell

Save the ZIP to Downloads. Run from the repository root:

```powershell
$ErrorActionPreference = 'Stop'
$Root = 'C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS'
Set-Location $Root
$Overlay = Join-Path $env:USERPROFILE 'Downloads\C11D_RENDERER_CANDIDATE_IO_CONTRACT_OVERLAY_V1.zip'
$Sidecar = "$Overlay.sha256"
if (-not (Test-Path -LiteralPath $Sidecar)) { throw 'HARD STOP: overlay .sha256 sidecar is missing.' }
$ExpectedZip = ((Get-Content -LiteralPath $Sidecar -Raw).Trim() -split '\s+')[0].ToLowerInvariant()
$ActualZip = (Get-FileHash $Overlay -Algorithm SHA256).Hash.ToLowerInvariant()
if ($ActualZip -ne $ExpectedZip) { throw "HARD STOP: overlay SHA-256 mismatch: $ActualZip" }

$ExpectedManifest = 'e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953'
$ManifestPath = '.\release\C11C_FREEZE_PACKAGE_MANIFEST.json'
if ((Get-FileHash $ManifestPath -Algorithm SHA256).Hash.ToLowerInvariant() -ne $ExpectedManifest) {
    throw 'HARD STOP: C11-C frozen manifest precondition failed.'
}
$Timebase = '.\definitions\c11d\production\D_RENDERER_UNIFIED_DELIVERY_TIMEBASE_POLICY_PROPOSAL_V1.json'
if ((Get-FileHash $Timebase -Algorithm SHA256).Hash.ToLowerInvariant() -ne '251b2384aabfe975b55938bc4a6696aba81b8dc817aa6902bf1f60f3894ad019') {
    throw 'HARD STOP: local timebase bytes differ from the exact source pinned by this overlay. Do not overwrite.'
}

# Existing policy/code files must still be the exact source-export versions.
$ExpectedBefore = @{
  'definitions/c11d/production/D_RENDERER_UNIFIED_AUDIO_MUSIC_DELIVERY_POLICY_PROPOSAL_SCHEMA_V1.json' = '04359ac7fc2af04a9203849192e16e3e8bef00e91563bc1d9813f094e2fef041'
  'definitions/c11d/production/D_RENDERER_UNIFIED_AUDIO_MUSIC_DELIVERY_POLICY_PROPOSAL_V1.json' = '12d9000b73f09318a005e8f1d76e2efb2777469715dfeb7d686760600ba11238'
  'definitions/c11d/production/D_RENDERER_UNIFIED_CONTENT_REVIEW_SCHEMA_V1.json' = '110295f0900d6f022e1f38305f8b20a3ba9002599bc8a4952cfd64bb3397613b'
  'definitions/c11d/production/D_RENDERER_UNIFIED_CONTENT_REVIEW_V1.json' = '7c16259a205777d9f7e3e9c8995c2f4883fed54a27a4ca6fa4abb1deac64b3e7'
  'tools/c11d/d9/d_renderer_unified_audio_music_delivery_policy.py' = '39e1e789cfa40393c5efc63f7fe8d2b733b4f0ff1b8125c76ce05d2674e82b23'
  'tools/c11d/d9/d_renderer_unified_content_review.py' = 'f2191ec671364b4a7accd2cf5f1f854584e369cadaf2a652ab50aa08bdfd7ef6'
  'tools/c11d/d9/test_d_renderer_unified_delivery_timebase_policy.py' = 'b8a597af7196621393623b8198e5c861fee0b904922c5339188267a32dff7acb'
}
foreach ($Rel in $ExpectedBefore.Keys) {
    if (-not (Test-Path -LiteralPath $Rel)) { throw "HARD STOP: required base file missing: $Rel" }
    $Got = (Get-FileHash -LiteralPath $Rel -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($Got -ne $ExpectedBefore[$Rel]) { throw "HARD STOP: local file differs from overlay base: $Rel ($Got)" }
}

# Documentation may be at either the source ZIP state or the prior reconciliation overlay state.
$AllowedDocs = @{
  'docs/current/d/C11D_CONTEXT_CHECKPOINT_D10_20261011.md' = @('947fc4f415b091afd2c81e5e31d90ab28ee4651b5bab1a90340c9163b9344f52','c5d1e3d07f9d2e7ea49f61bf4ead74d0daf4f705511c9a82248c9a234eacec54')
  'docs/current/d/C11-D_ROADMAP_V1.0_STATELESS.md' = @('ee151385930d5cb377cc43cc40bc8ea59d9db816388c8b4241047c97c877ea10','1b58f55d3f53370eb8ab0b7e06c5fc4fc8e2f430e4e1213053a23c27dba4a0e9')
  'docs/current/d/D_RENDERER_BASELINE_PREPARATION_PLAN_V1.md' = @('7552673c2e4eb065f4c574b965a4916c5bbec0a43f4b0d66b977323de7c345ae','8030fd271f705ec0ef2093b404e3b97998ddebd42ec96d5ee5afe585865be549')
  'docs/current/d/MASTER_HANDOVER_C11D_CURRENT.md' = @('2697adc9487ec1cd6ea193041858a79a5e03ed6dc101cb63debf9083493f4b29','c025297aae1076bad68db7383649fe6dfb0be1909696653e6f19265d6411a995')
  'docs/current/d/START_PROMPT_C11D_CURRENT.md' = @('39bb4b4695248186a44581f563eb71101c049d0b5129542ca88a253609e3be77','cc4d7f23065a989395730d2c55955230c661ac6baf9cba0c0e39494b8173b0d3')
}
foreach ($Rel in $AllowedDocs.Keys) {
    $Got = (Get-FileHash -LiteralPath $Rel -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($Got -notin $AllowedDocs[$Rel]) { throw "HARD STOP: documentation changed since either recognized base: $Rel ($Got)" }
}

Expand-Archive -LiteralPath $Overlay -DestinationPath $Root -Force
$ManifestAfter = (Get-FileHash $ManifestPath -Algorithm SHA256).Hash.ToLowerInvariant()
if ($ManifestAfter -ne $ExpectedManifest) { throw 'HARD STOP: frozen C11-C manifest changed after overlay.' }
$TimebaseAfter = (Get-FileHash $Timebase -Algorithm SHA256).Hash.ToLowerInvariant()
if ($TimebaseAfter -ne '251b2384aabfe975b55938bc4a6696aba81b8dc817aa6902bf1f60f3894ad019') { throw 'HARD STOP: timebase source bytes changed.' }
Write-Host 'Overlay applied; frozen manifest and timebase bytes remain unchanged.'
```

Keep the downloaded `.zip.sha256` sidecar next to the ZIP; the preflight reads the expected digest from that file. If any base precondition fails, stop and report the mismatched paths instead of extracting with `-Force`.

## Focused checks after application

```powershell
python -B .\tools\c11d\d9\test_d_renderer_candidate_io_contract.py
python -B .\tools\c11d\d9\test_d_renderer_candidate.py
python -B .\tools\c11d\d9\test_d_renderer_logical_composition.py
python -B .\tools\c11d\d9\test_d_renderer_frame_program.py
python -B .\tools\c11d\d9\test_d_renderer_request_scoped_payload_binding.py
python -B .\tools\c11d\d9\test_d_renderer_visual_payload_materialization_preview.py
python -B .\tools\c11d\d9\test_d_renderer_challenge_visual_payload_preview.py
python -B .\tools\c11d\d9\test_d_renderer_unified_presentation_region_policy.py
python -B .\tools\c11d\d9\test_d_renderer_unified_delivery_timebase_policy.py
python -B .\tools\c11d\d9\test_d_renderer_unified_audio_music_delivery_policy.py
python -B .\tools\c11d\d9\test_d_renderer_unified_content_review.py
python -B .\tools\c11d\d9\test_cross_suite_lifecycle.py
python -B .\tools\c11d\baseline_candidate\test_d_baseline_candidate.py

(Get-FileHash '.\release\C11C_FREEZE_PACKAGE_MANIFEST.json' -Algorithm SHA256).Hash.ToLowerInvariant()
(Get-FileHash '.\definitions\c11d\production\D_RENDERER_UNIFIED_DELIVERY_TIMEBASE_POLICY_PROPOSAL_V1.json' -Algorithm SHA256).Hash.ToLowerInvariant()
```

Expected final hashes are respectively `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953` and `251b2384aabfe975b55938bc4a6696aba81b8dc817aa6902bf1f60f3894ad019`. Do not add the new I/O test to the 22-step aggregate until its Windows run is reviewed.

## Verified preparation-copy results

- Candidate I/O contract: 30/30 source pins, 3/3 schemas, synthetic in-memory schema fixtures 2/2, and fail-closed negatives 13/13 under Draft 2020-12 validation. The explicit no-`jsonschema` fallback also passed with structural-only validation and static negatives 5/5; schema instance fixtures were explicitly skipped.
- Timebase 13/13; audio/music 14/14; unified content review 36/36 (17/17 cross-checks, 30/30 negatives, source lineage 22/22).
- Binding preview negatives 13/13; logical composition negatives 17/17; frame program negatives 19/19; request-scoped binding negatives 51/51; Loop/Drill materialization-preview negatives 29/29; Challenge preview 10/10 unit tests; presentation-region proposal 15 tests PASS.
- The exact frozen manifest and canonical timebase bytes were re-hashed after the relevant test runs and remained unchanged.

These are Python/static checks in an isolated preparation copy. Godot harnesses, Windows GUI/runtime acceptance and the full aggregate Suite were not executed here. This overlay does not enable renderer-native input, dispatch, rendering, media creation, baseline approval, D4.8 or release authority.

## Governance invariants

- C11-C 2.19.12 and the frozen manifest are immutable.
- D9.10 remains `PREPARE_ONLY`; renderer OFF; no media; `D4.8=BLOCKED`; `release_authority=NONE`.
- Presentation, timebase, temporal alignment, sampling, coordinate, editorial, delivery and audio/music policies remain proposals unless explicit approval evidence is added by the governing process.
- No output manifest instance or renderer-native input instance is created by this overlay.
