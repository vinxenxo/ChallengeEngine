# res://core/validation/FamilyAssets.gd
class_name FamilyAssets
extends RefCounted

static func configure_presentation(config: Dictionary, nodes: Dictionary) -> void:
	var assets_cfg: Dictionary = config.get("assets", {})

	if assets_cfg.has("background_path") and nodes.has("background"):
		var background_path: String = str(assets_cfg["background_path"])
		if ResourceLoader.exists(background_path):
			nodes["background"].texture = load(background_path)

	if assets_cfg.has("target_path") and nodes.has("target"):
		var target_path: String = str(assets_cfg["target_path"])
		if ResourceLoader.exists(target_path):
			nodes["target"].texture = load(target_path)

	if assets_cfg.has("object_path") and nodes.has("object"):
		var object_path: String = str(assets_cfg["object_path"])
		if ResourceLoader.exists(object_path):
			nodes["object"].texture = load(object_path)
