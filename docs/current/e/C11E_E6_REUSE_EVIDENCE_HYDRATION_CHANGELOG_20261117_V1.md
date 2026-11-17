# E6 reuse evidence hydration overlay changelog — V2

- Records the V1 audit result `E6HYDRATE_20261117T210711Z_C7D200D2` and its 55 exact blockers.
- Corrects V1's absolute-path handling by distinguishing active-checkout-contained files from external runtime executable references.
- Adds a narrow external runtime tool allowlist for `ffmpeg`, `ffprobe`, `godot`, `powershell` and `python`; checks basename, absolute path, and actual SHA-256. Does not allow arbitrary external artifact paths.
- Keeps the two CH004 historical source pin divergences as explicit hard blockers; no auto-waiver or expected-hash update.
- Adds a dedicated source drift adjudication register, current E6 next-action JSON, closeout document, and V3 handover/continuation prompts.
- Add-only installation; V1 files and all original evidence remain untouched.
- Does not invoke media tools, mutate project source, consume BatchId, activate renderer/dispatch or change D4.8.
