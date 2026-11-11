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
