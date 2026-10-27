import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PACKET_PATH = ROOT / "definitions/c11d/production/D_RENDERER_POLICY_DECISION_DOCKET_V1.json"
MANIFEST_PATH = "release/C11C_FREEZE_PACKAGE_MANIFEST.json"
EXPECTED_MANIFEST_SHA = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
EXPECTED_DECISIONS = {
    "EDITORIAL_VISIBILITY_WINDOWS",
    "EDITORIAL_FIELD_CONSUMPTION",
    "LANGUAGE_FIELD_SEMANTICS",
    "PRESENTATION_REGIONS_AND_GEOMETRY",
    "LOOP_DRILL_DELIVERY_TIMEBASE",
    "CHALLENGE_DELIVERY_TIMEBASE",
    "CHALLENGE_008_009_DURATION_CONFLICT",
    "COORDINATE_PROJECTION_AND_VISIBILITY_CONSUMPTION",
    "AUDIO_MUX_AND_DELIVERY_QA",
    "CANDIDATE_ADMISSION_AND_RENDER_AUTHORIZATION",
}
FIXED_PINS = {
    MANIFEST_PATH: EXPECTED_MANIFEST_SHA,
    "definitions/c11d/production/D_RENDERER_UNIVERSAL_EDITORIAL_FIELD_VISIBILITY_POLICY_PROPOSAL_V1.json": "8ccbb98f63f6e6041cf047ccff8cda2c0b4c4e1c7cb772017f7cb2851a0d99fe",
    "definitions/c11d/production/D_RENDERER_UNIVERSAL_EDITORIAL_FIELD_VISIBILITY_POLICY_PROPOSAL_SCHEMA_V1.json": "f17b39aa0c405d6244b3d1a3b765ee250a1dc8eba86fe8d7eced2c9cfb629bc9",
    "tools/c11d/d9/d_renderer_universal_editorial_field_visibility_policy_proposal.py": "fb949260a6c68b83f40751a2682caa9807c65e6aca2c0e9d02b38b478c6e3d18",
    "tools/c11d/d9/test_d_renderer_universal_editorial_field_visibility_policy_proposal.py": "29339f4834cac69e10443cd252470a2500e844ad68fec0dd58eaac0badd957ce",
    "docs/current/d/D_RENDERER_UNIVERSAL_EDITORIAL_FIELD_VISIBILITY_POLICY_PROPOSAL_CHECKPOINT_V1.md": "715772d708f9cbc410713810449b524bb839cbd6829ba1af9358eb5d3e59feda",
    "definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_ALLOWLISTED_COORDINATE_SOURCE_COMPOSITION_RUNTIME_EVIDENCE_V2_20261026.json": "c09e7beee55c3458e7f6d8778f090cb98ec12650a237787b72f6806ea8d3767b",
    "docs/current/d/C11D_V2B_ALLOWLISTED_COORDINATE_SOURCE_COMPOSITION_RUNTIME_DECISION_V2_20261026.md": "22715d2139dd5a1fd7d747d74cbb7eab9c87f37c3d8f074c5c4a69da4db5aa59",
}
EXPECTED_LOCKS = {
    "renderer": "OFF",
    "media_created": False,
    "candidate_input_admissible": False,
    "seed_domains_complete_for_candidate_input": False,
    "automatic_seed_generation": False,
    "master_seed": "NOT_ADOPTED",
    "approved_bindings": 0,
    "approved_custom_data_bindings": 0,
    "approved_renderer_projection_bindings": 0,
    "D4_8": "BLOCKED",
    "D9_10": "PREPARE_ONLY",
    "D9_14": "BLOCKED",
    "D9_16": "BLOCKED",
    "D9_17": "BLOCKED_NO_GO",
    "D10": "BLOCKED_FOR_PROMOTION",
    "baseline_approval": "MISSING",
    "freeze_eligible": False,
    "release_authority": "NONE",
}

def load_packet():
    with PACKET_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)

def validate_packet(packet):
    errors = []
    if packet.get("schema_version") != "1.0.0":
        errors.append("schema_version mismatch")
    if packet.get("artifact_id") != "C11D_POLICY_DECISION_DOCKET_V1":
        errors.append("artifact_id mismatch")
    if packet.get("status") != "PREPARATION_ONLY_DECISION_DOCKET_NOT_APPROVED":
        errors.append("docket status is not preparation-only")
    pins = packet.get("source_pins")
    if not isinstance(pins, list) or len(pins) != packet.get("source_pin_count"):
        errors.append("source_pin_count mismatch")
        pins = pins if isinstance(pins, list) else []
    paths = [item.get("path") for item in pins if isinstance(item, dict)]
    if len(paths) != len(set(paths)):
        errors.append("duplicate source pin paths")
    by_path = {item.get("path"): item for item in pins if isinstance(item, dict)}
    for path, sha in FIXED_PINS.items():
        item = by_path.get(path)
        if not item or item.get("sha256") != sha:
            errors.append("required fixed pin missing or wrong: " + path)
    for item in pins:
        if not isinstance(item, dict):
            errors.append("source pin is not an object")
            continue
        if not isinstance(item.get("path"), str) or not item["path"]:
            errors.append("source pin path missing")
        sha = item.get("sha256")
        if not isinstance(sha, str) or len(sha) != 64 or any(c not in "0123456789abcdef" for c in sha):
            errors.append("invalid SHA-256 for source pin: " + str(item.get("path")))
        if not isinstance(item.get("bytes"), int) or item["bytes"] < 1:
            errors.append("invalid byte count for source pin: " + str(item.get("path")))
    decisions = packet.get("decisions")
    if not isinstance(decisions, list) or {d.get("id") for d in decisions if isinstance(d, dict)} != EXPECTED_DECISIONS:
        errors.append("decision ID inventory mismatch")
    for decision in decisions if isinstance(decisions, list) else []:
        if not isinstance(decision, dict):
            errors.append("decision entry is not an object")
            continue
        if decision.get("status") != "PENDING_OPERATOR_DECISION":
            errors.append("decision must remain pending: " + str(decision.get("id")))
        for key in ("disposition", "operator", "decided_utc", "rationale"):
            if decision.get(key) is not None:
                errors.append("unexpected pre-filled operator decision field: " + str(decision.get("id")))
    if packet.get("locks") != EXPECTED_LOCKS:
        errors.append("governance locks differ from required closed state")
    readiness = packet.get("editorial_readiness", {})
    if readiness.get("editorial_field_instances") != 14 or readiness.get("candidate_window_rules") != 11:
        errors.append("editorial proposal inventory mismatch")
    if readiness.get("evaluated_windows") != 0:
        errors.append("docket may not claim evaluated editorial windows")
    if readiness.get("universal_editorial_policy_approved") is not False or readiness.get("consumer_authorized") is not False:
        errors.append("editorial policy/consumer was incorrectly authorized")
    return errors

def verify_source_pins(packet):
    errors = []
    for item in packet.get("source_pins", []):
        path = ROOT / item["path"]
        if not path.is_file():
            errors.append("pinned source missing: " + item["path"])
            continue
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != item["sha256"]:
            errors.append("pinned source SHA-256 changed: " + item["path"])
        if path.stat().st_size != item["bytes"]:
            errors.append("pinned source byte count changed: " + item["path"])
    return errors

def main():
    packet = load_packet()
    errors = validate_packet(packet) + verify_source_pins(packet)
    if errors:
        for error in errors:
            print("FAIL: " + error)
        return 1
    print(
        "C11-D POLICY DECISION DOCKET PASS"
        f" | source_pins={packet['source_pin_count']}"
        f" | decisions={len(packet['decisions'])}/10_PENDING"
        " | source_pins_verified=true"
        " | policies_approved=0"
        " | consumer_authorized=false"
        " | renderer=OFF"
        " | media_created=false"
        " | D4.8=BLOCKED"
        " | release_authority=NONE"
    )
    return 0

if __name__ == "__main__":
    sys.exit(main())