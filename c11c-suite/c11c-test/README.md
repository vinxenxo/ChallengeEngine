# c11c — test

Canonical C11-C operator shell exposing GUI/CLI orchestration surfaces.

## Directory contents

### Subdirectories
- None.

### Representative files
- `test_powershell_parse.bat` — operator/maintenance script.
- `test_powershell_parse.py` — Python tooling/test code.
- `main.py` — Python tooling/test code.
- `run.bat` — operator/maintenance script.
- `run_all.bat` — operator/maintenance script.
- `run_c11c_acceptance.bat` — operator/maintenance script.
- `run_c11c_challenge_family_smoke.bat` — operator/maintenance script.
- `run_c11c_challenge_family_smoke.ps1` — operator/maintenance script.
- `run_c11c_challenge_smoke.bat` — operator/maintenance script.
- `run_c11c_challenge_smoke.ps1` — operator/maintenance script.
- `run_c11c_complete_review.bat` — operator/maintenance script.
- `run_c11c_complete_video_review.bat` — operator/maintenance script.
- `run_c11c_family_coverage_smoke.bat` — operator/maintenance script.
- `run_c11c_focused_validation.bat` — operator/maintenance script.
- … 2 additional files.

## Lifecycle / authority

Persistent repository content. Changes should preserve deterministic behavior, provenance and documented ownership.

This README is a navigation aid. The files referenced above remain authoritative according to their own contracts, schemas, tests and handover documents.


## Test 0.2.0 — C11-D D9.12

The Test GUI retains every legacy C11-C route and registers additive D2–D9 validation routes. `BUILD_MANIFEST.json` is the declarative route index; `test_d9_test_integration.py` checks parity between the manifest, `C11_COMMANDS`, route targets, and the five-surface Suite topology.

D routes cover D2 family/asset roles, D3 music determinism, D4 request/personalization and GUI/CLI parity, D4.8 blocked activation governance, D5 provenance/lifecycle, D6 independent seed domains, D7 catalog identity/provenance, D8 visual/audio QA and non-authoritative release dry-run, and D9.8–D9.11 canonical tests. Aggregated D9 negative and GUI/CLI parity commands invoke existing tests; they do not reimplement backend logic.

The `D9 REAL-MEDIA GUI CERTIFICATION PREFLIGHT (NO MEDIA)` route validates the certification checklist only. It does not start Qt production, renderer execution, media creation, release staging, or maintenance mutation. Real-media operator execution remains a future D9.14 gate. `D4.8=BLOCKED`, renderer/media/production flags remain false, and `release_authority=NONE`.
