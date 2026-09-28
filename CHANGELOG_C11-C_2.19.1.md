# C11-C 2.19.1 — Producer Social Hook Schema Repair

- Fixed the single Visual Drill Producer failure caused by reading `authoring.json.content.hook`.
- The Producer now consumes the canonical `profiles/presentation/c11c_visual_hooks.json` hook bank and applies the same deterministic seed/family-offset selection rule as the proven review runner.
- Preserved the 2.19.0 temporary AVI Movie Maker capture route unchanged.
- No changes to simulation, RNG, runtime mechanics, timing truth, C11-B contracts, logical 540×960 geometry, audio ownership or delivery profile semantics.

## Verification

- C11-C Producer 0.9.7 self-test: PASS
- Producer GUI contract: PASS
- Dedicated Movie Capture contract: PASS
- Static 2.19.1 route assertions: PASS
- Windows/Godot 4.7.1 runtime: pending operator run
