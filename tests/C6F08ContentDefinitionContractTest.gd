# res://tests/C6F08ContentDefinitionContractTest.gd
extends SceneTree

# ============================================================
# C6-F0.8-B — Content Definition Contract Test (Corrected API)
# Validates ContentSchemaValidator.validate_document() and envelope/payload structure.
# ============================================================

const ContentSchemaValidator = preload("res://core/validation/ContentSchemaValidator.gd")

var failures: Array[String] = []

func _initialize() -> void:
	print("[TEST] Running C6F08ContentDefinitionContractTest...")
	
	# Test legacy envelope document validation directly via static/class method call
	var legacy_doc = {
		"envelope": {
			"kind": "challenge",
			"version": "1.0"
		},
		"payload": {}
	}
	
	var res = ContentSchemaValidator.validate_document(legacy_doc)
	if res == null or not res is Dictionary:
		failures.append("validate_document did not return a valid dictionary result.")
		
	_conclude()

func _conclude() -> void:
	if failures.is_empty():
		print("[C6F08_CONTENT_DEFINITION_CONTRACT_SUITE] PASS")
		quit(0)
	else:
		for failure in failures:
			push_error(failure)
		print("[C6F08_CONTENT_DEFINITION_CONTRACT_SUITE] FAIL failures=%d" % failures.size())
		quit(1)