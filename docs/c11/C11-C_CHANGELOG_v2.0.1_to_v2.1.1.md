# C11-C Consolidation Changelog — v2.0.1 to v2.1.2

## v2.0.1 — Editorial/audio loop package

Introduced the five-family editorial system, factual header parameters, large user-facing hooks, midpoint Matrix/split-flap transition, compact footer telemetry, deterministic ambient prototype audio, `-NoSound`, social sidecars, and the initial 18-second / 540-frame baseline.

## v2.0.2 — Editorial animator hotfix

Resolved the preload/class-name ambiguity by consuming the editorial animator through an explicit script preload rather than relying on global class-registration order.

## v2.0.3 — Shader/cleaner hotfix

Corrected the Invisible Forces `C11C_TAU` symbol and repaired the first standalone cleaner parser issue.

## v2.0.4 — Editorial palette, single-MP4, social hardening

Restored palette-derived editorial colors and decorative rules, consolidated single-MP4 output, added temp-only silent intermediates, and hardened BOM-compatible social metadata parsing.

## v2.0.5 — Reset experiment + Fractal shader identifiers

Added explicit reset concepts and fixed undeclared Fractal Bloom shader uniforms. The automatic-reset review orchestration was later superseded.

## v2.0.6 — Last known-good presentation reference

Used as the rebase reference for the consolidated toolchain: mobile-vivid palette, safe ambient audio, social sidecars, 18-second loop baseline and 720×1280 delivery intent.

## v2.0.7–v2.1.0 — Superseded orchestration attempts

These releases attempted tool separation and production storage, but introduced PowerShell argument-binding and reset orchestration regressions and are not canonical.

## v2.1.2 — Consolidated architecture attempt

Established unversioned canonical commands, protected production storage, temporary Movie Maker resolution override and explicit cleanup separation. Subsequent runtime testing revealed remaining resolution and script-invocation issues.

## v2.1.2 — Consolidated repair

Rebased the actual implementation again on the v2.0.6 presentation code and closed the known issues:

- typed `clampf()` in `C11CColorBoost.gd` to avoid Godot warning-as-error Variant inference;
- typed/explicit PowerShell argument passing between all orchestrators;
- temporary Movie Maker override now covers viewport width/height and window overrides, ensuring the effective capture target is 720×1280 without editing frozen `project.godot`;
- each family launcher verifies the Godot log itself reports a 720×1280 Movie Maker capture before packaging;
- review launcher generates exactly five seeds × five families and filters review extraction to that exact seed batch;
- review/render commands perform no prototype cleanup;
- cleanup and reset remain separate explicit commands;
- production renders and validates before replacing an existing final product;
- production stores final MP4 plus logs, manifests and social metadata in the protected production tree;
- canonical PowerShell syntax validator targets current tools only;
- documentation and handover prompts were consolidated.

No C11-B engine or C7/C9 contract was intentionally modified.
