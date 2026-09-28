# C11-C 2.19.6 — Test / Repair Candidate

This revision consolidates the 2.19.x repair line and addresses the latest workstation failure.

## Defect

Fresh isolated worker projects did not inherit `.godot`, and therefore lacked Godot's generated global script class cache. `UnifiedSocialFrame.gd` could not resolve `PresentationProfile`; Movie Maker still emitted gray/empty frames.

## Fix

Before concurrent capture, each worker runs a one-time headless editor bootstrap and verifies `.godot/global_script_class_cache.cfg` plus `PresentationProfile`.

## Concurrency

Only worker initialization is sequential. The capture pool remains concurrent with `Workers=7`, no mutex and required `MAX_OBSERVED_CONCURRENCY > 1`.

## Status

**FINAL REPAIR CANDIDATE — NOT FROZEN.** Runtime verification on Windows/Godot 4.7.1 is required.
