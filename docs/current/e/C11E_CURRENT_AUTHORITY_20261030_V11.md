# C11-E — autoridad vigente (V11)

**Fecha de corte:** 2026-10-30. **Checkout esperado para E0:** `main` / `a3c7c5d284a96ce115ca52208b4039002502753b`, padre directo `bc8330e794fe37efe0c4f9c2bb0c0bd389f28f2c`.

## Reinicio E0 sin pérdida de trabajo

E0 se reinicia como reconciliación del checkout real y corrección del método de ejecución. No se reinicia Git ni se borra E1/E2. El paquete E0 debe comprobar recibos, postimages vivos y manifiesto C antes de escribir; debe archivar byte por byte las instrucciones V9 actuales antes de sustituirlas; debe registrar estado Git y errores sin invocar renderer.

## Estado probado al corte

- C11-C manifest: 796318 bytes, SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.
- E1 shared service: instalación 8/8 y dos pruebas Windows (`producer_gui_contract`, `producer_self_test`) 2/2 exit code 0; GUI operador aún no observado en runtime.
- E2 V4 source/documentation overlay: 21/21 postimages y path guard 4/4. Physical attempt failed before Python; no Python tests, sidecars, Godot, AVI/MP4 or pixel compare occurred.
- Root cause: `Get-Command python -CommandType Application` returned Python313 and WindowsApps alias; conversion of `.Source` from a collection made one invalid concatenated FileName. Standalone probes later proved Python 3.13.14 at `C:\Users\vinxe\AppData\Local\Programs\Python\Python313\python.exe`, Godot 4.7.1 Mono, FFmpeg 9 and FFprobe can start.
- V4 created an empty stage and falsely announced a failure ZIP that did not exist. This is a runner evidence-reporting defect, not evidence of a rendered failure.
- The line `C11-E E2 V4 COMPLETED` printed manually after exit code 1 is not a gate result.

## Product objective

Deliver actual presentation+editorial+music MP4s for all three families. Use family-specific C binders and physical runners, the universal allowed editorial fields, D3 Music V5, FFmpeg mux and FFprobe validation. A Challenge-only A/B is an isolating step, not the product deliverable.

## Family editorial semantics

Common enabled fields: `title`, `subtitle`, `call_to_action`, `language`. Challenge-only: `player_name`, `challenge_label`. Reserved `hook`, preparation/final text, header/footer lines and show flags remain disabled. Never map title into hook or CTA. D9.9 is reused under its existing Challenge request contract; Loop/Drill need an E-owned universal family adapter rather than fictional D9.9 acceptance.

## Gate sequence

E0 actual checkout/receipts/toolchain reconciliation. E1 shared service. E2 Challenge title-to-pixels A/B, no audio. E3 Challenge D3 music/mux. E4A Challenge A/V editorial; E4B Loop A/V editorial; E4C Drill A/V editorial. E5 determinism/regression. E6 Smoke18. E7 Matrix101. E8 independent formal acceptance/promotion.

`request.seed` governs gameplay; `request.music_seed` governs music only. C11-C freeze manifest, protected mechanics, D governance records and release locks remain unchanged. CHALLENGE_008/009 are held pending 11 s vs 12 s timing adjudication. No test or family render grants release authority.
