# E4B Loop Editorial Composition Review — V5

## Current proposal identity

`definitions/c11d/production/C11E_E4B_LOOP_EDITORIAL_COMPOSITION_PROPOSAL_V1.json` SHA-256 `9e206704665ea85226ecc10854be9f679c32fe9ed7efb690a829f6e8456d43da`; status `PROPOSED_NOT_APPROVED_NOT_RENDERER_INPUT`. All approval gates remain false, including Loop field mapping, composition, renderer-native input, renderer activation, production dispatch, media creation and D4.8.

## Candidate outer layout only

- Canvas 720×1280, 9:16.
- Candidate top band y=0..192 (192 px).
- Original C11-C frame contained in x=108, y=192, width=504, height=896 (uniform scale 0.7 from 720×1280); no crop, no non-uniform stretch, no resampling claim.
- Candidate bottom band y=1088..1280 (192 px).
- Title/subtitle candidate HEADER; CTA candidate FOOTER; language metadata only. Four canonical editorial values remain present; `UNKNOWN`/empty handling follows approved D9.8 contract, not UI field omission.

Candidate line/font limits and exact layout are proposal data only. Static geometry tests (17/17) verify arithmetic/bounds/contain semantics; they do not verify Godot shaping, glyph fallback, font availability, actual raster wrapping, legibility or occlusion. The candidate composition is not renderer input and has no operator approval.

## Decision dependencies

Approval requires exact current hashes for shared regions A.1, Loop/Drill windows A.3 and this composition proposal. The historic D renderer packet V1 contains stale A.3/B.1/D.1 pins and cannot record approval against the new hashes. A new versioned decision record must state operator decision and exact fingerprint per policy. No D-only consumer patch before A.1/A.3/composition decisions and family binding scope review.

## Protected visual source

The full C11-C source frame, identity/grammar labels, metrics, palette, cycles, Matrix transitions and native layout remain intact. Editorial bands are outside the original source frame; no C11-C layer/binder/prototype edit is permitted.
