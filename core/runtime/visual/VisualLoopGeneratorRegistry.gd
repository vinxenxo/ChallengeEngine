class_name VisualLoopGeneratorRegistry
extends RefCounted

## C6-F0.4.1 — Visual Loop Generator Registry.
## Strict fail-closed canonical dictionary mapping.
## Non-modifiable by external consumers; hard-coded routing table.

static var _registry: Dictionary = {
	"fractal": FractalGenerator.new(),
	"vector_field": VectorFieldGenerator.new(),
	"particle_flow": ParticleFlowGenerator.new(),
	"kaleidoscope": KaleidoscopeGenerator.new(),
	"geometric": GeometricGenerator.new()
}

static func get_generator(generator_type: String) -> VisualLoopGenerator:
	if not _registry.has(generator_type):
		return null
	return _registry[generator_type]