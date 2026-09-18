extends SceneTree

func _initialize() -> void:
	print("[TEST] Running C11B0UnifiedSocialFrameContractTest...")
	var failures: Array[String] = []

	_test_profile_geometry(failures)
	_test_mapper(failures)
	_test_visibility_gate(failures)
	_test_scene_geometry(failures)

	if failures.is_empty():
		print("[C11B0_UNIFIED_SOCIAL_FRAME_CONTRACT_SUITE] PASS")
		quit(0)
		return

	for failure in failures:
		print("FAIL: ", failure)
	print("[C11B0_UNIFIED_SOCIAL_FRAME_CONTRACT_SUITE] FAIL count=%d" % failures.size())
	quit(1)

func _test_profile_geometry(failures: Array[String]) -> void:
	var profile := PresentationProfile.new()
	var regions := profile.get_social_regions()
	var header: Rect2 = regions["header_rect"]
	var body: Rect2 = regions["body_rect"]
	var footer: Rect2 = regions["footer_rect"]

	if header != Rect2(0.0, 0.0, 540.0, 144.0):
		failures.append("Unexpected HeaderRegion geometry: %s" % str(header))
	if body != Rect2(0.0, 144.0, 540.0, 672.0):
		failures.append("Unexpected BodyRegion geometry: %s" % str(body))
	if footer != Rect2(0.0, 816.0, 540.0, 144.0):
		failures.append("Unexpected FooterRegion geometry: %s" % str(footer))

func _test_mapper(failures: Array[String]) -> void:
	var body := CoordinateMapper.DEFAULT_SOCIAL_BODY_RECT
	var top_left := CoordinateMapper.map_position(
		Vector2(0.0, 0.0),
		CoordinateMapper.CoordinateSpace.CANVAS_1080X1920,
		CoordinateMapper.PRESENTATION_SIZE,
		body
	)
	var bottom_right := CoordinateMapper.map_position(
		Vector2(1080.0, 1920.0),
		CoordinateMapper.CoordinateSpace.CANVAS_1080X1920,
		CoordinateMapper.PRESENTATION_SIZE,
		body
	)
	var deep_y := CoordinateMapper.map_position(
		Vector2(540.0, 1700.0),
		CoordinateMapper.CoordinateSpace.CANVAS_1080X1920,
		CoordinateMapper.PRESENTATION_SIZE,
		body
	)

	if not top_left.is_equal_approx(Vector2(81.0, 144.0)):
		failures.append("Unexpected mapped top-left: %s" % str(top_left))
	if not bottom_right.is_equal_approx(Vector2(459.0, 816.0)):
		failures.append("Unexpected mapped bottom-right: %s" % str(bottom_right))
	if not deep_y.is_equal_approx(Vector2(270.0, 739.0)):
		failures.append("Unexpected mapped deep-Y sample: %s" % str(deep_y))

func _test_visibility_gate(failures: Array[String]) -> void:
	var body := CoordinateMapper.DEFAULT_SOCIAL_BODY_RECT
	var pass_case := WinningFrameVisibilityGate.evaluate_screen_rects(
		[{
			"id": "object",
			"visible": true,
			"has_geometry": true,
			"screen_rect": Rect2(200.0, 300.0, 40.0, 40.0)
		}],
		body
	)
	if not bool(pass_case["pass"]):
		failures.append("Visibility gate rejected an enclosed entity.")

	var fail_case := WinningFrameVisibilityGate.evaluate_screen_rects(
		[{
			"id": "object",
			"visible": true,
			"has_geometry": true,
			"screen_rect": Rect2(200.0, 800.0, 40.0, 40.0)
		}],
		body
	)
	if bool(fail_case["pass"]):
		failures.append("Visibility gate accepted an entity extending into FooterRegion.")

func _test_scene_geometry(failures: Array[String]) -> void:
	var scene := load("res://core/presentation/UnifiedSocialFrame.tscn")
	if scene == null:
		failures.append("UnifiedSocialFrame.tscn could not be loaded.")
		return
	var frame = scene.instantiate()
	if frame == null:
		failures.append("UnifiedSocialFrame.tscn could not be instantiated.")
		return
	root.add_child(frame)
	await process_frame

	var body: Rect2 = frame.get_body_rect()
	if body != Rect2(0.0, 144.0, 540.0, 672.0):
		failures.append("UnifiedSocialFrame BodyRegion mismatch: %s" % str(body))

	frame.queue_free()
