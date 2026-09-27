# Architecture — Current

## Four-layer model

### Definitions / authoring
Canonical challenge definitions, Visual Loop/Drill definitions, profiles and deterministic authoring transforms.

### Deterministic runtime / mechanics
Challenge and drill runtimes consume authored inputs and emit reproducible gameplay/render state. Gameplay truth lives here, not in presentation.

### Passive presentation
`PresentationUI`, `C11CVisualEditorialLayer`, family renderers and presentation binders consume render-ready state. They may style, frame and animate editorial elements but do not calculate mechanics or RNG truth.

### Production orchestration
Movie Maker, FFmpeg/FFprobe, audio export, social sidecars, manifests, batch/review runners and `c11c-producer` coordinate production.

## Producer boundary

Python GUI code must invoke canonical launchers. It may validate user input, construct CLI arguments, show progress, and maintain a local queue, but it must not copy challenge mechanics, seed algorithms or renderer code.

## Challenge path

```text
Challenge JSON
    ↓
canonical authoring / validation
    ↓
engine runtime + legacy audit
    ↓
SimulationResult / frame data
    ↓
presentation binding
    ↓
GeneradorMaestro / Movie Maker
    ↓
FFmpeg / FFprobe / manifest
```

## C11-C visual path

```text
family + seed
    ↓
seeded authoring transform
    ↓
review envelope / render-ready state
    ↓
family renderer + editorial layer
    ↓
Movie Maker / FFmpeg
    ↓
MP4 + audio + social.txt
```
