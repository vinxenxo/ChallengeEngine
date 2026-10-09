"""Focused acceptance for source-bound, non-renderable temporal previews."""
from __future__ import annotations
import copy, json, sys
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from d_renderer_temporal_bound_preview import (
    DRendererTemporalBoundPreviewError,
    build_temporal_bound_preview,
    validate_temporal_bound_preview,
    _godot_duration_to_frames,
    _sha_json,
)


def _reject(label: str, action: Callable[[], Any]) -> None:
    try:
        action()
    except (DRendererTemporalBoundPreviewError, ValueError, TypeError, KeyError, AssertionError):
        return
    raise AssertionError(f"Expected rejection for {label}")


def _no_truth_fields(value: Any, where: str = "root") -> None:
    forbidden = {"simulationresult","simulation_result","simulationtruth","simulation_truth","winning_frame","winningframe","close_calls","closecalls","derived_telemetry","derivedtelemetry","gameplay_rng","structural_rng"}
    if isinstance(value, dict):
        for k, v in value.items():
            assert k.replace("-", "_").lower() not in forbidden, f"truth field emitted at {where}.{k}"
            _no_truth_fields(v, f"{where}.{k}")
    elif isinstance(value, list):
        for i, v in enumerate(value): _no_truth_fields(v, f"{where}[{i}]")


def run_checks() -> dict[str, int]:
    content_checks = deterministic = lineage_checks = range_checks = schema_checks = jsonschema_checks = 0
    outputs = []
    for content_type in ("challenges", "visual_loops", "visual_drills"):
        out = build_temporal_bound_preview(content_type, ROOT)
        same = build_temporal_bound_preview(content_type, ROOT)
        assert out == same
        deterministic += 1
        validate_temporal_bound_preview(out, ROOT)
        assert out["status"] == "PREPARATION_ONLY_TEMPORAL_REVIEW_PREVIEW_NOT_RENDERER_INPUT"
        assert out["manifest_sha256"] == "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
        assert len(out["source_lineage"]) == 15
        assert out["topology_proposal_sha256"] == __import__("d_renderer_temporal_schedule").build_temporal_schedule_proposal(content_type, ROOT)["proposal_sha256"]
        lineage_checks += 1
        sched = out["temporal_schedule"]
        segments = sched["segments"]
        assert sched["total_frames"] > 0 and segments[0]["start_frame"] == 0
        for i, segment in enumerate(segments):
            assert segment["frame_count"] == segment["end_frame_exclusive"] - segment["start_frame"]
            assert segment["enabled"] == (segment["frame_count"] > 0)
            if i: assert segment["start_frame"] == segments[i-1]["end_frame_exclusive"]
        assert segments[-1]["end_frame_exclusive"] == sched["total_frames"]
        assert out["schedule_validation"]["segment_ranges_contiguous"] is True
        assert out["schedule_validation"]["segments_cover_total_span"] is True
        assert out["schedule_validation"]["topology_approved"] is False
        assert out["schedule_validation"]["simulation_truth_used"] is False
        _no_truth_fields(out)
        content_checks += 1
        range_checks += 1
        outputs.append(out)

    challenge, loop, drill = outputs
    assert challenge["source_identity"]["source_id"] == "CHALLENGE_004"
    assert challenge["temporal_schedule"]["fps"] == 60
    assert challenge["temporal_schedule"]["total_frames"] == 900
    assert [s["segment_id"] for s in challenge["temporal_schedule"]["segments"]] == ["HOOK", "GAME", "REVEAL", "CTA"]
    assert [(s["start_frame"], s["end_frame_exclusive"], s["frame_count"]) for s in challenge["temporal_schedule"]["segments"]] == [(0,180,180),(180,600,420),(600,780,180),(780,900,120)]
    assert loop["source_identity"]["subtype"] == "geometric"
    assert loop["temporal_schedule"]["total_frames"] == 60 and loop["temporal_schedule"]["fps"] == 30
    assert [s["segment_id"] for s in loop["temporal_schedule"]["segments"]] == ["CONTINUOUS_LOOP"]
    assert drill["source_identity"]["subtype"] == "tracking"
    assert drill["temporal_schedule"]["total_frames"] == 630 and drill["temporal_schedule"]["fps"] == 30
    assert [s["segment_id"] for s in drill["temporal_schedule"]["segments"]] == ["CONTINUOUS_DRILL"]
    assert _godot_duration_to_frames(1/120, 60) == 1  # half-frame rounds upward, unlike Python round()
    assert _godot_duration_to_frames(3/120, 60) == 2  # 1.5 frames rounds upward

    schema_path = ROOT / "definitions/c11d/production/D_RENDERER_TEMPORAL_BOUND_PREVIEW_SCHEMA_V1.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8-sig"))
    for out in outputs:
        assert set(out) == set(schema["required"])
        assert schema["additionalProperties"] is False
        assert out["preview_sha256"] == _sha_json({k:v for k,v in out.items() if k != "preview_sha256"})
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

    mutations: list[tuple[str, Any]] = []
    x=copy.deepcopy(challenge); x["temporal_schedule"]["segments"][0]["start_frame"] = 1; mutations.append(("nonzero initial frame",x))
    x=copy.deepcopy(challenge); x["temporal_schedule"]["segments"][1]["start_frame"] += 1; mutations.append(("segment gap",x))
    x=copy.deepcopy(challenge); x["temporal_schedule"]["segments"][1]["start_frame"] -= 1; mutations.append(("segment overlap",x))
    x=copy.deepcopy(challenge); x["temporal_schedule"]["segments"][1]["frame_count"] += 1; mutations.append(("frame count edit",x))
    x=copy.deepcopy(challenge); x["temporal_schedule"]["segments"][1]["source_duration_seconds"] += 1; mutations.append(("duration edit",x))
    x=copy.deepcopy(challenge); x["temporal_schedule"]["segments"].reverse(); mutations.append(("phase order drift",x))
    x=copy.deepcopy(challenge); x["temporal_schedule"]["fps"] = 30; mutations.append(("challenge FPS override",x))
    x=copy.deepcopy(challenge); x["temporal_schedule"]["total_frames"] += 1; mutations.append(("total frame count edit",x))
    x=copy.deepcopy(challenge); x["temporal_schedule"]["frame_index_convention"] = "ONE_BASED_INCLUSIVE"; mutations.append(("inclusive frame bounds",x))
    x=copy.deepcopy(challenge); x["temporal_schedule"]["segments"][0]["enabled"] = False; mutations.append(("phase disabled",x))
    x=copy.deepcopy(loop); x["temporal_schedule"]["segments"][0]["frame_count"] = 59; mutations.append(("loop frame-count mutation",x))
    x=copy.deepcopy(loop); x["temporal_schedule"]["segments"].append(copy.deepcopy(x["temporal_schedule"]["segments"][0])); mutations.append(("invent loop subphase",x))
    x=copy.deepcopy(drill); x["temporal_schedule"]["segments"][0]["segment_id"] = "TRAIN"; mutations.append(("invent drill subphase",x))
    x=copy.deepcopy(drill); x["temporal_schedule"]["fps"] = 60; mutations.append(("drill FPS override",x))
    x=copy.deepcopy(challenge); x["source_identity"]["source_path"] = "definitions/elsewhere.json"; mutations.append(("source path substitution",x))
    x=copy.deepcopy(challenge); x["source_identity"]["source_sha256"] = "0"*64; mutations.append(("source content hash tampering",x))
    x=copy.deepcopy(challenge); x["topology_proposal_sha256"] = "f"*64; mutations.append(("upstream topology hash tampering",x))
    x=copy.deepcopy(challenge); x["source_lineage"].pop(); mutations.append(("lineage removal",x))
    x=copy.deepcopy(challenge); x["source_lineage"][3]["sha256"] = "0"*64; mutations.append(("lineage digest mutation",x))
    x=copy.deepcopy(challenge); x["manifest_sha256"] = "0"*64; mutations.append(("C11-C manifest mismatch",x))
    x=copy.deepcopy(challenge); x["schedule_validation"]["topology_approved"] = True; mutations.append(("false topology approval",x))
    x=copy.deepcopy(challenge); x["schedule_validation"]["subphases_inferred"] = True; mutations.append(("subphase inference",x))
    x=copy.deepcopy(challenge); x["schedule_validation"]["simulation_truth_used"] = True; mutations.append(("simulation truth coupling",x))
    x=copy.deepcopy(challenge); x["schedule_validation"]["winning_frame_used"] = True; mutations.append(("winning_frame timing control",x))
    x=copy.deepcopy(challenge); x["schedule_validation"]["close_calls_used"] = True; mutations.append(("close_calls timing control",x))
    x=copy.deepcopy(challenge); x["execution_boundary"]["renderer_native_input_emitted"] = True; mutations.append(("renderer input emitted",x))
    x=copy.deepcopy(challenge); x["execution_boundary"]["renderer_dispatch_invoked"] = True; mutations.append(("renderer dispatch",x))
    x=copy.deepcopy(challenge); x["execution_boundary"]["renderer_activation"] = True; mutations.append(("renderer activation",x))
    x=copy.deepcopy(challenge); x["execution_boundary"]["production_execution"] = True; mutations.append(("production execution",x))
    x=copy.deepcopy(challenge); x["execution_boundary"]["media_output_created"] = True; mutations.append(("media creation",x))
    x=copy.deepcopy(challenge); x["execution_boundary"]["output_artifact_path"] = "out.mp4"; mutations.append(("output artifact path",x))
    x=copy.deepcopy(challenge); x["execution_boundary"]["d4_8"] = "AUTHORIZED"; mutations.append(("D4.8 escalation",x))
    x=copy.deepcopy(challenge); x["execution_boundary"]["release_authority"] = "GRANTED"; mutations.append(("release authority escalation",x))
    x=copy.deepcopy(challenge); x["execution_boundary"]["c11c_source_mutation"] = True; mutations.append(("C11-C mutation",x))
    x=copy.deepcopy(challenge); x["unexpected"] = True; mutations.append(("unknown field",x))
    x=copy.deepcopy(challenge); x["preview_sha256"] = "f"*64; mutations.append(("preview hash tampering",x))
    x=copy.deepcopy(challenge); x["temporal_schedule"]["segments"][0]["winning_frame"] = 100; mutations.append(("insert forbidden truth field",x))
    for label, candidate in mutations:
        _reject(label, lambda candidate=candidate: validate_temporal_bound_preview(candidate, ROOT))
    _reject("unsupported Longform", lambda: build_temporal_bound_preview("longform", ROOT))
    _reject("unknown content type", lambda: build_temporal_bound_preview("unknown", ROOT))
    return {"content_types":content_checks,"deterministic":deterministic,"source_lineage":lineage_checks,"frame_ranges":range_checks,"negative":len(mutations)+2,"schema":schema_checks,"jsonschema":jsonschema_checks}


def main() -> int:
    r=run_checks()
    print(
      "C11-D RENDERER TEMPORAL BOUND PREVIEW PASS"
      f" | content_types={r['content_types']}/3"
      f" | deterministic={r['deterministic']}/3"
      f" | source_lineage={r['source_lineage']}/3"
      f" | frame_ranges={r['frame_ranges']}/3"
      f" | negative={r['negative']}/{r['negative']}"
      f" | schema={r['schema']}/3"
      + (f" | jsonschema={r['jsonschema']}/3" if r['jsonschema']==3 else " | jsonschema=NOT_INSTALLED (strict structural checks PASS)")
      + " | challenge=HOOK>GAME>REVEAL>CTA:900_FRAMES@60FPS"
      + " | loop=CONTINUOUS_SPAN:60_FRAMES@30FPS"
      + " | drill=CONTINUOUS_SPAN:630_FRAMES@30FPS"
      + " | preview=IN_MEMORY_REVIEW_ONLY | topology_approved=false"
      + " | renderer_input=NOT_EMITTED | renderer=OFF | media_created=false"
      + " | D4.8=BLOCKED | release_authority=NONE"
    )
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
