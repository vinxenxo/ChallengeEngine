# D4.8 R1V Qualification Authorization Requirements — V8

The operator explicitly approved the bounded R1V scope in the current conversation: five first-family selectors × two independent executions (10 launches). The operator is independent reviewer and operator approver; ChatGPT is technical author.

Allowed: original pinned C11-C `-NoSound` launchers; exact native silent MP4 encode branch; FFprobe read-only; FFmpeg decode-to-memory for frame/pixel hashes. Forbidden: filters, transforms, scaling, fps conversion, audio/music, D composition/consumer, D9.10 dispatch, D3, mux, GIF, derived media, production delivery or release.

The C11-D production policy remains unchanged: `renderer_activation_policy.state=DISABLED`, `runtime_authority=NONE`, review authorization false, production execution false. Bounded R1V source qualification does not activate general renderer production.

## V3 installer defect

V3 failed before copy (0/15) because the installer resolved a command as the `Python313\python.exe` interpreter but passed `-3.13`, an option intended for the Python launcher. Python rejected `-3`. No files were installed by that attempt and no launcher/media was created.

## V4 separation of responsibilities

The installer is **PowerShell-only**. It does not invoke Python, `py.exe`, `Start-Process`, or the R1V test suite. It verifies manifest, governance/policy hashes, recovered R1P archive hash, payload integrity, allowlisted paths, PowerShell AST and add-only destination state, then copies. Identical pre-existing bytes are verified/skipped; differing bytes abort. It does not rerun Python tests.

The wrapper V3 owns Python 3.13 discovery and the one active-checkout suite run. It resolves a direct `python.exe`, probes via `-c`, redirects stdout/stderr to files using `Start-Process -Wait -PassThru`, reads the real numeric exit code, and runs exactly 32 tests once before any capture. If that test result is not 32/32 PASS, zero launchers are invoked.

After install PASS, run only `RUN_C11E_E4B_R1V_FIVE_FAMILY_QUALIFICATION_V3.ps1`. Do not run V1/V2 wrappers, V3 installer, individual launchers, or tests separately. Preserve the install and wrapper receipts. Technical PASS remains pending operator visual review.
