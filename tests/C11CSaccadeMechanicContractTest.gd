extends SceneTree

## C11-C.7 — Saccade mechanic contract test.

const SaccadeGeneratorClass = preload("res://core/runtime/visual_drill/generators/SaccadeGenerator.gd")
const SeedVariationClass = preload("res://core/authoring/VisualDrillSeedVariation.gd")
const BODY_RECT := Rect2(0.0, 144.0, 540.0, 672.0)
const MIN_JUMP_DISTANCE: float = 180.0
const MAX_JUMP_DISTANCE: float = 300.0

var failures: Array[String] = []

func _initialize() -> void:
    var generator := SaccadeGeneratorClass.new()
    var params := _params()
    _test_state_machine(generator, params)
    _test_discrete_positions(generator, params)
    _test_jump_distance(generator, params)
    _test_body_containment(generator, params)
    _test_determinism(generator, params)
    _test_cosmetic_isolation(generator, params)
    _test_seed_authoring_variation(generator, params)
    if failures.is_empty():
        print("[C11C_SACCADE_MECHANIC_CONTRACT_SUITE] PASS")
        quit(0)
    else:
        for failure in failures:
            push_error(failure)
        print("[C11C_SACCADE_MECHANIC_CONTRACT_SUITE] FAIL failures=%d" % failures.size())
        quit(1)

func _test_state_machine(generator: SaccadeGeneratorClass, params: Dictionary) -> void:
    var seen := {}
    for frame in range(80):
        var state: Dictionary = generator.generate(frame, 510, params)
        var phase: String = str(state.get("saccade_state", {}).get("phase", ""))
        seen[phase] = true
    _assert(seen.has("APPEAR"), "Saccade must expose APPEAR phase.")
    _assert(seen.has("IDLE"), "Saccade must expose IDLE phase.")
    _assert(seen.has("VANISH"), "Saccade must expose VANISH phase.")

func _test_discrete_positions(generator: SaccadeGeneratorClass, params: Dictionary) -> void:
    var previous_position := Vector2.ZERO
    var previous_jump_index := -1
    for frame in range(120):
        var state: Dictionary = generator.generate(frame, 510, params)
        var s: Dictionary = state.get("saccade_state", {})
        var jump_index: int = int(s.get("jump_index", -1))
        var p := Vector2(float(s.get("position", {}).get("x", 0.0)), float(s.get("position", {}).get("y", 0.0)))
        if previous_jump_index == jump_index:
            _assert(p.distance_to(previous_position) < 0.001, "Saccade position must remain fixed within a jump cycle; no spatial interpolation.")
        previous_position = p
        previous_jump_index = jump_index

func _test_jump_distance(generator: SaccadeGeneratorClass, params: Dictionary) -> void:
    var checked := 0
    for frame in range(510):
        var state: Dictionary = generator.generate(frame, 510, params)
        var s: Dictionary = state.get("saccade_state", {})
        if int(s.get("jump_index", 0)) > 0 and str(s.get("phase", "")) == "APPEAR":
            var d := float(s.get("jump_distance", 0.0))
            _assert(d >= MIN_JUMP_DISTANCE and d <= MAX_JUMP_DISTANCE, "Saccade jump distance outside guaranteed range: %.2f" % d)
            checked += 1
    _assert(checked > 3, "Saccade contract did not sample enough jumps.")

func _test_body_containment(generator: SaccadeGeneratorClass, params: Dictionary) -> void:
    for frame in range(510):
        var state: Dictionary = generator.generate(frame, 510, params)
        var target: Dictionary = state.get("target_states", [])[0]
        var p := Vector2(float(target.get("x", 0.0)), float(target.get("y", 0.0)))
        _assert(BODY_RECT.grow(-12.0).has_point(p), "Saccade target escaped Body safe zone.")

func _test_determinism(generator: SaccadeGeneratorClass, params: Dictionary) -> void:
    _assert(generator.generate(137, 510, params) == generator.generate(137, 510, params), "Saccade generation is not deterministic.")

func _test_cosmetic_isolation(generator: SaccadeGeneratorClass, params: Dictionary) -> void:
    var a := generator.generate_with_variation(90, 510, params, {"saccade_variant": 0.0})
    var b := generator.generate_with_variation(90, 510, params, {"saccade_variant": 0.99})
    _assert(a.get("target_states", []) == b.get("target_states", []), "saccade_variant must not modify target mechanic truth.")
    _assert(a.get("saccade_state", {}) == b.get("saccade_state", {}), "saccade_variant must not modify saccade mechanic truth.")


func _test_seed_authoring_variation(generator: SaccadeGeneratorClass, params: Dictionary) -> void:
    var seeds: Array[int] = [314159, 944296688, 1411540143, 489652843, 1266632463]
    var positions := {}
    for seed_value in seeds:
        var authored: Dictionary = SeedVariationClass.apply("saccade", seed_value, params)
        var a: Dictionary = generator.generate(8, 510, authored)
        var b: Dictionary = generator.generate(44, 510, authored)
        var pa: Vector2 = Vector2(float(a.get("saccade_state", {}).get("position", {}).get("x", 0.0)), float(a.get("saccade_state", {}).get("position", {}).get("y", 0.0)))
        var pb: Vector2 = Vector2(float(b.get("saccade_state", {}).get("position", {}).get("x", 0.0)), float(b.get("saccade_state", {}).get("position", {}).get("y", 0.0)))
        positions["%.4f:%.4f|%.4f:%.4f" % [pa.x, pa.y, pb.x, pb.y]] = true
    _assert(positions.size() >= 4, "Saccade seeds must alter the authored spatial sequence across review seeds.")

func _params() -> Dictionary:
    return {"duration": 17.0,"fps":30,"frame_count":510,"exercise_parameters":{"difficulty_tier":2,"speed_multiplier":1.0,"pacing_mode":"constant"},"trajectory":{"type":"polar_golden_angle"},"task":{"type":"saccade"}}

func _assert(condition: bool, message: String) -> void:
    if not condition:
        failures.append(message)
