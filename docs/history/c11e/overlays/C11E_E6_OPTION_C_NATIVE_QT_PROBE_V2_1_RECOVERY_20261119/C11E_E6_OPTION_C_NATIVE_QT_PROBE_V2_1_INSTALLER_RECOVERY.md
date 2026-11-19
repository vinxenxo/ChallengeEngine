# C11-E E6 Option C Native Qt Probe V2.1 — Installer recovery correction

**Date:** 2026-11-19  
**Purpose:** correct the V2 installer receipt-path failure without changing the QImage implementation, A3 adjudicator, existing D9/E1 service, or C11-C.

## Incident

The V2 installer passed its PowerShell 5.1 AST check, frozen C11-C and D4.8 pins, all 17 ZIP member checks, and the full add-only collision preflight (`ADD=15; SKIP_IDENTICAL=0`). It then failed while creating a temporary installation receipt file under a long checkout-relative path ending in a 32-character GUID suffix. The Python runner was consequently absent because the installer transaction did not complete.

The installer catch path owns a list of successfully moved destination postimages and removes only those exact SHA-256-matching additions. Existing identical files are not included in that list and are never removed. The operator's failure output contained no rollback warning, consistent with the owned additions being rolled back. Empty directory scaffolding may remain; that is harmless and is not treated as an installed file.

## Root cause and correction

For the operator's exact checkout and failed run ID, the receipt directory path measured 180 characters, the final receipt path 237 characters, and the actual `.partial.<32-hex-guid>` path passed to `FileStream` measured 278 characters. The 278-character temporary path exceeded the legacy path budget of the Windows PowerShell 5.1 / .NET Framework file API, producing the reported `DirectoryNotFoundException`. The earlier preflight had passed because it did not bound the *temporary receipt filename*. The source/package and payload pins were sound.

V2.1 moves the installation receipt to a short path:

`artifacts/tests/c11e/e6_qt_install/<short-run-id>/r.json`

It uses fixed short temporary names inside that unique directory, creates and verifies the receipt directory **before the first destination write**, and checks that every planned receipt/sidecar/temp path is at most 220 characters. Thus path-length failure occurs before payload writes rather than after them. Receipt and sidecar use `CreateNew`, flush-to-disk and non-overwriting `File.Move`.

## Recovery / idempotency

The original V2 payload destinations and hashes are preserved. The V2.1 recovery installer re-runs the full ZIP/member/source/destination preflight. For the original 15 destinations plus the single new V2.1 recovery-document destination, it accepts only:

- absent → `ADD` (write to unique `.partial`, verify size/hash, no-overwrite move);
- exact expected length and SHA-256 → `SKIP_IDENTICAL` (verify; do not write);
- anything else → fail closed before the first destination write.

After install, it verifies every postimage and verifies both receipt and sidecar. On a post-write exception it removes only exact postimages created by that invocation, verifies they are absent, and reports `ROLLBACK_STATUS=PASS` or `INCOMPLETE`. It never deletes an unexpected or modified destination.

The new V2.1 documentation file is add-only. No installer operation uses Git or invokes Godot, FFmpeg, FFprobe, audio generation, mux or production dispatch.

## Run boundary

1. Use only the V2.1 recovery ZIP and its SHA sidecar. Do not rerun the original V2 installer.
2. Keep the package outside the checkout and use the new `INSTALL_C11E_E6_OPTION_C_NATIVE_QT_PROBE_V2_1_RECOVERY.ps1` from that ZIP.
3. Require `POWERSHELL_5_1_AST_PARSE=PASS`, frozen pins PASS, package members PASS, receipt path budget PASS, complete destination preflight and `INSTALL_STATUS=PASS_ADD_ONLY`.
4. The install receipt is under the short path `artifacts/tests/c11e/e6_qt_install/<ID>/r.json`.
5. Only then run the already-pinned V2 QImage probe runner. Preserve all prior blocked receipts.

## Acceptance status

This is an installer recovery correction only. It is not proof that the 37 Qt runtime tests or QImage benchmark passed. It does not authorize a real source frame, D renderer, Godot, FFmpeg/FFprobe, audio, mux, BatchId, or E6 acceptance. C11-C 2.19.12 and D4.8 V2 remain unchanged; renderer/dispatch/media OFF; `release_authority=NONE`.
