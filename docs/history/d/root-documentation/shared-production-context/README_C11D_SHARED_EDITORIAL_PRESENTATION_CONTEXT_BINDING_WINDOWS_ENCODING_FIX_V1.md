# C11-D Shared Editorial/Presentation Context Binding Windows Encoding Fix V1

## Change

Fixes the Windows Python 3 subprocess JSON-parity check. The CLI emits JSON using ASCII escapes, and the test captures bytes, requires successful process exit, verifies ASCII-safe machine-readable output, then parses JSON with actionable diagnostics.

## Apply

Use the copy/paste PowerShell block supplied in the conversation. The ZIP contains only three modified files and this README. The block checks exact prior hashes and the immutable C11-C manifest before extraction.

## Validate

Run `python -B .\tools\c11d\d9\test_d_renderer_shared_editorial_presentation_context_binding.py`, then `python -B .\tools\c11d\d9\d_renderer_shared_editorial_presentation_context_binding.py --audit-only`, then the regression suite.

## Boundary

No renderer input, process dispatch to a renderer, media output, persistent receipt, or C11-C source change is introduced. Governance remains D4.8 BLOCKED and release authority NONE.
