# C11-D Editorial Field Window — Empty SHA-256 Guard Fix V1

Minimal hotfix for the Godot 4.7.1 runtime warning emitted when the field-window proposal hashes the empty canonical `reveal` string.

## Root cause

`HashingContext.update()` rejects an empty `PackedByteArray`, but an empty field is a valid editorial value and has a well-defined SHA-256 digest.

## Changes

- `tools/c11d/d9/review_editorial_field_windows_in_memory.gd`: `_sha256_bytes()` returns the canonical SHA-256(empty) digest before calling `HashingContext.update()` when the byte array is empty.
- `tools/c11d/d9/test_d_renderer_editorial_field_window_proposal.py`: adds a regression guard proving the harness contains and uses that empty-input branch.

## Apply

Extract this ZIP at the repository root. It contains only the two changed project files plus this README.

Then run:

```powershell
python -m py_compile `
  .\tools\c11d\d9\test_d_renderer_editorial_field_window_proposal.py

python .\tools\c11d\d9\test_d_renderer_editorial_field_window_proposal.py

godot --headless --path . --script res://tools/c11d/d9/review_editorial_field_windows_in_memory.gd
```

Expected result: no `HashingContext.update()` errors; the Python contract prints `empty_hash_guard=PASS`; Godot prints the usual field-window proposal `PASS` and summary. Treat any Godot error as failure even if a later line prints `PASS`.

This hotfix does not alter source content, C11-C, the proposed window policy, renderer activation, D4.8 or release authority. It creates no files at runtime and does not enable rendering.
