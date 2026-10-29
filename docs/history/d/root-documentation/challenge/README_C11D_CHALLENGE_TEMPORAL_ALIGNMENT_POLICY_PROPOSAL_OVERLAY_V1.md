# C11-D Challenge Temporal Alignment Policy Proposal — Overlay V1

## SHA-256

To be computed for the packaged ZIP after verification.

## Scope

Adds a proposal-only JSON contract/schema, deterministic Python validator and negative tests, plus current and historical checkpoint documentation. No existing runtime files or frozen C11-C files are modified.

## Supported reference case

`CHALLENGE_004`: source timeline 900 frames at 60 FPS, delivery timeline 450 frames at 30 FPS. Source phase boundaries `[0,180,600,780,900]` map to `[0,90,300,390,450]`; source phase sizes `180>420>180>120`, delivery phase sizes `90>210>90>60`. All ranges are zero-based and half-open.

The validator cross-checks the independent delivery-timeline, timebase, editorial-window, runtime-output and sample-selection contracts. The exact winning-frame reference is 574 -> 287; it is never used as the sampling origin. `close_calls` remains count-only. No interpolation, media, persistent evidence, renderer dispatch or renderer-native input is produced.

## Windows verification

```powershell
Get-FileHash "$env:USERPROFILE\Downloads\C11D_CHALLENGE_TEMPORAL_ALIGNMENT_POLICY_PROPOSAL_OVERLAY_V1_FINAL.zip" -Algorithm SHA256
Expand-Archive -LiteralPath "$env:USERPROFILE\Downloads\C11D_CHALLENGE_TEMPORAL_ALIGNMENT_POLICY_PROPOSAL_OVERLAY_V1_FINAL.zip" -DestinationPath "." -Force
python -m py_compile .\tools\c11d\d9\d_renderer_challenge_temporal_alignment_policy.py .\tools\c11d\d9\test_d_renderer_challenge_temporal_alignment_policy.py
python .\tools\c11d\d9\test_d_renderer_challenge_temporal_alignment_policy.py
```

Expected marker: `C11-D RENDERER CHALLENGE TEMPORAL ALIGNMENT POLICY PROPOSAL PASS`.

## Governance

This is a proposal, not authorization. It leaves approval flags false; C11-C immutable; renderer OFF; media false; D4.8 BLOCKED; release authority NONE. It does not close any D9 acceptance/closure gate or enable D10.
