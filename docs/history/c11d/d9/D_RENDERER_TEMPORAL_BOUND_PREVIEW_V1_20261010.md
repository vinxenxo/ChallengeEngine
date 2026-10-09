# D Renderer Temporal Bound Preview V1 — History (2026-10-10)

## Decision

Adds a read-only, D-owned temporal preview over one current Challenge, Visual Loop and Visual Drill timing source. This is the planned second stage after the topology-only proposal: it now emits concrete in-memory frame intervals from pinned canonical values, but not an executable schedule or renderer input.

## Verified source mapping in the prep tree

- `CHALLENGE_004`: explicit 60 FPS phase durations 3/7/3/2 seconds; 180/420/180/120 frames; total 900.
- `visual_loop_geometric_canonical`: 2 seconds, 30 FPS, 60 frames.
- `visual_drill_tracking_canonical`: 21 seconds, 30 FPS, 630 frames.

No C11-C source is edited. The output retains source SHA-256 values and the immutable C11-C manifest SHA-256. No simulation truth or telemetry participates.

## Test intent

The focused test rejects timing changes, altered frame boundaries, invented visual subphases, missing or changed source lineage, schema drift and all attempts to activate rendering, media creation, release authority or C11-C mutation. JSON Schema validation uses Draft 2020-12 when `jsonschema` is installed; structural/exact-output checks remain mandatory either way.

## Status at authoring

The test is run against the packaging/preparation tree before creating the overlay. Windows operator acceptance is pending. The preview remains unapproved and does not change `D4.8=BLOCKED`.
