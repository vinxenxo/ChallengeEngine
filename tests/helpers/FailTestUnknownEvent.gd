# tests/audio/helpers/FailTestUnknownEvent.gd
extends SceneTree

func _initialize() -> void:
	var profile = AudioProfileAdapter.from_authoring_profile("c7_test_profile", "non_existent_event_id_999")
	if profile == null:
		quit(0) # Rechazo operacional correcto
	else:
		quit(1) # Rechazo no ocurrido