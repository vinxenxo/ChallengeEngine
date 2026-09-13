# res://core/runtime/visual_drill/VisualDrillGeneratorRegistry.gd
class_name VisualDrillGeneratorRegistry
extends RefCounted

## C6-F0.4.2 — Visual Drill Generator Registry.
## Strict fail-closed canonical dictionary mapping for visual drill generators.

static var _registry: Dictionary = {
	"tracking": TrackingGenerator.new(),
	"pursuit": PursuitGenerator.new(),
	"saccade": SaccadeGenerator.new(),
	"peripheral_scan": PeripheralScanGenerator.new()
}

static func get_generator(generator_type: String) -> VisualDrillGenerator:
	if not _registry.has(generator_type):
		return null
	return _registry[generator_type]