# C11 Freeze Consolidation v2

Repairs the concrete post-C11-B.1 regressions and adds deterministic infrastructure for the final freeze.

## Main changes

- VisualContentPlayer compatibility for legacy direct-script instantiation.
- Physical smoke tests moved to canonical `artifacts/qa/physical_smoke/c10c_e2e` and executed only after physical generation.
- Current C6F2 productive metadata assertions repaired.
- C6F3 pilot asset-family oracle repaired to `fam_pilot_01`.
- C9E/C9F productive tests now have repository-local default outputs while preserving `--output-config=` overrides.
- C11 repository contract now validates the canonical artifact tree and consolidation tools.
- Deterministic 288-run stress runner: 9 challenges × 32 fixed seeds.
- QA challenge video matrix uses test-only copies and descriptive Hook/CTA text.

## Validation

Run the logical corpus with `python tests/run_all.py`.
Run physical validation with `tools/c11freeze/run_physical_export_suite.ps1`.
Run the complete freeze gate with `tools/c11freeze/run_all.ps1`.
Run stress smoke with `python tools/c11freeze/run_seed_stress.py --limit 3` and full stress with no limit.

## v3 hardening

- UnifiedSocialFrame path no longer creates an unattached SafeAreaLayout.
- C11-B.1 contract test completes node cleanup before exit.
- Retrocompatibility is a real 54-run telemetry comparison against C11-A.1, not merely a current validate-only smoke test.
- Seed stress is fixed-seed and repeated twice by default.
- `tools/c11freeze/run_all.ps1` is the single complete freeze gate.


## v4 fixes

- Explicit GDScript typing in `VisualContentPlayer.gd` and the physical export consumer tests, eliminating Variant inference warnings treated as errors.
- C6F2 adapter metadata regression test aligned with the current declared Pilot/Hit/Catch/Find/Choose/Count metadata.
- QA video matrix generator now assigns a unique test-only `challenge_id` per challenge/seed, satisfying batch coverage without changing mechanic or simulation math.
- `--include-canonical` generates exactly the six frozen C11-A.1 seeds; stress mode remains controlled by `--limit`.
- Physical export runner is ASCII-safe and prints the actual Godot test output on failure.
