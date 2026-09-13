# res://tests/C6F0_3MultiContentFoundationTest.gd
extends SceneTree

# ============================================================
# C6-F0.3 Multi-Content Foundation Test Suite
# Exhaustive verification of strict boundaries, numeric bounds, enums,
# additionalProperties guards, and temporal cross-field invariants.
# ============================================================

const ContentSchemaValidator = preload("res://core/validation/ContentSchemaValidator.gd")

var failures: int = 0

func _init() -> void:
	print("[TEST] Running C6F0_3MultiContentFoundationTest...")
	
	_test_valid_visual_loop()
	_test_valid_visual_drill()
	_test_negative_missing_envelope()
	_test_negative_missing_payload()
	_test_negative_extra_top_level_property()
	_test_negative_invalid_kind()
	_test_negative_missing_mandatory_field()
	_test_negative_invalid_content_id_pattern()
	_test_negative_lowercase_content_id()
	_test_negative_extra_envelope_property()
	_test_negative_presentation_theme_wrong_type()
	_test_negative_assets_background_wrong_type()
	_test_negative_invalid_audio_property()
	_test_negative_invalid_provenance_timestamp()
	_test_negative_frame_count_mismatch()
	_test_negative_wrong_payload_for_kind()
	_test_negative_visual_loop_unknown_property()
	_test_negative_malformed_layer_missing_fields()
	_test_negative_visual_drill_missing_stimulus_size()
	
	# New negative tests covering schema numeric bounds & enums
	_test_negative_boundary_tolerance_below_min()
	_test_negative_boundary_tolerance_above_max()
	_test_negative_transition_window_frames_negative()
	_test_negative_pacing_mode_invalid_enum()
	_test_negative_generator_non_string()
	
	if failures == 0:
		print("[C6F0_3_MULTI_CONTENT_FOUNDATION_SUITE] PASS")
		quit(0)
	else:
		push_error("[C6F0_3_MULTI_CONTENT_FOUNDATION_SUITE] FAIL failures=%d" % failures)
		quit(1)

func _test_valid_visual_loop() -> void:
	var doc := {
		"envelope": {
			"schema_version": "2.0",
			"content_id": "LOOP_001",
			"content_version": "1.0",
			"kind": "visual_loop",
			"subtype": "fractal",
			"engine_version": "1.0",
			"authoring_version": "1.0.0",
			"presentation": {"profile_id": "prof_01", "coordinate_space": "cartesian"},
			"assets": {"family_id": "fam_01"},
			"audio": {"profile_id": "aud_01", "enabled": false},
			"provenance": {"author": "system", "timestamp_ms": 1718000000000}
		},
		"payload": {
			"duration": 1.0,
			"fps": 30,
			"frame_count": 30,
			"loop": {"seamless": true, "boundary_tolerance": 0.001, "transition_window_frames": 5},
			"visual_parameters": {
				"generator": "fractal",
				"layers": [{"blend_mode": "normal", "speed": 1.0, "complexity": 3}]
			}
		}
	}
	var res = ContentSchemaValidator.validate_document(doc)
	if not bool(res.get("is_valid", false)):
		_fail("Valid visual loop failed validation: " + str(res.get("errors", [])))
	else:
		print("[PASS] _test_valid_visual_loop")

func _test_valid_visual_drill() -> void:
	var doc := {
		"envelope": {
			"schema_version": "2.0",
			"content_id": "DRILL_001",
			"content_version": "1.0",
			"kind": "visual_drill",
			"subtype": "tracking",
			"engine_version": "1.0",
			"authoring_version": "1.0.0",
			"presentation": {"profile_id": "prof_01", "coordinate_space": "cartesian"},
			"assets": {"family_id": "fam_01"},
			"audio": {"profile_id": "aud_01", "enabled": true},
			"provenance": {"author": "system", "timestamp_ms": 1718000000000}
		},
		"payload": {
			"duration": 2.0,
			"fps": 30,
			"frame_count": 60,
			"exercise_parameters": {"difficulty_tier": 2, "speed_multiplier": 1.2, "pacing_mode": "constant"},
			"stimulus": {"shape": "dot", "size": 10.0, "color": "#FFFFFF"},
			"targets": {"count": 1},
			"distractors": {"count": 2},
			"trajectory": {"pattern": "linear", "speed": 5.0},
			"task": {"type": "tracking", "target_switch_interval": 1.0}
		}
	}
	var res = ContentSchemaValidator.validate_document(doc)
	if not bool(res.get("is_valid", false)):
		_fail("Valid visual drill failed validation: " + str(res.get("errors", [])))
	else:
		print("[PASS] _test_valid_visual_drill")

func _test_negative_missing_envelope() -> void:
	var doc := {"payload": {}}
	var res = ContentSchemaValidator.validate_document(doc)
	if bool(res.get("is_valid", true)):
		_fail("Missing envelope test failed (expected invalid).")
	else:
		print("[PASS] _test_negative_missing_envelope")

func _test_negative_missing_payload() -> void:
	var doc := {"envelope": {}}
	var res = ContentSchemaValidator.validate_document(doc)
	if bool(res.get("is_valid", true)):
		_fail("Missing payload test failed (expected invalid).")
	else:
		print("[PASS] _test_negative_missing_payload")

func _test_negative_extra_top_level_property() -> void:
	var doc := {
		"envelope": {},
		"payload": {},
		"unexpected_root": true
	}
	var res = ContentSchemaValidator.validate_document(doc)
	if bool(res.get("is_valid", true)):
		_fail("Extra top level property test failed (expected invalid).")
	else:
		print("[PASS] _test_negative_extra_top_level_property")

func _test_negative_invalid_kind() -> void:
	var doc := {
		"envelope": {
			"schema_version": "2.0", "content_id": "TEST_01", "content_version": "1.0",
			"kind": "challenge", "subtype": "test", "engine_version": "1.0", "authoring_version": "1.0.0",
			"presentation": {"profile_id": "p", "coordinate_space": "c"},
			"assets": {"family_id": "f"}, "audio": {"profile_id": "a", "enabled": false},
			"provenance": {"author": "sys", "timestamp_ms": 123}
		},
		"payload": {}
	}
	var res = ContentSchemaValidator.validate_document(doc)
	if bool(res.get("is_valid", true)):
		_fail("Challenge kind in content envelope test failed (expected invalid).")
	else:
		print("[PASS] _test_negative_invalid_kind")

func _test_negative_missing_mandatory_field() -> void:
	var doc := {
		"envelope": {
			"schema_version": "2.0", "content_id": "TEST_01",
			"kind": "visual_loop", "subtype": "test", "engine_version": "1.0", "authoring_version": "1.0.0",
			"presentation": {"profile_id": "p", "coordinate_space": "c"},
			"assets": {"family_id": "f"}, "audio": {"profile_id": "a", "enabled": false},
			"provenance": {"author": "sys", "timestamp_ms": 123}
		},
		"payload": {}
	}
	var res = ContentSchemaValidator.validate_document(doc)
	if bool(res.get("is_valid", true)):
		_fail("Missing mandatory field test failed (expected invalid).")
	else:
		print("[PASS] _test_negative_missing_mandatory_field")

func _test_negative_invalid_content_id_pattern() -> void:
	var doc := {
		"envelope": {
			"schema_version": "2.0", "content_id": "", "content_version": "1.0",
			"kind": "visual_loop", "subtype": "test", "engine_version": "1.0", "authoring_version": "1.0.0",
			"presentation": {"profile_id": "p", "coordinate_space": "c"},
			"assets": {"family_id": "f"}, "audio": {"profile_id": "a", "enabled": false},
			"provenance": {"author": "sys", "timestamp_ms": 123}
		},
		"payload": {}
	}
	var res = ContentSchemaValidator.validate_document(doc)
	if bool(res.get("is_valid", true)):
		_fail("Empty content_id test failed (expected invalid).")
	else:
		print("[PASS] _test_negative_invalid_content_id_pattern")

func _test_negative_lowercase_content_id() -> void:
	var doc := {
		"envelope": {
			"schema_version": "2.0", "content_id": "loop_001", "content_version": "1.0",
			"kind": "visual_loop", "subtype": "test", "engine_version": "1.0", "authoring_version": "1.0.0",
			"presentation": {"profile_id": "p", "coordinate_space": "c"},
			"assets": {"family_id": "f"}, "audio": {"profile_id": "a", "enabled": false},
			"provenance": {"author": "sys", "timestamp_ms": 123}
		},
		"payload": {}
	}
	var res = ContentSchemaValidator.validate_document(doc)
	if bool(res.get("is_valid", true)):
		_fail("Lowercase content_id pattern test failed (expected invalid).")
	else:
		print("[PASS] _test_negative_lowercase_content_id")

func _test_negative_extra_envelope_property() -> void:
	var doc := {
		"envelope": {
			"schema_version": "2.0", "content_id": "TEST_01", "content_version": "1.0",
			"kind": "visual_loop", "subtype": "test", "engine_version": "1.0", "authoring_version": "1.0.0",
			"presentation": {"profile_id": "p", "coordinate_space": "c"},
			"assets": {"family_id": "f"}, "audio": {"profile_id": "a", "enabled": false},
			"provenance": {"author": "sys", "timestamp_ms": 123},
			"unexpected_hack_property": true
		},
		"payload": {}
	}
	var res = ContentSchemaValidator.validate_document(doc)
	if bool(res.get("is_valid", true)):
		_fail("Extra envelope property test failed (expected invalid).")
	else:
		print("[PASS] _test_negative_extra_envelope_property")

func _test_negative_presentation_theme_wrong_type() -> void:
	var doc := {
		"envelope": {
			"schema_version": "2.0", "content_id": "TEST_01", "content_version": "1.0",
			"kind": "visual_loop", "subtype": "test", "engine_version": "1.0", "authoring_version": "1.0.0",
			"presentation": {"profile_id": "p", "coordinate_space": "c", "theme": 12345},
			"assets": {"family_id": "f"}, "audio": {"profile_id": "a", "enabled": false},
			"provenance": {"author": "sys", "timestamp_ms": 123}
		},
		"payload": {}
	}
	var res = ContentSchemaValidator.validate_document(doc)
	if bool(res.get("is_valid", true)):
		_fail("Presentation theme wrong type test failed (expected invalid).")
	else:
		print("[PASS] _test_negative_presentation_theme_wrong_type")

func _test_negative_assets_background_wrong_type() -> void:
	var doc := {
		"envelope": {
			"schema_version": "2.0", "content_id": "TEST_01", "content_version": "1.0",
			"kind": "visual_loop", "subtype": "test", "engine_version": "1.0", "authoring_version": "1.0.0",
			"presentation": {"profile_id": "p", "coordinate_space": "c"},
			"assets": {"family_id": "f", "background_path": false},
			"audio": {"profile_id": "a", "enabled": false},
			"provenance": {"author": "sys", "timestamp_ms": 123}
		},
		"payload": {}
	}
	var res = ContentSchemaValidator.validate_document(doc)
	if bool(res.get("is_valid", true)):
		_fail("Assets background_path wrong type test failed (expected invalid).")
	else:
		print("[PASS] _test_negative_assets_background_wrong_type")

func _test_negative_invalid_audio_property() -> void:
	var doc := {
		"envelope": {
			"schema_version": "2.0", "content_id": "TEST_01", "content_version": "1.0",
			"kind": "visual_loop", "subtype": "test", "engine_version": "1.0", "authoring_version": "1.0.0",
			"presentation": {"profile_id": "p", "coordinate_space": "c"},
			"assets": {"family_id": "f"}, "audio": {"profile_id": "a"},
			"provenance": {"author": "sys", "timestamp_ms": 123}
		},
		"payload": {}
	}
	var res = ContentSchemaValidator.validate_document(doc)
	if bool(res.get("is_valid", true)):
		_fail("Invalid audio property test failed (expected invalid).")
	else:
		print("[PASS] _test_negative_invalid_audio_property")

func _test_negative_invalid_provenance_timestamp() -> void:
	var doc := {
		"envelope": {
			"schema_version": "2.0", "content_id": "TEST_01", "content_version": "1.0",
			"kind": "visual_loop", "subtype": "test", "engine_version": "1.0", "authoring_version": "1.0.0",
			"presentation": {"profile_id": "p", "coordinate_space": "c"},
			"assets": {"family_id": "f"}, "audio": {"profile_id": "a", "enabled": false},
			"provenance": {"author": "sys", "timestamp_ms": -5}
		},
		"payload": {}
	}
	var res = ContentSchemaValidator.validate_document(doc)
	if bool(res.get("is_valid", true)):
		_fail("Invalid provenance timestamp test failed (expected invalid).")
	else:
		print("[PASS] _test_negative_invalid_provenance_timestamp")

func _test_negative_frame_count_mismatch() -> void:
	var doc := {
		"envelope": {
			"schema_version": "2.0",
			"content_id": "LOOP_001",
			"content_version": "1.0",
			"kind": "visual_loop",
			"subtype": "fractal",
			"engine_version": "1.0",
			"authoring_version": "1.0.0",
			"presentation": {"profile_id": "prof_01", "coordinate_space": "cartesian"},
			"assets": {"family_id": "fam_01"},
			"audio": {"profile_id": "aud_01", "enabled": false},
			"provenance": {"author": "system", "timestamp_ms": 1718000000000}
		},
		"payload": {
			"duration": 1.0,
			"fps": 30,
			"frame_count": 99,
			"loop": {"seamless": true, "boundary_tolerance": 0.001},
			"visual_parameters": {
				"generator": "fractal",
				"layers": [{"blend_mode": "normal", "speed": 1.0, "complexity": 3}]
			}
		}
	}
	var res = ContentSchemaValidator.validate_document(doc)
	if bool(res.get("is_valid", true)):
		_fail("Frame count mismatch test failed (expected invalid).")
	else:
		print("[PASS] _test_negative_frame_count_mismatch")

func _test_negative_wrong_payload_for_kind() -> void:
	var doc := {
		"envelope": {
			"schema_version": "2.0",
			"content_id": "LOOP_001",
			"content_version": "1.0",
			"kind": "visual_loop",
			"subtype": "fractal",
			"engine_version": "1.0",
			"authoring_version": "1.0.0",
			"presentation": {"profile_id": "prof_01", "coordinate_space": "cartesian"},
			"assets": {"family_id": "fam_01"},
			"audio": {"profile_id": "aud_01", "enabled": false},
			"provenance": {"author": "system", "timestamp_ms": 1718000000000}
		},
		"payload": {
			"duration": 2.0, "fps": 30, "frame_count": 60,
			"exercise_parameters": {"difficulty_tier": 2, "speed_multiplier": 1.2},
			"stimulus": {"shape": "dot", "size": 10.0, "color": "#FFFFFF"},
			"targets": {"count": 1}, "distractors": {"count": 2},
			"trajectory": {"pattern": "linear", "speed": 5.0}, "task": {"type": "tracking"}
		}
	}
	var res = ContentSchemaValidator.validate_document(doc)
	if bool(res.get("is_valid", true)):
		_fail("Wrong payload for kind test failed (expected invalid).")
	else:
		print("[PASS] _test_negative_wrong_payload_for_kind")

func _test_negative_visual_loop_unknown_property() -> void:
	var doc := {
		"envelope": {
			"schema_version": "2.0", "content_id": "LOOP_001", "content_version": "1.0",
			"kind": "visual_loop", "subtype": "fractal", "engine_version": "1.0", "authoring_version": "1.0.0",
			"presentation": {"profile_id": "p", "coordinate_space": "c"},
			"assets": {"family_id": "f"}, "audio": {"profile_id": "a", "enabled": false},
			"provenance": {"author": "sys", "timestamp_ms": 123}
		},
		"payload": {
			"duration": 1.0, "fps": 30, "frame_count": 30,
			"loop": {"seamless": true, "boundary_tolerance": 0.001},
			"visual_parameters": {"generator": "fractal", "layers": [{"blend_mode": "normal", "speed": 1.0, "complexity": 3}]},
			"unauthorized_payload_field": true
		}
	}
	var res = ContentSchemaValidator.validate_document(doc)
	if bool(res.get("is_valid", true)):
		_fail("Visual loop unknown property test failed (expected invalid).")
	else:
		print("[PASS] _test_negative_visual_loop_unknown_property")

func _test_negative_malformed_layer_missing_fields() -> void:
	var doc := {
		"envelope": {
			"schema_version": "2.0", "content_id": "LOOP_001", "content_version": "1.0",
			"kind": "visual_loop", "subtype": "fractal", "engine_version": "1.0", "authoring_version": "1.0.0",
			"presentation": {"profile_id": "p", "coordinate_space": "c"},
			"assets": {"family_id": "f"}, "audio": {"profile_id": "a", "enabled": false},
			"provenance": {"author": "sys", "timestamp_ms": 123}
		},
		"payload": {
			"duration": 1.0, "fps": 30, "frame_count": 30,
			"loop": {"seamless": true, "boundary_tolerance": 0.001},
			"visual_parameters": {
				"generator": "fractal",
				"layers": [{"speed": 1.0}]
			}
		}
	}
	var res = ContentSchemaValidator.validate_document(doc)
	if bool(res.get("is_valid", true)):
		_fail("Malformed layer test failed (expected invalid).")
	else:
		print("[PASS] _test_negative_malformed_layer_missing_fields")

func _test_negative_visual_drill_missing_stimulus_size() -> void:
	var doc := {
		"envelope": {
			"schema_version": "2.0", "content_id": "DRILL_001", "content_version": "1.0",
			"kind": "visual_drill", "subtype": "tracking", "engine_version": "1.0", "authoring_version": "1.0.0",
			"presentation": {"profile_id": "p", "coordinate_space": "c"},
			"assets": {"family_id": "f"}, "audio": {"profile_id": "a", "enabled": true},
			"provenance": {"author": "sys", "timestamp_ms": 123}
		},
		"payload": {
			"duration": 2.0, "fps": 30, "frame_count": 60,
			"exercise_parameters": {"difficulty_tier": 2, "speed_multiplier": 1.2},
			"stimulus": {"shape": "dot", "color": "#FFFFFF"},
			"targets": {"count": 1}, "distractors": {"count": 2},
			"trajectory": {"pattern": "linear", "speed": 5.0}, "task": {"type": "tracking"}
		}
	}
	var res = ContentSchemaValidator.validate_document(doc)
	if bool(res.get("is_valid", true)):
		_fail("Visual drill missing stimulus size test failed (expected invalid).")
	else:
		print("[PASS] _test_negative_visual_drill_missing_stimulus_size")

func _test_negative_boundary_tolerance_below_min() -> void:
	var doc := {
		"envelope": {
			"schema_version": "2.0", "content_id": "LOOP_001", "content_version": "1.0",
			"kind": "visual_loop", "subtype": "fractal", "engine_version": "1.0", "authoring_version": "1.0.0",
			"presentation": {"profile_id": "p", "coordinate_space": "c"},
			"assets": {"family_id": "f"}, "audio": {"profile_id": "a", "enabled": false},
			"provenance": {"author": "sys", "timestamp_ms": 123}
		},
		"payload": {
			"duration": 1.0, "fps": 30, "frame_count": 30,
			"loop": {"seamless": true, "boundary_tolerance": -0.001}, # Invalid < 0.0
			"visual_parameters": {"generator": "fractal", "layers": [{"blend_mode": "normal", "speed": 1.0, "complexity": 3}]}
		}
	}
	var res = ContentSchemaValidator.validate_document(doc)
	if bool(res.get("is_valid", true)):
		_fail("Boundary tolerance below min test failed (expected invalid).")
	else:
		print("[PASS] _test_negative_boundary_tolerance_below_min")

func _test_negative_boundary_tolerance_above_max() -> void:
	var doc := {
		"envelope": {
			"schema_version": "2.0", "content_id": "LOOP_001", "content_version": "1.0",
			"kind": "visual_loop", "subtype": "fractal", "engine_version": "1.0", "authoring_version": "1.0.0",
			"presentation": {"profile_id": "p", "coordinate_space": "c"},
			"assets": {"family_id": "f"}, "audio": {"profile_id": "a", "enabled": false},
			"provenance": {"author": "sys", "timestamp_ms": 123}
		},
		"payload": {
			"duration": 1.0, "fps": 30, "frame_count": 30,
			"loop": {"seamless": true, "boundary_tolerance": 0.02}, # Invalid > 0.01
			"visual_parameters": {"generator": "fractal", "layers": [{"blend_mode": "normal", "speed": 1.0, "complexity": 3}]}
		}
	}
	var res = ContentSchemaValidator.validate_document(doc)
	if bool(res.get("is_valid", true)):
		_fail("Boundary tolerance above max test failed (expected invalid).")
	else:
		print("[PASS] _test_negative_boundary_tolerance_above_max")

func _test_negative_transition_window_frames_negative() -> void:
	var doc := {
		"envelope": {
			"schema_version": "2.0", "content_id": "LOOP_001", "content_version": "1.0",
			"kind": "visual_loop", "subtype": "fractal", "engine_version": "1.0", "authoring_version": "1.0.0",
			"presentation": {"profile_id": "p", "coordinate_space": "c"},
			"assets": {"family_id": "f"}, "audio": {"profile_id": "a", "enabled": false},
			"provenance": {"author": "sys", "timestamp_ms": 123}
		},
		"payload": {
			"duration": 1.0, "fps": 30, "frame_count": 30,
			"loop": {"seamless": true, "boundary_tolerance": 0.001, "transition_window_frames": -5}, # Invalid < 0
			"visual_parameters": {"generator": "fractal", "layers": [{"blend_mode": "normal", "speed": 1.0, "complexity": 3}]}
		}
	}
	var res = ContentSchemaValidator.validate_document(doc)
	if bool(res.get("is_valid", true)):
		_fail("Transition window frames negative test failed (expected invalid).")
	else:
		print("[PASS] _test_negative_transition_window_frames_negative")

func _test_negative_pacing_mode_invalid_enum() -> void:
	var doc := {
		"envelope": {
			"schema_version": "2.0", "content_id": "DRILL_001", "content_version": "1.0",
			"kind": "visual_drill", "subtype": "tracking", "engine_version": "1.0", "authoring_version": "1.0.0",
			"presentation": {"profile_id": "p", "coordinate_space": "c"},
			"assets": {"family_id": "f"}, "audio": {"profile_id": "a", "enabled": true},
			"provenance": {"author": "sys", "timestamp_ms": 123}
		},
		"payload": {
			"duration": 2.0, "fps": 30, "frame_count": 60,
			"exercise_parameters": {"difficulty_tier": 2, "speed_multiplier": 1.2, "pacing_mode": "hyperspeed"}, # Invalid enum
			"stimulus": {"shape": "dot", "size": 10.0, "color": "#FFFFFF"},
			"targets": {"count": 1}, "distractors": {"count": 2},
			"trajectory": {"pattern": "linear", "speed": 5.0}, "task": {"type": "tracking"}
		}
	}
	var res = ContentSchemaValidator.validate_document(doc)
	if bool(res.get("is_valid", true)):
		_fail("Pacing mode invalid enum test failed (expected invalid).")
	else:
		print("[PASS] _test_negative_pacing_mode_invalid_enum")

func _test_negative_generator_non_string() -> void:
	var doc := {
		"envelope": {
			"schema_version": "2.0", "content_id": "LOOP_001", "content_version": "1.0",
			"kind": "visual_loop", "subtype": "fractal", "engine_version": "1.0", "authoring_version": "1.0.0",
			"presentation": {"profile_id": "p", "coordinate_space": "c"},
			"assets": {"family_id": "f"}, "audio": {"profile_id": "a", "enabled": false},
			"provenance": {"author": "sys", "timestamp_ms": 123}
		},
		"payload": {
			"duration": 1.0, "fps": 30, "frame_count": 30,
			"loop": {"seamless": true, "boundary_tolerance": 0.001},
			"visual_parameters": {"generator": 12345, "layers": [{"blend_mode": "normal", "speed": 1.0, "complexity": 3}]} # Non-string generator
		}
	}
	var res = ContentSchemaValidator.validate_document(doc)
	if bool(res.get("is_valid", true)):
		_fail("Generator non-string test failed (expected invalid).")
	else:
		print("[PASS] _test_negative_generator_non_string")

func _fail(message: String) -> void:
	failures += 1
	print("[FAIL] " + message)