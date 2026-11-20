# C11-E installer and runner incident register — V65

## V4 QImage import failure
- Godot import and one-frame capture both exited 0.
- The captured source PNG and RGB24 file are present and hash-verified.
- QImage module loading failed with `AttributeError: 'NoneType' object has no attribute '__dict__'`.
- Root cause: `module_from_spec` + `exec_module` without registering in `sys.modules`; dataclasses with postponed annotations require module namespace lookup.
- V5 fix: register first, execute second; remove partial registration on failure.
- Recovery: reuse existing V4 evidence; no Godot repeat.

V1–V4 installers and receipts remain immutable.
