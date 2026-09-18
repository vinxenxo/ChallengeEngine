# C11-B.0 Package

This is a presentation-only delta against the C10 freeze.

Included:

- `UnifiedSocialFrame.tscn/.gd` — canonical Header/Body/Footer topology.
- `CoordinateMapper.gd` — optional target-rect projection with aspect preservation.
- `PresentationProfile.gd` — canonical social-region geometry without changing existing C6 composition semantics.
- `WinningFrameVisibilityGate.gd` — deterministic presentation geometry gate.
- `GeneradorMaestro.gd` — challenge object/target mapping constrained to BodyRegion plus audit mode.
- `C11B0UnifiedSocialFrameContractTest.gd` — contract test.
- `run_c11b_body_visibility_audit.ps1` — 54-run visibility audit using C11-A.1 artifacts.
- `docs/C11B0_CONTRACT.md` — contract and scope boundary.

## Apply

Copy the included files over the corresponding project paths, or use the supplied patch if working from a clean C10 freeze.

Then run:

```powershell
godot --headless --path . -s .\tests\C11B0UnifiedSocialFrameContractTest.gd
```

After C11-A.1 remains available:

```powershell
.\tools\run_c11b_body_visibility_audit.ps1
```

Do not regenerate C11-A or C11-A.1 artifacts.

### v3 correction
The `target_position` secondary binding is mapped through the same `BodyRegion` target rect as the primary entity. This keeps both winning-frame entities under the Unified Social Frame geometry.


### Windows PowerShell compatibility
The audit runner uses `ProcessStartInfo.Arguments` instead of `.ArgumentList` so it works under Windows PowerShell 5.1.
