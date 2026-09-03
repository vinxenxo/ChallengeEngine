extends SceneTree

const RESOLVER = preload("res://core/authoring/DifficultyResolver.gd")

func _init() -> void:
	print("[TEST] Running C6F2ResolverCorrectnessTest...")

	# 1. Exact band boundaries.
	assert(RESOLVER.get_band_for_level(0) == RESOLVER.BAND_EASY)
	assert(RESOLVER.get_band_for_level(1) == RESOLVER.BAND_EASY)
	assert(RESOLVER.get_band_for_level(24) == RESOLVER.BAND_EASY)
	assert(RESOLVER.get_band_for_level(25) == RESOLVER.BAND_NORMAL)
	assert(RESOLVER.get_band_for_level(49) == RESOLVER.BAND_NORMAL)
	assert(RESOLVER.get_band_for_level(50) == RESOLVER.BAND_HARD)
	assert(RESOLVER.get_band_for_level(74) == RESOLVER.BAND_HARD)
	assert(RESOLVER.get_band_for_level(75) == RESOLVER.BAND_EXTREME)
	assert(RESOLVER.get_band_for_level(100) == RESOLVER.BAND_EXTREME)

	var profile: Dictionary = {
		"allowed_parameters": ["distractor_count", "capture_radius", "speed"],
		"base_parameters": {"distractor_count": 5, "speed": 1.0},
		"scaling": {
			"EASY": {"distractor_count": 10},
			"NORMAL": {"distractor_count": 20},
			"HARD": {"distractor_count": 50},
			"EXTREME": {"distractor_count": 80}
		}
	}

	# 2. Base + band resolution.
	var hard_result: Dictionary = RESOLVER.resolve(60, profile, {})
	assert(bool(hard_result.get("success", false)))
	var hard_effective: Dictionary = hard_result.get("effective_parameters", {})
	assert(int(hard_effective.get("distractor_count", -1)) == 50)
	assert(is_equal_approx(float(hard_effective.get("speed", -1.0)), 1.0))

	# 3. Valid override may target an allowed key absent from base/scaling.
	var override_result: Dictionary = RESOLVER.resolve(60, profile, {"capture_radius": 15.0})
	assert(bool(override_result.get("success", false)))
	var override_effective: Dictionary = override_result.get("effective_parameters", {})
	assert(is_equal_approx(float(override_effective.get("capture_radius", -1.0)), 15.0))

	# 4. Override precedence is absolute over the band value.
	var precedence_result: Dictionary = RESOLVER.resolve(60, profile, {"distractor_count": 99})
	assert(bool(precedence_result.get("success", false)))
	var precedence_effective: Dictionary = precedence_result.get("effective_parameters", {})
	assert(int(precedence_effective.get("distractor_count", -1)) == 99)

	# 5. Firewall rejects an undeclared key and returns an explicit failure.
	var invalid_result: Dictionary = RESOLVER.resolve(60, profile, {"fake_key": 99})
	assert(not bool(invalid_result.get("success", true)))
	assert(not str(invalid_result.get("error", "")).is_empty())
	var invalid_effective: Dictionary = invalid_result.get("effective_parameters", {})
	assert(invalid_effective.is_empty())

	# 6. Pure resolver: same inputs must produce the same output.
	var first: Dictionary = RESOLVER.resolve(60, profile, {"capture_radius": 15.0})
	var second: Dictionary = RESOLVER.resolve(60, profile, {"capture_radius": 15.0})
	assert(JSON.stringify(first) == JSON.stringify(second))

	print("[C6F2_RESOLVER_CORRECTNESS_SUITE] PASS")
	quit(0)
