# C11-E Current Authority — V45

**Date:** 2026-11-04  
**Context snapshot:** `C11E_WORKING_CONTEXT_20261104_095552.zip` (context only; the live Windows checkout remains authoritative).  
**Checkout:** `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`  
**Production baseline:** C11-C 2.19.12 remains the sole production authority.

## 1. Product objective

Deliver one D+E production factory for Challenge, Visual Loop and Visual Drill. Share request orchestration and E1 intent sealing; preserve each family's binder, timeline, presentation semantics and audio route. Challenge uses D3 Music V5. Loop and Drill keep their established C11-C family music. C11-C generators/mechanics and delivery standards remain unchanged until E8 independent acceptance, immutable freeze and explicit promotion.

## 2. Accepted upstream evidence

E4A.2 BODY reference, E4A.3 V2 real-frame compositor proof and operator disposition, and E4A.4 test-only A/V mux pilot remain accepted in their recorded scopes. E4A.4 produces three H.264/AAC MP4s and three WAVs with A/B repeatability, music-seed audio isolation, unchanged H.264 and zero measured A/V drift. Those MP4s do **not** contain the D compositor. Do not rerun these accepted gates without relevant source drift.

## 3. E4A.5B handoff incident and recovery

The read-only E4A.5 handoff collected 88 source files before its receipt writer failed on PowerShell boolean literals. Follow-on E4A.5B V1–V5 attempts were stopped after independent defects in whole-ZIP pinning, ZIP-entry cardinality, member path lookup and root assumptions. No production source patch was applied by those attempts. Do not rerun any V1–V5 handoff scripts and do not create another packager iteration.

The latest context snapshot independently contains the 88 inventoried handoff files with matching content hashes. It is used only as source-navigation context. The one-step Windows application below verifies exact live source pins before writing anything; any mismatch aborts before application.

## 4. E1 Challenge presentation option increment — E4A.1

The existing Producer D9.9 surface gains one Challenge-only checkbox: `Mostrar hook y countdown en Challenge`, default ON. It serializes `presentation_options.show_hook_countdown` into the E1 request and sealed intent. The E1 semantic intent hash includes this value.

D9.9 remains strict: the GUI writes a second sanitized request for the D9.9 planner with `presentation_options` removed. The full request is passed to the existing E1 CLI. GUI/CLI parity now explicitly compares the option. Visual Loop and Visual Drill omit this Challenge-only request field and retain their existing E1 shape.

Compatibility is preserved: E1 schema version `1.1` and service version `0.2.0-E3.2` remain unchanged. Older sealed Challenge intents without the optional field still validate using their original semantic hash and historical visible default. E3 D3 V5 / D3.3 / mux contracts are not rewritten.

**Scope boundary:** this increment transports and seals the visibility option; it does not yet consume it in the D visual compositor or dispatch a renderer. E1 remains preparation-only. Manual GUI observation remains separate from static GUI contract coverage.

## 5. Challenge source architecture and next consumer

`project.godot` → `Main.tscn` → `GeneradorMaestro.gd` owns the C Challenge runtime scene. The phase-aware `ChallengePresentationBinder` builds the existing HOOK/GAME/REVEAL/CTA render model; `SocialUIBinder` sends it to `PresentationUI` and the existing `UnifiedSocialFrame`. The physical C launcher is `tools/prototypes/c11c_bulk/run_c11c_challenge_production.ps1` and captures the unchanged scene through Godot Movie Maker, then FFmpeg/FFprobe.

Do not patch `GeneradorMaestro.gd`, `ChallengePresentationBinder.gd`, `SocialUIBinder.gd`, `PresentationUI.gd`, the C presentation components, C mechanics or the C launcher to add editorial. The next visual integration is D-owned and must reuse the existing Challenge model plus `C11CVisualEditorialLayer` at the proven D materialization/consumer boundary. No second binder or parallel renderer.

The Challenge policy remains: title/subtitle → HEADER/HOOK; `call_to_action` → FOOTER/CTA; language metadata-only; empty fields omitted; player_name/challenge_label blocked; phase windows resolved from each selected Challenge source timeline. Countdown/hook may coexist with editorial when enabled. A populated D CTA must not silently duplicate or alias the native Challenge phase CTA; establish a single visible footer owner in the D adapter and verify it in the isolated pixel review.

## 6. Verification state and next action

The isolated source-copy tests for E4A.1 cover default ON, explicit OFF, invalid types/shapes, Challenge-only scope, semantic hash identity, legacy intents, E1 CLI and GUI/CLI parity. The Windows apply runner performs exact live preimage pin checks, applies the five-file D/E1 patch atomically, runs the same focused tests, and only then adds these versioned documents.

Next: implement the D-only Challenge presentation adapter against the existing in-memory materializer and shared editorial layer; verify phase-window pixel output and countdown ON/OFF on the accepted real-frame test path. Keep D9.10 PREPARE_ONLY, renderer/production dispatch OFF, D4.8 blocked, and `release_authority=NONE`.

## 7. Governance

Frozen C11-C manifest: 796,318 bytes / SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`. Preserve `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector`, `RenderedFrameStream`, `FrameSnapshot.custom_data`, C11-C mechanics/generators/RNG, `core/audio`, D3 V5 and all governance locks. Matrix101 remains 54 Challenge + 27 Loop + 20 Drill, with CH_008/009 held (99 provisional runnable). E8 is required for any freeze or promotion.

`release_authority=NONE`.
