# C11-E Apply and Installer Standard V1

**Date:** 2026-11-04

## Delivery format

- Deliver a single `.ps1` directly downloadable to `Downloads`. Do not nest the apply script inside multi-level ZIP folders. A sidecar SHA-256 file may accompany it.
- The active Windows checkout is the only source of truth. Never extract a snapshot ZIP over the checkout.
- Use Windows PowerShell 5.1 syntax and perform a native AST parse of the executing script before repository writes.

## Transaction contract

1. Check every target preimage SHA-256 and every protected source pin.
2. Construct all postimages in memory, calculate their UTF-8-no-BOM bytes and verify every specified postimage SHA before the first write.
3. Save exact preimages to a unique `Documents` evidence folder.
4. Write atomically through a temporary sibling file and verify the target postimage SHA.
5. Run the focused tests and py_compile; capture stdout/stderr hashes and exit codes.
6. For a runtime gate, invoke the actual pinned runtime and validate structured report/receipt, media counts, all hashes and clean error streams. Exit code 0 alone is insufficient.
7. Add versioned documentation only after the matching gate has been evaluated; never overwrite earlier records, stage or commit automatically.
8. If an upstream patch is already reflected in the exact preimage, assert its expected state; never reapply a stale text replacement for a prior migration.

## Failure behavior

- A preimage or computed postimage mismatch must stop before any target source write.
- If a write fails mid-transaction, restore only files whose current hashes match this transaction's postimages.
- After source/tests pass but a runtime gate fails, retain the valid, hash-verified source correction and preserve exact evidence; do not reinstall it. Diagnose the specific failing contract and patch only that boundary against the new exact preimages.
- Never trust an expected postimage hash merely because it is embedded in a script. Reproduce the transformation and tests before delivery.

## Scope rules

E-only adapters and validation may change. Frozen C11-C source, manifest, binders, mechanics, RNG, core/audio and canonical definitions remain protected. Production renderer, dispatch and media stay disabled without separate authority. Test-only technical PASS is not human visual approval or release authority.