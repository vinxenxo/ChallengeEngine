# C11-D to C11-E Full-Family Roadmap — V33

**Date:** 2026-11-04. Recovery identity correction and configuration-driven visual test clarification. No governance locks changed.

## Product outcome

One C11-E shared service and family adapters delivering validated audiovisual output for Challenge, Visual Loop and Visual Drill. Preserve C11-C generators/mechanics and existing family audio paths. Add D presentation, enabled family editorial, independent gameplay/music seeds, Challenge D3 V5, FFmpeg mux, FFprobe/audio QA and immutable receipts. GUI and CLI use the same E1 service.

## Current milestone state

- E0/E1/E2/E3.2/E3 GUI audio pilot/E3 negative controls: accepted in bounded scopes; reuse.
- E4A.2: accepted real C11-C BODY reference (CHALLENGE_004, 450 frames/15s).
- E4A.3 V2: accepted bounded D-owned Godot compositor proof over real frames (6/6, 18 PNGs, 12 comparisons; BODY preserved).
- E4A.3 operator disposition: countdown-on hook/editorial coincidence is intentional for that selected configuration. It is not a failed render. Future Producer GUI must expose visibility options through the shared E1 request. Test more than one supported editorial configuration; do not assume all fields always print.
- E4A.4 worker: native exit 0, 42/42 tests, worker PASS marker. D3 V5 → D3.3 → FFmpeg mux/FFprobe and H.264/audio-seed checks ran. The outer wrapper failed after worker success. Recovery V1 had a parameter-default path issue; V2 then had an identity comparison defect (`RUN_<run_id>` folder vs unprefixed receipt `run_id`). V3 is standalone and corrects the relation. Do not rerun the worker.
- E4A.4 closure: after archive/receipt/media integrity verification and operator listening/sync review. Current mux MP4s retain the immutable C11-C base video; the E4A.3 compositor layer is not embedded.
- E4A remaining: recover evidence; inspect/listen/sync; derive a compact presentation-configuration test matrix from historical Challenge definitions/binders/profiles/runs and approved policy; wire request-level visibility through E1; prove representative selected configurations; complete composited audiovisual path.
- E4B Loop: grammar/variant timeline/editorial; preserve existing C11-C Loop music.
- E4C Drill: phase/END_CTA/editorial; preserve existing C11-C Drill music.
- E5: determinism, seed isolation, no adapter/profile leakage, GUI/CLI parity.
- E6: Smoke18, six A/V scenarios per family.
- E7: Matrix101 target 54 Challenge + 27 Loop + 20 Drill. CH_008/009 held due declared 11s vs phase sum 12s; 99 provisional runnable.
- E8: row-by-row historical C11-C corpus, including 27 review and 9 Challenge cases plus applicable categories; independent acceptance, immutable freeze and explicit promotion.

## Configuration-driven presentation review

D1.1 maps nine Challenge definitions but leaves timing/geometry UNKNOWN; D1.5 establishes logical 540x960 Header/Body/Footer while safe areas, generic CTA geometry and typography remain UNKNOWN; D1.7 defines nine mappings and no Challenge layout overrides. Historical C11 presentation binders show phase-scoped hook/countdown and CTA behavior, while the C11C shared editorial layer exposes header/footer and matrix/intro visibility modes for its own supported surface. Treat historical code/tests/receipts as evidence for the test matrix, not permission to mutate C11-C or infer all switches apply to Challenge. Cover grounded configurations only, including countdown on/off and policy-authorized field presence/omission.

## Governance

C11-C 2.19.12 remains sole production authority; manifest 796,318 bytes / SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`. Do not alter protected generators/mechanics, `core/audio`, D3 V5, E1, manifest, D4.8/D9.10 locks or production authority. No E gate grants production renderer, dispatch, freeze or promotion; `release_authority=NONE` until E8 and explicit approval.
