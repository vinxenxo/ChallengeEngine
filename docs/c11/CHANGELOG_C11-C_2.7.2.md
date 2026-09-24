# C11-C 2.7.2 — Visual Drill End CTA Contract-Test Lifecycle Hotfix

## Status
Hotfix over C11-C 2.7.1. Test-only correction; no presentation runtime or gameplay truth changes.

## Root cause
`C11CVisualDrillEndCTAContractTest.gd` instantiated `UnifiedSocialFrame` and immediately constructed `PresentationUI`. The frame's `@onready` mount-point references are not populated until its `_ready()` callback runs, so the test observed null roots and reported a cascading CTA failure.

## Fix
- Await one `process_frame` after adding `UnifiedSocialFrame` to the SceneTree before constructing `PresentationUI`.
- Await the shared-CTA test from `_initialize()` so the contract suite cannot finish before the asynchronous lifecycle check completes.
- Preserve strict failure handling and cleanup.

## Expected result
`C11CVisualDrillEndCTAContractTest.gd` must pass without `SCRIPT ERROR`, null-node errors, or resource leaks.
