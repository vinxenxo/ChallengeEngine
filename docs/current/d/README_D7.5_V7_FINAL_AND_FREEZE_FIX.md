# C11-D D7.5 V7 — Final Authority/Governance Fix + Freeze Finalizer Fix

This overlay is intended to be applied on top of the existing D7.5 V5/V4 tree.

Fixes included:

1. D7.1/D7.2/D7.3/D7.4 authority validation reads canonical authorities from `canonical_authorities` with compatibility fallback, matching the real receipts.
2. D7.3 cross-domain governance is validated from the canonical D7.3 specification plus per-item governance. The canonical catalog does not need a duplicated root `cross_domain_seed_sharing` field.
3. C11-C `build_factory.py` remains at repository root and is checked against the frozen SHA-256.
4. No production/runtime activation is inferred; D4.8 remains BLOCKED.
5. The existing D7.5 runner/mutation guard remains the authority for filesystem mutation: only `artifacts/tests/c11d_d7/d7_5/` may change during acceptance.
6. `finalize_d7_freeze.ps1` now uses an explicit freeze-handover marker variable instead of an undefined PowerShell variable.

The freeze finalizer is intended to run only after D7.5 reports PASS/CLOSED twice.
