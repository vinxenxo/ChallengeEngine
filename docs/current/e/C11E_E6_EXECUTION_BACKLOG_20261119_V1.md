# C11-E E6 Execution Backlog — 2026-11-19 V1

**Target:** bounded Smoke18 visual render with editorial, music and layout, followed by A/V qualification and human review.  
**Current E6 accepted:** 0/18.

| ID | Work item | Entry condition | Exit evidence | State |
|---|---|---|---|---|
| E6-N01 | Diagnose Loop Policy V2 receipt status/A.3 mismatch | Existing V2 receipt and new overlay | Receipt fields consistent; active A.3 bridge/archive/current/model pins pass | NEXT |
| E6-N02 | Loop D-owned Option C post-compositor contract implementation | E6-N01 genuine PASS | Six-family static tests; source-frame invariance; four canonical fields; exact geometry | BLOCKED_BY_N01 |
| E6-N03 | Challenge E6 editorial successor consumer | Existing 18 PREPARE_ONLY envelopes | 54 positive windows; GAME fallback only at zero-frame primary; native hook migration guarded by show_hook | PREPARE_ONLY |
| E6-N04 | Freeze Smoke18 row/reuse predicates | E6-N01 through N03 pass | 18 frozen rows; 13 reuse rows independently accepted or explicitly retained as candidates | NOT_FROZEN |
| E6-N05 | Scoped D4.8 Smoke18 successor | Frozen matrix and source/tool contracts | New versioned policy explicitly supersedes only scoped TEST_ONLY clauses; original V2 unchanged | DRAFT_REQUIRED |
| E6-N06 | Exact E6 TEST_ONLY execution manifest | E6-N05 and tool inventory | Absolute executable paths, SHA/version, argv allowlists, process counts, output roots, stop-on-first-failure | NOT_ISSUED |
| E6-N07 | Visual render: six Loop D compositions and five fresh Challenge AV source groups | N01–N06 pass | Output hashes, frame/profile/timebase, visual review receipts | NOT_STARTED |
| E6-N08 | Challenge family music/A/V variants | Visual source QA and approved music fixture | A/B repeatability, C seed difference, AAC-LC, 48kHz stereo, non-silence, drift | NOT_STARTED |
| E6-N09 | Reuse Drill and CH004 candidates against frozen row predicates | E6-N04 pass | Exact predecessor receipt/media/profile/timebase/review predicates | NOT_ACCEPTED |
| E6-N10 | Operator visual/editorial/layout and audio review | Outputs present and hashes pinned | Per-row human decisions keyed to exact media hashes | NOT_STARTED |

## Rules

- Do not rerun accepted predecessor media to repair a ledger.
- Do not promote a candidate to E6 acceptance from a linked SHA alone.
- Do not invoke renderer, Godot, FFmpeg/FFprobe, audio, mux or media before the scoped successor and exact process manifest are pinned.
- Stop on first process failure. No automatic retries, no overwrite, no BatchId reuse.
- Keep E1 PREPARE_ONLY and all production/release locks intact.
