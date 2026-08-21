# CHECKPOINT 1.0.0-B — FIND V1 MATHEMATICAL CONTRACT

**Status:** DRAFT / REVISION REQUIRED  
**Selected family:** FIND  
**Implementation:** none  
**RNG assignments:** none  

## 1. Scope

FIND is selected as the candidate family for 1.0.0 because it introduces a spatial search problem while remaining compatible with the deterministic, frame-discrete simulation model and the presentation transport demonstrated by CATCH.

MATCH is rejected for 1.0.0 because its multi-entity, multi-state presentation requirements would expand the frozen renderer contract before that capability is needed.

## 2. Domain entities

The candidate domain contains:

- **Scanner:** moving search entity, represented by `p_scan(f)`.
- **Target:** entity the player is expected to locate, represented by `p_target(f)`; static or micro-mobile behavior remains a contract decision.
- **Distractors:** false-positive entities whose spatial relationship with the scanner participates in the mathematical difficulty.
- **Capture radius / aperture:** `r_capture`.

Distractors are therefore **mathematical state**, not decorative-only state.

## 3. Target distance

For each GAME frame:

```text
D_T(f) = |p_scan(f) - p_target(f)|
```

The current candidate contract uses the discrete argmin:

```text
f* = first argmin_f D_T(f)
```

The first-argmin rule is explicit: strict `<` determines the winner when equal distances occur.

## 4. Capture and score

Candidate capture rule:

```text
captured = (D_T(f*) <= r_capture)
```

Candidate score:

```text
score = clamp(1 - D_T(f*) / r_capture, 0, 1)
```

These formulas are structurally compatible with the sovereign mathematical ownership demonstrated by HIT and CATCH, but remain subject to the final contract review.

## 5. Close-call semantics — NOT YET FROZEN

The original draft proposed counting every frame where a distractor lies within `r_capture`. That is **not yet approved** because frame-count semantics would measure dwell time rather than the number of false-positive search events, and could scale unpredictably with scanner speed and distractor geometry.

The preferred candidate is an **event-based definition**:

```text
A distractor false-positive event is one contiguous sequence of GAME frames
in which at least one distractor satisfies D_D(f) <= r_capture,
outside the target-capture window.
```

where:

```text
D_D(f) = min_j |p_scan(f) - d_j|
```

The exact transition/hysteresis rule for separating two adjacent events remains to be finalized before contract freeze.

## 6. Distractor provenance and presentation — NOT YET FROZEN

A critical architectural rule is already fixed:

> Presentation MUST NOT regenerate structural distractor positions from a seed or consume structural RNG independently.

Distractor positions must be generated deterministically by the simulation/setup layer and transported to presentation without becoming a per-frame generic array bus.

The exact transport mechanism is deliberately deferred to the FIND presentation-isolation contract. Possible implementations include a one-time static presentation payload associated with the simulation result, but no transport mechanism is frozen here.

## 7. WinningFrameDetector sovereignty

FIND is expected to be mathematically sovereign and own:

```text
winning_frame
minimum_distance
score
close_calls
```

The generic `WinningFrameDetector` must not overwrite these results if the final FIND contract confirms this ownership.

## 8. RNG — deferred

No streams are assigned in this document.

The future DDI contract may require independent capabilities for:

- target placement;
- distractor topology;
- scanner path parameters.

Only after the mathematical contract is frozen should those dimensions be mapped to semantic streams.

## 9. Freeze gates

Before FIND can be frozen:

1. close-call event semantics are finalized;
2. target static/micro-motion behavior is finalized;
3. distractor topology constraints are defined;
4. deterministic tie behavior is defined;
5. capture/score semantics are validated analytically;
6. presentation transport is specified without structural RNG access;
7. `SimulationResult` compatibility is proven without global contract changes.
