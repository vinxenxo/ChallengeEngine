# C11-E D4.8 R1V Qualification-Only Authorization Requirements — V2

**Date:** 2026-11-07  
**State:** `PROPOSED_NOT_APPROVED`  
**Execution authorization:** `FALSE`  
**Renderer policy v1:** `DISABLED` (unchanged).

## 1. Authorization is separate from architecture approval

Option C architecture is now explicitly approved by the operator. That decision does not authorize physical R1V source rendering. Historical D4.8/D4.9 PASS/CLOSED results (8/8 governance, 102/102 GUI/CLI parity) prove the disabled-policy denial path; they do not authorize a launcher.

The only requested permission in this document is a temporary, bounded `R1V_QUALIFICATION_ONLY` scope for five silent C11-C source-generation selectors and one deterministic repeat each. It is not production, review-render, compositor, audio, mux, freeze, promotion or release authority.

## 2. Proposed five-family allowlist

| Family | Grammar | R1P receipt | Gameplay seed | Duration descriptor | Frames descriptor | Launcher SHA-256 | Prototype SHA-256 |
|---|---|---:|---:|---:|---:|---|---|
| Fractal Bloom | `radial_bloom` | 06 | 100006 | 22 s | 660 | `02e3721c92046f1f69119e5bbc6c69709dd0b97fad7191c08213ecc233930801` | `b596ecba5eeae80ba615d7cb8a741dffcab9db4c44296e660f4f9d6919cc5c55` |
| Geometric Waves | `harmonic_membrane` | 01 | 100001 | 23 s | 690 | `661bd61df61bc633e4b87cd4b9413c4317c8d4b6068194245aea7d40fcb5c7cd` | `ab2560cbe7fa42c5cad3b143aa59d1f2a0dc047682f7667983c7c0a0f6dbb61c` |
| Invisible Forces | `dipole_field` | 21 | 100021 | 22 s | 660 | `88924dd86ebdc9b51a51f354ec22f40beb75cf6daafbe869283fa187568b6f60` | `a68661a5fdf792aa7fe701afa6fbf1631a2b8215c214032f58ecfe0c69d8374a` |
| Living Particles | `swarm` | 16 | 100016 | 20 s | 600 | `3674fdf778927022d2ebc1d1a96865b441479c5e4e71802e90837d654278a638` | `835ba0df2c160a259be39bd1977bfac0e6a66f903ce1aa6b4247af7c508ad94a` |
| Sacred Symmetry | `astrolabe` | 11 | 100011 | 23 s | 690 | `8eea21f7b72f679d8951410597f0ecf968ac0a6f1ee629a48de965ea62b60b6e` | `12fdbc13e05df28b26cf95fe1907d150bd41f29196287700153521e9baee336b` |

Each is run twice, for ten total source-launcher invocations. The values 600/660/690 are R1P descriptors only; R1V must measure actual frame counts.

## 3. Mandatory execution constraints

- Run only the five pinned C11-C family launchers in the table, by their existing CLI contract.
- Use the exact R1P gameplay seed and grammar identity. Include `-NoSound`.
- Never pass or consume `request.music_seed` in the visual launcher.
- Use ten unique, initially nonexistent output roots. Never clean or overwrite an existing root.
- Revalidate the complete R1P parent chain and active-checkout pins immediately before the run.
- Capture executable pins, versions, exact arguments, environment facts required by the source runner, exit code, stdout/stderr files and hashes.
- Inspect source output with read-only FFprobe and FFmpeg decode-only streaming to an in-memory pixel hasher.
- Preserve source video bytes. No pixel/temporal transform is allowed in R1V.
- Any missing pin, path collision, output-root nonempty condition, frame/pixel mismatch or governance drift is a hard failure; no partial family start.

## 4. Forbidden operations

D compositor dispatch; D9.10 renderer consumer dispatch; D3 music engine; PCM generation; FFmpeg encode/filter/mux; FFprobe write; longform; Smoke18/Matrix99; production delivery; freeze/promotion/release; modifications to C11-C mechanics, RNG, protected sources or frozen manifest.

## 5. Approval record required before execution

The authorization package must contain all of the following before the first family launcher:

1. Policy author explicitly assigned.
2. Independent reviewer explicitly assigned and approval recorded.
3. Operator approval of this exact five-selector / ten-invocation scope.
4. Approval timestamp and SHA-256 of the immutable approval record.
5. Live active-checkout source pins and toolchain executable pins.
6. Verified unique empty output roots and fail-closed runner preflight.
7. A clear statement that this does not enable D composition, D3/audio/mux, production, promotion or release.

Until all seven exist, the policy remains `PROPOSED_NOT_APPROVED` and `execution_authorized=false`. Do not alter `C11D_PRODUCTION_ACTIVATION_POLICY_V1.json` to imply authorization; keep renderer policy v1 disabled.
