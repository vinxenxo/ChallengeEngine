# E4C Drill A/V Overlay Installation Contract V1

## Package mutations

Two exact-pinned replacements: existing Producer `main.py` and existing `c11e_production_cli.py`. D-owned additions: one execution adapter, focused stdlib tests, current E documentation, history records and versioned prompts. No E1 service replacement; no mutation of C11-C; no changes to dependencies or requirements.

## Pre-write gates

The PS5.1 installer validates its own AST, package manifest and every payload SHA/byte length, source pins, frozen manifest, replacement preimages, add-only destinations, path lengths, Python 3.13, existing PySide6/Qt and a non-null QPainter probe. It stages the patched entrypoints, adapter and tests under `%TEMP%`, runs py_compile and the stdlib test suite, then repeats all support pins and destination-state checks immediately before transaction.

## Transaction

A run-specific journal is durably written before each repository mutation. Each replacement stores and verifies an exact non-empty preimage backup. Temporary files are created beside the destination and verified against the package postimage before atomic replacement. Adds are atomic new-file moves. Existing identical postimages are reusable; differing collisions stop.

## Rollback

Rollback traverses the journal in reverse. A replacement is restored only if the current file still equals the exact package postimage and its backup equals the recorded preimage. An addition is removed only if its current file equals the package postimage. If a destination has any unknown hash/state, rollback refuses to overwrite it and reports incomplete rollback; it never guesses.

## Operator-owned validation

After install PASS, inspect the receipt and every postimage. Launch the existing GUI; plan a Visual Drill request with at least one real text field; run the first `tracking/tier-1` A/V qualification (gameplay 12345, music A/B 840001, C 840002). Review final video/audio and all receipts. Do not scale to 20 A/V selectors until this first end-to-end route passes.
