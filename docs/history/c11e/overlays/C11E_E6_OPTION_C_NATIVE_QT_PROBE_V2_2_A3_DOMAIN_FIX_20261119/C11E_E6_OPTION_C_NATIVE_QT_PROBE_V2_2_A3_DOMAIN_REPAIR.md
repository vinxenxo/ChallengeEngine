# C11-E E6 Option C — A3 identity-domain repair V2.2

**Date:** 2026-11-19  
**Status:** engineering correction package; not an E6 acceptance and not a renderer authorization.

## 1. Recorded run and outcome

The V2.1 installation completed successfully: 16/16 destinations verified, `INSTALL_STATUS=PASS_ADD_ONLY`, receipt SHA-256 `3585bfd3f946bcc3502c175daf6d058133393840f60a89623fe7ab83bb33181a`.

The V2.1 native Qt runner then stopped before QImage tests with:

`LOOP_POLICY_A3_ADJUDICATION=BLOCKED/A3_POINTER_VALUE_MISMATCH:old_pointer_expected`

The probe receipt SHA-256 is `6607dedc2a6868cb79bd9a2706b9a2195f6cda27f820210d0d2a3cd484e4b104`. The receipt records `QIMAGE_TESTS=0; STATUS=NOT_RUN`, exit code 2, and no source, C11-C or D4.8 V2 modifications. Godot, FFmpeg, FFprobe, audio generation and mux were not invoked.

## 2. Root cause: two identity domains were conflated

The V2.1 adjudicator treated all four legacy fields containing `pointer` as hashes stored at the JSON pointer. The live run rejected that assumption at `old_pointer_expected`. The active diagnostic JSON was not supplied as a separate file with this run, so V2.2 does not invent one global interpretation for those legacy labels. Instead, each side's expected/actual pair must agree exactly and match one of the two independently pinned identities for that side: its whole-manifest SHA or its value at the approved JSON pointer. The explicit bridge fields `bridge_old_pointer_value` / `bridge_new_pointer_value` must always match the pointer values.

The two domains are:

| Identity | Expected SHA-256 | Meaning |
|---|---|---|
| Historical manifest | `2075da9c33c689861a68d3bd8fb19b7ed593c6e76010ab200880746aa6d1a470` | Entire 8,591-byte historical JSON file |
| Current manifest | `5702092bc1c88e4b333dd30cc150f0d383cd2006121037b0198905c75a3af795` | Entire 8,591-byte current JSON file |
| Old pointer value | `50655c82521a353f1db6920f4d099cad92452ae369251f9fbde45cbaee4e8c53` | `source_lineage[6].sha256` in the historical manifest |
| New pointer value | `dabb458fc2215156ddb5ebea7e8ebec811098886ce2858733ba9fb13f6075ccb` | `source_lineage[6].sha256` in the current manifest and SHA of the pinned D9.8 model |

The bridge itself remains pinned at `aec0e387f167f4b821b7d94f06a67f78f498be939fe3cda857d20ce550819cac`. The approved pointer remains exactly `/source_lineage/6/sha256`.

## 3. V2.2/V3 correction

A new, separate runner and support module are installed under `tools/c11d/d9/c11e_e6_option_c_native_qt_probe_v2_2/`. The V2.1 files and receipt remain untouched.

The adjudicator now:

1. Validates each legacy expected/actual pair against a finite two-value domain for that side (whole historical/current manifest SHA or corresponding old/new pointer SHA), requiring exact expected/actual equality. The result records which domain each pair used.
2. If the diagnostic supplies `bridge_old_pointer_value` or `bridge_new_pointer_value`, checks each strictly against the corresponding **pointer value** in the pinned bridge. The bridge and source manifests are independently pinned whether or not these optional diagnostic fields are present.
3. Independently checks all four source identities on disk, both manifest byte counts and whole-file hashes, the D9.8 target file pin, and the operator A3 decision / approved proposal pins.
4. Reconstructs the current JSON from the historical JSON by changing only `/source_lineage/6/sha256`. Any extra field, structural difference, pointer drift or unrelated difference fails closed.
5. Accepts the specialized receipt status only when the 17 literal PASS rows, 1 exact specialized PASS row, top-level status, 18/18 counts and all source/policy checks match.

No diagnostic, source receipt, manifest, bridge, decision record, policy, or historic file is rewritten.

## 4. Scope and limits

The V2.2 runner reuses the already-installed, pinned V2 QImage implementation and its 37-test suite; it does not reinstall or modify that payload. The included A3 regression suite uses an isolated copy of the pinned project documents and never mutates the active checkout. Its output and receipts use a new V2.2 artifact directory. After A3 succeeds it may run 37 synthetic QImage tests and seven synthetic benchmark iterations only.

Even a green result means only `PASS_QIMAGE_STAGE_BENCHMARKED_NOT_END_TO_END`. It does not admit real video decode, real frame input, Godot, FFmpeg/FFprobe, music, audio, mux, dispatch, BatchId consumption, E6 acceptance, release authority or D4.8 promotion. D4.8 V2, renderer OFF, dispatch/media OFF, E1 PREPARE_ONLY and all D9/D10 locks remain intact.

## 5. Source-preservation guarantees

- C11-C frozen manifest SHA: `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953` (796,318 bytes), unchanged.
- D4.8 V2 SHA: `0866b53ad4fcdebe74d01f66864b2dfb00eb644ca28dcd59301c8f3208239c07` (12,996 bytes), unchanged.
- Option C V4 Python reference source remains pinned, unchanged.
- V2.1 support module/runner and both failed receipts remain immutable historical evidence.
- `GIT_CHECKS=SKIPPED`; commits remain operator-managed; source-file pins are enforced.
