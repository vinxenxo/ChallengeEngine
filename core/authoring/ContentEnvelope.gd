class_name ContentEnvelope
extends RefCounted

## C6-F0.3.3 — Shared Content Envelope Implementation.
## Strict fail-closed model mirroring the normative JSON schema with full nested type checks and additionalProperties guards.

var schema_version: String = ""
var content_id: String = ""
var content_version: String = ""
var kind: String = ""
var subtype: String = ""
var engine_version: String = ""
var authoring_version: String = ""
var presentation: Dictionary = {}
var assets: Dictionary = {}
var audio: Dictionary = {}
var provenance: Dictionary = {}

static func create_from_dictionary(dict: Dictionary) -> Dictionary:
	var errors: Array[String] = []
	
	if not dict is Dictionary:
		return {"success": false, "errors": ["Input is not a Dictionary."], "envelope": null}
		
	var allowed_keys := [
		"schema_version", "content_id", "content_version", "kind",
		"subtype", "engine_version", "authoring_version",
		"presentation", "assets", "audio", "provenance"
	]
	for key in dict.keys():
		if not key in allowed_keys:
			errors.append("Envelope contains disallowed additional property: '%s'." % str(key))
			
	var required_fields := [
		"schema_version", "content_id", "content_version", "kind",
		"subtype", "engine_version", "authoring_version",
		"presentation", "assets", "audio", "provenance"
	]
	
	for field in required_fields:
		if not dict.has(field):
			errors.append("Missing mandatory envelope field: '%s'." % field)
			
	if not errors.is_empty():
		return {"success": false, "errors": errors, "envelope": null}
		
	if not dict["schema_version"] is String or str(dict["schema_version"]) != "2.0":
		errors.append("Invalid or unsupported schema_version.")
		
	if not dict["content_id"] is String:
		errors.append("Field 'content_id' must be a String.")
	else:
		var cid := str(dict["content_id"])
		var regex := RegEx.new()
		regex.compile("^[A-Z0-9_]+$")
		if cid.is_empty() or not regex.search(cid):
			errors.append("Field 'content_id' does not match normative pattern ^[A-Z0-9_]+$.")
			
	if not dict["content_version"] is String or str(dict["content_version"]).is_empty():
		errors.append("Invalid or empty 'content_version'.")
		
	var c_kind := str(dict["kind"])
	if not c_kind in ["visual_loop", "visual_drill"]:
		errors.append("Invalid envelope kind: '%s'." % c_kind)
		
	if not dict["subtype"] is String or str(dict["subtype"]).is_empty():
		errors.append("Invalid or empty 'subtype'.")
		
	if not dict["engine_version"] is String or str(dict["engine_version"]).is_empty():
		errors.append("Invalid or empty 'engine_version'.")
		
	if not dict["authoring_version"] is String or str(dict["authoring_version"]).is_empty():
		errors.append("Invalid or empty 'authoring_version'.")
		
	if not dict["presentation"] is Dictionary:
		errors.append("Field 'presentation' must be a Dictionary.")
	else:
		var p: Dictionary = dict["presentation"]
		for p_key in p.keys():
			if not p_key in ["profile_id", "coordinate_space", "theme"]:
				errors.append("Presentation contains disallowed property: '%s'." % str(p_key))
		if not p.has("profile_id") or not p["profile_id"] is String or str(p["profile_id"]).is_empty():
			errors.append("Presentation missing or invalid 'profile_id'.")
		if not p.has("coordinate_space") or not p["coordinate_space"] is String or str(p["coordinate_space"]).is_empty():
			errors.append("Presentation missing or invalid 'coordinate_space'.")
		if p.has("theme") and not p["theme"] is String:
			errors.append("Presentation field 'theme' must be a String.")
			
	if not dict["assets"] is Dictionary:
		errors.append("Field 'assets' must be a Dictionary.")
	else:
		var a: Dictionary = dict["assets"]
		for a_key in a.keys():
			if not a_key in ["family_id", "background_path"]:
				errors.append("Assets contains disallowed property: '%s'." % str(a_key))
		if not a.has("family_id") or not a["family_id"] is String or str(a["family_id"]).is_empty():
			errors.append("Assets missing or invalid 'family_id'.")
		if a.has("background_path") and not a["background_path"] is String:
			errors.append("Assets field 'background_path' must be a String.")
			
	if not dict["audio"] is Dictionary:
		errors.append("Field 'audio' must be a Dictionary.")
	else:
		var au: Dictionary = dict["audio"]
		for au_key in au.keys():
			if not au_key in ["profile_id", "enabled"]:
				errors.append("Audio contains disallowed property: '%s'." % str(au_key))
		if not au.has("profile_id") or not au["profile_id"] is String or str(au["profile_id"]).is_empty():
			errors.append("Audio missing or invalid 'profile_id'.")
		if not au.has("enabled") or not au["enabled"] is bool:
			errors.append("Audio missing or invalid 'enabled' boolean.")
			
	if not dict["provenance"] is Dictionary:
		errors.append("Field 'provenance' must be a Dictionary.")
	else:
		var pr: Dictionary = dict["provenance"]
		for pr_key in pr.keys():
			if not pr_key in ["author", "timestamp_ms"]:
				errors.append("Provenance contains disallowed property: '%s'." % str(pr_key))
		if not pr.has("author") or not pr["author"] is String or str(pr["author"]).is_empty():
			errors.append("Provenance missing or invalid 'author'.")
		if not pr.has("timestamp_ms") or not pr["timestamp_ms"] is int or int(pr["timestamp_ms"]) < 0:
			errors.append("Provenance missing or invalid 'timestamp_ms' integer.")

	if not errors.is_empty():
		return {"success": false, "errors": errors, "envelope": null}
		
	var env := ContentEnvelope.new()
	env.schema_version = str(dict["schema_version"])
	env.content_id = str(dict["content_id"])
	env.content_version = str(dict["content_version"])
	env.kind = c_kind
	env.subtype = str(dict["subtype"])
	env.engine_version = str(dict["engine_version"])
	env.authoring_version = str(dict["authoring_version"])
	env.presentation = dict["presentation"].duplicate(true)
	env.assets = dict["assets"].duplicate(true)
	env.audio = dict["audio"].duplicate(true)
	env.provenance = dict["provenance"].duplicate(true)
	
	return {"success": true, "errors": [], "envelope": env}

func to_dictionary() -> Dictionary:
	return {
		"schema_version": schema_version,
		"content_id": content_id,
		"content_version": content_version,
		"kind": kind,
		"subtype": subtype,
		"engine_version": engine_version,
		"authoring_version": authoring_version,
		"presentation": presentation.duplicate(true),
		"assets": assets.duplicate(true),
		"audio": audio.duplicate(true),
		"provenance": provenance.duplicate(true)
	}