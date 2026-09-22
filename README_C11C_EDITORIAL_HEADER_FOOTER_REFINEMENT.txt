C11-C EDITORIAL HEADER/FOOTER REFINEMENT
Target baseline: ChallengeEngineV01_C11-C2.1.4-LATEST-FREEZE

Scope:
- Applies the same editorial refinement to all five C11-C Visual Loop prototype renderers.
- Header labels are horizontally centered.
- Header line 1 max size: 18pt (was 16pt).
- Header line 2 max size: 20pt (was 18pt), with fit-to-width fallback.
- Header rule moves between line 1 and line 2.
- Header line 2 now uses the deterministic technobabble that previously occupied footer line 1.
- Matrix/airport-board scramble is applied independently to both header lines; stable copy does not change.
- Footer becomes 3 lines because its former line 1 is promoted to header line 2.
- Remaining footer telemetry is centered and increases from 9pt to 10pt.
- Authoring/manifest header metadata is updated so the social sidecar matches the rendered header.

Frozen boundaries not touched:
- simulation math
- RNG ownership/algorithms
- SimulationResult
- winning_frame / close_calls
- C7 audio contracts
- C9 authoring contracts
- C11-B logical frame geometry
- duration
- production architecture/toolchain

Apply from repository root:
  git apply .\C11-C_EDITORIAL_HEADER_FOOTER_REFINEMENT.patch

Recommended validation:
  python .\tests\run_all.py
  .\tools\prototypes\c11c_bulk\validate_c11c_powershell.ps1
  .\tools\prototypes\c11c_bulk\validate_c11c_delivery_configuration.ps1
  .\tools\prototypes\c11c_bulk\run_c11c_art_direction_review.ps1 -ResetReviewAssets

The last command is the physical 25-render review; use it to visually inspect the new editorial layout.
