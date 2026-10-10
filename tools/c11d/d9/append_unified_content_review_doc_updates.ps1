$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$updates = @(
  @{ Path='docs/current/d/D_RENDERER_BASELINE_PREPARATION_PLAN_V1.md'; Marker='<!-- C11D_UNIFIED_CONTENT_REVIEW_V1 -->'; Heading='## Increment — Unified Content Review V1'; Body='Added a console-only orchestrator which sequentially runs the existing Visual Loop/Drill payload, Challenge runtime, profile identity, delivery timeline and editorial field-window harnesses. It joins summaries by pinned source identity and digest and rejects any Godot `ERROR:`/`SCRIPT ERROR:` line even when a PASS marker is present. The result distinguishes a consistent review chain from video readiness: Loop/Drill editorial mappings and Challenge visual payload/sample-selection policy remain unresolved. No persistent report, renderer input, media or authority change.' },
  @{ Path='docs/current/d/MASTER_HANDOVER_C11D_CURRENT.md'; Marker='<!-- C11D_UNIFIED_CONTENT_REVIEW_V1 -->'; Heading='## Unified Content Review V1'; Body='Use `python .\tools\c11d\d9\test_d_renderer_unified_content_review.py`, then `python .\tools\c11d\d9\run_d_renderer_unified_content_review.py --godot godot`. The runner executes five existing Godot 4.7.1 in-memory harnesses, verifies their summary hashes, source identity, timing, editorial field-window and simulation invariance cross-checks, and emits a joined JSON summary to stdout only. It does not write the report. A PASS means review-chain consistency only, not render readiness. Keep the Loop/Drill editorial maps unresolved, Challenge visual payload unmaterialized, timebase/field-window policies proposed, renderer OFF, D4.8 blocked and release authority NONE.' },
  @{ Path='docs/current/d/START_PROMPT_C11D_CURRENT.md'; Marker='<!-- C11D_UNIFIED_CONTENT_REVIEW_V1 -->'; Heading='## Resume — Unified Content Review V1'; Body='Run the unified contract test, then `python .\tools\c11d\d9\run_d_renderer_unified_content_review.py --godot godot`. This launches the five established review-only Godot harnesses sequentially and joins their outputs in memory. The runner must fail on nonzero exit, missing PASS/summary markers, source/hash drift, or any `ERROR:`/`SCRIPT ERROR:` log even if a harness prints PASS. Expected review is consistent but not video-ready. Do not turn the console summary into a renderer input or persistent report; no media is authorized.' },
  @{ Path='docs/current/d/D9_SUITE_INTEGRATION_CHANGELOG.md'; Marker='<!-- C11D_UNIFIED_CONTENT_REVIEW_V1 -->'; Heading='## D Renderer Unified Content Review V1'; Body='Added an in-memory cross-artifact coordinator for the Visual Loop and Drill materialization previews, real Challenge runtime output, profile identity split, delivery timeline review and editorial field-window proposal. It records each child harness and summary digest, checks cross-artifact identity and invariance, and rejects false PASS caused by runtime error logs. No harness is added to the frozen 22-step aggregate in this increment; no renderer/media/authority change.' }
)
# Preflight every target before any write.
foreach ($entry in $updates) {
  $path = Join-Path $root $entry.Path
  if (-not (Test-Path -LiteralPath $path -PathType Leaf)) { throw "Required documentation target missing: $($entry.Path)" }
}
$added=0; $already=0
foreach ($entry in $updates) {
  $path = Join-Path $root $entry.Path
  $content = [System.IO.File]::ReadAllText($path)
  if ($content.Contains($entry.Marker)) { $already++; continue }
  $append = "`r`n$($entry.Marker)`r`n$($entry.Heading)`r`n`r`n$($entry.Body)`r`n"
  [System.IO.File]::WriteAllText($path, $content.TrimEnd() + $append, [System.Text.UTF8Encoding]::new($false))
  $added++
}
Write-Output "C11-D unified content review docs update PASS | added=$added | already_present=$already | targets=$($updates.Count) | overwrite=FALSE"
