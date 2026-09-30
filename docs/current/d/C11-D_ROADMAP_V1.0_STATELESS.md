# Challenge Engine V1.0 STATELESS — C11-D Roadmap

**Entry baseline:** sealed C11-C 2.19.12 archive + verified SHA-256.

D is an additive productization branch around an immutable C11-C baseline. GUI and command line are co-equal operator surfaces over the same canonical backend commands.

## D0 — Baseline proof + historical Challenge recovery

Verify the frozen archive/tree hashes, run the frozen checks, inventory source/profiles/assets/seed evidence and recover `CHALLENGE_001` … `CHALLENGE_009` into evidence dossiers.

**Gate:** reproducible inventory, nine dossiers, provenance locked, no engine change.

## D1 — Challenge visual/editorial parity

Apply the proven C11-C composition, typography, safe-area and editorial hierarchy to Challenges without changing Challenge timing, mechanics or answer truth.

**Gate:** visual-parity contract + one pilot + focused regression.

`D1.5_PLATFORM_LAYOUT_TEMPLATE_CONTRACT.md` is treated as a sub-checkpoint under D1, not a separate top-level branch.

## D2 — Reusable Atari-2600-inspired asset families/templates

Create declarative, versioned asset-family templates with semantic slots, style/palette metadata, compatible routes, provenance and hashes. Assets are swappable without duplicating mechanic code.

**Gate:** schema + registry + swap/provenance test.

## D3 — Procedural Music V5

Design before implementation. Add layered timbre/harmony/rhythm/motif/texture/spatial treatment while keeping deterministic generation decoupled from structural RNG and gameplay truth.

**Gate:** design contract + deterministic render comparison + loudness/mobile QA.

## D4 — Declarative production request + personalization

One canonical request selects Challenge/content, seed, asset family, palette, typography, copy, music profile, delivery profile and single/batch mode. Persist request hash and exact provenance.

**Gate:** request schema + GUI/CLI parity test + reproduction test.

## D5 — Provenance + artifact topology

Separate durable production, review, test, log, scratch and index areas. Record commands, hashes, inputs and manifests without deleting historical evidence.

**Gate:** topology contract + dry-run migration + safety tests.

## D6 — Seed registry + governance

Introduce explicit seed lifecycle states (`USED`, `RESERVED`, `RELEASED`, `INVALIDATED`, `HISTORICAL`) and reject known-used seeds by default. Deliberate reuse is auditable.

**Gate:** registry schema + collision/reuse tests + GUI/CLI parity.

## D7 — Nine-Challenge production matrix + catalog

Drive all nine Challenges from normalized visual, asset, music, seed, layout and delivery declarations. `c11c-catalog` provides queryable evidence.

**Gate:** controlled matrix + catalog indexes + deterministic rerun.

## D8 — Media QA + release pipeline

Build the Final Export layer around the frozen backend: technical media validation, metadata, A/V QA, reproducible packaging and release evidence.

**Gate:** release candidate + full media audit + hashes.

## D9 — Suite integration/evolution

Extend Test, Producer, Maintenance, Catalog and Config surfaces as contracts mature. GUI actions remain thin wrappers around direct CLI operations.

**Gate:** operator parity for every new capability; no GUI-only logic.

## D10 — New mechanics

Only after D1-D6 are stable, schedule new cognitive/Challenge mechanics. Every new mechanic gets authored truth, answer data, focused tests, explicit timing semantics and a checkpoint.

**Gate:** mechanic contract + focused regression + integration regression + rollback evidence.

## Approved sequence

`D0 → D1 → D2 → D3 → D4 → D5 → D6 → D7 → D8 → D9 → D10`

**Decision: APPROVED.** This ordering deliberately delays mechanic expansion until visual/content/production/provenance foundations are stable.
