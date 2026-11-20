# Loop source and selector closure protocol — read-only

## Objective

Before any D-owned pixel consumer is exercised, establish exactly which source frame each Loop selector consumes and how the decoded frame's timing, bytes and color interpretation are represented. This is an evidence-collection gate, not a decode/render task.

## Required evidence per selector

1. **Identity:** stable selector ID, family/row ID, source media relative path, file size and full SHA-256.
2. **Frame selection:** stream index, source frame index or stable presentation ordinal, exact selector rule, frame order, duplicate/drop behavior and source-to-selector mapping.
3. **Timing:** PTS, DTS if available, duration if available, rational timebase numerator/denominator, declared frame rate and evidence source. Preserve integer ticks and rational values; do not round to decimal seconds as the only representation.
4. **Decoded layout:** width, height, decoded pixel format, plane count/layout, component order, bit depth, bytes per row/stride, active row bytes, padding policy, and exact packed/unpacked representation. Record the decoder/library and version only when already captured in evidence.
5. **Color interpretation:** range, matrix coefficients, primaries, transfer function, chroma location where applicable, alpha/premultiplication handling and orientation/rotation. Use explicit `UNKNOWN` when evidence does not establish a value.
6. **Lineage:** exact D9.9, D9.10 and R1P receipt/manifest paths and SHA-256 values; identify the receipt fields that bind source path, source hash, selector and frame timing.
7. **Pixel identity:** when an existing receipt already captures a decoded-frame byte stream/hash, record its algorithm, byte domain and SHA-256. Do not synthesize a new pixel hash by running a decoder under this read-only gate.

## Evidence hierarchy and fail-closed rules

- Prefer source-pinned receipts and manifests over prose summaries.
- Container-level metadata does not prove decoded pixel format, row stride, RGB packing, per-frame color metadata or actual selector mapping.
- Do not infer missing PTS/timebase or color values from nominal FPS, codec defaults or neighboring frames.
- Preserve rational timing and original integer values.
- Any missing or contradictory field remains `UNKNOWN` / `CONFLICT` and blocks closure for that selector.
- Do not call Godot, FFmpeg or FFprobe; do not decode, render, extract media or produce audio/mux outputs during this read-only closure.

## Closure table (one row per actual Loop selector)

| Field | Required record |
|---|---|
| Selector / family row | Exact canonical IDs |
| Source path / size / SHA-256 | Exact source asset identity |
| Stream / frame / ordering | Exact mapping and selection evidence |
| PTS / DTS / duration / timebase | Original ticks and rational timebase |
| Dimensions / pixel format | Exact decoded-frame values |
| Planes / component order / stride | Exact packed byte layout |
| Range / matrix / primaries / transfer | Exact color interpretation or UNKNOWN |
| Orientation / alpha | Exact value or UNKNOWN |
| D9.9 / D9.10 / R1P links | Paths, hashes and binding fields |
| Pixel-byte hash | Only if already present in evidence |
| Disposition | PASS / UNKNOWN / CONFLICT, with source citation |

## Exit criterion

Every selector proposed for the one-frame D-only proof must have a complete, non-contradictory record for all fields relevant to its source bytes and timing. Missing evidence is not a waiver. Source closure does not authorize consumption: L2 still requires a separately approved successor policy and exact E6 TEST_ONLY execution manifest.
