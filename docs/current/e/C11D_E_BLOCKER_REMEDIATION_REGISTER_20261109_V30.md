# C11-D/E Blocker Remediation Register — V30 (2026-11-09)

| ID | Issue | Evidence / cause | Remediation | State |
|---|---|---|---|---|
| E4B-L22-PS-01 | V1 Loop22 wrapper stops during Python unittest invocation | User execution log: `NativeCommandError` at V1 PS1 line 26; unittest normal diagnostics surfaced on native stderr while `$ErrorActionPreference=Stop` | Add-only V2 wrapper uses `System.Diagnostics.Process`, concurrent stdout/stderr drains, explicit exit code, bridge regression tests, persistent logs/receipt | V2 package generated; install/preflight pending |
| E4B-L22-AV-02 | 44 physical audiovisual qualifications | No valid media-run evidence from the failed V1 wrapper attempt | Resume only after V2 install and all preflight tests pass; then execute exact 22×A/B | BLOCKED_BY_V2_PREFLIGHT |
| E4B-L22-HR-03 | Human review of audiovisual outputs | Requires real MP4s from 44/44 technical pass | Operator visual/editorial/layout review and audio listening | NOT_STARTED |

Previously accepted R1P 27/27, R1V pilot and five policy approvals are carried forward without repetition. C11-C and governance locks remain intact. Git checks remain skipped and commits operator-managed.
