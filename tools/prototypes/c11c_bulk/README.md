# C11-C Visual Loop Prototype Bulk

This directory contains presentation-only runners.

## Single-family runners

- `..\c11c_geometric_waves_v1\run_prototype.ps1`
- `..\c11c_fractal_bloom_v1\run_prototype.ps1`
- `..\c11c_sacred_symmetry_v1\run_prototype.ps1`
- `..\c11c_living_particles_v1\run_prototype.ps1`
- `..\c11c_invisible_forces_v1\run_prototype.ps1`

## Group runners

- `run_remaining_visual_loops.ps1` — C11-C.3 through C11-C.5
- `run_all_c11c_visual_loops.ps1` — all five families

All runners expect the repository root as their working tree and preserve the frozen engine boundaries.


## Multi-seed bulk

`run_c11c_multiseed_bulk.ps1` renders all five families for a deterministic seed matrix.
Default: `314159`, `271828`, `161803`, `112358` = 20 renders.

Example custom matrix:

```powershell
.\tools\prototypes\c11c_bulk\run_c11c_multiseed_bulk.ps1 -Seeds 314159,271828,161803,577215,424242
```

Every family launcher accepts `-Seed <int>`; the seed is propagated to visual presentation and prototype audio.


## Seed variation policy
The multiseed stage is no longer a filename-only test. Each family receives a restrained, deterministic parameter envelope from `C11C_SEED`: geometry/frequency for Geometric Waves; Julia/zoom treatment for Fractal Bloom; symmetry order/ring/gear ratios for Sacred Symmetry; attractor positions/flow envelope for Living Particles; and field orientation/pulse envelope for Invisible Forces. Same family + same seed remains reproducible.


## Artifact naming integrity
Every launcher uses expandable seed-specific output paths (for example `*_seed_271828.mp4`). Literal `$Seed` filenames are treated as legacy artifacts from the pre-fix runner and are never reused by the current bulk matrix.


## Seed-driven variation
The multiseed stage is a deterministic variation test, not just a filename test. Geometric Waves varies polygon/frequency/morph envelope; Fractal Bloom varies zoom/warp/bloom envelope; Sacred Symmetry varies radial order/ring bias/gear relations; Living Particles varies attractor positions/flow envelope; Invisible Forces varies field orientation/storm/pulse envelope. Same family + same seed remains reproducible.

## Deterministic geek text

Prototype Footer includes family-specific deterministic technobabble generated from family + seed.
Use `-NoFooter` on individual prototype launchers to render without Footer for future production-style previews.

## Seed diversity policy

The current four-seed matrix is a qualification matrix, not the final production diversity envelope. Production bulk will widen family-specific parameters while remaining bounded by each family's art contract.

## 1.3.1 Godot parse hotfix

Godot 4.7.1 requires explicit typing for several values originating from untyped Arrays/Dictionaries in the deterministic technobabble utility. The 1.3.1 package contains that hotfix and does not alter the visual formulas or frozen engine boundaries.
