# C11-D D6.3 mutation guard repair V1

Patch purpose:
- Exclude the entire `artifacts/tests/c11d_d6/d6_3/` evidence tree from the repository mutation snapshot.
- Keep a strict post-run check that the D6.3 output directory contains exactly the four declared evidence JSON files and no subdirectories.

Files replaced:
- tools/c11d/d6/seed_isolation_collision_validator.py
- tools/c11d/d6/run_d6_3_seed_isolation_collision_validator.ps1

No other repository files are included.
