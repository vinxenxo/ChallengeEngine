# D6.4 Runner Repair V3

Fixes the D6.4 integration gate so it consumes the final closed D3.3 receipt instead of requiring the intermediate D3.1 receipt to be PASS/CLOSED.

Modified files:
- tools/c11d/d6/seed_request_plan_integrator.py
- tools/c11d/d6/run_d6_4_seed_request_plan_integrator.ps1
- docs/current/d/D6.4_REQUEST_PLAN_PROVENANCE_INTEGRATION_CONTRACT.md

The runner remains evidence-only and writes D6.4 evidence under:
`artifacts/tests/c11d_d6/d6_4/`

It does not write `release/`.
