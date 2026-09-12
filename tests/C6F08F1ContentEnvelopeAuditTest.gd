extends SceneTree

# ============================================================
# C6-F0.8-F1 — Global Content/Payload E2E Audit
#
# Pipeline validado:
# JSON -> Content Definition -> ContentRuntimeRegistry.resolve() -> Runtime -> First Frame
# ============================================================

const ContentRuntimeRegistry = preload("res://core/runtime/ContentRuntimeRegistry.gd")
const ContentRuntime = preload("res://core/runtime/ContentRuntime.gd")

var canonical_files: Array[String] = [
	"definitions/visual_loop_fractal_canonical.json",
	"definitions/visual_loop_vector_field_canonical.json",
	"definitions/visual_loop_particle_flow_canonical.json",
	"definitions/visual_loop_kaleidoscope_canonical.json",
	"definitions/visual_loop_geometric_canonical.json",
	"definitions/visual_drill_tracking_canonical.json",
	"definitions/visual_drill_pursuit_canonical.json",
	"definitions/visual_drill_saccade_canonical.json",
	"definitions/visual_drill_peripheral_scan_canonical.json"
]

var failures: Array[String] = []


func _initialize() -> void:
	print("==================================================")
	print("[TEST] Running C6F08F1ContentEnvelopeAuditTest...")
	print("==================================================")

	var registry := ContentRuntimeRegistry.create_default()

	_assert(
		registry.registered_routes().size() >= 18,
		"Production registry must contain the expected route corpus."
	)

	for file_path in canonical_files:
		_audit_definition(file_path, registry)

	_conclude()


func _assert(condition: bool, fail_msg: String) -> void:
	if not condition:
		failures.append(fail_msg)


func _audit_definition(path: String, registry: ContentRuntimeRegistry) -> void:
	print("[AUDIT] Analizando: %s" % path)

	# 1. IO & JSON parse
	var file := FileAccess.open(path, FileAccess.READ)
	if file == null:
		_assert(false, "[%s] FAILED_TO_OPEN_FILE" % path)
		return

	var raw_text := file.get_as_text()
	file.close()

	var json := JSON.new()
	var parse_error := json.parse(raw_text)
	if parse_error != OK:
		_assert(false, "[%s] INVALID_JSON" % path)
		return

	var definition = json.get_data()
	if not definition is Dictionary:
		_assert(false, "[%s] DEFINITION_NOT_DICTIONARY" % path)
		return

	# 2. Envelope & Metadata Validation
	for required_key in ["kind", "subtype", "schema_version", "rng_version", "seed"]:
		_assert(
			definition.has(required_key),
			"[%s] MISSING_REQUIRED_FIELD:%s" % [path, required_key]
		)

	_assert(definition.get("kind") is String, "[%s] KIND_TYPE_INVALID" % path)
	_assert(definition.get("subtype") is String, "[%s] SUBTYPE_TYPE_INVALID" % path)
	_assert(definition.get("rng_version") == "2.0", "[%s] RNG_VERSION_INVALID" % path)
	
	var kind: String = str(definition.get("kind", ""))
	var subtype: String = str(definition.get("subtype", ""))

	# Asegurar puente de contenido/payload para el runtime
	if not definition.has("payload") and definition.has("content"):
		definition["payload"] = definition["content"]
	elif not definition.has("content") and definition.has("payload"):
		definition["content"] = definition["payload"]

	# 3. Route Resolution
	if not registry.has_route(kind, subtype):
		_assert(false, "[%s] ROUTE_NOT_REGISTERED:%s::%s" % [path, kind, subtype])
		return

	var resolution: Dictionary = registry.resolve(definition)
	_assert(resolution is Dictionary, "[%s] RESOLUTION_RESULT_NOT_DICTIONARY" % path)
	if resolution.is_empty() or not bool(resolution.get("success", false)):
		_assert(false, "[%s] REGISTRY_RESOLUTION_FAILED:%s" % [path, str(resolution.get("error_code", "UNKNOWN"))])
		return

	# 4. Runtime Extraction & Initialization Contract
	var runtime = resolution.get("runtime", null)
	_assert(runtime != null and runtime is ContentRuntime, "[%s] RESOLUTION_RUNTIME_TYPE_INVALID" % path)
	if runtime == null or not runtime is ContentRuntime:
		return
	_assert(runtime.is_initialized(), "[%s] RUNTIME_NOT_INITIALIZED" % path)

	# 5. First-frame execution & Domain-specific checks
	var frame: Dictionary = runtime.next_frame()
	_assert(not frame.is_empty(), "[%s] RUNTIME_PRODUCED_EMPTY_FRAME" % path)
	if frame.is_empty():
		return

	_assert(frame.has("frame_index") and frame.has("payload"), "[%s] FRAME_MISSING_INDEX_OR_PAYLOAD" % path)
	var frame_payload = frame.get("payload", {})
	_assert(frame_payload is Dictionary, "[%s] FRAME_PAYLOAD_INVALID" % path)
	if not frame_payload is Dictionary:
		return

	var reported_generator := ""
	var reported_parameters: Dictionary = {}

	if kind == "visual_loop":
		_assert(frame_payload.has("generator"), "[%s] VISUAL_LOOP_MISSING_GENERATOR" % path)
		_assert(frame_payload.has("layers") and frame_payload["layers"] is Array, "[%s] VISUAL_LOOP_MISSING_LAYERS" % path)

		var layers: Array = frame_payload.get("layers", [])
		if not layers.is_empty() and layers[0] is Dictionary:
			var first_layer: Dictionary = layers[0]
			_assert(first_layer.has("generator"), "[%s] VISUAL_LOOP_LAYER_MISSING_GENERATOR" % path)
			_assert(first_layer.has("parameters") and first_layer["parameters"] is Dictionary, "[%s] VISUAL_LOOP_LAYER_MISSING_PARAMETERS" % path)
			reported_generator = str(first_layer.get("generator", ""))
			reported_parameters = first_layer.get("parameters", {})

	elif kind == "visual_drill":
		_assert(frame_payload.has("generator_type"), "[%s] VISUAL_DRILL_MISSING_GENERATOR_TYPE" % path)
		_assert(frame_payload.has("parameters") and frame_payload["parameters"] is Dictionary, "[%s] VISUAL_DRILL_MISSING_PARAMETERS" % path)
		reported_generator = str(frame_payload.get("generator_type", ""))
		reported_parameters = frame_payload.get("parameters", {})

	print("   -> OK (%s/%s) | Seed: %s | Generator: %s | Frame: %s | Params: %s" % [
		kind,
		subtype,
		str(definition.get("seed", "?")),
		reported_generator,
		str(frame.get("frame_index", "?")),
		str(reported_parameters)
	])


func _conclude() -> void:
	if failures.is_empty():
		print("")
		print("[C6F08_F1_PAYLOAD_E2E_AUDIT] PASS - 9/9 Definitions Validated")
		quit(0)
	else:
		print("")
		print("[C6F08_F1_PAYLOAD_E2E_AUDIT] FAIL - %d errors detected:" % failures.size())
		for failure in failures:
			push_error(failure)
		quit(1)