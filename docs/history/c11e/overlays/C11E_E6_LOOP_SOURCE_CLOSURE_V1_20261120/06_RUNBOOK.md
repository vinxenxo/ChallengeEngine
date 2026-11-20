# Loop source closure V1 runbook

1. Install ADD_ONLY from a fresh temporary extraction path. Documentation is installed under `docs/history/c11e/overlays/`, `docs/current/e/` and `prompts/` in the checkout.
2. Run the focused 27-test contract suite once.
3. Run `RUN_C11E_E6_LOOP_SOURCE_CLOSURE_V1.ps1` once. The runner validates its own PS 5.1 AST and the pinned Python auditor before invocation.
4. Preserve receipt and sidecar. Inspect `source_media_rehash_complete`, each row's `source_mp4_rehashed`, `colorimetry_gate`, and `visual_resampler_gate`.
5. Do not proceed to L2 on this audit alone.
