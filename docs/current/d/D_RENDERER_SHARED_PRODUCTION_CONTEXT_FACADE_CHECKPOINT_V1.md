# D9 Shared Backend Facade V1 — Checkpoint

## Purpose

This increment establishes one reusable Python API for future GUI and CLI callers. The facade composes existing authorities only: D9.9 canonical request planning, D9.10 editorial bridge, the D-owned prepare-only adapter, and the shared editorial/presentation context binder. It does not duplicate editorial resolution or family-specific visual logic.

## Contract

- API: `prepare_shared_production_context(raw_request, project_root=None)`.
- Validation: `validate_shared_production_context(record, raw_request, project_root=None)`.
- CLI: `shared_production_context_cli.py --request <read-only-request.json>` or `--audit-only`.
- GUI and CLI must call the same service API; no UI-specific resolver is authorised.
- The returned object carries canonical result, D9.10 bridge record, D-only adapter envelope, and shared editorial/presentation binding under a single integrity envelope.
- CLI stdout is ASCII-safe JSON for portable process parity. No output-path option exists, and the service does not persist results.

## Scope and limitations

Supported types remain Challenges, Visual Loops and Visual Drills. A selection or registered presentation identity not accepted by the canonical contract is rejected. `social_default_v1` remains a reference identity, not an approved physical profile; geometry and editorial visibility timing are not resolved here. Editorial values are bound to context but not yet consumed visually. No renderer-native input or media is produced.

## Governance locks

C11-C remains immutable. `renderer=OFF`, `media_created=false`, `D4.8=BLOCKED`, `release_authority=NONE`, D9.17 remains NO-GO and D10 remains blocked. This record is a common backend preparation facade, not a production or render-ready manifest.

## Validation

The dedicated test covers all three supported types, API/CLI exact parity, deterministic identities, editorial override isolation, profile rejection, unsupported type rejection, tamper rejection, output-schema validation and source-drift fail-closed behaviour. Local Python validation must be followed by the user's Windows checkout regression suite.
