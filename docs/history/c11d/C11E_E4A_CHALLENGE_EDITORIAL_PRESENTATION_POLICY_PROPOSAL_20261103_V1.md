# C11-E E4A — Challenge Editorial Presentation Policy Proposal V1

**Status:** `PROPOSED_NOT_APPROVED`  
**Scope:** Challenge only; initial technical fixture `CHALLENGE_004`. This proposal does not authorize renderer input, visual payload mutation, dispatch, media or release.

## 1. Decision requested

Approve or amend a D-owned policy defining how the five enabled Challenge D9.9 visual text fields map into existing semantic regions and Challenge source-timeline intervals. `language` remains metadata-only. No field is mapped to a reserved C11-C/Challenge phase field, and no geometry is invented here.

## 2. Evidence boundary

The Gate A evidence proves canonical values and hashes can be carried in a sidecar (14/14 field instances) but the current visual payload consumes 0/14. The Challenge `CHALLENGE_004` in-memory source-timebase preview is deterministic (2/2), has 3/3 assets and 420/420 game frames at 60 FPS, but coordinate projection and delivery resampling remain unresolved. This is not proof of editorial pixels.

The Challenge fixture timeline contains named intervals `HOOK`, `GAME`, `REVEAL`, `CTA`. For CHALLENGE_004 the current fixture reports 900 total source frames at 60 FPS: HOOK 0–180, GAME 180–600, REVEAL 600–780, CTA 780–900. These frame numbers are fixture evidence only; the proposed policy refers to named intervals, never hard-coded frame numbers or delivery-frame indices.

## 3. Recommended field policy — approval required

| D9.9 field | Proposed semantic region | Proposed source-timeline visibility | Kind |
|---|---|---|---|
| `title` | `HEADER` | `HOOK` | Visual text |
| `subtitle` | `HEADER` | `HOOK` | Visual text |
| `player_name` | `CHALLENGE_OVERLAY` | `HOOK` + `GAME` | Visual text |
| `challenge_label` | `CHALLENGE_OVERLAY` | `HOOK` + `GAME` | Visual text |
| `call_to_action` | `FOOTER` | `CTA` | Visual text |
| `language` | None | None | Metadata only |

This is a D policy proposal, not a claim that these mappings already exist. `CHALLENGE_OVERLAY` is a semantic role only. Its rectangle, typography, z-order and clipping rules must be derived from the existing D1.5/profile/family hierarchy and resolved by a separately pinned layout contract. If that authority cannot resolve the region for a given profile/family, reject the visual binding rather than guessing coordinates.

## 4. Namespace and timeline rules

- D9.9 text fields are exactly `title`, `subtitle`, `call_to_action`, `player_name`, `challenge_label`; `language` is instruction metadata.
- The Challenge phase-field names `hook`, `reveal`, `cta` are a separate namespace. The proposed `call_to_action`→`CTA` timing relationship is an explicit D policy mapping to a named timeline segment, not an alias of the `cta` phase field or any C11-C field.
- Resolve named phase boundaries from each selected canonical Challenge timeline in its source timebase. Do not copy CHALLENGE_004's numeric boundaries to other variants. If a required phase is absent, malformed or ambiguous, fail closed for the affected field.
- Delivery resampling to 30 FPS and output 720×1280 occur downstream; they must not redefine source visibility intervals. Coordinate projection/timebase policies remain separately governed.

## 5. Empty values, inheritance and safety

- A null/empty/whitespace-only effective value is omitted from the D visual composition; do not display placeholders and do not fall back to `hook`, `reveal`, `cta`, `preparation_text`, `final_text`, header/footer reserved fields or `show_*` flags.
- Effective values continue to resolve through canonical D9.8 inheritance: `global → content_type → family → subtype → variant → production_override`. The visual consumer must not implement a second inheritance engine.
- Preserve the exact effective text bytes/value hash and source lineage. Reject unknown fields, unsupported profile/family mappings, stale source/policy hashes, missing approval and text/hash mismatch.
- Never put editorial data into `SimulationResult`, `FrameSnapshot.custom_data`, telemetry, seed material or C11-C simulation truth. Never change `winning_frame` or `close_calls` semantics.

## 6. Implementation after approval

After a separate explicit, versioned, hash-bound approval record:
1. Extend the existing D-only in-memory Challenge visual payload/composition route; do not create a parallel binder/renderer/producer.
2. Carry each field's name, exact value/hash, region ID, named phase interval, policy hash and lineage into the payload-side visual binding.
3. Add deterministic positive/negative tests for correct field routing, empty fields, missing phases, unresolved geometry, missing/stale approval, wrong namespace, stale source pins, identity drift and no simulation/payload-source mutation.
4. Prove layout, visibility, clipping and actual pixel effect on the existing Challenge consumer before any physical audiovisual acceptance.

## 7. Operator decision

Proposed status remains `PROPOSED_NOT_APPROVED`. No implementation may treat this document or a test PASS as approval. Record acceptance/rejection in a separate immutable decision artifact with approver, timestamp, policy SHA-256, scope and any amended rows.
