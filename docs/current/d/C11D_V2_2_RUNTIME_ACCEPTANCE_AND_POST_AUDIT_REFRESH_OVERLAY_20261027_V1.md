# Overlay — C11-D V2.2 Runtime Acceptance + one-shot audit refresh

**Overlay ID:** `C11D_V2_2_RUNTIME_ACCEPTANCE_AND_POST_AUDIT_REFRESH_OVERLAY_20261027_V1`  
**Mode:** 2 guarded replacements + 3 add-only destinations  
**Purpose:** record the observed Windows V2.2 PASS and install a read-only helper to refresh I/O gap + candidate identity once.

## Root cause resolved

The V2.2 fix kept the composite canonical editorial digest separate from the map-only sidecar digest, reconstructed the complete canonical selection + editorial-map hash, and verified exact sidecar field values. The Windows acceptance confirms 16/16 focused tests, three runtime joins, 14/14 fields, 0/14 visual consumption and 60/60 source pins.

## Files

- Replaces `docs/current/d/D_RENDERER_REQUEST_PAYLOAD_INSTANCE_INTEGRATION_CHECKPOINT_V2_2.md` under its exact source SHA.
- Replaces `docs/current/d/C11D_ENGINEERING_PHASE_LEDGER_20261027_V1.md` under its exact source SHA.
- Adds `docs/current/d/C11D_REQUEST_PAYLOAD_V2_2_RUNTIME_ACCEPTANCE_20261027_V1.md` as an immutable per-phase record.
- Adds `tools/c11d/d9/refresh_d_renderer_candidate_io_and_identity_after_v2_2.ps1` to run both read-only audits once and capture evidence.
- Adds this overlay record at `docs/current/d/C11D_V2_2_RUNTIME_ACCEPTANCE_AND_POST_AUDIT_REFRESH_OVERLAY_20261027_V1.md`.

## Apply and execute

Extract the separate PowerShell Test Kit delivered with this overlay, then run `C11D_V2_2_PostRuntime_Run_All.ps1` from PowerShell 5.1. It verifies the ZIP hash and exact archive entries (sorted strings are compared in separate variables to avoid PowerShell operator-precedence bugs), checks all preconditions and add-only destinations, verifies backups, applies, and verifies final hashes. It then runs the read-only I/O and identity refresh helper.

The helper checks current hashes for C11-C, the V2.2 implementation/test/contract/schema, and both audit runners. It captures report stdout/stderr independently and stops on any pin drift or policy mismatch. The helper stores a completed marker under `%TEMP%` after both audits pass, preventing routine accidental re-execution on the same phase. If an audit fails, it retains the folder and does not mark the refresh completed.

## Evidence captured from V2.2 runtime

- Focused test exit `0`, tests `16/16`; stdout SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`; stderr SHA-256 `3183ebabac73872621e28e140dc029fb9875826166ab85b7a0fe2687f6b7215f`.
- Godot `4.7.1.stable.mono.official.a13da4feb`; runtime exit `0`.
- Runtime stdout SHA-256 `00a0d51627618ae3ee167a7d2ca029f6ed5cd05ecf369f8d816ef5774d99051a`; stderr SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
- Receipt SHA-256 `1a2a729137458f633cf520c211180ce5a3fff2d21ed441e866ae0e1c946169af`.

## Governance boundary

El runner no escribió solicitud, payload ni recibo de integración dentro del repositorio. La orquestación sí conservó el registro de validación `runtime_validation_evidence.json` en `%TEMP%`, según la ruta indicada arriba. No se emitió renderer-native input/dispatch ni se creó media. Las auditorías siguientes son read-only. `renderer=OFF`, `candidate_input_admissible=false`, `D4.8=BLOCKED`, `release_authority=NONE`, frozen C11-C unchanged. The next documentation overlay must record the real post-runtime audit outputs, not assume their values.
