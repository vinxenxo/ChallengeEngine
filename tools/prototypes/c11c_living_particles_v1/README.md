# C11-C.4_LIVING_PARTICLES_V1

This is an isolated C11-C art-direction prototype for the `particle_flow` Visual Loop family.

## Visual brief
**Living Particles** — magnetic dust fluid ink.

deterministic particle positions + analytic attractor/vortex field + segment trails + soft-depth glow.

## Physical review
Run from the repository root:

```powershell
.\tools\prototypes\c11c_living_particles_v1\run_prototype.ps1
```

The launcher renders 540x960, 30 FPS, 300 frames, 10.0 seconds, generates deterministic stereo 44.1 kHz WAV, muxes audio into MP4, creates a GIF review surface and validates the final MP4 with FFprobe.

## Boundaries
This prototype does not touch `core/`, simulation math, RNG architecture, `SimulationResult`, C7, C9 or C11-B geometry.
