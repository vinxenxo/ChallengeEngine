C11-C 2.17.5 — HISTORICAL CHALLENGE 720 CAPTURE REPAIR

BASELINE: C11-C 2.16.9 FROZEN + C11-C 2.17.x additive challenge production overlay.

ROOT CAUSE FIXED
The 2.17.4 producer invoked Godot through the PowerShell native call operator. In this Windows/PowerShell 5.1 path, the arguments after `--` were not reaching OS.get_cmdline_user_args(), causing GeneradorMaestro to emit CHALLENGE_INVALID and Movie Maker to record exactly 1 frame.

2.17.5 fixes this by launching godot.exe through System.Diagnostics.ProcessStartInfo with explicit Windows quoting.

PHYSICAL CAPTURE
The producer now reuses tools/prototypes/c11c_common/C11CMovieCapture.ps1 and its certified temporary override.cfg mechanism to obtain 720x1280, while keeping the frozen logical 540x960 composition unchanged. override.cfg is restored/removed in finally after each sequential run.

FAIL-CLOSED
The producer verifies:
- Movie Maker mode enabled
- 720x1280 capture startup
- Movie Maker completion
- no CHALLENGE_INVALID in the log
- captured AVI width/height = 720x1280
- captured AVI frame count = expected exact frame count

Do not run the 54-run bulk until the single CHALLENGE_001 / seed 12345 smoke passes.

APPLY
Expand-Archive -LiteralPath <this ZIP> -DestinationPath . -Force
