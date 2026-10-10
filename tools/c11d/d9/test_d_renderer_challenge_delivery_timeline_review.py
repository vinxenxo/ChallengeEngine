from __future__ import annotations
import copy
import sys
from pathlib import Path
from typing import Any, Callable
HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
from d_renderer_challenge_delivery_timeline_review import (
    ChallengeDeliveryTimelineReviewError, EXPECTED_LINEAGE, build_preview,
    project_boundary, validate_contract, validate_preview,
)
ROOT = Path(__file__).resolve().parents[3]


def reject(label: str, candidate: dict[str, Any]) -> None:
    try:
        validate_preview(candidate, ROOT)
    except (ChallengeDeliveryTimelineReviewError, ValueError, TypeError, KeyError, AssertionError):
        return
    raise AssertionError(f"Expected rejection: {label}")


def run_checks() -> dict[str, int]:
    contract, schema = validate_contract(ROOT)
    assert len(contract["source_lineage"]) == len(EXPECTED_LINEAGE) == 15
    base = build_preview(ROOT)
    validate_preview(base, ROOT)
    try:
        from jsonschema import Draft202012Validator
    except ImportError:
        Draft202012Validator = None
    schema_checks = 1
    jsonschema_checks = 0
    if Draft202012Validator is not None:
        Draft202012Validator.check_schema(schema)
        Draft202012Validator(schema).validate(base)
        jsonschema_checks = 1
    assert [project_boundary(x, 60, 30) for x in [0, 180, 600, 780, 900]] == [0, 90, 300, 390, 450]
    assert project_boundary(1, 2, 1) == 1 and project_boundary(1, 2, 1) == project_boundary(1, 2, 1)
    assert base["runtime_evidence"]["mode"] == "NOT_RUN_BY_PYTHON_CONTRACT_TEST"
    assert base["runtime_evidence"]["runtime_success"] is None
    assert base["source_timeline"]["total_frames"] == 900
    assert sum(x["frame_count"] for x in base["source_segments"]) == 900
    assert sum(x["frame_count"] for x in base["delivery_segments"]) == 450
    mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
      ("wrong schema", lambda x: x.update(schema="OTHER")),
      ("wrong version", lambda x: x.update(schema_version="2.0")),
      ("wrong status", lambda x: x.update(status="RENDERER_INPUT_READY")),
      ("wrong manifest", lambda x: x.update(frozen_c11c_manifest_sha256="0"*64)),
      ("wrong Challenge hash", lambda x: x.update(challenge_source_sha256="f"*64)),
      ("wrong challenge id", lambda x: x["profile_identity"].update(challenge_id="CHALLENGE_003")),
      ("legacy id conflated", lambda x: x["profile_identity"].update(legacy_video_profile_id="REVIEW_720")),
      ("source presentation lost", lambda x: x["profile_identity"].update(source_presentation_profile_id="test_master_11s")),
      ("D presentation conflated with delivery", lambda x: x["profile_identity"].update(d_presentation_profile_id="REVIEW_720")),
      ("wrong delivery id", lambda x: x["delivery_profile"].update(profile_id="MASTER_1080")),
      ("wrong source fps", lambda x: x["source_timeline"].update(fps=30)),
      ("wrong source total", lambda x: x["source_timeline"].update(total_frames=450)),
      ("wrong source duration", lambda x: x["source_timeline"].update(duration_seconds=11)),
      ("wrong phase order", lambda x: x["source_timeline"].update(phase_order=["GAME","HOOK","REVEAL","CTA"])),
      ("wrong source boundaries", lambda x: x["source_timeline"].update(boundary_frames=[0,180,599,780,900])),
      ("wrong delivery fps", lambda x: x["delivery_profile"].update(fps=60)),
      ("wrong delivery geometry", lambda x: x["delivery_profile"].update(width=1080)),
      ("wrong hook source range", lambda x: x["source_segments"][0].update(end_frame=179)),
      ("wrong game source range", lambda x: x["source_segments"][1].update(start_frame=181)),
      ("wrong reveal source count", lambda x: x["source_segments"][2].update(frame_count=179)),
      ("wrong CTA source end", lambda x: x["source_segments"][3].update(end_frame=899)),
      ("wrong hook delivery end", lambda x: x["delivery_segments"][0].update(end_frame=91)),
      ("wrong game delivery start", lambda x: x["delivery_segments"][1].update(start_frame=91)),
      ("wrong game delivery count", lambda x: x["delivery_segments"][1].update(frame_count=211)),
      ("wrong reveal delivery range", lambda x: x["delivery_segments"][2].update(start_frame=299)),
      ("wrong CTA delivery range", lambda x: x["delivery_segments"][3].update(end_frame=451)),
      ("field windows invented", lambda x: x["field_visibility"].update(frame_ranges={"hook":[0,90]})),
      ("field window state promoted", lambda x: x["field_visibility"].update(state="APPROVED")),
      ("Python falsely claims runtime success", lambda x: x["runtime_evidence"].update(runtime_success=True)),
      ("Python falsely claims repeat determinism", lambda x: x["runtime_evidence"].update(repeat_deterministic=True)),
      ("Python falsely claims simulation invariant", lambda x: x["runtime_evidence"].update(simulation_frame_signature_unchanged=True)),
      ("Python falsely claims winning frame invariant", lambda x: x["runtime_evidence"].update(winning_frame_unchanged=True)),
      ("Python falsely claims metrics invariant", lambda x: x["runtime_evidence"].update(metrics_unchanged=True)),
      ("wrong game frames", lambda x: x["runtime_evidence"].update(game_frame_count=419)),
      ("policy approved", lambda x: x.update(policy_state="APPROVED")),
      ("lineage truncated", lambda x: x.update(source_lineage=x["source_lineage"][:-1])),
      ("lineage hash changed", lambda x: x["source_lineage"][0].update(sha256="a"*64)),
      ("report persisted", lambda x: x["execution_boundary"].update(report_file_written=True)),
      ("renderer input emitted", lambda x: x["execution_boundary"].update(renderer_native_input_emitted=True)),
      ("renderer dispatched", lambda x: x["execution_boundary"].update(renderer_dispatch_invoked=True)),
      ("renderer activated", lambda x: x["execution_boundary"].update(renderer_activation=True)),
      ("media created", lambda x: x["execution_boundary"].update(media_created=True)),
      ("C11-C mutation", lambda x: x["execution_boundary"].update(c11c_source_mutation=True)),
      ("output path set", lambda x: x["execution_boundary"].update(output_artifact_path="preview.mp4")),
      ("D4.8 escalation", lambda x: x["execution_boundary"].update(d4_8="AUTHORIZED")),
      ("release authority escalation", lambda x: x["execution_boundary"].update(release_authority="GRANTED")),
      ("video ready escalation", lambda x: x["execution_boundary"].update(video_render_ready=True)),
      ("inject winning-frame mapping", lambda x: x.update(winning_frame_delivery_frame=197)),
      ("inject simulation samples", lambda x: x.update(simulation_sampling_frames=[0,2,4])),
      ("unknown field", lambda x: x.update(renderer_input={})),
    ]
    for label, mutate in mutations:
        changed = copy.deepcopy(base)
        mutate(changed)
        reject(label, changed)
    # Independent arithmetic guard rails for ties, unsupported values, and bool-as-int pitfalls.
    for label, args in [("negative boundary", (-1,60,30)), ("zero source FPS", (0,0,30)), ("zero delivery FPS", (0,60,0)), ("boolean boundary", (True,60,30)), ("boolean FPS", (0,True,30))]:
        try:
            project_boundary(*args)
        except ChallengeDeliveryTimelineReviewError:
            continue
        raise AssertionError(f"Expected projection rejection: {label}")
    return {"lineage": len(EXPECTED_LINEAGE), "negative": len(mutations) + 5, "schema": schema_checks, "jsonschema": jsonschema_checks}


if __name__ == "__main__":
    c = run_checks()
    js = "1/1" if c["jsonschema"] else "NOT_INSTALLED (strict structural checks PASS)"
    print(
      "C11-D RENDERER CHALLENGE DELIVERY TIMELINE REVIEW CONTRACT PASS"
      f" | content_types=1/1 | deterministic=1/1 | source_lineage={c['lineage']}/{c['lineage']}"
      f" | source_ranges=4/4 | delivery_ranges=4/4 | negative={c['negative']}/{c['negative']}"
      f" | schema={c['schema']}/1 | jsonschema={js}"
      " | challenge=CHALLENGE_004:900@60FPS"
      " | delivery=REVIEW_720:450@30FPS"
      " | phase_counts=90>210>90>60"
      " | field_windows=UNRESOLVED | policy=PROPOSED_NOT_APPROVED"
      " | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE"
    )
