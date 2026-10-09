"""Acceptance/regression tests for the renderer-neutral frame-program candidate."""
from __future__ import annotations

import ast
import copy
import json
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any, Callable

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from d_renderer_candidate import build_renderer_binding_preview, sha256_json
from d_renderer_logical_composition import build_logical_composition_plan
from d_renderer_frame_program import (
    CONTRACT_REL, OUTPUT_SCHEMA_REL, LOGICAL_CONTRACT_REL, LOGICAL_SCHEMA_REL,
    DRendererFrameProgramError, PROGRAM_SCHEMA, PROGRAM_STATUS,
    build_renderer_neutral_frame_program, validate_renderer_neutral_frame_program, _load_contract,
)
from test_d_renderer_candidate import _envelope, _representative_selections, _reseal_adapter


def _fixture(content_type: str, request_id: str, *, title: str = "Frame program title", seed: int = 12345, music_seed: int = 840001):
    envelope = _envelope(_representative_selections()[content_type], request_id, title=title, seed=seed, music_seed=music_seed)
    preview = build_renderer_binding_preview(envelope, ROOT)
    composition = build_logical_composition_plan(preview, envelope, ROOT)
    program = build_renderer_neutral_frame_program(composition, preview, envelope, ROOT)
    return envelope, preview, composition, program


def _reseal(program: dict[str, Any]) -> dict[str, Any]:
    program["program_sha256"] = sha256_json({key: value for key, value in program.items() if key != "program_sha256"})
    return program


def _must_reject(label: str, action: Callable[[], Any]) -> None:
    try:
        action()
    except (DRendererFrameProgramError, ValueError, TypeError, KeyError):
        return
    raise AssertionError(f"Expected fail-closed rejection: {label}")


def run_checks() -> dict[str, int]:
    # Static import/call guard: this candidate must remain pure, in-memory and non-dispatchable.
    tree = ast.parse((HERE / "d_renderer_frame_program.py").read_text(encoding="utf-8"))
    forbidden_modules = {"subprocess", "ffmpeg", "godot", "os", "shutil", "socket", "multiprocessing", "pygame", "cv2", "PIL"}
    forbidden_calls = {"write_text", "write_bytes", "open", "Popen", "system", "startfile", "run", "call", "check_call", "check_output", "unlink", "mkdir", "makedirs"}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            assert not any(alias.name.split(".")[0] in forbidden_modules for alias in node.names), "frame program must not import execution/media/persistence modules"
        elif isinstance(node, ast.ImportFrom):
            assert (node.module or "").split(".")[0] not in forbidden_modules, "frame program must not import execution/media/persistence modules"
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            assert node.func.attr not in forbidden_calls, f"forbidden execution/persistence call in frame program: {node.func.attr}"

    schema_doc = json.loads((ROOT / OUTPUT_SCHEMA_REL).read_text(encoding="utf-8"))
    assert schema_doc.get("$schema") == "https://json-schema.org/draft/2020-12/schema"
    assert schema_doc.get("$id") == "urn:c11d:renderer-neutral-frame-program:v1"
    assert schema_doc.get("additionalProperties") is False
    assert set(schema_doc["required"]) == set(schema_doc["properties"])
    for name in ("contract_identity", "implementation_identity", "source_identity", "content_identity", "canvas_descriptor", "localization", "temporal_model", "seed_isolation", "truth_and_telemetry", "execution_boundary"):
        obj = schema_doc["properties"][name]
        assert obj.get("type") == "object" and obj.get("additionalProperties") is False, name
        assert set(obj.get("required", [])) == set(obj.get("properties", {})), name
    for array_name in ("region_declarations", "instructions"):
        item_schema = schema_doc["properties"][array_name]["items"]
        assert item_schema.get("additionalProperties") is False
        assert set(item_schema.get("required", [])) == set(item_schema.get("properties", {}))
    try:
        import jsonschema  # type: ignore[import-not-found]
    except ImportError:
        jsonschema = None
    if jsonschema is not None:
        jsonschema.Draft202012Validator.check_schema(schema_doc)

    positive = 0
    deterministic = 0
    flow = 0
    schema_checks = 0
    full_schema_checks = 0
    fixtures = {}
    expected_counts = {"challenges": 5, "visual_loops": 3, "visual_drills": 3}
    for content_type in ("challenges", "visual_loops", "visual_drills"):
        envelope, preview, composition, program = _fixture(content_type, f"D-FRAME-PROGRAM-{content_type.upper()}")
        repeated = build_renderer_neutral_frame_program(copy.deepcopy(composition), copy.deepcopy(preview), copy.deepcopy(envelope), ROOT)
        assert repeated == program, f"non-deterministic frame declarations for {content_type}"
        assert program["schema"] == PROGRAM_SCHEMA and program["status"] == PROGRAM_STATUS
        assert program["content_identity"]["content_type"] == content_type
        assert program["source_identity"]["logical_composition_sha256"] == composition["composition_sha256"]
        assert len(program["instructions"]) == expected_counts[content_type]
        assert [item["instruction_index"] for item in program["instructions"]] == list(range(expected_counts[content_type]))
        assert all(item["instruction_type"] == "DECLARE_SEMANTIC_TEXT_BINDING" for item in program["instructions"])
        assert all(item["target_mapping_state"] == "PROPOSED_NOT_APPROVED" for item in program["instructions"])
        assert all(item["layout_binding_state"] == "UNRESOLVED_NO_COORDINATES" for item in program["instructions"])
        assert all(item["temporal_binding_state"] == "NOT_SCHEDULED_NO_FRAME_RANGE" for item in program["instructions"])
        assert program["temporal_model"] == {"schedule_state":"NOT_DEFINED","frame_ranges_defined":False,"frame_ranges":None,"duration_frames":None,"timing_source":"NOT_PROVIDED_BY_LOGICAL_COMPOSITION"}
        assert program["canvas_descriptor"]["pixel_coordinates_emitted"] is False
        assert program["execution_boundary"] == {
            "program_mode":"IN_MEMORY_DECLARATIVE_REVIEW_ONLY","program_executable":False,
            "renderer_native_input_emitted":False,"renderer_dispatch_invoked":False,"renderer_activation":False,
            "production_execution":False,"media_output_created":False,"output_artifact_path":None,
            "frame_schedule_defined":False,"pixel_coordinates_emitted":False,"d4_8":"BLOCKED",
            "release_authority":"NONE","c11c_source_mutation":False,
        }
        assert validate_renderer_neutral_frame_program(program, composition, preview, envelope, ROOT) is True
        expected_by_id = {item["element_id"]: item for item in composition["text_elements"]}
        actual_by_id = {item["element_id"]: item for item in program["instructions"]}
        assert set(expected_by_id) == set(actual_by_id)
        for element_id, source in expected_by_id.items():
            instruction = actual_by_id[element_id]
            assert instruction["text_value"] == source["text_value"]
            assert instruction["text_sha256"] == source["text_sha256"]
            assert instruction["region_id"] == source["target_region"]
            assert instruction["z_order"] == source["z_order"]
        assert set(program) == set(schema_doc["required"])
        schema_checks += 1
        if jsonschema is not None:
            jsonschema.Draft202012Validator(schema_doc).validate(program)
            full_schema_checks += 1
        fixtures[content_type] = (envelope, preview, composition, program)
        positive += 1
        deterministic += 1
        flow += 1

    # Editorial mutation must affect the bound declaration, not just provenance.
    loop_selection = _representative_selections()["visual_loops"]
    envelope_a = _envelope(loop_selection, "D-FRAME-EDITORIAL-DELTA", title="Editorial A")
    envelope_b = _envelope(loop_selection, "D-FRAME-EDITORIAL-DELTA", title="Editorial B")
    preview_a = build_renderer_binding_preview(envelope_a, ROOT)
    preview_b = build_renderer_binding_preview(envelope_b, ROOT)
    composition_a = build_logical_composition_plan(preview_a, envelope_a, ROOT)
    composition_b = build_logical_composition_plan(preview_b, envelope_b, ROOT)
    program_a = build_renderer_neutral_frame_program(composition_a, preview_a, envelope_a, ROOT)
    program_b = build_renderer_neutral_frame_program(composition_b, preview_b, envelope_b, ROOT)
    title_a = next(item for item in program_a["instructions"] if item["source_field"] == "title")
    title_b = next(item for item in program_b["instructions"] if item["source_field"] == "title")
    assert title_a["text_value"] == "Editorial A" and title_b["text_value"] == "Editorial B"
    assert title_a["text_sha256"] != title_b["text_sha256"]
    assert program_a["program_sha256"] != program_b["program_sha256"]

    # Music seed changes lineage, but not visual/text declarations.
    _, _, _, music_program = _fixture("visual_loops", "D-FRAME-MUSIC-SEED", seed=12345, music_seed=840002)
    assert music_program["instructions"] == fixtures["visual_loops"][3]["instructions"]
    assert music_program["seed_isolation"]["cross_domain_seed_sharing"] == "FORBIDDEN"

    negative = 0
    envelope, preview, composition, original = fixtures["visual_loops"]

    altered_text = copy.deepcopy(original)
    altered_text["instructions"][0]["text_value"] = "forged"
    _reseal(altered_text)
    _must_reject("forged editorial text even with resealed program", lambda: validate_renderer_neutral_frame_program(altered_text, composition, preview, envelope, ROOT)); negative += 1

    promoted_region = copy.deepcopy(original)
    promoted_region["region_declarations"][0]["mapping_state"] = "APPROVED"
    _reseal(promoted_region)
    _must_reject("semantic region self-promotion", lambda: validate_renderer_neutral_frame_program(promoted_region, composition, preview, envelope, ROOT)); negative += 1

    promoted_field = copy.deepcopy(original)
    promoted_field["instructions"][0]["target_mapping_state"] = "APPROVED"
    _reseal(promoted_field)
    _must_reject("field target self-promotion", lambda: validate_renderer_neutral_frame_program(promoted_field, composition, preview, envelope, ROOT)); negative += 1

    activated = copy.deepcopy(original)
    activated["execution_boundary"]["renderer_activation"] = True
    _reseal(activated)
    _must_reject("renderer activation promotion", lambda: validate_renderer_neutral_frame_program(activated, composition, preview, envelope, ROOT)); negative += 1

    emitted = copy.deepcopy(original)
    emitted["execution_boundary"]["renderer_native_input_emitted"] = True
    _reseal(emitted)
    _must_reject("renderer-native input claim", lambda: validate_renderer_neutral_frame_program(emitted, composition, preview, envelope, ROOT)); negative += 1

    executable = copy.deepcopy(original)
    executable["execution_boundary"]["program_executable"] = True
    _reseal(executable)
    _must_reject("declaration plan cannot become executable", lambda: validate_renderer_neutral_frame_program(executable, composition, preview, envelope, ROOT)); negative += 1

    media = copy.deepcopy(original)
    media["execution_boundary"]["media_output_created"] = True
    _reseal(media)
    _must_reject("media output escalation", lambda: validate_renderer_neutral_frame_program(media, composition, preview, envelope, ROOT)); negative += 1

    schedule = copy.deepcopy(original)
    schedule["temporal_model"]["frame_ranges_defined"] = True
    _reseal(schedule)
    _must_reject("invented frame schedule", lambda: validate_renderer_neutral_frame_program(schedule, composition, preview, envelope, ROOT)); negative += 1

    pixels = copy.deepcopy(original)
    pixels["canvas_descriptor"]["pixel_coordinates_emitted"] = True
    _reseal(pixels)
    _must_reject("pixel coordinate escalation", lambda: validate_renderer_neutral_frame_program(pixels, composition, preview, envelope, ROOT)); negative += 1

    release = copy.deepcopy(original)
    release["execution_boundary"]["release_authority"] = "APPROVED"
    _reseal(release)
    _must_reject("release authority escalation", lambda: validate_renderer_neutral_frame_program(release, composition, preview, envelope, ROOT)); negative += 1

    unknown = copy.deepcopy(original)
    unknown["execution_path"] = "godot"
    _reseal(unknown)
    _must_reject("unknown top-level field", lambda: validate_renderer_neutral_frame_program(unknown, composition, preview, envelope, ROOT)); negative += 1

    instruction_missing = copy.deepcopy(original)
    instruction_missing["instructions"].pop()
    _reseal(instruction_missing)
    _must_reject("missing declaration", lambda: validate_renderer_neutral_frame_program(instruction_missing, composition, preview, envelope, ROOT)); negative += 1

    instruction_duplicate = copy.deepcopy(original)
    instruction_duplicate["instructions"].append(copy.deepcopy(instruction_duplicate["instructions"][0]))
    _reseal(instruction_duplicate)
    _must_reject("duplicate declaration", lambda: validate_renderer_neutral_frame_program(instruction_duplicate, composition, preview, envelope, ROOT)); negative += 1

    region_mismatch = copy.deepcopy(original)
    region_mismatch["instructions"][0]["region_id"] = "FOOTER"
    _reseal(region_mismatch)
    _must_reject("semantic region mismatch", lambda: validate_renderer_neutral_frame_program(region_mismatch, composition, preview, envelope, ROOT)); negative += 1

    bad_hash = copy.deepcopy(original)
    bad_hash["program_sha256"] = "0" * 64
    _must_reject("program digest mismatch", lambda: validate_renderer_neutral_frame_program(bad_hash, composition, preview, envelope, ROOT)); negative += 1

    changed_source = _envelope(_representative_selections()["visual_loops"], "D-FRAME-WRONG-SOURCE", title="Other request")
    _must_reject("program attached to a different adapter lineage", lambda: validate_renderer_neutral_frame_program(original, composition, preview, changed_source, ROOT)); negative += 1

    unsupported_program = copy.deepcopy(original)
    unsupported_program["content_identity"]["content_type"] = "longform"
    _reseal(unsupported_program)
    _must_reject("Longform rejected at frame-program boundary", lambda: validate_renderer_neutral_frame_program(unsupported_program, composition, preview, envelope, ROOT)); negative += 1

    with tempfile.TemporaryDirectory(prefix="c11d_frame_program_contract_lock_") as temp:
        temp_root = Path(temp)
        for rel in (CONTRACT_REL, OUTPUT_SCHEMA_REL, LOGICAL_CONTRACT_REL, LOGICAL_SCHEMA_REL):
            destination = temp_root / rel
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / rel, destination)
        target = temp_root / CONTRACT_REL
        contract_doc = json.loads(target.read_text(encoding="utf-8"))
        contract_doc["approval_state"]["frame_program_approved"] = True
        target.write_text(json.dumps(contract_doc, indent=2), encoding="utf-8")
        _must_reject("contract self-approval", lambda: _load_contract(temp_root)); negative += 1

    with tempfile.TemporaryDirectory(prefix="c11d_frame_program_region_lock_") as temp:
        temp_root = Path(temp)
        for rel in (CONTRACT_REL, OUTPUT_SCHEMA_REL, LOGICAL_CONTRACT_REL, LOGICAL_SCHEMA_REL):
            destination = temp_root / rel
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / rel, destination)
        target = temp_root / CONTRACT_REL
        contract_doc = json.loads(target.read_text(encoding="utf-8"))
        contract_doc["region_definitions"]["HEADER"]["geometry_state"] = "PIXELS_ASSIGNED"
        target.write_text(json.dumps(contract_doc, indent=2), encoding="utf-8")
        _must_reject("region geometry self-promotion", lambda: _load_contract(temp_root)); negative += 1

    assert positive == 3, positive
    assert deterministic == 3, deterministic
    assert flow == 3, flow
    assert negative == 19, negative
    return {"content_types":positive,"deterministic":deterministic,"editorial_flow":flow,"negative":negative,"schema":schema_checks,"jsonschema":full_schema_checks}


def main() -> int:
    counts = run_checks()
    schema_label = f"schema={counts['schema']}/3"
    full_schema = f"jsonschema={counts['jsonschema']}/3" if counts['jsonschema'] else "jsonschema=NOT_INSTALLED (strict structural checks PASS)"
    print(
        "C11-D RENDERER-NEUTRAL FRAME PROGRAM PASS | "
        f"content_types={counts['content_types']}/3 | deterministic={counts['deterministic']}/3 | "
        f"editorial_flow={counts['editorial_flow']}/3 | negative={counts['negative']}/19 | {schema_label} | {full_schema} | "
        "renderer_input=NOT_EMITTED | frame_schedule=NOT_DEFINED | pixel_coordinates=NOT_EMITTED | "
        "renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
