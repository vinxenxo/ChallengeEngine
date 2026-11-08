# C11-E R1V prior Fractal A lineage-schema correction — V1

**Date:** 2026-11-08. **Status:** V1.1 install PASS; wrapper fail-closed before capture; correction prepared, not yet installed.

## Evidence reviewed

- User evidence archive `r1v_av_qualification.zip`, SHA-256 `749107a2d73a49e7b383ec4b0449583eed13052bc78312bf8c789e46c85a1bd5`, ZIP integrity PASS, eight entries.
- V1.1 installer receipt `R1V_AV_INSTALL_20261108_010626_76F32276`: `PASS_ADD_ONLY_INSTALL`, 21/21; install receipt hash `256b774a5e45763e56d22c6583c637e53515813678b5e7dbab53b124b71e6b00`. Frozen C11-C manifest SHA remains `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.
- Wrapper receipt `R1V_AV_WRAPPER_V1_20261108_000635_3E5304E1`, SHA `109364524d3101959d6a18baaf8a906d74256040edba17b8e5073a934fde6b7f`: 52 tests, 1 error, 0 failures, 0 skips; `capture_exit_code=null`; no launcher started.
- Exact failing test: `test_20_prior_fractal_bloom_a_capture_is_reusable_and_pinned`.
- Prior report SHA `19b96a87be957a3c97f57828991651aaa72baec08a33a099f145263d89f71ebb`; prior process receipt SHA `c22404dca13f34216769d87b311ae81670adc6102fda72851d3156ed83907134`; prior Fractal A MP4 SHA `7971ced1d9cdbb7dd76a0d8d76e766faa9a051fc27419c9e737c41264796f659`. They match the original evidence archive and the pinned constants.

## Root cause

The V1.1 function `verify_prior_fractal_a()` queried `report.governance.d4_8_production_policy_state`, a field absent from the genuine accepted V3 report. The schema stores `DISABLED_UNCHANGED` under `report.approval.d4_8_production_policy_state`. The governance object uses `d4_8_general_production=BLOCKED`, `d_renderer_dispatch=OFF`, and `release_authority=NONE`.

This is a new-validator schema-path bug; the parent report has not lost its policy or provenance. It is not a C11-C launcher, video, audio, mux, source-pin, R1P or Option C failure.

## Correction boundary

The patch changes only the lineage assertion in `tools/c11d/d9/c11e_r1v_av_family_qualification_v1.py` to bind the actual schema and assert every production lock explicitly. The 52-test count, wrapper, runner, selectors, seeds, audio profiles, command lines, mux settings, policy, approval and allowed outputs remain unchanged. It updates Authority/Roadmap/Backlog/Gates/Blocker/Runbook/Index and Master/Start/First prompts.

## Operator sequence

1. Do not install the V1.0 Library package; it is not installed in the active checkout and is not a prerequisite.
2. Install the lineage-fix V2 overlay, which preflights exact existing V1.1 hashes and frozen/governance pins.
3. Run the existing integrated wrapper once. The prior Fractal A capture is reused; do not rerun it. R1P and Option C are not repeated.
4. Only if all 52 tests pass with zero skips/errors/failures does the one integrated A/V capture flow start.

No general production activation, renderer/dispatch change, D compositor, release authority or downstream phase unlock is implied.


## V1 installer package-preflight defect and V2 correction (2026-11-08)

The first lineage-fix installer package did not copy or replace any files. Its complete preflight stopped at the first new versioned document path (`C11D_E_BLOCKER_REMEDIATION_REGISTER_20261108_V17.md`) because the manifest incorrectly classified a new versioned filename as `PINNED_REPLACE` and looked for V16 bytes at the V17 path. The same operation-type mistake affected other versioned documentation targets.

V2 corrects the operation model: versioned successor documents are `ADD` targets, while their installed predecessor filenames (V16, V42, V95, V56, V70, V93, Runbook V8, Master/Start V96 and First V20) are separately SHA-256/size-pinned in `verify_existing`. Only the Python validator module is a same-path `PINNED_REPLACE`, with its exact V1.1 predecessor hash. The V1 attempt was a no-op due to preflight failure; do not repair it manually or install V1.0.
