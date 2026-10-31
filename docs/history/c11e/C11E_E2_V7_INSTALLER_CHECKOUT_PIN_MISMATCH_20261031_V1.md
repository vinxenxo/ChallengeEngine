# C11-E E2 V7 V1 installer — stale checkout pin refusal

**Date:** 2026-10-31. **Disposition:** CORRECTLY REFUSED BEFORE WRITES; package identity defect belongs to package preparation.

V7 V1 was built using the prior checkout identity `main / a3c7c5d284a96ce115ca52208b4039002502753b`, parent `bc8330e794fe37efe0c4f9c2bb0c0bd389f28f2c`. The operator commits locally at each iteration. Before V7 V1 was installed, E0 re-entry had been committed as `b92434d6a8b50cef7e49ba6b75a4813777927fe7`, parent `a3c7c5d284a96ce115ca52208b4039002502753b`.

Operator diagnostic confirmed branch `main`, actual HEAD `b92434d`, parent `a3c7c5d`, tree `91aa803c2d675ec9fc7afff120b2bc7d3de479ef`, and clean status `## main...origin/main [ahead 2]`. The commit is a direct child of the expected prior E1 foundation; it adds the E0 V11/V13 authority/roadmap/hygiene/README/prompt/history reconciliation. C11-C manifest remained 796318 bytes / SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`. Critical E2 source pins remained unchanged: runner V6 `33186f24...`, GDScript V6 `d53faa36...`, pair builder `37889062...`, pair tests `36b6f296...`, scene `6dfe47eb...`.

The installer emitted `Unexpected checkout identity` before any destination preflight, temporary write, receipt directory creation or payload application. No V7 receipt was created and no V7 payload changed. Later console commands continued after `throw`, reused the V6 receipt variables and printed a false PASS; those lines are not evidence of V7 installation.

## Correction

V7 V2 installer is pinned to the actual operator-reported `b92434d` / parent `a3c7c5d`. Its runtime runner no longer freezes current HEAD to one historical hash. It verifies that E1 commit `a3c7c5d` and E0 re-entry commit `b92434d` are ancestors of active `main`, validates exact source pins, and binds actual runtime HEAD/parent into its receipt. Each future installer package must refresh its exact HEAD/parent pins after the user's next local commit.
