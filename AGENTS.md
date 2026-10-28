# AGENTS.md — C11-D current authority (2026-10-28 V25)

## Continuation authority

Active Windows checkout: `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`. Use these current artifacts in order:

1. `AGENTS.md` and `.continue/rules/CONTINUE.md` for execution constraints.
2. `prompts/C11D_D_FINAL_CLOSEOUT_HANDOVER_MASTER_PROMPT_20261028_V25.md`.
3. `docs/current/d/C11D_FULL_CONTEXT_CONTINUITY_CHECKPOINT_20261028_V25.md`.
4. `docs/current/d/C11D_ENGINEERING_PHASE_LEDGER_20261028_V2.md`.
5. `docs/current/d/C11D_PHASE_P_STATIC_TEST_EVIDENCE_RECORD_20261028_V1.json` and `docs/current/d/C11D_PHASE_P_RUNTIME_RECOVERY_AND_NEXT_GATE_20261028_V1.md`.
6. `docs/current/d/C11D_POWERSHELL_51_TEST_EXECUTION_PLAYBOOK_20261028_V1.md` and `docs/current/d/C11D_RENDER_TO_BASELINE_D_CLOSEOUT_ROADMAP_20261028_V1.md`.
7. `docs/current/d/C11D_ENGINEERING_PHASE_LEDGER_20261027_V1.md`, Phase O acceptance artifacts, Phase P contract/schema, gate contracts and earlier V24 documentation as history.

## Current scoped state

Phase O is accepted as a read-only source-frame semantic crosswalk; it approves no bindings. Phase P implementation static suite is reported by the Windows operator as 30/30 after the Python version-normalization fix. Python preflight was 3.13.14. Phase P **runtime is not accepted yet**. The immediate action is one guarded execution of the current Phase P runner followed by verification of its actual report, pins, process evidence and hashes; do not create another speculative patch or repeat the runtime blindly after failure.

The next context should receive `C11D_PHASE_P_CONTEXT_HANDOVER_DOCUMENTATION_OVERLAY_20261028_V1.zip` plus a fresh `c11c-suite` context snapshot named `ChallengeEngineV01_STATELESS_C11-D10_CONTEXT_SNAPSHOT_20261028_POST_PHASE_P_STATIC_PASS.zip`. A new snapshot hash is expected. Treat it as read-only, never extract over the working tree, and do not infer anything about the canonical live manifest from a snapshot's overall hash.

## Frozen C11-C and governance locks

C11-C 2.19.12 remains authoritative and immutable until C11-D completes separate approval, freeze and promotion. The **live checkout** `release/C11C_FREEZE_PACKAGE_MANIFEST.json` must remain SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`, 796318 bytes. Do not copy a manifest out of the archive. Do not modify C11-C implementation, canonical seed V1, simulation truth, RNG ownership, `SimulationResult`, frozen geometry or source `winning_frame`.

`winning_frame` is the only Challenge temporal anchor; `close_calls` is episode count. `CHALLENGE_008` and `CHALLENGE_009` declared duration 11s vs phase sum 12s remains unresolved. `target_x` remains scalar. Editorial sidecar consumption is 0/14.

Hard locks: `renderer=OFF`; `media_created=false`; `payload_materialized=false`; `candidate_input_admissible=false`; `seed_domains_complete_for_candidate_input=false`; `automatic_seed_generation=false`; `master_seed=NOT_ADOPTED`; `approved_bindings=0`; `approved_custom_data_bindings=0`; `approved_renderer_projection_bindings=0`; `D4.8=BLOCKED`; `D9.10=PREPARE_ONLY`; `D9.14=BLOCKED`; `D9.16=BLOCKED`; `D9.17=BLOCKED_NO_GO`; `D10=BLOCKED_FOR_PROMOTION`; `baseline_approval=MISSING`; `freeze_eligible=false`; `release_authority=NONE`.

## Engineering conduct

PowerShell 5.1; complete pasteable blocks; no `&&`, `Read-Host` or PS7-only syntax. Use `Start-Process -Wait -PassThru`, separate stdout/stderr, inspect process exit code and required marker. Keep apply and test separate. Verify exact hashes before changes. New dated artifacts are add-only; stable pointer changes require exact prehash, backup and posthash. Stop on first mismatch. Never claim PASS after a thrown error. Never loosen tests or infer binding/render authorization from evidence PASS.

## Nota específica sobre el ZIP de releases y la captura usada

El snapshot que llegó primero a la biblioteca (`ChallengeEngineV01_STATELESS_C11-D10_latest_FROZEN_20261028_163525.zip`) se inspeccionó con SHA-256 `199a65ee76eb72a878808cb7b3c862a3eeb945b356cab9726c5d6c86f64b55a1`, tamaño 8.366.872 bytes, 3.476 entradas y CRC limpio. Ese archivo no contenía todavía los artefactos Phase P y, por tanto, no es la captura correcta de continuidad posterior a Phase P.

Aclaración del operador: la divergencia observada en el contenido empaquetado de `releases` está causada por la generación del ZIP freeze/snapshot mediante `c11c-suite` para continuar el trabajo en otra ventana; no es un defecto adicional que deba abrir otra línea de investigación. La nueva captura tendrá una huella de archivo distinta intencionadamente. No invertir más iteraciones en intentar normalizar esa huella del ZIP. Solo comprobar la integridad del archivo y el estado del checkout vivo; no reescribir ni sustituir el manifiesto canónico desde el ZIP.
