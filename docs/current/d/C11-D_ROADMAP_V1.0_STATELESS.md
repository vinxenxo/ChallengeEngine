# Challenge Engine V1.0 STATELESS — C11-D Roadmap

**Current phase: D9 — Suite Integration/Evolution (ACTIVE).** D9.4 is a PASS checkpoint for real media, not final D9 closure. D10 remains BLOCKED.

**Frozen D7.5 source baseline:** `ChallengeEngineV01_STATELESS_C11-D_7.5_V8_FROZEN_20261008_111052.zip`  
**SHA-256:** `396d9f4bfdbb44b4878acf06db8d6c1c385103c110de537a174632e93611cd1d`

C11-D is an additive productization branch around immutable C11-C behavior. The existing five applications under `c11c-suite` are the only canonical GUI surfaces: **Test, Producer, Maintenance, Catalog and Config**. No sixth suite/control application is to be created. GUI and CLI remain co-equal clients of the same canonical backend.

## D0–D8 — PASS / CLOSED

- **D0:** baseline proof and recovery of the nine existing Challenges.
- **D1:** Challenge visual/editorial parity.
- **D2:** reusable asset families/templates and binding evidence.
- **D3:** deterministic Music Engine V5, isolated from gameplay RNG.
- **D4:** declarative Production Request, personalization, canonical plan, GUI/CLI parity. **D4.8 production activation remains BLOCKED.**
- **D5:** artifact topology, provenance and lifecycle.
- **D6:** independent gameplay/music seed governance. `master_seed=NOT_ADOPTED`; runtime derivation and automatic seed generation disabled; cross-domain sharing forbidden.
- **D7:** nine-Challenge matrix/catalog, five delivery profiles, two modes; FROZEN.
- **D8:** media QA/release control-plane acceptance. `PASS_NO_MEDIA`; no release authority is inferred.

## D9 — Suite integration/evolution (ACTIVE)

**D9 acceptance principle:** a branch capability is not integrated merely because its script/test passes. The matching existing GUI must expose it, call the canonical CLI/backend path, preserve inputs/provenance/results, surface job status/logs/errors, and provide reproducibility. Every suite update has a version bump, focused tests, cross-suite tests and Windows/GUI evidence.

### Checkpoint already earned

- **D9.1:** one real Challenge video, 540 frames.
- **D9.2:** audio-enabled A/V pilot, AAC 48 kHz stereo.
- **D9.3:** exact same-input WAV/MP4 repeatability and changed-music-seed negative.
- **D9.4:** PASS checkpoint for D9.1–D9.3. Does not close overall D9 or authorize D4.8/release execution.

### D9.x implementation and acceptance sequence

| Milestone | Existing surface / version target | Work and required tests | Status |
|---|---|---|---|
| **D9.5.1** | `c11c-producer` **0.10.0** | Additive D4 Production Request + D4.3 editorial personalization tab; exact D4.6/D4.5 plan parity; 90 core + 12 personalization + negative tests; preserve existing C11-C Producer flows and backend fingerprint. | Implemented in overlay; static + canonical adapter matrix PASS; Windows GUI interaction pending |
| **D9.5.2** | `c11c-producer` 0.10.x | Inspect/implement a contract-safe bridge between the request's editorial fields and actual Challenge media. Must not modify protected C11-C truth/geometry or silently bypass D4.8. Prove text is visible in actual MP4, with render manifests/hashes and QA. | Next |
| **D9.5.3** | `c11c-producer` 0.10.x | Windows GUI smoke: open app, create/edit/save request, inspect normalized request/plan, error/cancel paths, rerun from saved request. Existing C11-C workflows regression-tested. | Pending |
| **D9.6** | `c11c-catalog` target **0.2.0** | Add D5/D7/D8/D9 product and artifact records: Challenge, both seeds, delivery/presentation/personalization, hashes, manifest/provenance, media streams, eligibility/status and canonical reproduction command. Test with D9.1–D9.3 and future GUI products; missing/ambiguous provenance negatives. | Planned |
| **D9.7** | `c11c-config` target **0.2.0** | Governed access to D2 asset bindings, D3 Music V5 style/registry, D4 delivery/presentation/personalization profiles, D6 seed settings and request snapshots. Validate schemas, diff/hash, explicit save, backup/restore, invalid config and forbidden-seed negatives. No silent defaults or auto-seed. | Planned |
| **D9.8** | `c11c-maintenance` target **0.2.0** | Expose current D cleanup, repository organization, quarantine, docs consolidation, verification and freeze operations. Dry-run-first, allowlisted targets, immutable evidence, protected-root guard tests and failure recovery. No automatic destructive action. | Planned |
| **D9.9** | `c11c-test` target **0.2.0** | Add GUI-accessible D2–D9 canonical test commands: D4 planning/parity, D6 seed governance, D7 matrix/catalog, D8 ffprobe/visual/audio/eligibility negatives, D9 GUI/job lifecycle and E2E. Verify command registry targets, output, exit codes, cancel/failure behavior. | Planned |
| **D9.10** | `c11c-suite` shell target **0.1.5** | Update common shell/status routing only when required by the five suite integrations; expose app versions and environment/preflight status; verify start failure, child exit codes, cancellation and log capture. No sixth app. | Planned |
| **D9.11** | All five existing suites | Cross-suite lifecycle: Producer request/job → Catalog provenance → Test/QA receipts → Maintenance safe archive/cleanup → Config reproducibility. Check all surfaces read the same persisted records and do not create duplicate backend semantics. | Planned |
| **D9.12** | Windows GUI E2E | Create and run a real single-case Challenge through the current Producer GUI path; inspect MP4/A/V with ffprobe; prove personalization in media once D9.5.2 is ready; catalog the product; replay stored request/seeds and compare expected hashes; change music seed and check isolation. | Pending |
| **D9.13** | Five-suite acceptance | Run each upgraded suite's self-test and focused GUI tests, then the consolidated logical suite. Include bad request/config, missing tools, overwrite protection, cancellation, and protected-root mutation attempts. | Pending |
| **D9.14** | D9 closure | Consolidate contracts, per-suite version matrix, test receipts, acceptance report, changelog, master handover, start prompt and freeze/checkpoint manifest. Close D9 only when every preceding gate is PASS and GUI E2E evidence exists. | Pending |

**Version policy:** planned versions above are targets, not current versions. A suite's version is bumped only with its own implementation/tests and acceptance. At this checkpoint only `c11c-producer` has been advanced to 0.10.0; the Suite shell remains 0.1.4.

## D10 — New mechanics (BLOCKED)

D10 may start only after D9.14 PASS/CLOSED: all five existing suites updated, all new CLI capabilities represented in their GUI surfaces, stable GUI job lifecycle, successful Windows GUI real-media production/reproduction, and safety/negative acceptance. No new Challenge mechanic is authorized by D9.4 or D9.5.1.

## Global invariants

- C11-C 2.19.12 frozen behavior is immutable: simulation/mechanics/RNG, `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector`, `RenderedFrameStream`, C7/C9 contracts, logical 540×960 geometry, and proven C11-C presentation/production.
- `master_seed=NOT_ADOPTED`; gameplay seed is `request.seed`; music seed is `request.music_seed`; cross-domain sharing forbidden; automatic/runtime seed derivation disabled.
- D4.8 remains `BLOCKED` unless a separate explicit governance decision changes it.
- Runtime/renderer activation is false for D4 plan adapters; `runtime_authority=NONE`; `release_authority=NONE` for the D9.5.1 request tab.
- The old `c11c-studio` is retired and must not be revived; no sixth suite is to be introduced.
