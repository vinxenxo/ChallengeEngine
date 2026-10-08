# C11-D D7.5 Runner V8

Final runner hardening for the D7.5 acceptance gate.

Changes:
- runs the builder from a temporary directory outside the repository;
- uses `python.exe -B` and `PYTHONDONTWRITEBYTECODE=1`;
- keeps the mutation guard strict: only `artifacts/tests/c11d_d7/d7_5/` may change;
- reports exact added/modified/deleted paths if the mutation guard detects a difference;
- preserves PS 5.1 compatibility and the four-file D7.5 evidence contract;
- preserves deterministic repeated-run SHA validation.

This overlay does not modify the D7.5 builder, C11-C sources, simulation, RNG, or freeze data.
