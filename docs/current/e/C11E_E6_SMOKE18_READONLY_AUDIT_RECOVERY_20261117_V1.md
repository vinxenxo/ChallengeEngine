# C11-E E6 Smoke18 Read-only Audit Recovery Overlay V2 — 2026-11-17

## Purpose

This is an ADD_ONLY, re-entrant recovery overlay for the failed/partial V1 audit installation. It does not replace, delete or edit V1 files. It re-delivers the exact 14 V1 payloads, adds the 11 baseline documents pinned by the V1 audit but not bundled inside its V1 ZIP, and installs a separate V2 audit module/runner/tests.

## Installer semantics

- Validate the package manifest, all payload SHA-256 values and byte counts before writing.
- Validate the frozen C11-C manifest (`e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`) and D4.8 R1V V2 policy (`0866b53ad4fcdebe74d01f66864b2dfb00eb644ca28dcd59301c8f3208239c07`).
- Classify each destination as `ADD`, `SKIP_IDENTICAL` or `CONFLICT`. Any conflict blocks the whole write phase; no destination is overwritten.
- Stage and hash every missing payload before applying any of them. Each destination is installed with a same-directory temporary file and atomic create/move semantics.
- Write a unique journal checkpoint after preflight and after each successful file. If interrupted, rerun the same installer: exact files are skipped; missing files are safely added; changed files remain conflicts.
- No rollback deletes user files. A partial run is intentionally recoverable by idempotent completion.

## Run sequence

1. Verify ZIP SHA-256 using the supplied sidecar.
2. Expand into a fresh temporary directory, not into the checkout.
3. Run the V2 installer once. It is safe to rerun after an interrupted V2 run because it never replaces.
4. Run the V2 read-only audit wrapper once. It checks the V2 scripts' own pins, uses Python 3.13, executes 13 focused tests, then audits source/evidence pins and writes a receipt.

## Diagnostic behavior

The V2 Python audit always records missing and mismatching source/document pins as separate rows. Evidence evaluators are isolated: a missing/corrupt JSON or closeout produces `BLOCKED_INPUT_ERROR` in the receipt rather than aborting before a diagnostic receipt can be written. A fail-closed audit returns exit 3 and keeps the receipt; inspect `diagnostics`, `source_pins.rows`, `baseline_document_pins.rows`, and `prior_evidence` before retrying.

The audit has no subprocess/media dependency. It never invokes Producer, Godot, FFmpeg, FFprobe, D3, renderer, media generation, mux, dispatch, or BatchId reservation. Its expected result is an audit-only pass with E6 media still held; it is not Smoke18 acceptance or authorization.

## Immutable boundaries

C11-C 2.19.12 and the frozen manifest remain unchanged. D4.8 remains unchanged and continues to prohibit Smoke18, D3/audio/PCM and FFmpeg mux. E1 remains PREPARE_ONLY; family adapter remains NOT_CONNECTED_E1; renderer OFF; dispatch/media false; release authority NONE. No Git inspection; commits remain operator-managed.
