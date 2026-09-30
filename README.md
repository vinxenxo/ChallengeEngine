# C11-C 2.19.12 — V38 Pre-freeze maintenance correction

Minimal maintenance-only correction.

The V36 Maintenance repair note was accidentally left under `docs/current/c11c/`, so the freeze correctly rejected the tree as stale.

V38 explicitly archives `C11-C_2.19.12_PREFREEZE_MAINTENANCE_FIX_V36.md` through the existing documentation consolidator. No runtime, renderer, mechanics, simulation, RNG, definitions, profiles or product tests are changed.

After applying V38, run the documentation consolidator and then the freeze dry-run. Do not rerun the 52-video corpus solely for this documentation move.
