#!/usr/bin/env python3
"""Static review of the source-runtime to allowlisted-consumer composition harness."""
from __future__ import annotations
import hashlib, json, pathlib, sys

EXPECTED_C11C = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
EXPECTED_RUNTIME_RECEIPT = "ea3acf30b29e8d59fcfa87e0452cb0f979ed7c0d48d9412999ba405c2a86098d"
EXPECTED_RUNTIME_STDOUT = "86e67fa5d548108603bee16466daa8c5ceb2172c5d904afab2f912291ab524cd"
EXPECTED_RUNTIME_STATIC_STDOUT = "bbf030cb4aa8319d007eae259a7dac52294a29fc9cddd1d242b09306b25548df"
EXPECTED_EMPTY = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
EXPECTED_RUNTIME_ACCEPTANCE_RECORD_SHA = "5ce4cddace9a8a04b4c1ba520cfdeeb79ee3a7e1952dc70f60baf45e02623d34"
EXPECTED_COMPOSITION_CONTRACT_SHA = "d3265f1ba91dc664e85bbb0dc87ea6b145f0fed34ffa4552412c8fa70c19b2ab"
EXPECTED_CONSUMER_SHA = "2376d4c9208d749b3681f8083d1d0be1a5658f62930b9b92167916196aec3eef"
EXPECTED_BRIDGE_SHA = "c53f04df064b3697f8dd02cd779f8ef002a4e3e2d40fa0e01aa7d9b1a80a8191"
EXPECTED_SIMULATION_RESULT_SHA = "2e040003d1a1661f84f049d69dbfb0ab07537f9d837fa4484667041c5abac296"
EXPECTED_FRAME_SNAPSHOT_SHA = "61060d0937063400447cd5f2513265cb82d8e38017f5bd097c2870da03967180"
EXPECTED_CANDIDATES = {
    "CHALLENGE_003": ("challenges/CHALLENGE_003.json", "38cb0166482c5ba4862deef8ab75dad4a6e1524590b6850312bab5238f078419", "target_x"),
    "CHALLENGE_005": ("challenges/CHALLENGE_005.json", "e173736fcbb0e340cd250be1111fa9d38489934d55cc0e0c93835c66f9596e30", "target_position"),
    "CHALLENGE_006": ("challenges/CHALLENGE_006.json", "2d7d7397cbb0a2109f300859a5d7c0830ded0553522a5120f61750f5bc0b5694", "target_position"),
    "CHALLENGE_007": ("challenges/CHALLENGE_007.json", "269f9588e5a6b7d253e2e944440cc41dc3a9db8967775ffa819edebe729a3a61", "target_position"),
}


def sha(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

checks: list[tuple[str, bool]] = []
def check(name: str, value: bool) -> None:
    checks.append((name, bool(value)))

def main() -> int:
    if len(sys.argv) != 2:
        print("usage: python test_d_renderer_challenge_visual_payload_v2b_allowlisted_coordinate_source_composition_static.py <repo-root>", file=sys.stderr)
        return 2
    repo = pathlib.Path(sys.argv[1]).resolve()
    def read(rel: str) -> bytes:
        return (repo / rel).read_bytes()
    def textfile(rel: str) -> str:
        return read(rel).decode("utf-8")

    frozen = repo / "release/C11C_FREEZE_PACKAGE_MANIFEST.json"
    acceptance_path = repo / "definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_ALLOWLISTED_COORDINATE_CONSUMER_RUNTIME_ACCEPTANCE_RECORD_V2_20261022.json"
    contract_path = repo / "definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_ALLOWLISTED_COORDINATE_CONSUMER_SOURCE_COMPOSITION_CONTRACT_V1.json"
    schema_path = repo / "definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_ALLOWLISTED_COORDINATE_CONSUMER_SOURCE_COMPOSITION_CONTRACT_SCHEMA_V1.json"
    consumer_path = repo / "tools/c11d/d9/allowlisted_coordinate_consumer_review_only_v2.gd"
    harness_path = repo / "tools/c11d/d9/test_allowlisted_coordinate_consumer_source_composition_runtime.gd"
    bridge_path = repo / "core/execution/ChallengeRuntimeBridge.gd"
    simulation_path = repo / "core/simulation/SimulationResult.gd"
    snapshot_path = repo / "core/data/FrameSnapshot.gd"

    check("frozen_manifest_sha", frozen.is_file() and sha(frozen) == EXPECTED_C11C)
    check("runtime_acceptance_record_file_exists", acceptance_path.is_file())
    check("runtime_acceptance_record_sha", acceptance_path.is_file() and sha(acceptance_path) == EXPECTED_RUNTIME_ACCEPTANCE_RECORD_SHA)
    check("composition_contract_file_exists", contract_path.is_file())
    check("composition_contract_sha", contract_path.is_file() and sha(contract_path) == EXPECTED_COMPOSITION_CONTRACT_SHA)
    check("composition_schema_file_exists", schema_path.is_file())
    check("consumer_v2_exists", consumer_path.is_file())
    check("consumer_v2_sha", consumer_path.is_file() and sha(consumer_path) == EXPECTED_CONSUMER_SHA)
    check("runtime_bridge_sha", bridge_path.is_file() and sha(bridge_path) == EXPECTED_BRIDGE_SHA)
    check("simulation_result_sha", simulation_path.is_file() and sha(simulation_path) == EXPECTED_SIMULATION_RESULT_SHA)
    check("frame_snapshot_sha", snapshot_path.is_file() and sha(snapshot_path) == EXPECTED_FRAME_SNAPSHOT_SHA)
    check("harness_exists", harness_path.is_file())

    acceptance = json.loads(acceptance_path.read_text(encoding="utf-8"))
    check("acceptance_schema", acceptance.get("schema") == "C11D-V2B-ALLOWLISTED-COORDINATE-CONSUMER-RUNTIME-ACCEPTANCE-RECORD-V2")
    check("acceptance_status", acceptance.get("status") == "PASS_GODOT_MONO_RUNTIME_FIX_V2_TESTS")
    op = acceptance.get("operator_evidence", {})
    check("accepted_godot_version", op.get("godot_version") == "4.7.1.stable.mono.official.a13da4feb")
    check("accepted_static_count", op.get("static_test_count") == 115)
    check("accepted_static_stdout", op.get("static_test_stdout_sha256") == EXPECTED_RUNTIME_STATIC_STDOUT)
    check("accepted_static_stderr", op.get("static_test_stderr_sha256") == EXPECTED_EMPTY)
    check("accepted_negative_count", op.get("runtime_negative_test_count") == 241)
    check("accepted_positive_count", op.get("runtime_positive_test_count") == 36)
    check("accepted_total_count", op.get("runtime_test_count") == 277)
    check("accepted_exit_code", op.get("runtime_exit_code") == 0)
    check("accepted_runtime_stdout", op.get("runtime_stdout_sha256") == EXPECTED_RUNTIME_STDOUT)
    check("accepted_runtime_stderr", op.get("runtime_stderr_sha256") == EXPECTED_EMPTY)
    check("accepted_receipt_sha", op.get("runtime_test_receipt_sha256") == EXPECTED_RUNTIME_RECEIPT)
    check("accepted_single_lookup", acceptance.get("observed_runtime_markers", {}).get("custom_data_lookups_per_frame") == 1)
    check("accepted_enumeration_forbidden", acceptance.get("observed_runtime_markers", {}).get("custom_data_enumeration") == "FORBIDDEN")
    check("accepted_production_calls_zero", acceptance.get("observed_runtime_markers", {}).get("production_calls") == 0)
    check("accepted_renderer_off", acceptance.get("observed_runtime_markers", {}).get("renderer") == "OFF")
    check("accepted_media_false", acceptance.get("observed_runtime_markers", {}).get("media_created") is False)
    check("acceptance_c11c_pin", acceptance.get("lineage", {}).get("frozen_c11c_manifest_sha256") == EXPECTED_C11C)

    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    check("contract_schema_id", contract.get("schema") == "C11D-V2B-ALLOWLISTED-COORDINATE-CONSUMER-SOURCE-COMPOSITION-CONTRACT-V1")
    check("contract_pending_before_operator_run", contract.get("status") == "PENDING_OPERATOR_SOURCE_RUNTIME_COMPOSITION_TEST")
    check("contract_c11c_pin", contract.get("source_authority", {}).get("frozen_c11c_manifest_sha256") == EXPECTED_C11C)
    check("contract_acceptance_record_sha", contract.get("source_authority", {}).get("runtime_acceptance_record_sha256") == EXPECTED_RUNTIME_ACCEPTANCE_RECORD_SHA)
    check("contract_receipt_sha", contract.get("source_authority", {}).get("runtime_acceptance_receipt_sha256") == EXPECTED_RUNTIME_RECEIPT)
    check("contract_static_runtime_out_sha", contract.get("source_authority", {}).get("runtime_acceptance_stdout_sha256") == EXPECTED_RUNTIME_STDOUT)
    check("contract_static_runtime_err_sha", contract.get("source_authority", {}).get("runtime_acceptance_stderr_sha256") == EXPECTED_EMPTY)
    check("contract_source_pin_denominator", contract.get("source_authority", {}).get("source_pin_count") == len(contract.get("source_authority", {}).get("source_pins", [])) == 81)
    check("contract_runtime_input_pin_denominator", contract.get("source_authority", {}).get("runtime_input_pin_count") == len(contract.get("source_authority", {}).get("runtime_input_pins", [])) == 6)
    check("contract_four_candidates", contract.get("composition", {}).get("candidate_count") == 4 and len(contract.get("composition", {}).get("candidates", [])) == 4)
    check("contract_real_runtime_entrypoint", contract.get("composition", {}).get("runtime_entrypoint") == "ChallengeRuntimeBridge.run_effective_pipeline(source_config)")
    check("contract_review_only_entrypoint", contract.get("composition", {}).get("consumer_entrypoint") == "project_allowlisted_target_marker_track(candidate_id, simulation_result, upstream_validation)")
    check("contract_test_only", contract.get("composition", {}).get("composition_invocation_scope") == "TEST_HARNESS_ONLY")
    check("contract_production_callsites_zero", contract.get("composition", {}).get("production_callsite_count") == 0)
    check("contract_420_frames_each", contract.get("composition", {}).get("expected_per_candidate_source_frames") == 420)
    check("contract_1680_total_frames", contract.get("composition", {}).get("expected_total_source_frames") == 1680)
    check("contract_1680_output_frames", contract.get("composition", {}).get("expected_total_marker_frames") == 1680)
    check("contract_no_synthetic_frames", contract.get("composition", {}).get("no_synthetic_frame_snapshots") is True)
    check("contract_no_field_arg", contract.get("composition", {}).get("no_alternate_candidate_field_argument") is True)
    check("contract_no_prod_adapter", contract.get("composition", {}).get("no_production_adapter_created") is True)
    policy = contract.get("input_policy", {})
    check("input_allowlist_exact", policy.get("allowlisted_pairs") == {k: v[2] for k, v in EXPECTED_CANDIDATES.items()})
    check("input_single_get", "exactly one Dictionary.get(allowlisted_field, unique_missing_sentinel)" in policy.get("custom_data_access", ""))
    check("input_no_enum", policy.get("enumeration") is False)
    check("input_no_has_then_get", policy.get("has_then_get") is False)
    check("input_no_indexing", policy.get("direct_indexing") is False)
    check("input_no_copy", policy.get("copy_duplicate") is False)
    check("input_no_serialization", policy.get("serialization") is False)
    check("harness_no_custom_data_reads", policy.get("harness_direct_custom_data_reads") == 0)
    check("harness_no_raw_values", policy.get("raw_values_in_logs") is False)
    output_policy = contract.get("output_policy", {})
    check("closed_root_keys", output_policy.get("root_keys") == ["contract_id", "candidate_id", "logical_canvas_id", "source_frame_count", "frames"])
    check("closed_frame_keys", output_policy.get("frame_keys") == ["source_frame_index", "target_marker"])
    check("closed_marker_keys", output_policy.get("marker_keys") == ["role", "asset_path", "anchor_x", "anchor_y", "logical_width", "logical_height", "anchor_mode", "asset_bounds_policy"])
    check("strict_closed_shape", output_policy.get("strict_closed_shape") is True)
    check("winning_frame_not_filter", output_policy.get("winning_frame_filtering") is False)
    check("whole_custom_data_forbidden", output_policy.get("whole_custom_data_serialization_allowed") is False)
    check("renderer_native_input_forbidden", output_policy.get("renderer_native_input") is False)
    locks = contract.get("governance_locks", {})
    check("lock_renderer_off", locks.get("renderer") == "OFF")
    check("lock_media_false", locks.get("media_created") is False)
    check("lock_payload_false", locks.get("payload_materialized") is False)
    check("lock_candidate_inadmissible", locks.get("candidate_input_admissible") is False)
    check("lock_release_none", locks.get("release_authority") == "NONE")
    check("lock_bindings_zero", locks.get("approved_bindings") == 0)
    check("lock_custom_bindings_zero", locks.get("approved_custom_data_bindings") == 0)
    check("lock_projection_bindings_zero", locks.get("approved_renderer_projection_bindings") == 0)
    check("lock_prod_implementation_false", locks.get("runtime_implementation_authorized_for_production") is False)
    check("lock_render_false", locks.get("render_test_authorized") is False)

    harness = harness_path.read_text(encoding="utf-8")
    consumer = consumer_path.read_text(encoding="utf-8")
    bridge = bridge_path.read_text(encoding="utf-8")
    for cid, (rel, expected_sha, expected_field) in EXPECTED_CANDIDATES.items():
        candidate_file = repo / rel
        check(cid.lower() + "_source_exists", candidate_file.is_file())
        check(cid.lower() + "_source_sha", candidate_file.is_file() and sha(candidate_file) == expected_sha)
        candidate = json.loads(candidate_file.read_text(encoding="utf-8"))
        check(cid.lower() + "_source_identity", candidate.get("challenge_id") == cid)
        check(cid.lower() + "_mechanic_identity", candidate.get("mechanic") == {"CHALLENGE_003":"pilot","CHALLENGE_005":"hit_v1","CHALLENGE_006":"catch_v1","CHALLENGE_007":"find_v1"}[cid])
        check(cid.lower() + "_source_field_pinned", contract["composition"]["candidates"][[c["candidate_id"] for c in contract["composition"]["candidates"]].index(cid)].get("candidate_field") == expected_field)
        check(cid.lower() + "_harness_has_path", rel in harness)

    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    check("schema_id", schema.get("$id") == "C11D-V2B-ALLOWLISTED-COORDINATE-CONSUMER-SOURCE-COMPOSITION-CONTRACT-V1")
    check("schema_additional_properties_false", schema.get("additionalProperties") is False)
    check("schema_requires_locks", "governance_locks" in schema.get("required", []))
    check("schema_four_candidate_const", schema.get("properties", {}).get("composition", {}).get("properties", {}).get("candidate_count", {}).get("const") == 4)
    check("schema_runtime_frames_const", schema.get("properties", {}).get("runtime_test_contract", {}).get("properties", {}).get("total_source_frames_expected", {}).get("const") == 1680)

    # Harness should compose real runtime output and should not itself inspect custom_data.
    for token in ["RuntimeBridge.run_effective_pipeline(source_config)", "simulation_result.validate_contract(expected_frames)", "weakref(simulation_result)", "project_allowlisted_target_marker_track(candidate_id, simulation_result, validation)", "_validate_closed_output(output, candidate_id, expected_frames)", "C11D_V2B_ALLOWLISTED_COORDINATE_CONSUMER_SOURCE_COMPOSITION_CANDIDATES=", "C11D_V2B_ALLOWLISTED_COORDINATE_CONSUMER_SOURCE_COMPOSITION_RUNTIME_TEST_STATUS=PASS"]:
        check("harness_token_" + token[:16], token in harness)
    check("harness_no_custom_data_member", ".custom_data" not in harness)
    check("harness_no_dictionary_serialization", "JSON.stringify" not in harness)
    check("harness_no_resource_loading", "ResourceLoader" not in harness and ".load(" not in harness)
    check("harness_no_rendering_server", "RenderingServer" not in harness)
    check("harness_no_file_writes", "FileAccess.WRITE" not in harness and "FileAccess.open" not in harness)
    check("harness_no_dispatch", "renderer_dispatch" not in harness.lower() and "dispatch_renderer" not in harness.lower())
    check("harness_4_real_rows", harness.count('"candidate_id":"CHALLENGE_') == 4)
    check("harness_pinned_timebase", "expected_frames != 420" in harness and "_total_source_frames == 1680" in harness)
    check("harness_closed_keys", "ROOT_KEYS" in harness and "FRAME_KEYS" in harness and "MARKER_KEYS" in harness)
    check("harness_constant_challenge005", 'candidate_id == "CHALLENGE_005" and not _validate_constant_track(output)' in harness)
    check("consumer_single_get", "frame_value.custom_data.get(field_name, missing_sentinel)" in consumer)
    check("consumer_no_enumeration", "custom_data.keys" not in consumer and "custom_data.values" not in consumer)
    check("consumer_no_has", "custom_data.has" not in consumer)
    check("consumer_no_direct_index", "custom_data[" not in consumer)
    check("consumer_no_duplicate", "custom_data.duplicate" not in consumer and "custom_data.duplicate(" not in consumer)
    check("consumer_no_serialize", "JSON.stringify" not in consumer and "var_to_bytes" not in consumer)
    check("consumer_review_only", "review-only consumer" in consumer and "no production call site" in consumer)
    check("bridge_effective_method_pinned", "static func run_effective_pipeline(legacy_config: Dictionary)" in bridge)
    check("bridge_no_renderer", "RenderingServer" not in bridge)

    failed = [name for name, passed in checks if not passed]
    print(f"C11D_V2B_ALLOWLISTED_COORDINATE_CONSUMER_SOURCE_COMPOSITION_STATIC_CHECKS={len(checks)-len(failed)}/{len(checks)}")
    print("C11D_V2B_ALLOWLISTED_COORDINATE_CONSUMER_SOURCE_COMPOSITION_STATIC_STATUS=" + ("PASS" if not failed else "FAIL"))
    print("C11D_V2B_ALLOWLISTED_COORDINATE_CONSUMER_SOURCE_COMPOSITION_ACCEPTED_V2_RECEIPT_PINNED=true")
    print("C11D_V2B_ALLOWLISTED_COORDINATE_CONSUMER_SOURCE_COMPOSITION_PRODUCTION_CALLS=0")
    print("C11D_V2B_ALLOWLISTED_COORDINATE_CONSUMER_SOURCE_COMPOSITION_RENDERER=OFF")
    print("C11D_V2B_ALLOWLISTED_COORDINATE_CONSUMER_SOURCE_COMPOSITION_MEDIA_CREATED=false")
    if failed:
        for name in failed:
            print("C11D_V2B_ALLOWLISTED_COORDINATE_CONSUMER_SOURCE_COMPOSITION_STATIC_FAILURE=" + name, file=sys.stderr)
        return 1
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
