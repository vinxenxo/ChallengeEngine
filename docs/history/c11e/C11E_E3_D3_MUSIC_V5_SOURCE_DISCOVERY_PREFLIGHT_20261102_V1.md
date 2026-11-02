# C11-E E3 — D3 Music V5 Source Discovery and Preflight Test Plan V1

**Date:** 2026-11-02
**Entry authority:** `C11E_E2_R4_FORMAL_CLOSURE_DECISION_20261102_V1.md`
**Current state:** `E3_OPEN_FOR_READ_ONLY_SOURCE_DISCOVERY`

## Purpose

Locate and pin the authoritative D3 Music V5 contract, schema, implementation, validators and tests in the active Windows checkout. The first E3 test is discovery/preflight only. It must not produce audio, invoke the music renderer, invoke a production video renderer, or execute FFmpeg mux.

## Contract facts already established at the roadmap level

- The production request has independent domains `request.seed` (gameplay) and `request.music_seed` (music).
- No automatic seed generation or cross-domain RNG consumption is permitted.
- Same music seed and same canonical inputs must deterministically reproduce the music selection/render.
- Changing only `music_seed` must affect the audio selection/output, not gameplay frames or the gameplay seed domain.
- Final A/V assembly uses FFmpeg; FFprobe validates both streams and their timing.

These are the required properties, not a substitute for the concrete D3 Music V5 specification. Do not guess its implementation or media settings.

## Read-only discovery test

`tools/c11e/e3/RUN_C11E_E3_D3_MUSIC_V5_PREFLIGHT_20261102.ps1` checks the E2 closure evidence, branch ancestry, Git cleanliness and frozen C11-C manifest. It then inventories source/document/test candidates in the approved project locations, recording path, SHA-256, size, and matching lines for D3 Music V5 identifiers, `music_seed`, deterministic selection/render, audio, FFmpeg and FFprobe. Results are written under the user's Documents folder, not into the repository.

Expected output categories:

- exact D3 Music V5 specification/contract candidate(s);
- schema and request-field definition;
- music selection/render implementation;
- audio asset/configuration and duration policy;
- FFmpeg mux integration and options;
- FFprobe validators and stream/timing assertions;
- positive, negative, and deterministic tests;
- all source pins needed for the E3 test harness.

A discovery result with no exact D3 V5 contract or no matching implementation/tests is `BLOCKED_SOURCE_DISCOVERY_INCOMPLETE`, not PASS.

## E3 functional acceptance tests (must be derived from the discovered contract)

1. Same canonical request + same `music_seed` twice: same music selection and deterministic audio output (define byte/hash equality versus decoded-sample equality according to the source contract).
2. Change only `music_seed`: audio selection/output changes while gameplay seed, canonical gameplay inputs and gameplay video frames remain identical.
3. Change gameplay `seed` only: music result remains identical when `music_seed` and all music inputs stay fixed.
4. Reject missing, wrong-type, out-of-range, or forbidden automatic music-seed values as the active schema requires.
5. Reject missing/invalid music catalog/assets/configuration and invalid render output as the active D3 validator requires.
6. FFmpeg mux: verify the actual D3-specified codec, sample rate, channel layout, bit rate, fade policy, duration policy and any mapping/options. Do not invent or normalize these values before reading the contract.
7. FFprobe: verify video/audio stream count, codecs, sample rate, channels/layout, stream start times, durations, offsets, end alignment and A/V synchronization using contract-specific tolerances. Check audio is not truncated.
8. Negative mux/probe cases: missing audio, invalid container/codec, truncated audio, incorrect duration/offset and synchronization failure must be rejected using the contract's expected failure behavior.
9. Prove no audio randomness consumes gameplay RNG and no gameplay randomness consumes music RNG.

## Prohibited until contract review

No audio render, test music file, production MP4, mux, media-side effect, source edit, C11-C generator/mechanic edit, or release/governance mutation. No E4A/B/C adapter work starts as a side effect of E3 discovery.

## Exit of discovery preflight

Only after the D3 V5 contract, implementation and test sources are identified and source-pinned may an exact E3 test runner be authored. The next engineering response must first review the generated discovery JSON and selected source files, then freeze a test matrix and run the non-rendering unit tests. Physical audio/mux tests require their own fresh RequestId and separate evidence receipt.
