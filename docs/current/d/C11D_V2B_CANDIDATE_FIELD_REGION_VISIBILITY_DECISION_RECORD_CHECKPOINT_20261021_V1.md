# C11-D V2-B Candidate Field-Region Visibility Decision Record — Checkpoint V1 (2026-10-21)

## Verified predecessor

The active Windows checkout reported the field-region/visibility proposal tests **551/551**, with 4/4 candidates, 81/81 source pins, 9/9 authority-input pins, and 6/6 semantic decision-input pins. Stdout SHA-256: `dc6ecb960fc59852c4b3251a1146ef6425675c44be4cf03304d3fc0026942d27`; stderr was empty; canonical empty-stream SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`; receipt SHA-256: `87c8ab97db18a7531dc2df610b51fe819c8bf746b2b66475b544220c37c95cbb`.

The proposal itself remains immutable and its status remains `PROPOSED_NOT_APPROVED_OPERATOR_REVIEW_REQUIRED`. Its independent decision record accepts the four proposals only to advance to a future coordinate-policy specification.

## Decision recorded by this overlay

- `CHALLENGE_003.target_x`: accepted for future coordinate-policy specification only. It remains scalar X-only in `PILOT_0X100`; no Y, normalization, or actual placement is inferred.
- `CHALLENGE_005.target_position`: accepted for future coordinate-policy specification only. It remains a run-constant `Vector2` repeated in the source frames.
- `CHALLENGE_006.target_position`: accepted for future coordinate-policy specification only. It remains a per-source-frame target track separate from the catcher.
- `CHALLENGE_007.target_position`: accepted for future coordinate-policy specification only. It remains a per-source-frame target track separate from the scanner.
- `CHALLENGE_008.active_selection` and `CHALLENGE_009.displayed_count`: remain blocked by the prior semantic decision record. No challenge JSON is changed.

The current proposal is not edited. This new record authorizes authoring a separate coordinate-policy proposal; it does **not** approve actual coordinate transforms, visibility policy for rendering, asset sizing, field bindings, pixel placement, payload consumer, renderer, render test, media, release or promotion.

## Locks retained

`renderer=OFF`; no payload or media; candidate input inadmissible; approved bindings/projections zero; `D4.8=BLOCKED`; `D9.10=PREPARE_ONLY`; `D9.14/D9.16=BLOCKED`; `D9.17=BLOCKED_NO_GO`; `D10=BLOCKED_FOR_PROMOTION`; baseline approval missing; freeze ineligible; release authority none. C11-C manifest stays `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`. `winning_frame` remains the only Challenge temporal anchor; `close_calls` remains episode-count metadata only. Never serialize `FrameSnapshot.custom_data` as a whole.

## Next engineering gate

Prepare an explicit, still-unapproved coordinate-policy proposal for each accepted candidate. It must make the source-to-logical and logical-to-delivery mappings explicit, distinguish coordinate systems, preserve source frame timing/cardinality, and keep `CHALLENGE_003` unavailable for actual pixel placement unless the missing Y dimension is resolved by a separate explicit policy. Do not implement or invoke a payload consumer during that specification step.

## V2 correction after Windows regression

The first decision-record test run reported `652/653` at `CHECK_644` because the unaccepted V1 overlay encoded the empty-stderr SHA-256 incorrectly (62 hex characters, missing `bf`). The original 551/551 Windows receipt and stdout/stderr logs remain unchanged. V2 corrects the stderr digest in the decision record, test constant and manifest; it does not relax a check or alter the decision matrix.
