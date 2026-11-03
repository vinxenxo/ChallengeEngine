# C11-E Recovery/Discovery Overlay V1 — Failure Analysis and Corrective Record

**Date:** 2026-11-03

## Observed failures

1. Apply V1 stopped before any add-only write because its V26 protected-document pin was one hexadecimal character short. Expected: `c4bc1bb8b62b64d3b60685b30428c47adfff6ecbfd53826647c0184aa91fed1`; actual: `c4bc1bb8b62b64d3b60685b30428c47adfff6ecbfd53826647c0184aa91fed1a`.
2. Discovery V1 emitted `Los tipos de argumentos no coinciden` before writing its report. The V1 script used `System.Collections.Generic.List[object]`/`List[string]`, method `.Add()` with PowerShell-created ordered dictionaries, and a multiple-pattern `Select-String` invocation. The exact failing statement was not included in the operator's console excerpt, so the isolated root statement is not claimed. V2 removes those argument-binding surfaces and enriches failure output with exception type, line and stack trace.

## Corrective design

- Full-length, verified SHA pin in the V2 apply manifest.
- Add-only docs apply is idempotent only for exact postimages; unknown existing bytes abort.
- Discovery uses arrays/PSCustomObject records, one scalar regular-expression string passed to `Select-String`, bounded results and no mutable collection method bindings.
- On failure, `DISCOVERY_BLOCKED.txt` includes error type, invocation line and script stack trace.
- A one-command launcher checks the package hash, expands to a fresh directory, applies docs, checks the pre-existing E3 recovery receipt and runs discovery. It captures per-stage stdout/stderr/exit codes; it never reruns the E3 50-test suite.

## Evidence and boundaries

E3 V1.5 recovery returned PASS and receipt SHA `8e01946da3de35c05430335259a88e14f5bae1b660c6896de5d8f13c37c3fafe`. The operator's original runner BLOCKED receipt is retained. The V1 apply stopped during preflight before writes. V1 discovery was read-only and made no checkout changes. V2 discovery is also read-only. No renderer/media/GUI/CLI production job is invoked.

E3 is closed test-only; E4A remains discovery-pending until V2 audit PASS. C11-C 2.19.12 and its frozen manifest remain authoritative; no release authority or promotion.
