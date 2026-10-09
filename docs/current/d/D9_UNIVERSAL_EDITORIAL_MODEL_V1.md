# C11-D D9 — Universal Editorial Model V1

## Purpose

The current D9.5.1 Producer GUI correctly exposes D4.3 editorial personalization for Challenge, but that scope is intentionally insufficient for final D9 completion.

The target is a **single declarative editorial model across the entire content system**, consumed by the existing `c11c-producer` and later materialized by the D renderer/production baseline.

## Content hierarchy

```text
CONTENT TYPE
  ├─ Challenge
  ├─ Visual Loop
  │    ├─ family
  │    └─ grammar / subtype / variant
  ├─ Visual Drill
  │    ├─ family
  │    └─ drill type / subtype / variant
  └─ Longform
       └─ family / variant where defined
```

The GUI selection flow is:

`Content type → family → subfamily/grammar/type → production variant → editorial profile`

## Editorial inheritance

```text
GLOBAL DEFAULT
      ↓
CONTENT-TYPE DEFAULT
      ↓
FAMILY DEFAULT
      ↓
SUBFAMILY / GRAMMAR DEFAULT
      ↓
INDIVIDUAL PRODUCTION OVERRIDE
```

A value may be inherited or explicitly overridden. The effective configuration must be shown to the operator before execution.

## Four data classes

### 1. Editorial — editable

Examples:

- title;
- subtitle/descriptor;
- CTA;
- language;
- player/name where applicable;
- challenge label;
- hook;
- preparation/final text;
- permitted header/footer lines;
- permitted editorial visibility flags.

### 2. Derived telemetry — not freely editable

Examples:

- seed values displayed as technical metadata;
- FPS;
- duration;
- frame count;
- palette/system identifiers;
- generated family statistics.

These remain derived from the actual request/render and cannot be replaced by editorial overrides.

### 3. Provenance — immutable lineage

Examples:

- request identity;
- plan hash;
- profile IDs;
- source revision;
- generator/tool identity;
- artifact/media SHA-256.

### 4. Simulation truth — immutable

Examples:

- mechanic semantics;
- `SimulationResult`;
- `winning_frame`;
- `close_calls`;
- gameplay RNG ownership;
- timing semantics.

## Existing C11-C editorial capabilities to reuse

The current C11-C implementation already provides reusable presentation/editorial binders for the visual families and drills. D9 must **wrap and normalize those existing surfaces**, not replace their simulation or presentation truth.

Visual Loops currently span five families:

1. Geometric Waves
2. Fractal Bloom
3. Sacred Symmetry
4. Living Particles
5. Invisible Forces

Visual Drills include the established attention/perception families and their existing presentation binders.

The GUI must expose the editable subset of each surface while preserving derived telemetry and protected simulation data.

## Determinism rules

Changing editorial values must not change:

- gameplay seed;
- music seed;
- gameplay RNG consumption;
- structural RNG consumption;
- `winning_frame`;
- `close_calls`;
- simulation result.

Changing `music_seed` must remain an audio-domain change only.

Changing editorial values must change the personalization/editorial identity and, once the D renderer bridge exists, the resulting media identity.

## Rendering rule

The current C11-C 2.19.12 renderer is frozen. D9 must not modify it solely to obtain early editorial rendering.

The final bridge is expected to exist in the next D frozen baseline, where:

`GUI → canonical request → personalization → production plan → D renderer → media → QA → catalog`

can be certified as one chain.

## Required GUI behavior

The Producer should always show:

- content type;
- family/subfamily/variant;
- effective editorial profile;
- effective editorial values;
- gameplay seed;
- music seed;
- delivery profile;
- presentation profile;
- audio state;
- production authority/state;
- plan identity;
- personalization identity.

The user should be able to preview the effective editorial configuration before production.

## Required negative cases

The GUI must block:

- unknown content type;
- unknown family/grammar/type;
- unsupported editorial field for the selected content;
- missing gameplay seed;
- missing music seed where audio is enabled/required;
- attempts to edit derived telemetry as if it were editorial;
- attempts to alter simulation truth;
- release execution without authority.


## D9.8 implementation record — 2026-10-09

Canonical source: `definitions/c11d/personalization/C11D_UNIVERSAL_EDITORIAL_MODEL_V1.json` (`C11-D-D9-UNIVERSAL-EDITORIAL-MODEL-V1`). The small backend resolver is `tools/c11d/d9/universal_editorial_model.py`; it reads the canonical model and the existing Producer inventory and returns selection/editorial resolution only. It does **not** build a D4 request, plan identity, production job, renderer input, or media.

### Inventory discovered from the current Producer contract

- Challenge: 9 declared IDs. Mechanic/family grouping is derived from the `mechanic` field; each Challenge ID is the current D4-compatible variant identity.
- Visual Loop: 5 declared families and 27 concrete grammars. The `auto` entry, when present, is classified as a selector mode, not counted as a concrete grammar.
- Visual Drill: 4 declared drill types and 20 explicit type/tier variants (five declared tiers per type in the current inventory).
- Longform: visible in the model as **disabled**. The current D4 request schema and Producer `video_types` do not define Longform as a producible content type. `LONGFORM_1080` is a delivery profile, not proof of a supported Longform request.

### Editorial fields and inheritance

V1 enables `title`, `subtitle`, `call_to_action`, and `language` across Challenge/Loop/Drill; `player_name` and `challenge_label` are Challenge-only. Values are trimmed, language is normalized to lowercase, optional empty/null values become `UNKNOWN`, and text is limited to 160 characters. Inheritance runs in this exact order: `global → content_type → family → subtype → variant → production_override`; the resolver rejects unknown layers, fields, unsupported scopes, reserved fields and overlong/non-string values. It does not persist or mutate profiles.

Editorial keys are structurally separated from derived telemetry (including seeds, FPS, duration, frames, palettes and difficulty tier), provenance/identity (request/plan/personalization hashes and artifact/media digests), and simulation truth (mechanics, target/speed/collision/timing, `winning_frame`, `close_calls`, simulation result and RNG ownership). Gameplay and music seed ownership remain `request.seed` and `request.music_seed`; `master_seed=NOT_ADOPTED`, cross-domain sharing is forbidden, and automatic/runtime derivation stays disabled.

### Integration and acceptance boundary

The shared Config surface now registers this contract read-only. The shared launcher is restricted to exactly the five canonical surfaces; the legacy `c11d-control` directory in the incoming ZIP is **not registered**. Its physical archive/removal is deferred to the Maintenance/quarantine workflow because the current freeze package manifest references it and must be reconciled deliberately.

At the D9.8 checkpoint, Loop/Drill were intentionally marked **not D4 request/plan compatible**. D9.9 subsequently adds a universal request identity and deterministic editorial-intent plan for those types, plus GUI/CLI process parity; only Challenge embeds an existing canonical D4 subordinate plan. Renderer activation, production execution and release authority remain disabled. D9.10 is the future bridge-planning checkpoint; physical editorial-to-media materialization remains deferred to the future D frozen baseline. C11-C 2.19.12 sources, simulation truth and renderer were not changed for this checkpoint.

Primary static test: `python tools/c11d/d9/test_universal_editorial_model.py`. It covers live inventory counts, inheritance/normalization, current request compatibility, protected data-class negatives, unsupported Longform and unchanged canonical source hashes. D9.8 is a closed model checkpoint; D9.9 is separately accepted for the plan-only scope recorded below. Neither implies D9 closure, Windows GUI acceptance, physical D renderer integration, or D10 authorization.


## D9.9 Producer universal coverage — acceptance record

D9.9 implements the universal GUI and CLI request/plan surface in the existing Producer 0.11.0. The canonical adapter is `tools/c11d/d9/universal_producer.py`, with CLI entrypoint `tools/c11d/d9/universal_producer_cli.py`; the GUI only collects inputs, calls the adapter and compares a separate canonical CLI result. The acceptance checkpoint is `docs/current/d/D9.9_PRODUCER_UNIVERSAL_COVERAGE_CHECKPOINT.md`. All 9 Challenge identities, 27 concrete Loop grammars (+ five `auto` family selectors), and 20 Drill tiers resolve. Three separate-process parity cases and 20 negative controls pass. Challenge delegates to D4; Loop/Drill output declarative editorial-intent plans only. Renderer, production execution and release authority stay disabled. The operator subsequently confirmed Windows GUI plan generation for all currently implemented D content types. This confirms D9.9 plan-only GUI smoke behavior, not the separate D9.10 bridge-output tab nor real-media certification; D9 remains OPEN. D9.10 bridge records also bind contract/model SHA-256 identity for auditable future renderer-binding work.


## D9.10 bridge record boundary

`definitions/c11d/production/C11D_EDITORIAL_RENDER_BRIDGE_D9_10_V1.json` specifies the downstream mapping of content identity, model-allowlisted editorial values, explicit independent seed domains, profile references and immutable provenance. `tools/c11d/d9/editorial_render_bridge.py` validates the D9.9 plan and emits a hashed `C11-D-D9.10-EDITORIAL-RENDER-BRIDGE-PLAN-V1` inspection record only. It is intentionally not an executable renderer input. The future D frozen baseline must separately define/version/hash the adapter, certify binders, receive explicit D4.8 authorization, test determinism/seed isolation and complete media QA/catalog reproduction gates before rendering can be activated.
