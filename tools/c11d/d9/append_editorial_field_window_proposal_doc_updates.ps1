$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$updates = @(
  @{ Path = 'docs/current/d/D_RENDERER_BASELINE_PREPARATION_PLAN_V1.md'; Marker = '<!-- C11D_EDITORIAL_FIELD_WINDOW_PROPOSAL_V1 -->'; Heading = '## D9 editorial field-window proposal V1'; Body = 'Added a proposal-only field-to-phase map for CHALLENGE_004: canonical `hook` maps to delivery frames `[0,90)`, empty `reveal` is suppressed, and canonical `cta` maps to `[390,450)`. This is an explicit per-field policy candidate, not an inference that phase ranges always equal text visibility. Visual Loop and Drill field maps remain unresolved. See `D_RENDERER_EDITORIAL_FIELD_WINDOW_PROPOSAL_CHECKPOINT_V1.md`.' },
  @{ Path = 'docs/current/d/MASTER_HANDOVER_C11D_CURRENT.md'; Marker = '<!-- C11D_EDITORIAL_FIELD_WINDOW_PROPOSAL_V1 -->'; Heading = '## Latest increment — editorial field-window proposal'; Body = 'The new in-memory proposal gives CHALLENGE_004 hook/CTA field windows only under explicit policy `C11D_SAME_NAME_EDITORIAL_FIELD_TO_PHASE_FULL_WINDOW_V1`; empty reveal is suppressed. It preserves copy exactly and hashes it. Visual Loop/Drill editorial windows remain unresolved; policy is PROPOSED_NOT_APPROVED and no renderer input or media is produced.' },
  @{ Path = 'docs/current/d/START_PROMPT_C11D_CURRENT.md'; Marker = '<!-- C11D_EDITORIAL_FIELD_WINDOW_PROPOSAL_V1 -->'; Heading = '## Resume — editorial field-window proposal V1'; Body = 'Run the Python contract test and `godot --headless --path . --script res://tools/c11d/d9/review_editorial_field_windows_in_memory.gd`. This proposes `hook=[0,90)`, suppresses empty reveal, and proposes `cta=[390,450)` at REVIEW_720; it does not approve the policy. Do not infer corresponding windows for Loops/Drills or start rendering.' },
  @{ Path = 'docs/current/d/D9_SUITE_INTEGRATION_CHANGELOG.md'; Marker = '<!-- C11D_EDITORIAL_FIELD_WINDOW_PROPOSAL_V1 -->'; Heading = '### D renderer editorial field-window proposal V1'; Body = 'Added a source-pinned, deterministic field-to-phase proposal for CHALLENGE_004, including exact editorial text digests, half-open delivery-frame windows, empty-field suppression, 53 negative cases, and a Godot runtime/invariance harness. No renderer input, media, or authority change.' }
)
# Preflight all targets and duplicate-marker state before writing any file.
foreach ($entry in $updates) {
  $path = Join-Path $root $entry.Path
  if (-not (Test-Path -LiteralPath $path -PathType Leaf)) { throw "Required documentation target missing: $($entry.Path)" }
}
$added = 0; $already = 0
foreach ($entry in $updates) {
  $path = Join-Path $root $entry.Path
  $content = [System.IO.File]::ReadAllText($path)
  if ($content.Contains($entry.Marker)) { $already++; continue }
  $append = "`r`n$($entry.Marker)`r`n$($entry.Heading)`r`n`r`n$($entry.Body)`r`n"
  [System.IO.File]::WriteAllText($path, $content.TrimEnd() + $append, [System.Text.UTF8Encoding]::new($false))
  $added++
}
Write-Output "C11-D editorial field-window proposal docs update PASS | added=$added | already_present=$already | targets=$($updates.Count) | overwrite=FALSE"
