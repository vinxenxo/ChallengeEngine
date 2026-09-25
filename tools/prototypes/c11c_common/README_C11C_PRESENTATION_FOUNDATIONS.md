# C11-C Presentation Foundations

## Typography

Use `core/presentation/C11CVisualTypography.gd`.
Header: Inter Bold. Footer: Noto Sans Mono Regular. Do not load font files directly from new C11-C presentation code.

## Music

Use `C11CSafeAmbient.py` as the launcher-facing entry point. It resolves family -> semantic profile through the C11-C music table and delegates to `generate_c11c_family_music.py`.

CLI:

```text
C11CSafeAmbient.py OUTPUT.wav SEED LOOP_CYCLES DURATION_SECONDS FAMILY [KIND] [GRAMMAR]
```

`KIND` is `loop` or `drill`. In drill mode the generator settles gently over the final three seconds. No gameplay events are passed into the generator.
