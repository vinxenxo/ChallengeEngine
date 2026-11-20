# E6 L2 Direct RGB24 Visual Probe V1 — 2026-11-20

## Purpose

Advance from Loop source-provenance closure to one bounded, test-only visual frame using the existing C11-C Fractal Bloom source scene and the already-pinned Option C QImage compositor. This is a fresh viewport recapture, not a decoded or byte-identical frame from the historical R1V/Loop22 MP4.

The single case is `E6-L-01`: `fractal_bloom/radial_bloom`, gameplay seed `100006`, frame index `0`. The same existing C11-C scene and transitive source files are SHA-pinned. No C11-C source file is modified.

## Why this route

The historical MP4 streams are H.264 `yuvj420p`, full range, and omit matrix/primaries/transfer metadata. No BT.709 or other profile is inferred. Instead, this probe captures a new frame from the original Godot viewport as opaque RGBA8, verifies alpha=255 for every pixel, and copies the R/G/B bytes in order into RGB24. It performs no YUV decode and applies no colour transform.

This bypass applies only to the new direct viewport recapture. It does not retroactively resolve the colour metadata of the historic MP4s or claim pixel identity with them.

## Single-frame scope

- One original scene: `FractalBloomPrototype.tscn`.
- One family/grammar: `fractal_bloom/radial_bloom`.
- One gameplay seed: `100006`.
- One frame: index `0`.
- One RGB24 buffer: 720×1280, stride 2160, 2,764,800 bytes.
- One QImage composition using the existing `SmoothTransformation` implementation.
- One composed still: 720×1280, with approved body rectangle (108,192,504,896).

The only Godot invocations are (1) a headless import/class scan against a temporary isolated project and (2) the single viewport capture. QImage runs in-process under Python 3.13.14/PySide6 6.11.2.

## Not authorized

No Movie Maker, video decode/encode, historical MP4 read, FFmpeg, FFprobe, audio, mux, six-selector widening, Smoke18, dispatch, BatchId, renderer promotion, or release authority. `E6_ACCEPTED=0` and `release_authority=NONE` remain unchanged.
