# E4B Loop Editorial Composition Review — V3

## Proposal status

`C11E_E4B_LOOP_EDITORIAL_COMPOSITION_PROPOSAL_V1` remains `PROPOSED_NOT_APPROVED_NOT_RENDERER_INPUT`. The 17 static tests validate arithmetic and selected non-rendering constraints only. They do not prove Godot shaping, font coverage, clipping, localization wrapping, actual social safe-area legibility, accessibility or user acceptance.

## Candidate geometry under review

Canvas 720x1280. Top/bottom bands 192px each. Contained, unmodified C11-C source view 504x896 at x=108,y=192, uniform scale 0.7. This geometric arrangement avoids cropping the source frame. It does not by itself prove the C11-C frame remains legible at 0.7 scale or that 192px bands can carry all text in supported languages.

## Required review before approval

1. Confirm whether `REVIEW_720` is the correct actual target canvas for Loop and derive all safe area margins from the registered delivery profile rather than hard-coded assumptions.
2. Validate source viewport across all 27 grammars and five family compositions; no crop/occlusion or altered aspect ratio.
3. Define typography by actual installed font assets, glyph fallback, shaping, line-height, max lines and overflow fail-closed behavior.
4. Validate Spanish and every supported language; do not infer that one accent fixture proves coverage.
5. Establish character limits based on rendered glyph metrics, not a generic character count alone.
6. Test title/subtitle/CTA on both static frames and worst-case Matrix transitions and busy backgrounds.
7. Define behavior for `UNKNOWN`/empty values without dropping keys or accidentally painting sentinel text.
8. Obtain explicit acceptance of a versioned policy before implementation. Until then, no renderer input/media.

## Protected source regions

Do not place D editorial over C11-C header/footer or modify `C11CVisualEditorialLayer`. Candidate bands must sit outside the complete source frame. No new binder or producer.
