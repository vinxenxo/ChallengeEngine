# C11-E E3 Windows Automated Test Acceptance — V1

**Date:** 2026-11-03
**Runner:** `RUN_C11E_E3_TESTS_FROM_DOWNLOADS_V1_4.ps1`
**Runner SHA-256:** `eb57854d90aac1bf78367aa63f101c54206ae9777d9cbcfc65df02207cf404b5`
**Patch:** `C11E_E3_AUDIO_TEST_OVERLAY_V1_3.zip` SHA-256 `69ae53e1ee1edbf7db015b3e311f0826e0d94f4195b5153ed8820d69af0030c1`.

## Operator-observed Windows result

- Evidence directory: `C:\Users\vinxe\Documents\C11E_E3_TEST_EVIDENCE\C11E_E3_TESTS_V14_f371a0bfdccf407aba5e3e4cbf6c5f4b`.
- Receipt: `C11E_E3_WINDOWS_TEST_RECEIPT.json`.
- Receipt SHA-256: `84fc86c96ca237c7dd16837666882e80afe6dda8292a04527d19fcbd3579e30b`.
- Python 3.13.14 discovery and `python --version`: PASS.
- `py_compile` over changed producer/service/engine/test modules: exit 0.
- `python -m unittest discover -s c11c-suite\c11c-producer -p test_c11e*.py -v`: **31/31 PASS**, 18.085 seconds, exit 0.
- PySide6 import: PASS, version `6.11.2`.

## Test composition

- 8 E3.2 contract/binding tests.
- 5 E3 audio-pipeline tests, including the full Challenge audio mux/repeatability/seed-isolation integration test against the immutable R4 fixture.
- 5 E3 GUI integration contract tests (source/contract level).
- 13 existing E1 shared production service tests.
- Total: 31 tests, no failures or skips reported.

## Scope and limits

The E3 pipeline integration test invoked FFmpeg mux using temporary test media. The runner reports `FFMPEG_MUX_IN_TESTS=true`, `TEST_MEDIA_SCOPE=TEMPORARY_ONLY`, and no production audio creation. It did not invoke Godot, rerender gameplay, launch the GUI or create a production product. PySide6 import and GUI source-contract tests do not constitute real GUI runtime acceptance.

This is accepted automated Windows evidence for the installed V1.3 code. It does not close E3. The pending gate is E3-GUI-01, followed by one operator-driven GUI pilot and complete E3 receipt/QA review.
