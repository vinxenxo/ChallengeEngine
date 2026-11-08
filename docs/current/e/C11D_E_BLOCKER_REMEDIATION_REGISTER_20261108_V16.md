# C11-D/E Blocker Remediation Register — V16

## R1V capture-log false negative

- Prior C11-C launcher for Fractal Bloom A exited 0 and created a valid silent H.264 MP4; operator visual review confirms the Loop/layers are correct.
- V3 runner failed after one launcher because it expected ASCII `720x1280@30`; Godot 4.7.1 writes UTF-16LE with `720×1280 @ 30 FPS`. It also expected `yuv420p/tv` where C11-C produced `yuvj420p/pc`. This is a validator bug, not a launcher failure. Reuse the existing pinned capture; do not rerender A.

## R1V audio integration amendment

- Operator approved the bounded integrated A/V qualification (5 × A/B = 10 outputs, 9 new source captures + reused Fractal A). Use existing C11-C FAMILY_MUSIC_V4 helper and profile registry. Pass R1P music_seed; never gameplay seed.
- Loop music profiles remain C11-C family-specific; do not use D3 V5 (Challenge-only). Preserve H.264 with `-c:v copy`, mux only AAC 192k/44.1k/stereo, FFprobe the final container.
- Old R1V silent-only policy and approval are immutable. New amendment supersedes only the prohibition of audio/mux for this exact R1V A/V test. General D4.8 policy still DISABLED.

## Final review findings before integrated A/V package

- The original source capture confirms Godot writes a Unicode multiplication sign and spaces in the Movie Maker geometry line; the parser accepts UTF-16LE BOM and exact dimensions/FPS/frame count. Source pixel-format/range is pinned to observed `yuvj420p/pc` or the explicit alternative `yuv420p/tv`; mismatched pairs fail closed.
- Five native C11-C FAMILY_MUSIC_V4 WAVs and repeated outputs were tested locally for deterministic PCM16/44.1 kHz/stereo and profile RMS/peak limits. A reference AAC mux confirms H.264 elementary-stream identity with `-c:v copy` and a separate AAC stream. These are local engineering validations, not Windows A/V qualification receipts.
- Second installer review corrected two schema/path issues before packaging: the new amendment/approval files are validated from the ZIP payload before installation; the Option C installation receipt uses `status`, not `install_status`. The combined test report includes skip count and Windows wrapper requires zero skips.

## Apply and execution safeguards

- Installer V4 is PowerShell-only, with no Python invocation or repeated test suite. It verifies every payload hash, parent evidence, policies, source pins, PowerShell AST and collisions, then add-only copies.
- Wrapper runs one combined 52-test suite through direct Python 3.13 and redirected native streams. No standalone tests or manual launchers.
- Different-byte collisions abort; identical files verify/skip; no overwrite. Preflight checks Fractal A evidence and all output/temp roots. Runner stops fail-closed and preserves partial evidence; no cleanup or rerun of prior roots.

## Other historical blockers

- E4A.6 `GeneradorMaestro.gd` postimage remains a known baseline candidate-policy conflict. Do not restore it or soften the candidate rule; progress with the independent Option C D compositor.
- D compositor is not implemented. D9.10 PREPARE_ONLY.
- D9.14/D9.16 BLOCKED, D9.17 BLOCKED_NO_GO, D10 BLOCKED_FOR_PROMOTION, release authority NONE.
- E4C Drill, E5, Smoke18, Matrix101 and E8 remain downstream. CH_008/009 remain held until the 11s/12s timing contradiction is formally resolved.

No Git inspection/bookkeeping. Operator owns commits. C11-C 2.19.12 and all protected paths remain immutable.
