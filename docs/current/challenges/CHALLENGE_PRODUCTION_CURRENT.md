# Challenge Production — Current 2.17.8

## Scope

Post-freeze production orchestration for CHALLENGE_001…009. This wrapper consumes the existing Challenge definitions and never reimplements gameplay truth.

## Pipeline

```text
challenge JSON
   ↓ copy + seed replacement
phase-sum timeline
   ↓
Godot Movie Maker 540×960
   ↓
source AVI
   ↓
FFmpeg delivery profile
   ↓
MP4 + manifest + social metadata
```

## Historical matrix

| ID | Mechanic | FPS | Duration | Frames |
|---|---|---:|---:|---:|
| 001 | key | 60 | 9 s | 540 |
| 002 | parking | 60 | 10 s | 600 |
| 003 | pilot | 60 | 12 s | 720 |
| 004 | parking_v2 | 60 | 15 s | 900 |
| 005 | hit_v1 | 60 | 7 s | 420 |
| 006 | catch_v1 | 60 | 9 s | 540 |
| 007 | find_v1 | 60 | 10 s | 600 |
| 008 | choose_v1 | 60 | 12 s | 720 |
| 009 | count_v1 | 60 | 12 s | 720 |

## Seed rule

Only the disposable effective definition receives the requested `generation.seed`. The original Challenge JSON is not rewritten.

## Resolution rule

The Challenge runtime/source capture remains 540×960. `MASTER_1080`, `REVIEW_720` and `MIN_540` are output profiles applied after capture. This is the mechanism that permits multiple qualities without changing mechanics or simulation truth.

## Diagnostics

Every failed run retains its complete scratch directory, including effective JSON, command line, stdout, stderr and Godot log.

## Gate

Run one `CHALLENGE_001` smoke and verify source + delivery before starting the 54-run matrix. The bulk QA remains sequential because `override.cfg` is project-wide.
