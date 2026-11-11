# ADDENDUM — E4C OVERLAY INSTALLER V1

The overlay installer uses Windows PowerShell 5.1, strict mode, ASCII-only source, exact SHA-256 source pins and no Git commands. It stages patched Python sources and stdlib-only contract tests under a short `%TEMP%` root, then performs AST parse, Python 3.13/PySide6 probe, py_compile, tests and an immediate pre-transaction recheck before the first repository mutation. It must not call pip or modify requirements/shared dependencies.

Transaction journaling is persisted before every mutation. REPLACE operations back up exact non-empty preimages; rollback is permitted only when the current destination matches the expected postimage and the backup matches the exact preimage. ADD operations are removed only when their current hash matches the package postimage. Unknown or changed states are never overwritten.

---

# C11-E PowerShell Runner Style Guide — V18 (2026-11-11)

## V8 current state — 2026-11-11

V7 failed closed in `STAGED_VALIDATION` before transaction. Its installer imported `QT_VERSION_STR` from `PySide6.QtCore`; the canonical PySide6 runtime does not export that symbol. This is an installer probe defect, not evidence that PySide6, Qt, QImage or QPainter is missing. The preceding imports of `PySide6.__version__` succeeded. `journal=[]`; `rollback=NOT_NEEDED`; no checkout write occurred.

V8 changes the probe to `from PySide6.QtCore import qVersion` and records `qVersion()` as the Qt runtime version. It requires Qt 6.x, alongside Python 3.13.x, existing PySide6 6.8–6.x, non-null RGB888 QImage and active QPainter. The official Qt for Python API lists `qVersion()` as a QtCore function. V8 does not install, upgrade or uninstall packages, invoke pip, edit requirements, or mutate the shared Python environment.

The consumer, its 35 Qt tests and the E1 service replacement are byte-identical to V7. No functional test result is inferred from the failed V7 runtime probe. V8 must still pass Windows PowerShell 5.1 AST, inventory/pins/destinations/staging, runtime probe, `py_compile` 3/3, all 35 Qt tests and immediate pre-transaction checks before any write. Do not repeat accepted A.3, binder V2, Godot V3, Loop22 or historical Drill authoring.

Governance remains unchanged: C11-C frozen manifest SHA `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`; renderer OFF; dispatch/media/audio OFF; `release_authority=NONE`; operator manages commits; Git checks skipped.

### Qt version API rule
For PySide6 runtime reporting, import `qVersion` from `PySide6.QtCore` and call `qVersion()`. Do not import or reference `QT_VERSION_STR`; it is not a guaranteed exported PySide6 binding symbol. Validate returned Qt major version `6`. This probe must remain read-only and must not call pip or mutate shared dependencies.

---


## Current E4C Drill visual-consumer policy — Qt reuse, no dependency additions

- **No new Python dependency** is permitted for the D-owned Drill visual consumer. Reuse only the existing PySide6 dependency declared by the existing Producer; do not add a wheel, package, requirements file, lockfile or environment prerequisite.
- Do not introduce Pillow, PIL, RAQM, FreeType bindings, or another imaging/text dependency for this consumer. Do not run `pip`, `ensurepip`, package managers or dependency installers from the overlay installer, its setup instructions or its tests.
- Do not install, uninstall, upgrade, downgrade or otherwise mutate the shared Python environment as part of this phase. Do not modify either C11-C requirements file.
- Require the canonical explicit `-PythonExe` path and validate Python 3.13.x plus the existing Producer PySide6 `>=6.8,<7`, Qt version, `QGuiApplication`, RGB888 `QImage` creation and active `QPainter`.
- Use `QT_QPA_PLATFORM=offscreen` only as a temporary process-scoped value while launching staged Qt test subprocesses. Preserve and restore the exact prior process value on success and failure; never write user/machine environment settings.
- The Qt backend is a new renderer implementation. Require fresh active-Windows `py_compile` 3/3 and all 35 rewritten Qt tests before any checkout transaction. Pillow-suite results do not transfer.

## Historical dependency guidance — superseded

The earlier V14 generic exact-dependency-pin guidance and the interim V5 Pillow proposal are historical only. They are superseded for the E4C Drill visual consumer by this V16 no-new-dependency policy. Do not apply the former Pillow 12.3.0 / RAQM installation instructions, do not create `requirements-visual-consumer.txt`, and do not treat that abandoned proposal as current authority. The V5 shared-environment installation recommendation was explicitly rejected by the operator.

## PowerShell 5.1 / Unicode

1. `.ps1` source must be ASCII-only. PowerShell 5.1 may decode UTF-8 without BOM through the active ANSI code page.
2. Spanish/editorial strings belong in UTF-8 JSON or Python fixtures, not PS literals.
3. Compare Unicode codepoints and NFC against independent fixtures; reject mojibake (`Ã`) and U+FFFD.
4. GUI/CLI replay derives CLI input from saved GUI UTF-8 evidence; change only provenance/request identity.

## Source authority / add-only installation

- Active checkout only; ZIPs are evidence/read-only. Never overlay snapshots onto checkout.
- Verify SHA-256 pins and frozen C11-C manifest. Never run Git or inspect HEAD/status/branch/.git/commit IDs.
- Preflight all source pins, payload hashes/byte counts and destinations before the first write. Different same-path bytes block the entire install; identical reuse is reported; no silent overwrite.
- D-owned source patch must be narrow, preimage/postimage hash-gated and have a byte-exact backup before atomic replacement. Do not patch protected C11-C source.
- The visual consumer remains an in-memory D-owned component at the existing E1 boundary. It must not activate renderer-native input, dispatch, media/audio production or release.

## Process / receipts

- Use `Start-Process -Wait -PassThru` or an equivalent process API; capture stdout/stderr separately with SHA-256 and propagate nonzero exit codes immediately.
- Receipts record run IDs, source pins, evidence input hashes, output hashes, process exit codes, governance booleans and `release_authority=NONE`.
- Read-only audit runners must not write into source directories except their unique evidence output root; never call Git, generators, Godot, D3 V5, FFmpeg, renderer or media.
- Keep no more than one new GUI/CLI entrypoint pair; both call the same shared helper.

## V12 package self-containment and hash-guarded rollback

A package must carry every newly introduced guide, register, docket or reference that its own installer requires as an ADD operation. The installer must validate the package member SHA and staged postimage; it must not require the new file to exist in the checkout before installation. Document/prompt references must resolve either to the current checkout or to a same-package ADD. The canonical continuity prompt directory is root `prompts/`.

### Hash-guarded rollback

Rollback is allowed only when the installed destination still matches the exact expected postimage. A replacement backup must hash to the exact preimage recorded before mutation before it is restored. If the current destination matches neither the expected postimage nor the expected preimage, refuse to overwrite/delete it and preserve the unknown/operator-modified state. Restore the verified backup atomically and verify the restored destination against the preimage. For ADD rollback, delete only when the current file matches the exact expected postimage. The transaction journal must be written before each mutation. If the journal is empty, report `rollback=NOT_NEEDED`; never imply that a rollback occurred.

V12 also requires static checks that the installer source retains these postimage/preimage/unknown-state guards, not only a textual policy assertion. It continues to require PowerShell 5.1 AST, ASCII-only runner source, validated payload operation rows, short `%TEMP%` staging with a maximum path length of 240 characters, direct Python 3.13 executable probing, separate stdout/stderr, immediate exit-code checks, non-null byte-exact backups, no automatic dependency installation, source SHA pins and frozen C11-C manifest checks.

## V13 complete E1 Drill test staging roots

The E1 Drill consumer suite calls the existing shared production service and D9.9/D9.10 resolver chain. A staged test tree must include the complete pinned source roots required by that chain, not merely the new consumer files. For this gate the stage must copy and path-budget-check `challenges/`, the complete `assets/` tree (including `assets/c6/garage_background.svg`), `docs/current/d/` (including the D1.5 platform layout contract), `docs/current/e/`, `docs/history/c11e/`, `definitions/`, `profiles/`, `release/`, `core/`, `tools/`, and `c11c-suite/c11c-producer/`. Verify required stage-root existence before Python execution. Do not widen repository writes: these are read-only staged test inputs; only the 18 manifest operations may enter the transaction.


## StrictMode variable initialization

Under `Set-StrictMode -Version 2.0`, every variable must be assigned before its first read. For staged-source inspection, load every file into its corresponding variable before checking any of those variables; do not put an unassigned variable in a compound `-or` expression. Validate required source strings are non-empty before inspection. Build-time validation must assert assignment-before-first-use for staged source variables checked statically.
