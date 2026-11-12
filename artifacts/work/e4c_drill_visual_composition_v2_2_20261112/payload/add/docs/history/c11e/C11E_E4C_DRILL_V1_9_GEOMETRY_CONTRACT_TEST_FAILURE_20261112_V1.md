# C11-E E4C V1.9 geometry-contract staged-test failure — V1

**Date:** 2026-11-12  
**Disposition:** FAIL_CLOSED_PRE_TRANSACTION_NO_DESTINATION_WRITES  
**Superseding overlay:** V2.0 consolidated geometry-contract correction

## Operator diagnostic

Package SHA `c661ed47d821241bce2969b8b9c74bf1471b991f504c529b6fbdd197ad20aa97`; package inventory 26/26 PASS; source pins 21/21 PASS; frozen C11-C manifest PASS; PowerShell AST 2/2 PASS; operation classification 1 replacement + 23 additions. Python 3.13 py_compile completed for consumer, test and requalifier. The Qt staged test process exited 1 in `setUpClass`; `_verify_decision_and_proposals()` raised `V2 social-region geometry mismatch: canvas`, so `Ran 0 tests`.

## Root cause

The pinned V2 proposal intentionally declares `geometry.canvas` as `{x:0,y:0,width:720,height:1280,aspect_ratio:"9:16"}`. The consumer's expected-region dictionary in `_verify_decision_and_proposals()` omitted `aspect_ratio` and compared dictionaries for exact equality. `validate_plan()` contained the same duplicated four-field expectation and would reject the valid plan after the setup issue was bypassed. The source profile, proposal geometry, body rectangle, and 4/3 projection were not at fault.

The frozen source profile is 540x960 with header/footer ratios 0.15/0.15 and body ratio 0.70. At output scale 720/540 = 1280/960 = 4/3, these regions map to header `(0,0,720,192)`, body `(0,192,720,896)`, and footer `(0,1088,720,192)`. The contract's 9:16 metadata is valid and must be retained in the canvas equality expectation.

## Transaction disposition

Failure occurred at `STAGING_AND_PYTHON_TESTS`, after the installer created its designated evidence directory and failure diagnostic but before `TRANSACTION_INITIALIZE`, journal creation, backup staging or destination mutation. The diagnostic status is `FAIL_CLOSED_PRE_TRANSACTION_NO_DESTINATION_WRITES`; the transaction journal remained empty. The evidence-root diagnostic is an intentional artifact write, not a source or destination operation. No rollback of repository payloads was required.

## V2.0 consolidated correction

- Define one `EXPECTED_SOCIAL_REGIONS` constant, including the exact `aspect_ratio: 9:16` canvas metadata, and use it in both proposal validation and plan validation.
- Validate logical source geometry 540x960, 15%/70%/15% region ratios, and 4/3 output projection to REVIEW_720.
- Add two focused tests: wrong canvas aspect ratio is rejected; logical-to-output mapping is exact. Focused suite is 20/20 expected.
- Preserve the same one existing D consumer replacement and add-only new test path; retain all 21 source pins and frozen manifest checks.
- Do not modify proposal/decision/timebase hashes, C11-C, E1 service, GUI/CLI entrypoints, shared D A/V executor, music path, binder, native media, requalifier or runner.
- V2.0 installer performs staged py_compile 3/3 and 20 Qt tests before transaction, plus PowerShell AST, runtime probe, operation/payload closure, File.Replace round-trip, immediate pre-write rechecks, journal-first mutation, backups and hash-guarded rollback.

## Governance

C11-C 2.19.12 remains sole production authority; frozen manifest SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`. E1 is `PREPARE_ONLY` / `NOT_CONNECTED_E1`; production dispatch false; `release_authority=NONE`. No Git, pip, C11-C source mutation, re-render or audio generation.

## V2.1 authoritative reconciliation (2026-11-12)

`E4C_OPEN_V2_REQUALIFICATION_PENDING`. Geometry V2 and the Test 04 boundary correction are accepted: `validate_plan()` now requires `source_frame_viewport == EXPECTED_SOCIAL_REGIONS["body_rect"]`. Reconciled consumer SHA-256: `e5cf97651e546ad86e2a4d46698553038e4161dc97a55da2654f197ed71f623c` (36,678 bytes); unchanged test SHA-256: `62327e32ed4c15b497efb4a93fecc1d484cebff0b79beaa7ced5099905ffb2bf`; isolated Python 3.13.14 evidence is py_compile PASS and 20/20 PASS.

V1.7 destination preflight, V1.8 operation/package binding, V1.9 geometry contract and V2.0 staging Test 04 failures are closed before transaction; none installed this correction. V2.1 is rebuilt and pending Windows installation, complete receipt and postimage review. Do not install V2.0 and do not repeat GUI, CLI smoke, native capture, music or Binder.

Preserve evidence GUI `D99-GUI-6514F1066E79`, CLI `E4C-CLI-SMOKE-20261112T091253Z-5a2e96b8`, native silent MP4, WAV A/B/C, seeds and bitstreams. V1 composition was visually rejected; `tracking/tier-1` is not yet an accepted V2 matrix row.

Required sequence: documentation; V2.1 installation; receipt/postimage audit; one existing-media requalification; seven-image/three-MP4 review; operator visual/audio acceptance; row 1/20; remaining 19; E4C close; E5, E6 Smoke18, E7 Matrix101, E8. C11-C 2.19.12 only; frozen manifest `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`; E1 `PREPARE_ONLY / NOT_CONNECTED_E1`; no Git, pip, C11-C mutation, dispatch or release; operator-managed commits.
