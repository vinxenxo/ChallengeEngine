# MASTER HANDOVER — C11-C / ART DIRECTION 2.0 — v2.1.4

## State
C11-B is CLOSED / CERTIFIED / FROZEN. C11-C is presentation/art-direction only.

## Five families
1. Geometric Waves
2. Fractal Bloom
3. Sacred Symmetry
4. Living Particles
5. Invisible Forces

## Social delivery baseline
- 720x1280 / 9:16
- 30 FPS
- 540 frames
- 18.00 s baseline for the current review corpus
- Audio ON by default; `-NoSound` / `-Silent` disables audio
- Exactly one final MP4 per successful run
- Social metadata sidecar generated per run

## Real-world feedback incorporated
- 540x960 was unsuitable for Facebook/mobile presentation; C11-C capture is 720x1280.
- Palette treatment is more vivid for mobile viewing.
- Ambient audio is restrained to reduce perceived speaker resonance/coupling.
- Header/footer decorative rules are present and palette-derived.
- Footer does not repeat `VISUAL LOOP // FAMILY`.

## Toolchain invariants
- Family renderers do not clean artifacts.
- Review generation does not perform general cleanup.
- `-ResetReviewAssets` affects only `artifacts\\prototypes\\c11c_review_assets`.
- Production lives under `artifacts\\production\\audiovisual` and is protected from review cleanup.
- No nested `powershell.exe -File` is used for orchestration.
- Seed arrays/switches are passed between PowerShell scripts through typed hashtable splatting.
- Godot receives `--resolution 720x1280` as a single CLI argument.
- `project.godot` is not modified.

## Canonical commands
```powershell
.\tools\prototypes\c11c_bulk\validate_c11c_preflight.ps1
.\tools\prototypes\c11c_bulk\run_c11c_art_direction_review.ps1 -ResetReviewAssets
.\tools\prototypes\c11c_bulk\run_c11c_production.ps1 -Family <family> -Seed <seed>
```

## Immediate objective
Generate a clean 25-video corpus: five seeds × five families. Then perform Art Direction 2.0 from actual renders.

Evaluate identity, motion grammar, palette intensity on mobile, typography hierarchy, decorative lines, editorial transition, visual density, seed diversity, loop closure, and audio comfort.

## Explicitly deferred
Do not introduce seed-dependent duration classes yet. Short/medium/long loop duration is a future independent contract.
