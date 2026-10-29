# C11-D Render Integration — Master Prompt V2 (29-10-2026)

## Mission

Move from D planning contracts to the actual D-owned visual consumer and A/V integration, then qualify Challenge, Visual Loops and Visual Drills. Do not mistake documentation volume, a green unit test, a plan hash or a Godot harness for an accepted physical video.

## Source hierarchy

The active checkout `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS` is authoritative. The uploaded filtered snapshot is validated context only (SHA-256 `5b8d06ad82bca798c94db03f943a85afb309d91484d4499ed40fed36056ca774`, 9,190,399 bytes, 3,721 unique ZIP entries). Read `AGENTS.md`, `.continue/rules/CONTINUE.md`, the V2 documentation index, the snapshot validation note, and current ledger/checkpoint/AD files. Verify actual bytes before treating any version/hash as current.

## Current boundary

- Ledger V18 / Checkpoint V41 are the latest verified continuity references from this snapshot.
- Phase AD's 60/60 tests and structural verifier pass validate its decision packet, not permission to render. Operator decision `PENDING_EVIDENCE_OR_KEEP_BLOCKED`, authority evidence count 0, adjudications 0, policy adoption `NONE`.
- Phase AC found no applicable approval within the reviewed 107-candidate corpus; do not generalize beyond the corpus.
- `renderer=OFF`, media/payload not materialized, candidate input inadmissible, seed domains incomplete, automatic seed generation false, `master_seed=NOT_ADOPTED`, approved bindings = 0, D4.8 BLOCKED, D9.10 PREPARE_ONLY, D9.14/D9.16 BLOCKED, D9.17 BLOCKED_NO_GO, D10 BLOCKED_FOR_PROMOTION, baseline approval missing, freeze ineligible, release authority NONE.
- A general instruction to continue toward a render is permission to continue engineering, not a substitute for exact policy adoption. No D renderer invocation or D MP4 until the existing AD packet and downstream gates explicitly permit it. Do not invent approval metadata or set flags by hand.

## Product and architecture constraints

Families: Challenge, Visual Loops, Visual Drills. Baseline scope 54 Challenges + 27 concrete Loop grammars + 20 Drill type/tier variants = 101 videos; smoke 18. Longform out of scope. Keep 008/009 blocked until the declared 11-second vs 12-second phase-sum conflict is explicitly resolved.

The target is one canonical production service used by both GUI and CLI: D request/catalog/profile resolution → effective editable editorial values → unchanged C generation/mechanics → D-owned presentation consumer → shared D3 audio with independent `music_seed` → delivery/mux/validation. This is the target architecture; do not claim it is wired until code proves it.

Do not create a sixth operational surface, `c11d-control` or `c11c-studio`. Keep the five existing surfaces. Do not mutate `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector`, `RenderedFrameStream`, game mechanics, gameplay RNG, structural RNG or protected C code just to make fields display. `winning_frame` is the temporal anchor; `close_calls` is episode count. Never serialize all `FrameSnapshot.custom_data`.

## Observed snapshot call graph

- `tools/qa/c11/run_c11c_challenge_bulk_qa.ps1` → `tools/prototypes/c11c_bulk/run_c11c_challenge_production.ps1` → Godot source capture and FFmpeg delivery.
- `c11c-suite/c11c-producer/main.py` `MainWindow._run_challenge_job` / `_run_content_job` uses the legacy C production runners. D tabs/request path is plan-only.
- `c11c-suite/c11c-producer/c11d_gui_request.py` builds D request/parity data.
- `tools/c11d/d9/universal_producer.py` / `universal_producer_cli.py` produce canonical D9.9 requests/plans.
- `editorial_render_bridge.py` produces a plan-only bridge record; `d_render_adapter.py` produces a `PLANNING_ONLY_NOT_RENDERABLE` envelope and must remain non-dispatching until its contract is legitimately changed.
- D3 audio exists as `tools/c11d/d3/c11d_music_engine_v5.py`; end-to-end D mux delivery remains to be proved.

## Work method

1. Verify pins in active checkout. Do not extract a snapshot over the checkout or overwrite different bytes.
2. Generate the live doc catalogue with `tools/c11d/documentation/organize_c11d_documentation.ps1`; it indexes without moving source documents. Read only current controls and contracts relevant to the discovered call graph.
3. Inspect C runners without launching them; map exact entrypoints, command arguments, output roots and acceptance signals. Inspect `c11c-suite/c11c-test/BUILD_MANIFEST.json` and applicable GUI contracts.
4. Trace D9.9 → D9.10 → request-scoped binding/materialization → payload/frame program/logical composition → actual compositor → D3 audio/mux. Check real implementation hashes and current receipts. Do not clone an existing binder or build another generic audit phase.
5. Propose/implement the smallest D-only slice that passes allowed focused unit/static tests. It must demonstrate a value-to-frame path at source level and preserve seed/mechanics/provenance invariants. Do not claim actual render/visual proof without a real, authorized artifact.
6. Only after AD and downstream gates permit execution: produce one isolated MP4 per family, inspect ffprobe streams, audio/loudness, frames and editorial A/B changes; then scale to smoke 18 and matrix 101. Keep output roots unique.
7. Each run must preserve command, runtime versions, real exit code, stdout/stderr files and hashes, source pins, output path/hash, review result and gate status. Keep contract, harness, physical MP4, visual/editorial A/V and overall acceptance statuses distinct.

## Rules against wasted work

Do not repeat AD's 60 tests while relevant source hashes are unchanged. Do not rerun broad C QA as a diagnostic default. Do not re-review the 107-candidate authority corpus without a concrete new source. Do not create documentation-only engineering phases. Do not mutate governance booleans or fabricate sign-off. Document existing gate blockage exactly and continue permitted engineering instead of claiming success.

## Acceptance target

C11-D is promoted only after all required independent gates, visible D editorial consumption, shared service parity across GUI/CLI, seed determinism/isolation, real A/V integration, family matrix acceptance, operator GUI evidence, and formal D freeze/promotion decisions pass. Until then C11-C 2.19.12 remains authoritative and immutable.
