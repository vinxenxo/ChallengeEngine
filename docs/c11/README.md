# C11-C Remaining Visual Loops v1 — Formal Contracts + Prototype Runners

This bundle contains isolated gold-benchmark prototypes and the formal visual contracts for Sacred Symmetry, Living Particles and Invisible Forces.

## Individual prototype commands

```powershell
.\tools\prototypes\c11c_sacred_symmetry_v1\run_prototype.ps1
.\tools\prototypes\c11c_living_particles_v1\run_prototype.ps1
.\tools\prototypes\c11c_invisible_forces_v1\run_prototype.ps1
```

## Remaining-three test command

```powershell
.\tools\prototypes\c11c_bulk\run_remaining_visual_loops.ps1
```

## All-five visual loop test command

Requires the already validated Geometric Waves and Fractal Bloom prototype folders to be present in the project.

```powershell
.\tools\prototypes\c11c_bulk\run_all_c11c_visual_loops.ps1
```

The five-family runner executes, in order: Geometric Waves, Fractal Bloom, Sacred Symmetry, Living Particles and Invisible Forces.

The bulk launchers are PowerShell-ASCII-safe in their control/error strings and resolve the project root from the c11c_bulk folder correctly. C11-C art remains presentation-only; C7, RNG architecture, SimulationResult and frozen engine boundaries are not reopened by these prototypes.
