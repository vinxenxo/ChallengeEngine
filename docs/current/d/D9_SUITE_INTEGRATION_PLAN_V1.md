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
| D9.5.2 | Producer / future frozen D GUI | 0.10.x | Connect D4.3 editorial fields to the definitive D renderer after C11-D production freeze; never modify the frozen C11-C renderer to force the new D fields into media | DEFERRED by operator architecture decision |
| D9.5.3 | Producer | 0.10.x | Windows request/plan smoke and existing C11-C production regression; job/log/error/cancel evidence in D9.12 | D request/plan GUI reported working; full E2E pending |
| D9.6 | Catalog | **0.2.0** | D7 intents, D9.4 hash-verified pilots, D9.5.1 plans and provenance/replay; path/hash/parity negatives | PASS: user confirms Windows GUI works |
| D9.7 | Config | **0.2.0** | Read-only D2–D9 registries; operator profile schema; explicit independent seeds; validate/hash/diff/save/backup/validated restore; invalid/unknown-field/seed/path negatives | Overlay prepared; isolated tests PASS; Windows GUI acceptance pending |
| D9.8 | Maintenance | **0.2.0** | D5/D8/D9 dry-run, quarantine, cleanup, repository/docs organization and freeze surfaces; protected-root negatives |
| D9.9 | Test | **0.2.0** | D2–D9 test command registration, GUI-triggered execution, output/exit/error/cancel states and GUI E2E entrypoints |
| D9.10 | Existing Suite shell | **0.1.5** | surface version/preflight, shared launch/process status/log behavior only if required; all five apps stay canonical |
| D9.11 | Cross-suite | no new app | producer → catalog → test → maintenance/config provenance/replay/lifecycle integration |
| D9.12 | Windows GUI E2E | — | Produce a real fixed-seed video/A-V through the existing Producer C11-C GUI route; ffprobe/media QA; Catalog provenance; Config profile/hash; replay + changed-music-seed control; overwrite/error/cancel negatives. D request tab remains plan-only until the future frozen D GUI. | Pending |
| D9.13 | All suites | — | full version matrix, all focused self-tests, GUI/CLI parity and safety negatives |
| D9.14 | D9 close | — | docs/prompts/changelog, receipts, freeze/acceptance package, handover; only then D9 CLOSED |

## D9.5.1 current implementation boundary

Producer 0.10.0 adds a tab to the existing Producer GUI; no `c11d-control` suite and no `c11c-studio`. It collects Challenge, mode, gameplay seed, independent music seed, delivery/presentation profile, variation, audio choice and D4.3 text fields. It calls `tools/c11d/d4/gui_production_adapter.py` and compares against `tools/c11d/d4/production_cli.py`; D4 remains the normalization/personalization/plan authority. Successful runs persist a request, canonical request, personalization, plan, parity and receipt under `artifacts/tests/c11d_d9/producer_gui/<request_id>/`.

D9.5.1 does **not** render a video. D4.8 remains BLOCKED, `renderer_activation=false`, `production_execution=false`, `runtime_authority=NONE`, `release_authority=NONE`. By operator decision, editorial-field-to-renderer integration is deferred to the definitive GUI after the C11-D production baseline freezes; the frozen C11-C renderer must not be modified to force D request fields into pixels.

## Real GUI acceptance contract

The real Windows acceptance will not stop at “the app opened” or “self-test passed”. It must include:

1. Launch the existing `c11c-suite` and open each updated surface.
2. Create/edit a request from Producer; validate request, resolved personalization, plan hash and GUI/CLI parity.
3. Through the existing Producer C11-C GUI production route, render one Challenge with fixed gameplay/music seeds. The D request tab remains plan-only during the frozen C11-C phase; do not activate D4.8 or alter the C11-C renderer.
4. Verify MP4 streams/dimensions/FPS/frames/duration, audio codec/rate/channels, visual QA and audio QA.
5. Confirm Catalog discovers media/provenance; Config validates and saves an operator profile with explicit independent seeds and a stable hash; Test invokes acceptance; Maintenance dry-run leaves protected products unchanged.
6. Replay the same saved request and verify the correct deterministic identities; change only `music_seed` and prove gameplay seed remains fixed and audio/media identities change as designed.
7. Run negative request/config, overwrite protection, absent dependency, process error and cancellation checks.
8. Archive receipts/logs and rerun consolidated suite acceptance.

## Freeze boundaries

No changes to protected C11-C simulation/mechanics/RNG, `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector`, `RenderedFrameStream`, C7/C9 contracts, logical 540×960 geometry or proven C11-C production behavior. Do not auto-generate seeds. Do not merge gameplay/music seed streams. Do not create a sixth suite. D10 remains BLOCKED.

## D9.6 implementation checkpoint — Catalog 0.2.0 (PASS)

The existing `c11c-catalog` keeps its generic artifact browser and adds the `C11-D PRODUCTS / PROVENANCE` tab. D7 intents and D9.5.1 plans remain non-release products; D9.4 media remains `VALIDATED_PILOT / NOT_REGISTERED_FOR_D8_RELEASE`. Hash/size checks, project-root path confinement and request/plan/parity checks are enforced. The operator confirmed that Catalog's Windows GUI works. Renderer and release authority remain NONE.

## D9.7 implementation checkpoint — Config 0.2.0 (Windows acceptance pending)

The existing `c11c-config` keeps Repository Config and adds `C11-D CONTRACTS` plus `C11-D OPERATOR PROFILES`. Twenty D2–D9 canonical JSON contracts are read-only and inspected with status/SHA-256/governance invariants. Profiles live under `profiles/c11d/operator/`, require explicit independent integer `seed` and `music_seed`, known Challenge/delivery/music/personalization IDs, schema validation, SHA-256/diff, explicit save, backup and validated restore. Blank profiles carry no operational defaults.

The generic Repository Config editor protects all profile paths and `challenges/`, `definitions/`, `schemas/`, `assets/`, `core/`, `tools/`, `tests/` and `c11c-suite/`. Only the dedicated Operator Profiles tab can write allowlisted operator JSON. Pure-data tests cover 20/20 contracts, seven negative controls and save/backup/validated-restore lifecycle. Isolated tests pass; Windows Qt and real filesystem interaction remain pending. Profiles do not auto-feed Producer, and D4.8/runtime/renderer/production/release authority remain disabled.
