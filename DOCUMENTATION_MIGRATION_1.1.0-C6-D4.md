# Documentation migration — 1.1.0-C6-D4

## Why this exists
The repository accumulated checkpoint documents whose historical “current” sections outlived the contracts they described. This note records the cleanup boundary without rewriting historical evidence.

## Rules
- Historical checkpoint handovers remain unchanged in meaning and are not used as live status.
- Current docs must identify C6-D4 as the live checkpoint.
- FIND is no longer described as a draft candidate; it is part of the frozen 1.0.0 baseline.
- `factory_version = 0.10.0` is the current factory implementation version; the frozen 0.9.0 provenance contract remains a historical/normative schema baseline.
- Per-challenge video duration is governed by the four `video.*_duration` fields and `VideoTimeline.gd`; zero omits a phase and GAME remains mandatory.
- Output files/manifests from prior renders are evidence only when their physical artifacts and hashes are available and match the current source definition.
