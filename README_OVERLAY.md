# C11-E foundation overlay — apply instructions

Keep this ZIP next to `APPLY_C11E_FOUNDATION_OVERLAY_20261030_V3.ps1`.

The apply script validates the archive SHA-256 (pinned in the script), each file against `C11E_OVERLAY_MANIFEST.json`, the reconciled clean parent checkout (`main` / `bc8330e794fe37efe0c4f9c2bb0c0bd389f28f2c`, parent `8f6905003a4dff979ed97dc2e721d1abc4375de8`), the C manifest and the preimages of `AGENTS.md` and `.continue/rules/CONTINUE.md`. It installs the foundation directly on the user's active local `main` branch. It does not create/switch branches, alter local or remote refs, or push. Existing `c11e-unified-editorial-production` refs are recorded but left untouched.

No renderer, media creation, C source modification, reset/clean, commit or push is performed. See `overlay/docs/current/e/C11E_E0_BOOTSTRAP_RUNBOOK_20261030_V3.md` after installation.
