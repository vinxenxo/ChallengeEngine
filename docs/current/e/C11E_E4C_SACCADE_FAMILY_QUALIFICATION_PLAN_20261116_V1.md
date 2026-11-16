# C11E_E4C_SACCADE_FAMILY_QUALIFICATION_PLAN_20261116_V1

## Saccade qualification plan — 0/5 pending execution — 2026-11-16

### Scope

Qualify visual drill family `saccade`, tiers 1–5, through the existing CLI facade and shared D drill executor/visual composition consumer. This is a coordination and qualification driver, not a new Producer, binder, renderer, mechanic, compositor or audio engine. All five tiers are new Saccade outputs; the accepted Tracking CLI smoke is only a request-schema template. No Pursuit outputs or any other family may be reused as a Saccade tier.

### Pinned native contract

- Canonical path: `definitions/visual_drill_saccade_canonical.json`.
- Canonical SHA-256: `daba3fa558f6898a17107ab68894d15c58fa5b2127e8da7d7b11b203f4ddfaa1`.
- Native gameplay: 17.0 seconds, 510 frames, 30fps.
- D presentation phases: PRE_ROLL 3.0s /90 frames; GAME 17.0s /510 frames; END_CTA 3.0s /90 frames.
- Expected composed stream: 690 frames /23.0 seconds at 30fps.
- Family music profile: `CIRCUIT_PULSE`.
- Gameplay seed: 12345; A/B music seed 840001; C uses a distinct derived music seed through the existing executor.

Do not modify the canonical definition, difficulty profile, family mechanic, RNG domain, binder, consumer, D executor or C11-C source. The coordinator verifies the canonical hash and derives the composed total from the pinned definition plus the existing 3s/3s consumer phases.

### Technical acceptance per tier

1. Request binds exactly `visual_drills/saccade/tier-N`, Spanish editorial, audio on and personalization enabled.
2. Existing CLI returns `PASS_E4C_DRILL_SINGLE_SELECTOR_A_V_QUALIFICATION`, process exit code zero.
3. Qualification receipt identifies family `saccade`, tier N, profile `CIRCUIT_PULSE`, 690 total frames, 23.0 seconds, phase counts 90/510/90.
4. FFprobe: 720x1280, 30fps, H.264 High, yuv420p, TV range; AAC-LC, 48kHz, stereo; zero A/V start drift.
5. A/C video bitstreams are identical while A/C audio bitstreams differ. A/B music generated at the same seed is identical; C changed-seed music is distinct.
6. A/B/C music paths and final A/C video paths physically exist and match receipt SHA-256.
7. Three independently captured 91-row source inventories (pre-execution, immediately pre-renderer, post-execution) are equal and each path is safe, unique and physically rehashed.
8. Coordinator reruns all its 37 source pins after each child; source pins and frozen C11-C manifest remain unchanged.

### Batch and failure policy

Default driver mode is `PREPARE_ONLY`. Prepare-only must check environment, all source pins, style guides, canonical timebase, base CLI template, output collisions and a new BatchId plan without creating authorization markers or media. The installer only invokes this default path.

Only a separate explicit `-Execute`/`--execute` authorizes execution. Driver creates a fresh `E4C-SACCADE-T1-5-...` BatchId and an ATTEMPT_RESERVED lock plus EXECUTION_AUTHORIZED_ONCE marker before invoking tier 1. All five tiers run sequentially and fail-fast. Any failed child, timeout, missing result, media/receipt mismatch, source drift or post-child audit failure consumes the BatchId. Preserve all evidence and do not retry that ID. An output or evidence-root collision must fail before authorization.

### Operator acceptance

After all five technical receipts pass, the operator reviews final A and C video and A/B/C family music for each tier. Confirm layout, typography, title role, subtitle/CTA, editorial, visual identity, behavior and audio. No operator acceptance is implied by installer PASS, PREPARE_ONLY, technical receipts alone, or another family's acceptance.

### E4C progress and next work

Tracking 5/5 accepted; Pursuit 5/5 accepted; Saccade 0/5; Peripheral Scan 0/5. E4C total 10/20. After Saccade closes, Peripheral Scan follows under `ORBITAL_RITUAL`. E4C closes only at 20/20; E5 remains blocked until that gate.

### Governance

C11-C frozen manifest SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`, 796318 bytes. E1 PREPARE_ONLY, family adapter NOT_CONNECTED_E1, production dispatch false, release authority NONE. Git checks skipped; commits operator-managed; source pins enforced.
