# C10-B — Visual Authoring Reproducibility & Determinism

## Scope

Product-authoring layer only. No changes to C6-F0.8 runtime, generators, RNG stream implementation, renderers, Movie Maker or build_factory.

## Suite

`tests/C10BDeterminismTest.gd`

## Assertions

1. Identity determinism 9/9: same request + same context -> exact identical Content Envelope V2.
2. Seed injection isolation 9/9: changing only external seed changes only envelope `seed`; non-seed authoring data remains identical.
3. Tier-4 propagation 9/9: resolver output must exactly match the declarative subtype policy and be propagated through the correct payload branch; external seed remains unchanged.
4. Input immutability 9/9: request and assembly context are unchanged after generation.

## Execution

```powershell
godot --headless --path . -s .\tests\C10BDeterminismTest.gd
```

Expected terminal marker:

`[C10B_VISUAL_AUTHORING_DETERMINISM_SUITE] PASS — C10-B 9/9`
