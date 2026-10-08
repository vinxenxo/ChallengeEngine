# C11-D D7.5 V5 + D7 Freeze Pack

V5 fixes the D7.5 governance false-negative path, uses the canonical root `build_factory.py`, normalizes boolean gate values safely, and emits exact governance/full error diagnostics. The D7.5 runner disables Python bytecode generation and its mutation guard excludes only `artifacts/tests/c11d_d7/d7_5/` evidence.

After applying this overlay, run the PS5.1 parse audit and execute the D7.5 runner twice. Only after both executions are PASS/CLOSED, run `finalize_d7_freeze.ps1`. That script rechecks D7.0-D7.5 receipts, invokes the proven D7.5 handover closure, verifies the frozen C11-C build identity, creates D7 freeze evidence, and advances the current handovers to D8.0.

The exact D7.5 frozen Library baseline name is intentionally not invented here; the Library artifact itself is the external baseline identity.

No C11-C engine/runtime/presentation surface is modified or activated. `release/` is never created by this pack.
