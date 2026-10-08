# MASTER HANDOVER — C11-D D8.5

Continue from D8.4 PASS/CLOSED.

Authorities:
- D7.1 matrix = `CANONICAL_D7_1`
- D7.3 catalog = `CANONICAL_D7_3`
- D7.4 identity/provenance = `CANONICAL_D7_4`
- D8 media scope = `EXPLICIT_REGISTRY_ONLY`

D8.5 purpose:
`explicit media registry -> deterministic manifest preview -> staging decision`

Never:
- infer candidates from filesystem discovery;
- treat historical media as release candidates;
- create a release product while release authority is NONE;
- copy/move/transcode/mux/render/encode physical media;
- modify C11-C or D7 authorities/evidence.

A non-empty registry with `release_authority=NONE` must be blocked, not staged.
