# C11-E E2 V7 — JSON float seed validation failure (V1)

**Run:** `C11E-E2-CH001-AB-20261031-V7` on 2026-10-31, branch `main`, HEAD `b92434d6a8b50cef7e49ba6b75a4813777927fe7`, parent `a3c7c5d284a96ce115ca52208b4039002502753b`.

## Evidence

Failure ZIP `C11E_E2_CH001_AB_FAILURE_EVIDENCE_20261031_191440_13012eef.zip`, 29,568 bytes, 47 entries, SHA-256 `27fa769c35165e8171120bc0fce16fc3739505198157a874360c2de432c6bbe7`; CRC check clean. `C11E_E2_FAILURE_DIAGNOSTIC.json` records exception `godot_render_A failed with exit code 40`, renderer invoked true, invocation count 1, media-created true, one recorded AVI path, media accepted false, release authority NONE.

Pair tests: 9/9 PASS. Python preparation and tool version probes exit 0. Godot 4.7.1 Mono enters Movie Maker, writes a partial AVI and reports a single frame before stderr says `[C11E_E2] Editorial sidecar contract validation failed.` at `C11EChallenge001E2.gd:62`. The source AVI fragment is 12,374 bytes. B was not rendered. No final MP4, success receipt, pixel A/B proof or human review exists.

## Exact root cause

The sidecar includes integer-valued seed JSON tokens `193847` and `840001`. The GDScript validator used `typeof(value) == TYPE_INT`. Godot JSON parsing produces `TYPE_FLOAT` for JSON numeric tokens, so both seed-type checks returned false. The surrounding sidecar predicates (schema, family, title, visual slot, boundary, source pins, seed domains, and bounds) match the contract. This is an E validator type-assumption defect.

## Corrective requirement

Accept only `TYPE_INT` or `TYPE_FLOAT`, then require finite, positive, integral values within the request's permitted range `1..2147483646`. Reject decimal floats, strings, booleans, zero, negatives and overflow. Run a Godot-native headless regression of the actual parser + predicate before E2 physical rendering.

## Disposition

V7 is FAILED and remains immutable. Do not reinterpret the partial AVI as an accepted render. V8 package is designed to apply the type fix and add the preflight regression. E2 remains blocked until a valid two-run A/B package and independent visual review pass.
