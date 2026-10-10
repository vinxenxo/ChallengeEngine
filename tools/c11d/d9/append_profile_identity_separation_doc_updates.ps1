$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$updates = @(
    @{ Path='docs/current/d/D_RENDERER_BASELINE_PREPARATION_PLAN_V1.md'; Marker='## Increment — D Renderer Profile Identity Separation V1'; Text=@'

## Increment — D Renderer Profile Identity Separation V1 (2026-10-10)

The profile identity review separates four roles for CHALLENGE_004: legacy `video_profile=test_master_11s` (its named profile is 30 FPS / 11 seconds), canonical inline source timing (60 FPS / 15 seconds / 900 frames), explicit source `presentation.profile=social_default_v1`, and independent delivery `REVIEW_720` (30 FPS / 720×1280). The legacy migration maps the top-level `video_profile` identifier into canonical presentation binding, so the frozen runtime reports `test_master_11s` as presentation profile even though the source also declares `social_default_v1`. D must bind presentation and delivery identity explicitly without modifying C11-C. The new in-memory rebind harness changes only a deep copy's presentation-profile identifier and verifies simulation-frame signature, winning frame, frame count and metrics remain unchanged. No renderer input or media is emitted; delivery timebase projection remains proposed/unapproved and D4.8 remains BLOCKED.
'@ },
    @{ Path='docs/current/d/D9_SUITE_INTEGRATION_CHANGELOG.md'; Marker='## D Renderer Profile Identity Separation V1'; Text=@'

## D Renderer Profile Identity Separation V1 — 2026-10-10

Added a read-only source audit and Godot headless harness distinguishing legacy video profile identity, inline challenge timing, explicit presentation profile and D delivery profile. The D-owned in-memory rebind verifies simulation invariance and keeps renderer/media/authority disabled. See `D_RENDERER_PROFILE_IDENTITY_SEPARATION_CHECKPOINT_V1.md`.
'@ },
    @{ Path='docs/current/d/MASTER_HANDOVER_C11D_CURRENT.md'; Marker='## Profile Identity Separation V1'; Text=@'

## Profile Identity Separation V1 (2026-10-10)

The next validation step is `tools/c11d/d9/rebind_challenge_presentation_profile_in_memory.gd`. It explicitly separates source `social_default_v1` presentation intent from legacy `test_master_11s` binding and `REVIEW_720` delivery. Run the Python contract test and the Godot headless harness; this is not a renderer invocation. Preserve the C11-C frozen manifest and keep the timebase projection unapproved, D4.8 blocked and release authority none.
'@ },
    @{ Path='docs/current/d/START_PROMPT_C11D_CURRENT.md'; Marker='## Resume — Profile Identity Separation V1'; Text=@'

## Resume — Profile Identity Separation V1 (2026-10-10)

Run `python .\tools\c11d\d9\test_d_renderer_profile_identity_separation.py` and `godot --headless --path . --script res://tools/c11d/d9/rebind_challenge_presentation_profile_in_memory.gd`. This increment separates legacy video profile, inline timeline, explicit presentation profile and D delivery profile; it must not modify C11-C or approve 60→30 projection, renderer baseline, D4.8 or release authority. Investigate any Godot error before proceeding.
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
Write-Output "C11-D profile identity separation docs update PASS | added=$added | already_present=$existing | targets=$($updates.Count) | overwrite=FALSE"
