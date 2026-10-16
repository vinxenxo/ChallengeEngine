# C11-D renderer path — ordered closeout gate map (2026-10-16)

This map is the operational sequence toward a controlled first D-only render and final branch closure. It does not authorize any stage. A gate is closed only when its canonical contract, execution evidence, lineage and authority explicitly say so.

## A. Preserve source and governance

- Keep C11-C 2.19.12 and its frozen manifest byte-identical; expected manifest SHA-256 is `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.
- Implement new behavior in D-owned components only. Do not alter simulation truth, RNG, `SimulationResult`, `winning_frame` (sole temporal anchor), `close_calls` (episode count, not timing), frozen geometry or C11-C renderer logic.
- Keep existing C11-C suite surfaces only: `c11c-test`, `c11c-producer`, `c11c-catalog`, `c11c-config`, `c11c-maintenance`. Do not introduce `c11d-control` as a substitute.
- Keep D9.10 `PREPARE_ONLY`, renderer OFF, candidate input inadmissible, no media, D4.8 blocked and release authority NONE until explicitly authorized.

## B. Close complete deterministic request identity and seed domains

1. Retain the passed seed-collision regression: reject absent, invalid, implicit, zero/out-of-range and equal-numeric cross-domain seed inputs before Godot.
2. Expand cross-type runtime matrices beyond `parking_v2/CHALLENGE_004` and `harmonic_membrane`; do not claim all selectors/families from two representatives.
3. Cover every supported canonical Challenge selector and each supported Visual Loop family/subfamily/grammar, and separately retain the existing Visual Drill type/tier matrix.
4. For each selector, prove baseline repeat identity, gameplay-seed sensitivity, music-seed orthogonality, independent repeats, canonical binding/source pins and clean negative rejection. Keep non-seed request identity fixed while varying one domain at a time.
5. Resolve default/automatic seed and arbitrary-request behavior explicitly. Until approved and proven, defaults/automatic derivation remain disabled and `master_seed` remains not adopted.
6. The expected scope must be read from canonical registries/contracts rather than a hard-coded count guessed in a launcher. Any source/selector inventory change must be source-pinned and regression-tested.

**Exit condition:** coverage includes every admitted canonical selector and explicit excluded/invalid forms fail closed; a report must not label seed domains complete while the matrix excludes supported inputs.

## C. Close candidate identity, lineage and payload instance

1. Reconcile the 164-source identity inventory and 54-pin candidate I/O contract/gap audit against the active checkout.
2. Extend request-bound manifests from representative selectors to the full admitted catalogue. Verify exact content type, family, subtype/tier, selector/variant, profile, seed domains, request binding, and payload/visual-state identity survive planning, D9.10 preparation and the in-memory payload binder.
3. Keep cross-chain contracts independently versioned; do not weaken existing pinned V1/V2 contracts in place to fit a new selector.
4. Prove deterministic independent repetitions and fail-closed stale/missing/mutated lineage. No source fixture or mock-only pass substitutes for a real Godot runtime where required.

**Exit condition:** all supported candidate inputs have complete identity, source lineage and in-memory payload identity without creating renderer-native input or dispatching.

## D. Resolve editorial consumption, presentation and delivery semantics

1. Obtain an explicit policy decision before turning any policy proposal into behavior: editorial value/window/visibility, semantic region/coordinate projection, timebase/timeline and audio/music delivery. Review proposals as proposals until approved.
2. Prove every approved editorial value reaches the visual payload and intended presentation target. Current assessment was 0/14 visual editorial sidecar values consumed; do not report this as closed without new evidence.
3. Preserve shared editorial/presentation behavior across content types by default; family exceptions must be explicit and tested. GUI/CLI must use the same canonical D contracts and preserve deterministic results.
4. Preserve logical frame 540×960 (header 0–144, body 144–816, footer 816–960) and the 720×1280 / 30 FPS delivery target only where required canonical policy says so. Use the established coordinate mapper/projection rather than inventing new geometry.
5. Resolve timeline/temporal policy against existing contracts; `winning_frame` remains the sole temporal anchor and `close_calls` is never used as timing.
6. Resolve technical audio/music delivery and prove visual payload orthogonality to `music_seed`. Do not copy music seed into gameplay/randomness.

**Exit condition:** every I/O group required for candidate input is complete or has a formally accepted, explicitly scoped exclusion. No silent assumptions for geometry, time, visibility or audio.

## E. Close D-only renderer candidate and candidate I/O admission

1. Use a renderer-agnostic D candidate architecture consuming only the proven D request/payload and approved presentation/delivery data.
2. Keep implementation isolated from C11-C and maintain a read-only/preparation boundary during development. No dispatch from D9.10, no hidden activation and no persisted production request before authorization.
3. Resolve the 10-group audit from its last known `0 complete / 6 partial / 4 blocked` status. Refresh the exact report and source pins after every upstream contract changes.
4. Have an independent reviewer verify deterministic output, source lineage, no cross-domain seed leakage, strict schema/report integrity and the complete input contract before seeking any render authorization.

**Exit condition:** baseline preparation is complete and independently reviewed; the renderer's supported input surface is explicit and fail-closed.

## F. Controlled render qualification — not production

A real candidate render is permitted only after the D-only candidate and exact input contract have passed prerequisite review and an explicit D4.8/test-run authorization allows that isolated test. The authorized test should be minimal and reversible: known selector/input/seed, known frame/timebase, explicit output sandbox, no C11-C mutation, independent repeat, file/media inspection, and captured exit code/log/hash. Its status must be identified as a qualification artifact, not a release.

Do not call a static parameter-mapping probe a render. Do not call renderer-off payload/materialization evidence a render. Do not claim a rendered artifact was created when `media_created=false` or when no output file exists.

## G. Final acceptance, freeze and cutover

After the authorized candidate render succeeds, close its visual/audio/technical QA findings, reproducibility and packaging. Then complete the canonical gates in their dependency order:

- D9.14 real-media / production qualification (scope and criteria from the canonical runbook).
- D9.16 full acceptance with all required evidence and no unresolved blocker.
- D9.17 closure adjudication; no-go remains until explicitly accepted.
- D10 final reconciliation, formal renderer baseline approval and freeze eligibility.
- Explicit operator/authority sign-off for D baseline promotion and cutover.

A successful subtest is never a substitute for a later gate. No stage can self-approve the baseline or set `release_authority` by writing a report. Only after the entire C11-D closure and the explicit cutover decision may D and its Producer replace C11-C as authoritative. C11-C stays available as the immutable reference throughout.

## Current gate snapshot

| Gate / fact | State at handover |
|---|---|
| Seed collision rejection regression | Operator-confirmed 7/7 PASS |
| Cross-type runtime audit | Operator-confirmed 12/12 receipts PASS; 2 selectors only |
| Visual Drill seed audit | Separate prior operator-confirmed 20-selector / 120-invocation matrix |
| Seed domains complete for all candidate inputs | **False / open** |
| Candidate I/O groups | 0 complete / 6 partial / 4 blocked |
| Renderer | OFF |
| Renderer-native input / dispatch | Not admitted / not invoked |
| Media created by latest cross-type audit | false |
| D4.8 | BLOCKED |
| Baseline approval / freeze eligibility | MISSING / false |
| D9.14 / D9.16 | blocked |
| D9.17 / D10 | BLOCKED_NO_GO / blocked |
| Release authority | NONE |
