# OVERHAND MASTER PROMPT — C11-D controlled baseline completion (2026-10-17 V2)

## Mission

Bring C11-D to a deterministic, renderer-agnostic production system that can safely replace frozen C11-C only after all technical gates, formal baseline approval/freeze and explicit cutover acceptance. The product should share editorial and presentation behavior by default across Challenges, Visual Loops and Visual Drills; all on-video text should be editable through the existing Producer/CLI and GUI/CLI should use the same canonical request contracts.

Do not optimize for a green summary. Optimize for verified, source-pinned, reproducible gates and explicit boundaries. A subgate PASS is scoped to its named contract and is not baseline authorization.

## Immutable source/reference

Active checkout: `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`.
Frozen C11-C manifest: `release\C11C_FREEZE_PACKAGE_MANIFEST.json`.
Expected SHA-256: `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.

Never mutate C11-C simulation truth, RNG, `SimulationResult`, `winning_frame` (sole temporal anchor), `close_calls` (episode count only), frozen geometry or manifest. Do not apply a full repo snapshot over the current checkout. Existing suite surfaces only: `c11c-test`, `c11c-producer`, `c11c-catalog`, `c11c-config`, `c11c-maintenance`; no `c11d-control`.

## Current latest verified gate

On 2026-10-17 the operator ran the exact-selector Visual Loop V2 audit on Windows with Godot `4.7.1.stable.mono.official.a13da4feb`, exit `0`. Result: direct source pins 70/70; request plans 5/5; request-bound grammar parameter instances 5/5; exact in-memory selector payloads 5/5; distinct payload digests 5/5; deterministic repeats 5/5; authoring envelopes 5/5; shader branch mapping reviews 5/5; 45/45 metadata-only policy reference pairs; policy values not consumed; zero renderer inputs and zero payload files; 19 approvals checked and zero granted. Internal report SHA-256 `55240ee0e34340bd860e4243f03d49ce777aa6ef87e5154443f5e2b1a9754d74`; stdout SHA `2b8a7bba0bf042c83d622c44ae5c3512c3ce5adc351c2c3f440008a2f7ca0b83`; stderr SHA `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`; report-file SHA `ecdaac7e6155663ec13661427808c05f636874edb18ac0bb2c509bfa0499a03f`. Source checkpoint: `docs/current/d/C11D_VISUAL_LOOP_EXACT_SELECTOR_PAYLOAD_V2_RUNTIME_ACCEPTANCE_CHECKPOINT_20261017.md`.

Covered selector IDs are exactly `harmonic_membrane`, `interference_plane`, `parametric_ribbon`, `lattice_wave`, `orbital_wave` under `c11c_geometric_waves_v1`. Payload materialization is in memory only. This does not run a shader, create a renderer or media, consume the policy bodies, close candidate I/O, or accept seed domains.

## Immediate next engineering increment

Implement a separately versioned `D_RENDERER_VISUAL_LOOP_SEED_DOMAIN_AUDIT_V2`, scoped to the five supported geometric grammar selectors. Do not edit the V1 cross-type seed audit or current V2 request/payload contracts in place. Full details and edge-case rules are in `docs/current/d/C11D_SEED_DOMAIN_NEXT_INCREMENT_PLAN_20261017.md`.

Matrix per selector: baseline `gameplay_seed=12345`, `music_seed=840001`; gameplay-only change `54321/840001`; music-only change `12345/840002`; two independent Godot processes for every variant (30 invocations total as the intended acceptance scope). Each row must re-run canonical request planning and all downstream binding/parameter/payload identities. If current references are bound to fixed baseline request hashes, version the reference-carrier/build function to support changed requests; do not fake source-lineage joins.

Seed assertions:
- gameplay-only mutation changes request/plan/binding identity and seed-derived style/visual-content projection for every grammar;
- music-only mutation changes request identity but preserves gameplay-derived style/variation/palette/visual-spec projection;
- independent process repeats reproduce the appropriate hashes;
- the outer exact-selector envelope includes full request identity, so its overall digest may change when only music seed changes; do not incorrectly require that entire envelope hash remain equal;
- cross-domain equal numeric seeds and malformed/implicit seed inputs fail closed before Godot; `master_seed=NOT_ADOPTED`, automatic/default seeds disabled.

## Subsequent canonical gates

1. Complete the V2 five-grammar Loop seed audit with strict schema, direct source pins, 30 complete runtime receipts, defined negatives, report self-hash and evidence-grade log hashes.
2. Refresh candidate identity and the 10-group Candidate I/O audit against the active checkout; previous last recorded status is 0 complete / 6 partial / 4 blocked. Don't edit counts by hand.
3. Expand Challenge seed/selector coverage through canonical planning and payload binding; distinguish all nine Challenge definition files from selectors actually supported by canonical D contracts.
4. Keep Visual Drill's 20-selector seed population separate. Broaden other Loop families only through their own canonical sources/contracts.
5. Resolve policy approval and end-to-end consumption for editorial values/field windows/visibility, presentation regions/coordinates, Challenge temporal sample/composition, delivery timebase/timeline and audio/music. A metadata-only reference count is not approval or use.
6. Close content identity, source lineage, payload identity and candidate I/O groups; keep renderer admission fail-closed until the complete supported input contract is accepted.
7. Obtain independent review and formal D4.8/test-run authorization before a controlled D-only qualification render. Record output/exit/log/hash/repeatability and visual/audio quality. Qualification render is not release.
8. Complete D9.14, D9.16, D9.17, D10, formal baseline approval/freeze and explicit C11-C→D promotion/cutover in canonical order.

## Required habits

- Inspect active checkout, current files and pins before every overlay; snapshot history is context only.
- Prefer concise additive ZIP overlays and complete pasteable PowerShell 5.1 blocks from the repository root. Verify ZIP hash, C11-C manifest hash, each target precondition and post-copy hash. Stop on first failure; apply and test in separate blocks; use explicit rollback for any partial copy.
- For native processes, capture stdout and stderr separately, then validate actual exit code, Godot version, exact pass markers, source pins, receipt count and strict report/schema/self-hash before stating PASS. Never hash a nonexistent file or convert a wrapper failure into a test failure/pass claim.
- Use fresh source pins after accepted code changes; never modify a pin just to silence drift.
- Preserve C11-C and governance flags across every failure and success path.

## Non-negotiable state until formal closure

`renderer=OFF`; `candidate_input_admissible=false`; `media_created=false`; `D4.8=BLOCKED`; `release_authority=NONE`; `D9.10=PREPARE_ONLY`; `baseline_approval=MISSING`; `freeze_eligible=false`; D9.14/D9.16 blocked; `D9.17=BLOCKED_NO_GO`; D10 blocked. C11-C remains the immutable authoritative baseline and rollback reference until explicit D approval/freeze/promotion/cutover.
