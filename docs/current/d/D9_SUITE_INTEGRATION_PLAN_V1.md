# C11-D D9 — Suite Integration Plan V1

## Purpose

D9 integrates the D0–D8 capabilities into the five existing GUIs and updates/tests each surface. It is not only a test-suite expansion. A branch capability is complete only when the canonical CLI/backend remains usable directly and the matching GUI invokes the same authority with equivalent inputs, provenance, state, errors and reproducible output.

## Canonical suite topology — no new suite

| Existing application | D branch responsibilities to integrate | Required proof |
|---|---|---|
| `c11c-producer` | D3 music choice, D4 request/personalization/plan, D6 independent seeds, D7 product context, D8 QA hooks and D9 job lifecycle. Existing C11-C production routes remain intact. | request/plan parity, explicit seeds, rendered media checks, error/cancel, replay and personalization-visible-in-media test |
| `c11c-catalog` | D5 provenance/topology, D7 matrix/catalog identity, D8 media metadata/eligibility, D9 producer job references and replay command | known D9.1–D9.3 artifacts resolve to correct seeds/profiles/hashes; missing/mismatched manifest negatives |
| `c11c-config` | D2 asset family bindings, D3 style registry, D4 delivery/presentation/personalization profiles, D6 governed seed policy and snapshots | schema validity, before/after diff/hash, backup/restore, invalid/unknown-field rejection and seed-isolation checks |
| `c11c-maintenance` | D5 artifact lifecycle, D8 quarantine/staging/cleanup/freeze checks, docs and repository organization | dry-run, allowlist enforcement, protected roots unchanged, quarantine restore and failed-operation evidence |
| `c11c-test` | D2–D9 validations, D4 parity, D6 seed, D7 matrix, D8 media QA and D9 GUI E2E command registry | every registered command path exists; logs/exit codes/cancel/failure shown; real GUI test jobs run and return receipts |
| `c11c-suite` existing shell | route/version display, process lifecycle and common logging only where needed | all five current apps launch; no orphaned process on cancel; failed launch/exit shown; no sixth app |

## Version/update gates

Version numbers for future targets below are planned, not active until the suite's implementation and tests pass.

| D9.x | Surface | Planned version | Gate |
|---|---|---|---|
| D9.5.1 | Producer | **0.10.0** | D4 request and personalization inputs; D4.6/D4.5 parity; 90 core + 12 personalization + 4 negatives; preserve old Producer/backend fingerprint |
| D9.5.2 | Producer | 0.10.x | Contract-safe text-to-media path discovered/implemented without changing protected C11-C truth or silently bypassing D4.8; real MP4 contains proved text changes |
| D9.5.3 | Producer | 0.10.x | Windows GUI interaction, request save/reload/reproduction, job/log/error/cancel smoke |
| D9.6 | Catalog | **0.2.0** | D5/D7/D8/D9 product identity, lineage, seeds, personalization, media stream metadata, hashes and reproduction |
| D9.7 | Config | **0.2.0** | D2/D3/D4/D6 registries/profiles, validated edits/snapshots/backups and invalid-config negatives |
| D9.8 | Maintenance | **0.2.0** | D5/D8/D9 dry-run, quarantine, cleanup, repository/docs organization and freeze surfaces; protected-root negatives |
| D9.9 | Test | **0.2.0** | D2–D9 test command registration, GUI-triggered execution, output/exit/error/cancel states and GUI E2E entrypoints |
| D9.10 | Existing Suite shell | **0.1.5** | surface version/preflight, shared launch/process status/log behavior only if required; all five apps stay canonical |
| D9.11 | Cross-suite | no new app | producer → catalog → test → maintenance/config provenance/replay/lifecycle integration |
| D9.12 | Windows GUI E2E | — | real video/A-V from GUI, ffprobe/visual/audio QA, catalog record, reproducibility and changed-seed control |
| D9.13 | All suites | — | full version matrix, all focused self-tests, GUI/CLI parity and safety negatives |
| D9.14 | D9 close | — | docs/prompts/changelog, receipts, freeze/acceptance package, handover; only then D9 CLOSED |

## D9.5.1 current implementation boundary

Producer 0.10.0 adds a tab to the existing Producer GUI; no `c11d-control` suite and no `c11c-studio`. It collects Challenge, mode, gameplay seed, independent music seed, delivery/presentation profile, variation, audio choice and D4.3 text fields. It calls `tools/c11d/d4/gui_production_adapter.py` and compares against `tools/c11d/d4/production_cli.py`; D4 remains the normalization/personalization/plan authority. Successful runs persist a request, canonical request, personalization, plan, parity and receipt under `artifacts/tests/c11d_d9/producer_gui/<request_id>/`.

D9.5.1 does **not** render a video. D4.8 remains BLOCKED, `renderer_activation=false`, `production_execution=false`, `runtime_authority=NONE`, `release_authority=NONE`. The request form's editorial fields are not claimed to affect actual pixels yet. D9.5.2 must close that gap under an explicit safe integration design before final acceptance claims personalized media.

## Real GUI acceptance contract

The real Windows acceptance will not stop at “the app opened” or “self-test passed”. It must include:

1. Launch the existing `c11c-suite` and open each updated surface.
2. Create/edit a request from Producer; validate request, resolved personalization, plan hash and GUI/CLI parity.
3. Through the authorized existing GUI production route, render a single Challenge with fixed gameplay and music seeds; do not activate D4.8 unless its own policy gate is explicitly changed.
4. Verify MP4 streams/dimensions/FPS/frames/duration, audio codec/rate/channels, visual QA and audio QA.
5. Confirm Catalog discovers the media and provenance; Config can show/validate the profiles and exact text request; Test can invoke acceptance; Maintenance dry-run leaves protected products unchanged.
6. Replay the same saved request and verify the correct deterministic identities; change only `music_seed` and prove gameplay seed remains fixed and audio/media identities change as designed.
7. Run negative request/config, overwrite protection, absent dependency, process error and cancellation checks.
8. Archive receipts/logs and rerun consolidated suite acceptance.

## Freeze boundaries

No changes to protected C11-C simulation/mechanics/RNG, `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector`, `RenderedFrameStream`, C7/C9 contracts, logical 540×960 geometry or proven C11-C production behavior. Do not auto-generate seeds. Do not merge gameplay/music seed streams. Do not create a sixth suite. D10 remains BLOCKED.
