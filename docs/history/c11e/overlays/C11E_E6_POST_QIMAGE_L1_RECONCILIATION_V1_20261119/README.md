# C11-E E6 post-QImage L1 reconciliation — V1

## Purpose

Consolidate the operator-confirmed V2.7 result with predecessor evidence already present in the active checkout. This is a read-only PREPARE_ONLY audit; it does not repeat earlier tests, alter any prior receipt, run an engine, decode media or authorize Smoke18.

## Current accepted technical result

V2.7 installed 18/18, placed 11/11 documents inside the repository, passed the eight import-bootstrap tests, then passed the 37 original QImage tests using Python 3.13.14 / PySide6 6.11.2. Seven iterations yielded P50 4.7681 ms, P95 5.5743 ms and 179.3947 fps at P95. Runner receipt SHA-256: `95819ea730283ded149faa490b21e0df392341366a853b3c0913318fb203d783`. This qualifies a synthetic native pixel stage only.

## What this overlay audits

- V2.7 installation receipt, runner receipt and sidecars.
- All 23 source checks carried in the V2.7 runner receipt, rehashed against the active checkout.
- The 3 synthetic preview PNGs and their runner-bound hashes. Hash validity is not human visual acceptance.
- Challenge static consumer contract: 18 envelopes, 117 frame sample vectors, 27 visible slots and 27 intentional zero-window suppressions; runtime readback remains unperformed.
- CH004 historical source preimages, semantic noninterference and Smoke18 reuse linkage; CH004 remains a candidate, not an accepted E6 row.
- Loop Policy V2 and the V2.7 A3 V4 adjudication; this is not six-selector D-compositor acceptance.

## Install location

The versioned documentation is installed under `docs/history/c11e/overlays/C11E_E6_POST_QIMAGE_L1_RECONCILIATION_V1_20261119/`. Current authority, matrix, doc index, incident register, roadmap and phase ledger go under `docs/current/e/`. Continuation prompts go under `prompts/`. Test-only policy/authorization drafts go under `definitions/c11e/test_only/`. No document is left only in Downloads.

## Scope and safety

`D4.8 V2` remains immutable and BLOCKED. E1 remains PREPARE_ONLY; renderer OFF; dispatch/media OFF; E6 accepted 0; no BatchId; release authority NONE. No Godot, FFmpeg, FFprobe, audio, mux, media, source frame copy, or production renderer input is invoked.
