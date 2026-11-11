# C11-E NEXT WINDOW START PROMPT V131 — 2026-11-11

The previous V1 installer failed before transaction because its inline `python.exe -c` probe was altered by Windows PowerShell 5.1 quoting. Do not rerun V1. Use the complete V1.1 ZIP; the corrected installer invokes temporary `.py` probe files by path and emits a `%TEMP%` failure diagnostic. No checkout mutation occurred in the failed V1 attempt.


Continue from overlay `C11E_E4C_DRILL_SHARED_AV_EXECUTION_V1_1` and the latest package manifest. The package is a candidate until installed on active Windows; do not claim PASS or E4C closure from local static tests.

Active checkout: `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`. Do not extract ZIP snapshots over it. Do not run Git. Operator owns commits. Python 3.13, Windows PowerShell 5.1 and existing PySide6 runtime; no pip or shared dependency changes.

C11-C 2.19.12 remains sole production authority and frozen manifest SHA is `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`. E1 remains PREPARE_ONLY and `family_adapter.status=NOT_CONNECTED_E1`. The GUI and CLI route through the one shared D execution module; CLI execution only with `--execute-drill-av --origin CLI`.

First run the self-contained PowerShell 5.1 installer. Verify ZIP sidecar; require package inventory, all source pins, exact replacement preimages, add-only destination states, PS AST, canonical Python 3.13/PySide6 runtime, staged py_compile/tests, and immediate pre-write rechecks. On failure, stop; inspect journal and rollback receipt. No Git or pip.

After install PASS, inspect all postimages, open existing Producer, choose Visual Drill → tracking → tier-1 → PRODUCTION → REVIEW_720 → audio ON → personalization ON, provide at least one actual non-empty title/subtitle/CTA, gameplay seed 12345, music seed 840001. Use Resolver + Plan, then the E4C Drill A/V button. Adapter must run existing C11-C silently (`-NoSound`), D-composite, generate FAMILY_MUSIC_V4 A/B 840001 and C 840002, verify identical A/C video and changed audio stream. Review receipt, visual and listen.

Do not run 20 A/V cases until the single selector is accepted. Do not change E1 service, C11-C, renderer/dispatch/release controls. Release authority NONE.


## Current installer handoff — V1.2 (2026-11-11)

V1 and V1.1 installer attempts failed closed before transaction; neither changed the active checkout. V1.1 passed source pins, destination preflight, Python/PySide6/Qt probes, and `py_compile 6/6`, but PowerShell 5.1 treated unittest's ordinary stderr progress (`... ok`) as a terminating NativeCommandError due `$ErrorActionPreference='Stop'` and `2>&1`. Its diagnostic shows `stage=STAGED_UNIT_TESTS`, `journal=[]`, `rollback=NOT_NEEDED`. The V1.2 installer must be used. It captures stdout and stderr using .NET ProcessStartInfo and evaluates the process exit code; it does not suppress or weaken tests. Verify V1.2 ZIP SHA, then run the complete extracted-package installer in Windows PowerShell 5.1. Require `STAGED_TESTS=13/13`, `PY_COMPILE=6/6`, immediate rechecks and the full install receipt. Do not repeat accepted Binder, native source capture, or 100/100 visual pixel qualification. Only after install PASS inspect all 22 postimages, then run GUI/CLI smoke and one A/V pilot for tracking/tier-1. E1 stays PREPARE_ONLY / NOT_CONNECTED_E1; no Git checks; commits operator-managed; C11-C sole production authority; release NONE.


## V1.3 installer handoff — 2026-11-11

V1.2 must not be rerun. It failed at OP-001 because `File.Replace` was called with a null backup path; the Windows diagnostic confirms rollback completed and the destination remained at exact preimage. V1.3 corrects both forward replacement and rollback with unique non-existing backup paths, journals and SHA-256 verifies the displaced images, and performs a disposable same-volume File.Replace round-trip preflight before the repository transaction. V1.3 is not yet installed or Windows-qualified. Do not repeat Binder, 20 native captures or 100/100 pixel qualification. After installer PASS, inspect all 22 postimages and receipt, then GUI/CLI smoke and only one `tracking/tier-1` A/V pilot. E1 remains PREPARE_ONLY; C11-C remains production authority; renderer/dispatch/release promotion remain blocked; Git checks skipped; commits operator-managed.
