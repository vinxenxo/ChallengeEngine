# Challenge Production — Current C11-C 2.19.12

The nine canonical Challenge definitions remain authoritative. Current production and current review use one canonical Challenge producer path; historical C11-A.1 qualification is a separate compatibility QA surface.

## Current production pipeline

```text
challenge JSON
   ↓ disposable seed-specific definition
phase-sum timeline / definition FPS
   ↓
Godot Movie Maker source 540×960
   ↓
FFmpeg delivery profile
   ├── REVIEW_720 → 720×1280
   ├── MASTER_1080 → 1080×1920
   └── MIN_540 → 540×960
   ↓
MP4 + production manifest + telemetry/logs
```

Challenge delivery never changes mechanic truth, RNG ownership or the frozen logical social geometry.

## Current review

`tools/qa/c11/run_c11c_challenge_bulk_qa.ps1` is the current 9 Challenge × 6 seed review. It derives timing from the four canonical phase fields. An absent optional `reveal_duration` is normalized to zero; stale `video.total_duration` is not authoritative.

## Historical A1 qualification

`tools/qa/c11/run_c11a1_challenge_bulk_qa.ps1` remains the historical 54-run qualification surface. Its current rendering implementation delegates to the canonical producer and writes a deterministic compatibility adapter manifest.

## Seed rule

Only the disposable effective definition receives the requested `generation.seed`. Original Challenge JSON files are not rewritten by QA.

## Diagnostics

Failed runs retain their diagnostic directories. Production and QA are kept separate from durable source/evidence.
