# C11-E E6 Historical Conflict Matrix — V2

**Date:** 2026-11-18. Supersedes V1 only as the current reconciliation summary; all historical receipts and policies remain immutable.

| ID | Historical authority / evidence | Exact scope | Reconciled disposition | Resolution still required |
|---|---|---|---|---|
| H01 | D4.8 R1V V2 `0866b53a…` | Ten silent C11-C source qualification invocations across five Loop selectors | Valid only for that bounded source qualification; prohibits Smoke18, D3/audio/PCM, FFmpeg filters/mux and D compositor | Separate successor policy with clause-level non-overlap and explicit E6 scope |
| H02 | R1V A/V amendment and human closeout | Five Loop selectors, ten A/B outputs and their family music route | Closed in declared scope; do not rerun | Does not extend to D compositor or Smoke18 |
| H03 | Option C boundary `795be1da…` | D post-composition over immutable Loop source media | Static PREPARE_ONLY only; no D compositor | Implement/test a D-only post-composition consumer |
| H04 | E4B shared-service review V3 `ed17c190…` | E1/GUI/CLI family preparation and D9 handoff | `PASS_TEST_ONLY_SHARED_SERVICE_PREPARATION`; no rendered request payload or accepted D pixel consumer | E6-specific Loop compositor evidence |
| H05 | Visual Loop composite checkpoint `11db1b9f…` | One selector's deterministic in-memory composite | Not materialized renderer/shader/pixels/video; editorial visual consumption 0/14 | Real visual payload and consumer acceptance |
| H06 | Challenge E4A.7 | CH004 D-composited A/V | Accepted anchor in its exact 15s/selector/profile scope | Five additional selectors require fresh A/V; E6 editorial fixture still missing |
| H07 | E4C six Drill receipts + closeout | Six exact Drill A/V candidate rows | Candidate reuse; E6 predicates must be checked | Do not regenerate unless predicate fails or source drift is proven |
| H08 | E6 reuse requalification | 13 evidence-linkage candidates, 21/21 | Candidate linkage PASS; E6 accepted 0 | Final row acceptance matrix and evidence role mapping |
| H09 | Challenge PREPARE_ONLY | Six groups / 18 intents / 18 envelopes; 28 pins | Static prep PASS; no media | New run-only fixture manifest; five A/V routes; CH004 requalification |
| H10 | Challenge current intent payloads | title/subtitle/CTA `UNKNOWN`, personalization false | Cannot prove visible editorial consumption | Operator-approved synthetic editorial fixture in new plan only |
| H11 | Global renderer I/O audit checkpoint | 10 input groups | Last located report 0/10 complete, 6 partial, 4 blocked | Separate D baseline remediation; do not infer readiness from Smoke18 exception |
| H12 | E6 successor scope approval (operator reply 2026-11-18) | 18 rows and fixture-only music | Approved to prepare scope and proposal | Not execution permission; E6 TEST_ONLY authorization still separate |

## Exact D4.8 R1V V2 clause reconciliation

The successor must preserve—not widen by implication—the following exact source-policy clauses (`definitions/c11d/production/C11E_D4_8_R1V_QUALIFICATION_ONLY_POLICY_V2.json`, SHA `0866b53ad4fcdebe74d01f66864b2dfb00eb644ca28dcd59301c8f3208239c07`):

| V2 field / clause | Existing bounded meaning | E6 Smoke18 consequence | Successor treatment proposed |
|---|---|---|---|
| `authority_boundary.r1v_qualification_only` | `AUTHORIZED` only for the bounded R1V task | Does not grant Smoke18 or a D compositor | Leave true only as a historical record; successor uses its own E6-scoped authority field. |
| `authority_boundary.general_d4_8_production` | `BLOCKED` | Still blocked after E6 TEST_ONLY | Must remain blocked until E8 and separate production transition. |
| `scope.allowed_selector_count` + `selectors[]` | Exactly five Visual Loop selectors: radial_bloom, harmonic_membrane, dipole_field, swarm, astrolabe | Does not contain Challenge, Drill or Loop22 interference_plane | Do not append selectors to V2; list 18 E6 rows in a distinct successor manifest. |
| `execution.approval_scope.launcher_invocations` | Exactly 10 (five selectors × A/B) | Not 18 Smoke18 rows and not Challenge A/B/C | Separate E6 row/subrun cardinality, one-shot batch and per-family launcher routes in the successor. |
| `execution.approval_scope.no_filters_audio_d3_mux_or_d_consumer` | No filters, audio, D3, mux or D consumer | E6 needs family-specific audio/mux QA and D composition in TEST_ONLY | Create a narrow, separate E6 exception with exact tool pins/argv/output limits; never interpret V2 as granting these operations. |
| `allowances.c11c_no_sound_mp4_encode` | Existing pinned C11-C `-NoSound` encode branch only | Does not authorize compositing or audio | Reuse only for explicitly qualified source-capture steps, if still required by an E6 row. |
| `allowances.ffprobe_read_only` / `ffmpeg_decode_only_pipe_to_memory` | Metadata/PTS read and decode-only pixel hashing | Not FFmpeg encode/filter/mux, not D output | Reuse as read-only/decode operations with per-family pixel format/range handling and pinned binaries. |
| `allowances.d_compositor` / `d9_10_renderer_consumer_dispatch` | Both false | Blocks Loop D post-composition and renderer dispatch under V2 | Successor may permit a bounded D-only test compositor only after implementation, source invariants and separate authorization. No production dispatch. |
| `allowances.audio_or_music_generation` / `forbidden.d3_music_engine` / `forbidden.pcm_audio_generation` | False/prohibited | No music generation under V2 | Successor may identify Challenge D3 V5 fixture and existing Loop/Drill family music only within approved TEST_ONLY execution; not product defaults. |
| `forbidden.smoke18_or_matrix99` | Explicitly forbidden | Direct scope conflict with E6 | Supersede only through a separate, versioned successor policy. V2 remains unchanged and auditable. |
| `expected_source_media` | 720×1280, 30 FPS, H.264, yuv420p, silent; frame count/PTS/duration rules are R1V source-capture predicates | These are not universal Challenge/Loop22/Drill delivery assumptions | Use per-family exact technical profiles; do not impose the R1V yuv420p or timebase on full-range Loop22 or other families. |
| `failure_policy.fail_closed` and `stop_after_first_failed_launcher_or_invariant` | Preserve outputs; never delete/overwrite; stop first failure; operator visual review required | Must remain applicable to E6 batches | Keep fail-closed; define exact E6-specific output cardinalities and stop conditions. |
| `governance.general_renderer_activation` / `release_authority` | Renderer disabled; release NONE | No production activation | Keep `renderer=OFF`, production dispatch/media false and `release_authority=NONE` throughout E6 TEST_ONLY. |

The key distinction is that V2's top-level `execution_authorized=true` is not a global boolean: its own `authority_boundary.meaning`, `execution.approval_scope` and `forbidden` entries restrict it to ten C11-C source-qualification launcher calls. The E6 successor must have its own scope, approval, run identity and `execution_authorized` state; it must not alter, re-open or reinterpret V2.

## Counting invariants

- Smoke18 = 18 top-level rows, six per family.
- Challenge A/B/C = 18 nested subruns; not additional scenario rows.
- Reuse candidates = 13; E6-accepted = 0 until row-level predicates and final acceptance are recorded.
- Five Challenge selector groups still require new audiovisual evidence.
- Six Loop source/audio candidates do not prove six D-composited outputs.

## Global locks

Keep C11-C frozen manifest `e405d08e…`, D4.8 R1V V2 `0866b53a…`, E1 PREPARE_ONLY, D9.10 PREPARE_ONLY, renderer OFF, dispatch/media false and release authority NONE. Never edit the original D4.8 policy to solve its scope conflict.
