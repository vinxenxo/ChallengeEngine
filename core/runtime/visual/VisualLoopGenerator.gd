class_name VisualLoopGenerator
extends RefCounted

## C6-F0.4 / C6-F0.8-D2 — Visual Loop Generator Base
## Polymorphic base for all loop generators.

func generate(loop_frame: int, total_frames: int, layer_params: Dictionary) -> Dictionary:
	push_error("VisualLoopGenerator.generate() must be overridden by subclasses.")
	return {}

## C6-F0.8-D2 Extension: Polymorphic entry point for RNG variation injection.
## Default fallback guarantees backwards compatibility for unmigrated generators.
func generate_with_variation(loop_frame: int, total_frames: int, layer_params: Dictionary, variation: Dictionary) -> Dictionary:
	return generate(loop_frame, total_frames, layer_params)