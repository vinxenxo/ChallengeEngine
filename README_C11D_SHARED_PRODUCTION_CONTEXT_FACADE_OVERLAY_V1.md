# C11-D Shared Production Context Facade V1 Overlay

Adds one D-owned in-memory backend facade and a thin CLI wrapper for future GUI/CLI consumers. The facade composes D9.9, D9.10 bridge, D-only prepare adapter and shared editorial/presentation binding.

## Apply

Extract this ZIP to the repository root after verifying its SHA-256 and the immutable C11-C manifest. It contains new files only and must not overwrite anything.

## Validate

Run `python -B tools/c11d/d9/test_shared_production_context_service.py` and then `python -B tools/c11d/d9/shared_production_context_cli.py --audit-only`. Re-run the canonical D9.8/D9.9/D9.10 tests, cross-suite lifecycle and D baseline preflight.

## Boundary

No renderer input, dispatch, production, media output or persistent result record is created. The presentation-profile registry proves identity only; profile geometry remains unresolved.
