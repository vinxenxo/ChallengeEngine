# C11-E Current Authority — V93

**Date:** 2026-11-07. **Authority:** active Windows checkout `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`. V84 ZIP is context/evidence only; never unpack snapshots over checkout. Do not inspect or operate Git. `GIT_CHECKS=SKIPPED`; commits operator-managed; source SHA pins enforced.

## Immutable baseline

C11-C 2.19.12 immutable. Frozen manifest SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`. Preserve protected generators, mechanics, RNG, audio, binder, canonical definitions and all protected paths. Gameplay `request.seed` and `request.music_seed` remain independent.

## Accepted evidence

- E4A D99 GUI/CLI parity: PASS_TEST_ONLY.
- E4B mapping: PASS 5/5 families, 27/27 selectors.
- R1P: CLOSED PASS 27/27; family counts 5/5/7/5/5; 30/30 R1P source pins; recovered ZIP SHA `d49f54ffdee6026426c2bb87fcb72b5c8a68f09cb64fb91f71e25dc10fd26b52`.
- Option C: operator-approved architecture; checkout contract PASS 27/27 PREPARE_ONLY; 33/33 live pins; report SHA `ba76c626d92736c2f139380ec2b93d865015e8ef7e53f2881fdb16b6c4a54246`; process receipt SHA `db1cc4b8393f84d944391efdd6daa325e0ed9a5aac69ce7b0d7efc9ed9ea9355`.
- R1V bounded approval: operator approved five selectors × two executions (10 launches), native silent C11-C MP4 encode only, read-only FFprobe and FFmpeg decode-to-memory. No filters/audio/D3/D composition/mux/GIF/delivery/release.

## R1V installer incidents — no media

- R1V wrapper V2 failed before capture: PowerShell native STDERR interaction left Python exit code null.
- R1V installer V3 failed before copying (0/15): it selected `py.exe` semantics (`-3.13`) but the operator host resolved the command as `Python313\python.exe`; Python rejected `-3`. No launcher was invoked.
- R1V wrapper V1/V2 preflight attempt also failed with null test/capture exit codes. No launcher was invoked.
- These failed attempts did not create R1V media. Preserve their receipts; do not repeat the failed versions.

## V4 repair design — no duplicate preflight

The V4 installer is deliberately PowerShell-only. It verifies the package manifest and payload SHA/size, frozen C11-C manifest, R1V approval/policy hashes, C11-D production policy hash, recovered R1P archive hash, allowed paths, PowerShell AST, and add-only destination state. It does **not** invoke Python, call `py.exe`, run the 32-test suite, or launch a native process. Identical pre-existing payload bytes are verified/skipped; different bytes abort without overwrite.

The R1V wrapper V3 is the single owner of Python preflight. It resolves the direct `python.exe`, probes `sys.version_info[:2] == (3,13)` via `-c`, then executes the 32-test active-checkout suite exactly once using stdout/stderr file redirection and a numeric process exit code. Only a 32/32 PASS permits the ten authorised launches. This separation removes duplicate Python execution from the installer.

## R1V exact bounded scope

Five selectors (radial_bloom 100006 22s; harmonic_membrane 100001 23s; dipole_field 100021 22s; swarm 100016 20s; astrolabe 100011 23s), A/B each. R1P gameplay seeds only; never `music_seed`. Ten distinct non-existing output roots. No reuse/cleanup/overwrite. Guard `override.cfg`, deterministic temporary MP4 and AVI patterns. Only native silent C11-C H.264 encode branch, FFprobe read-only, FFmpeg decode to memory for pixel hashes. No filters, derived/transcoded media, audio, D consumer, D9.10 dispatch, D3, mux, GIF or release.

## Roadmap

After 10/10 technical capture and operator visual review: qualify remaining 22 selectors under separate scope; implement one generic Option C D consumer over immutable C inputs and measured R1V evidence; validate layout/editorial; then D3 music/mux. Target remains five families and 27 variants.

## Gates

R1V capture: AUTHORIZED, NOT RUN. D compositor: NOT IMPLEMENTED. General D4.8 production renderer: DISABLED. D9.10 PREPARE_ONLY. D9.14/D9.16 BLOCKED. D9.17 BLOCKED_NO_GO. D10 BLOCKED_FOR_PROMOTION. Release authority NONE. E4C/Drill, E5, Smoke18, Matrix99 and E8 downstream.
