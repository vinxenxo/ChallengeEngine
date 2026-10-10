$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$updates = @(
  @{ Path='docs/current/d/D9_SUITE_INTEGRATION_PLAN_V1.md'; Marker='<!-- C11D_CHALLENGE_COORDINATE_PROJECTION_PREVIEW_V1 -->'; Heading='## Increment — Challenge Coordinate Projection Preview V1'; Body='Added a proposed, D-owned coordinate projection preview using the frozen `CoordinateMapper`: `CANVAS_1080X1920` → `540x960` at 0.5, then → `REVIEW_720 720x1280` at 4/3, composing to 2/3. A detached in-memory list projects 420 GAME positions and projects three asset intrinsic base sizes while preserving local snapshot multipliers and other snapshot values. Delivery sampling/interpolation remains unresolved; no rendering, renderer input, file output or media is produced.' },
  @{ Path='docs/current/d/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_PREVIEW_CHECKPOINT_V1.md'; Marker='<!-- C11D_CHALLENGE_COORDINATE_PROJECTION_PREVIEW_V1 -->'; Heading='## Follow-on — Coordinate Projection Preview V1'; Body='The projection proposal now formalizes `CANVAS_1080X1920` → `540x960` at uniform scale 0.5 and `540x960` → `REVIEW_720 720x1280` at uniform scale 4/3. The composed coordinate scale is 2/3. Use `tools/c11d/d9/review_challenge_coordinate_projection_in_memory.gd` only for a headless in-memory review, after passing its Python contract. This does not approve the mapping and does not resolve delivery resampling or interpolation.' },
  @{ Path='docs/current/d/MASTER_HANDOVER_C11D_CURRENT.md'; Marker='<!-- C11D_CHALLENGE_COORDINATE_PROJECTION_PREVIEW_V1 -->'; Heading='## Resume — Challenge Coordinate Projection Preview V1'; Body='Run `python tools/c11d/d9/test_d_renderer_challenge_coordinate_projection.py`, then `godot --headless --path . --script res://tools/c11d/d9/review_challenge_coordinate_projection_in_memory.gd`. Require a clean PASS and no `ERROR:`/`SCRIPT ERROR:`. Expected coordinate stages are 1080x1920→540x960 (0.5)→REVIEW_720 720x1280 (4/3), combined 2/3. 420 GAME positions and three asset base sizes are projected into a detached review representation; source simulation fields remain unchanged. Keep delivery sampling/interpolation unresolved, renderer OFF, D4.8 BLOCKED, release authority NONE.' },
  @{ Path='docs/current/d/START_PROMPT_C11D_CURRENT.md'; Marker='<!-- C11D_CHALLENGE_COORDINATE_PROJECTION_PREVIEW_V1 -->'; Heading='## Next check — Challenge Coordinate Projection Preview V1'; Body='Validate the contract test and execute the in-memory Godot coordinate projection harness. Accept only clean deterministic output and simulation invariance. This is a proposed transform preview, not renderer input. The projection is 0.5 from source coordinates to 540x960 and 4/3 to REVIEW_720 720x1280 (combined 2/3); sample selection/interpolation remains unresolved and all production locks remain active.' },
  @{ Path='docs/current/d/D9_SUITE_INTEGRATION_CHANGELOG.md'; Marker='<!-- C11D_CHALLENGE_COORDINATE_PROJECTION_PREVIEW_V1 -->'; Heading='## D Renderer Challenge Coordinate Projection Preview V1'; Body='Added a source-pinned Python contract and Godot headless preview for the proposed coordinate transform `CANVAS_1080X1920`→`540x960`→`REVIEW_720 720x1280`. The harness maps all 420 GAME positions in a detached in-memory descriptor list, projects intrinsic asset base dimensions and verifies determinism/source simulation invariance. No rendering, resampling, files, renderer input, or media is created.' }
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
Write-Output "C11-D Challenge coordinate projection docs update PASS | added=$added | already_present=$already | targets=$($updates.Count) | overwrite=FALSE"
