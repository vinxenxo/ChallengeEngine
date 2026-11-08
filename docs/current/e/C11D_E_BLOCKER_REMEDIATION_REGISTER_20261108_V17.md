# C11-D/E Blocker Remediation Register — V17

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


## Active R1V A/V preflight blocker — prior report lineage field mapping

**Observed:** V1.1 add-only installation passed 21/21. The integrated 52-test wrapper then failed with one error in `test_20_prior_fractal_bloom_a_capture_is_reusable_and_pinned`; it started zero launchers. Evidence ZIP SHA-256: `749107a2d73a49e7b383ec4b0449583eed13052bc78312bf8c789e46c85a1bd5`. Wrapper receipt: `R1V_AV_WRAPPER_V1_20261108_000635_3E5304E1`, SHA-256 `109364524d3101959d6a18baaf8a906d74256040edba17b8e5073a934fde6b7f`.

**Root cause:** `verify_prior_fractal_a()` incorrectly requested `report.governance.d4_8_production_policy_state`. In the exact accepted prior report schema, the field is `report.approval.d4_8_production_policy_state = DISABLED_UNCHANGED`; general production lock is `report.governance.d4_8_general_production = BLOCKED`. Also require `d_renderer_dispatch = OFF` and `release_authority = NONE`. The report, process receipt and prior Fractal MP4 hashes match the hard pins; this is not missing/corrupt evidence and not a launcher or audio failure.

**Remediation:** a source-pinned update changes only the lineage assertion in `c11e_r1v_av_family_qualification_v1.py` and advances current docs/prompts. It does not change the A/V runner, test count (52), seeds, music route, capture command, mux, scope policy or authorization. Installer preflights exact V1.1 code/doc hashes and existing approval/frozen-baseline pins. Then execute the integrated wrapper once; 52 tests, zero skips/errors/failures are mandatory before any launcher.

**Do not:** install the Library V1.0 package as a workaround; rerun Fractal A, R1P or Option C; manually run tests or individual launchers; create a silent-only phase.


## Lineage-fix installer packaging correction

The first lineage-fix installer package V1 failed complete preflight because it treated successor document paths (V17/V43/V96 etc.) as existing same-path replacements. It made no filesystem changes. V2 adds those new versioned documents and pins the actual V1.1 predecessor paths/hashes; only the Python validator is same-path pinned replacement. Do not install Library V1.0 and do not manually create successor documents.


## Lineage-fix installer V1 packaging defect — superseded by V2

The first correction installer V1 stopped at complete preflight on `docs/current/e/C11D_E_BLOCKER_REMEDIATION_REGISTER_20261108_V17.md`, because it treated a new successor-version path as an existing same-path replacement. No files were copied/replaced. Actual installed predecessor is V16 (SHA `4b1ab75a5610d4996100340c44c57573c8594ee0cff8d25bb126acb2c0ca2380`). V2 uses ADD for all successor-version documents and pins the real predecessor paths separately. It uses same-path PINNED_REPLACE only for the Python validator, with exact installed V1.1 SHA.
