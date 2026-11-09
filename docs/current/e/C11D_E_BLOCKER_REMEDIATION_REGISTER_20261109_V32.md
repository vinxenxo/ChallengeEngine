# C11-D/E Blocker Remediation Register — V32 (2026-11-09)

| ID | Issue | Evidence / root cause | Remediation | State |
|---|---|---|---|---|
| E4B-L22-PS-01 | V1 wrapper treated Python unittest stderr as terminating PowerShell error | V1 used native `& ... 2>&1` under `$ErrorActionPreference=Stop` | V2 .NET process bridge separates both pipes and preserves exit codes 0/23; operator verified bridge, AST and 24/24 tests | RESOLVED |
| E4B-L22-AV-02 | Shared output directory collision | 44 logical jobs reuse role/family/repeat directories; original V1 repeatedly called `mkdir(exist_ok=False)` | Runner V2 deduplicates to 40 unique directories and creates each once; 25/25 isolated tests PASS | RESOLVED_TEST_ONLY |
| E4B-L22-PS-03 | V3 wrapper falsely rejected the shared-dir installation receipt | V3's duplicated frozen C11-C hash literal on line 146 was 63 characters (missing one `5`) while the canonical frozen hash is 64 characters; operator receipt and installer are correct | V4 declares the canonical hash once, pins the exact V1 shared-dir receipt SHA `1fc8ecfee3ea34ba9c0853aea627808153372c7ad678e385f2e3f603d9835fd7`, and validates fields separately with named diagnostics | CORRECTED_OVERLAY_READY; WINDOWS_INSTALL_PENDING |
| E4B-L22-AV-04 | Physical 44-slot audiovisual qualification | No V3 prelaunch passed; no V3 test or media process started | Install receipt-pin V2 overlay, run only V4; runner launches only after bridge/AST/25 tests/prelaunch PASS | BLOCKED_PENDING_V4 |
| E4B-L22-HR-05 | Human review of 44 audiovisual outputs | No new 44-slot deliverables yet | Operator visual/editorial/layout and listening review after technical 44/44 | NOT_STARTED |

Previously accepted E4A, R1P 27/27, Loop22 projection 22/22, five policy approvals and R1V pilot remain closed. No C11-C mutation or governance unlock.
