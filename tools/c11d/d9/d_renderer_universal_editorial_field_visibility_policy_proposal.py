from __future__ import annotations
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CONTRACT_PATH = ROOT / "definitions/c11d/production/D_RENDERER_UNIVERSAL_EDITORIAL_FIELD_VISIBILITY_POLICY_PROPOSAL_V1.json"
SCHEMA_PATH = ROOT / "definitions/c11d/production/D_RENDERER_UNIVERSAL_EDITORIAL_FIELD_VISIBILITY_POLICY_PROPOSAL_SCHEMA_V1.json"


def canonical_bytes(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def validate(root=ROOT):
    contract_path = root / "definitions/c11d/production/D_RENDERER_UNIVERSAL_EDITORIAL_FIELD_VISIBILITY_POLICY_PROPOSAL_V1.json"
    schema_path = root / "definitions/c11d/production/D_RENDERER_UNIVERSAL_EDITORIAL_FIELD_VISIBILITY_POLICY_PROPOSAL_SCHEMA_V1.json"
    contract = load_json(contract_path)
    schema = load_json(schema_path)
    try:
        import jsonschema
    except ImportError as exc:
        raise RuntimeError("jsonschema is required for strict proposal validation") from exc
    jsonschema.Draft202012Validator.check_schema(schema)
    jsonschema.Draft202012Validator(schema).validate(contract)

    for pin in contract["source_lineage"]:
        source = root / Path(pin["path"])
        if not source.is_file():
            raise RuntimeError("missing pinned source: " + pin["path"])
        actual = sha256(source)
        if actual != pin["sha256"]:
            raise RuntimeError("source pin mismatch: " + pin["path"] + " expected=" + pin["sha256"] + " actual=" + actual)

    expected = {
        "challenges": (6, 60, 30, 450),
        "visual_loops": (4, 30, 30, 600),
        "visual_drills": (4, 30, 30, 630),
    }
    seen_types = set()
    total_fields = 0
    visible_fields = 0
    metadata_fields = 0
    for entry in contract["content_matrix"]:
        ct = entry["content_type"]
        if ct in seen_types:
            raise RuntimeError("duplicate content type: " + ct)
        seen_types.add(ct)
        if ct not in expected:
            raise RuntimeError("unsupported content type: " + ct)
        count, sfps, dfps, frames = expected[ct]
        if (len(entry["field_rules"]), entry["source_fps"], entry["delivery_fps"], entry["candidate_delivery_frame_count"]) != (count, sfps, dfps, frames):
            raise RuntimeError("candidate timeline/cardinality mismatch: " + ct)
        if entry["candidate_duration_seconds"] != frames / dfps:
            raise RuntimeError("candidate duration mismatch: " + ct)
        ids = [f["field_id"] for f in entry["field_rules"]]
        wanted = ["title", "subtitle", "call_to_action", "language"] if ct != "challenges" else ["title", "subtitle", "call_to_action", "player_name", "challenge_label", "language"]
        if ids != wanted:
            raise RuntimeError("field namespace/order mismatch: " + ct)
        for rule in entry["field_rules"]:
            total_fields += 1
            fid = rule["field_id"]
            if fid == "language":
                metadata_fields += 1
                if (rule["field_class"], rule["target_region"], rule["value_condition"], rule["candidate_window_rule"], rule["candidate_interval_formula"], rule["window_evaluated"]) != ("METADATA_ONLY", None, "METADATA_VALUE", "NO_VISIBILITY_WINDOW", None, False):
                    raise RuntimeError("language must remain metadata-only")
            else:
                visible_fields += 1
                targets = {"title": "HEADER", "subtitle": "HEADER", "call_to_action": "FOOTER", "player_name": "CHALLENGE_OVERLAY", "challenge_label": "CHALLENGE_OVERLAY"}
                if rule["field_class"] != "VISUAL_TEXT" or rule["target_region"] != targets[fid]:
                    raise RuntimeError("field-region mismatch: " + ct + "." + fid)
                if (rule["value_condition"], rule["candidate_window_rule"], rule["candidate_interval_formula"], rule["window_evaluated"]) != ("NONEMPTY_STRING", "FULL_DELIVERY_TIMELINE_IF_NONEMPTY", "[0,delivery_frame_count)", False):
                    raise RuntimeError("candidate window rule mismatch: " + ct + "." + fid)
    if seen_types != set(expected) or (total_fields, visible_fields, metadata_fields) != (14, 11, 3):
        raise RuntimeError("field inventory cardinality mismatch")
    if contract["policy"]["state"] != "PROPOSED_NOT_APPROVED":
        raise RuntimeError("proposal state promoted")
    if contract["policy"]["window_evaluation_state"] != "NOT_EVALUATED_RAW_FIELD_VALUES_ARE_NOT_EXPOSED_BY_CURRENT_RUNTIME_SUMMARY":
        raise RuntimeError("unearned window evaluation claim")
    if contract["policy"]["challenge_phase_namespace_rule"].find("NO_IMPLICIT_ALIAS") < 0:
        raise RuntimeError("phase namespace alias guard missing")
    if contract["approval_state"]["payload_consumer_implementation_authorized"] is not False:
        raise RuntimeError("consumer implementation authorization must remain false")
    if contract["execution_boundary"]["renderer"] != "OFF" or contract["execution_boundary"]["media_created"] is not False:
        raise RuntimeError("renderer/media governance lock violated")

    return {
        "schema": contract["schema"],
        "status": "PREPARATION_ONLY_PROPOSAL_VALIDATED_NOT_APPROVED",
        "content_types": 3,
        "field_instances": total_fields,
        "candidate_window_rules": visible_fields,
        "language_metadata_only": metadata_fields,
        "evaluated_windows": 0,
        "source_pins": len(contract["source_lineage"]),
        "source_pins_verified": True,
        "candidate_input_admissible": False,
        "renderer": "OFF",
        "media_created": False,
        "d4_8": "BLOCKED",
        "release_authority": "NONE",
        "contract_sha256": sha256(contract_path),
        "schema_sha256": sha256(schema_path),
    }


def main():
    try:
        report = validate()
        receipt = hashlib.sha256(canonical_bytes(report)).hexdigest()
        print("C11-D UNIVERSAL EDITORIAL FIELD VISIBILITY POLICY PROPOSAL PASS | content_types=3/3 | field_instances=14/14 | candidate_window_rules=11/11 | language=3/3_METADATA_ONLY | evaluated_windows=0 | approved=false | consumer=NOT_AUTHORIZED | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE")
        report["receipt_sha256"] = receipt
        print("C11-D UNIVERSAL EDITORIAL WINDOW PROPOSAL RECEIPT=" + json.dumps(report, sort_keys=True, separators=(",", ":")))
        return 0
    except Exception as exc:
        print("C11-D UNIVERSAL EDITORIAL WINDOW PROPOSAL FAIL | " + str(exc), file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
