# C11-D/E Blocker Remediation Register — V33 (2026-11-09)

| ID | Issue | Evidence / root cause | Remediation / state |
|---|---|---|---|
| E4B-L22-PS-01 | V1 wrapper stopped on unittest stderr | Normal Python child stderr became a PowerShell 5.1 terminating error under `$ErrorActionPreference=Stop` | V2 .NET process bridge installed; bridge/AST/24 tests/prelaunch PASS. Historical failure closed as wrapper defect. |
| E4B-L22-AV-02 | Loop22 runner exit 2 before media | Shared family directory attempted to be created once per job with `exist_ok=False` | Runner V2 plans unique physical directories; isolated 25/25 focused tests PASS. Windows media qualification pending. |
| E4B-L22-RC-03 | Receipt Pin V2 install receipt rejected | Installer receipt constructor writes 63-character `frozen_c11c_manifest_sha256`; semantic post-write validation missing | One-shot repair corrects only this generated receipt field/sidecar, preserves preimage and validates canonical frozen manifest. Pending operator execution. |
| E4B-L22-V4-04 | V4 consumer reads unbound SHA variable | `$BaseV2ReceiptSha` referenced where `$BaseV2ReceiptSha256` is declared | Exact single-reference source-pinned repair. Pending one-shot execution. |
| E4B-L22-AV-05 | 44 physical audiovisual qualifications | No media launch has occurred in V1/V2/V3/V4/hotfix attempts | Remains BLOCKED until V4 full preflight PASS; then execute 22×A/B once. |
| E4B-L22-HR-06 | Human review of 44 AV outputs | Requires 44/44 technical result | NOT_STARTED; operator visual/editorial/layout + audio review required after technical PASS. |

Previously accepted R1P 27/27, Loop22 projection 22/22, five policy fingerprints and R1V pilot remain accepted and are not repeated. C11-C and production governance locks remain intact. No Git checks; commits operator-managed.
