extends SceneTree

const PresentationFramer = preload("res://core/presentation/PresentationFramer.gd")

var failures: int = 0

func _initialize() -> void:
	_run()
	print("[C11B02_PRESENTATION_FRAMING_CONTRACT_SUITE] %s" % ("PASS" if failures == 0 else "FAIL"))
	quit(0 if failures == 0 else 1)

func _assert_true(condition: bool, message: String) -> void:
	if not condition:
		failures += 1
		print("[FAIL] ", message)

func _run() -> void:
	var config := {
		"presentation": {
			"framing_policy": "PRIMARY_FOCUS"
		}
	}
	_assert_true(
		PresentationFramer.resolve_policy(config) == PresentationFramer.POLICY_PRIMARY_FOCUS,
		"PRIMARY_FOCUS must resolve from presentation.framing_policy."
	)

	var body := Rect2(0.0, 144.0, 540.0, 672.0)
	var entities := [
		{
			"id": "object",
			"visible": true,
			"screen_rect": Rect2(219.7912, 1359.253, 100.4176, 100.4176)
		},
		{
			"id": "target",
			"visible": true,
			"screen_rect": Rect2(220.0, 430.0, 100.0, 100.0)
		}
	]

	var offset: Vector2 = PresentationFramer.calculate_presentation_offset(
		entities,
		body,
		PresentationFramer.POLICY_PRIMARY_FOCUS,
		"object"
	)
	var object_rect: Rect2 = entities[0]["screen_rect"]
	var object_center: Vector2 = object_rect.position + object_rect.size * 0.5
	var body_center: Vector2 = body.position + body.size * 0.5
	_assert_true(offset.is_equal_approx(body_center - object_center), "PRIMARY_FOCUS offset must center the primary entity.")
