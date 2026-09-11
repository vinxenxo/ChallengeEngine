extends SceneTree

# ============================================================
# C6-F0.8-D0 — Visual Loop Presentation/State Binding Contract Test
# Validates VisualLoopPresentationBinder boundaries and geometry integration.
# ============================================================

const VisualLoopPresentationBinder = preload("res://core/presentation/VisualLoopPresentationBinder.gd")
const PresentationProfile = preload("res://core/presentation/PresentationProfile.gd")

var failures: Array[String] = []

func _initialize() -> void:
	print("[TEST] Running C6F08VisualLoopBindingContractTest...")
	_run_tests()
	_conclude()

func _assert(condition: bool, fail_msg: String) -> void:
	if not condition:
		failures.append(fail_msg)

func _run_tests() -> void:
	var profile := PresentationProfile.new()
	var binder = VisualLoopPresentationBinder.new()
	
	var mock_frame := {
		"payload": {
			"frame_index": 0,
			"total_frames": 60,
			"layer_states": [
				{"blend_mode": "alpha", "speed": 1.0, "complexity": 2}
			]
		}
	}
	
	var render_model = binder.bind_frame(mock_frame, profile, "GAME")
	
	# 1. El render model debe contener las estructuras requeridas
	_assert(render_model is Dictionary, "Fallo: El binder debe retornar un Dictionary (Render Model).")
	_assert(render_model.has("visual_frame_state"), "Fallo: El Render Model carece de 'visual_frame_state'.")
	_assert(render_model.has("geometry"), "Fallo: El Render Model carece de geometría.")
	
	# 2. El VisualFrameState debe mantenerse íntegro (sin modificaciones mutadas)
	var bound_state = render_model["visual_frame_state"]
	_assert(bound_state["frame_index"] == 0, "Fallo: El frame_index fue alterado por el binder.")
	_assert(bound_state["total_frames"] == 60, "Fallo: El total_frames fue alterado por el binder.")
	_assert(bound_state["layer_states"].size() == 1, "Fallo: Los layer_states fueron alterados.")
	
	# 3. La geometría debe proceder estrictamente del PresentationProfile
	var profile_geom = profile.get_composition_geometry()
	var bound_geom = render_model["geometry"]
	_assert(bound_geom.has("content_rect"), "Fallo: La geometría carece de 'content_rect'.")
	_assert(bound_geom["content_rect"] == profile_geom["content_rect"], "Fallo: El content_rect del binder no coincide con el del PresentationProfile.")
	_assert(bound_geom["header_rect"] == profile_geom["header_rect"], "Fallo: El header_rect no coincide.")
	_assert(bound_geom["footer_rect"] == profile_geom["footer_rect"], "Fallo: El footer_rect no coincide.")

func _conclude() -> void:
	if failures.is_empty():
		print("[C6F08_VISUAL_LOOP_BINDING_CONTRACT_SUITE] PASS")
		quit(0)
	else:
		for failure in failures:
			push_error(failure)
		print("[C6F08_VISUAL_LOOP_BINDING_CONTRACT_SUITE] FAIL failures=%d" % failures.size())
		quit(1)