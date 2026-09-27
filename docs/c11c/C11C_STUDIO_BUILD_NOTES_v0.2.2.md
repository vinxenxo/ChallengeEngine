# C11-C Studio v0.2.2 — Build Notes

## Critical fix

Fixed the bootstrap/runtime mismatch where `services/seed_manager.py` imported `SeedRecord` but `domain/seed.py` did not export it. `SeedRecord` is now an explicit domain model.

## Additional hardening

- Removed the unused/broken seed-model import path.
- Added seed validation and uniqueness validation to the domain model.
- Manual Review and Production seed entry now validates count, uniqueness and backend seed range.
- Production grammar selector is family-specific instead of showing grammars belonging to other families.
- CommandBuilder no longer invents `-Families` for a canonical Review launcher that does not expose that parameter; it refuses unsupported partial-family review requests instead of executing a different corpus.
- JobManager now marks a process RUNNING only after QProcess reports `started`.
- JobManager drains both output streams before finalizing a job and records cancellation separately from failure.
- Version bumped to 0.2.2.
- Bootstrap packaging excludes Python `__pycache__` artifacts.
- Added a pure-Python self-test covering the seed domain/service and command construction.

## Backend policy

C11-C Studio remains an orchestration/control layer. C11-B, rendering mathematics, RNG ownership, C7 and C9 are not reimplemented by the GUI.
