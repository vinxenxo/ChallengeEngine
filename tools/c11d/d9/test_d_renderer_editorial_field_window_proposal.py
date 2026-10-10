from __future__ import annotations

import copy
import json
import sys
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import d_renderer_editorial_field_window_proposal as mod

SEGMENTS = [dict(x) for x in mod.EXPECTED_DELIVERY_SEGMENTS]
EDITORIAL = dict(mod.EXPECTED_EDITORIAL)


def _reject(label: str, action: Callable[[], Any]) -> None:
    try:
        action()
    except (mod.EditorialFieldWindowError, TypeError, KeyError, ValueError):
        return
    raise AssertionError(f"Negative case unexpectedly passed: {label}")


def run_checks() -> dict[str, int | str]:
    contract, schema, source_status = mod.validate_contract(ROOT)
    harness_path = ROOT / "tools/c11d/d9/review_editorial_field_windows_in_memory.gd"
    harness_source = harness_path.read_text(encoding="utf-8")
    empty_digest = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    if f'const EmptySha256 := "{empty_digest}"' not in harness_source:
        raise AssertionError("Godot harness must declare the canonical SHA-256 digest for empty UTF-8 text")
    empty_hash_guard = (
        "func _sha256_bytes(bytes: PackedByteArray) -> String:\n"
        "    # Godot HashingContext.update() rejects an empty PackedByteArray. SHA-256(empty)\n"
        "    # is a defined digest; return the standard value without invoking update().\n"
        "    if bytes.is_empty():\n"
        "        return EmptySha256\n"
    )
    if empty_hash_guard not in harness_source:
        raise AssertionError("Godot harness must handle empty bytes before calling HashingContext.update")
    good = mod.build_field_window_proposal(EDITORIAL, SEGMENTS)
    mod.validate_preview(good, schema)
    repeat = mod.build_field_window_proposal(EDITORIAL, SEGMENTS)
    if mod.canonical_json(good) != mod.canonical_json(repeat):
        raise AssertionError("Determinism check failed")
    if good["proposal_sha256"] != repeat["proposal_sha256"]:
        raise AssertionError("Canonical digest determinism check failed")
    fields = good["fields"]
    if len(fields) != 3 or fields[0]["visibility_range"] != {"start_frame": 0, "end_frame": 90, "frame_count": 90}:
        raise AssertionError("HOOK field window mismatch")
    if fields[1]["state"] != "SUPPRESSED_EMPTY_EDITORIAL_FIELD" or fields[1]["visibility_range"] is not None:
        raise AssertionError("Empty REVEAL field must be suppressed")
    if fields[2]["visibility_range"] != {"start_frame": 390, "end_frame": 450, "frame_count": 60}:
        raise AssertionError("CTA field window mismatch")
    if good["execution_boundary"]["renderer_native_input_emitted"] is not False:
        raise AssertionError("Renderer input boundary invariant failed")

    negatives: list[str] = []
    def bad(label: str, mutate: Callable[[dict[str, Any]], None]) -> None:
        altered = copy.deepcopy(good)
        mutate(altered)
        _reject(label, lambda: mod.validate_preview(altered, schema))
        negatives.append(label)

    bad("status promoted", lambda x: x.update(status="APPROVED_RENDERER_INPUT"))
    bad("policy approved", lambda x: x["policy"].update(state="APPROVED"))
    bad("policy ID changed", lambda x: x["policy"].update(policy_id="OTHER"))
    bad("delivery profile changed", lambda x: x["delivery_profile"].update(profile_id="MASTER_1080"))
    bad("delivery FPS changed", lambda x: x["delivery_profile"].update(fps=60))
    bad("delivery frame count changed", lambda x: x["delivery_profile"].update(total_frames=900))
    bad("field count reduced", lambda x: x.update(fields=x["fields"][:2]))
    bad("field order changed", lambda x: x.update(fields=list(reversed(x["fields"]))))
    bad("field identity changed", lambda x: x["fields"][0].update(field_id="title"))
    bad("field phase changed", lambda x: x["fields"][0].update(phase="GAME"))
    bad("hook text rewritten", lambda x: x["fields"][0].update(source_text="new copy"))
    bad("hook text hash changed", lambda x: x["fields"][0].update(source_text_sha256="0" * 64))
    bad("hook start shifted", lambda x: x["fields"][0]["visibility_range"].update(start_frame=1))
    bad("hook end shifted", lambda x: x["fields"][0]["visibility_range"].update(end_frame=89))
    bad("hook cardinality changed", lambda x: x["fields"][0]["visibility_range"].update(frame_count=89))
    bad("hook state concealed", lambda x: x["fields"][0].update(state="APPROVED_VISIBLE_WINDOW"))
    bad("empty reveal gets window", lambda x: x["fields"][1].update(visibility_range={"start_frame": 300, "end_frame": 390, "frame_count": 90}))
    bad("empty reveal state changed", lambda x: x["fields"][1].update(state="PROPOSED_VISIBLE_WINDOW"))
    bad("CTA start shifted", lambda x: x["fields"][2]["visibility_range"].update(start_frame=389))
    bad("CTA end shifted", lambda x: x["fields"][2]["visibility_range"].update(end_frame=451))
    bad("visual loop fields invented", lambda x: x["unresolved_content_types"].update(visual_loops="MAPPED"))
    bad("drill fields invented", lambda x: x["unresolved_content_types"].update(visual_drills="MAPPED"))
    bad("source lineage digest changed", lambda x: x["source_lineage"][0].update(sha256="0" * 64))
    bad("frozen manifest changed", lambda x: x.update(frozen_c11c_manifest_sha256="0" * 64))
    bad("challenge source changed", lambda x: x.update(challenge_source_sha256="0" * 64))
    bad("write report enabled", lambda x: x["execution_boundary"].update(report_file_written=True))
    bad("renderer input enabled", lambda x: x["execution_boundary"].update(renderer_native_input_emitted=True))
    bad("renderer dispatch enabled", lambda x: x["execution_boundary"].update(renderer_dispatch_invoked=True))
    bad("renderer activation enabled", lambda x: x["execution_boundary"].update(renderer_activation=True))
    bad("media created", lambda x: x["execution_boundary"].update(media_created=True))
    bad("C11-C source mutation enabled", lambda x: x["execution_boundary"].update(c11c_source_mutation=True))
    bad("video readiness escalated", lambda x: x["execution_boundary"].update(video_render_ready=True))
    bad("D4.8 escalated", lambda x: x["execution_boundary"].update(d4_8="AUTHORIZED"))
    bad("release authority escalated", lambda x: x["execution_boundary"].update(release_authority="GRANTED"))
    bad("output path inserted", lambda x: x["execution_boundary"].update(output_artifact_path="artifacts/production.mp4"))
    bad("unknown output field inserted", lambda x: x.update(renderer_command=["godot", "--render"]))
    bad("proposal digest altered", lambda x: x.update(proposal_sha256="0" * 64))
    if len(negatives) != 37:
        raise AssertionError(f"Unexpected negative-test cardinality: {len(negatives)}")

    input_negatives: list[str] = []
    def bad_input(label: str, action: Callable[[], Any]) -> None:
        _reject(label, action)
        input_negatives.append(label)
    bad_input("unsupported visual loop content type", lambda: mod.build_field_window_proposal(EDITORIAL, SEGMENTS, "visual_loops"))
    bad_input("unsupported visual drill content type", lambda: mod.build_field_window_proposal(EDITORIAL, SEGMENTS, "visual_drills"))
    bad_input("unsupported longform content type", lambda: mod.build_field_window_proposal(EDITORIAL, SEGMENTS, "longform"))
    bad_input("editorial root not object", lambda: mod.build_field_window_proposal([], SEGMENTS))
    bad_input("field missing", lambda: mod.build_field_window_proposal({"hook": EDITORIAL["hook"], "cta": EDITORIAL["cta"]}, SEGMENTS))
    bad_input("unknown field added", lambda: mod.build_field_window_proposal({**EDITORIAL, "game_label": "x"}, SEGMENTS))
    bad_input("wrong hook source copy", lambda: mod.build_field_window_proposal({**EDITORIAL, "hook": "rewritten"}, SEGMENTS))
    bad_input("numeric editorial field", lambda: mod.build_field_window_proposal({**EDITORIAL, "hook": 3}, SEGMENTS))
    bad_input("phase array missing", lambda: mod.build_field_window_proposal(EDITORIAL, []))
    bad_input("phase order altered", lambda: mod.build_field_window_proposal(EDITORIAL, [SEGMENTS[1], SEGMENTS[0], SEGMENTS[2], SEGMENTS[3]]))
    bad_input("duplicate phase", lambda: mod.build_field_window_proposal(EDITORIAL, [SEGMENTS[0], SEGMENTS[0], SEGMENTS[2], SEGMENTS[3]]))
    bad_input("frame boundary bool", lambda: mod.build_field_window_proposal(EDITORIAL, [{**SEGMENTS[0], "start_frame": False}, *SEGMENTS[1:]]))
    bad_input("frame count drift", lambda: mod.build_field_window_proposal(EDITORIAL, [{**SEGMENTS[0], "frame_count": 89}, *SEGMENTS[1:]]))
    bad_input("gap between phases", lambda: mod.build_field_window_proposal(EDITORIAL, [SEGMENTS[0], {**SEGMENTS[1], "start_frame": 91}, SEGMENTS[2], SEGMENTS[3]]))
    bad_input("overlapping phases", lambda: mod.build_field_window_proposal(EDITORIAL, [SEGMENTS[0], {**SEGMENTS[1], "start_frame": 89}, SEGMENTS[2], SEGMENTS[3]]))
    bad_input("delivery end drift", lambda: mod.build_field_window_proposal(EDITORIAL, [*SEGMENTS[:3], {**SEGMENTS[3], "end_frame": 449, "frame_count": 59}]))
    if len(input_negatives) != 16:
        raise AssertionError(f"Unexpected input-negative cardinality: {len(input_negatives)}")

    schema_count = 1
    try:
        import jsonschema
        jsonschema.Draft202012Validator.check_schema(schema)
        jsonschema.Draft202012Validator(schema).validate(good)
        schema_count = 1
    except ImportError:
        # Strict structural checks above remain active when the optional package is absent.
        schema_count = 0
    except Exception as exc:
        raise AssertionError(f"Schema validation failed: {exc}") from exc

    return {
        "fields": 3,
        "mapped": 2,
        "deterministic": 1,
        "lineage_declarations": len(mod.EXPECTED_LINEAGE),
        "source_status": source_status,
        "empty_hash_guard": "PASS",
        "negative": len(negatives) + len(input_negatives),
        "schema": 1,
        "jsonschema": schema_count,
    }


def main() -> int:
    result = run_checks()
    jsonschema_status = f"{result['jsonschema']}/1" if result["jsonschema"] else "NOT_INSTALLED (strict structural checks PASS)"
    print(
        "C11-D RENDERER EDITORIAL FIELD WINDOW PROPOSAL CONTRACT PASS"
        f" | content_types=1/1 | fields={result['fields']}/3 | mapping={result['mapped']}/3"
        f" | deterministic={result['deterministic']}/1 | source_lineage={result['lineage_declarations']}/{result['lineage_declarations']}"
        f" | source_files={result['source_status']} | negative={result['negative']}/{result['negative']}"
        f" | schema={result['schema']}/1 | jsonschema={jsonschema_status}"
        f" | empty_hash_guard={result['empty_hash_guard']}"
        " | hook=[0,90) | reveal=EMPTY_SUPPRESSED | cta=[390,450)"
        " | policy=PROPOSED_NOT_APPROVED | non_challenge_fields=UNRESOLVED"
        " | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE"
    )
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
