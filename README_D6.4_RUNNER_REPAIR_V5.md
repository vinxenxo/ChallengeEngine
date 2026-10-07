# C11-D D6.4 Runner Repair V5

Purpose: fix the runtime NameError in the D6.4 integrator after the D3 closure gate was migrated from D3.1 to D3.3.

Fixes:
- injects the resolved D3.3 closed-receipt path into build_integration();
- keeps D3.3 as the D6.4 D3 closure gate;
- validates D3 receipt result/status as PASS/CLOSED;
- preserves the V4 PowerShell runner fix (`--root` and output directory creation).

No production activation, no renderer execution, no changes to D4/D5/D6.1-D6.3 authorities.

Evidence remains under `artifacts/tests/c11d_d6/d6_4/`; no writes to `release/`.
