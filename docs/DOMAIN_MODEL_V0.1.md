# DOMAIN_MODEL.md — Modelo de dominio y contratos de datos

## 1. Contrato JSON Declarativo (Entrada Capa 0)

```json
{
  "id": "CHALLENGE_001",
  "engine_version": "0.1",
  "mechanic": "key",
  "mechanic_version": "1.0",
  "video": {
    "fps": 60,
    "hook_duration": 3.0,
    "game_duration": 7.0,
    "cta_duration": 1.0
  },
  "difficulty": {
    "level": 5,
    "tolerance": {
      "rotation_deg": 4.5
    }
  },
  "generation": {
    "seed": 193847
  },
  "assets": {
    "background_path": "res://assets/families/fam_001/bg.png",
    "target_path": "res://assets/families/fam_001/target.png",
    "object_path": "res://assets/families/fam_001/key.png"
  },
  "content": {
    "hook": "¡SOLO EL 1% LLEGA AL CENTRO!",
    "cta": "¡INTÉNTALO TÚ TAMBIÉN!"
  }
}

## Addendum V2.0 — CHALLENGE_003

V2.0 challenges may declare:

```json
"generation": {
  "seed": 314159,
  "rng_version": "2.0"
}
```

`CHALLENGE_003` uses `mechanic: "pilot"` and `mechanic_version: "2.0"`.

The Pilot fixture defines its structural input entirely through deterministic functions of `seed`, semantic stream coordinates, and the challenge configuration. The streams used by the pilot are:

- `10 / TRAJECTORY` — `index_semantics: frame`;
- `20 / CONTROL` — `index_semantics: frame`.

The presentation RNG is deliberately absent from the mechanic's capability scope.

## Current V2.0 Domain Addendum

The domain model now distinguishes three RNG concerns:

```text
DeterministicLCG
    ↓ primitive mathematics
StructuralRNG / MechanicRNGContext
    ↓ structural capability
Simulation Core

CosmeticRNG / PresentationRNGContext
    ↓ presentation capability
Presentation Layer
```

`PilotMechanic` proves the capability model in a deliberately simple domain. `ParkingMechanicV2` applies the same architectural contract to continuous 2D trajectory generation using Bézier geometry, deterministic generation parameters, and per-frame steering noise.
