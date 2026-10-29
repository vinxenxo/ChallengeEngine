# C11-D Profile Identity Separation — Godot typing fix V1

## Purpose

Fixes the Godot 4.7.1 GDScript parse error in the profile identity-separation harness by giving `frames_unchanged` an explicit `bool` type and casting the dynamic frame-array size to `int`.

## ZIP scope

This is a minimal overlay. It replaces only:

`tools/c11d/d9/rebind_challenge_presentation_profile_in_memory.gd`

It does not change C11-C, the profile identity contract, schemas, Python validator, documentation, renderer gates or authorization state.

## Apply

Extract this ZIP into the existing `ChallengeEngineV01_STATELESS` repository root.

## Verify and run

```powershell
Select-String -Path .\tools\c11d\d9\rebind_challenge_presentation_profile_in_memory.gd -Pattern 'var frames_unchanged: bool'
godot --headless --path . --script res://tools/c11d/d9/rebind_challenge_presentation_profile_in_memory.gd
```

Do **not** run `append_profile_identity_separation_doc_updates.ps1` until the Godot harness completes with `PASS`. If it reports another parse/runtime error, capture the complete output before making further changes.

Expected guardrails remain unchanged: in-memory review only, no report file, no renderer input/dispatch/activation, no media, `D4.8=BLOCKED`, and `release_authority=NONE`.
