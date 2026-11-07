# C11-E E4B R1V Actual Frame Inventory & Pixel Identity — V3

**State:** bounded five-family qualification explicitly approved; add-only Windows installation and physical capture pending.  
**Lineage:** E4B R1P CLOSED 27/27 → Option C active-checkout static PASS 27/27 → R1V V2 approval.

## 1. Scope

R1V measures real frames from silent C11-C source MP4s. R1P receipts describe deterministic parameter recipes and timing, not instantiated prototypes, frames or pixels. R1V therefore treats R1P timing as a consistency descriptor only and measures the actual media independently.

Initial admission is deliberately limited to five selectors × two executions:

| Family | Grammar | R1P receipt | Gameplay seed | Duration | Expected count (consistency only) |
|---|---|---:|---:|---:|---:|
| Fractal Bloom | `radial_bloom` | 06 | 100006 | 22 s | 660 |
| Geometric Waves | `harmonic_membrane` | 01 | 100001 | 23 s | 690 |
| Invisible Forces | `dipole_field` | 21 | 100021 | 22 s | 660 |
| Living Particles | `swarm` | 16 | 100016 | 20 s | 600 |
| Sacred Symmetry | `astrolabe` | 11 | 100011 | 23 s | 690 |

The exact selector tuple and all pins are machine-readable in `C11E_D4_8_R1V_QUALIFICATION_ONLY_POLICY_V2.json`.

## 2. Source generation boundary

Only the five C11-C family `run_prototype.ps1` launchers may be invoked. The invocation passes the R1P gameplay seed, grammar, duration, `-NoSound`, a new unique output root and a run-id-bearing output tag. It does not pass `music_seed`. No `-ExportGif`, `-KeepAvi` or `-NoFooter` switches are allowed.

The launcher uses Godot 4.7.1 to generate its native temporary AVI, then its existing `-NoSound` branch encodes a silent H.264 MP4 using the exact FFmpeg vector in the approval policy. This narrowly allowed native encode is distinct from D composition. FFprobe performs read-only inspection; FFmpeg decode writes raw YUV420P bytes directly to the in-memory hashing pipe. No decoded frame image is spooled to disk.

## 3. Captured measurements

For every one of the ten outputs:

- source MP4 SHA-256 and byte length, recalculated after inspection;
- FFprobe format and video-stream metadata: codec/profile, dimensions, pixel format, frame rate, time base, color fields, duration, frame count;
- frame-level PTS, best-effort timestamps, packet duration, keyframe and picture type;
- exact rational time base and 1/30-second interval validation;
- per-frame SHA-256 over contiguous decoded YUV420P planes;
- ordered global decoded-byte-stream SHA-256 and ordered frame-hash digest;
- launcher sidecars and logs with SHA-256;
- executable path/version/SHA-256 for PowerShell, Python, Godot, FFmpeg and FFprobe.

Each A/B pair must match exactly in actual frame count, PTS sequence, time base, geometry, pixel-format and per-frame pixel-hash sequence. MP4 byte identity is reported separately; metadata-container byte variance alone does not replace pixel identity comparison.

## 4. Failure handling

Stop on the first failed launcher or invariant. Keep completed outputs, process logs and partial inventories as evidence; never rerun into the same output roots. If a rerun is required, it receives a new run ID, tags and ten new non-existent paths. Any protected-source pin drift, unexpected `override.cfg` contents, temp AVI residue or stale temp-silent artifact fails the run. The guard restores only the exact known C11C temporary override bytes; it never overwrites unknown external edits.

## 5. Subsequent stages

After the five-family evidence passes and the operator completes visual review, separately admit the remaining 22 loop grammars in a new qualification batch. Do not silently expand the V2 five-selector allowlist. The D-only post-composition consumer is a separate implementation and acceptance stage, consuming immutable C source media plus R1V inventories and canonical Option C/D9.9/D9.10/R1P lineage. D3 music and final mux remain separately gated after visual consumer acceptance.
