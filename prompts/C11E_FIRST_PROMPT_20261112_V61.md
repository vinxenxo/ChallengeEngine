# C11-E FIRST PROMPT V61 — 2026-11-12

The V1.4 locale-safe D adapter is installed and the first real GUI A/V pilot is now accepted. Evidence: `D99-GUI-6514F1066E79-production.zip` SHA `5fb910dd7515ca1f80f2fa77a0829836613e933ca7106f00852ccd31d797f8e4`; `D99-GUI-6514F1066E79-tests.zip` SHA `5c94ad64666548db478a4265a71345efe28c2a346f215e7cdb477f51dc8dde91`; qualification receipt SHA `d8aad7176ed99d8bc0c067cece58272c5ac44045d55d746c768ea72324d459db`. Selector `tracking/tier-1`, gameplay seed 12345, music A/B 840001 and changed C 840002, REVIEW_720. 91/91 pins unchanged at pre-execution, pre-render and post-execution; GUI/CLI E1 semantic parity PASS; 810 D-composed frames, phase counts 90/630/90; FAMILY_MUSIC_V4 A/B identical, C distinct; final H.264 A/C identical, AAC A/C changed; FFprobe 27s, 720x1280 30fps, H.264 High yuv420p TV, AAC-LC 48k stereo. Operator visual/audio review PASS. The accepted GUI run is matrix row 1/20.

The previous locale-decimal issue is closed. Do NOT create another adapter patch or repeat GUI A/V. Install the add-only V1.5 overlay, run the new CLI smoke runner with the successful GUI request as baseline and a fresh request ID; it invokes the existing CLI facade with `--origin CLI --execute-drill-av` and the same D executor. After CLI smoke PASS and human review, run only the remaining 19 selectors in the 4-family × 5-tier A/V matrix, then close E4C.

C11-C remains sole production authority; E1 remains PREPARE_ONLY / NOT_CONNECTED_E1; no Git, no pip, no C11-C source mutation, no production dispatch; release NONE. Continue E5 → E6 Smoke18 → E7 Matrix101 (99 provisional; CH_008/009 held) → E8 historical C-to-E regression, independent acceptance, freeze and separately authorized promotion.


Continue the active ChallengeEngine C11-E project from the installed Windows checkout. Latest package V1.3 installed successfully and passed its transactional preflight, 13/13 tests and 6/6 py_compile. The first `tracking/tier-1` GUI A/V attempt failed before C11-C capture due locale-sensitive speed multiplier transport: expected 0.75, adapter passed comma decimal and PowerShell saw 75000. `Resolver + Plan`, E1, GUI/CLI parity and D composition plan passed. The tests ZIP contains prep/contract artifacts, not a separate A/V failure. See `docs/history/c11e/C11E_E4C_DRILL_LOCALE_DECIMAL_ARGUMENT_FAILURE_20261112_V1.md`.

Your task: install the V1.4 locale-safe patch, which replaces only the D execution adapter and its test module. Its invariant wrapper parses ASCII `0.75000` with `InvariantCulture`, then passes a typed `[double]` to the unchanged C11-C launcher. Before transaction, installer must force `es-ES` and verify the dummy launcher's captured value is exactly 0.75, plus PS 5.1 AST, source pins, 16/16 tests, py_compile 7/7 and hash-guarded transaction checks.

Keep D99 failure artifacts. Retry with a fresh request ID. Complete single-selector GUI A/V `tracking/tier-1` with gameplay seed 12345, music A/B 840001 and C 840002; review the full receipt/media/audio and require operator visual and listening acceptance. Then CLI smoke; only then the 20-selector A/V matrix and E4C closeout. E1 stays PREPARE_ONLY, family_adapter NOT_CONNECTED_E1; C11-C stays sole production authority; release NONE. No Git, no pip, operator manages commits.

---

# C11-E FIRST PROMPT V55 — 2026-11-11

The previous V1 installer failed before transaction because its inline `python.exe -c` probe was altered by Windows PowerShell 5.1 quoting. Do not rerun V1. Use the complete V1.1 ZIP; the corrected installer invokes temporary `.py` probe files by path and emits a `%TEMP%` failure diagnostic. No checkout mutation occurred in the failed V1 attempt.


The next authorized task is to install and validate the single-selector E4C shared A/V execution overlay, not to promote production. First verify the package ZIP SHA-256 and sidecar. Use the bundled PowerShell 5.1 installer with the active checkout and existing canonical Python 3.13 executable. Never extract the overlay over the active checkout. Do not run Git; commits are operator-managed.

Installer requirements: seven operator-accepted source pins and additional direct dependency pins; two exact preimages (`main.py` and existing E1 CLI facade); add-only destination checks; complete ZIP inventory; PowerShell 5.1 AST; Python 3.13/PySide6 runtime; staged py_compile and tests; immediate source/destination rechecks; durable journal before writes; exact backups, atomic mutation and hash-guarded rollback. Stop at first failure and preserve the receipt. No pip or package changes.

After installation, inspect every postimage and launch the existing Producer. E1 remains PREPARE_ONLY and `family_adapter.status=NOT_CONNECTED_E1`. GUI and CLI must call the one D-owned executor; CLI remains plan-only unless `--execute-drill-av --origin CLI` is specified. Reject empty editorial.

Run one `tracking/tier-1` A/V case first: gameplay seed 12345, music A/B 840001, changed C 840002, REVIEW_720, audio/personalization ON and a visible editorial title/subtitle/CTA. C11-C source capture must be silent, FAMILY_MUSIC_V4 uses only music seed, A/B same, C changed, final video stream A/C same, audio stream A/C different. Human visual/listening review is mandatory. Only then consider 20 A/V cases. E4C closes only after all required acceptance gates; C11-C is sole production authority and release NONE.


## Current installer handoff — V1.2 (2026-11-11)

V1 and V1.1 installer attempts failed closed before transaction; neither changed the active checkout. V1.1 passed source pins, destination preflight, Python/PySide6/Qt probes, and `py_compile 6/6`, but PowerShell 5.1 treated unittest's ordinary stderr progress (`... ok`) as a terminating NativeCommandError due `$ErrorActionPreference='Stop'` and `2>&1`. Its diagnostic shows `stage=STAGED_UNIT_TESTS`, `journal=[]`, `rollback=NOT_NEEDED`. The V1.2 installer must be used. It captures stdout and stderr using .NET ProcessStartInfo and evaluates the process exit code; it does not suppress or weaken tests. Verify V1.2 ZIP SHA, then run the complete extracted-package installer in Windows PowerShell 5.1. Require `STAGED_TESTS=13/13`, `PY_COMPILE=6/6`, immediate rechecks and the full install receipt. Do not repeat accepted Binder, native source capture, or 100/100 visual pixel qualification. Only after install PASS inspect all 22 postimages, then run GUI/CLI smoke and one A/V pilot for tracking/tier-1. E1 stays PREPARE_ONLY / NOT_CONNECTED_E1; no Git checks; commits operator-managed; C11-C sole production authority; release NONE.


## V1.3 installer handoff — 2026-11-11

V1.2 must not be rerun. It failed at OP-001 because `File.Replace` was called with a null backup path; the Windows diagnostic confirms rollback completed and the destination remained at exact preimage. V1.3 corrects both forward replacement and rollback with unique non-existing backup paths, journals and SHA-256 verifies the displaced images, and performs a disposable same-volume File.Replace round-trip preflight before the repository transaction. V1.3 is not yet installed or Windows-qualified. Do not repeat Binder, 20 native captures or 100/100 pixel qualification. After installer PASS, inspect all 22 postimages and receipt, then GUI/CLI smoke and only one `tracking/tier-1` A/V pilot. E1 remains PREPARE_ONLY; C11-C remains production authority; renderer/dispatch/release promotion remain blocked; Git checks skipped; commits operator-managed.


## Immediate continuation (V1.5 → V1.6)
GUI `tracking/tier-1` A/V has already passed operator visual/audio review and counts as matrix row 1/20. Do not rerun it. V1.5 CLI smoke overlay failed before transaction in staged Python tests with `PYTHON_TIMEOUT: ;`, journal empty. Root-cause assessment: PowerShell installer used `$Args` as a function parameter and positional array binding; V1.6 fixes with `$PythonArguments`, named calls, nonempty guards, closed stdin and command diagnostics. Install V1.6, then execute `tools/c11d/d9/RUN_C11E_E4C_DRILL_CLI_SMOKE_V1.ps1` once with a fresh request ID. CLI smoke + remaining 19 A/V selector matrix remain before E4C closure. Keep E1 PREPARE_ONLY / NOT_CONNECTED_E1, C11-C production authority, no Git, no pip, no dispatch, release NONE.
