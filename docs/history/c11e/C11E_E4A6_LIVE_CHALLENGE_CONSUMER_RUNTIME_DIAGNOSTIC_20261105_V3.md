# C11-E E4A.6 Live Challenge Consumer — Runtime Diagnostic V3

**Date:** 2026-11-05. Status: `BLOCKED_FIELD_RANGE_VALIDATION_REPAIR_PENDING`. This record supersedes the V2 diagnostic only for current runtime status; it does not supersede accepted C11-C or E4A evidence.

## V2 user-run evidence

Evidence archive: `C11E_E4A6_LIVE_CONSUMER_V2_20261105_134630.zip`; SHA-256 `590040f2f3d838d15fb5ef2e4a90b3e023ef862f5b85665c0a0fe7b454249588`; ZIP CRC PASS; 21 entries. Original checkout: `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`; Git HEAD `a18444655cdb844104561840a59a473b7bbbb172`.

- PowerShell 5.1 AST: PASS.
- Nine base source pins: 9/9 PASS. `GeneradorMaestro.gd` preimage/postimage transaction: PASS. 32 add-only files: PASS.
- Python `py_compile`: PASS; 16/16 focused tests: PASS; E1 envelope + SHA sidecar: PASS.
- Godot 4.7.1 editor import: PASS, exit 0, stderr 0; generated `.godot/global_script_class_cache.cfg` verified by runner.
- Godot live root started and reached `GeneradorMaestro._ready`; stderr 0. It rejected the envelope with `C11E_E4A6_ENVELOPE_INVALID`: `D envelope field source frame ranges do not match approved phase windows: title`. No runtime summary or PASS receipt.
- The envelope's title row declares HOOK `[0,180)` at 60 FPS; its source phase table declares HOOK `[0,180)`, GAME `[180,600)`, REVEAL `[600,780)`, CTA `[780,900)`. Python's 16 tests validate those source ranges. The failure is at the GDScript field-row comparison; the V2 log does not expose expected/actual row internals, so no off-by-one or timeline defect is yet established.

## V3 minimal D-only correction

V3 changes only `tools/c11d/d9/C11EChallengeLiveEditorialConsumer.gd` and its focused source-contract test. The field-range comparison becomes explicit and schema-aware: exact row count, phase, integer-normalized start/end frame, and exact `SOURCE_FPS_HALF_OPEN` timebase. A rejection prints expected and actual JSON rows. No approved phase windows or frame ranges are changed. The test suite increases from 16 to 17.

`GeneradorMaestro.gd` is not modified by V3. Its existing postimage SHA-256 remains `d42782e8f5bb94ff0ede653a1c4624dc91541cc8203abf136b09a8fc288a7d82`. Its reviewed diff is additive and conditional on `--c11e-editorial-envelope`; with no envelope argument, the new helper returns immediately and existing native rendering path is unchanged.

## Worktree and snapshot decision

V2's nine pins passed on the original Git checkout. The reviewed E4A5B ZIP is a source snapshot without `.git` metadata and without generated `.godot` state. Do not extract it over the checkout or switch work roots. The V2 editor import has now generated the class cache in the original checkout; the remaining failure is field-range validation, not missing project content or class cache. Keep the snapshot as reference/evidence only.

## Acceptance still required

V3 must pass PowerShell 5.1 AST, exact source pre/post hashes, `py_compile`, 17/17 focused tests, Godot 4.7.1 import and 900-frame live root with `C11E_E4A6_LIVE_CONSUMER_SUMMARY=...`. Required counters remain 900 frames, one shared-layer mount, 180 header-owner frames, 120 footer-owner frames, zero native CTA-owner frames, and all governance flags false/NONE. A V3 pass is still test-only and does not close E4A final A/V.

## Governance

C11-C 2.19.12 remains immutable; renderer/dispatch/media OFF; D4.8 BLOCKED; D9.10 PREPARE_ONLY; D9.14/D9.16 BLOCKED; D9.17 BLOCKED_NO_GO; D10 BLOCKED_FOR_PROMOTION; `release_authority=NONE`. E4B/E4C remain held. No D3 V5 audio, FFmpeg, Movie Maker, production dispatch, staging or commit is authorized by this diagnostic.
