# C11-E Next Window Start Prompt — V24

Continue `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`.

## Read these documents first

1. `docs/current/e/C11E_CURRENT_AUTHORITY_20261103_V24.md`
2. `docs/current/e/C11E_GATES_ACCEPTANCE_MATRIX_20261103_V24.md`
3. `docs/current/e/C11E_EXECUTION_HYGIENE_AND_ASSISTANT_ERROR_LOG_20261103_V20.md`
4. `docs/current/e/C11E_GUI_PRIMARY_WORKFLOW_AND_CLI_COMPATIBILITY_20261103_V1.md`
5. `docs/current/e/C11E_E3_EXECUTION_BACKLOG_20261103_V1.md`
6. `docs/history/c11e/C11E_E3_2_FORMAL_CLOSURE_AND_DECISION_RECORD_20261103_V1.md`
7. `docs/history/c11e/C11E_ARCHITECTURE_DECISION_RECORD_AND_BACKLOG_20261103_V1.md`
8. `docs/history/c11e/C11E_E3_CHALLENGE_AUDIOVISUAL_IMPLEMENTATION_PLAN_20261103_V1.md`
9. `docs/history/c11d/C11D_TO_C11E_FULL_FAMILY_ROADMAP_20261103_V14.md`
10. `prompts/C11E_CONTINUATION_MASTER_PROMPT_20261103_V24.md`

Also read live `AGENTS.md` and `.continue/rules/CONTINUE.md`, reconcile their current contents, and apply the C11-E authority boundaries. The active checkout always outranks ZIP snapshots.

## Known base before this documentation overlay

E3.2 code commit: `3cc1caa6d740b1525a4ebb30a4ff7f02868ac5a8`; parent `a30b63d31b2d071ebab9c67ec9f8ff7393731488`; tree `de8a1180f04eb0f5e0ea5c8130eedaaccf7e78fa`. Branch `main`, last supplied worktree clean, `ahead 4`. After the user applies and commits this docs overlay, capture the new actual HEAD/tree. Do not use the pre-doc HEAD for any subsequent code installer.

## First engineering action after the docs commit

Refresh current source pins and the GUI runtime state. Then build the next code overlay for E3 Challenge audio integration. Use the accepted E2 R4 MP4 as the video input and verify it by receipt/hash; do not rerender gameplay for a music-seed change. GUI is the manual operator workflow. CLI is only an automated separate-process test of the same service.

## E3 first audio pilot constraints

- D3 V5 `challenge_8bit_v1`, `music_seed` independent of gameplay `seed`.
- Pilot fixture `tempo_bpm=104`, `variation_index=0` comes from the historical D9.2 runner only; do not make it a global default.
- `duration_seconds` must come from FFprobe-verified visual frame count/rate/duration; do not use the engine's CLI duration default.
- Preserve raw WAV. Follow active D3.3 30-second measurement/mastering precedent; create a final audio stream aligned to video duration, never 30 seconds untrimmed in the R4 9-second MP4.
- Mux video by stream copy; use pinned D9.2 AAC 192k/48k/stereo precedent and 0.15s tolerance only after refreshing source hashes.
- FFprobe exactly one video and one audio stream; no video frame change; deterministic repeat and changed-seed audio tests; negative controls; structured receipt.
- No renderer invocation in E3 audio attach; no production audio/release mutation.

## Family roadmap

After E3, implement E4A Challenge, E4B Loop and E4C Drill presentation/editorial binders. Preserve C11-C music generators: Challenge uses D3 V5; Loop/Drill retain family/grammar C11-C audio through a verified audio-only E adapter. Then E5 seed isolation/determinism/parity, E6 Smoke18, E7 Matrix101 (54+27+20; two Challenge cases held, provisional 99 runnable), E8 independent acceptance/freeze/promotion.

C11-C 2.19.12 remains production authority; release authority NONE until E8. Do not modify `core/audio`, protected C generators/mechanics, frozen manifest, D4.8 or D9.10 locks. No sixth suite module or `c11d-control`.
