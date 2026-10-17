# C11-D Workstream Non-Duplication Register — 2026-10-17 V5

| Concern | Canonical owner / existing surface | V2 work must do | Must not do |
|---|---|---|---|
| Challenge selector/catalog and planning | D9.9 `universal_editorial_model.py` + `universal_producer.py`; D4 GUI/CLI adapter | Call canonical resolver/planner, retain source/request/plan hashes and D4 parity evidence | Duplicate selector inventory or create a second planner |
| Request-to-payload V1 for Challenge | `d_renderer_dynamic_request_payload_binding.py`; `materialize_challenge_visual_payload_in_memory.gd`; V1 definition/schema/tests | Preserve as accepted `parking_v2 / CHALLENGE_004` scope and regression | Broaden fixed selector, remove source pins, weaken V1 assertions or silently replace accepted gate |
| Challenge V2 source frame/payload prep | New, separately versioned Challenge V2 contract, orchestrator and harness | Establish selector-specific mechanics/asset/frame capabilities; use exact hashes; output per-selector pass/block; use in-memory-only receipts | Clone the whole V1 binder, assume identical mechanics, assets, frame counts or timebase |
| Frozen simulation / seed ownership | C11-C runtime bridge, execution pipeline and mechanic RNG paths | Verify the actual seed path and compare safe visual projections through real runtime receipts | Change RNG ownership/algorithm, synthesize visual variation, feed music seed into gameplay, alter simulation truth |
| Snapshot payload safety | Frozen `SimulationResult.frames` / `FrameSnapshot` | Allowlist only necessary visual snapshot fields and hash them | Include scores, telemetry, `custom_data`, `winning_frame` as sampler, or `close_calls` as timing |
| Asset binding | Each pinned `challenges/CHALLENGE_00*.json` `assets` object and declared physical assets | Confine paths, hash each declared file, validate SVG/resource type/dimensions if applicable, reject missing or unreferenced assets | Hardcode CHALLENGE_004's 3 assets for all selectors or fuzzy-load replacements |
| Timebase & timeline | Existing shared temporal-policy workstream; Challenge video metadata | Validate per selector, keep evidence staged; mark 008/009 phase payloads blocked | Choose 11s vs 12s unilaterally or edit canonical JSON |
| Seed-domain readiness | Current seed-domain audits and contracts | Distinguish identity hashes vs visual-subprojection hashes; two independent process runs | Infer runtime visual sensitivity from planner hashes alone |
| Candidate I/O / editorial / presentation / geometry / delivery / audio | Existing gap audits and policy proposals | Refresh from active source after V2; consume only after formal policy approval | Mark proposals approved just because payload assembly passes |
| D9.10 / renderer / release | Existing PREPARE_ONLY adapter and governance gates | Keep preparation status; report no renderer input | Renderer dispatch, media creation, baseline promotion or C11-C cutover |

## Active next dependency

Challenge planner preflight V2 is accepted as planning-only. The next work is a new V2 static source/capability contract, followed by actual runtime receipts and seed projection tests. The timebase gate for `CHALLENGE_008/009` remains a separate explicit dependency.
