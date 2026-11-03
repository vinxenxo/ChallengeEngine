# C11-E E4A — Challenge Editorial Presentation Policy V1 (Approved)

**Decision:** `APPROVED_BY_OPERATOR_FOR_CHALLENGE_SEMANTIC_MAPPING`  
**Date:** 2026-11-03  
**Approver evidence:** explicit user message `APROBAR POLICY V1`  
**Approved proposal SHA-256:** `a1151999003b890abedb5d3b73382d1861d8ef3a56b0768a10fe480cfa841405`  
**Approval JSON:** `definitions/c11d/production/C11E_E4A_CHALLENGE_EDITORIAL_PRESENTATION_POLICY_APPROVAL_V1.json`

## 1. Approved mappings

| D9.9 editorial field | Semantic region | Source timeline visibility | Disposition |
|---|---|---|---|
| `title` | `HEADER` | `HOOK` | visual text |
| `subtitle` | `HEADER` | `HOOK` | visual text |
| `player_name` | `CHALLENGE_OVERLAY` | `HOOK` + `GAME` | visual text |
| `challenge_label` | `CHALLENGE_OVERLAY` | `HOOK` + `GAME` | visual text |
| `call_to_action` | `FOOTER` | `CTA` | visual text |
| `language` | none | none | metadata only |

This accepts the semantic mapping and named source-phase policy from proposal V1. It does not assign coordinates or invent frame boundaries.

## 2. Binding rules

- Resolve effective values only through canonical D9.8 inheritance: `global → content_type → family → subtype → variant → production_override`.
- Omit null, empty or whitespace-only values. Do not substitute placeholders or reserved C11-C/phase fields.
- Resolve the named windows from the selected canonical Challenge's own source timeline. CHALLENGE_004's 900-frame/60-FPS HOOK/GAME/REVEAL/CTA sample is fixture evidence, not a reusable numeric schedule.
- Keep D9.9 fields distinct from Challenge phase-field identifiers `hook`, `reveal`, `cta`. `call_to_action`→`CTA` is an approved policy relationship, not an alias.
- Keep `language` metadata-only.
- Reject a field when its source phase is absent/ambiguous or its semantic region cannot be resolved from existing D1.5/profile/family authority. No coordinate guess.
- Preserve exact effective text/hash and source lineage. No editorial data in `SimulationResult`, `FrameSnapshot.custom_data`, telemetry, seed material or C11-C simulation truth.

## 3. Historical D/C implementation reuse

D1.1 already records Challenge visual/editorial mapping evidence, D1.7 passed its 9-selector declarative mapping and canonical inherited layout checks, and D1.5 establishes the 540×960 logical HEADER/BODY/FOOTER hierarchy. C11-C `ChallengePresentationBinder.gd`, `C11CVisualEditorialLayer.gd` and `VisualContentPlayer.gd` are frozen references and must not be modified.

The D V2B allowlisted coordinate consumer (277 runtime cases) and V2B source-composition chain (402 static/evidence checks, four Challenge fixtures, 1680 source frames and markers) are prior isolated logical/descriptor evidence. They are not pixel/render acceptance. Reuse their contracts and call boundary; do not repeat those suites merely to move forward.

## 4. Explicit render-test authorization

The user's current instruction to continue toward renders authorizes **isolated E4A test rendering**. It does not authorize production renderer activation, production dispatch or the real-media D9.14 path. The first render test must be test-only, write its outputs under a dedicated evidence directory, and have no production side effects.

`renderer=OFF` for production, `D9.10=PREPARE_ONLY`, `D4.8=BLOCKED`, `D9.14/D9.16=BLOCKED`, `D9.17=BLOCKED_NO_GO`, `D10=BLOCKED_FOR_PROMOTION`, `release_authority=NONE`, no freeze and no promotion.

## 5. Next engineering increment

Extend the existing D-only Challenge in-memory composition/allowlisted consumer path with the approved editorial values and policy identity; do not add a parallel binder or renderer. Then create an isolated Godot off-screen visual test using that same D path, asserting text is visible only in the approved region/window, expected pixels change, gameplay pixels/source-frame hashes remain unchanged, and unsupported/unresolved fields fail closed. Use a bounded A/B control before any audiovisual mux acceptance.
