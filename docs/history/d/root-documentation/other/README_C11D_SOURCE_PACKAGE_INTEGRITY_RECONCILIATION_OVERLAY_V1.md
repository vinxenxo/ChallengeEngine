# C11-D Source Package Integrity Reconciliation Overlay V1

**Type:** additive ZIP overlay; D-only documentation/audit metadata plus guarded canonical restoration of five frozen C11-C-protected files. No renderer code, GUI code, payload consumer, simulation code, or release authority is added.

## Apply scope

The ZIP contains only new/modified files:

- Five canonical C11-C-protected files, included only so the apply block can restore them if and only if the current file hashes match the known contaminated versions from the source archive. If already canonical, skip; if any unexpected hash is seen, stop.
- `definitions/c11d/production/D_RENDERER_CANDIDATE_IO_GAP_AUDIT_V1.json`: refreshes four D-owned source pins and corrects `next_safe_increment` to test the existing dynamic request/payload binding contract against real Godot 4.7.1 before proposing any new contract.
- Two current D checkpoints, updated to point to the designated 2026-10-13 16:14:18 source package and existing dynamic-binding runtime gate.
- `docs/current/d/C11D_SOURCE_PACKAGE_INTEGRITY_RECONCILIATION_V1.md`: integrity findings, preparation-copy tests and remaining runtime/governance limits.
- This README.

The PowerShell application block separately performs exact, surgical text substitutions in `docs/current/d/MASTER_HANDOVER_C11D_CURRENT.md` and `docs/current/d/START_PROMPT_C11D_CURRENT.md`. It does not wholesale replace those large operator-maintained documents. The block preflights every expected source snippet and file hash before making changes.

## Do not

- Do not extract the designated source context ZIP wholesale: it has duplicate `release/C11C_FREEZE_PACKAGE_MANIFEST.json` entries and prepends D context to five frozen-protected files.
- Do not change the frozen C11-C manifest or other protected source files.
- Do not add renderer input, dispatch, generate media, enable D4.8, freeze or release.
- Do not implement payload-side editorial visual consumption. Field-to-region/visibility policy is not approved.

## Required next runtime gate

Run `test_d_renderer_dynamic_request_payload_binding.py` and the ten-case `d_renderer_dynamic_request_payload_binding.py` runner against the actual Windows Godot 4.7.1 executable, exactly as specified in `D_RENDERER_DYNAMIC_REQUEST_PAYLOAD_BINDING_CHECKPOINT_V1.md`. The Python tests are mocked and do not close the runtime gate. The exact Visual Loop grammar payload for `harmonic_membrane` remains unresolved in the existing contract.

## Expected governance after application

C11-C 2.19.12 immutable; D9.10 `PREPARE_ONLY`; renderer OFF; no renderer input or dispatch; `media_created=false`; D4.8 BLOCKED; `release_authority=NONE`; D9.14/D9.16 blocked as required; D9.17 `BLOCKED_NO_GO`; D10 blocked; baseline approval missing; `freeze_eligible=false`.
