import hashlib
import json
import re
import sys
import unittest
from pathlib import Path, PurePosixPath
from collections.abc import Mapping

ROOT = Path(sys.argv[1]).resolve()
GODOT = Path(sys.argv[2]).resolve()

HERE = ROOT / "tools" / "c11d" / "d9"
sys.path.insert(0, str(HERE))

import d_renderer_request_scoped_payload_materialization_binding as materializer
import d_renderer_editorial_field_consumption_audit as consumption_audit

MANIFEST = "release/C11C_FREEZE_PACKAGE_MANIFEST.json"
DOCKET = "definitions/c11d/production/D_RENDERER_POLICY_DECISION_DOCKET_V1.json"
EXPECTED_MANIFEST_SHA = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
EXPECTED_DOCKET_SHA = "e008217bd57303b638e13329d21e5ae56ee3b4efef790566e3702c89ee41a83f"

FIXED_HASHES = {
    "tools/c11d/d9/d_renderer_request_scoped_payload_materialization_binding.py":
        "244426e8f742e221f1fbb6885103135bd01d202cb6c8b641f877bd089e81ab9d",
    "tools/c11d/d9/d_renderer_request_scoped_payload_binding.py":
        "3b3ced5f51309fff791a166109baebd37511b354b1704ae2e59a0b9aa4e6df8b",
    "tools/c11d/d9/d_renderer_editorial_field_consumption_audit.py":
        "7001098cec9239027784abfc20ed17024f5bb45993b20f308e1debfb7fd5b85a",
    "tools/c11d/d9/materialize_visual_payloads_in_memory.gd":
        "33c63c2f692ddf64a37d3e64a7be219c96df048059dcfded848ae9f3dada29a8",
    "tools/c11d/d9/materialize_challenge_visual_payload_in_memory.gd":
        "8f8e4c9be6170d48319b62512a1e1cdb40c4f126563deb3546dfd302b080179e",
    "definitions/c11d/production/D_RENDERER_EDITORIAL_REVIEW_MANIFEST_V1.json":
        "2075da9c33c689861a68d3bd8fb19b7ed593c6e76010ab200880746aa6d1a470",
    "definitions/c11d/production/D_RENDERER_CHALLENGE_TEMPORAL_ALIGNMENT_POLICY_PROPOSAL_V1.json":
        "39f6f979a5d8b189cbb3a375b0c33ed7fdb3f2b9bc59fcb587f31a6c65ede5a6",
    "definitions/c11d/production/D_RENDERER_EDITORIAL_FIELD_WINDOW_PROPOSAL_V1.json":
        "4bb817b3d782b4f7c61d93a48df9c11766c78018b6c9e7ea43155cb96bda5229",
    "definitions/c11d/production/D_RENDERER_UNIFIED_DELIVERY_TIMEBASE_POLICY_PROPOSAL_V1.json":
        "41a62b0766db47cd99772f28642ef67766314f20f0f7891789d6b7497bbfee85",
    "definitions/c11d/production/D_RENDERER_UNIVERSAL_EDITORIAL_FIELD_VISIBILITY_POLICY_PROPOSAL_V1.json":
        "8ccbb98f63f6e6041cf047ccff8cda2c0b4c4e1c7cb772017f7cb2851a0d99fe",
}

EXPECTED_FIELDS = {
    "challenges": {"title", "subtitle", "call_to_action", "player_name", "challenge_label", "language"},
    "visual_loops": {"title", "subtitle", "call_to_action", "language"},
    "visual_drills": {"title", "subtitle", "call_to_action", "language"},
}


def sha256_file(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(relative):
    path = ROOT.joinpath(*PurePosixPath(relative).parts)
    if not path.is_file():
        raise FileNotFoundError("Missing required source: " + relative)
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def verify_source_pins():
    if sha256_file(ROOT / MANIFEST) != EXPECTED_MANIFEST_SHA:
        raise RuntimeError("Frozen C11-C manifest SHA-256 mismatch")

    docket_path = ROOT / DOCKET
    if sha256_file(docket_path) != EXPECTED_DOCKET_SHA:
        raise RuntimeError("Decision docket SHA-256 mismatch")

    docket = read_json(DOCKET)
    pins = docket.get("source_pins", [])
    if docket.get("source_pin_count") != 198 or len(pins) != 198:
        raise RuntimeError("Decision docket must declare exactly 198 source pins")

    seen = set()
    for pin in pins:
        relative = pin.get("path")
        if not isinstance(relative, str) or not relative:
            raise RuntimeError("Source pin path missing")
        pure = PurePosixPath(relative)
        if pure.is_absolute() or ".." in pure.parts:
            raise RuntimeError("Unsafe source pin path: " + relative)
        if relative in seen:
            raise RuntimeError("Duplicate source pin: " + relative)
        seen.add(relative)

        source = ROOT.joinpath(*pure.parts)
        if not source.is_file():
            raise RuntimeError("Pinned source missing: " + relative)
        if sha256_file(source) != pin.get("sha256"):
            raise RuntimeError("Pinned source SHA-256 mismatch: " + relative)
        if source.stat().st_size != pin.get("bytes"):
            raise RuntimeError("Pinned source byte count mismatch: " + relative)

    for relative, expected in FIXED_HASHES.items():
        source = ROOT.joinpath(*PurePosixPath(relative).parts)
        if not source.is_file() or sha256_file(source) != expected:
            raise RuntimeError("Fixed runtime source pin mismatch: " + relative)

    return docket


JOIN_CONTRACT_REL = "definitions/c11d/production/D_RENDERER_EDITORIAL_PAYLOAD_PROVENANCE_JOIN_CONTRACT_V2.json"
JOIN_SCHEMA_REL = "definitions/c11d/production/D_RENDERER_EDITORIAL_PAYLOAD_PROVENANCE_JOIN_SCHEMA_V2.json"

JOIN_EXTRA_FIXED_HASHES = {
    "tools/c11d/d9/d_renderer_visual_payload_materialization_preview.py":
        "cebe9b79c519675e61aa0d136ec08814e38eef91d3f55d19e9355929d677bfee",
    "definitions/c11d/production/D_RENDERER_LOOP_DRILL_EDITORIAL_FIELD_WINDOW_PROPOSAL_V1.json":
        "609a4d183aac07c2cbe1abaf41444160fdd137217faffbead3aef618320d57dc",
    "definitions/c11d/production/D_RENDERER_UNIFIED_PRESENTATION_REGION_POLICY_PROPOSAL_V1.json":
        "101092bb32127bb8854a501a9215c0b6cf69581594383903716907d49719c01a",
    "definitions/c11d/production/D_RENDERER_CHALLENGE_SIMULATION_SAMPLE_SELECTION_PROPOSAL_V1.json":
        "dbd12b8e71f55223b29a479c93c7b4565b2fee3dfe0da54816900cf6da10d33b",
}

EXPECTED_JOIN_OBSERVATIONS = {
    "challenges": {
        "request_id": "D-PAYLOAD-BIND-CHALLENGES",
        "payload_instance_id": "D-CHALLENGE-CHALLENGE_004-7fe2bcf47b7127ee",
        "payload_instance_sha256": "7fe2bcf47b7127ee44c6c9d3a9aeea5bf54fb78ca28ca09757a99058e86b4809",
        "payload_identity_quality": "DERIVED_RECEIPT_ALIAS_NOT_NATIVE_RUNTIME_INSTANCE_ID",
        "observed_source_frame_count": 900,
        "observed_source_fps": 60,
        "observed_source_duration_seconds": 15.0,
        "challenge_game_frame_count": 420,
    },
    "visual_loops": {
        "request_id": "D-PAYLOAD-BIND-VISUAL_LOOPS",
        "payload_instance_id": "D-VLP-5ac67e64ff717d97",
        "payload_instance_sha256": "5ac67e64ff717d9756b37152dd1ee1ff81a1b0e754f83c06a618964c9a62e090",
        "payload_identity_quality": "MATERIALIZER_INSTANCE_ID_AND_SHA256",
        "observed_source_frame_count": 600,
        "observed_source_fps": 30,
        "observed_source_duration_seconds": 20.0,
        "challenge_game_frame_count": None,
    },
    "visual_drills": {
        "request_id": "D-PAYLOAD-BIND-VISUAL_DRILLS",
        "payload_instance_id": "D-VDP-1a96afdd7a0d950e",
        "payload_instance_sha256": "1a96afdd7a0d950ef3eabb5531fe13496b4206a7d4fd1d7f233892b0329a592b",
        "payload_identity_quality": "MATERIALIZER_INSTANCE_ID_AND_SHA256",
        "observed_source_frame_count": 630,
        "observed_source_fps": 30,
        "observed_source_duration_seconds": 21.0,
        "challenge_game_frame_count": None,
    },
}


def validate_join_contract(contract):
    errors = []

    if contract.get("schema") != "C11-D-D9-RENDERER-EDITORIAL-PAYLOAD-PROVENANCE-JOIN-CONTRACT-V2":
        errors.append("contract schema ID mismatch")
    if contract.get("schema_version") != "1.0":
        errors.append("contract version mismatch")
    if contract.get("status") != "PREPARATION_ONLY_IN_MEMORY_PROVENANCE_JOIN_NOT_RENDERER_INPUT":
        errors.append("contract status is not preparation-only")

    expected_pins = {
        MANIFEST: EXPECTED_MANIFEST_SHA,
        DOCKET: EXPECTED_DOCKET_SHA,
        **FIXED_HASHES,
        **JOIN_EXTRA_FIXED_HASHES,
    }
    pins = contract.get("source_pins")
    if not isinstance(pins, list) or contract.get("source_pin_count") != len(pins):
        errors.append("contract source pin count mismatch")
        pins = pins if isinstance(pins, list) else []

    pin_map = {}
    for pin in pins:
        if not isinstance(pin, dict):
            errors.append("source pin entry is not an object")
            continue
        path = pin.get("path")
        sha = pin.get("sha256")
        size = pin.get("bytes")
        if not isinstance(path, str) or not path:
            errors.append("source pin path missing")
            continue
        if path in pin_map:
            errors.append("duplicate source pin: " + path)
        pin_map[path] = sha
        if not isinstance(sha, str) or not re.fullmatch(r"[0-9a-f]{64}", sha):
            errors.append("malformed source SHA-256: " + path)
        if not isinstance(size, int) or size < 1:
            errors.append("invalid source byte count: " + path)

    if pin_map != expected_pins:
        errors.append("contract source path/hash inventory differs from fixed expected inventory")

    for pin in pins:
        if not isinstance(pin, dict) or not isinstance(pin.get("path"), str):
            continue
        relative = pin["path"]
        pure = PurePosixPath(relative)
        if pure.is_absolute() or ".." in pure.parts:
            errors.append("unsafe source path: " + relative)
            continue
        source = ROOT.joinpath(*pure.parts)
        if not source.is_file():
            errors.append("pinned source missing: " + relative)
            continue
        if sha256_file(source) != pin.get("sha256"):
            errors.append("pinned source SHA-256 differs: " + relative)
        if source.stat().st_size != pin.get("bytes"):
            errors.append("pinned source byte count differs: " + relative)

    cardinality = contract.get("editorial_field_cardinality", {})
    if cardinality != {
        "challenges": 6,
        "visual_loops": 4,
        "visual_drills": 4,
        "total": 14,
        "nonempty_visual_fields_in_pinned_fixture": 11,
        "language_metadata_fields": 3,
    }:
        errors.append("editorial field cardinality mismatch")

    observations = contract.get("expected_payload_observations")
    if not isinstance(observations, list) or len(observations) != 3:
        errors.append("expected payload observation matrix must have three rows")
        observations = observations if isinstance(observations, list) else []

    by_type = {
        row.get("content_type"): row
        for row in observations if isinstance(row, dict)
    }
    if set(by_type) != set(EXPECTED_JOIN_OBSERVATIONS):
        errors.append("expected payload content-type inventory mismatch")

    for content_type, expected in EXPECTED_JOIN_OBSERVATIONS.items():
        row = by_type.get(content_type)
        if not isinstance(row, dict):
            continue
        for key, value in expected.items():
            if row.get(key) != value:
                errors.append(f"contract observation mismatch: {content_type}.{key}")
        if row.get("effective_delivery_frame_count") is not None:
            errors.append(f"contract must not establish delivery frame count: {content_type}")
        if row.get("delivery_frame_count_status") != "NOT_ESTABLISHED_TIMEBASE_POLICY_NOT_APPROVED":
            errors.append(f"contract timebase state mismatch: {content_type}")
        if row.get("visibility_window_status") != "NOT_EVALUATED":
            errors.append(f"contract unexpectedly evaluates a visibility window: {content_type}")
        if row.get("editorial_payload_consumption") != "NOT_CONSUMED_BY_CURRENT_IN_MEMORY_VISUAL_PAYLOAD_HARNESS":
            errors.append(f"contract overclaims visual consumption: {content_type}")

    phase = contract.get("challenge_phase_namespace", {})
    if phase.get("field_ids") != ["hook", "reveal", "cta"]:
        errors.append("Challenge phase field names differ from the pinned proposal")
    if phase.get("distinct_from_universal_D9_9_fields") is not True:
        errors.append("Challenge phase field namespace is not marked distinct")
    if phase.get("empty_reveal_suppressed") is not True:
        errors.append("empty reveal suppression requirement missing")
    if phase.get("range_state") != "POLICY_FIXTURE_ONLY_NOT_EVALUATED":
        errors.append("Challenge phase ranges must remain unevaluated")

    runtime_evidence = contract.get("runtime_evidence", {})
    for key in ("previous_in_memory_receipt_sha256", "previous_in_memory_trace_sha256", "godot_executable_sha256"):
        value = runtime_evidence.get(key)
        if not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{64}", value):
            errors.append("runtime evidence hash invalid: " + key)
    if runtime_evidence.get("previous_integration_tests_passed") != 20:
        errors.append("prior integration test count mismatch")

    boundary = contract.get("execution_boundary", {})
    must_be_false = (
        "persistent_receipt_written",
        "payload_files_written",
        "renderer_native_input_emitted",
        "renderer_dispatch_invoked",
        "renderer_activation",
        "production_execution",
        "media_created",
        "candidate_input_admissible",
    )
    for key in must_be_false:
        if boundary.get(key) is not False:
            errors.append("execution boundary must remain false: " + key)
    if boundary.get("effective_delivery_frame_count") is not None:
        errors.append("effective delivery frame count must remain unresolved")
    if boundary.get("visibility_windows_evaluated") != 0:
        errors.append("visibility window evaluation count must remain zero")
    if boundary.get("renderer") != "OFF" or boundary.get("D4_8") != "BLOCKED" or boundary.get("release_authority") != "NONE":
        errors.append("renderer or release lock mismatch")

    approvals = contract.get("approval_state", {})
    for key, value in approvals.items():
        if isinstance(value, bool) and value is True:
            errors.append("unexpected approved boolean: " + key)
    if approvals.get("D9_14") != "BLOCKED_AS_REQUIRED" or approvals.get("D9_16") != "BLOCKED_AS_REQUIRED":
        errors.append("full acceptance lock mismatch")
    if approvals.get("D9_17") != "BLOCKED_NO_GO" or approvals.get("D10") != "BLOCKED_FOR_PROMOTION":
        errors.append("closure/promotion lock mismatch")
    if approvals.get("release_authority") != "NONE":
        errors.append("release authority must remain NONE")

    return errors


def load_join_contract():
    contract = read_json(JOIN_CONTRACT_REL)
    schema = read_json(JOIN_SCHEMA_REL)

    if schema.get("title") != "C11-D Editorial Payload Provenance Join Contract V2":
        raise RuntimeError("Join contract JSON Schema title mismatch")
    if schema.get("type") != "object":
        raise RuntimeError("Join contract JSON Schema root must be an object")
    required = {
        "schema", "schema_version", "status", "purpose", "runtime_scope",
        "source_pin_count", "source_pins", "editorial_field_cardinality",
        "expected_payload_observations", "challenge_phase_namespace",
        "runtime_evidence", "execution_boundary", "approval_state",
    }
    if not required.issubset(set(schema.get("required", []))):
        raise RuntimeError("Join contract JSON Schema omits required properties")

    errors = validate_join_contract(contract)
    if errors:
        raise RuntimeError("Join contract rejected: " + " | ".join(errors))

    return contract

def content_result_rows(report):
    matches = []
    for value in report.values():
        if (
            isinstance(value, list)
            and len(value) == 3
            and all(isinstance(row, dict) and "content_type" in row and "editorial_fields" in row for row in value)
        ):
            matches.append(value)
    if len(matches) != 1:
        raise AssertionError("Could not unambiguously locate three content-type editorial audit rows")
    return matches[0]


def locate_challenge_timeline(node, path="$"):
    found = []

    if isinstance(node, Mapping):
        # The real Challenge harness reports this as source_timeline.
        # Accept the legacy timeline key only when its facts match the pinned fixture.
        for timeline_key in ("source_timeline", "timeline"):
            candidate = node.get(timeline_key)
            if (
                isinstance(candidate, Mapping)
                and candidate.get("fps") == 60
                and candidate.get("total_frames") == 900
            ):
                found.append((path + "." + timeline_key, dict(candidate)))

        for key, value in node.items():
            if isinstance(value, (Mapping, list)):
                found.extend(locate_challenge_timeline(value, path + "." + str(key)))

    elif isinstance(node, list):
        for index, value in enumerate(node):
            if isinstance(value, (Mapping, list)):
                found.extend(locate_challenge_timeline(value, f"{path}[{index}]"))

    return found


def find_key_values(node, wanted_key):
    values = []

    if isinstance(node, Mapping):
        for key, value in node.items():
            if key == wanted_key:
                values.append(value)
            if isinstance(value, (Mapping, list)):
                values.extend(find_key_values(value, wanted_key))

    elif isinstance(node, list):
        for value in node:
            if isinstance(value, (Mapping, list)):
                values.extend(find_key_values(value, wanted_key))

    return values


# Pinned preconditions before any runtime materialization.
DOCKET_DATA = verify_source_pins()
JOIN_CONTRACT = load_join_contract()
JOIN_CONTRACT_SHA = sha256_file(ROOT / JOIN_CONTRACT_REL)
JOIN_SCHEMA_SHA = sha256_file(ROOT / JOIN_SCHEMA_REL)

contract, schema, lineage = materializer._load_contract(ROOT)
chains = materializer._build_request_chains(ROOT, contract)

# Existing consumption audit builds the real canonical D9.9 plan and checks
# exact editorial string/hash parity with the review manifest.
consumption_report = consumption_audit._build_report(ROOT)
consumption_rows = {
    row["content_type"]: row for row in content_result_rows(consumption_report)
}

# These two existing harnesses create in-memory payload fixtures only.
observations = {}
for harness_name in (
    "visual_loop_drill_materialization",
    "challenge_visual_payload_materialization",
):
    if harness_name not in materializer.HARNESS_SPECS:
        raise RuntimeError("Contracted materialization harness missing: " + harness_name)
    report, evidence = materializer._run_harness(
        harness_name,
        ROOT,
        str(GODOT),
        300,
    )
    observations[harness_name] = (report, evidence)

raw_reports = {name: pair[0] for name, pair in observations.items()}
instances, validated_reports = materializer._validate_reports(ROOT, raw_reports)

# build_receipt constructs and validates the existing request->payload bindings
# in memory. Nothing here writes this receipt to disk.
receipt = materializer.build_receipt(ROOT, observations)

expected_receipt_sha = materializer._sha_json({
    key: value for key, value in receipt.items() if key != "receipt_sha256"
})
if expected_receipt_sha != receipt.get("receipt_sha256"):
    raise RuntimeError("In-memory materialization receipt hash mismatch")

binding_by_type = {row["content_type"]: row for row in receipt["content_bindings"]}
if set(binding_by_type) != set(EXPECTED_FIELDS):
    raise RuntimeError("Receipt binding does not cover the three supported content types")

challenge_report = validated_reports["challenge"]
candidate_timelines = locate_challenge_timeline(challenge_report)
if not candidate_timelines:
    raise RuntimeError("Challenge materializer did not expose the pinned 900-frame @60 FPS source timeline")

unique_timelines = {
    (timeline["fps"], timeline["total_frames"], timeline.get("duration_seconds"))
    for _, timeline in candidate_timelines
}
if len(unique_timelines) != 1:
    raise RuntimeError("Challenge report exposes conflicting source timeline summaries")

challenge_game_counts = find_key_values(challenge_report, "game_frame_count")
if 420 not in challenge_game_counts:
    raise RuntimeError("Challenge report did not expose the expected 420 game-frame snapshots")

challenge_timeline_path, challenge_timeline = candidate_timelines[0]

# Build a compact, deterministic in-memory trace. Do not expose editorial plaintext;
# each canonical value is represented by its exact existing canonical hash.
trace_rows = []
all_field_hashes = {}
nonempty_visual_count = 0
language_count = 0

for content_type in ("challenges", "visual_loops", "visual_drills"):
    chain = chains[content_type]
    canonical_request = chain["result"]["canonical_request"]
    canonical_editorial = chain["result"].get("plan", {}).get("editorial")

    if not isinstance(canonical_editorial, Mapping):
        raise RuntimeError("Canonical D9.9 editorial object missing: " + content_type)

    if set(canonical_editorial) != EXPECTED_FIELDS[content_type]:
        raise RuntimeError("Canonical editorial field set mismatch: " + content_type)

    audit_row = consumption_rows[content_type]
    audit_fields = {row["field"]: row for row in audit_row["editorial_fields"]}

    if set(audit_fields) != set(canonical_editorial):
        raise RuntimeError("Editorial consumption audit field coverage mismatch: " + content_type)

    field_rows = []
    for field, value in canonical_editorial.items():
        if not isinstance(value, str):
            raise RuntimeError(f"Canonical editorial field is not a string: {content_type}.{field}")

        value_hash = consumption_audit._sha(value)
        if value_hash != audit_fields[field]["value_sha256"]:
            raise RuntimeError(f"Canonical editorial value/hash parity failed: {content_type}.{field}")

        if field == "language":
            language_count += 1
            classification = "METADATA_ONLY"
        else:
            classification = "VISUAL_TEXT"
            if value != "":
                nonempty_visual_count += 1

        field_rows.append({
            "field_id": field,
            "value_sha256": value_hash,
            "exact_empty_string": value == "",
            "field_class": classification,
            "review_chain_state": audit_fields[field]["review_chain_state"],
            "visual_payload_consumption_state": audit_fields[field]["visual_payload_consumption_state"],
        })
        all_field_hashes[f"{content_type}.{field}"] = value_hash

    binding = binding_by_type[content_type]
    if binding["request_id"] != canonical_request.get("request_id"):
        raise RuntimeError("Receipt request_id does not bind to the canonical request: " + content_type)
    if binding["canonical_request_sha256"] != chain["result"].get("request_hash"):
        raise RuntimeError("Receipt request hash does not match canonical D9.9 result: " + content_type)
    if binding["producer_plan_sha256"] != chain["result"].get("plan_hash"):
        raise RuntimeError("Receipt producer plan hash does not match canonical result: " + content_type)
    if binding["selection"] != chain["fixture"]["selection"]:
        raise RuntimeError("Receipt selection does not match the pinned request fixture: " + content_type)
    if binding["gameplay_seed"] != canonical_request.get("seed"):
        raise RuntimeError("Gameplay seed identity mismatch: " + content_type)
    if binding["source_seed_matches_request"] is not True:
        raise RuntimeError("Payload source seed mismatch: " + content_type)
    if binding["materialization"] != "IN_MEMORY_ONLY":
        raise RuntimeError("Payload materialization is not in-memory-only: " + content_type)
    if binding["video_render_ready"] is not False:
        raise RuntimeError("Payload unexpectedly claims render readiness: " + content_type)

    if content_type in ("visual_loops", "visual_drills"):
        instance = instances[content_type]
        materialized_frame_count = instance.get("frame_count")
        materialized_fps = instance.get("fps")
        duration = instance.get("duration_seconds")

        if not isinstance(materialized_frame_count, int) or materialized_frame_count <= 0:
            raise RuntimeError("Materialized frame_count is invalid: " + content_type)
        if not isinstance(materialized_fps, (int, float)) or materialized_fps <= 0:
            raise RuntimeError("Materialized FPS is invalid: " + content_type)
        if round(duration * materialized_fps) != materialized_frame_count:
            raise RuntimeError("Materialized duration/FPS/frame_count arithmetic mismatch: " + content_type)

        payload_id = instance.get("instance_id")
        payload_hash = instance.get("payload_instance_sha256")

        if payload_id != binding["payload_instance_id"]:
            raise RuntimeError("Materialized payload ID mismatch: " + content_type)
        if payload_hash != binding["payload_instance_sha256"]:
            raise RuntimeError("Materialized payload hash mismatch: " + content_type)

        observed_frames = {
            "frame_count": materialized_frame_count,
            "fps": materialized_fps,
            "duration_seconds": duration,
            "frame_domain": "REQUEST_SCOPED_IN_MEMORY_AUTHORING_PAYLOAD",
        }
        identity_quality = "MATERIALIZER_INSTANCE_ID_AND_SHA256"
    else:
        materialized_frame_count = int(challenge_timeline["total_frames"])
        materialized_fps = int(challenge_timeline["fps"])

        if binding["payload_instance_sha256"] != challenge_report.get("payload_sha256"):
            raise RuntimeError("Challenge receipt hash does not match materialized Challenge payload")
        if binding["payload_instance_id"] != (
            "D-CHALLENGE-CHALLENGE_004-" + str(challenge_report["payload_sha256"])[:16]
        ):
            raise RuntimeError("Challenge derived receipt alias changed unexpectedly")

        observed_frames = {
            "frame_count": materialized_frame_count,
            "fps": materialized_fps,
            "duration_seconds": challenge_timeline.get("duration_seconds"),
            "game_frame_count": 420,
            "frame_domain": "FROZEN_CHALLENGE_SOURCE_TIMELINE",
            "timeline_path": challenge_timeline_path,
        }
        identity_quality = "DERIVED_RECEIPT_ALIAS_NOT_NATIVE_RUNTIME_INSTANCE_ID"

    trace_rows.append({
        "content_type": content_type,
        "request_id": binding["request_id"],
        "canonical_request_sha256": binding["canonical_request_sha256"],
        "producer_plan_sha256": binding["producer_plan_sha256"],
        "editorial_hash_from_canonical_plan": chain["result"].get("editorial_hash"),
        "selection": binding["selection"],
        "payload_instance_id": binding["payload_instance_id"],
        "payload_instance_sha256": binding["payload_instance_sha256"],
        "payload_identity_quality": identity_quality,
        "materialization": binding["materialization"],
        "observed_materialized_frame_summary": observed_frames,
        "effective_delivery_frame_count": None,
        "delivery_frame_count_status": "NOT_ESTABLISHED_TIMEBASE_POLICY_NOT_APPROVED",
        "editorial_payload_consumption": "NOT_CONSUMED_BY_CURRENT_IN_MEMORY_VISUAL_PAYLOAD_HARNESS",
        "visibility_window_status": "NOT_EVALUATED",
        "editorial_fields": field_rows,
    })

phase_contract = read_json(
    "definitions/c11d/production/D_RENDERER_EDITORIAL_FIELD_WINDOW_PROPOSAL_V1.json"
)
temporal_contract = read_json(
    "definitions/c11d/production/D_RENDERER_CHALLENGE_TEMPORAL_ALIGNMENT_POLICY_PROPOSAL_V1.json"
)
phase_values = phase_contract["pinned_fixture"]["editorial_values"]
phase_ranges = temporal_contract["editorial_windows_reference"]["expected_field_ranges"]

if set(phase_values) != {"hook", "reveal", "cta"}:
    raise RuntimeError("Challenge phase-field namespace changed unexpectedly")
if phase_values["reveal"] != "" or phase_ranges["reveal"] is not None:
    raise RuntimeError("Challenge empty reveal suppression fixture no longer matches the proposal")
if phase_ranges["hook"] != [0, 90] or phase_ranges["cta"] != [390, 450]:
    raise RuntimeError("Pinned Challenge phase-window proposal fixture drift")

delivery_policy = read_json(
    "definitions/c11d/production/D_RENDERER_UNIFIED_DELIVERY_TIMEBASE_POLICY_PROPOSAL_V1.json"
)
universal_policy = read_json(
    "definitions/c11d/production/D_RENDERER_UNIVERSAL_EDITORIAL_FIELD_VISIBILITY_POLICY_PROPOSAL_V1.json"
)
if delivery_policy["policy"]["state"] != "PROPOSED_NOT_APPROVED":
    raise RuntimeError("Delivery timebase proposal state changed unexpectedly")
if universal_policy["policy"]["state"] != "PROPOSED_NOT_APPROVED":
    raise RuntimeError("Universal editorial visibility proposal state changed unexpectedly")

trace = {
    "artifact_id": "C11D_EDITORIAL_PAYLOAD_PROVENANCE_JOIN_IN_MEMORY_DIAGNOSTIC_V1",
    "status": "IN_MEMORY_DIAGNOSTIC_ONLY_NOT_RENDER_INPUT",
    "receipt_sha256": receipt["receipt_sha256"],
    "canonical_content_types": ["challenges", "visual_loops", "visual_drills"],
    "content_rows": trace_rows,
    "editorial_field_instance_count": sum(len(row["editorial_fields"]) for row in trace_rows),
    "nonempty_visual_field_count": nonempty_visual_count,
    "language_metadata_field_count": language_count,
    "challenge_phase_namespace": {
        "field_ids": ["hook", "reveal", "cta"],
        "empty_reveal_suppressed": True,
        "candidate_ranges_status": "POLICY_FIXTURE_ONLY_NOT_EVALUATED",
        "candidate_ranges": phase_ranges,
    },
    "governance": {
        "renderer": "OFF",
        "media_created": False,
        "candidate_input_admissible": False,
        "delivery_timebase_policy_approved": False,
        "universal_editorial_field_window_policy_approved": False,
        "payload_consumer_implementation_authorized": False,
        "approved_bindings": 0,
        "D4_8": "BLOCKED",
        "release_authority": "NONE",
    },
    "persistent_receipt_written": False,
    "renderer_native_input_emitted": False,
    "renderer_dispatch_invoked": False,
    "media_output_created": False,
}
trace_bytes = json.dumps(
    trace, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False
).encode("utf-8")
TRACE_SHA256 = hashlib.sha256(trace_bytes).hexdigest()

class ProvenanceJoinTests(unittest.TestCase):
    def test_01_frozen_manifest_and_docket_source_pins(self):
        self.assertEqual(sha256_file(ROOT / MANIFEST), EXPECTED_MANIFEST_SHA)
        self.assertEqual(sha256_file(ROOT / DOCKET), EXPECTED_DOCKET_SHA)
        self.assertEqual(198, len(verify_source_pins()["source_pins"]))

    def test_02_runtime_sources_match_fixed_hashes(self):
        for relative, expected in FIXED_HASHES.items():
            with self.subTest(path=relative):
                self.assertEqual(sha256_file(ROOT.joinpath(*PurePosixPath(relative).parts)), expected)

    def test_03_canonical_request_chains_cover_three_content_types(self):
        self.assertEqual({"challenges", "visual_loops", "visual_drills"}, set(chains))
        self.assertEqual({"challenges", "visual_loops", "visual_drills"}, set(binding_by_type))

    def test_04_editorial_field_cardinality_is_six_four_four(self):
        expected_counts = {"challenges": 6, "visual_loops": 4, "visual_drills": 4}
        for content_type, expected in expected_counts.items():
            with self.subTest(content_type=content_type):
                self.assertEqual(expected, len(trace_rows_by_type[content_type]["editorial_fields"]))

    def test_05_fourteen_editorial_values_have_exact_hash_parity(self):
        self.assertEqual(14, len(all_field_hashes))
        self.assertEqual(14, trace["editorial_field_instance_count"])
        self.assertEqual(14, len(set(all_field_hashes.keys())))
        self.assertTrue(all(
            isinstance(value, str) and re.fullmatch(r"[0-9a-f]{64}", value)
            for value in all_field_hashes.values()
        ))

    def test_06_all_eleven_visual_test_fields_are_nonempty(self):
        self.assertEqual(11, nonempty_visual_count)
        self.assertEqual(3, language_count)

    def test_07_canonical_editorial_hashes_match_consumption_audit(self):
        self.assertEqual(3, len(consumption_rows))
        for content_type, chain in chains.items():
            editorial = chain["result"]["plan"]["editorial"]
            audit_row = consumption_rows[content_type]
            audit_fields = {row["field"]: row for row in audit_row["editorial_fields"]}
            self.assertEqual(set(editorial), set(audit_fields))
            for field, value in editorial.items():
                with self.subTest(content_type=content_type, field=field):
                    self.assertEqual(consumption_audit._sha(value), audit_fields[field]["value_sha256"])

    def test_08_receipt_request_identity_matches_canonical_chain(self):
        for content_type, chain in chains.items():
            binding = binding_by_type[content_type]
            with self.subTest(content_type=content_type):
                self.assertEqual(chain["result"]["canonical_request"]["request_id"], binding["request_id"])
                self.assertEqual(chain["result"]["request_hash"], binding["canonical_request_sha256"])
                self.assertEqual(chain["result"]["plan_hash"], binding["producer_plan_sha256"])
                self.assertEqual(chain["fixture"]["selection"], binding["selection"])

    def test_09_all_payload_hashes_are_well_formed(self):
        for content_type, binding in binding_by_type.items():
            with self.subTest(content_type=content_type):
                self.assertRegex(binding["payload_instance_sha256"], r"^[0-9a-f]{64}$")
                self.assertTrue(binding["payload_instance_id"])

    def test_10_loop_materialized_frame_count_is_600_at_30_fps(self):
        item = instances["visual_loops"]
        self.assertEqual(600, item["frame_count"])
        self.assertEqual(30, item["fps"])
        self.assertEqual(20.0, item["duration_seconds"])

    def test_11_drill_materialized_frame_count_is_630_at_30_fps(self):
        item = instances["visual_drills"]
        self.assertEqual(630, item["frame_count"])
        self.assertEqual(30, item["fps"])
        self.assertEqual(21.0, item["duration_seconds"])

    def test_12_challenge_source_timeline_is_900_at_60_fps(self):
        self.assertEqual(900, challenge_timeline["total_frames"])
        self.assertEqual(60, challenge_timeline["fps"])
        self.assertIn(420, challenge_game_counts)

    def test_13_effective_delivery_frame_counts_remain_unestablished(self):
        for row in trace_rows:
            with self.subTest(content_type=row["content_type"]):
                self.assertIsNone(row["effective_delivery_frame_count"])
                self.assertEqual("NOT_EVALUATED", row["visibility_window_status"])

    def test_14_all_payloads_are_in_memory_only_and_not_render_ready(self):
        self.assertEqual(materializer.STATUS, receipt["status"])
        self.assertIs(receipt["candidate_input_admissible"], False)
        self.assertIs(receipt["readiness"]["video_render_ready"], False)
        self.assertIs(receipt["execution_boundary"]["payload_files_written"], False)
        self.assertIs(receipt["execution_boundary"]["renderer_dispatch_invoked"], False)
        self.assertIs(receipt["execution_boundary"]["media_output_created"], False)

    def test_15_no_editorial_payload_consumption_is_claimed(self):
        self.assertTrue(all(
            row["editorial_payload_consumption"] ==
            "NOT_CONSUMED_BY_CURRENT_IN_MEMORY_VISUAL_PAYLOAD_HARNESS"
            for row in trace_rows
        ))

    def test_16_challenge_phase_fields_remain_separate(self):
        self.assertEqual(["hook", "reveal", "cta"], trace["challenge_phase_namespace"]["field_ids"])
        self.assertIs(trace["challenge_phase_namespace"]["empty_reveal_suppressed"], True)
        self.assertEqual("POLICY_FIXTURE_ONLY_NOT_EVALUATED",
                         trace["challenge_phase_namespace"]["candidate_ranges_status"])

    def test_17_policy_approval_and_governance_locks_remain_closed(self):
        self.assertEqual("PROPOSED_NOT_APPROVED", delivery_policy["policy"]["state"])
        self.assertEqual("PROPOSED_NOT_APPROVED", universal_policy["policy"]["state"])
        self.assertIs(trace["governance"]["candidate_input_admissible"], False)
        self.assertIs(trace["governance"]["media_created"], False)
        self.assertEqual(0, trace["governance"]["approved_bindings"])
        self.assertEqual("BLOCKED", trace["governance"]["D4_8"])
        self.assertEqual("NONE", trace["governance"]["release_authority"])

    def test_18_receipt_and_trace_hashes_are_reproducible(self):
        self.assertEqual(
            materializer._sha_json({k: v for k, v in receipt.items() if k != "receipt_sha256"}),
            receipt["receipt_sha256"],
        )
        self.assertRegex(TRACE_SHA256, r"^[0-9a-f]{64}$")
        self.assertIs(trace["persistent_receipt_written"], False)

    def test_19_challenge_identity_quality_is_explicitly_limited(self):
        row = trace_rows_by_type["challenges"]
        self.assertEqual(
            "DERIVED_RECEIPT_ALIAS_NOT_NATIVE_RUNTIME_INSTANCE_ID",
            row["payload_identity_quality"],
        )

    def test_20_exact_content_bindings_and_clean_harness_evidence(self):
        self.assertTrue(receipt["readiness"]["all_three_bound"])
        self.assertEqual(3, receipt["readiness"]["bound_content_types"])
        for evidence in receipt["harness_evidence"]:
            with self.subTest(harness=evidence["name"]):
                self.assertEqual(0, evidence["exit_code"])
                self.assertIs(evidence["pass_marker_seen"], True)
                self.assertIs(evidence["runtime_error_log_seen"], False)

    def test_21_join_contract_hashes_and_schema_are_valid(self):
        self.assertEqual([], validate_join_contract(JOIN_CONTRACT))
        self.assertRegex(JOIN_CONTRACT_SHA, r"^[0-9a-f]{64}$")
        schema = read_json(JOIN_SCHEMA_REL)
        self.assertEqual("object", schema["type"])
        self.assertIn("expected_payload_observations", schema["required"])

    def test_22_runtime_observations_match_contract(self):
        expected = {row["content_type"]: row for row in JOIN_CONTRACT["expected_payload_observations"]}
        self.assertEqual({"challenges", "visual_loops", "visual_drills"}, set(expected))
        for content_type, row in trace_rows_by_type.items():
            observed = row["observed_materialized_frame_summary"]
            contract_row = expected[content_type]
            actual = {
                "request_id": row["request_id"],
                "payload_instance_id": row["payload_instance_id"],
                "payload_instance_sha256": row["payload_instance_sha256"],
                "payload_identity_quality": row["payload_identity_quality"],
                "observed_source_frame_count": observed["frame_count"],
                "observed_source_fps": observed["fps"],
                "observed_source_duration_seconds": observed["duration_seconds"],
                "challenge_game_frame_count": observed.get("game_frame_count"),
                "effective_delivery_frame_count": row["effective_delivery_frame_count"],
                "delivery_frame_count_status": row["delivery_frame_count_status"],
                "editorial_payload_consumption": row["editorial_payload_consumption"],
                "visibility_window_status": row["visibility_window_status"],
            }
            with self.subTest(content_type=content_type):
                for key, value in actual.items():
                    self.assertEqual(contract_row[key], value, f"{content_type}.{key}")

    def test_23_previous_deterministic_receipt_and_trace_are_reproduced(self):
        self.assertEqual(
            JOIN_CONTRACT["runtime_evidence"]["previous_in_memory_receipt_sha256"],
            receipt["receipt_sha256"],
        )
        self.assertEqual(
            JOIN_CONTRACT["runtime_evidence"]["previous_in_memory_trace_sha256"],
            TRACE_SHA256,
        )

    def test_24_contract_keeps_delivery_and_governance_unresolved(self):
        boundary = JOIN_CONTRACT["execution_boundary"]
        self.assertIsNone(boundary["effective_delivery_frame_count"])
        self.assertEqual(0, boundary["visibility_windows_evaluated"])
        self.assertEqual("OFF", boundary["renderer"])
        self.assertIs(boundary["candidate_input_admissible"], False)
        self.assertIs(boundary["media_created"], False)
        self.assertEqual("BLOCKED", boundary["D4_8"])
        self.assertEqual("NONE", boundary["release_authority"])

trace_rows_by_type = {row["content_type"]: row for row in trace_rows}
test_suite = unittest.defaultTestLoader.loadTestsFromTestCase(ProvenanceJoinTests)
test_result = unittest.TextTestRunner(stream=sys.stdout, verbosity=2).run(test_suite)

# Recheck the entire docket source pin inventory, fixed runtime files and manifest.
post_errors = []
try:
    verify_source_pins()
except Exception as exc:
    post_errors.append(str(exc))

if post_errors:
    for error in post_errors:
        print("POSTCHECK_FAIL: " + error)
else:
    print("POSTCHECK_SOURCE_PINS=198/198_UNCHANGED")
    print("FIXED_RUNTIME_HASHES=UNCHANGED")
    print("C11C_FROZEN_MANIFEST=UNCHANGED")

print("CONTENT_TYPES=3/3")
print("EDITORIAL_FIELD_INSTANCES=" + str(trace["editorial_field_instance_count"]))
print("NONEMPTY_VISUAL_FIELDS=" + str(nonempty_visual_count))
print("LANGUAGE_METADATA_FIELDS=" + str(language_count))
for row in trace_rows:
    observed = row["observed_materialized_frame_summary"]
    print(
        "JOIN_ROW="
        + row["content_type"]
        + " | request_id=" + row["request_id"]
        + " | payload_id=" + row["payload_instance_id"]
        + " | payload_sha256=" + row["payload_instance_sha256"]
        + " | observed_frame_count=" + str(observed["frame_count"])
        + " | observed_fps=" + str(observed["fps"])
        + " | delivery_frame_count=NOT_ESTABLISHED"
        + " | visibility_windows=NOT_EVALUATED"
    )
print("JOIN_CONTRACT_SHA256=" + JOIN_CONTRACT_SHA)
print("IN_MEMORY_RECEIPT_SHA256=" + receipt["receipt_sha256"])
print("IN_MEMORY_TRACE_SHA256=" + TRACE_SHA256)
print("PERSISTENT_RECEIPT_WRITTEN=false")
print("RENDERER=OFF")
print("MEDIA_CREATED=false")
print("CANDIDATE_INPUT_ADMISSIBLE=false")
print("APPROVED_BINDINGS=0")
print("D4.8=BLOCKED")
print("RELEASE_AUTHORITY=NONE")

if test_result.wasSuccessful() and not post_errors:
    print(
        "EDITORIAL_PAYLOAD_PROVENANCE_JOIN=PASS"
        f" | tests={test_result.testsRun}/{test_result.testsRun}"
        " | source_pins=198/198"
        " | visual_payload_consumption=NOT_PROVEN"
        " | effective_delivery_frame_counts=NOT_ESTABLISHED"
        " | visibility_windows_evaluated=0"
    )
    sys.exit(0)

print("EDITORIAL_PAYLOAD_PROVENANCE_JOIN=FAIL")
sys.exit(1)