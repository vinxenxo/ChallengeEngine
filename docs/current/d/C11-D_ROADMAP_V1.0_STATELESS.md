# Challenge Engine V1.0 STATELESS — D Roadmap

## D0 — Baseline lock and migration map

Start from the **C11-C 2.18.x FROZEN** repository. Create a machine-readable inventory of current definitions, profiles, assets, manifests, generated products and seeds. No D work begins by modifying a frozen C contract.

## D1 — Challenge Visual Convergence

Bring the historical Challenge family onto the visual language proven by C11-C Visual Loops/Drills while preserving each Challenge's mechanics and native timing:

- common 540×960 logical composition and 720×1280/1080×1920 delivery strategy;
- unified editorial hierarchy;
- modernized typography and readable text rules;
- family-aware palette treatment;
- reusable CTA/header/footer treatment;
- deterministic presentation variation isolated from mechanic truth.

The first D deliverable should be a Challenge visual parity contract plus one representative Challenge pilot before propagation to all nine.

## D1.5 — Platform Layout Template System

Create versioned, declarative presentation-layout profiles so the same video content can target different platforms without embedding platform-specific composition logic into Challenges or Visual families.

The layout profile should be able to define, at minimum:

```text
layout_profile_id
platform
version
canvas / safe-area rules
header template
body template
footer template
CTA placement
text constraints
asset crop/fit rules
metadata / provenance
```

Initial targets should cover the project's social outputs (for example Instagram, Facebook and other supported vertical/social destinations), while keeping the logical content model independent of the platform. A production request selects the layout profile explicitly, and the selected profile is recorded in provenance.

This is presentation/delivery infrastructure only: it must not alter Challenge mechanics, deterministic authored truth or Visual Drill/Loop gameplay state.

## D2 — Challenge Asset Family / Template System

Create a declarative, versioned asset-family system for the Atari-2600-inspired Challenge aesthetic. Assets are selected through semantic slots rather than copied into mechanic implementations.

Proposed asset-family contract:

```text
asset_family_id
version
style_profile
palette_profile
compatible_mechanics[]
slots{}
variants[]
preview
source/provenance
hashes
````

A family such as a garage, space, sports or abstract retro set should be swappable across compatible mechanics without changing mechanics code.

## D3 — Procedural Music V5

Extend the C family-aware music work into a richer mathematical composition system:

- layered instruments/timbres;
- harmonic, rhythmic and textural layers;
- deterministic seed mapping;
- content-family and authored-parameter influence;
- controlled motif/repetition;
- loudness and mobile translation checks;
- complete audio provenance in manifests.

Audio must remain separated from gameplay event truth unless a dedicated future contract explicitly couples them.

## D4 — Video Personalization

Introduce a declarative production request that can select, per video:

- palette/colorway;
- Challenge asset family/template;
- typography family/font;
- editorial text/content;
- audio profile;
- delivery profile;
- platform layout profile;
- seed;
- individual versus batch mode.

The request becomes part of provenance and is hashed.

## D5 — Artifact, Folder and Provenance Normalization

Create a clean artifact topology that separates durable products from generated evidence and scratch material:

```text
artifacts/
  products/
  reviews/
  tests/
  logs/
  scratch/
  indexes/
```

Keep manifests beside products where appropriate, while batch/index manifests remain queryable. Add source/config hashes so a product can be reconstructed from recorded inputs.

## D6 — Seed Registry and Traceability

Introduce a persistent registry with states such as:

```text
USED
RESERVED
RELEASED
INVALIDATED
HISTORICAL
```

Default generation requests a new seed and rejects known-used seeds unless the operator explicitly enables a deliberate reuse override. Preserve seed lineage in production manifests and review batches.

## D7 — Challenge Production Matrix

Once D1–D6 are stable, run a controlled production matrix across all nine Challenges, asset families, visual presets, audio profiles and delivery targets. The matrix should become data-driven and queryable from `c11c-catalog`.

## D8 — Release / Media QA

Bring the historical C11-D final-export intent into the current architecture: metadata, physical media validation, audio/video technical QA, reproducible packaging and release evidence.

## D9 — Suite evolution

Use the proof-of-concept `c11c-suite` as the operator shell for D:

- Test: unified QA and diagnostics;
- Catalog: artifact/provenance browser;
- Maintenance: cleanup, archives and package generation;
- Config: declarative configuration editor;
- Producer: production orchestration;
- future dedicated Asset, Music and Seed Registry surfaces when their contracts justify separate GUIs.

## Sequencing rule

Do not implement new Challenge mechanics until the asset-family/template contract, Challenge visual parity baseline, provenance model and production request model are stable enough to prevent another generation of one-off pipelines.

## Historical continuity

This roadmap combines the frozen C post-roadmap's explicit **Video Challenger + Asset Recovery** next phase with the older production roadmap's **Final Export / Distribution** stages, and the older C6-G direction for production assets and reusable templates. The six-family mathematical taxonomy remains a design vocabulary, while themes/assets remain presentation/content classifications rather than new mechanics families.
