from __future__ import annotations
import ast, copy, hashlib, json, sys
from pathlib import Path
from typing import Any, Callable
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
if str(HERE) not in sys.path: sys.path.insert(0, str(HERE))
from d_renderer_delivery_timebase_projection import build_delivery_timebase_projection, validate_delivery_timebase_projection, DRendererDeliveryTimebaseProjectionError, _sha_json

CASES = ("challenges", "visual_loops", "visual_drills")

def _reject(label: str, action: Callable[[], Any]) -> None:
    try: action()
    except (DRendererDeliveryTimebaseProjectionError, ValueError, TypeError, KeyError): return
    raise AssertionError(f"Expected fail-closed rejection: {label}")

def run_checks() -> dict[str, int]:
    source = (HERE / "d_renderer_delivery_timebase_projection.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    forbidden_modules = {"subprocess", "socket", "multiprocessing", "ffmpeg", "godot"}
    forbidden_calls = {"write_text", "write_bytes", "Popen", "system", "startfile", "run", "call", "check_call", "check_output"}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import): assert not any(alias.name.split(".")[0] in forbidden_modules for alias in node.names)
        elif isinstance(node, ast.ImportFrom): assert (node.module or "").split(".")[0] not in forbidden_modules
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute): assert node.func.attr not in forbidden_calls, f"Persistence/dispatch call in module: {node.func.attr}"
    contract = json.loads((ROOT / "definitions/c11d/production/D_RENDERER_DELIVERY_TIMEBASE_PROJECTION_V1.json").read_text(encoding="utf-8-sig"))
    schema = json.loads((ROOT / "definitions/c11d/production/D_RENDERER_DELIVERY_TIMEBASE_PROJECTION_SCHEMA_V1.json").read_text(encoding="utf-8-sig"))
    assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema" and schema["additionalProperties"] is False
    assert set(schema["required"]) == set(schema["properties"])
    assert contract["normalization_policy"]["state"] == "PROPOSED_NOT_APPROVED"
    try:
        from jsonschema import Draft202012Validator
    except ImportError:
        Draft202012Validator = None
    if Draft202012Validator is not None: Draft202012Validator.check_schema(schema)
    counts = {"content":0,"deterministic":0,"lineage":0,"ranges":0,"schema":0,"jsonschema":0}
    candidates: dict[str, dict[str, Any]] = {}
    for content_type in CASES:
        candidate = build_delivery_timebase_projection(content_type, "REVIEW_720", ROOT)
        assert candidate == build_delivery_timebase_projection(content_type, "REVIEW_720", ROOT)
        assert validate_delivery_timebase_projection(candidate, content_type, "REVIEW_720", ROOT) is True
        assert candidate["execution_boundary"]["renderer_native_input_emitted"] is False
        assert candidate["execution_boundary"]["media_output_created"] is False
        assert candidate["execution_boundary"]["video_render_ready"] is False
        assert candidate["normalization_policy"]["approved"] is False
        assert candidate["source_identity"]["source_total_frames"] == candidate["source_timebase"]["total_frames"]
        assert candidate["delivery_timebase"]["total_frames"] == candidate["segments"][-1]["delivery_end_frame_exclusive"]
        assert sum(x["source_frame_count"] for x in candidate["segments"]) == candidate["source_timebase"]["total_frames"]
        assert sum(x["delivery_frame_count"] for x in candidate["segments"]) == candidate["delivery_timebase"]["total_frames"]
        for i, seg in enumerate(candidate["segments"]):
            assert seg["source_end_frame_exclusive"] - seg["source_start_frame"] == seg["source_frame_count"]
            assert seg["delivery_end_frame_exclusive"] - seg["delivery_start_frame"] == seg["delivery_frame_count"]
            assert seg["enabled"] is (seg["delivery_frame_count"] > 0)
            if i:
                assert seg["source_start_frame"] == candidate["segments"][i-1]["source_end_frame_exclusive"]
                assert seg["delivery_start_frame"] == candidate["segments"][i-1]["delivery_end_frame_exclusive"]
        if content_type == "challenges":
            assert candidate["source_timebase"]["fps"] == 60 and candidate["delivery_timebase"]["fps"] == 30
            assert candidate["source_timebase"]["total_frames"] == 900 and candidate["delivery_timebase"]["total_frames"] == 450
            assert [s["delivery_frame_count"] for s in candidate["segments"]] == [90,210,90,60]
            assert candidate["projection_assessment"]["duration_delta_seconds"] == {"numerator":0,"denominator":1}
            assert [s["segment_id"] for s in candidate["segments"]] == ["HOOK","GAME","REVEAL","CTA"]
        else:
            assert candidate["source_timebase"]["fps"] == 30 and candidate["delivery_timebase"]["fps"] == 30
            assert candidate["source_timebase"]["total_frames"] == candidate["delivery_timebase"]["total_frames"]
            assert all(s["source_frame_count"] == s["delivery_frame_count"] for s in candidate["segments"])
        assert candidate["projection_assessment"]["video_render_ready"] is False
        assert candidate["projection_assessment"]["field_visibility_windows"] == "UNRESOLVED_NOT_EMITTED"
        assert candidate["projection_assessment"]["selected_visual_payload_instance_bound"] is False
        assert set(candidate) == set(schema["required"])
        assert candidate["projection_sha256"] == _sha_json({k:v for k,v in candidate.items() if k!="projection_sha256"})
        counts["content"] += 1; counts["deterministic"] += 1; counts["lineage"] += 1; counts["ranges"] += 1; counts["schema"] += 1
        if Draft202012Validator is not None:
            Draft202012Validator(schema).validate(candidate); counts["jsonschema"] += 1
        candidates[content_type] = candidate
    base = candidates["challenges"]
    mutations = [
        ("forged status", lambda x:x.update(status="APPROVED_RENDERER_INPUT")),
        ("profile fps mutation", lambda x:x["delivery_profile"].update(fps=60)),
        ("approved policy escalation", lambda x:x["normalization_policy"].update(approved=True)),
        ("formula mutation", lambda x:x["normalization_policy"].update(formula="drop frames")),
        ("source fps mutation", lambda x:x["source_timebase"].update(fps=x["source_timebase"]["fps"]+1)),
        ("delivery total mutation", lambda x:x["delivery_timebase"].update(total_frames=449)),
        ("source range mutation", lambda x:x["segments"][0].update(source_start_frame=1)),
        ("source count mutation", lambda x:x["segments"][0].update(source_frame_count=x["segments"][0]["source_frame_count"]+1)),
        ("delivery start mutation", lambda x:x["segments"][0].update(delivery_start_frame=x["segments"][0]["delivery_start_frame"]+1)),
        ("delivery end mutation", lambda x:x["segments"][0].update(delivery_end_frame_exclusive=x["segments"][0]["delivery_end_frame_exclusive"]+1)),
        ("delivery count mutation", lambda x:x["segments"][0].update(delivery_frame_count=x["segments"][0]["delivery_frame_count"]+1)),
        ("media-output escalation", lambda x:x["execution_boundary"].update(media_output_created=True)),
        ("D4.8 escalation", lambda x:x["execution_boundary"].update(d4_8="AUTHORIZED")),
    ]
    negatives = 0
    for content_type in CASES:
        source_candidate = candidates[content_type]
        for label, mutate in mutations:
            c = copy.deepcopy(source_candidate); mutate(c)
            _reject(f"{content_type}: {label}", lambda c=c, t=content_type:validate_delivery_timebase_projection(c,t,"REVIEW_720",ROOT))
            negatives += 1
    _reject("unsupported longform", lambda: build_delivery_timebase_projection("longform", "REVIEW_720", ROOT))
    negatives += 1
    _reject("unknown delivery profile", lambda: build_delivery_timebase_projection("challenges", "NOT_A_PROFILE", ROOT))
    negatives += 1
    # One output hash corruption case makes the digest boundary explicit.
    bad_hash = copy.deepcopy(base); bad_hash["projection_sha256"] = "0" * 64
    _reject("projection digest corruption", lambda:validate_delivery_timebase_projection(bad_hash,"challenges","REVIEW_720",ROOT))
    negatives += 1
    assert negatives == 42
    return {**counts,"negative":negatives}

def main() -> int:
    r = run_checks()
    print("C11-D RENDERER DELIVERY TIMEBASE PROJECTION PASS"
      + f" | content_types={r['content']}/3 | deterministic={r['deterministic']}/3 | source_lineage={r['lineage']}/3 | frame_ranges={r['ranges']}/3"
      + f" | negative={r['negative']}/42 | schema={r['schema']}/3"
      + (f" | jsonschema={r['jsonschema']}/3" if r['jsonschema']==3 else " | jsonschema=NOT_INSTALLED (strict structural checks PASS)")
      + " | challenge=900@60FPS_TO_450@30FPS | output_phases=90>210>90>60"
      + " | loops=FPS_MATCH_CONTINUOUS_SPAN | drills=FPS_MATCH_CONTINUOUS_SPAN"
      + " | policy=PROPOSED_NOT_APPROVED | simulation_sampling=UNRESOLVED_NOT_EMITTED"
      + " | video_render_ready=false | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE")
    return 0
if __name__ == "__main__": raise SystemExit(main())
