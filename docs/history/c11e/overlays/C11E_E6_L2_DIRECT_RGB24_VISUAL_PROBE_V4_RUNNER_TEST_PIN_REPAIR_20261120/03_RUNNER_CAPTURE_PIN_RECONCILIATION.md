# V4 runner capture pin reconciliation

V3 had two competing capture-script SHA domains: the execution manifest and source-pin manifest recorded the correct V3 file, while the Python runner constant retained a stale prior digest. V4 computes the final V4 GDScript bytes first and writes that exact SHA-256 and byte count into all three locations:

- Execution manifest `capture_script_sha256` / `capture_script_bytes`.
- Source pin manifest `godot_capture_harness`.
- Python runner `CAPTURE_GD_SHA` / `CAPTURE_GD_BYTES`.

The test suite independently asserts equality across these representations, then hashes the actual installed capture script. Expected V4 capture harness SHA: `f7edeba719558db4b4e6151d1ba2a14ebb490ee63b27f66fdc1c748192bc81d9`; bytes: `6640`.
