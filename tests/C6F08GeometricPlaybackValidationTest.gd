extends SceneTree

# ============================================================
# C6-F0.8-D7 — Geometric Playback & Physical Validation
# Verifies state fidelity, geometry confinement, and legacy fallback.
# ============================================================

const VisualContentPlayerScript = preload("res://core/presentation/rendering/VisualContentPlayer.gd")

var failures: Array[String] = []

func _initialize() -> void:
	print("[TEST] Running C6F08GeometricPlaybackValidationTest...")
	await _run_tests()

func _assert(condition: bool, fail_msg: String) -> void:
	if not condition:
		failures.append(fail_msg)

func _run_tests() -> void:
	var def_a = _create_mock_definition(12345, "geometric")
	var def_b = _create_mock_definition(99999, "geometric")
	var def_legacy = _create_mock_definition(12345, "fractal")
	
	var path_a = "user://c6f08_geo_mock_a.json"
	var path_b = "user://c6f08_geo_mock_b.json"
	var path_legacy = "user://c6f08_geo_mock_legacy.json"
	
	_write_json(path_a, def_a)
	_write_json(path_b, def_b)
	_write_json(path_legacy, def_legacy)
	
	var state_a = await _run_player_and_validate(path_a, "GEOMETRIC_A")
	var state_b = await _run_player_and_validate(path_b, "GEOMETRIC_B")
	
	if state_a != null and state_b != null:
		_assert(str(state_a) != str(state_b), "Fallo D7: Diferentes semillas deben variar salida geométrica.")
		
	await _run_player_and_validate(path_legacy, "LEGACY")
	
	_conclude()

func _write_json(path: String, data: Dictionary) -> void:
	var file = FileAccess.open(path, FileAccess.WRITE)
	file.store_string(JSON.stringify(data))
	file.close()

func _create_mock_definition(seed_val: int, generator_type: String) -> Dictionary:
	return {
		"schema_version": "2.0",
		"content_id": "D7_PILOT",
		"content_version": "1.0.0",
		"kind": "visual_loop",
		"subtype": generator_type,
		"engine_version": "1.0",
		"authoring_version": "1.0",
		"rng_version": "2.0",
		"seed": seed_val,
		"presentation": {"profile_id": "social_default_v1", "coordinate_space": "2d"},
		"assets": {"family_id": "f1"},
		"audio": {"profile_id": "a1", "enabled": false},
		"provenance": {"author": "system", "timestamp_ms": 1000},
		"content": {
			"domain": "visual_loop",
			"duration": 0.5,
			"fps": 30,
			"frame_count": 15,
			"visual_parameters": {
				"generator": generator_type,
				"speed": 1.0,
				"complexity": 3,
				"layers": [{"blend_mode": "alpha"}]
			}
		}
	}

func _run_player_and_validate(def_path: String, mode: String):
	var node := Node2D.new()
	var player = VisualContentPlayerScript.new()
	player.content_definition_path = def_path
	node.add_child(player)
	root.add_child(node)
	
	var timeout := 0.0
	while not player.is_ready_initialized and timeout < 2.0:
		await process_frame
		timeout += 0.016
		
	_assert(player.is_ready_initialized, "[%s] VisualContentPlayer failed to initialize." % mode)
	if not player.is_ready_initialized:
		node.queue_free()
		return null
		
	var captured_params = null
	
	while not player.playback_finished:
		if player._current_frame_index == 1 and captured_params == null: 
			var geo_renderer = _find_renderer(player, "GeometricRenderer.gd")
			
			if mode.begins_with("GEOMETRIC"):
				if geo_renderer == null:
					_assert(false, "[%s] GeometricRenderer must exist." % mode)
				else:
					_assert(geo_renderer.visible, "[%s] GeometricRenderer must be visible." % mode)
					var rect = geo_renderer.get("_rect")
					if rect == null:
						_assert(false, "[%s] Geometry Contract: _rect not found." % mode)
					else:
						_assert(rect.size.x > 0 and rect.size.y > 0, "[%s] Geometry Contract invalid." % mode)
						var mat = rect.material as ShaderMaterial
						if mat != null:
							var current_state = player._runtime.get_current_render_state()
							var logical_params = current_state.layer_states[0].parameters
							captured_params = logical_params.duplicate(true)
							
							var raw_zoom = mat.get_shader_parameter("zoom")
							var mat_zoom: float = float(raw_zoom) if raw_zoom != null else 1.0
							var log_zoom: float = float(logical_params.get("zoom", 1.0))
							
							_assert(abs(mat_zoom - log_zoom) < 0.001, "[%s] Fidelity Contract: Shader zoom %f != %f." % [mode, mat_zoom, log_zoom])
			elif mode == "LEGACY":
				if geo_renderer != null:
					_assert(not geo_renderer.visible, "[%s] Legacy Protection: Renderer MUST be hidden." % mode)
					
		await process_frame
		
	_assert(player._current_frame_index == player._total_frames, "[%s] Loop Closure: reached %d, expected %d." % [mode, player._current_frame_index, player._total_frames])
	
	node.queue_free()
	await process_frame
	return captured_params

func _find_renderer(node: Node, script_name: String) -> Node:
	var script = node.get_script()
	if script != null and script_name in script.resource_path:
		return node
	for child in node.get_children():
		var found = _find_renderer(child, script_name)
		if found != null:
			return found
	return null

func _conclude() -> void:
	if failures.is_empty():
		print("[C6F08_GEOMETRIC_PLAYBACK_VALIDATION_SUITE] PASS")
		quit(0)
	else:
		for failure in failures:
			push_error(failure)
		print("[C6F08_GEOMETRIC_PLAYBACK_VALIDATION_SUITE] FAIL failures=%d" % failures.size())
		quit(1)