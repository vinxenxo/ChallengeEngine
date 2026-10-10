$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$updates = @(
    @{ Path='docs/current/d/D_RENDERER_BASELINE_PREPARATION_PLAN_V1.md'; Marker='## Increment — Challenge Delivery Timeline Review V1'; Text=@'

## Increment — Challenge Delivery Timeline Review V1 (2026-10-10)

The D review harness now joins actual frozen `CHALLENGE_004` runtime timing with the D-owned `social_default_v1` presentation bind and the still-proposed `REVIEW_720@30FPS` delivery projection. It checks repeated runtime determinism and simulation invariance, then derives source ranges `[0,180,600,780,900]` and delivery ranges `[0,90,300,390,450]`. Phase ranges are not text-visibility windows; those remain unresolved. No source simulation truth is mapped to delivery frames, no renderer input is emitted, and no media is created. The timebase proposal remains unapproved and D4.8 remains BLOCKED.
'@ },
    @{ Path='docs/current/d/D9_SUITE_INTEGRATION_CHANGELOG.md'; Marker='## D Renderer Challenge Delivery Timeline Review V1'; Text=@'

## D Renderer Challenge Delivery Timeline Review V1 — 2026-10-10

Added a Godot headless in-memory review that joins `CHALLENGE_004` runtime timing, explicit presentation binding, and proposed delivery phase projection. It asserts simulation invariance and deliberately leaves per-field visibility ranges, simulation sampling, interpolation and winning-frame mapping unresolved. No renderer/media/authority change. See `D_RENDERER_CHALLENGE_DELIVERY_TIMELINE_REVIEW_CHECKPOINT_V1.md`.
'@ },
    @{ Path='docs/current/d/MASTER_HANDOVER_C11D_CURRENT.md'; Marker='## Challenge Delivery Timeline Review V1'; Text=@'

## Challenge Delivery Timeline Review V1 (2026-10-10)

Run `python .\tools\c11d\d9\test_d_renderer_challenge_delivery_timeline_review.py` and `godot --headless --path . --script res://tools/c11d/d9/review_challenge_delivery_timeline_in_memory.gd`. This produces only an in-memory review summary. Source phase frames are `180/420/180/120` at 60 FPS; proposed `REVIEW_720@30FPS` phase frames are `90/210/90/60`. Do not interpret phase ranges as editorial field windows, do not map `winning_frame`, and do not activate the renderer. The timebase policy is not approved, D4.8 remains blocked, and release authority remains none.
'@ },
    @{ Path='docs/current/d/START_PROMPT_C11D_CURRENT.md'; Marker='## Resume — Challenge Delivery Timeline Review V1'; Text=@'

## Resume — Challenge Delivery Timeline Review V1 (2026-10-10)

Validate `tools/c11d/d9/d_renderer_challenge_delivery_timeline_review.py` and run `godot --headless --path . --script res://tools/c11d/d9/review_challenge_delivery_timeline_in_memory.gd`. The harness joins the actual frozen Challenge timeline to `social_default_v1` presentation and the proposed `REVIEW_720@30FPS` projection, preserving simulation hashes and `winning_frame`. Expected delivery phases are `90>210>90>60` / total 450 frames. Editorial field visibility, sampling/interpolation and winning-frame mapping stay unresolved; the timebase policy stays proposed/unapproved, renderer OFF, media false, D4.8 blocked, release authority none. Run regressions after the Godot harness passes.
'@ }
)
$added=0; $existing=0
foreach ($u in $updates) {
    $p=Join-Path $root $u.Path
    if (-not (Test-Path -LiteralPath $p)) { throw "Missing documentation target: $($u.Path)" }
    $old=[System.IO.File]::ReadAllText($p)
    if ($old.Contains($u.Marker)) { $existing++; continue }
    $new=$old.TrimEnd()+"`r`n`r`n"+$u.Text.Trim()+"`r`n"
    [System.IO.File]::WriteAllText($p,$new,[System.Text.UTF8Encoding]::new($false))
    $added++
}
Write-Output "C11-D Challenge delivery timeline review docs update PASS | added=$added | already_present=$existing | targets=$($updates.Count) | overwrite=FALSE"
