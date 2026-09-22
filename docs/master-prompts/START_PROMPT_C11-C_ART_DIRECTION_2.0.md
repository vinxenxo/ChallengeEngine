# START PROMPT — C11-C ART DIRECTION 2.0 — v2.1.4

Continue `ChallengeEngineV01_STATELESS` from C11-C v2.1.4.

C11-B is CLOSED / CERTIFIED / FROZEN. C11-C is presentation/art-direction only.

Five active families: Geometric Waves, Fractal Bloom, Sacred Symmetry, Living Particles, Invisible Forces.

Current delivery baseline: 720x1280, 9:16, 30 FPS, 540 frames, 18.00 s. Default audio ON; `-NoSound` / `-Silent` disables audio. One final MP4 per run.

Real Facebook/mobile testing already established three delivery requirements: higher resolution, more vivid palette treatment, and non-intrusive ambient audio.

Canonical preflight:
`.\tools\prototypes\c11c_bulk\validate_c11c_preflight.ps1`

Canonical review corpus:
`.\tools\prototypes\c11c_bulk\run_c11c_art_direction_review.ps1 -ResetReviewAssets`

Expected corpus: 5 seeds × 5 families = 25 renders.

Godot capture resolution must remain exactly `--resolution 720x1280` as one argument. Do not modify `project.godot`.

Do not reintroduce versioned launcher proliferation, nested PowerShell invocation, review-time general cleanup, or variable-duration logic.

Use the actual 25 rendered videos/keyframes as the evidence base for Art Direction 2.0.
