# C11-D — MASTER HANDOVER — D8.0 MEDIA QA + RELEASE PIPELINE

## 1. Exact entry baseline

Start from the immutable D7.5 source baseline stored in the project Library:

`ChallengeEngineV01_STATELESS_C11-D_7.5_V8_FROZEN_20261008_111052.zip`

SHA-256:

`396d9f4bfdbb44b4878acf06db8d6c1c385103c110de537a174632e93611cd1d`

This archive is the D8 source of truth. Do not resume from earlier D7 candidates, V5/V7/V8 repair overlays, or pre-freeze workspaces.

## 2. Immutable C11-C baseline

`ChallengeEngineV01_STATELESS_C11-C_2.19.12_FROZEN_20260930_175709.zip`

- ZIP SHA-256: `D85425CF18C5211C8497574F4FC66202D613EACC0EC14CD4E2FEF0B24F634A32`
- Tree SHA-256: `2D39B7B923B42CDC6647A4D25493B75023CDD19CEE18214BBDE1FDD295B8F256`
- Root `build_factory.py` SHA-256: `3DB8FBC21CF0C78430018424F83A9EED5B42DF34A3908BA152F6771F0679D2A3`

The C11-C layer is frozen and is not a D8 implementation target.

## 3. Completed C11-D state

### D0 — Baseline proof + Challenge recovery — PASS / CLOSED

- Re-established the frozen C11-C identity and repository baseline.
- Recovered the nine canonical definitions `CHALLENGE_001` … `CHALLENGE_009`.
- Historical intent/mismatch evidence was preserved rather than silently rewriting truth.

### D1 — Visual/editorial parity — PASS / CLOSED

- Challenge presentation follows the proven C11-C editorial/layout discipline.
- No challenge timing, mechanic truth or answer truth was rewritten.
- D1.5 platform-layout/template work is subordinate to D1, not a separate branch.

### D2 — Reusable asset families/templates — PASS / CLOSED

- Declarative C11-D asset-family contracts/registries are established.
- Asset selection is separated from mechanic implementation.
- Provenance and slot compatibility are explicit.

### D3 — Procedural Music V5 — PASS / CLOSED

- Shared deterministic Music Engine V5 is established.
- Gameplay/structural RNG remains isolated from music generation.
- Final D3.3 delivery QA target used -14 LUFS, true peak approximately -6.50 dBFS, mono, 48 kHz.
- `challenge_8bit_v1` is the D3 style-profile reference.
- No simulation truth, `winning_frame`, `close_calls` or C11-C runtime activation was changed.

### D4 — Production request/personalization/GUI-CLI parity — PASS / CLOSED

- Canonical production request and normalization contracts are established.
- GUI and CLI converge on the same canonical inputs/plans and reproducible identities.
- `seed` and `music_seed` are distinct fields.
- **D4.8 production activation remains BLOCKED.**
- D4 did not activate production, renderer or runtime authority.

### D5 — Artifact topology/provenance/lifecycle — PASS / CLOSED

- Audited 19,938 repository files.
- Governed graph: 75 logical identities, 79 physical locations, 11 lineage edges.
- 9 ORPHANED records remain inventoried.
- 12,304 global orphan candidates remain unmanaged because cleanup authority was deliberately not granted.
- Lifecycle policy separates production, review, test, log, scratch and index concerns without deleting historical evidence.

### D6 — Seed governance — PASS / CLOSED

Canonical seed authorities:

- gameplay — `GAMEPLAY` — `request.seed` — owner `c11d_production_request`
- music — `MUSIC` — `request.music_seed` — owner `d3_music_engine_v5`

Locks:

- cross-domain sharing: `FORBIDDEN`
- `master_seed`: `NOT_ADOPTED`
- runtime derivation: disabled
- automatic seed generation: disabled
- D6 evidence does not promote shared/global RNG observations into canonical authority.

### D7 — Nine-Challenge matrix + catalog — FROZEN

D7.0–D7.5 are PASS / CLOSED.

Canonical authorities:

- matrix: `CANONICAL_D7_1`
- catalog: `CANONICAL_D7_3`
- identity/provenance: `CANONICAL_D7_4`
- full acceptance: `CANONICAL_D7_5`

Coverage:

- 9 challenges
- 5 delivery profiles
- 2 modes
- 90 matrix rows
- 90 catalog items
- 90 core cases
- complete coverage
- deterministic rerun PASS
- mutation guard PASS
- D7 negative tests PASS

D7 is metadata/governance only. It does not authorize media production, renderer execution or release execution.

D7 governed-tree SHA at freeze:
`e28139195131b749df27e1bbdff7a4acea7ed94fd6e0ef2669ed73810942d9dd`

## 4. Governance that D8 inherits

These values are intentionally locked unless a future explicit authorization checkpoint changes them:

- gameplay seed authority = `request.seed`
- music seed authority = `request.music_seed`
- `master_seed=NOT_ADOPTED`
- runtime seed derivation = disabled
- automatic seed generation = disabled
- cross-domain seed sharing = `FORBIDDEN`
- D4.8 = `BLOCKED`
- runtime authority = `NONE`
- D7 production execution = `false`
- D7 renderer execution = `false`

Do not infer release authorization from the fact that D7 is frozen.

## 5. Protected invariants

Do not modify any of the following during ordinary D8 work:

- C11-C simulation mathematics;
- mechanic truth and authored answer semantics;
- RNG algorithm, stream ownership or structural RNG behavior;
- `SimulationResult`;
- `winning_frame` as the sole temporal anchor;
- `close_calls` as an episode count rather than timing control;
- `WinningFrameDetector`;
- `RenderedFrameStream`;
- C7 audio ownership/contracts;
- C9 authoring semantics;
- logical 540×960 composition geometry;
- proven C11-C presentation and production behavior.

If a D8 design appears to require one of these changes, stop and treat it as a separate authorization/checkpoint question.

## 6. D8 roadmap

D8 is intentionally staged:

1. **D8.0 — Media QA / execution-boundary inventory + canonical contract**
2. **D8.1 — ffprobe/media integrity**
3. **D8.2 — visual QA**
4. **D8.3 — audio QA integration**
5. **D8.4 — artifact eligibility / provenance-to-media**
6. **D8.5 — deterministic release manifest / staging policy**
7. **D8.6 — release dry-run + negative cases**
8. **D8.7 — full D8 acceptance + freeze**

## 7. D8.0 exact first objective

Do a read-only inventory of existing media QA and release-related tooling/evidence already present in the frozen repository.

The inventory must locate and classify, at minimum:

- ffmpeg/ffprobe helpers and version assumptions;
- media roots and lifecycle classes;
- MP4/WAV/other media evidence already produced by C11-C/D3/C11-C Producer;
- frame-rate, resolution, duration, codec/container and audio validation helpers;
- A/V synchronization checks;
- metadata/social sidecars and provenance records;
- D7 matrix/catalog identities available for linking to media;
- existing release/evidence paths and their actual authority;
- mutation guards and deterministic rerun patterns;
- any GUI/CLI surface that already exposes media QA or release actions.

Do not add release execution merely to discover what the existing tooling does.

## 8. Canonical D8.0 contract target

Before implementation of release execution, establish a deterministic contract specifying:

- authoritative inputs and media roots;
- accepted media formats and technical constraints;
- QA checks and severity semantics;
- canonical command paths and ownership;
- ffmpeg/ffprobe invocation and evidence capture;
- deterministic output/evidence layout;
- provenance linkage from D7 catalog/matrix identity to candidate media;
- mutation-guard scope;
- explicit production/release authorization boundaries;
- deterministic negative cases.

These are investigation targets, not pre-authorized implementation assumptions.

## 9. Operator/tooling rules

- PowerShell 5.1 compatibility remains mandatory.
- Prefer focused checks before expensive aggregate runs.
- Use `python -B` or `PYTHONDONTWRITEBYTECODE=1` where repository mutation guards are active.
- Keep evidence writes narrowly scoped.
- Never broaden a mutation guard to hide an unexpected worktree mutation.
- GUI and CLI remain co-equal operator surfaces over the same canonical backend commands.

## 10. Required reading order in the new window

1. `MASTER_HANDOVER_C11D_D7_FROZEN.md`
2. `START_PROMPT_C11D_D8.0.md`
3. `docs/current/d/D7_DOCUMENTATION_CLOSURE.md`
4. `docs/current/d/D8.0_ENTRY_BRIEF.md`
5. `docs/current/d/C11-D_ROADMAP_V1.0_STATELESS.md`
6. `docs/current/d/README.md`
7. relevant D7 contracts/receipts only when a D8 decision needs them

**First implementation decision: none yet. Inventory first.**
