# C11-C Visual Hook + Social Copy Contract v1.0

## Scope

Visual Drill hooks are presentation/editorial content. They are not gameplay truth and never alter authoring, runtime mechanics, answer sheets or `RenderedFrameStream` semantics.

## Hook bank

Each of the four Visual Drill families has exactly 10 authored hooks:

- `tracking`
- `saccade`
- `pursuit`
- `peripheral_scan`

The source of truth is `profiles/presentation/c11c_visual_hooks.json` and the runtime resolver is `core/presentation/C11CVisualHookBank.gd`.

## Deterministic selection

The selected hook is calculated as:

```text
index = (seed + family_offset) mod hook_count
```

The selected hook is used by the Header and is reused verbatim by the Visual Drill social sidecar. This prevents the video and its publication copy from describing different hooks.

The hook is exposed in the presentation render model as:

- `hook_text`
- `hook_index`
- `hook_bank_version`

## Social format

The social `.txt` sidecar now begins with the selected hook and uses a publication-friendly Markdown-style body:

```text
[HOOK]

**FAMILY NAME** — ...

- **Variante:** ...
- **Paleta:** ...
- **Seed:** ...
- **Detalles:** ...

Diseñado en código con #GodotEngine ...

#GenerativeArt #GodotEngine #LoopArt #OddlySatisfying ...
```

The four fixed hashtags are always present on current C11-C social output:

`#GenerativeArt #GodotEngine #LoopArt #OddlySatisfying`

Family-specific hashtags are appended after them.

## Copy integrity

The sidecar must not invent gameplay results, statistics or answer-sheet facts. Hooks are editorial copy supplied by the hook bank and are treated as copy, not as evidence.

## Visual Loop hook reuse

For Visual Loops, the publication hook is the rendered artifact's existing Header line 2 (`editorial.header_line_2`) when present. The social writer falls back to the generic `🌀 ¿Puedes notar dónde termina el bucle? 👇` only for legacy manifests that do not contain a Header hook.
