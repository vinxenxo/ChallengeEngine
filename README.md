# C10-A — Visual Authoring Contract

Status: DESIGN / INTEGRATION PACKAGE — NOT CERTIFIED

## Intent

This package defines the product-authoring boundary for the two visual domains:

- `visual_loop`
- `visual_drill`

It does not modify any C6-F0.8 runtime, generator, RNG registry, renderer, binder, or Movie Maker code.

## Contract

`VisualAuthoringRequest` contains product intent only:

- `authoring_version`
- `domain_family`
- `subtype`
- `duration_seconds`
- `fps`
- `difficulty_tier` 1..5
- `custom_parameters`

Seed and infrastructure metadata are intentionally externalized into `VisualAuthoringAssemblyContext`.

## Difficulty resolution

`VisualDifficultyResolver` is pure and deterministic. It applies:

1. base parameters
2. tier parameters
3. controlled custom overrides

Unknown/custom keys fail closed. RNG-level fields are not exposed through the request contract.

## Canonical output

The generator emits the existing Content Envelope V2 shape with:

- `schema_version=2.0`
- `kind=visual_loop|visual_drill`
- exact `subtype`
- externally supplied `seed`
- `rng_version=2.0`
- explicit presentation/assets/audio/provenance metadata
- domain-specific `payload`

No new runtime contract is introduced.

## Certification

The test suite must be executed in the real project with Godot 4.7.1. Passing this package statically or by inspection is not certification.

The expected command is:

```powershell
godot --headless --path . -s .\tests\C10AVisualAuthoringPipelineTest.gd
```

Before execution, the test's sample `presentation`, `assets`, and `audio` identifiers must be aligned with the exact production registries present in the authoritative ZIP. The current package intentionally uses explicit placeholders rather than silently inventing production defaults.
