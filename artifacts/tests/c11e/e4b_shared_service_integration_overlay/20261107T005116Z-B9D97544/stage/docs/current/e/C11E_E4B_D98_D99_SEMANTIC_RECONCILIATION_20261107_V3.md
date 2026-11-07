# C11-E D9.8 / D9.9 Semantic Reconciliation — V3

**Date:** 2026-11-07

The V80 source patch separates two propositions that must not share one compatibility flag:

| Proposition | Loop/Drill status | Meaning |
|---|---|---|
| D9.9 universal request → canonical editorial intent/plan | `PLAN_ONLY_COMPATIBLE` | The request can be normalized and planned; it is not a renderer input. |
| D4 executable renderer-native request/input | `NOT_EXECUTABLE_COMPATIBLE` | No dispatch or renderer-native input is admitted. |

The E4B service integration invokes the existing E1 shared service boundary for Loop preparation, then retains D9.10 bridge/envelope semantics as preparation only. A green D9.8 model test verifies metadata semantics, not actual pixel consumption.

V1 installation did not apply the source changes: it aborted while creating backup 3 because its absolute destination measured 262 characters. V2 preserves the source postimages but moves backup destinations to short `b/NN.bak` paths and preflights all six before copying.

After Windows V2 acceptance, keep D9.9 `PLAN_ONLY`, D9.10 `PREPARE_ONLY`, D4.8 `BLOCKED` until its separate baseline authority process. Never upgrade D4 on the strength of this model or E4B contract tests.
