# C11E E6 Challenge Live Consumer Readback PREPARE_ONLY V1

This add-only overlay performs a static compatibility audit of the 18 exact Challenge D envelopes produced by the successful editorial binding run. It validates the exact pinned consumer and adapter source, derives per-phase frame samples, and records expected D/native ownership.

It does **not** invoke Godot or claim runtime readback. It does not create pixels, media, audio, mux, renderer input or dispatch. D4.8 remains BLOCKED and E6 TEST_ONLY runtime authorization remains false.

## Install and run

Run from Windows PowerShell 5.1 with the active checkout and canonical Python 3.13.14. The delivery is one self-contained PowerShell 5.1 Apply `.ps1` plus SHA-256 sidecar. The Apply validates its own hash, embedded archive member list, manifest/sidecars, payload/source pins, parent paths, reparse points and destination collisions; stages `py_compile` plus 38 tests; validates the exact binding install receipt and its sidecar; runs one static readback audit before the ADD_ONLY transaction; then commits the payload and links the audit plan/receipt in its install receipt. No nested installer is required and no post-commit duplicate audit is run. No existing file is replaced.

Expected result: `PASS_STATIC_CONSUMER_CONTRACT_18_ENVELOPES_RUNTIME_READBACK_NOT_PERFORMED`.
