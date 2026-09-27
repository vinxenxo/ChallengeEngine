# Video Challenger + Asset Recovery — Starting Point

## Why this phase is next

The project has now accumulated the visual-generation experience, regression discipline and production know-how needed to recover the original Video Challenger family without mixing mechanics truth with presentation experimentation.

## Existing challenge corpus in the frozen baseline

| ID | Mechanic | Seed | FPS | Duration |
|---|---|---:|---:|---:|
| CHALLENGE_001 | key | 193847 | 60 | 9 s |
| CHALLENGE_002 | parking | 987654 | 60 | 10 s |
| CHALLENGE_003 | pilot | 314159 | 60 | 12 s |
| CHALLENGE_004 | parking_v2 | 314159 | 60 | 15 s |
| CHALLENGE_005 | hit_v1 | 998877 | 60 | 7 s |
| CHALLENGE_006 | catch_v1 | 884422 | 60 | 9 s |
| CHALLENGE_007 | find_v1 | 7770001 | 60 | 10 s |
| CHALLENGE_008 | choose_v1 | 20260824 | 60 | 11 s |
| CHALLENGE_009 | count_v1 | 20260901 | 60 | 11 s |

## Current asset surface

The frozen baseline contains 15 C6 asset files under `assets/c6/`, including backgrounds, targets, mechanic objects and transparent/cursor assets.

The next step is to map **challenge → mechanic → asset role → presentation binding → provenance → authoring/runtime contract**.

## Rule for new work

Do not add a new asset merely because a renderer lacks a desired visual. First determine whether the original challenge intended that asset, whether a vector/constructed asset is sufficient, and where asset truth belongs in the architecture.
