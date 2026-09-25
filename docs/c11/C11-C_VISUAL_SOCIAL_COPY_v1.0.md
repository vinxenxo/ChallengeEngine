# C11-C Visual Social Copy v1.0

## Public format

Social `.txt` is publication copy, not QA telemetry. Current loop example shape:

```text
🌀 ¿Puedes notar dónde termina el bucle? 👇

**FRACTAL BLOOM** — Visual loop de arte generativa matemática y procedural.

- **Variante:** FRACTAL FILIGREE
- **Paleta:** midnight_electric_violet
- **Seed:** 1209245824
- **Detalles:** Duración 18.00s, 3 ciclo(s) completo(s), audio ambiental determinista.

Diseñado en código con #GodotEngine para reproducción continua en bucle.

#GenerativeArt #GodotEngine #LoopArt #OddlySatisfying #FractalBloom #FractalArt #MathematicalArt #ProceduralArt
```

The selected Visual Drill hook is reused verbatim as the first line of both Header and social copy.

Fixed hashtags always precede family/subfamily tags:
`#GenerativeArt #GodotEngine #LoopArt #OddlySatisfying`.

Internal fields such as music profile, hook index, CTA placement and typography stay in render manifests, not in public copy.


For Visual Loops, the `grammar` field is treated as the visual subfamily and may contribute secondary grammar hashtags. Fixed hashtags remain first, followed by family and subfamily hashtags.


## Hook reuse
For Visual Loops, the social first line reuses the rendered Header line 2 hook from the manifest. For Visual Drills, it reuses the deterministically selected hook from `c11c_visual_hooks.json`.
