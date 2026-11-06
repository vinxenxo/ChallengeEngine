# C11-E Gates / Acceptance Matrix — V69

| Gate | Status | Evidence / next condition |
|---|---|---|
| E0 foundation / governance | ACCEPTED | Reuse; do not restart. |
| E1 shared GUI/CLI service | ACCEPTED_BOUNDED; MANUAL_GUI_RUNTIME_PENDING | Automated service bounded acceptance remains valid. E4A closeout still requires an operator-run Producer GUI D9.9 callback and its generated parity receipts. |
| E2 Challenge control | ACCEPTED_BOUNDED | Existing bounded title-to-pixels control; no repeat absent relevant drift. |
| E3 D3 V5 / D3.3 / mux | ACCEPTED_BOUNDED | Reuse accepted method/contracts; E4A.7 now proves isolated D-composited A/V. No production dispatch. |
| E4A.2 Challenge base | PASS_TEST_ONLY | Real C11-C BODY baseline. |
| E4A.3D.1 isolated compositor | PASS_TEST_ONLY | Technical compositor proof only. |
| E4A.4 audio/mux pilot | PASS_TEST_ONLY | Earlier uncomposited C11-C MP4; method precedent only. |
| E4A.5B source review | PASS_STATIC_SOURCE_REVIEW | Latest supplied snapshot reviewed; ZIP is evidence, checkout remains authority. |
| E4A.6 D visual / reserved bands | PASS_TEST_ONLY_USER_VISUAL_REVIEW | Recovery V1.2 receipt `327901...`; silent D-composited H.264 `841b...`; 12/12 inactive black and 4/4 active editorial; user visual review PASS. |
| E4A.7 D-composited D3 V5 A/V | **PASS_TEST_ONLY_AUDITED** | ZIP `RUN_20261106T070808Z-62F31F9C.zip`, SHA `ad4024...`; receipt `102cf0...`; 267/267 checksums. D3 raw/master A/B repeat, C changes; three AAC muxes FFprobe PASS; source H.264 copy identity; 0.000 s A/V drift. Operator listening A/B/C is PASS (user-confirmed 2026-11-06). |
| Full E4A Challenge | IN_PROGRESS · D99_V2_RUNNER_PENDING | V1 runner preflight/tests passed but source replacement failed on a null `File.Replace` backup pathname; V2 repairs installer mechanics. Then one post-patch Producer GUI runtime parity PASS is still required. Operator listening is PASS. |
| E4B Visual Loop | ON_HOLD | Start only after full E4A; preserve grammar/variant timeline, binder and family music. |
| E4C Visual Drill | ON_HOLD | Start after E4B; preserve phase timeline, END_CTA, binder and family music. |
| E5 cross-family determinism | NOT_STARTED | Three-family determinism, independent seed domains, profile/binder non-leakage and GUI/CLI parity. |
| E6 Smoke18 | NOT_STARTED | Six complete A/V cases per family. |
| E7 Matrix101 | NOT_STARTED | 54 Challenge + 27 Loop + 20 Drill; CH_008/009 held; 99 provisional runnable. |
| E8 independent acceptance | NOT_STARTED | Historical C→E regression, independent review, freeze and separately authorized promotion. |

## Hard limits

C11-C 2.19.12 frozen manifest SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`. Renderer and production dispatch/media OFF; D4.8 BLOCKED; D9.10 PREPARE_ONLY; D9.14/D9.16 BLOCKED; D9.17 BLOCKED_NO_GO; D10 BLOCKED_FOR_PROMOTION; `release_authority=NONE`. CH_008/009 unresolved (11 s declared vs 12 s phase sum). All runners avoid Git; operator manages commits.


## E4A.7 listening and D99 GUI disposition update

- E4A.7 automated audio/mux evidence remains PASS_TEST_ONLY; user listening A/B/C is now PASS.
- Full E4A remains IN_PROGRESS. V1 did not apply the source change: `File.Replace(...,$null)` failed and the catch receipt used bare `false` tokens. V2 corrects these runner-only defects and adds the documentation versions add-only. A new post-patch GUI/D9.9/E1 parity run is still mandatory.
- D22A8281E993 artifact reports E1 and D9 parity PASS. It contains `presentation_options` only in the outer `request.json`, not `d9_request.json`; it does not reproduce the separately reported unknown-field exception.
- Surgical fix: remove Hook/countdown UI serialization from Producer `main.py`; preserve E1's existing default. D9.9 strict schema stays unchanged. Preserve all D9.8 editorial key names and `UNKNOWN` empty-value sentinel.


## V2 repair and transition gate

V2 preserves the approved source postimage SHA and focused regression test SHA. It only changes the runner's atomic replacement backup path and PowerShell boolean literals, then installs the new versioned documentation after source/test acceptance. E4B Visual Loop remains ON_HOLD until the new GUI run records E1 and D9 parity PASS, valid lifecycle receipts and the fail-closed renderer/dispatch/media boundary.
