# C11-E First Prompt — V2 (2026-11-18)

Continue in `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`; the active checkout is authoritative. Never extract ZIPs over it. Operator commits; do not perform Git/HEAD/status/branch checks. Enforce SHA-256 pins and the frozen C11-C manifest.

Read `docs/master-prompts/C11E_MASTER_HANDOVER_20261118_V2.md` and `docs/current/e/C11E_E6_D9_DEPENDENCY_PIN_RECONCILIATION_20261118_V2.md` first.

The V1 dependency reconciliation audit already passed on the active checkout: 13/13 fixed evidence pins/sidecars, 33/33 accepted source pins, 9/9 route dependencies, 2/2 CH004 observed-current hashes, zero blockers. Do not repeat the V1 test that creates an OS symlink; it is not Windows-privilege portable. V2 uses deterministic `Path.resolve()` substitution for that containment test.

Immediate action: run `APPLY_AND_RUN_C11E_E6_D9_PIN_RECONCILIATION_V2.ps1` from a fresh extracted package folder. It performs add-only installation, V2 focused tests, then the existing read-only V1 audit. Do not check `$LASTEXITCODE` after a PowerShell `.ps1`; only inspect it immediately after native Python processes (the integrated script handles this).

After PASS, continue D9 selector/config route and output-ledger closure in PREPARE_ONLY and CH004 historical A/V lineage adjudication. No media/render/audio/mux until separate E6 TEST_ONLY authorization and explicit D4.8 governance resolution.
