# C11-E — local commit at each iteration policy (V1)

## Operator workflow fact

The operator commits the repository locally at each engineering iteration. This is normal workflow and must not be treated as unexpected drift, a dirty checkout or an accidental branch movement.

## Required assistant/package behavior

1. At the start of each new installation iteration, request or inspect the latest operator-reported `git branch --show-current`, `git rev-parse HEAD`, `git rev-parse HEAD^`, tree hash and `git status --short --branch`.
2. Every installer package pins the exact branch, HEAD and parent observed when that package is built. Never carry an earlier iteration's HEAD/parent constants forward by habit.
3. Before writing, verify the current commit identity, required receipt lineage, frozen C11-C manifest, source pins, all replacement preimages, add-only destination absence and package hashes. Abort before writes on any mismatch.
4. After installation, the operator may commit that iteration locally. A subsequent runtime runner must not assume its HEAD still equals the installer-time HEAD. It records the actual runtime HEAD and parent, requires the known E1/E0 commits to remain ancestors, and enforces exact hashes for all source files relevant to the gate.
5. Any later remediation package is rebuilt against the newly committed HEAD/parent. Do not reset, clean, rebase, amend, switch branches, move refs, or push as part of an overlay installer.
6. The existence of a new local commit is not itself evidence that a gate passed. Acceptance remains tied to source-bound receipts, test results, actual rendered media and independent review.

## 2026-10-31 reconciliation

The checkout at V7 V1 installation attempt was `main`, HEAD `b92434d6a8b50cef7e49ba6b75a4813777927fe7`, parent `a3c7c5d284a96ce115ca52208b4039002502753b`, tree `91aa803c2d675ec9fc7afff120b2bc7d3de479ef`, clean worktree (`## main...origin/main [ahead 2]`). HEAD `b92434d` is a direct child of `a3c7c5d`, with subject `C11-E — E0 re-entry and actual-checkout reconciliation`. Its commit files are the E0 V11/V13 governance/documentation reconciliation; the protected pins shown by the operator remain unchanged. Therefore V7 V1's refusal was caused by a stale package pin, not by a bad operator checkout.
