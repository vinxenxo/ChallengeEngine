# C11-C Visual Loop subtype + music coverage

## Current coverage

The production review corpus contains 27 explicit visual grammars:

- geometric: harmonic_membrane, interference_plane, parametric_ribbon, lattice_wave, orbital_wave
- fractal: radial_bloom, dendritic_tunnel, spiral_fractal, fractal_filigree, nested_worlds
- sacred_symmetry: astrolabe, gear_train, polygon_orrery, origami_mandala, celestial_chart
- living_particles: swarm, vortex, collision_cloud, organic_pulse, magnetic_filament_cloud
- invisible_forces: dipole_field, vortex_field, saddle_field, quadrupole_field, gravitational_lens, topographic_basin, scalar_potential

The coverage launcher forces the technical grammar with `-Grammar`, validates `grammar_id`, validates a FAMILY_MUSIC_V4 audio stream and rejects duplicate WAV hashes inside each family.

Command:

```powershell
.\tools\prototypes\c11c_bulk\run_c11c_visual_loops_subtype_music_coverage.ps1 -ResetReviewAssets
```
