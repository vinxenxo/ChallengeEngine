# C11-E E4A GUI Contract Failure Analysis — V4

**Date:** 2026-11-03  
**Incident:** source audit V3 `BLOCKED` on the legacy GUI contract test's first assertion.  
**Diagnostic:** V4 read-only capture PASS.  
**Disposition:** obsolete test-version literal; historical test remains unchanged; validate a versioned successor.

## Evidence

- Current `main.py` SHA-256: `f0adc54de884d6d812396707cd6ced49038df0f52e4a9bc516a9ca5e6a0ddcd3`.
- Current app constant at line 53: `APP_VERSION = "0.12.0-E3"`.
- Historical test SHA-256: `ce073a39db0af583ea215c66a6c5303230539e8de857505076963a46dddf4139`.
- Its first assertion at line 16 requires `APP_VERSION = "0.11.1"`; V3 traceback stops at that assertion before any subsequent assertion is evaluated.
- Test source later prints `Producer 0.11.1` but contains no independent requirement that application version remain 0.11.1.
- `main.py` provenance field `source_revision=C11D-D9.10-PRODUCER-0.11.1` is a distinct D9.10 source lineage token, not the app's displayed version.
- Git branch `main`, HEAD `dd1a40f4df797c80ebcbfc90f0d40c55b4e186bd`, target main/test files clean.
- C11-C frozen manifest pin PASS: `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.

## Corrective test strategy

Do not edit `main.py` and do not rewrite the historical test in place. Build an ephemeral successor copy under an external audit run directory. Exactly three controlled transformations are permitted: (1) bind `ROOT` to the checkout's `c11c-suite/c11c-producer` folder because the copy executes outside the checkout, (2) change the expected app version literal to `0.12.0-E3`, and (3) update the printed app-version label. Verify each transformation matches exactly once. Compare the transformed source against the original and fail closed if any other content differs. Re-run the entire successor test once under Python 3.13.

A functional assertion failure is a real unresolved contract issue and remains BLOCKED. A PASS validates the full successor GUI contract test; combined with the six already passing V3 tests, this closes the read-only static audit only. It does not prove field-to-pixel consumption, authorize renderer invocation, or close physical Challenge rendering acceptance.

## Immutable boundaries

No edit to original `main.py`, historical `test_producer_gui_contract.py`, frozen C11-C manifest, C11-C generators/mechanics, D3 engine, E1 service, or protected definitions. No GUI, renderer, media, gameplay job, or production dispatch during this test.
