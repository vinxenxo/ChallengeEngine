extends SceneTree

const HIGHLIGHT = preload("res://core/presentation/components/WinningHighlightComponent.gd")

var failures: int = 0

func _init() -> void:
	var root := Control.new()
	root.size = Vector2(540, 960)
	get_root().add_child(root)

	var component := HIGHLIGHT.new(root)
	var rects: Array = [Rect2(Vector2(100, 200), Vector2(80, 60)), Rect2(Vector2(300, 400), Vector2(100, 90))]

	component.show_for_rects(rects)
	_assert(component.is_visible(), "Highlight must be visible when rects are provided.")
	_assert(root.get_node_or_null("WinningHighlight_0") != null, "Primary highlight node missing.")
	_assert(root.get_node_or_null("WinningHighlight_1") != null, "Secondary highlight node missing.")

	component.hide()
	_assert(not component.is_visible(), "Highlight must be hidden after hide().")

	component.show_for_rects([])
	_assert(not component.is_visible(), "Empty rect set must remain hidden.")

	component.show_for_rects([Rect2(Vector2(10, 20), Vector2(30, 40))])
	var panel := root.get_node("WinningHighlight_0") as Control
	_assert(panel.position == Vector2(-2, 8), "Highlight padding position mismatch.")
	_assert(panel.size == Vector2(54, 64), "Highlight padding size mismatch.")

	# Integration contract: PresentationUI owns and orchestrates E4 via RenderModel
	var ui_root := Control.new()
	ui_root.size = Vector2(540, 960)
	root.add_child(ui_root)
	var profile = PresentationProfile.new()
	var ui := PresentationUI.new(ui_root, "default_c6", profile)
	var Binder = load("res://core/presentation/ChallengePresentationBinder.gd")

	var rm1 = Binder.build_frame_render_model("GAME", {
		"ui_state_frame": 41,
		"winning_frame_game": 42,
		"winning_highlight_rects": [Rect2(Vector2(100, 100), Vector2(50, 50))]
	}, profile)
	ui.apply_render_model(rm1)
	_assert(
		not ui.winning_highlight.is_visible(),
		"Highlight must be OFF immediately before winning frame."
	)

	var rm2 = Binder.build_frame_render_model("GAME", {
		"ui_state_frame": 42,
		"winning_frame_game": 42,
		"winning_highlight_rects": [Rect2(Vector2(100, 100), Vector2(50, 50))]
	}, profile)
	ui.apply_render_model(rm2)
	_assert(
		ui.winning_highlight.is_visible(),
		"Highlight must be ON exactly at winning frame."
	)

	var rm3 = Binder.build_frame_render_model("GAME", {
		"ui_state_frame": 43,
		"winning_frame_game": 42,
		"winning_highlight_rects": [Rect2(Vector2(100, 100), Vector2(50, 50))]
	}, profile)
	ui.apply_render_model(rm3)
	_assert(
		not ui.winning_highlight.is_visible(),
		"Highlight must be OFF immediately after winning frame."
	)

	if failures == 0:
		print("[C6E4_WINNING_HIGHLIGHT_CONTRACT_SUITE] PASS")
		quit(0)
	else:
		print("[C6E4_WINNING_HIGHLIGHT_CONTRACT_SUITE] FAIL failures=%d" % failures)
		quit(1)

func _assert(condition: bool, message: String) -> void:
	if not condition:
		failures += 1
		print("[C6E4] " + message)