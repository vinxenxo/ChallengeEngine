$ErrorActionPreference = 'Stop'
$repoRoot = (Get-Location).Path
$updates = @(
  [pscustomobject]@{ Path='docs/current/d/D_RENDERER_BASELINE_PREPARATION_PLAN_V1.md'; Marker='<!-- C11D_REQUEST_SCOPED_PAYLOAD_BINDING_V1_PLAN -->'; Section=@'
<!-- C11D_REQUEST_SCOPED_PAYLOAD_BINDING_V1_PLAN -->

## Request-scoped payload source binding — 2026-10-10

`tools/c11d/d9/d_renderer_request_scoped_payload_binding.py` now resolves the exact selection in the canonical D9.9 request against a pinned canonical source and audits the complete D9.9→D9.10→renderer-neutral review chain. V1 covers only `parking_v2/CHALLENGE_004`, `c11c_geometric_waves_v1/harmonic_membrane`, and `tracking/tier-2`, because the current temporal/editorial reference contracts are pinned to those examples. Other pairs fail closed.

Critical distinction: source resolution is not instance materialization. Challenge runtime payload remains absent; the Visual Loop family profile is not a grammar-specific instance; a Visual Drill type/tier example is not a request-generated instance. Payload instance ID/hash/path remain null and `video_render_ready=false`. Next required engineering item is a separately governed request-specific payload materializer that consumes the real seed/profile/selection and emits a hash-bound in-memory or approved review artifact without mutation of C11-C.
'@ },
  [pscustomobject]@{ Path='docs/current/d/D9_SUITE_INTEGRATION_CHANGELOG.md'; Marker='<!-- C11D_REQUEST_SCOPED_PAYLOAD_BINDING_V1_CHANGELOG -->'; Section=@'
<!-- C11D_REQUEST_SCOPED_PAYLOAD_BINDING_V1_CHANGELOG -->

## 2026-10-10 — request-scoped visual source binding V1

Added a fail-closed audit for three representative canonical D9.9 requests. It hashes the selected definition and registry and validates source identity through the bridge, PREPARE_ONLY adapter, binding preview, logical composition, frame program, temporal projection and editorial review. It explicitly does not claim that a request-specific visual payload has been generated and does not enable renderer/media output.
'@ },
  [pscustomobject]@{ Path='docs/current/d/MASTER_HANDOVER_C11D_CURRENT.md'; Marker='<!-- C11D_REQUEST_SCOPED_PAYLOAD_BINDING_V1_HANDOVER -->'; Section=@'
<!-- C11D_REQUEST_SCOPED_PAYLOAD_BINDING_V1_HANDOVER -->

## Request-scoped payload binding checkpoint (2026-10-10)

Run `python .\tools\c11d\d9\test_d_renderer_request_scoped_payload_binding.py`. V1 validates the exact representative selection/source references and the D9.9→D9.10→renderer-neutral/temporal/editorial chain. It deliberately reports `exact_request_payload_instance_materialized=false` for all three types. Visual Loop family definitions are not grammar-generated instances, and Visual Drill type/tier definitions are not per-request generated payloads. The renderer remains OFF and no media is created.
'@ },
  [pscustomobject]@{ Path='docs/current/d/START_PROMPT_C11D_CURRENT.md'; Marker='<!-- C11D_REQUEST_SCOPED_PAYLOAD_BINDING_V1_START_PROMPT -->'; Section=@'
<!-- C11D_REQUEST_SCOPED_PAYLOAD_BINDING_V1_START_PROMPT -->

## Current context addendum — request-scoped payload binding V1 (2026-10-10)

After the delivery-timebase, temporal-preview and editorial-review tests pass, run the request-scoped payload binding test. Treat its PASS as a source-resolution/chain-integrity PASS only, not as proof a visual instance is generated. The next engineering stage is the governed request-specific payload materializer and explicit visual/editorial review; do not activate renderer or produce media until the independent D baseline approval and D4.8 authorization gates are met.
'@ }
)
foreach ($item in $updates) {
  $full = Join-Path $repoRoot $item.Path
  if (-not (Test-Path -LiteralPath $full -PathType Leaf)) { throw "Required document missing; no files modified: $($item.Path)" }
  $content = [System.IO.File]::ReadAllText($full, [System.Text.Encoding]::UTF8)
  $count = ([regex]::Matches($content, [regex]::Escape($item.Marker))).Count
  if ($count -gt 1) { throw "Duplicate marker; no files modified: $($item.Path)" }
}
$encoding = [System.Text.UTF8Encoding]::new($false)
$added = 0; $skipped = 0
foreach ($item in $updates) {
  $full = Join-Path $repoRoot $item.Path
  $content = [System.IO.File]::ReadAllText($full, [System.Text.Encoding]::UTF8)
  if ($content.Contains($item.Marker)) { $skipped++; continue }
  [System.IO.File]::AppendAllText($full, [Environment]::NewLine + [Environment]::NewLine + $item.Section.Trim() + [Environment]::NewLine, $encoding)
  $added++
}
Write-Output "C11-D request-scoped payload binding docs update PASS | added=$added | already_present=$skipped | targets=$($updates.Count) | overwrite=FALSE"
