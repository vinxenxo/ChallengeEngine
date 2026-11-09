# E4B Loop22 — V3 Install-Receipt False Negative / Corrective V4 Handoff V2

**Date:** 2026-11-09. **Disposition:** root cause confirmed; V4 wrapper packaged for Windows validation; no media launch occurred in V3.

## Operator-observed result

The shared-directory V1 installer completed:

- `INSTALL_STATUS=PASS_ADD_ONLY_INSTALL`
- `SOURCE_PINS_VERIFIED=37`
- `PAYLOAD_FILES=13`
- `ADDED_FILES=13`
- package manifest SHA-256 `fe6b9d8dc642ba177909cc2778abccd544ed6a275461b96660cb6af84553568c`
- install receipt SHA-256 `1fc8ecfee3ea34ba9c0853aea627808153372c7ad678e385f2e3f603d9835fd7`

The subsequent V3 wrapper stopped at its line 146 with `Shared-directory fix install receipt is not an accepted 13-file / 37-pin add-only install`.

## Exact root cause

The installer wrote the canonical frozen C11-C manifest SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953` (64 hexadecimal characters). V3 wrapper line 126 used the same correct value for the live frozen manifest check. However, its second, duplicated comparison in line 146 accidentally omitted one `5`, expecting `e405d08e4d166b1ad9595358f4a088e73eea9527e6e89244beb4096eac4b953` (63 characters). The install receipt therefore failed a comparison against a malformed expected literal, despite successful installation and the correct frozen manifest.

The failure was before the process bridge, AST, focused tests and media runner. Therefore the V3 invocation establishes zero new tests run by V3 and zero launcher/music/FFmpeg/FFprobe/media invocations. It does not invalidate the independent 25/25 Python regression already run against the V2 runner in an isolated Python 3.13.5 fixture.

## V4 correction

V4 declares the frozen C11-C SHA exactly once and uses that constant for every comparison and receipt. It pins the exact operator shared-directory V1 install receipt `1fc8ecfee3ea34ba9c0853aea627808153372c7ad678e385f2e3f603d9835fd7` and exact package manifest `fe6b9d8dc642ba177909cc2778abccd544ed6a275461b96660cb6af84553568c`, validates the sidecar, then checks schema, status, 13 payloads, 13 additions, 37 source pins, V1/V2 predecessor manifests, V2 receipt SHA, governance fields and `added_files` cardinality independently. A failure now names the mismatching field rather than returning an opaque compound-condition message.

V4 keeps runner V2/test V2/support V1 and the corrected shared-directory algorithm unchanged. It retains .NET concurrent stdout/stderr capture, exit-code 0/23 bridge regression, PowerShell/Python AST, exactly 25 focused tests and fail-closed media prelaunch. Output evidence uses a new `e4b_loop22_av_ps_bridge_v4` directory; V3 evidence/code remains immutable.

## Required operator sequence

1. Install `C11E_E4B_LOOP22_AV_RECEIPT_PIN_FIX_V2_20261109.zip` from a new Downloads folder, add-only.
2. Require 37/37 source pins, 13/13 previous overlay postimages and 11/11 new payload additions.
3. Run only `RUN_C11E_E4B_LOOP22_AV_QUALIFICATION_V4.ps1` from the active checkout.
4. Require bridge PASS, both AST PASS markers, 25/25 tests and `LOOP22_MEDIA_PRELAUNCH=PASS_ALL_PRELAUNCH_GATES` before the first media process.
5. Preserve every log, preflight receipt, runner report, process receipt and evidence ZIP.

C11-C remains frozen. No Git checks; commits operator-managed. Renderer OFF; D4.8 BLOCKED; D9.10 PREPARE_ONLY; D9.14/D9.16 BLOCKED; D9.17 BLOCKED_NO_GO; D10 BLOCKED_FOR_PROMOTION; release authority NONE.
