# C11-E — new-window start prompt (V16)

Continue the C11-E work at `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`. Read `AGENTS.md`, `.continue/rules/CONTINUE.md`, `docs/current/e/README.md`, current authority V16, gate matrix V16, E2 V8 remediation note, execution hygiene V12 and full-family roadmap V6 before acting. The supplied snapshot is context-only; never extract it over the active checkout.

**Do not restart E0/E1, do not repeat accepted work, and do not mistake CH001 A/B for the full product.** Product objective remains final A/V MP4 generation across Challenge, Visual Loop and Visual Drill, C presentation and mechanics intact, enabled D9.8 editorial fields in each real binder, D3 Music V5 on independent `request.music_seed`, FFmpeg mux, FFprobe, and a single GUI/CLI production service. C11-C remains frozen authoritative until E8.

## Latest known evidence

- Context snapshot: `C11E_WORKING_CONTEXT_20261031_191534.zip`, 9,618,925 bytes, SHA-256 `250c154ddb74813a7478d9aeb03ddaac7ccd15595c82bbfad607552f048408b5`; sidecar/report agree. Captured `main`, HEAD `b92434d6a8b50cef7e49ba6b75a4813777927fe7`, parent `a3c7c5d284a96ce115ca52208b4039002502753b`, tree `91aa803c2d675ec9fc7afff120b2bc7d3de479ef`.
- V7 failure evidence: `C11E_E2_CH001_AB_FAILURE_EVIDENCE_20261031_191440_13012eef.zip`, 29,568 bytes, 47 entries, SHA-256 `27fa769c35165e8171120bc0fce16fc3739505198157a874360c2de432c6bbe7`.
- E2 V7 pair tests 9/9 pass, but Godot A exits 40 at `_validate_c11e_sidecar`: JSON parser returns float Variants, while V7 demanded integer type for both seed fields. Only one renderer invocation/one-frame partial AVI; no B, no final MP4, no success receipt. E2 FAILED; E3 BLOCKED.
- A manual console success validation continued after the nonzero runner exit and printed a false PASS. Ignore it. Never continue success checks after failure.

## First action — reconcile active checkout and remediation package

Check live `git branch --show-current`, `git rev-parse HEAD`, `git rev-parse HEAD^`, `git rev-parse HEAD^{tree}`, `git status --short --branch`; inspect current files and V7 installer receipt. The last verified installer baseline was `main`/`b92434d`/parent `a3c7c5d`/tree `91aa803`. The operator commits locally per iteration, so a later descendant is expected, but a stale installer identity is not. If V8 installer has already been applied, verify its receipt and all postimages and **do not apply it again**. If not applied and current identity still exactly matches, inspect/install `C11E_E2_V8_JSON_FLOAT_SEED_REMEDIATION_20261031_V1.zip`; verify package SHA sidecar, V7 V2 APPLIED receipt SHA `9b8a0176d8044b433962b28042816fe1b5b1085c3a00c9fcc578abaeab7cebc6`, V7 failure ZIP SHA above, C11-C manifest and installer preimages. If identity changed, stop without writes and prepare a new iteration-specific overlay.

V8 must add the Godot-native headless JSON numeric test and use the corrected integral seed predicate. The V8 runner must execute that test before pair preparation/render and require marker `C11E_E2_GODOT_JSON_NUMERIC_CONTRACT=PASS`. Then run exactly two CHALLENGE_001 renders with fresh RequestId `C11E-E2-CH001-AB-20261031-V8`, no audio. After a nonzero exit, stop; do not type or run success-only receipt checks. Upload the new failure/success evidence ZIP separately because context snapshots exclude media and the artifacts directory.

No E3 until E2 automated technical checks and independent human visual review are both accepted. If E2 passes, next planned gate is E3 D3 Music V5 + independent `music_seed` + FFmpeg mux/FFprobe; E4A Challenge, E4B Loop, E4C Drill; E5; E6 Smoke18; E7 Matrix101 (99 runnable while CH_008/009 remain blocked); E8.

## Snapshot ZIP command for the next context window

Run only after this V16 overlay has been installed, its receipt/postimages checked and the current iteration committed locally. This makes a fresh filtered source/docs context ZIP; it deliberately excludes artifacts/media and is not a release backup. Upload the resulting ZIP, `.sha256` and `.report.json`; upload the E2 media/evidence ZIP separately.

```powershell
$ErrorActionPreference = 'Stop'
$Root = 'C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS'
$SnapshotTool = Join-Path $Root 'tools\c11d\packaging\New-C11DWorkingSnapshot.ps1'
$Documents = [Environment]::GetFolderPath('MyDocuments')
$SnapshotDirectory = Join-Path $Documents 'C11E_CONTEXT_SNAPSHOTS'
$ArchiveName = 'C11E_WORKING_CONTEXT_' + (Get-Date -Format 'yyyyMMdd_HHmmss') + '.zip'
if (-not (Test-Path -LiteralPath $SnapshotTool -PathType Leaf)) { throw ("No existe el generador: {0}" -f $SnapshotTool) }
if (-not (Test-Path -LiteralPath $SnapshotDirectory -PathType Container)) { New-Item -ItemType Directory -Path $SnapshotDirectory -Force | Out-Null }
& $SnapshotTool -OutputDirectory $SnapshotDirectory -ArchiveName $ArchiveName -PreflightOnly
if (-not $?) { throw 'SNAPSHOT PREFLIGHT FAILED.' }
& $SnapshotTool -OutputDirectory $SnapshotDirectory -ArchiveName $ArchiveName
if (-not $?) { throw 'SNAPSHOT GENERATION FAILED.' }
$SnapshotZip = Join-Path $SnapshotDirectory $ArchiveName
$SnapshotSha = (Get-FileHash -LiteralPath $SnapshotZip -Algorithm SHA256).Hash.ToLowerInvariant()
$SnapshotBytes = (Get-Item -LiteralPath $SnapshotZip).Length
$SnapshotSidecar = $SnapshotZip + '.sha256'
$SnapshotReport = $SnapshotZip + '.report.json'
if (-not (Test-Path -LiteralPath $SnapshotSidecar -PathType Leaf)) { throw 'Snapshot SHA256 sidecar missing.' }
if (-not (Test-Path -LiteralPath $SnapshotReport -PathType Leaf)) { throw 'Snapshot report missing.' }
Write-Host 'C11-E SNAPSHOT GENERATED'
Write-Host ("ZIP={0}" -f $SnapshotZip)
Write-Host ("BYTES={0}" -f $SnapshotBytes)
Write-Host ("SHA256={0}" -f $SnapshotSha)
Write-Host ("SIDECAR={0}" -f $SnapshotSidecar)
Write-Host ("REPORT={0}" -f $SnapshotReport)
```

The snapshot script derives the repository root from its own location; do **not** pass `-Root`. Never regenerate/overwrite the current snapshot as a substitute for the V7 failure archive. Preserve C11-C manifest bytes/hash exactly. Do not invoke E3 or claim promotion/release authority.
