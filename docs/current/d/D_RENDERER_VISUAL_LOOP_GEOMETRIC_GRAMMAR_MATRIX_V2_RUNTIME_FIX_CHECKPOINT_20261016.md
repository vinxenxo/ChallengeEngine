# D Renderer Visual Loop Geometric Grammar Matrix V2 Runtime Validator Fix — 2026-10-16

## Observed Windows failure

The operator executed the V2 Python audit and received the exact Godot version `4.7.1.stable.mono.official.a13da4feb`. Godot launched the headless probe and failed at `probe_visual_loop_geometric_grammar_matrix_v2.gd`, `_validate_input()`, while comparing one deserialized grammar-row Dictionary to the GDScript literal mapping. The error was `Grammar matrix differs from the exact five-entry mapping`.

This is not consistent with a missing/wrong executable path: the configured executable ran and emitted the expected version and a GDScript stack trace. The confirmed failure point is JSON-decoded matrix validation. A plausible cause is numeric representation normalization for JSON numbers; the original message did not print field-level differences, so the exact differing Variant type/value was not directly captured. The bounded correction avoids recursive Dictionary equality and checks exact keys plus each field explicitly. The numeric index must be finite and numerically equal to the pinned value.

## Changes

- Probe validation is now key-set and field based; no matrix row is accepted based only on a casted/truncated index.
- The source-lineage pin for the GDScript probe is updated in the contract.
- A regression test rejects reintroduction of recursive Dictionary comparison and checks the explicit field-level validation.
- C11-C sources and manifest are unchanged; the Python runner/receipt/gates are unchanged.

## Verification boundary

The overlay is source- and contract-testable in isolation. The real Godot runtime must be rerun from the active Windows checkout after installation. No claim is made that the runtime fix passes until the Python process exits 0 and prints the exact PASS receipt and expected 20/20 case/repeat and 12/12 source-pin markers.

## Governance remains locked

`PREPARATION_ONLY_GEOMETRIC_GRAMMAR_PARAMETER_MATRIX_NOT_CANONICAL_REQUEST_BINDING_NOT_RENDERER_INPUT`; renderer OFF; no media; D4.8 blocked; release authority NONE; D9.17 `BLOCKED_NO_GO`; D9.10 `PREPARE_ONLY`; D10 blocked for promotion.
