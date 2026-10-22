# C11-D Overhand Master Prompt V19 — Coordinate Consumer Track

## Mission

Continue C11-D toward a controlled, review-only path to a first D-baseline render. The eventual goal is replacement of C11-C only after formal acceptance, freeze, approval, and promotion. No routine confirmation is needed to proceed through defined engineering gates, but formal locks must never be bypassed.

## State

The active Windows checkout has operator-confirmed PASS gates: semantic decision `146/146` (receipt `3cf2284c454a06571ea97a2e771a259d2b73a8f4616432063a581b5c3e57ecf9`); field-region proposal `551/551` (receipt `87c8ab97db18a7531dc2df610b51fe819c8bf746b2b66475b544220c37c95cbb`); field-region decision `653/653` (receipt `4df0b28d7d933ca2c28b34e50e126112007bc0cc6fe24322e020d9d5f222677a`); coordinate policy proposal `961/961` (receipt `1518168dd6b50fc869dbd18b05dcdef13397ea8023ff6fa1f896f55dee5b9f96`); coordinate policy decision `2756/2756` (receipt `b61fb3403e0ad5725937be05f8a7153c3cf35ccde167306f45151ece0f1cc4cb`).

## Next artefact

Validate the renderer-neutral allowlisted coordinate consumer specification. It reads one approved custom_data field only, emits only a strictly allowlisted logical target-marker track contract, preserves source-frame ordinal and cardinality, and rejects invalid or mixed tracks atomically. It is not implementation.

## Permanent safeguards

Frozen C11-C manifest SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953` stays immutable. `renderer=OFF`; `media_created=false`; `payload_materialized=false`; `candidate_input_admissible=false`; zero approved bindings of all classes; `D4.8=BLOCKED`; `D9.10=PREPARE_ONLY`; `D9.14/D9.16=BLOCKED`; `D9.17=BLOCKED_NO_GO`; `D10=BLOCKED_FOR_PROMOTION`; baseline approval missing; freeze ineligible; release authority none. Never serialize all of `FrameSnapshot.custom_data`. Do not mutate challenge JSON or the CHALLENGE_004 V1 harness.

## Workflow

Use additive ZIP overlays with checksummed manifests and explicit source/authority/evidence pins. Deliver separate APPLY and TEST blocks, use PowerShell 5.1-compatible constructs, start processes with explicit logs and ExitCode checks, and never claim PASS when a helper did not run. After this spec gate, progress to the implementation design and negative-test contract without dispatching or invoking the renderer.
