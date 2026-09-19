# C11-B.1 — Social UI Integration Contract

## Objective
Integrate the frozen C11-B.0 UnifiedSocialFrame with the existing C6 presentation components without changing simulation, RNG, FrameSnapshot/SimulationResult semantics or the frozen ContentEnvelope schema.

## Topology
UnifiedSocialFrame is 540x960: Header 0..144, Body 144..816, Footer 816..960. BodyContentRoot is offset -144 inside the clipped BodyRegion, preserving existing full-canvas presentation coordinates while making the Body a real visual sandbox. BodyUIOverlay hosts presentation overlays.

## Reuse
PresentationUI, HookComponent, CTAComponent and PresentationProfile remain the UI primitives. SocialUIBinder is only an adapter from normalized render models / existing presentation metadata to PresentationUI.

## ContentEnvelope
No `ui_elements` or other new envelope property is added. Existing presentation metadata is read without mutation.

## Challenge
Main.tscn mounts UnifiedSocialFrame and places GestorJuego under BodyContentRoot. Existing C11-B.0 CoordinateMapper/PresentationFramer logic therefore keeps its established coordinate space.

## Visual families
VisualContentPlayer mounts UnifiedSocialFrame and mounts ContentRendererHost under BodyContentRoot. RenderedFrameStream and existing visual generators/renderers remain untouched.
