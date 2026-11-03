# C11-E E3.2 — Formal Closure and Decision Record V1

**Decision date:** 2026-11-03
**Code commit:** `3cc1caa6d740b1525a4ebb30a4ff7f02868ac5a8`
**Parent:** `a30b63d31b2d071ebab9c67ec9f8ff7393731488`
**Tree:** `de8a1180f04eb0f5e0ea5c8130eedaaccf7e78fa`

## Decision

**E3.2 is ACCEPTED / CLOSED for the bounded D3 V5-to-E1 music contract binding and deterministic V5 compatibility change.** The decision is based on the operator-supplied local application result, all seven payload postimage checks, protected-path checks, the frozen C11-C manifest pin, the complete 21-test run and the final integrity audit.

This closure does not accept actual C11-E Challenge audio generation, D3.3 mastering, FFmpeg mux, FFprobe final A/V, GUI dispatch or any Loop/Drill integration.

## Evidence

- Commit: `3cc1caa6d740b1525a4ebb30a4ff7f02868ac5a8`; parent: `a30b63d31b2d071ebab9c67ec9f8ff7393731488`; tree: `de8a1180f04eb0f5e0ea5c8130eedaaccf7e78fa`.
- Branch: `main`; operator reported `## main...origin/main [ahead 4]`; clean worktree.
- Installer: `APPLY=PASS`, `GIT_DIFF_CHECK=PASS`.
- Tests: 21/21 PASS, exit code 0; stdout SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`; stderr SHA-256 `1a278e8e17ed078eee3dac5bc3271b89c193140dcb10025dfd16affb2ac1b99b`.
- Seven files individually matched bytes and SHA-256 in the final integrity audit.
- Protected paths all PASS; frozen C11-C manifest remains 796,318 bytes / `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.
- Test WAVs only in a temporary directory. No production audio, renderer or FFmpeg mux.

## Engineering decision rationale

1. **Do not invent missing E1 parameters.** The V5 spec requires `music_seed`, style profile, tempo, duration and variation. E1's D9.9-resolved intent did not define a general tempo/duration policy. E3.2 therefore binds identity/provenance and leaves unavailable dispatch values unresolved.
2. **Normalize profile naming explicitly.** The declarative profile uses `profile_id/profile_version`, while the V5 implementation historically read `style_profile_id/style_profile_version` aliases with matching defaults. E3.2 performs an explicit identity-checked mapping without changing synthesis behavior.
3. **Keep Challenge-only D3 V5 dependency scoped.** Loop/Drill requests must not load or pin the Challenge V5 profile; their existing family music route remains untouched by E3.2.
4. **Retain the independent seed domains.** `request.seed` belongs to visual/gameplay generation; `request.music_seed` belongs to music. A change to the latter must not rerender or mutate the visual stream.
5. **Do not call V5 from E1 prepare.** E1 remains a side-effect-free canonical request/intent service. The actual dispatch happens in the later E runner through the GUI-facing service path.

## Historical corrections carried forward

- `104 BPM` is present in the historical D9.2 runner's fixed CH001 pilot invocation. It is not a general BPM default in the V5 spec/profile or D9.2 prose contract.
- The V5 CLI's `duration=4` fallback is not a production timing policy. The E3 duration must be derived from a verified visual artifact.
- D3.3's 30-second window is used for loudness measurement/mastering. Final E3 audio must be aligned to the actual visual duration; 30 seconds must not leak into a 9-second MP4.
- D9.2's AAC 192k/48k/stereo and 0.15-second A/V duration tolerance are historical Challenge pilot implementation values, to be reverified against active sources before use.

## Next gate

E3-A source-pin refresh and active contract review, followed by Challenge raw WAV, D3.3 mastering, mux, FFprobe, deterministic/negative tests and an actual Producer GUI run. No physical E3 execution is claimed by this decision.
