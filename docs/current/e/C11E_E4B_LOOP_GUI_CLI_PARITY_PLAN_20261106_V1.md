# C11-E E4B Visual Loop — GUI/CLI Plan Parity Plan V1

**Purpose:** Prove the existing Producer GUI and CLI resolve the same canonical D9.9 Visual Loop request, E1 intent, editorial plan, bridge and D-only adapter envelope. This is a single plan-only request. It is not a render, music, media, runtime/Godot, or production test.

## Preconditions

- E4A is closed `PASS_TEST_ONLY`.
- D99 V2 is installed; `c11c-suite/c11c-producer/main.py` SHA is `4141072659f307468900c1cfb09774479abc6c10abae6ae638a11192cfcd04e6`.
- Use the existing Producer started by `c11c-suite\c11c-producer\run.bat`; do not create another Producer or runner.
- No other project change is needed for this plan-only run.

## Exact GUI fixture

Open `C11-D · EDITORIAL UNIVERSAL (D9.9)` and set:

| GUI field | Value |
|---|---|
| Content Type | Visual Loop (`visual_loops`) |
| Family / mechanic | Geometric Waves (`c11c_geometric_waves_v1`) |
| Grammar / subtype | `harmonic_membrane` |
| Variant / tier | No native variant (disabled / not applicable) |
| Mode | REVIEW · PLAN (`REVIEW`) |
| Gameplay seed | `314159` |
| Music seed | `840001` |
| Delivery profile | `REVIEW_720` |
| Presentation profile | `social_default_v1` |
| Variation index | `0` |
| Audio enabled | ON (planning metadata only; no audio generation) |
| Editorial personalization | ON |
| Edit scope | Global |
| Title | Blank |
| Subtitle | Blank |
| CTA | Blank |
| Language | `es` |

Do not attempt to fill `player_name` or `challenge_label`; they are Challenge-only and not canonical Loop keys. There is no Hook/countdown field. Do not add `presentation_options`.

Click only `RESOLVER + PLAN EDITORIAL / PUENTE (SIN RENDER)` once.

## Expected canonical values

- Selection: `content_type=visual_loops`, `family_id=c11c_geometric_waves_v1`, `subtype_id=harmonic_membrane`.
- Exactly four canonical Loop editorial keys: `title=UNKNOWN`, `subtitle=UNKNOWN`, `call_to_action=UNKNOWN`, `language=es`.
- `request.seed=314159` and `request.music_seed=840001` remain separate fields and separate seed domains.
- Music contract: `PROTECTED_FAMILY_NOT_REWIRED` / `PRESERVE_EXISTING_C11C_FAMILY_MUSIC_PATH`; no D3 V5 engine request, no engine invocation and no audio creation.
- E1 family adapter remains `NOT_CONNECTED_E1`, `target_gate=E4`, `renderer_input_emitted=false`. D9.10 bridge and adapter are planning-only.

## Required evidence

Upload the complete generated folder:

`artifacts\tests\c11d_d9\producer_universal\D99-GUI-<ID>\`

Retain and inspect at least:
- `request.json`
- `d9_request.json`
- `canonical_request.json`
- `universal_plan.json`
- `editorial_render_bridge_plan.json`
- `d_only_render_adapter_envelope.json` (use actual filename if versioned differently by the GUI receipt)
- `c11e_production_intent_receipt.json`
- `producer_universal_receipt.json`
- `gui_cli_parity.json`
- `c11e_gui_cli_parity.json`
- `cross_suite_lifecycle_receipt.json`

Require request/editorial/plan/intent semantic parity, bridge/envelope equality, correct family/subtype and four fields, and lifecycle PASS. If a named optional file is not produced, preserve the folder as generated and record the exact inventory rather than editing the evidence.

## Fail-closed predicates

Every relevant receipt must preserve:

- `renderer=false`
- `renderer_input_emitted=false`
- `renderer_dispatch_invoked=false`
- `production_execution=false`
- `media_created=false`
- `dispatch_authorized=false`
- `release_authority=NONE`
- `D4.8=BLOCKED`

## Prohibitions

Do not run Godot, any `run_prototype.ps1`, `C11CSafeAmbient.py`, `generate_c11c_family_music.py`, FFmpeg/FFprobe, D3 V5, D9.14, E3, renderer dispatch, or media generation for this parity step. Do not change any source file. Do not run Smoke18/Matrix101.

After PASS, E4B proceeds to a separate D-owned editorial coexistence contract review. This request parity run alone does not close E4B.
