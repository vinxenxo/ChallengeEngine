$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$updates = @(
  @{ Path = 'docs/current/d/D_RENDERER_BASELINE_PREPARATION_PLAN_V1.md'; Marker = '<!-- C11D_VISUAL_PAYLOAD_MATERIALIZATION_PREVIEW_V1 -->'; Heading = '## D9 visual payload materialization preview V1'; Body = 'D9 V1 now contains a headless, in-memory materialization harness for the exact Visual Loop `harmonic_membrane` and Visual Drill `tracking/tier-2` review fixtures using existing C11-C authoring APIs. It prints only hashes and frame/timing summaries, does not persist payloads or media, and leaves Challenge runtime output unresolved. `variation_index` is metadata-only in this V1. See `D_RENDERER_VISUAL_PAYLOAD_MATERIALIZATION_PREVIEW_CHECKPOINT_V1.md`.' },
  @{ Path = 'docs/current/d/MASTER_HANDOVER_C11D_CURRENT.md'; Marker = '<!-- C11D_VISUAL_PAYLOAD_MATERIALIZATION_PREVIEW_V1 -->'; Heading = '## Latest increment — in-memory visual payload materialization preview'; Body = 'The current preview stage materializes two exact request-scoped visual authoring payloads in memory through the existing C11-C API: geometric/harmonic_membrane and tracking/tier-2. This is not renderer input. CHALLENGE_004 remains dependent on frozen ChallengeExecutionPipeline output. C11-C stays immutable; renderer OFF; no media; D4.8 BLOCKED; release authority NONE.' },
  @{ Path = 'docs/current/d/START_PROMPT_C11D_CURRENT.md'; Marker = '<!-- C11D_VISUAL_PAYLOAD_MATERIALIZATION_PREVIEW_V1 -->'; Heading = '## Current renderer-preparation state — visual payload materialization preview'; Body = 'The latest isolated increment is the D renderer in-memory visual payload materialization preview. Run the Python contract test and the Godot headless harness. It prepares Visual Loop and Visual Drill review payloads only; it does not write payload files, render video or resolve the Challenge runtime payload. Treat `variation_index` as metadata-only until an explicit policy is approved.' },
  @{ Path = 'docs/current/d/D9_SUITE_INTEGRATION_CHANGELOG.md'; Marker = '<!-- C11D_VISUAL_PAYLOAD_MATERIALIZATION_PREVIEW_V1 -->'; Heading = '### D renderer visual payload materialization preview V1'; Body = 'Added a headless in-memory materialization contract/harness for exact Visual Loop and Visual Drill review fixtures, with source lineage, deterministic payload digests, and negative governance tests. No persisted output, renderer invocation, media generation, C11-C source mutation or D4.8 authorization.' }
)
$added = 0; $already = 0
foreach ($entry in $updates) {
  $path = Join-Path $root $entry.Path
  if (-not (Test-Path -LiteralPath $path -PathType Leaf)) { throw "Required documentation target missing: $($entry.Path)" }
  $content = Get-Content -LiteralPath $path -Raw -Encoding UTF8
  if ($content.Contains($entry.Marker)) { $already++; continue }
  $block = "`r`n$($entry.Marker)`r`n$($entry.Heading)`r`n`r`n$($entry.Body)`r`n"
  Add-Content -LiteralPath $path -Value $block -Encoding UTF8
  $added++
}
Write-Output "C11-D visual payload materialization preview docs update PASS | added=$added | already_present=$already | targets=$($updates.Count) | overwrite=FALSE"
