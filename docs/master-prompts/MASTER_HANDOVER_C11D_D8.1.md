# C11-D — MASTER HANDOVER — D8.1 FFPROBE INTEGRITY

D0–D7.5 = PASS / CLOSED. D7 = FROZEN. D8.0 = PASS / CLOSED.

Next active checkpoint: **D8.1 — ffprobe / media integrity**.

D8.1 is read-only physical media inspection. `ffprobe` may be invoked against existing media. FFmpeg processing and all media mutation remain forbidden.

D7 authorities remain:

- `CANONICAL_D7_1` — matrix
- `CANONICAL_D7_3` — catalog
- `CANONICAL_D7_4` — identity/provenance
- `CANONICAL_D7_5` — full acceptance

Governance remains locked: `master_seed=NOT_ADOPTED`; gameplay seed = `request.seed`; music seed = `request.music_seed`; cross-domain seed sharing = `FORBIDDEN`; runtime derivation disabled; automatic seed generation disabled; D4.8 `BLOCKED`; runtime authority `NONE`; production false; renderer false.

Protect all C11-C simulation, mechanics, RNG, `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector`, `RenderedFrameStream`, C7/C9 contracts, logical 540×960 geometry and proven presentation/production behaviour.

Read:

1. `MASTER_HANDOVER_C11D_D7_FROZEN.md`
2. D7 freeze/acceptance evidence
3. `D8.0_BOUNDARY_INVENTORY_CONTRACT.md`
4. `D8.1_FFPROBE_INTEGRITY_CONTRACT.md`
5. `artifacts/tests/c11d_d8/d8_0/d8_0_validation_receipt.json`
6. `artifacts/tests/c11d_d8/d8_0/d8_0_inventory.json`

Do not invoke `release_gate.py`. Do not render or encode. Do not alter D7/C11-C.

The only D8.1 write scope is `artifacts/tests/c11d_d8/d8_1/`.


## V1.1 scope correction
D8.1 compares inventory drift against the same global workspace-media universe recorded by D8.0. Probe execution remains limited to media located under `artifacts/` and `release/`. Adding D8.1 code/documentation/evidence must not cause a false-positive drift.
