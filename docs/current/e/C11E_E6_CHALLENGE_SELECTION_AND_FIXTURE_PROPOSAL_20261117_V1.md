# C11-E E6 Challenge six-selector and fixture proposal — V1

**Date:** 2026-11-17  
**Disposition:** `WORKING_SELECTION_PLAN_ONLY / NOT_MEDIA_AUTHORIZATION`  
**Parent gate:** E6 read-only audit V2 `PASS_AUDIT_READ_ONLY_EVIDENCE_RECONCILED_EXECUTION_HELD`  
**Purpose:** Prepare and validate six Challenge E1 TEST intents and six matching D editorial-envelope plans, each with A/B/C fixture rows, without executing media.

## 1. Proposed six-selector set

| Selector | Mechanic | Gameplay seed | Canonical phases (s) | Source fps / frames | Proposed REVIEW_720 fps / frames | Disposition |
|---|---|---:|---:|---:|---:|---|
| CHALLENGE_001 | key | 193847 | 0+7+0+2 = 9 | 60 / 540 | 30 / 270 | SELECTED |
| CHALLENGE_002 | parking | 987654 | 3+7+0+0 = 10 | 60 / 600 | 30 / 300 | SELECTED |
| CHALLENGE_004 | parking_v2 | 314159 | 3+7+3+2 = 15 | 60 / 900 | 30 / 450 | SELECTED — accepted E4A.7 anchor |
| CHALLENGE_005 | hit_v1 | 998877 | 0+7+0+0 = 7 | 60 / 420 | 30 / 210 | SELECTED |
| CHALLENGE_006 | catch_v1 | 884422 | 0+7+0+2 = 9 | 60 / 540 | 30 / 270 | SELECTED |
| CHALLENGE_007 | find_v1 | 7770001 | 3+7+0+0 = 10 | 60 / 600 | 30 / 300 | SELECTED |
| CHALLENGE_003 | pilot | 314159 | 3+7+0+2 = 12 | 60 / 720 | — | EXCLUDED — explicit RNG-isolation pilot and duplicates CHALLENGE_004 gameplay seed |

CHALLENGE_008/009 remain excluded and are not part of the seven-candidate pool because their declared 11-second duration conflicts with 12 seconds of canonical phase sum. The producer schema declares `phase_sum_only; legacy total_duration is ignored`; CHALLENGE_002 is therefore 10 seconds from its canonical phases, not its legacy `test_master_11s` label.

The six selected IDs have six distinct mechanics and six distinct gameplay seeds. This is the working selection for this plan-only step. It becomes a frozen Smoke18 selection only after source pins are verified in the active checkout and the subsequent E6 manifest/governance process is complete.

## 2. Proposed A/B/C music fixture proposal

- Family profile: `challenge_8bit_v1`, version `1.0`.
- A/B music seed: `840001`.
- C changed-music seed: `840002`.
- Historical tempo fixture: `104 BPM`, from the D9.2 fixed pilot/E4A.7 precedent.
- Variation index: `0`.
- Proposed duration source: each selector's canonical phase sum, not a global fixed duration.

These are test-fixture proposals only, not product defaults, not a music-seed authorization, and not a D3 invocation. E1 intents intentionally preserve `tempo_bpm=null` and `duration_seconds=null`, with `PLANNED_NOT_RENDERED`, `dispatchable=false`, and no generated audio. The E1 service remains the authority for the preparation contract; the fixture proposal remains outside its unresolved engine parameters.

All six gameplay seeds are distinct from 840001 and 840002. A/B/C are planned as three request rows per selector (18 total): A and B repeat the same gameplay/music seeds; C changes only the music seed. No audio is rendered in this step.

## 3. Evidence reuse anchor

CHALLENGE_004 remains selected because it is the only Challenge selector with accepted E4A.7 D-composited A/V evidence. The accepted evidence is scoped to CHALLENGE_004, a 15-second `challenge_8bit_v1` review, gameplay seed 314159, A/B music seed 840001 and C music seed 840002. This is not generalized evidence for the other five selectors and does not prove a multi-selector executor.

## 4. Plan-only output contract

This proposal prepares exactly:

- 18 E1 TEST intents validated as `PASS_E1_PREPARATION_ONLY`.
- 18 D editorial envelopes validated statically for schema, selector identity, source timebase and phase ranges.
- One selector plan and one immutable plan-only receipt with SHA-256 sidecars.

The D envelope's frame ranges use canonical source frame indexing at 60 fps. REVIEW_720 frame-count values at 30 fps are planning metadata derived from the phase sum; they are not a render command or a Godot-approved runtime mapping.

## 5. Explicit exclusions

This proposal does not:

- invoke Godot or the live Challenge scene;
- invoke the E4A.6 builder, E4A.7 A/V runner, E3 D3 audio pipeline, FFmpeg or FFprobe;
- synthesize PCM/WAV/AAC, mux, render, export, dispatch or create media;
- reserve a Smoke18 BatchId;
- modify C11-C, D4.8, the producer schema, family binders, E1 service or any protected source;
- grant media, renderer, production, release or promotion authority.

D4.8 R1V V2 remains unchanged and forbids Smoke18, D3/audio/PCM and FFmpeg filters/mux. A separate E6 TEST_ONLY authorization is mandatory after the exact 18 rows, reuse rules, executors, tools, arguments, outputs and stop conditions have been frozen and governance approval has been recorded.
