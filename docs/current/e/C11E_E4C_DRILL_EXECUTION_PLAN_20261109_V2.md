# C11-E E4C Visual Drill Execution Plan — V2 (2026-11-09)

## Objective

Complete the Drill family integration through the existing D9 dynamic request binder V2 and E1 shared service. Preserve the four Drill types, five difficulty tiers, C11-C-native phases and END_CTA precedence, and existing `FAMILY_MUSIC_V4`. No parallel binder, producer or generator.

## Exact selector matrix

- `tracking`: `tier-1` … `tier-5`
- `pursuit`: `tier-1` … `tier-5`
- `saccade`: `tier-1` … `tier-5`
- `peripheral_scan`: `tier-1` … `tier-5`

The historical 20/20 authoring-adapter audit remains accepted (24/24 pins; report SHA `fc550cf26161c5428e2b8edf280baf611fb3c06f2e3c00773910e352115eaa6e`). Do not rerun it if pins remain valid.

## Integration in this increment

The E1 service branch calls the existing V2 binder's canonical contract/chain functions for the selected Drill request and emits a strict non-rendering preview into the E1 intent. The existing Producer GUI reads the returned E1 bridge/stage/binding preview and writes evidence artifacts; it does not reconstruct or rebind Drill. The CLI uses the same service. The V2 real-Godot request manifest is still produced only by the dedicated V2 runner, not by E1 preview.

## Native Drill phase/CTA contract

- PRE_ROLL: `CountdownPresentationLogic.COUNTDOWN_SECONDS` (3.0 seconds).
- GAME: actual C11-C generated gameplay frame count / frame rate.
- END_CTA: `VisualDrillPresentationPhaseLogic.END_CTA_SECONDS` (3.0 seconds).
- DONE: after the full native presentation frame count.
- During END_CTA, the native C11-C Drill CTA owns the header; editorial header line 1 and 2 are suppressed. D cannot override native CTA. Footer telemetry remains under native UI semantics.

Never infer Drill phase windows from field names or copy Challenge HOOK/CTA or Loop grammar intervals.

## Native music and seed separation

Preserve `FAMILY_MUSIC_V4` type/profile mappings: tracking=`FLOWING_VECTOR`, pursuit=`ORGANIC_BLOOM`, saccade=`CIRCUIT_PULSE`, peripheral_scan=`ORBITAL_RITUAL`. Native PCM source is 44.1 kHz stereo, from the inspected generator constants; verify actual output duration and format on Windows before delivery conversion.

C11-C `run_visual_drill_production.ps1` uses its gameplay `$Seed` for its built-in audio call. Do not modify this protected launcher. For future E4C A/V, invoke it with `-NoSound`, then call the existing C11-C family-music helper with `request.music_seed` and the bound family profile, then mux/QC using the accepted E path. No D3 V5 for Drill.

## Gate 1 — install and local-contract verification

Install only if the exact seven preimage hashes in the installer match the active checkout. The installer has a full preflight and transaction rollback; if a preimage differs, it must stop before any write. No retry with relaxed pins.

## Gate 2 — Windows runtime acceptance

Run:
`powershell.exe -NoProfile -ExecutionPolicy Bypass -File ".\tools\c11d\d9\RUN_C11E_E4C_DRILL_BINDER_V2_ACCEPTANCE_V1.ps1" -ProjectRoot "C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS"`

Requirements: Python 3.13, Godot 4.7.1 Mono exact build. The runner executes 32 E1 service tests, 7 V2 source-chain tests, current V1/request-scope/review-manifest regressions, then the actual V2 20-pair matrix with two independent real-Godot executions per pair. It records stdout/stderr, 20 VERIFIED receipt rows and a hash-bound report. The matrix is in-memory/preparation-only; it does not enable renderer, media or dispatch.

## Gate 3 — visual policy is separate

The A.3 Loop/Drill field-window proposal still pins an older editorial review manifest. Refreshing current D9.8 transitive contract hashes exposes this mismatch. Do not edit the already approved A.3 proposal/decision in place. Issue a new versioned dependency reconciliation and obtain a new explicit decision before a visual consumer may use the proposal. Until then E1 may prepare request/source identity, but field windows and pixels are blocked.

## Gate 4 — GUI and A/V

The local suite proves E1 CLI request handling and a static GUI-source contract; it is not a Qt GUI runtime acceptance. A separate operator GUI observation remains due. The actual V2 runtime manifests, policy approval, visual consumer, native audio helper and final A/V qualification remain separate gates. E4C closes only after all are accepted and the operator reviews every bounded A/V output.

## Governance

C11-C 2.19.12 immutable; frozen manifest SHA `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`. Renderer OFF, D4.8 BLOCKED, D9.10 PREPARE_ONLY, D9.14/D9.16 BLOCKED, D9.17 BLOCKED_NO_GO, D10 BLOCKED_FOR_PROMOTION, release NONE.
