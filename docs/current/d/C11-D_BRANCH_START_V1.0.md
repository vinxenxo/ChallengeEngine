# C11-D — Branch Start V1.0

## Entry condition

Start D only from the sealed C11-C 2.19.12 archive produced by the canonical Maintenance freeze packager, with verified archive SHA-256, source-tree SHA-256 and freeze receipt.

## First action

Create a new D workspace from the sealed archive. Do not develop D directly in the frozen C11-C source tree.

## D0

1. Verify archive and source-tree hashes.
2. Run the frozen Suite/Producer/parser/layout checks before mutation.
3. Inventory source, definitions, profiles, assets, manifests, seeds and preserved evidence.
4. Recover `CHALLENGE_001` … `CHALLENGE_009` into evidence dossiers.
5. Record current-vs-historical mismatches instead of rewriting historical evidence.
6. Produce the D1 visual-parity contract.

## Operator architecture

GUI and CLI are co-equal. A D feature is not complete until its canonical console operation and GUI surface agree on inputs, provenance and reproducible outputs.

## Frozen C boundary

Do not modify C11-B/C mechanics, simulation truth, RNG, result semantics, timing truth, proven rendering/presentation behavior, C7/C9 contracts or logical 540x960 geometry without an explicit new checkpoint.

## Approved roadmap

`D0 → D1 → D2 → D3 → D4 → D5 → D6 → D7 → D8 → D9 → D10`
