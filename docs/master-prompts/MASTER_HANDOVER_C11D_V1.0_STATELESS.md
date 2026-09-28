# MASTER HANDOVER — Challenge Engine V1.0 STATELESS — D

## Baseline authority

The source baseline for D is the repository state frozen as **C11-C 2.18.x**. The C freeze document is:

`docs/current/c11c/C11-C_2.18.x_FROZEN_CURRENT_STATE.md`

Do not silently reconstruct D from older C11-C checkpoints when this frozen repository is available. Historical material under `docs/history/` is evidence, not current instruction.

## D mission

Advance `ChallengeEngineV01_STATELESS` toward a productized, highly traceable deterministic video challenger system without reopening the established engine semantics unnecessarily.

## Non-negotiable boundaries

Do not modify C11-B simulation truth, RNG ownership, `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector`, `RenderedFrameStream`, C7 contracts, C9 Challenge semantics or historical fixture behavior without an explicit D checkpoint that names the reopened contract.

Presentation, production and asset systems may evolve around those boundaries.

## First D objectives

1. Recover the nine historical Challenge definitions and assets into dossiers.
2. Establish Challenge visual parity with the C11-C visual system.
3. Define the Atari-2600-inspired Challenge asset-family/template contract.
4. Define versioned platform layout profiles for Header / Body / Footer / CTA / safe areas across supported social destinations.
4. Define a normalized declarative production request and provenance model.
5. Define the D seed registry and anti-reuse policy.
6. Create the roadmap-driven procedural music V5 design before implementation.

## Challenge visual direction

The target is not to rewrite mechanics. It is to bind the existing mechanic outputs to a consistent C11-C composition/editorial system and then apply the selected retro asset family.

## Challenge asset system

Use semantic slots and versioned families so compatible assets can be exchanged across Challenges without embedding family-specific graphics into mechanic code. Record provenance and hashes.

## Music

The next audio system should be richer than C11-C while remaining deterministic and mathematically driven. Design layered instrument/timbre, rhythm, harmony, motif and texture parameters before coding. Avoid hidden coupling to gameplay timing.

## Platform layouts and personalization

Production must be able to select a versioned platform layout profile (Header / Body / Footer / CTA / safe areas) independently from content and mechanics. Every production request should also be able to select palette, asset family, typography, text template, audio profile, delivery profile and seed. Store the exact request and its hash.

## Seed traceability

D should maintain USED/RESERVED/INVALIDATED/HISTORICAL seed states and reject known-used seeds by default. Deliberate reuse requires an explicit operator action and an auditable reason.

## Artifact architecture

D should move toward a clean separation of products, reviews, tests, logs, scratch and indexes. Migration must be staged and never destroy historical evidence.

## Suite

`c11c-suite` is the operator shell. Any new test/script/function must be exposed through the appropriate Suite GUI and direct console launcher.

## First context deliverables

Do not start by adding a new mechanic. The first D window should produce: a verified baseline inventory, nine Challenge recovery dossiers, the Challenge visual parity contract, the asset-family schema proposal, the production-request schema proposal, and the D0/D1 focused tests.
