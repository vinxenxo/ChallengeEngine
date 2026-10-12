# C11-D Shared Production Context GUI State Contract V1 — Checkpoint

Status: `PREPARE_ONLY_CANONICAL_UI_STATE_MAPPING_NO_GUI_SOURCE_MODIFICATION`.

This increment formalizes the future GUI's in-memory state shape and maps it to the existing canonical D9.9 request vocabulary. It is not a widget implementation and does not patch the current C11-C Producer GUI.

## Core contract

- The GUI state explicitly identifies content type, family, and exactly one subtype/grammar or variant selector.
- Production controls explicitly contain gameplay seed, music seed, delivery profile, presentation profile, variation index, audio enablement, and personalization enablement. Seeds are never generated implicitly.
- Editorial state separates profile selection from text overrides. Shared fields are title, subtitle, call to action and language metadata. `player_name` and `challenge_label` are Challenges-only.
- The mapper owns only UI-state structural validation and field mapping. Catalog identity, editorial resolution, profile identity and planning remain owned by D9.8/D9.9 and the shared context backend.
- The resulting canonical request declares origin `GUI`, is passed to the existing GUI adapter and must produce a record identical to the direct shared facade and CLI outputs.
- Unknown fields, Longform, ambiguous selectors, bad seed types, unsupported challenge-only fields for other types and disabled personalization carrying overrides are rejected.

## Verification

`tools/c11d/d9/test_shared_production_context_gui_state.py` exercises all three supported content types, API/CLI equality, input immutability, editorial isolation, ten fail-closed cases and source drift in a temporary mirror.

## Boundaries

`current_gui_connected=false`; no existing GUI source is changed. No persistence, renderer input, dispatch, media, or release authority is created. `renderer=OFF`, `media_created=false`, `D4.8=BLOCKED`, `release_authority=NONE`, D9.17 remains NO-GO, D10 remains blocked, and C11-C remains immutable.
