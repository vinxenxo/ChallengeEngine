# res://core/authoring/AudioProfileValidator.gd
class_name AudioProfileValidator
extends RefCounted

const ALLOWED_ROOT_KEYS := [
	"profile_id",
	"music",
	"sfx"
]

const ALLOWED_MUSIC_KEYS := [
	"enabled",
	"mode",
	"asset_id",
	"procedural_config",
	"volume_db",
	"loop"
]

const ALLOWED_PROCEDURAL_KEYS := [
	"tempo",
	"intensity"
]

const ALLOWED_SFX_KEYS := [
	"enabled",
	"events"
]


static func validate(profile: Dictionary) -> Array:
	var errors: Array[String] = []

	# =========================================================
	# ROOT
	# =========================================================

	for key in profile:
		if not ALLOWED_ROOT_KEYS.has(key):
			errors.append(
				"Unknown root field: '%s'"
				% str(key)
			)

	if (
		not profile.has("profile_id")
		or typeof(profile["profile_id"]) != TYPE_STRING
		or profile["profile_id"].strip_edges().is_empty()
	):
		errors.append(
			"Missing or invalid 'profile_id'"
		)

	# =========================================================
	# MUSIC
	# =========================================================

	if profile.has("music"):
		var music = profile["music"]

		if typeof(music) != TYPE_DICTIONARY:
			errors.append(
				"'music' must be a Dictionary"
			)
		else:
			for key in music:
				if not ALLOWED_MUSIC_KEYS.has(key):
					errors.append(
						"Unknown music field: '%s'"
						% str(key)
					)

			if (
				not music.has("enabled")
				or typeof(music["enabled"]) != TYPE_BOOL
			):
				errors.append(
					"music 'enabled' must be a boolean"
				)

			var music_enabled := bool(
				music.get("enabled", false)
			)

			if music_enabled:
				var mode := str(
					music.get("mode", "")
				)

				if mode != "asset" and mode != "procedural":
					errors.append(
						"music 'mode' must be 'asset' or 'procedural'"
					)

				if mode == "asset":
					_validate_asset_music(
						music,
						errors
					)

				elif mode == "procedural":
					_validate_procedural_music(
						music,
						errors
					)

			# Optional common fields.
			if music.has("volume_db"):
				var volume = music["volume_db"]

				if (
					typeof(volume) != TYPE_INT
					and typeof(volume) != TYPE_FLOAT
				):
					errors.append(
						"music 'volume_db' must be a number"
					)
				else:
					var volume_value := float(volume)

					if not is_finite(volume_value):
						errors.append(
							"music 'volume_db' must be finite"
						)
					elif (
						volume_value < -80.0
						or volume_value > 12.0
					):
						errors.append(
							"music 'volume_db' must be in [-80, 12]"
						)

			if music.has("loop"):
				if typeof(music["loop"]) != TYPE_BOOL:
					errors.append(
						"music 'loop' must be a boolean"
					)

	# =========================================================
	# SFX
	# =========================================================

	if profile.has("sfx"):
		var sfx = profile["sfx"]

		if typeof(sfx) != TYPE_DICTIONARY:
			errors.append(
				"'sfx' must be a Dictionary"
			)
		else:
			for key in sfx:
				if not ALLOWED_SFX_KEYS.has(key):
					errors.append(
						"Unknown sfx field: '%s'"
						% str(key)
					)

			if (
				not sfx.has("enabled")
				or typeof(sfx["enabled"]) != TYPE_BOOL
			):
				errors.append(
					"sfx 'enabled' must be a boolean"
				)

			if sfx.has("events"):
				if typeof(sfx["events"]) != TYPE_DICTIONARY:
					errors.append(
						"sfx 'events' must be a Dictionary"
					)
				else:
					for event_name in sfx["events"]:
						var event_value = sfx["events"][event_name]

						if typeof(event_name) != TYPE_STRING:
							errors.append(
								"sfx event name must be a string"
							)

						if (
							typeof(event_value)
							!= TYPE_STRING
							or str(event_value).strip_edges().is_empty()
						):
							errors.append(
								"sfx event '%s' must reference a non-empty asset ID"
								% str(event_name)
							)

	return errors


static func _validate_asset_music(
	music: Dictionary,
	errors: Array[String]
) -> void:
	if (
		not music.has("asset_id")
		or typeof(music["asset_id"]) != TYPE_STRING
		or music["asset_id"].strip_edges().is_empty()
	):
		errors.append(
			"music 'asset_id' is required when mode is 'asset'"
		)

	if music.has("procedural_config"):
		errors.append(
			"music 'procedural_config' is not allowed when mode is 'asset'"
	)


static func _validate_procedural_music(
	music: Dictionary,
	errors: Array[String]
) -> void:
	if (
		not music.has("procedural_config")
		or typeof(music["procedural_config"]) != TYPE_DICTIONARY
	):
		errors.append(
			"music 'procedural_config' dictionary is required when mode is 'procedural'"
		)
		return

	var config: Dictionary = music["procedural_config"]

	for key in config:
		if not ALLOWED_PROCEDURAL_KEYS.has(key):
			errors.append(
				"Unknown procedural field: '%s'"
				% str(key)
			)

	if not config.has("tempo"):
		errors.append(
			"procedural_config 'tempo' is required"
		)
	else:
		var tempo = config["tempo"]

		if (
			(typeof(tempo) != TYPE_INT)
			and (typeof(tempo) != TYPE_FLOAT)
		):
			errors.append(
				"procedural_config 'tempo' must be a number"
			)
		else:
			var tempo_value := float(tempo)

			if (
				not is_finite(tempo_value)
				or tempo_value <= 0.0
			):
				errors.append(
					"procedural_config 'tempo' must be finite and > 0"
				)

	if not config.has("intensity"):
		errors.append(
			"procedural_config 'intensity' is required"
		)
	else:
		var intensity = config["intensity"]

		if (
			(typeof(intensity) != TYPE_INT)
			and (typeof(intensity) != TYPE_FLOAT)
		):
			errors.append(
				"procedural_config 'intensity' must be a number"
			)
		else:
			var intensity_value := float(intensity)

			if (
				not is_finite(intensity_value)
				or intensity_value < 0.0
				or intensity_value > 1.0
			):
				errors.append(
					"procedural_config 'intensity' must be finite and in [0, 1]"
				)

	if music.has("asset_id"):
		errors.append(
			"music 'asset_id' is not allowed when mode is 'procedural'"
	)