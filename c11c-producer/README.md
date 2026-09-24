# C11-C Producer 0.3.0

Standalone production dashboard built independently of `c11c-studio`.

Top-level video types are represented explicitly: `Challenges`, `Visual Loops`, `Visual Drills`. Only `Visual Loops` is enabled in this phase.

Visual Loop source of truth is the frozen C11-C 2.9.1 backend, especially `tools/prototypes/c11c_common/C11CVariationProfile.gd` and the canonical production launcher `tools/prototypes/c11c_bulk/run_c11c_production.ps1`.

The UI exposes the five canonical Visual Loop families and their grammar modes as subfamilies. Every variation field can be left `ALEATORIO` or set as a target. Fixed targets are solved by querying the real backend variation profile; the renderer is never overridden by the Producer.
