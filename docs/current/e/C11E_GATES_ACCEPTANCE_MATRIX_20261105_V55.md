# C11-E Gates and Acceptance Matrix — V55

| Gate | Current state | Exit evidence / boundary |
|---|---|---|
| E0–E3 | ACCEPTED within declared scopes | Preserve prior evidence; do not rerun absent drift/defect. |
| E4A.2 | ACCEPTED TEST-ONLY | Real Challenge_004 body/source control. |
| E4A.3D.1 | PASS — isolated D compositor proof | 6/6 real frames; 18 PNG; 12 pixel comparisons; BODY identity and single CTA owner; placement approval still separate. |
| E4A.4 | PASS — isolated D3 V5/D3.3 audio/mux TEST-ONLY | Same-seed repeatability, changed-seed audio difference, AAC 48 kHz stereo, FFprobe, non-silence, zero measured A/V drift. Input video has no D compositor; operator review pending. |
| E4A.5B | PASS — source review and active root pins | Root/launcher/QA seam reviewed; V3 used active Git checkout. |
| E4A.6 live-root runtime | PASS_TEST_ONLY | V3: PS5 AST, Python 17/17, Godot 4.7.1 root PASS, 900 frames, 1 mount, HEADER 180, FOOTER 120, native CTA 0. |
| E4A.6 pixel/geometry | OPEN — next action | Silent Movie Maker visual-only capture, FFprobe 540x960/60/900 and 720x1280/30/450, eight phase-boundary stills; independent layout review required. |
| E4A final | OPEN | D-composited Challenge MP4 + D3 V5 audio, final FFprobe/non-silence/A/V drift, same/different music seed with gameplay identity, operator visual/audio review, GUI/CLI parity. |
| E4B Loop | HELD | Do not begin until full E4A accepted. Preserve 27 grammar/variant identities and existing Loop music. |
| E4C Drill | HELD | Do not begin until full E4A accepted. Preserve 20 variants, phases, END_CTA and existing Drill music. |
| E5 | PENDING | Cross-family determinism, independent gameplay/music seeds, no adapter/profile leakage, GUI/CLI parity. |
| E6 | PENDING | Smoke18: six audiovisual scenarios per family. |
| E7 | PENDING | Matrix101: 54 Challenge + 27 Loop + 20 Drill. CH_008/009 held until timing authority resolves 11s vs 12s. |
| E8 | BLOCKED | Full historical C11-C regression mapping, independent acceptance, immutable freeze and explicit separate promotion. |

## Non-negotiable invariants

C11-C 2.19.12 manifest remains `e405d08e4d166b1ad9595358f4a088e73eea9527e6e89244beb4096eac4b953`. No C mechanics/generator/binder/timeline/RNG mutations; no sixth module or parallel producer. `request.seed` and `request.music_seed` remain independent; no automatic seed generation; do not serialize all `FrameSnapshot.custom_data`. Production renderer/dispatch/media OFF; `release_authority=NONE`.
