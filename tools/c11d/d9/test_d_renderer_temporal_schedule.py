"""Focused tests for source-grounded temporal topology; no instance, renderer or media."""
from __future__ import annotations
import copy, json
from pathlib import Path
from typing import Any
from d_renderer_temporal_schedule import (
    DRendererTemporalScheduleError,
    build_temporal_schedule_proposal,
    validate_temporal_schedule_proposal,
)
ROOT = Path(__file__).resolve().parents[3]
SUPPORTED = ("challenges", "visual_loops", "visual_drills")

def _reject(label: str, fn) -> None:
    try:
        fn()
    except (DRendererTemporalScheduleError, KeyError, TypeError, ValueError):
        return
    raise AssertionError(f"Negative control failed to reject: {label}")

def run_checks() -> dict[str, int]:
    content_checks = deterministic_checks = lineage_checks = schema_checks = jsonschema_checks = 0
    outputs = []
    for ctype in SUPPORTED:
        a = build_temporal_schedule_proposal(ctype, ROOT)
        b = build_temporal_schedule_proposal(ctype, ROOT)
        assert a == b, f"non-deterministic temporal topology for {ctype}"
        validate_temporal_schedule_proposal(a, ROOT)
        assert a["content_type"] == ctype
        assert a["status"] == "PREPARATION_ONLY_TEMPORAL_TOPOLOGY_NOT_RENDERER_INPUT"
        assert a["manifest_sha256"] == "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
        assert len(a["source_lineage"]) == 11
        assert a["instantiation"] == {
            "concrete_schedule_instantiated": False, "duration_values_emitted": False,
            "frame_indices_emitted": False, "frame_ranges_emitted": False,
            "timeline_instantiated": False, "duration_state": "UNBOUND_PROPOSAL_NOT_APPROVED",
        }
        assert a["spatial_integration"]["D1_5_shared_frame_is_unchanged"] is True
        assert a["spatial_integration"]["prior_normalized_permille_proposal_is_canonical"] is False
        content_checks += 1; deterministic_checks += 1; lineage_checks += 1
        outputs.append(a)
    assert outputs[0]["temporal_topology"]["phase_sequence"] == ["HOOK", "GAME", "REVEAL", "CTA"]
    assert outputs[1]["temporal_topology"]["phase_sequence"] == []
    assert outputs[2]["temporal_topology"]["phase_sequence"] == []
    assert outputs[1]["temporal_topology"]["model"] == "EXISTING_CONTINUOUS_LOOP_SPAN"
    assert outputs[2]["temporal_topology"]["model"] == "EXISTING_CONTINUOUS_DRILL_SPAN"

    schema_path = ROOT / "definitions/c11d/production/D_RENDERER_TEMPORAL_SCHEDULE_PROPOSAL_SCHEMA_V1.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8-sig"))
    for out in outputs:
        assert set(out) == set(schema["required"])
        assert schema["additionalProperties"] is False
        assert out["proposal_sha256"] == __import__("d_renderer_temporal_schedule")._sha_json({k: v for k, v in out.items() if k != "proposal_sha256"})
        schema_checks += 1
    try:
        from jsonschema import Draft202012Validator
    except ImportError:
        jsonschema_checks = 0
    else:
        validator = Draft202012Validator(schema)
        for out in outputs:
            errors = list(validator.iter_errors(out))
            if errors:
                raise AssertionError("JSON Schema rejection: " + "; ".join(str(e.message) for e in errors))
            jsonschema_checks += 1

    base = outputs[0]
    mutations: list[tuple[str, Any]] = []
    x = copy.deepcopy(base); x["temporal_topology"]["phase_sequence"] = ["HOOK", "REVEAL", "GAME", "CTA"]; mutations.append(("invented challenge phase order", x))
    x = copy.deepcopy(base); x["temporal_topology"]["phase_sequence"].append("RESULT"); mutations.append(("invent challenge subphase", x))
    x = copy.deepcopy(base); x["temporal_topology"]["duration_authority"] = "FAMILY_NAME_DEFAULT"; mutations.append(("duration from family name", x))
    x = copy.deepcopy(outputs[1]); x["temporal_topology"]["phase_sequence"] = ["HOOK", "GAME"]; mutations.append(("invent Visual Loop phases", x))
    x = copy.deepcopy(outputs[2]); x["temporal_topology"]["phase_sequence"] = ["PREPARE", "TRAIN", "COMPLETE"]; mutations.append(("invent Visual Drill subphases", x))
    x = copy.deepcopy(base); x["temporal_topology"]["model"] = "EXISTING_CONTINUOUS_LOOP_SPAN"; mutations.append(("content model mismatch", x))
    x = copy.deepcopy(outputs[1]); x["temporal_topology"]["duration_authority"] = "RESOLVED_VIDEO_PROFILE_PHASE_DURATIONS"; mutations.append(("wrong loop duration authority", x))
    x = copy.deepcopy(outputs[2]); x["temporal_topology"]["subphase_policy"] = "INFER_FROM_DRILL_TYPE"; mutations.append(("infer drill subphases", x))
    x = copy.deepcopy(base); x["instantiation"]["concrete_schedule_instantiated"] = True; mutations.append(("instantiate concrete schedule", x))
    x = copy.deepcopy(base); x["instantiation"]["duration_values_emitted"] = True; mutations.append(("invent duration values", x))
    x = copy.deepcopy(base); x["instantiation"]["frame_indices_emitted"] = True; mutations.append(("emit frame indices", x))
    x = copy.deepcopy(base); x["instantiation"]["frame_ranges_emitted"] = True; mutations.append(("emit frame ranges", x))
    x = copy.deepcopy(base); x["instantiation"]["timeline_instantiated"] = True; mutations.append(("instantiate timeline", x))
    x = copy.deepcopy(base); x["spatial_integration"]["prior_normalized_permille_proposal_is_canonical"] = True; mutations.append(("promote prior normalized layout", x))
    x = copy.deepcopy(base); x["spatial_integration"]["spatial_bounds_used_by_schedule"] = True; mutations.append(("use unapproved bounds", x))
    x = copy.deepcopy(base); x["source_lineage"].pop(); mutations.append(("remove timing source lineage", x))
    x = copy.deepcopy(base); x["source_lineage"][2]["sha256"] = "0" * 64; mutations.append(("source hash tampering", x))
    x = copy.deepcopy(base); x["manifest_sha256"] = "0" * 64; mutations.append(("mutate C11-C manifest pin", x))
    x = copy.deepcopy(base); x["execution_boundary"]["renderer_native_input_emitted"] = True; mutations.append(("emit renderer input", x))
    x = copy.deepcopy(base); x["execution_boundary"]["renderer_dispatch_invoked"] = True; mutations.append(("dispatch renderer", x))
    x = copy.deepcopy(base); x["execution_boundary"]["renderer_activation"] = True; mutations.append(("activate renderer", x))
    x = copy.deepcopy(base); x["execution_boundary"]["production_execution"] = True; mutations.append(("enable production", x))
    x = copy.deepcopy(base); x["execution_boundary"]["media_output_created"] = True; mutations.append(("create media", x))
    x = copy.deepcopy(base); x["execution_boundary"]["d4_8"] = "AUTHORIZED"; mutations.append(("D4.8 escalation", x))
    x = copy.deepcopy(base); x["execution_boundary"]["release_authority"] = "GRANTED"; mutations.append(("release authority escalation", x))
    x = copy.deepcopy(base); x["execution_boundary"]["c11c_source_mutation"] = True; mutations.append(("mutate C11-C", x))
    x = copy.deepcopy(base); x["unexpected"] = True; mutations.append(("unknown output field", x))
    x = copy.deepcopy(base); x["proposal_sha256"] = "f" * 64; mutations.append(("proposal hash tampering", x))
    for label, candidate in mutations:
        _reject(label, lambda candidate=candidate: validate_temporal_schedule_proposal(candidate, ROOT))
    _reject("longform is unsupported", lambda: build_temporal_schedule_proposal("longform", ROOT))
    _reject("unknown type fails closed", lambda: build_temporal_schedule_proposal("unknown", ROOT))
    _reject("unknown temporal source path", lambda: validate_temporal_schedule_proposal({"content_type":"challenges"}, ROOT))
    return {"content_types":content_checks,"deterministic":deterministic_checks,"source_lineage":lineage_checks,"negative":len(mutations)+3,"schema":schema_checks,"jsonschema":jsonschema_checks}

def main() -> int:
    r=run_checks()
    print(
      "C11-D RENDERER TEMPORAL SCHEDULE PROPOSAL PASS"
      f" | content_types={r['content_types']}/3"
      f" | deterministic={r['deterministic']}/3"
      f" | source_lineage={r['source_lineage']}/3"
      f" | negative={r['negative']}/31"
      f" | schema={r['schema']}/3"
      + (f" | jsonschema={r['jsonschema']}/3" if r['jsonschema']==3 else " | jsonschema=NOT_INSTALLED (strict structural checks PASS)")
      + " | challenge_phases=HOOK>GAME>REVEAL>CTA"
      + " | loops=CONTINUOUS_SPAN | drills=CONTINUOUS_SPAN_NO_SUBPHASES"
      + " | concrete_schedule=NOT_INSTANTIATED | durations=NOT_EMITTED | frame_indices=NOT_EMITTED"
      + " | spatial_source=D1.5_HIERARCHY | renderer_input=NOT_EMITTED"
      + " | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE"
    )
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
