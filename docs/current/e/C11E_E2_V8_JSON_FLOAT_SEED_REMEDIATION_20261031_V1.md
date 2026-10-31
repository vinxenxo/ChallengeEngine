# C11-E E2 V8 — JSON float seed contract correction

## V7 failure established

V7 pair tests passed 9/9 and pair preparation succeeded. Godot 4.7.1 Mono entered `godot_render_A`, then the E2 sidecar validator at `C11EChallenge001E2.gd:62` returned false (exit 40). Failure ZIP SHA-256 `27fa769c35165e8171120bc0fce16fc3739505198157a874360c2de432c6bbe7` (29,568 bytes / 47 entries). The failure record proves one renderer invocation and one partial AVI path, with `media_accepted=false`; no B render or success receipt.

## Root cause

Godot's `JSON.parse_string()` converts JSON numeric tokens into `TYPE_FLOAT`. The V7 validator incorrectly required `TYPE_INT` for gameplay and music seed values. The actual sidecar integers were valid, but their parsed Variant type did not meet that incorrect assertion.

## V8 code changes

- Add `is_positive_integral_seed(value: Variant)` to the E-owned E2 GDScript. Accept `TYPE_INT` or `TYPE_FLOAT` only when finite, positive, exactly integral and no greater than 2,147,483,646.
- Validate both `seed_domains.gameplay.value` and `seed_domains.music.value` using that function. Do not allow numeric strings, booleans, fractional values or out-of-range values.
- Add a Godot-native headless test that JSON-round-trips a complete valid E2 sidecar, asserts both parsed seed values are `TYPE_FLOAT`, invokes the actual `_validate_c11e_sidecar()` path, and proves both seed domains reject invalid values.
- Pin the new GDScript and test in the V8 runner. Execute the Godot numeric-contract preflight before Python pair preparation and physical rendering; require marker `C11E_E2_GODOT_JSON_NUMERIC_CONTRACT=PASS`.
- The E2 retry uses fresh RequestId `C11E-E2-CH001-AB-20261031-V8`. V7 output/evidence is never overwritten.

## Installation and execution

Installer exact identity is `main` / HEAD `b92434d6a8b50cef7e49ba6b75a4813777927fe7`, parent `a3c7c5d284a96ce115ca52208b4039002502753b`, tree `91aa803c2d675ec9fc7afff120b2bc7d3de479ef`, as captured in the supplied 2026-10-31 19:17:27 Europe/Madrid snapshot. It requires the V7 V2 APPLIED receipt, V7 failure archive and exact V7 source postimages. It modifies only E2-owned files and E documentation/root instructions; no C mechanics, C11-C manifest or D governance lock is changed. It invokes no renderer/media.

After APPLIED and full receipt/postimage verification, the operator may locally commit. Then run E2 V8 on the same `main`; its runtime validation accepts verified descendants of E0/E1 only with exact source pins. If the Godot numeric test fails, the physical renderer is not invoked. If the physical A/B fails, keep its failure receipt and stop. E2 acceptance still needs both outputs, FFprobe, body/title/header pixel proofs, provenance and human visual review. E3 remains blocked.
