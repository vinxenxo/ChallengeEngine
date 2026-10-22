#!/usr/bin/env python3
"""Review-only tests for the V2B allowlisted coordinate consumer implementation design.

This suite validates a design/negative-test contract only. It does not execute a consumer,
launch Godot, access the renderer, materialize payloads, or write files.
"""
from __future__ import annotations
import hashlib
import json
import math
import sys
from pathlib import Path

DESIGN_REL = Path("definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_ALLOWLISTED_COORDINATE_CONSUMER_IMPLEMENTATION_DESIGN_V1.json")
SCHEMA_REL = Path("definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_ALLOWLISTED_COORDINATE_CONSUMER_IMPLEMENTATION_DESIGN_SCHEMA_V1.json")
SPEC_REL = Path("definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_ALLOWLISTED_COORDINATE_PROJECTION_CONSUMER_SPECIFICATION_V1.json")
SPEC_SCHEMA_REL = Path("definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_ALLOWLISTED_COORDINATE_PROJECTION_CONSUMER_SPECIFICATION_SCHEMA_V1.json")
SPEC_TEST_REL = Path("tools/c11d/d9/test_d_renderer_challenge_visual_payload_v2b_allowlisted_coordinate_projection_consumer_specification_v1.py")
C11C_REL = Path("release/C11C_FREEZE_PACKAGE_MANIFEST.json")
COORD_POLICY_REL = Path("definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_CANDIDATE_COORDINATE_POLICY_DECISION_RECORD_V1.json")
COORD_MAPPER_REL = Path("core/presentation/CoordinateMapper.gd")
EXPECTED_SPEC_SHA = "be2a42e26fc22a25df378d234a358c4005610eefbcb02f6b70e2ee56f6625a52"
EXPECTED_SPEC_SCHEMA_SHA = "d8381ca133e4962d30e861e3e092eb1870909842d210b3ebf25ed702e14c3446"
EXPECTED_SPEC_TEST_SHA = "3e155960c8c6862ecc29ab28f8e4dccc9f115219734f21bc6a18262676e336ab"
EXPECTED_C11C_SHA = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
EXPECTED_COORD_POLICY_SHA = "45841adf320c4815b1a63b26555497adf38b57672bd62069c81385ef327e6a1e"
EXPECTED_COORD_MAPPER_SHA = "244bace2eaf87e29d653715ae18c0b4824cdf9503e915932be53d0f52bbe461c"
EXPECTED_RECEIPT_SHA = "c52d3f5ca276beea0482eb1ab521d163e201023f818e9448f6f7279c306b2ef0"
EXPECTED_RECEIPT_STDOUT_SHA = "c5daea5a270aec81d76aa1c5b1499f8826d1d09e9047b3ad7ae0a7941dfc3682"
EMPTY_SHA = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"

class Checker:
    def __init__(self):
        self.count = 0
        self.failures = []
    def check(self, condition, label):
        self.count += 1
        if not condition:
            self.failures.append(label)
    def same(self, actual, expected, label):
        self.check(actual == expected, f"{label}: expected {expected!r}, got {actual!r}")
    def exact_keys(self, obj, expected, label):
        self.check(isinstance(obj, dict) and set(obj) == set(expected), f"{label}: keyset mismatch")

def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main() -> int:
    if len(sys.argv) != 3:
        print("USAGE: test_d_renderer_challenge_visual_payload_v2b_allowlisted_coordinate_consumer_implementation_design_v1.py REPO_ROOT SPEC_TEST_RECEIPT", file=sys.stderr)
        return 2
    root = Path(sys.argv[1]).resolve()
    receipt_path = Path(sys.argv[2]).resolve()
    g = Checker()

    design_path = root / DESIGN_REL
    schema_path = root / SCHEMA_REL
    spec_path = root / SPEC_REL
    spec_schema_path = root / SPEC_SCHEMA_REL
    spec_test_path = root / SPEC_TEST_REL
    c11c_path = root / C11C_REL
    coord_policy_path = root / COORD_POLICY_REL
    coord_mapper_path = root / COORD_MAPPER_REL

    missing = [str(p) for p in [design_path,schema_path,spec_path,spec_schema_path,spec_test_path,c11c_path,coord_policy_path,coord_mapper_path,receipt_path] if not p.is_file()]
    if missing:
        print("MISSING_REQUIRED_INPUTS=" + "|".join(missing), file=sys.stderr)
        return 2

    D = json.loads(design_path.read_text(encoding="utf-8"))
    S = json.loads(schema_path.read_text(encoding="utf-8"))
    SPEC = json.loads(spec_path.read_text(encoding="utf-8"))
    R = json.loads(receipt_path.read_text(encoding="utf-8"))

    # Immutable file and predecessor receipt pins.
    for path, expected, label in [
        (spec_path,EXPECTED_SPEC_SHA,"accepted consumer specification SHA"),
        (spec_schema_path,EXPECTED_SPEC_SCHEMA_SHA,"accepted consumer schema SHA"),
        (spec_test_path,EXPECTED_SPEC_TEST_SHA,"accepted consumer suite SHA"),
        (c11c_path,EXPECTED_C11C_SHA,"frozen C11-C manifest SHA"),
        (coord_policy_path,EXPECTED_COORD_POLICY_SHA,"coordinate decision record SHA"),
        (coord_mapper_path,EXPECTED_COORD_MAPPER_SHA,"CoordinateMapper reference SHA")]:
        g.same(digest(path), expected, label)

    g.same(digest(receipt_path), EXPECTED_RECEIPT_SHA, "accepted specification test receipt SHA")
    g.same(R.get("status"), "PASS_STATIC_TESTS", "accepted specification receipt status")
    g.same(R.get("test_count"), 1038, "accepted specification receipt test count")
    g.same(R.get("specification_sha256"), EXPECTED_SPEC_SHA, "receipt specification SHA")
    g.same(R.get("specification_schema_sha256"), EXPECTED_SPEC_SCHEMA_SHA, "receipt schema SHA")
    g.same(R.get("test_script_sha256"), EXPECTED_SPEC_TEST_SHA, "receipt test script SHA")
    g.same(R.get("stdout_sha256"), EXPECTED_RECEIPT_STDOUT_SHA, "receipt stdout SHA")
    g.same(R.get("stderr_sha256"), EMPTY_SHA, "receipt stderr SHA")
    g.same(R.get("frozen_manifest_sha256"), EXPECTED_C11C_SHA, "receipt frozen manifest SHA")
    g.same(R.get("renderer"), "OFF", "receipt renderer lock")
    g.same(R.get("render_test_authorized"), False, "receipt render test lock")
    g.same(R.get("binding_authorization"), "NOT_GRANTED", "receipt binding lock")
    g.same(R.get("renderer_projection_authorization"), "NOT_GRANTED", "receipt projection lock")
    g.same(R.get("candidate_input_admissible"), False, "receipt candidate admissibility lock")

    # Closed top-level schema and matching design object keyset.
    g.same(S.get("schema"), "C11D-V2B-ALLOWLISTED-COORDINATE-CONSUMER-IMPLEMENTATION-DESIGN-SCHEMA-V1", "schema ID")
    g.same(S.get("type"), "object", "schema top-level type")
    g.same(S.get("additionalProperties"), False, "schema forbids extra top-level properties")
    g.same(set(S.get("required", [])), set(S.get("properties", {}).keys()), "schema requires every declared top-level key")
    g.same(set(D.keys()), set(S.get("properties", {}).keys()), "design exact top-level keyset")
    for key, prop in S.get("properties", {}).items():
        expected_type = "object" if isinstance(D.get(key), dict) else "array" if isinstance(D.get(key), list) else "boolean" if isinstance(D.get(key), bool) else "integer" if isinstance(D.get(key), int) else "number" if isinstance(D.get(key), float) else "string" if isinstance(D.get(key), str) else "null"
        g.same(prop.get("type"), expected_type, "schema type " + key)

    # Design identity and the no-runtime/no-render boundary.
    g.same(D.get("schema"), "C11D-V2B-ALLOWLISTED-COORDINATE-CONSUMER-IMPLEMENTATION-DESIGN-V1", "design schema ID")
    g.same(D.get("schema_version"), "1.0", "design schema version")
    g.same(D.get("status"), "REVIEW_ONLY_DESIGN_PENDING_IMPLEMENTATION", "design status")
    g.same(D.get("decision_scope"), "IMPLEMENTATION_DESIGN_AND_NEGATIVE_TEST_CONTRACT_ONLY_NO_RUNTIME_AUTHORIZATION", "design decision scope")
    boundary = D["implementation_boundary"]
    for k in ["production_consumer_code_included","runtime_execution_included","renderer_dispatch_reachable","renderer_native_input_emitted","payload_materialized","media_created","challenge_json_modification_allowed","coordinate_mapper_modification_allowed","simulation_or_rng_mutation_allowed","whole_custom_data_serialization_allowed"]:
        g.same(D["scope"].get(k), False, "scope lock " + k)
    g.same(boundary.get("production_consumer_code_included"), False, "no production consumer code included")
    g.same(boundary.get("planned_module"), "isolated review-only GDScript RefCounted helper, not in production call graph", "planned isolated module")
    g.same(boundary.get("no_scene_or_render_nodes"), True, "no scene/render nodes")
    g.same(boundary.get("rendering_server_access"), False, "RenderingServer forbidden")
    g.same(boundary.get("resource_loading"), False, "resource loading forbidden")
    g.same(boundary.get("no_production_wiring"), True, "production call graph unchanged")
    g.same(boundary.get("no_preview_or_delivery_scale"), True, "delivery scale not applied")
    g.same(boundary.get("no_raster_rounding_or_crop_policy"), True, "pixel policy remains blocked")
    g.same(D.get("next_gate"), "ISOLATED_REVIEW_ONLY_CONSUMER_IMPLEMENTATION_AND_NEGATIVE_RUNTIME_TESTS_NO_RENDERER_ACTIVATION", "next gate")

    # Candidate pairings are exact and bound to the accepted spec.
    pairs = D["scope"]["accepted_candidate_field_pairs"]
    spec_pairs = [{"candidate_id": c["candidate_id"], "field": c["field"]} for c in SPEC["field_allowlist"]]
    g.same(pairs, spec_pairs, "accepted candidate-field pairs match source specification")
    g.same(D["scope"]["accepted_candidate_count"], 4, "accepted candidate count")
    g.same(D["scope"]["blocked_candidate_count"], 2, "blocked candidate count")
    g.same(D["scope"]["blocked_candidate_field_pairs"], [{"candidate_id":"CHALLENGE_008","field":"active_selection"},{"candidate_id":"CHALLENGE_009","field":"displayed_count"}], "blocked candidate-field pairs retained")
    handlers = D["candidate_handlers"]
    g.same(len(handlers), 4, "handler count")
    g.same([h["candidate_id"] for h in handlers], ["CHALLENGE_003","CHALLENGE_005","CHALLENGE_006","CHALLENGE_007"], "handler order and IDs")
    for handler, c in zip(handlers, SPEC["field_allowlist"]):
        for key in ["candidate_id","field","semantic_type","track_kind","source_space","source_domain","projection","asset_path","asset_role","track_constraints"]:
            g.same(handler.get(key), c.get(key), handler["candidate_id"] + " source specification " + key)
        g.same(handler.get("field"), {"CHALLENGE_003":"target_x","CHALLENGE_005":"target_position","CHALLENGE_006":"target_position","CHALLENGE_007":"target_position"}[handler["candidate_id"]], "no alternate field for " + handler["candidate_id"])

    # Input contract, single lookup and no leak rules.
    input_contract = D["input_contract"]
    g.same(input_contract["candidate_id"]["rule"], "exact, case-sensitive candidate ID; no aliases, trimming, numeric coercion, or inference from frame data", "candidate ID strictness")
    g.same(input_contract["simulation_result"]["type"], "SimulationResult", "input SimulationResult type")
    g.same(input_contract["upstream_validation"]["required"], {"is_valid":True,"error_code":"OK"}, "upstream validation result contract")
    g.same(input_contract["frame_index_source"], "zero-based local array ordinal i; do not read a snapshot frame_index field", "frame ordinal source")
    g.same(input_contract["custom_data_access"], "exactly one Dictionary.get(allowlisted_key, unique_missing_sentinel) per source frame; never pair has() with a second index/get read", "exactly one field access")
    g.same(input_contract["no_enumeration_or_copy"], "do not enumerate, duplicate, merge, stringify, log, hash, or serialize custom_data or any full snapshot object", "no custom_data enumeration or copy")
    g.same(input_contract["empty_frames"], "reject before output allocation", "empty frames fail before output")
    g.same(input_contract["atomicity"], "all frames validate before a success track is returned; any invalid sample discards all local partial frame entries and returns only a safe error envelope", "atomic fail-closed")
    g.same(D["implementation_boundary"]["output_lifetime"], "in-memory return value only; no JSON serialization, file writes, logs containing inputs, payload store, or renderer handoff", "ephemeral return")

    # Coordinate math is identical to the accepted source contract; boundaries are inclusive.
    coord = D["coordinate_contract"]
    g.same(coord["output_space"], SPEC["coordinate_mapping_contract"]["output_space"], "output logical space")
    g.same(coord["logical_canvas"], SPEC["coordinate_mapping_contract"]["logical_canvas"], "logical canvas")
    g.same(coord["vector_candidates"]["candidate_ids"], ["CHALLENGE_005","CHALLENGE_006","CHALLENGE_007"], "vector candidate IDs")
    g.same(coord["vector_candidates"]["x"], "source.x * 0.5", "vector X transform")
    g.same(coord["vector_candidates"]["y"], "source.y * 0.5", "vector Y transform")
    g.same(coord["vector_candidates"]["rounding"], "NONE", "no rounding")
    g.same(coord["vector_candidates"]["clamp"], "NONE", "no clamp")
    g.same(coord["vector_candidates"]["y_inversion"], False, "no Y inversion")
    g.same(coord["pilot_candidate"], {"candidate_id":"CHALLENGE_003","x":"(target_x / 100.0) * 540.0","y":480.0,"y_semantics":"PRESENTATION_CENTERLINE_DEFAULT_NOT_SOURCE_DATA"}, "pilot scalar transform")
    g.same(coord["asset"]["intrinsic_size"], [100.0,100.0], "pinned intrinsic asset size")
    g.same(coord["asset"]["logical_size"], [50.0,50.0], "logical asset size")
    g.same(coord["asset"]["anchor"], "CENTER", "asset center anchor")
    g.same(coord["asset"]["edge_policy"], "CLIP_BOUNDS_WITHOUT_MOVING_POINT", "edge doesn't move target point")
    g.same(coord["delivery_profile"], "REVIEW_720 is reference-only; this consumer must not apply delivery scaling", "REVIEW_720 reference-only")
    g.same(coord["source_timeline"], "one sample per existing source frame; no interpolation, extrapolation, resampling, duplication, winning_frame remapping, or temporal smoothing", "source timeline unchanged")

    # Output schema remains closed and exactly matches the accepted specification.
    out = D["success_output_contract"]
    for k,v in SPEC["output_contract"].items(): g.same(out.get(k),v,"output contract source parity " + k)
    g.same(out["root_additional_fields_allowed"], False, "root fields closed")
    g.same(out["frame_additional_fields_allowed"], False, "frame fields closed")
    g.same(out["marker_additional_fields_allowed"], False, "marker fields closed")
    g.same(out["raw_source_value_in_output"], False, "raw source value excluded")
    g.same(out["custom_data_in_output"], False, "custom_data excluded")
    g.same(out["score_or_close_calls_in_output"], False, "scores/close calls excluded")

    # Ordered fail-closed pipeline and stable error vocabulary.
    pipeline = D["validation_pipeline"]
    g.same([x["step"] for x in pipeline], list(range(1,15)), "pipeline step sequence")
    g.same([x["name"] for x in pipeline], ["projection_stage_gate","candidate_id_gate","candidate_field_pair_gate","upstream_contract_gate","source_frame_gate","asset_contract_gate","single_key_extraction","strict_type_gate","finite_value_gate","inclusive_domain_gate","per_run_invariant_gate","ordered_projection","closed_output_check","atomic_return"], "pipeline operation ordering")
    g.same(pipeline[6]["rule"], input_contract["custom_data_access"], "single-key extraction rule is consistent")
    g.same(D["failure_contract"]["success_track_on_failure"], False, "no success track on failure")
    g.same(D["failure_contract"]["partial_track_on_failure"], False, "no partial track on failure")
    g.same(D["failure_contract"]["input_values_in_error"], False, "no input values in errors")
    spec_failure_codes = SPEC["safe_failure_codes"]
    design_failure_codes = [x["code"] for x in D["failure_contract"]["failure_codes"]]
    g.same(design_failure_codes, spec_failure_codes, "safe failure code vocabulary matches specification")

    # Negative test contract denominators, uniqueness, and exact coverage declarations.
    nt = D["negative_test_contract"]
    g.same(nt["status"], "PLANNED_NOT_EXECUTED_AGAINST_IMPLEMENTATION", "negative matrix is planned only")
    g.same(nt["planned_negative_case_count"], 261, "negative case denominator")
    families = nt["negative_families"]
    g.same(sum(int(x["planned_cases"]) for x in families), nt["planned_negative_case_count"], "negative family sum")
    g.same([x["id"] for x in families], ["wrong_candidate_field_pair","unsupported_candidate_ids","missing_allowlisted_field","invalid_scalar_values","invalid_vector_values","invalid_upstream_validation","empty_source_frames","atomic_failure_position","challenge_005_constant_violation","closed_output_and_no_leakage"], "negative families are complete and ordered")
    g.same(len({x["id"] for x in families}), len(families), "negative family IDs are unique")
    for family in families:
        g.check(int(family["planned_cases"]) > 0, "positive negative-family denominator " + family["id"])
        g.check(bool(family.get("expected_code") or family.get("expected_codes") or family.get("test_oracle")), "expected failure/test oracle exists " + family["id"])
        g.same(family.get("atomic_output"), "NO_TRACK" if family["id"] not in ("atomic_failure_position","closed_output_and_no_leakage") else ("NO_PARTIAL_TRACK" if family["id"] == "atomic_failure_position" else "ASSERT_EXACT_OUTPUT_KEYS_AND_ZERO_SOURCE_LEAKAGE"), "atomic/output policy " + family["id"])
    g.same(nt["case_generation_is_deterministic"], True, "negative test generation deterministic")
    g.same(nt["invalid_frame_positions"], ["FIRST","MIDDLE","LAST"], "negative cases target frame positions")
    g.same(nt["atomicity_oracle"], "every invalid track returns no projected track and never exposes an accepted prefix", "atomicity oracle")
    required_coverage = [
      "all 4 accepted candidate-field pairs",
      "all 12 wrong cross-pairings among the accepted candidates and their fields",
      "all 7 unsupported candidate IDs",
      "scalar invalid classes at first/middle/last frame",
      "vector invalid classes for every vector candidate at first/middle/last frame",
      "missing source key at first/middle/last frame",
      "upstream validation missing/mismatch/failure variants",
      "zero source frames for every supported candidate",
      "atomic failure for every candidate and frame position",
      "CHALLENGE_005 run-constant violation at multiple positions",
      "closed output and forbidden data leakage mutation tests"]
    g.same(nt["coverage_requirements"], required_coverage, "required negative coverage list")
    g.same(D["positive_test_contract"]["execution_status"], "NOT_EXECUTED; implementation is not included", "positive tests not falsely reported executed")
    g.check(len(D["positive_test_contract"]["planned_positive_families"]) >= 8, "positive design checks cover all major contract classes")

    # Governance locks and immutable source statements.
    locks = D["governance_locks"]
    expected_locks = {
      "renderer":"OFF","media_created":False,"payload_materialized":False,"candidate_input_admissible":False,
      "seed_domains_complete_for_candidate_input":False,"automatic_seed_generation":False,"master_seed":"NOT_ADOPTED",
      "approved_bindings":0,"approved_custom_data_bindings":0,"approved_renderer_projection_bindings":0,
      "D4.8":"BLOCKED","D9.10":"PREPARE_ONLY","D9.14":"BLOCKED","D9.16":"BLOCKED","D9.17":"BLOCKED_NO_GO",
      "D10":"BLOCKED_FOR_PROMOTION","baseline_approval":"MISSING","freeze_eligible":False,"release_authority":"NONE",
      "whole_custom_data_serialization_allowed":False,"challenge_json_modification_allowed":False,"challenge_004_v1_harness_mutation_allowed":False,
      "runtime_implementation_authorized_for_production":False,"runtime_coordinate_transform_authorized":False,
      "render_test_authorized":False,"payload_output_is_renderer_native_input":False}
    g.same(locks, expected_locks, "all governance locks remain unchanged")
    g.same(D["source_authority"]["frozen_c11c_manifest_sha256"], EXPECTED_C11C_SHA, "source authority C11-C hash")
    g.same(D["source_authority"]["consumer_specification_test_receipt_sha256"], EXPECTED_RECEIPT_SHA, "spec receipt source pin")
    g.same(D["scope"]["accepted_candidate_field_pairs"], spec_pairs, "exact candidate allowlist repeated consistently")

    # No runtime code is embedded in this contract artifact.
    forbidden_design_claims = [
      D["scope"].get("production_consumer_code_included") is True,
      D["scope"].get("runtime_execution_included") is True,
      D["scope"].get("renderer_dispatch_reachable") is True,
      D["scope"].get("renderer_native_input_emitted") is True,
      D["governance_locks"].get("runtime_implementation_authorized_for_production") is True,
      D["governance_locks"].get("render_test_authorized") is True]
    for i,value in enumerate(forbidden_design_claims): g.same(value,False,"forbidden authorization claim " + str(i))

    # Check all JSON-design identifiers are strings and avoid accidental permissive wildcard/alias rules.
    g.same(len(D["candidate_handlers"]), 4, "exactly four handlers")
    for cid in ["CHALLENGE_003","CHALLENGE_005","CHALLENGE_006","CHALLENGE_007"]:
        matches = [h for h in D["candidate_handlers"] if h["candidate_id"] == cid]
        g.same(len(matches),1,"unique handler " + cid)
        g.check(isinstance(matches[0]["field"],str) and matches[0]["field"] != "*", "field is explicit " + cid)
        g.same(matches[0]["asset_role"],"TARGET","target role " + cid)
    for cid in ["CHALLENGE_001","CHALLENGE_002","CHALLENGE_004","CHALLENGE_008","CHALLENGE_009"]:
        g.check(cid not in [h["candidate_id"] for h in D["candidate_handlers"]], "no handler for blocked/unsupported " + cid)

    # A stable expected count prevents accidental thinning of this static design suite.
    expected_count = int(D["negative_test_contract"].get("static_design_test_expected", 0))
    if expected_count:
        g.check(g.count + 1 == expected_count, "fixed static design suite denominator")
    if g.failures:
        print("C11D_V2B_ALLOWLISTED_COORDINATE_CONSUMER_IMPLEMENTATION_DESIGN_TEST_FAILURES=" + str(len(g.failures)))
        for item in g.failures[:100]: print("FAIL | " + item)
        print("C11D_V2B_ALLOWLISTED_COORDINATE_CONSUMER_IMPLEMENTATION_DESIGN_TESTS=" + str(g.count) + "/" + str(expected_count or g.count))
        return 1
    print("C11D_V2B_ALLOWLISTED_COORDINATE_CONSUMER_IMPLEMENTATION_DESIGN_TESTS=" + str(g.count) + "/" + str(expected_count or g.count))
    print("C11D_V2B_ALLOWLISTED_COORDINATE_CONSUMER_IMPLEMENTATION_DESIGN_NEGATIVE_CASES=261/261_PLANNED")
    print("C11D_V2B_ALLOWLISTED_COORDINATE_CONSUMER_IMPLEMENTATION_DESIGN_CANDIDATES=4/4")
    print("C11D_V2B_ALLOWLISTED_COORDINATE_CONSUMER_IMPLEMENTATION_DESIGN_SOURCE_SPEC=PINNED")
    print("C11D_V2B_ALLOWLISTED_COORDINATE_CONSUMER_IMPLEMENTATION_DESIGN_CUSTOM_DATA_ENUMERATION=FORBIDDEN")
    print("C11D_V2B_ALLOWLISTED_COORDINATE_CONSUMER_IMPLEMENTATION_DESIGN_RUNTIME_IMPLEMENTATION=NOT_INCLUDED")
    print("C11D_V2B_ALLOWLISTED_COORDINATE_CONSUMER_IMPLEMENTATION_DESIGN_RENDERER=OFF")
    print("C11D_V2B_ALLOWLISTED_COORDINATE_CONSUMER_IMPLEMENTATION_DESIGN_RENDER_TEST_AUTHORIZATION=NOT_GRANTED")
    print("C11D_V2B_ALLOWLISTED_COORDINATE_CONSUMER_IMPLEMENTATION_DESIGN_C11C_IMMUTABLE=true")
    print("C11D_V2B_ALLOWLISTED_COORDINATE_CONSUMER_IMPLEMENTATION_DESIGN_REPOSITORY_WRITES=0")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
