# C11-E E4B Loop — Editorial Field Ownership Decision V1

**Disposition:** `HOLD_VISUAL_FIELD_MAPPING_UNAPPROVED`. This is a source-backed engineering decision for E4B; it does not change D9.8 canonical editorial fields or grant renderer authority.

## Canonical data ownership

D9.8 owns the human-authored Loop fields `title`, `subtitle`, `call_to_action`, `language`. C11-C owns generated family identity, grammar/math/metrics, technobabble, seed/duration/FPS/loop-cycle telemetry, palette/profile/family-music identity, family/version label and frame-indexed Matrix transitions. These data classes are distinct. Neither side may silently delete or overwrite the other.

## Why the current proposal cannot be applied

`definitions/c11d/production/D_RENDERER_LOOP_DRILL_EDITORIAL_FIELD_WINDOW_PROPOSAL_V1.json` (8,376 bytes / SHA `609a4d183aac07c2cbe1abaf41444160fdd137217faffbead3aef618320d57dc`) proposes `title`/`subtitle` in HEADER and `call_to_action` in FOOTER for the full `[0, frame_count)` span, with language as metadata. Its own approval flags state that Loop field mapping and field-window policy are not approved.

The C11-C layer already uses a three-line animated header and an up-to-three-line footer. All five family prototypes populate the two header source strings and all three footer source strings. The shared layer wraps and fits those combined values but does not expose an additional reserved D-only text lane. A full-span HEADER/FOOTER mapping would therefore replace or collide with C11-C content unless a separate coexistence design is proven. The D9.8 per-field max length is 160 characters, so simple string concatenation cannot be assumed to fit all families or all valid inputs.

## Binding decision

1. Preserve all C11-C-native header/footer strings and Matrix transitions byte-for-byte at the source/model boundary.
2. Do not map D title/subtitle/CTA directly to the current C11-C header/footer fields.
3. Do not infer that `UNKNOWN` means the field can be deleted. It remains a canonical D9.8 value with no visible text until a placement rule is approved.
4. Keep `language` as editorial metadata; do not render it as visible text absent a specific policy.
5. Do not add a parallel binder, additional producer, sixth module, or modify `C11CVisualEditorialLayer`, any family prototype scene, or `UnifiedSocialFrame`.
6. Before an adapter is implemented, prepare a D-owned composition contract that preserves every C-generated string and defines how D copy can coexist within proven capacity. It must state the overflow/wrapping policy at max D9.8 lengths, the Matrix timing/transition behavior, per-family identity invariants, and testable output geometry. A visual review is required after a bounded test render.

## Music boundary in the same E4B adapter

Loop audio remains C11-C `FAMILY_MUSIC_V4`, not D3 V5. Because current C11-C family runners pass a single `$Seed` to both visual and music generation, the D-owned orchestrator must call the visual runner silently with `request.seed`, then invoke the unchanged `C11CSafeAmbient.py` / `generate_c11c_family_music.py` with `request.music_seed` plus the unchanged family/profile/grammar/loop-cycle/duration inputs. Mux must stream-copy H.264. The generators themselves remain protected and unchanged.

## Reopen conditions

Only reopen this decision with a complete D-owned composition proposal that demonstrates non-loss of C11-C header/footer data and stable layout across all five families, including long but valid editorial values. Until then the visual editorials remain plan-only and E4B cannot claim field-to-pixels acceptance.
