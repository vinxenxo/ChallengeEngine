# tests/audio/helpers/FailTestUnknownAsset.gd
extends SceneTree

func _initialize() -> void:
	var result = AudioAssetRegistry.resolve_asset("non_existent_asset_id_999")
	if result.is_empty():
		quit(0) # Rechazo operacional correcto
	else:
		quit(1) # Rechazo no ocurrido