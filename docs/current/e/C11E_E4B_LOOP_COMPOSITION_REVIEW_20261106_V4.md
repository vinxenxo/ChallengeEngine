# E4B Loop Editorial Composition Review — V4

## Proposal status

`C11E_E4B_LOOP_EDITORIAL_COMPOSITION_PROPOSAL_V1` remains `PROPOSED_NOT_APPROVED_NOT_RENDERER_INPUT`. The 17 static checks validate geometry and selected non-rendering rules only. The new 27-grammar D9.9/D9.10/E1 matrix does not evaluate the composition and does not authorize text drawing.

## Candidate geometry under review

Canvas 720x1280. Top/bottom bands 192px each. Contained, unmodified C11-C source view 504x896 at x=108,y=192, uniform scale 0.7. This arithmetic candidate does not prove actual typography, shaping, glyph coverage, clipping, localized wrapping, Matrix-transition readability, safe-area legibility or accessibility.

## Required review before approval

1. Confirm actual Loop target canvas against the registered delivery profile.
2. Validate 27 grammar/family source frames and all five family Matrix/header-footer states with no crop/occlusion.
3. Define actual font coverage, shaping, fallback, line height, max lines and fail-closed overflow behavior.
4. Validate Spanish and every supported locale; no character count may substitute for rendered glyph metrics.
5. Test static and animated transitions on high-density source frames and worst-case contrast.
6. Define `UNKNOWN`/empty behavior without dropping keys or painting sentinel text.
7. Obtain explicit approval of a versioned field-window/timing/layout policy before consumer code or renderer input.

## Protected source regions

Do not overlay D editorial on C11-C header/footer or modify `C11CVisualEditorialLayer`. Candidate bands must sit outside the full source frame. No renderer input/media from this proposal.
