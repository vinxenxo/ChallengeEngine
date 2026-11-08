# D4.8 R1V Qualification Authorization Requirements — V10

## Existing bounded source-capture approval

The operator approved five representative Visual Loop selectors × two repeats (10 slots). The original V2 silent-only policy and approval remain unchanged and continue to govern the native source capture itself: pinned C11-C launcher with `-NoSound`, native C11-C silent MP4 encode, read-only FFprobe and FFmpeg pixel decode to memory.

## Supplemental family-native audio A/V approval

On 2026-11-08 the operator explicitly approved adding the native family music to the same R1V qualification production. The supplement is represented by:
- `C11E_D4_8_R1V_FAMILY_AUDIO_SCOPE_AMENDMENT_V1.json`
- `C11E_D4_8_R1V_FAMILY_AUDIO_APPROVAL_AMENDMENT_20261108_V1.json`

Exact scope: five representative selectors × A/B = 10 final A/V outputs. Reuse the previously created Fractal Bloom A source (validating its original report/receipt/logs/MP4); nine new C11-C source launcher invocations. Generate each Loop WAV with the original `C11CSafeAmbient.py` / `C11C_FAMILY_MUSIC_V4` helper using the R1P `music_seed`, cycle count, duration, internal family and grammar. Then mux AAC 192k, 44.1 kHz stereo with H.264 `-c:v copy` into a separate A/V MP4. Verify FFprobe, H.264 elementary-stream identity, WAV metrics, AAC digest and A/B determinism.

D3 V5 is not the Visual Loop music route; it remains Challenge-specific. No D compositor, filters, video re-encode, GIF, D9.10 dispatch, general D4.8 activation, production delivery or release is authorized by this supplement.

## Independent review and governance

The operator is both operator approver and independent reviewer. ChatGPT is the technical author. The supplement is strictly bounded test authority; it does not change `C11D_PRODUCTION_ACTIVATION_POLICY_V1.json`, whose renderer remains DISABLED and runtime authority NONE. D9.10 remains PREPARE_ONLY; D9.14/D9.16 remain BLOCKED; D9.17 NO-GO; D10 BLOCKED_FOR_PROMOTION; release authority NONE.

## Execution controls

One PowerShell-only installer checks hashes/governance/parents/source pins/AST/destinations and copies add-only. It does not invoke Python. One wrapper resolves direct Python 3.13 and runs the combined 52 tests once. Only 52 executed tests with zero skips, errors and failures allow the integrated A/V runner on Windows. The runner reuses Fractal A, makes nine new source captures and performs music+AAC mux per slot. No standalone audio phase or separate test iteration.


## Integrated A/V wrapper execution condition

The active Windows wrapper must report exactly 52 tests, zero failures, zero errors and zero skips. The single Windows-only prior-Fractal-A integration test must run against the pinned report/receipt/MP4/log paths; an environment skip is not accepted for active qualification. The PowerShell-only installer does not call Python; the wrapper resolves direct Python 3.13 once and is the only test/capture entry point.
