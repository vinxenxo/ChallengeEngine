# C11-D Renderer Challenge Runtime Output Preview V1 — Checkpoint

**State:** contract prepared; Godot headless runtime result awaits Windows execution evidence. Not approved, not a renderer payload, and not a production artifact.

## Scope
- Exact source: `challenges/CHALLENGE_004.json` (`parking_v2` 2.0, `fam_garage_01`, seed 314159, RNG 2.0).
- Calls the existing frozen `ChallengeRuntimeBridge.run_effective_pipeline` twice with the source dictionary.
- Captures a digest-only in-memory review summary of the actual `SimulationResult`, `VideoTimeline`, editorial fields and `PresentationBindingResult`.
- Keeps `winning_frame` local to GAME as read-only runtime evidence. It does not determine phase lengths, and does not change any simulation state or truth.

## Expected source timing
- 60 FPS; HOOK 180, GAME 420, REVEAL 180, CTA 120 frames; total 900 frames / 15 seconds.
- Simulation result frame count should be 420, corresponding to GAME only.
- `CHALLENGE_004` has hook and CTA copy in source; absent reveal copy resolves to the empty string. No copy is invented.

## Evidence and boundaries
- Two effective runtime invocations must produce the same stable digest.
- Source and frozen C11-C manifest SHA-256 values are pinned in the contract.
- Only digest and summary metadata are printed. No report/payload file, image, video, renderer-native input, renderer dispatch, or production invocation is permitted.
- A runtime result is not a challenge visual payload. Asset paths are bound metadata only; this harness does not load/compose/render them.

## Locks
`renderer=OFF`, `media_created=false`, `D4.8=BLOCKED`, `release_authority=NONE`; C11-C immutable.

## Run on Windows / Godot 4.7.1
```powershell
python -m py_compile .	ools\c11d\d9\d_renderer_challenge_runtime_output_preview.py .	ools\c11d\d9	est_d_renderer_challenge_runtime_output_preview.py
python .	ools\c11d\d9	est_d_renderer_challenge_runtime_output_preview.py
godot --headless --path . --script res://tools/c11d/d9/materialize_challenge_runtime_output_in_memory.gd
```

Expected runtime summary: `materialized=1/1`, `deterministic=2/2`, phases `180>420>180>120`, 900 total frames at 60 FPS, 420 simulation frames, presentation binding PASS, challenge visual payload not materialized.
