# V4 acceptance and remaining gates

V4 build validation is local only. Operator Windows acceptance requires: installer PASS_ADD_ONLY; focused tests PASS with `C11E_L2_INSTALLER_SOURCE` pointing to the extracted V4 installer; then one V4 runner invocation. The runner must verify the V4 capture script's exact SHA/bytes before either Godot process.

Only a successful receipt plus both source/composited frame artifacts enables visual inspection. L2 remains TEST_ONLY until pixel-contract review and operator visual/resampler decision. L3 negative controls and L4 six Loop selectors remain separate gates.
