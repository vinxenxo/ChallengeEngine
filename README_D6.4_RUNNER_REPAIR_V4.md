# C11-D D6.4 Runner Repair V4

Fixes the D6.4 runner snapshot invocation and ensures the evidence directory exists before execution.

Changes:
- `--root $Root` is now passed to `seed_request_plan_integrator.py` for `--snapshot-only`.
- `artifacts/tests/c11d_d6/d6_4` is created explicitly before the mutation baseline.

No Python integrator logic, D3/D4/D5/D6.1-D6.3 sources, Producer, renderer, simulation, or C11-C files are modified.

Expected evidence remains:
- artifacts/tests/c11d_d6/d6_4/d6_4_integration_matrix.json
- artifacts/tests/c11d_d6/d6_4/d6_4_provenance_matrix.json
- artifacts/tests/c11d_d6/d6_4/d6_4_negative_tests.json
- artifacts/tests/c11d_d6/d6_4/d6_4_integration_receipt.json

`release/` is intentionally not written by D6.4.
