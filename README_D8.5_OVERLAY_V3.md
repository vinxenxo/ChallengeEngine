# C11-D D8.5 Release Manifest/Staging Overlay V3

Fixes the V2 mutation-guard false failure by defining the workspace guard as an explicit protected perimeter: every workspace file except the declared D8.5 write root. The protected `release` and `artifacts/releases` roots are also snapshotted independently. D8.5 remains a non-authority preview with no physical staging.

PowerShell 5.1 compatibility: no Generic.List, no Measure-Object -Sum, no ambiguous TrimStart, no bare boolean literals.
