# C11-E E6 — D4.8 Historical Conflict Matrix — 2026-11-18 V1

## 1. Confirmed target scope

The operator explicitly confirmed in the current conversation:

- Smoke18 contains **18 top-level scenario rows**: six Challenge, six Visual Loop and six Visual Drill.
- The six Challenge rows contain **18 nested A/B/C qualification subruns** (three per Challenge row). These are not 18 additional top-level rows.
- The objective is a complete cross-family TEST_ONLY qualification of the D work, so the C11-E factory can proceed toward editorial, layout and family-native music integration after the required gates pass.

This fixes the scope question. It does not itself approve media execution or supersede D4.8.

## 2. Evidence reviewed and source authority

The following two archives were inspected as evidence/reference only; neither is an active-checkout authority and neither was extracted over the checkout:

| Evidence | SHA-256 | Finding |
|---|---|---|
| `C11E_E6_CHALLENGE_SOURCE_CAPTURE_20261118_210430.zip` | `01cdc329614d99e835bafa09da9c63a3cb155a7fd2c9e3c5be0157d731c4c457` | ZIP CRC PASS; six entries including directory entry; four files: frozen C11-C manifest, D4.8 R1V V2 policy, D9.9 universal request, Challenge editorial approval, plus capture manifest. |
| `ChallengeEngineV01_STATELESS-nightly build.zip` | `6a3c4c6cae2d19faffe9fe22c86b940f4178d301c1591c4b7acae5d9e7180382` | ZIP CRC PASS; 23,917 entries; used to inspect historical D4.8 records, audio amendments, D/E4 evidence and family contracts. Snapshot timestamp in Library: 2026-11-16; reference only. |

Source-capture `SOURCE_CAPTURE_MANIFEST.json` records:

- `release/C11C_FREEZE_PACKAGE_MANIFEST.json`: 796,318 bytes; SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.
- `definitions/c11d/production/C11E_D4_8_R1V_QUALIFICATION_ONLY_POLICY_V2.json`: 12,996 bytes; SHA-256 `0866b53ad4fcdebe74d01f66864b2dfb00eb644ca28dcd59301c8f3208239c07`.
- `definitions/c11d/production/C11D_UNIVERSAL_PRODUCER_REQUEST_D9_9_V1.json`: 1,761 bytes; SHA-256 `342a61338c80a2f1616e8e9f38986bd90f410257c0e321f99840380fb0fd804b`.
- `definitions/c11d/production/C11E_E4A_CHALLENGE_EDITORIAL_PRESENTATION_POLICY_APPROVAL_V1.json`: 4,200 bytes; SHA-256 `764629384896a255cf992da89fa427c19f60f9b2e623b81ad17d909674b466b5`.

Before any implementation or execution overlay, each required source pin must be rechecked against the active checkout. No source snapshot is to be copied over it.

## 3. Clause-level historical conflict matrix

| Authority / evidence | Existing approved scope | Explicit restriction or unresolved point | Consequence for Smoke18 | Required successor decision |
|---|---|---|---|---|
| D4.8 production activation contract; SHA-256 `e275b0f3d080f18d252b38c0b6f140b34e89c0a915f498c24d8e660c85e102a8` | Declarative D4.8 authorization evaluation only. REVIEW can validate but is never production-authorized. | Even a valid PRODUCTION request remains BLOCKED with `RENDERER_POLICY_DISABLED`; D4.8 does not invoke a renderer. Historical D4.8 validation matrix is 8/8 PASS because it correctly enforces the block. | Historical D4.8 PASS/CLOSED is not a rendering permission. | Approve a separately versioned, bounded E6 TEST_ONLY successor decision. Do not edit D4.8 or its old policy in place. |
| `C11E_D4_8_R1V_QUALIFICATION_ONLY_POLICY_V2.json`; SHA-256 `0866b53a...8239c07` | Five Visual Loop selectors × A/B = ten C11-C silent source captures; `-NoSound`; FFprobe read-only; FFmpeg decode-only to in-memory pixel hasher; exact unique output roots; no AVI retention. | `audio_or_music_generation=false`; D compositor=false; D9.10 renderer-consumer dispatch=false; FFmpeg filters/mux=false; D3/PCM prohibited; `smoke18_or_matrix99=true` under forbidden operations. | Does not authorize any of the 18 Smoke18 rows or D-branch family composition. | Define an E6-only exception/authority with exact family scope and pinned test consumer path. Keep production renderer and production dispatch disabled. |
| R1V operator approval record dated 2026-11-07; file SHA-256 `fc26f9af81658f4a4e24977c5f3dbcd800bc11eb511062cff3918d1d69ae5789` | User-approved exactly five Loop selectors × two independent runs; ten launcher invocations; silent C11-C MP4 only. | Approval expressly excluded audio, D3, D compositor/consumer, filters, mux and production release. | Cannot be stretched to Challenge, Drill, Smoke18, or D composition. | New explicit successor-policy approval is required for any expanded TEST_ONLY scope. |
| R1V Family Audio Scope Amendment; file SHA-256 `c0a6a1e2391b0528347fc3a0a8e5b10b0c691e90131d0a0afbaaacfd15ec9905`; approval record SHA-256 `6a0081a5a769a1b2efdc2cc6c2f807e57fd8af541bbba211c310cf6781e3c132` | Extends only the bounded five Loop selectors × A/B = ten Loop A/V outputs; `C11C_FAMILY_MUSIC_V4`; WAV PCM16 / 44.1 kHz / stereo; AAC 192 kbps / 44.1 kHz / stereo; H.264 stream copy; one prior Fractal Bloom A reuse plus nine new native C11-C captures. | D3 V5 remains prohibited for Visual Loop; D compositor and D9.10 dispatch remain prohibited; no general D4.8, release or promotion. | Gives Loop-family A/V precedent only, not cross-family E6 authority. | Keep Loop music native to Loop; decide only whether existing eligible Loop A/V evidence is reused in Smoke18 after requalification. Do not broaden this amendment. |
| Challenge editorial presentation approval; SHA-256 `764629384896a255cf992da89fa427c19f60f9b2e623b81ad17d909674b466b5` | Challenge semantic mapping on canonical D9.8 selectors, with bounded fixture `CHALLENGE_004`; fields title/subtitle, player_name/challenge_label, CTA and metadata-only language. E4A isolated test rendering was separately approved. | It does not approve all six Challenge selectors or general D production. Geometry and phase windows must resolve from D-owned contracts; no C11-C simulation-truth mutation. | Supports the CH004 proof and Challenge contract lineage, but not all five fresh Challenge A/V obligations. | Pin the D consumer/profile contracts and explicitly authorize the exact E6 test-only Challenge path. |
| E4A.7 CH004 D-composited A/V; run `RUN_20261106T070808Z-62F31F9C`; report SHA-256 `efb0f1a9245d3fce15bf48041c8972e90f6874d308fa99340afb5c731f94403a` | Isolated CH004 A/B/C proof. Gameplay seed 314159; A/B music seed 840001; C music seed 840002; D3 V5 / `challenge_8bit_v1`; 104 BPM historical D9.2 pilot fixture; 450 frames / 30 FPS = 15 seconds. Operator visual and listening review PASS. | 104 BPM and 15 seconds are historical CH004 test facts, not global product defaults. The other Challenge selectors must use their own pinned source-timebase facts. | CH004 is reusable evidence, not proof that all six Challenge rows are rendered. | Keep A/B equality and C changed-music behavior as a candidate test pattern, but explicitly approve all seed/tempo inputs and derive each selector duration from its own canonical timebase. |
| E4C Drill composition proposal V2 and isolated Drill A/V receipts | D-owned Drill composition contract covers 20 selectors / four families, pixel-exact GAME body crop, native PRE_ROLL/END_CTA passthrough and family-specific music profiles. Existing isolated A/V qualification receipts include A/B/C seed comparisons; E5 operator A/V review was accepted for the `tracking / tier-2` representative. | The proposal's execution boundary does not authorize new native capture, new audio generation or production renderer/dispatch. A representative approval is not global Smoke18 authority. | Six Drill rows are reuse candidates only after exact E6 ledger requalification; do not regenerate accepted Drill media. | Requalify exact linked evidence, preserve Drill phase/timeline/music contracts and family profile; only a demonstrated gap may become a separately authorized test. |
| Unified audio delivery proposal V1; SHA-256 `3dd4874e1b6506de6d9ddbe6ad1b567a284b94cc00ef1bac0d35d1731af05e23` | Proposal metadata describes REVIEW_720 AAC-LC 192 kbps / 48 kHz / stereo and nominal content durations: Loop 20 s/600 frames; Drill 21 s/630 frames; Challenge 15 s/450 frames. | Status `PROPOSED_NOT_APPROVED`; music selection, mixing, loudness, missing-audio behavior, encoder delay and post-encode duration tolerance are unresolved; no audio is selected or emitted. It expressly forbids assuming silence or synthesizing audio. | It must not overwrite existing family-native timelines/profiles. Existing evidence includes Loop C at 22 s/660 frames, Drill composition V2 at 810 frames/30 FPS = 27 s, and CH004 at 15 s/450 frames. | Do not make the proposal a renderer input or universal duration authority. Reconcile each family from its own accepted timeline and audio contract. |
| E6 reuse requalification `E6SMK18REQUAL_20261118T141200Z_BA5AC046`; receipt SHA-256 `4d63b8caec7a975cc0362ee9d7a5924f5ab8371e8e8e1457e1d60956bf65ce33` | 21/21 checks; 13 reuse candidates: CH004 + six Loop + six Drill; five fresh Challenge A/V obligations. | `E6_ACCEPTED=0`. Candidates are not accepted Smoke18 rows until exact ledger acceptance. | Full 18-row coverage can be achieved without rerunning already accepted media: requalify 13 candidates and satisfy five fresh Challenge selector-level obligations, while preserving 18 nested A/B/C probes. | Use the requalified reuse mapping; render only the missing Challenge A/V work unless a source-pin/evidence failure proves a specific reuse candidate ineligible. |
| Challenge PREPARE_ONLY orchestrator; run `E6CHPREP_20261118T202841Z_37C6AE0E`; receipt SHA-256 `b54a884f1574d22fa65ea198d279d9ba84bb3967adc87885213f7659a1b1c944` | Six Challenge groups; 18 A/B/C subruns; 18 E1 intents; 18 static D envelopes; 28/28 source pins unchanged pre/post. | `E1=PREPARE_ONLY`; `family_adapter=NOT_CONNECTED_E1`; E6 accepted 0; matrix not frozen; music fixtures proposal-only; tempo/duration null; all media operations false. | Preparation proves intent/envelope formation, not D consumer runtime, rendering, audio or media acceptance. | Define a one-run TEST_ONLY consumer bridge or direct pinned test harness without silently changing E1 production state. Resolve seed, tempo and duration authority before building the execution allowlist. |

## 4. Smoke18 execution coverage — locked denominator

| Family | Top-level rows | Nested qualification |
|---|---:|---|
| Challenge | 6 | 18 A/B/C subruns total (3 per Challenge row) |
| Visual Loop | 6 | The existing E6 row-level reuse candidates are linked to family-native evidence; preserve each Loop selector/timeline/music binder. |
| Visual Drill | 6 | The existing E6 row-level reuse candidates are linked to family-native evidence; preserve each Drill selector/timeline/music binder and END_CTA precedence. |
| **Total** | **18** | **18 nested Challenge A/B/C subruns; not 36 top-level rows.** |

The current reuse requalification identifies 13 candidates (CH004 + six Loop + six Drill) and five fresh Challenge A/V obligations. This is the recommended efficient completion path. Do not rerun an already accepted output merely to make the row count look complete. A candidate becomes reusable only after exact path/hash/receipt/sidecar/source-pin and operator-review predicates pass. `E6_ACCEPTED` remains zero until a later explicit E6 ledger acceptance receipt records acceptance.

Challenge selector pool confirmed in the current E6 preparation plan: `CHALLENGE_001`, `CHALLENGE_002`, `CHALLENGE_004`, `CHALLENGE_005`, `CHALLENGE_006`, `CHALLENGE_007`. `CHALLENGE_008/009` remain excluded until the historic 11-second declared duration versus 12-second phase-sum conflict is resolved; do not silently add them to Smoke18.

## 5. Family-specific media and music rules that must not be flattened

- **Challenge:** D3 Music V5 / `challenge_8bit_v1` is the family-native route. CH004's 104 BPM, 15-second, gameplay/music seed values are historical test fixtures only. The other Challenge selector durations must come from their own canonical D timebase. No automatic tempo, music seed or duration default is authorized by E1 PREPARE_ONLY.
- **Visual Loop:** preserve the Loop-native C11-C Family Music V4 route. R1V's bounded audio amendment is Loop-only and uses 44.1 kHz AAC; do not reclassify it as D3 or convert it to the unapproved unified proposal.
- **Visual Drill:** preserve each native Drill family music profile and phase timeline. Existing receipts distinguish e.g. `FLOWING_VECTOR`, `ORGANIC_BLOOM`, `ORBITAL_RITUAL` and `CIRCUIT_PULSE`; historic seeds 840001/840002 are fixtures in those receipts, not global product defaults.
- Preserve per-family H.264 pixel-format/range contracts. In particular, do not normalize Loop `yuvj420p/pc` evidence into Challenge `yuv420p/tv`.
- The unified audio proposal is not approved and is not a music asset, mixing, loudness or encoder-delay policy. It is not a renderer input.

## 6. What must be decided before an E6 execution overlay

1. Approve or reject a **separate, versioned E6 TEST_ONLY successor policy** that resolves only the Smoke18 qualification conflict. It must not mutate `C11E_D4_8_R1V_QUALIFICATION_ONLY_POLICY_V2.json`, the D4.8 production activation policy, the frozen C11-C manifest or protected C11-C sources.
2. Approve the exact D-owned test consumer/composition route. Preferred boundary: invoke only pinned D test consumers/compositors inside an isolated Smoke18 TEST_ONLY runner; keep `E1=PREPARE_ONLY`, the global production renderer OFF, production dispatch false and release authority NONE. Do not connect the E1 family adapter globally or use D9.10 production dispatch by implication.
3. Approve the Challenge audio fixture authority: exact gameplay seed source, A/B music seed, changed C music seed, D3 V5 profile and tempo. Per-selector source durations must be derived from the corresponding canonical Challenge timebase, not copied from CH004.
4. Confirm reuse strategy: 13 current candidates are reused only after exact evidence requalification; five Challenge selector-level A/V obligations are fresh. Any reuse failure is isolated and escalated rather than silently replaced by an unbounded rerun.
5. Keep Loop/Drill audio profiles and media predicates family-native. Do not approve the unified audio proposal V1 by accident; it is still proposal-only.
6. Only after those choices, build a separate execution overlay pinning executable path/version/SHA-256, exact argument vectors, working/input/output roots, process counts, concurrency, timeouts, output cardinality/byte ceilings, stop-on-first-failure, quarantine, hashes, FFprobe checks and human visual/audio review. No execution is permitted by this documentation overlay.

## 7. Current invariant state — unchanged

`D4.8=BLOCKED; E1=PREPARE_ONLY; FAMILY_ADAPTER=NOT_CONNECTED_E1; D9.10=PREPARE_ONLY; D9.14=BLOCKED; D9.16=BLOCKED; D9.17=BLOCKED_NO_GO; D10=BLOCKED_FOR_PROMOTION; E6_ACCEPTED=0; MATRIX_FROZEN=FALSE; RENDERER=OFF; PRODUCTION_DISPATCH=FALSE; PRODUCTION_MEDIA=FALSE; RELEASE_AUTHORITY=NONE`.

`GIT_CHECKS=SKIPPED; COMMITS=OPERATOR_MANAGED; SOURCE_FILE_PINS=ENFORCED`.

This matrix is a technical reconciliation document, not an approval record. Do not run Godot, FFmpeg, FFprobe, D3/audio/PCM, mux, renderer, dispatch, BatchId reservation/consumption, production output writes or media creation from this gate. Do not rerun previously accepted E4A/E4B/E4C/E5 media. Do not change C11-C, D4.8 V2 or any protected source.
