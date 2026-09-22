C11-C Visual Drill Social Presentation v1.0

BASELINE
ChallengeEngineV01_C11-C2.1.4-LATEST-FREEZE.zip
SHA-256: f4ceb95fd506d1ea40e70c0f2102c91e8e29b30acc0d5c0a0b032f69765d1996

SCOPE
Presentation/editorial layer + modern Visual Drill review pipeline + global ambient audio generator.
No simulation/math/RNG/SimulationResult/timeline/C11-B contract changes.

INSTALL
Copy the overlay paths into the repository, preserving relative paths.
No file in the overlay should be copied into artifacts/production.

WINDOWS VALIDATION
1. .\tools\prototypes\c11c_bulk\validate_c11c_powershell.ps1
2. .\tools\prototypes\c11c_bulk\validate_c11c_delivery_configuration.ps1
3. python .\tests\run_all.py

VISUAL DRILL MODERN REVIEW
.\tools\prototypes\c11c_bulk\run_c11c_visual_drill_review.ps1 -ResetReviewAssets

Optional:
-RegenerateEnvelopes   Rebuild the C11-A envelope corpus before rendering.
-NoSound               Render the same visual corpus without the shared ambient audio.

EXPECTED REVIEW
4 families x 5 seeds = 20 renders.
Physical delivery: 720x1280, 9:16, 30 FPS.
Matrix transition: OFF.
Shared social/editorial layout: ON.
Audio: GLOBAL_AMBIENT by default.

NOTE
The legacy C11-A envelopes remain the source of mechanical input for this first modern social review pass.
The four Visual Drill generators/renderers remain the next art/mechanics work item and are intentionally not altered by this overlay.
