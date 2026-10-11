# C11-D Renderer Candidate I/O Conformance Gap Audit Overlay V1

Additive, read-only preparation overlay. Contains six new files and overwrites none.

## Apply

Extract the ZIP at the existing repository root. Review the source pins before executing.

## Verify

```powershell
python -B .\tools\c11d\d9\test_d_renderer_candidate_io_gap_audit.py
python -B .\tools\c11d\d9\d_renderer_candidate_io_gap_audit.py
```

The audit covers the ten required groups in the prospective renderer input schema. It reports source/conformance readiness only: candidate input stays inadmissible, no input or output-manifest instance is emitted, no renderer dispatch or media creation occurs, D4.8 stays blocked and release authority remains NONE. It is not a renderer-runtime test.
