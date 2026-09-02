# C6-E — STEP 0 / E1 REPORT

## Status

C6-E Step 0 and E1 implementation prepared on top of certified C6-D4.

## 1. Output contract resolved

| Layer | Contract |
|---|---|
| Simulation coordinate canvas | 1080 × 1920 logical coordinates |
| Godot source movie | 540 × 960 @ configured FPS |
| Master MP4 | 1080 × 1920 @ configured FPS |
| Master codec | H.264 |
| Master pixel format | YUV420-compatible |
| Master scaling | explicit FFmpeg Lanczos 2× |
| Physical authority | FFprobe on source + master |

Historical C6-D4 MP4s are 540×960 and remain historical evidence. They are not the new master-output contract.

## 2. Asset integrity gate

Mandatory assets are now checked in Layer 0 before simulation/render:

- `background_path`
- `target_path`
- `object_path`

Rules:

- required;
- non-empty;
- `res://` only;
- `ResourceLoader.exists()` must be true.

`CHALLENGE_009` was genuinely missing `res://assets/c6/count_background.svg`. A dedicated asset has been added, so the nine-challenge corpus no longer contains a knowingly unresolved asset reference.

## 3. E1 Presentation Profile

Added `core/presentation/PresentationProfile.gd`.

The profile owns presentation configuration only; its canvas/output dimensions are read-only contract values:

- profile id;
- source canvas size;
- master output size;
- safe area;
- typography scale/config;
- composition hints;
- theme;
- asset family identity.

It has no timeline, RNG, seed, simulation or winning-frame state.

Challenges now select the profile declaratively using:

```json
"presentation": {
  "profile": "social_default_v1"
}
```

Optional `profile_overrides` are supported for controlled presentation variation.

## 4. Required isolation proof

Added `C6EPresentationProfileIsolationTest.gd`.

The test constructs one `SimulationResult`, resolves two presentation profiles against it, and verifies:

- presentation models differ;
- `SimulationResult` is unchanged;
- `winning_frame` remains unchanged.

This is an architectural isolation test, not a pixel-diff test. Pixel-level visual regression belongs to the next presentation-validation step.

## 5. Factory hardening

`build_factory.py` now:

1. probes the Godot source movie;
2. rejects a source movie that is not 540×960;
3. explicitly scales the master to 1080×1920;
4. probes the master;
5. rejects wrong resolution, codec or pixel format;
6. records source/master output contract in the manifest.

## 6. Validation executed in this environment

PASS:

```text
python -m py_compile build_factory.py tests/*.py
python tests/c6e_output_contract_test.py
python tests/phase_duration_contract_test.py
```

The physical source/master contract test generated a synthetic 540×960 source and verified an actual 1080×1920 H.264 master with FFprobe.

## 7. Environment limitation

Godot 4.7.1 is not installed in this execution environment, therefore the new GDScript suites have not been executed here. They are registered in `tests/run_all.py` and must be run in the existing Windows/Godot 4.7.1 certification environment before E1 is declared fully certified.

## 8. Explicit non-changes

No changes were made to:

- RNG architecture;
- RNG streams or seeds;
- deterministic mechanic mathematics;
- `SimulationResult` contract;
- `WinningFrameDetector`;
- C3/C4/C5 deterministic contracts;
- `VideoTimeline` semantics.
