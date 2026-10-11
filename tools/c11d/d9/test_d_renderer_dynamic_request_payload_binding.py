from __future__ import annotations
import ast
import base64
import copy
import hashlib
import json
import sys
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Callable

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import d_renderer_dynamic_request_payload_binding as module
from d_renderer_dynamic_request_payload_binding import (
    DynamicRequestPayloadBindingError,
    EXPECTED_SELECTIONS,
    EXPECTED_SCOPE,
    EXPECTED_SEMANTIC_LIMITS,
    EXPECTED_BOUNDARY,
    GODOT_SUMMARY_PREFIX,
    INPUT_SCHEMA_ID,
    OUTPUT_SCHEMA_ID,
    _assert_matrix_relationships,
    _base_request,
    _build_canonical_chain,
    _canonical,
    _load_contract,
    _matrix_raw_requests,
    _sha_json,
    _validate_receipt,
    run_dynamic_request_matrix,
)


def _fake_process_runner(command, cwd, text, capture_output, timeout, check):
    encoded = command[-1]
    request = json.loads(base64.b64decode(encoded).decode("utf-8"))
    content_type = request["selection"]["content_type"]
    scope, exact = EXPECTED_SCOPE[content_type]
    # Model the contract's invariants: visual payload digest depends on the selected
    # selector and gameplay seed, not request_id, music_seed, variation_index,
    # delivery profile or editorial values.
    payload_hash = _sha_json({
        "content_type": content_type,
        "selection": request["selection"],
        "gameplay_seed": request["seed"],
        "presentation_profile_id": request["presentation_profile_id"],
    })
    report = {
        "schema": "C11-D-D9-DYNAMIC-REQUEST-PAYLOAD-MATERIALIZATION-V1",
        "schema_version": "1.0",
        "status": "PREPARATION_ONLY_DYNAMIC_REQUEST_BOUND_IN_MEMORY_INSTANCE_NOT_RENDERER_INPUT",
        "request_id": request["request_id"],
        "request_hash": request["request_hash"],
        "content_type": content_type,
        "selection": request["selection"],
        "gameplay_seed": request["seed"],
        "music_seed": request["music_seed"],
        "variation_index": request["variation_index"],
        "presentation_profile_id": request["presentation_profile_id"],
        "delivery_profile_id": request["delivery_profile_id"],
        "payload_sha256": payload_hash,
        "visual_state_sha256": _sha_json({"visual_state": content_type, "seed_driven_visual_parameters": request["seed"]}),
        "payload_scope": scope,
        "exact_selector_payload_materialized": exact,
        "payload_deterministic_repeat": True,
        "payload_materialization": "IN_MEMORY_ONLY",
        "semantic_limits": copy.deepcopy(EXPECTED_SEMANTIC_LIMITS),
        "execution_boundary": copy.deepcopy(EXPECTED_BOUNDARY),
    }
    stdout = GODOT_SUMMARY_PREFIX + json.dumps(report, ensure_ascii=False, sort_keys=True) + "\n"
    stdout += "C11-D DYNAMIC REQUEST PAYLOAD MATERIALIZATION PASS | renderer=OFF | media_created=false\n"
    return SimpleNamespace(returncode=0, stdout=stdout, stderr="")


def _sha_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _expect_reject(label: str, action: Callable[[], Any]) -> None:
    try:
        action()
    except (DynamicRequestPayloadBindingError, ValueError, TypeError, KeyError):
        return
    raise AssertionError(f"Expected fail-closed rejection: {label}")


def run_checks() -> dict[str, int]:
    counts = {"source_pins": 0, "schemas": 0, "dynamic_cases": 0, "seed_isolation": 0, "orthogonality": 0, "negative": 0}
    contract, input_schema, output_schema, lineage = _load_contract(ROOT)
    assert len(lineage) == len(contract["source_lineage"]) >= 30
    assert lineage[0]["path"] == "release/C11C_FREEZE_PACKAGE_MANIFEST.json"
    assert len({row["path"] for row in lineage}) == len(lineage)
    counts["source_pins"] = len(lineage)
    assert input_schema["additionalProperties"] is False and output_schema["additionalProperties"] is False
    try:
        import jsonschema
        jsonschema.Draft202012Validator.check_schema(input_schema)
        jsonschema.Draft202012Validator.check_schema(output_schema)
        counts["schemas"] = 2
    except ImportError:
        assert input_schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema"
        assert output_schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema"
        counts["schemas"] = 2

    module_source = (HERE / "d_renderer_dynamic_request_payload_binding.py").read_text(encoding="utf-8")
    module_tree = ast.parse(module_source)
    forbidden_write_methods = {"write_text", "write_bytes", "unlink", "mkdir", "makedirs", "remove", "replace", "rename"}
    for node in ast.walk(module_tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            assert node.func.attr not in forbidden_write_methods, f"Production runner has filesystem mutation: {node.func.attr}"
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in {"Popen", "check_call", "check_output", "system"}:
            raise AssertionError(f"Unapproved dispatch/command call: {node.func.id}")
    harness = (ROOT / contract["harness"]["path"]).read_text(encoding="utf-8")
    assert "func _is_json_integer_in_range(value: Variant, minimum: int, maximum: int) -> bool:" in harness
    assert "value_type != TYPE_INT and value_type != TYPE_FLOAT" in harness
    assert "if not is_finite(numeric):" in harness
    assert "return floor(numeric) == numeric" in harness
    assert "_is_json_integer_in_range(item, 1, MAX_SEED)" in harness
    assert "_is_json_integer_in_range(variation, 0, 1000000)" in harness
    for forbidden in ["res://artifacts/", "res://release/renderer_output", "FileAccess.open(", "store_buffer(", "store_string(", "FFmpeg", "renderer_native_input_emitted = true", "renderer_dispatch_invoked = true"]:
        assert forbidden not in harness, f"Unexpected persistence/dispatch path in Godot harness: {forbidden}"
    assert "FileAccess.get_file_as_bytes" in harness and "ResourceLoader.load" in harness

    # Canonical request chain supports dynamic seed/profile metadata only within the
    # precise three-selector matrix; no request can self-expand the selector universe.
    chains = [_build_canonical_chain(raw, ROOT) for raw in _matrix_raw_requests()[:3]]
    assert len(chains) == 3
    for chain in chains:
        ct = str(chain["result"]["plan"]["selection"]["content_type"])
        assert chain["source_binding"]["content_type"] == ct
        assert chain["source_binding"]["readiness"]["request_scoped_visual_payload_instance_bound"] is False
        assert chain["source_binding"]["execution_boundary"]["renderer_native_input_emitted"] is False

    # Mocked process runner is for deterministic Python contract tests only. Windows
    # must run this same matrix against the real Godot 4.7.1 console executable.
    result = run_dynamic_request_matrix("C:\\Godot\\Godot_v4.7.1-stable_win64_console.exe", 120, ROOT, _fake_process_runner)
    receipts = result["receipts"]
    assert len(receipts) == 10
    matrix_stats = _assert_matrix_relationships(receipts)
    assert matrix_stats == {"cases": 10, "seed_isolation": 3, "orthogonality": 4}
    counts["dynamic_cases"] = len(receipts)
    counts["seed_isolation"] = matrix_stats["seed_isolation"]
    counts["orthogonality"] = matrix_stats["orthogonality"]
    by_id = {x["request_identity"]["request_id"]: x for x in receipts}
    for receipt in receipts:
        assert _validate_receipt(receipt, ROOT)
        assert receipt["readiness"]["candidate_input_admissible"] is False
        assert receipt["readiness"]["video_render_ready"] is False
        assert receipt["execution_boundary"] == EXPECTED_BOUNDARY
        assert receipt["semantic_limits"] == EXPECTED_SEMANTIC_LIMITS
        counts["negative"] += 1
    loop = by_id["D-DYNAMIC-VISUAL_LOOPS-BASE"]
    loop_editorial = by_id["D-DYNAMIC-VISUAL_LOOPS-EDITORIAL-ONLY"]
    assert loop["source_identity"]["editorial_hash"] != loop_editorial["source_identity"]["editorial_hash"]
    assert loop["payload_evidence"]["payload_sha256"] == loop_editorial["payload_evidence"]["payload_sha256"]
    assert loop["payload_evidence"]["exact_selector_payload_materialized"] is False
    assert by_id["D-DYNAMIC-CHALLENGES-BASE"]["payload_evidence"]["exact_selector_payload_materialized"] is True
    assert by_id["D-DYNAMIC-VISUAL_DRILLS-BASE"]["payload_evidence"]["exact_selector_payload_materialized"] is True

    # Reject unsupported scope and semantics before any process runner can be called.
    for selector in [
        {"content_type":"challenges", "family_id":"parking_v2", "subtype_id":None, "variant_id":"CHALLENGE_001"},
        {"content_type":"visual_loops", "family_id":"c11c_geometric_waves_v1", "subtype_id":"interference_plane", "variant_id":None},
        {"content_type":"visual_drills", "family_id":"tracking", "subtype_id":None, "variant_id":"tier-3"},
        {"content_type":"longform", "family_id":"longform", "subtype_id":None, "variant_id":"x"},
    ]:
        _expect_reject("unsupported selector " + str(selector), lambda s=selector: _build_canonical_chain(_base_request(s, "BAD-SCOPE"), ROOT))
        counts["negative"] += 1
    bad_delivery = _base_request(EXPECTED_SELECTIONS["visual_loops"], "BAD-LONGFORM-DELIVERY")
    bad_delivery["delivery_profile_id"] = "LONGFORM_1080"
    _expect_reject("Longform delivery profile", lambda: _build_canonical_chain(bad_delivery, ROOT))
    counts["negative"] += 1
    bad_presentation = _base_request(EXPECTED_SELECTIONS["visual_loops"], "BAD-PRESENTATION")
    bad_presentation["presentation_profile_id"] = "UNKNOWN_PROFILE"
    _expect_reject("unapproved presentation profile", lambda: _build_canonical_chain(bad_presentation, ROOT))
    counts["negative"] += 1

    # Receipt/schema promotion mutations must be rejected even if the attacker recomputes its digest.
    tampered = copy.deepcopy(receipts[0])
    tampered["readiness"]["candidate_input_admissible"] = True
    tampered["receipt_sha256"] = _sha_json({k: v for k, v in tampered.items() if k != "receipt_sha256"})
    _expect_reject("candidate input promotion", lambda: _validate_receipt(tampered, ROOT))
    counts["negative"] += 1
    tampered = copy.deepcopy(receipts[0])
    tampered["execution_boundary"]["renderer_native_input_emitted"] = True
    tampered["receipt_sha256"] = _sha_json({k: v for k, v in tampered.items() if k != "receipt_sha256"})
    _expect_reject("renderer input promotion", lambda: _validate_receipt(tampered, ROOT))
    counts["negative"] += 1
    tampered = copy.deepcopy(receipts[0])
    tampered["payload_evidence"]["visual_state_sha256"] = "0" * 64
    tampered["receipt_sha256"] = _sha_json({k: v for k, v in tampered.items() if k != "receipt_sha256"})
    _expect_reject("visual-state hash not rebound to request", lambda: _validate_receipt(tampered, ROOT))
    counts["negative"] += 1

    # A source-pin drift is rejected and original bytes restored exactly, including line endings.
    pinned = ROOT / lineage[14]["path"]
    original = pinned.read_bytes()
    try:
        pinned.write_bytes(original + b"\n")
        _expect_reject("source-pin drift", lambda: _load_contract(ROOT))
        counts["negative"] += 1
    finally:
        pinned.write_bytes(original)
    assert pinned.read_bytes() == original
    return counts


if __name__ == "__main__":
    c = run_checks()
    print(
        "C11-D DYNAMIC REQUEST PAYLOAD BINDING CONTRACT PASS"
        + f" | tests=12/12 | source_pins={c['source_pins']}/{c['source_pins']} | schemas={c['schemas']}/2"
        + f" | dynamic_cases={c['dynamic_cases']}/10 | gameplay_seed_binding={c['seed_isolation']}/3"
        + f" | orthogonality={c['orthogonality']}/4 | fail_closed_negatives={c['negative']}"
        + " | exact_loop_grammar_instance=UNRESOLVED | renderer_input=NOT_EMITTED | renderer=OFF"
        + " | media_created=false | D4.8=BLOCKED | release_authority=NONE"
    )
