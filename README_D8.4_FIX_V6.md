# C11-D D8.4 Artifact Eligibility Fix V6

Fixes PowerShell 5.1 `ArgumentException: Argument types do not match` caused by array-subexpression evaluation of `System.Collections.Generic.List[object]` created with `New-Object`.

V6 replaces the generic `List[object]` / `List[string]` accumulators with native PowerShell arrays and preserves the D8.4 eligibility/provenance rules unchanged.

No C11-C, D7 authority, media, or release product is modified by the runner.
