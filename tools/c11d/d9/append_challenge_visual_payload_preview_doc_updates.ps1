$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$updates = @(
  @{ Path='docs/current/d/D_RENDERER_BASELINE_PREPARATION_PLAN_V1.md'; Marker='<!-- C11D_CHALLENGE_VISUAL_PAYLOAD_PREVIEW_V1 -->'; Heading='## Increment — Challenge Visual Payload Preview V1'; Body='Added a Godot headless in-memory logical visual payload builder for CHALLENGE_004. It invokes the frozen runtime twice, rebinds social_default_v1 on a deep copy, loads and hashes the three canonical SVG Texture2D assets, preserves all 420 GAME transform snapshots at source 60 FPS, excludes telemetry/winning_frame/close_calls, and checks simulation invariance. Coordinate projection and 30 FPS sample selection/interpolation remain unresolved and are not applied. The payload is not renderer input and is never written to disk.' },
  @{ Path='docs/current/d/MASTER_HANDOVER_C11D_CURRENT.md'; Marker='<!-- C11D_CHALLENGE_VISUAL_PAYLOAD_PREVIEW_V1 -->'; Heading='## Challenge Visual Payload Preview V1'; Body='After the 10-source contract test, run `godot --headless --path . --script res://tools/c11d/d9/materialize_challenge_visual_payload_in_memory.gd`, then rerun the Python contract test. Accept only a clean Godot PASS with no `ERROR:`/`SCRIPT ERROR:` lines. This harness binds the authentic source-timebase GAME snapshots and canonical static assets into a deterministic in-memory logical payload. It intentionally does not resolve the CANVAS_1080X1920 versus profile source-canvas projection or resample to 30 FPS. No scene nodes, media, files, renderer input or authority are created. The current unified review runner has not yet incorporated this sixth harness; its follow-on integration must consume this preview before the unified gate summary is treated as current.' },
  @{ Path='docs/current/d/START_PROMPT_C11D_CURRENT.md'; Marker='<!-- C11D_CHALLENGE_VISUAL_PAYLOAD_PREVIEW_V1 -->'; Heading='## Resume — Challenge Visual Payload Preview V1'; Body='Validate `tools/c11d/d9/test_d_renderer_challenge_visual_payload_preview.py`, then run `godot --headless --path . --script res://tools/c11d/d9/materialize_challenge_visual_payload_in_memory.gd`, requiring a clean `C11-D RENDERER CHALLENGE VISUAL PAYLOAD PREVIEW PASS`. If clean, rerun the contract test. The result only proves an in-memory source-timebase logical payload (3 assets + 420 GAME transform records) and simulation invariance. Coordinate projection and delivery sampling remain unresolved. Keep renderer OFF, D4.8 BLOCKED and release authority NONE.' },
  @{ Path='docs/current/d/D9_SUITE_INTEGRATION_CHANGELOG.md'; Marker='<!-- C11D_CHALLENGE_VISUAL_PAYLOAD_PREVIEW_V1 -->'; Heading='## D Renderer Challenge Visual Payload Preview V1'; Body='Added a D-owned headless harness to build a deterministic source-timebase Challenge visual payload in memory from the authentic runtime result, canonical PresentationBinder render model and three physical SVG assets. The 420 GAME snapshot transforms remain in source order at 60 FPS; visual telemetry fields are omitted. No frame drawing, renderer-native input, persistence or media is produced. This harness remains separately accepted pending its Windows Godot run; it has not been added to the 22-step aggregate.' }
)
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
Write-Output "C11-D Challenge visual payload preview docs update PASS | added=$added | already_present=$already | targets=$($updates.Count) | overwrite=FALSE"
