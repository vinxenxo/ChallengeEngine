$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$updates = @(
  @{ Path = 'docs/current/d/D_RENDERER_BASELINE_PREPARATION_PLAN_V1.md'; Marker = '<!-- C11D_CHALLENGE_RUNTIME_OUTPUT_PREVIEW_V1 -->'; Heading = '## D9 CHALLENGE_004 in-memory runtime output preview'; Body = 'The challenge runtime preview invokes the frozen `ChallengeRuntimeBridge.run_effective_pipeline` twice for source `CHALLENGE_004.json` and summarizes only in-memory runtime results. The SimulationResult is real runtime evidence, but is **not** a rendered/visual challenge payload; no image/video or renderer input is produced. See `D_RENDERER_CHALLENGE_RUNTIME_OUTPUT_PREVIEW_CHECKPOINT_V1.md`.' },
  @{ Path = 'docs/current/d/MASTER_HANDOVER_C11D_CURRENT.md'; Marker = '<!-- C11D_CHALLENGE_RUNTIME_OUTPUT_PREVIEW_V1 -->'; Heading = '## Latest increment — CHALLENGE_004 frozen runtime output preview'; Body = 'An isolated Godot headless harness runs the existing effective C11-C Challenge runtime twice and compares stable summaries in memory. It captures source editorial copy, timing phases, actual GAME SimulationResult frame signature, read-only local winning_frame, and presentation/asset binding metadata. This does not materialize the challenge visual payload, invoke the renderer, create media or grant authority.' },
  @{ Path = 'docs/current/d/START_PROMPT_C11D_CURRENT.md'; Marker = '<!-- C11D_CHALLENGE_RUNTIME_OUTPUT_PREVIEW_V1 -->'; Heading = '## Current renderer-preparation state — Challenge runtime output preview'; Body = 'To test the CHALLENGE_004 runtime preview run the Python contract test and `godot --headless --path . --script res://tools/c11d/d9/materialize_challenge_runtime_output_in_memory.gd`. This harness calls `ChallengeRuntimeBridge.run_effective_pipeline` twice and prints digest-only in-memory evidence. It does not render or persist output. A real SimulationResult is not a visual challenge payload; keep renderer OFF, D4.8 BLOCKED, authority NONE.' },
  @{ Path = 'docs/current/d/D9_SUITE_INTEGRATION_CHANGELOG.md'; Marker = '<!-- C11D_CHALLENGE_RUNTIME_OUTPUT_PREVIEW_V1 -->'; Heading = '### D renderer Challenge runtime output preview V1'; Body = 'Added a headless in-memory evidence harness for CHALLENGE_004 using the frozen effective ChallengeRuntimeBridge, two-run deterministic digest comparison, GAME-local frame-signature summary, canonical editorial copy, phase cardinality and presentation-binding metadata. No files/media/renderer input; no C11-C source mutation; D4.8 remains blocked.' }
)
$added = 0; $already = 0
foreach ($entry in $updates) {
  $path = Join-Path $root $entry.Path
  if (-not (Test-Path -LiteralPath $path -PathType Leaf)) { throw "Required documentation target missing: $($entry.Path)" }
  $content = Get-Content -LiteralPath $path -Raw -Encoding UTF8
  if ($content.Contains($entry.Marker)) { $already++; continue }
  Add-Content -LiteralPath $path -Value ("`r`n$($entry.Marker)`r`n$($entry.Heading)`r`n`r`n$($entry.Body)`r`n") -Encoding UTF8
  $added++
}
Write-Output "C11-D challenge runtime output preview docs update PASS | added=$added | already_present=$already | targets=$($updates.Count) | overwrite=FALSE"
