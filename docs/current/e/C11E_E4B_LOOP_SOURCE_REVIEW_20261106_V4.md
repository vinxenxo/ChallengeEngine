# E4B Loop Source Review — V4

## Active family surface

Five C11-C Loop families, 27 grammars (5/5/5/5/7). Their five prototype scenes already mount `C11CVisualEditorialLayer`; their native header/footer/Matrix contain family identity, grammar/math, metrics, palette, seed, duration/FPS/loop count and music/version information. Preserve these surfaces and all C11-C source pins.

## D9/E1 boundary

D9.9 GUI populates `production_override` with exactly four Loop fields: `title`, `subtitle`, `call_to_action`, `language`. D9.8 resolves all four. E1 records those fields as `NOT_CONSUMED_E1`, family adapter `c11e_visual_loops_adapter=NOT_CONNECTED_E1`, required gate E4, and existing C11-C family music route. This is intentional while the D consumer is unimplemented.

## Prior D renderer checkpoint

`D_RENDERER_VISUAL_LOOP_COMPOSITE_PAYLOAD_INTEGRATION_CHECKPOINT_V1` is prepare-only. It proved one-selector composite planning but did not define a renderer-side editorial consumer or field-to-region/visibility policy. Do not infer the missing consumer exists.

## Protected integration

Implement the future consumer only at the existing D-owned boundary. No new Producer, no sixth module, no parallel binder and no edits to C11-C `C11CVisualEditorialLayer`, family scenes, binders, timelines, Matrix, RNG or music generator. Keep full source frame intact; D framing must sit outside it.

Future orchestration: silent visual uses `request.seed`; existing family music generator uses `request.music_seed`; preserve family, profile, grammar, cycles and duration; mux AAC onto H.264 by stream-copy. D3 V5 is not the Loop music engine.

## Current state

Static proposal tests 17/17 and populated GUI plan-only PASS. CLI V1's mojibake prevents populated parity acceptance. V2 runner replays GUI UTF-8 to both D9.9 and E1 CLI; no GUI rerun required. No rendering/media authorized.
