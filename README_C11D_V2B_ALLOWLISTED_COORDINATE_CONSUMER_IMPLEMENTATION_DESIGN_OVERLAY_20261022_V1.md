# C11-D V2-B Allowlisted Coordinate Consumer Implementation Design Overlay V1

**Mode:** `ADD_ONLY`  
**Status:** `REVIEW_ONLY_DESIGN_PENDING_IMPLEMENTATION`  
**Implementation runtime executed:** no  
**Renderer:** `OFF`

## Payload

This overlay adds an implementation-design JSON, its closed schema, a stdlib-only static design/pin regression suite, a checkpoint, continuity checkpoint V20, start and master prompts V20, and this README. It does **not** include production consumer code.

The design pins the already-accepted consumer specification and operator-confirmed receipt (`1038/1038`, receipt SHA-256 `c52d3f5ca276beea0482eb1ab521d163e201023f818e9448f6f7279c306b2ef0`). It details exact allowlist and extraction rules and specifies a 261-case negative runtime matrix. The matrix is planned only; it has not run against an implementation.

## Critical semantic safeguards

- Only the exact pairs `CHALLENGE_003.target_x`, `CHALLENGE_005.target_position`, `CHALLENGE_006.target_position`, `CHALLENGE_007.target_position` are accepted.
- `CHALLENGE_008.active_selection` and `CHALLENGE_009.displayed_count` stay blocked.
- One `custom_data.get(allowlisted_key, sentinel)` lookup per source frame; no `has()` plus second read; no enumeration/copy/serialization/logging.
- Source frame sequence and ordinal remain authoritative; one valid output descriptor per source frame; no interpolation/extrapolation/resampling or `winning_frame` remapping.
- Atomic fail-closed behavior: any invalid sample rejects the entire track; no partial projected track.
- The output contract is a closed in-memory logical marker descriptor, not renderer-native input. No renderer nodes, asset loading, file writes, payload, or media.

## Active-checkout workflow

Apply and run the separate blocks provided with this overlay from `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`. The Windows checkout is authoritative. Keep C11-C immutable and do not advance to the consumer implementation until the design suite passes in that checkout.
