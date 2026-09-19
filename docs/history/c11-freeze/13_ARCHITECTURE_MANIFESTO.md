# C11 Architecture Manifesto

## Why the social frame exists

The same engine must serve challenge videos and visual loops/drills without duplicating scene geometry or leaking presentation concerns into gameplay. A single structural frame gives every output a predictable social composition while keeping the body content independent from the frame chrome.

## UnifiedSocialFrame

`UnifiedSocialFrame` owns three regions only: Header, Body and Footer. It does not calculate content, simulation results or timing semantics.

Its responsibility is analogous to a shell around a deterministic payload. The shell can change visually; the payload contract does not.

## CoordinateMapper

The simulator can continue producing logical geometry at its established scale. `CoordinateMapper` converts that geometry into presentation space, specifically the Body region of the social canvas, using a stable aspect-preserving transform.

This separation answers a critical architectural question: **where an object appears on a phone-sized video is a presentation concern; whether the object hit, parked, was caught or won is a simulation concern.**

## PresentationFramer

`PresentationFramer` makes framing explicit rather than scattering ad-hoc offsets across renderers. This keeps composition policy inspectable, testable and replaceable without rewriting mechanics.

## Winning-frame visibility

The winning frame is still identified by simulation truth. Visibility is a second-stage screen-space question: after the winning snapshot is projected into the Body, is the rendered entity visibly inside the permitted region? The gate therefore validates screen rectangles and does not reinterpret logical coordinates.

## Header / Body / Footer semantics

The regions are structural. The content within them is not hard-wired to a single challenge family. Header may carry the hook or context; Body carries gameplay or visual content; Footer may carry CTA, diagnostics or persistent metadata depending on the active presentation contract.

## Architectural consequence

C11 proves that visual evolution can proceed independently of simulation evolution. That is the principal boundary to preserve in all later work.
