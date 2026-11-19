# C11E E6 Challenge Editorial Binding PREPARE_ONLY V1 — 2026-11-19

This overlay advances E6 by binding the already approved synthetic Challenge family editorial fixture into 18 derived test-only D envelopes (six selectors × A/B/C probes). It does not change existing E1 intents, source D envelopes, canonical Challenge definitions, E4A policy V1, D1.5 layout, source timebases or phase timing.

## Operator-confirmed zero-second semantics

A HOOK/CTA phase of zero seconds is intentional suppression. Title/subtitle appear only in HOOK; CTA appears only in CTA. A zero-width canonical interval becomes `OMITTED_EMPTY`. Do not move those fields to GAME or another phase.

Expected aggregate: 54 field/probe slots = 27 visible + 27 intentionally suppressed.

## Apply and execute

1. Extract this ZIP into a fresh folder (do not extract over the project checkout).
2. Verify the external ZIP SHA-256 sidecar.
3. Run `INSTALL_AND_RUN_C11E_E6_CHALLENGE_EDITORIAL_BINDING_PREPARE_ONLY_V1.ps1` once with `ProjectRoot`, `PackageRoot` and the canonical Python 3.13.14 executable.
4. The installer validates package, source pins, staged AST/tests, exact destination collisions and ADD_ONLY transaction. It then commits the add-only payload and runs the PREPARE_ONLY binding runner in a separate process with stdout/stderr captured independently.
5. Review the emitted `E6_CHALLENGE_EDITORIAL_BINDING_RECEIPT_V1.json` and `.sha256` sidecar. A nonzero child exit is failure; no later console line can convert it to PASS.

## Output

`artifacts/tests/c11e/e6_challenge_editorial_binding_prepare_only/<RUN_ID>/` contains 18 derived envelope JSONs and sidecars, a binding manifest and a receipt. Original E1 intents and source envelopes are never rewritten.

## Boundary

No Godot, FFmpeg, FFprobe, renderer, audio, mux, media, production dispatch or BatchId. Runtime editorial readback remains NOT_PROVEN. D4.8 V2 remains immutable/BLOCKED; E1 PREPARE_ONLY; renderer OFF; E6 accepted 0; release authority NONE.
