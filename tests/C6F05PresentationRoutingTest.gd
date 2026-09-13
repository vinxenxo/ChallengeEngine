# res://tests/C6F05PresentationRoutingTest.gd
extends SceneTree

# ============================================================
# C6-F0.5 Presentation Routing & Isolation Test Suite
# Validates fail-closed presentation registry routing via RenderedFrameStream authority.
# Ensures payload.domain is ignored for routing and PresentationProfile composition behaves correctly.
# ============================================================

const PresentationBinderRegistry = preload("res://core/presentation/PresentationBinderRegistry.gd")
const VisualLoopPresentationBinder = preload("res://core/presentation/VisualLoopPresentationBinder.gd")
const VisualDrillPresentationBinder = preload("res://core/presentation/VisualDrillPresentationBinder.gd")
const RenderedFrameStream = preload("res://core/runtime/RenderedFrameStream.gd")
const PresentationProfile = preload("res://core/presentation/PresentationProfile.gd")

var failures: Array[String] = []

func _init() -> void:
	print("[TEST] Running C6F05PresentationRoutingTest...")
	
	_test_registry_stream_routing_fail_closed()
	_test_visual_loop_routing_and_payload_isolation()
	_test_visual_drill_routing_and_payload_isolation()
	
	if failures.is_empty():
		print("[C6F0_5_PRESENTATION_ROUTING_SUITE] PASS")
		quit(0)
	else:
		for failure in failures:
			push_error(failure)
		print("[C6F0_5_PRESENTATION_ROUTING_SUITE] FAIL failures=%d" % failures.size())
		quit(1)

func _test_registry_stream_routing_fail_closed() -> void:
	var registry := PresentationBinderRegistry.create_default()
	
	# 1. Null stream
	var res_null = registry.resolve_stream(null)
	_assert(not bool(res_null.get("success", false)), "Registry must fail on null stream.")
	
	# 2. Unknown subtype
	var stream_unknown = RenderedFrameStream.new("visual_loop", "unknown_subtype", 30)
	var res_unknown = registry.resolve_stream(stream_unknown)
	_assert(not bool(res_unknown.get("success", false)), "Registry must fail on unknown subtype.")
	
	# 3. Empty components
	var stream_empty = RenderedFrameStream.new("", "fractal", 30)
	var res_empty = registry.resolve_stream(stream_empty)
	_assert(not bool(res_empty.get("success", false)), "Registry must fail on empty kind.")
	
	# 4. Strict matching (no silent normalization)
	var stream_padded = RenderedFrameStream.new("visual_loop", " fractal ", 30)
	var res_padded = registry.resolve_stream(stream_padded)
	_assert(not bool(res_padded.get("success", false)), "Registry must not normalize padded strings.")
	
	var stream_upper = RenderedFrameStream.new("visual_loop", "FRACTAL", 30)
	var res_upper = registry.resolve_stream(stream_upper)
	_assert(not bool(res_upper.get("success", false)), "Registry must not normalize uppercase strings.")
	
	print("[PASS] _test_registry_stream_routing_fail_closed")

func _test_visual_loop_routing_and_payload_isolation() -> void:
	var registry := PresentationBinderRegistry.create_default()
	
	# Authoritative routing from stream
	var stream = RenderedFrameStream.new("visual_loop", "fractal", 30)
	var res = registry.resolve_stream(stream)
	
	_assert(bool(res.get("success", false)), "Registry must resolve canonical visual_loop/fractal stream.")
	if not bool(res.get("success", false)):
		return
		
	var binder = res.get("binder")
	_assert(binder is VisualLoopPresentationBinder, "Resolved binder must be VisualLoopPresentationBinder.")
	
	# Malicious/Contradictory Frame Payload
	var dummy_frame := {
		"frame_index": 5,
		"payload": {"domain": "challenge", "generator_type": "fractal"} 
	}
	
	# Test with null profile
	var model_null: Dictionary = binder.bind_frame(dummy_frame, null, "CTA")
	_assert(model_null.get("cta_main", "") == "LINK IN BIO", "Visual loop binder must preserve default CTA contract with null profile.")
	
	# Test with real PresentationProfile instance
	var profile := PresentationProfile.new()
	profile.composition = {"cta_main": "CUSTOM CTA", "cta_sub": "Custom sub"}
	
	var model_profile: Dictionary = binder.bind_frame(dummy_frame, profile, "CTA")
	_assert(model_profile.get("cta_main", "") == "CUSTOM CTA", "Visual loop binder must respect real PresentationProfile composition.")
	
	# 1. Check Shared Envelope
	_assert(model_profile.get("cta_visible", false) == true, "Visual loop model must inject CTA state.")
		
	# 2. Check strict exclusion of Challenge semantics
	var forbidden_keys = ["is_success_game", "reveal_visible", "winning_frame", "success_highlight_rects"]
	for k in forbidden_keys:
		_assert(not model_profile.has(k), "Visual loop model must not leak Challenge-specific key: " + k)
			
	# 3. Check domain specific payload pass-through
	_assert(model_profile.has("visual_frame_state"), "Visual loop model must contain 'visual_frame_state'.")
	
	var passed_payload: Dictionary = model_profile.get("visual_frame_state", {})
	_assert(passed_payload.get("domain", "") == "challenge", "Payload must be passed through untouched, proving it was strictly content, not authority.")
		
	print("[PASS] _test_visual_loop_routing_and_payload_isolation")

func _test_visual_drill_routing_and_payload_isolation() -> void:
	var registry := PresentationBinderRegistry.create_default()
	
	var stream = RenderedFrameStream.new("visual_drill", "tracking", 30)
	var res = registry.resolve_stream(stream)
	
	_assert(bool(res.get("success", false)), "Registry must resolve canonical visual_drill/tracking stream.")
	if not bool(res.get("success", false)):
		return
		
	var binder = res.get("binder")
	_assert(binder is VisualDrillPresentationBinder, "Resolved binder must be VisualDrillPresentationBinder.")
	
	var dummy_frame := {
		"frame_index": 10,
		"payload": {"generator_type": "tracking"}
	}
	
	# Test with real PresentationProfile instance
	var profile := PresentationProfile.new()
	profile.composition = {"cta_main": "DRILL CTA"}
	
	var model: Dictionary = binder.bind_frame(dummy_frame, profile, "GAME")
	_assert(model.get("cta_main", "") == "DRILL CTA", "Visual drill binder must respect real PresentationProfile composition.")
	
	_assert(model.get("cta_visible", true) == false, "Visual drill model must hide CTA in GAME state.")
		
	var forbidden_keys = ["is_success_game", "reveal_visible", "winning_frame", "success_highlight_rects"]
	for k in forbidden_keys:
		_assert(not model.has(k), "Visual drill model must not leak Challenge-specific key: " + k)
			
	_assert(model.has("visual_drill_frame_state"), "Visual drill model must contain 'visual_drill_frame_state'.")
		
	print("[PASS] _test_visual_drill_routing_and_payload_isolation")

func _assert(condition: bool, message: String) -> void:
	if not condition:
		failures.append(message)