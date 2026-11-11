# C11-E E4C Drill Shared Execution Adapter Design V1

Date: 2026-11-11
Scope: D-owned, isolated single-selector A/V qualification path.

## Boundary decision

E1 is not promoted. `c11e_production_service.py` remains unchanged, E1 reports `PASS_E1_PREPARATION_ONLY`, and `family_adapter.status=NOT_CONNECTED_E1` remains as authored. The new execution connection is a downstream D adapter consuming the canonical, validated E1 intent.

There are exactly two modified entrypoints: existing Producer GUI `c11c-suite/c11c-producer/main.py` and existing CLI facade `c11c-suite/c11c-producer/c11e_production_cli.py`. Exactly one new execution module is added: `tools/c11d/d9/c11e_e4c_drill_execution.py`. No parallel Producer, binder, business service or sixth suite module is introduced. Both entrypoints call the same module; CLI execution requires the explicit `--execute-drill-av` flag with `--origin CLI`. Without the flag, CLI behavior remains E1 plan-only.

## Contract

The adapter accepts only canonical Visual Drill PRODUCTION requests with REVIEW_720, audio ON, personalization ON, distinct gameplay/music seeds and one of the 20 existing family/tier selectors. The consumer plan must contain at least one real, non-empty title/subtitle/CTA value (not whitespace, not UNKNOWN). D editorial is visible only during GAME.

The E1 pin inventory and frozen C11-C manifest are verified at preparation, immediately before native capture and after execution; normalized before/immediate-pre/post pin sets must match.

## Media path

The existing C11-C Drill launcher is invoked silently (`-NoSound`) using gameplay seed and native tier rules. D composes every output frame through the pinned Qt consumer. The existing `C11CSafeAmbient.py` wrapper calls `FAMILY_MUSIC_V4` with `request.music_seed`: A and B use 840001; C uses 840002 for the first agreed pilot. D3 V5 and C11-C's embedded gameplay-seed-coupled audio are explicitly excluded. FFmpeg muxes AAC-LC 48kHz stereo and FFprobe validates stream properties, timing and frame count. A/B music WAV hashes must be equal; C must differ; final A/C video bitstreams must be identical and audio bitstreams different.

## Authority

Only isolated E4C qualification media are allowed under the explicit operator test authorization. `production_dispatch=false`, `release_authority=NONE`, C11-C source unchanged. The package does not close E4C: Windows install, GUI smoke, one-selector A/V, operator listening/visual review and later 20-selector A/V remain pending.
