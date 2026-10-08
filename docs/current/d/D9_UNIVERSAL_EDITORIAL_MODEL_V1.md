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
