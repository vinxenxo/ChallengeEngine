"""Focused acceptance/regression tests for the in-memory D logical composition plan."""
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
from d_renderer_logical_composition import (
    CONTRACT_REL,
    OUTPUT_SCHEMA_REL,
    BINDING_CONTRACT_REL,
    DRendererLogicalCompositionError,
    PLAN_SCHEMA,
    PLAN_STATUS,
    build_logical_composition_plan,
    validate_logical_composition_plan,
    _load_contract,
)
from test_d_renderer_candidate import _envelope, _must_reject, _representative_selections, _reseal_adapter


def _reseal_plan(plan: dict[str, Any]) -> dict[str, Any]:
    plan["composition_sha256"] = sha256_json({key: value for key, value in plan.items() if key != "composition_sha256"})
    return plan


def _fixture(content_type: str, request_id: str, *, title: str = "Composition title", seed: int = 12345, music_seed: int = 840001):
    selection = _representative_selections()[content_type]
    envelope = _envelope(selection, request_id, title=title, seed=seed, music_seed=music_seed)
    preview = build_renderer_binding_preview(envelope, ROOT)
    plan = build_logical_composition_plan(preview, envelope, ROOT)
    return envelope, preview, plan


def _must_reject(label: str, action: Callable[[], Any]) -> None:
    try:
        action()
    except (DRendererLogicalCompositionError, ValueError, TypeError, KeyError):
        return
    raise AssertionError(f"Expected fail-closed rejection: {label}")


def run_checks() -> dict[str, int]:
    # The candidate implementation must remain pure/in-memory and may not dispatch.
    tree = ast.parse((HERE / "d_renderer_logical_composition.py").read_text(encoding="utf-8"))
    forbidden_modules = {"subprocess", "ffmpeg", "godot", "os", "shutil", "socket", "multiprocessing"}
    forbidden_calls = {"write_text", "write_bytes", "open", "Popen", "system", "startfile", "run", "call", "check_call", "check_output"}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            assert not any(alias.name.split(".")[0] in forbidden_modules for alias in node.names), "Logical composition must not import process/filesystem-dispatch modules"
        elif isinstance(node, ast.ImportFrom):
            assert (node.module or "").split(".")[0] not in forbidden_modules, "Logical composition must not import process/filesystem-dispatch modules"
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            assert node.func.attr not in forbidden_calls, f"Forbidden execution/persistence call: {node.func.attr}"

    schema_doc = json.loads((ROOT / OUTPUT_SCHEMA_REL).read_text(encoding="utf-8"))
    assert schema_doc.get("$schema") == "https://json-schema.org/draft/2020-12/schema"
    assert schema_doc.get("$id") == "urn:c11d:renderer-candidate-logical-composition:v1"
    assert schema_doc.get("additionalProperties") is False
    schema_checked = 0
    full_schema_checked = 0
    nested_objects = ("contract_identity", "implementation_identity", "source_identity", "content_identity", "canvas_target", "localization", "seed_isolation", "truth_and_telemetry", "execution_boundary")
    for object_name in nested_objects:
        object_schema = schema_doc["properties"][object_name]
        assert object_schema.get("type") == "object" and object_schema.get("additionalProperties") is False, object_name
        assert set(object_schema.get("required", [])) == set(object_schema.get("properties", {})), object_name
    element_schema = schema_doc["properties"]["text_elements"]["items"]
    assert element_schema.get("additionalProperties") is False
    assert set(element_schema.get("required", [])) == set(element_schema.get("properties", {}))
    assert set(schema_doc.get("required", [])) == set(schema_doc.get("properties", {}))
    try:
        import jsonschema  # type: ignore[import-not-found]
    except ImportError:
        jsonschema = None
    if jsonschema is not None:
        jsonschema.Draft202012Validator.check_schema(schema_doc)

    positive = 0
    deterministic = 0
    editorial_flow = 0
    fixtures: dict[str, tuple[dict[str, Any], dict[str, Any], dict[str, Any]]] = {}
    expected_visible_counts = {"challenges": 5, "visual_loops": 3, "visual_drills": 3}
    for content_type in ("challenges", "visual_loops", "visual_drills"):
        envelope, preview, plan = _fixture(content_type, f"D-LOGICAL-COMPOSITION-{content_type.upper()}")
        repeated = build_logical_composition_plan(copy.deepcopy(preview), copy.deepcopy(envelope), ROOT)
        assert plan == repeated, f"non-deterministic plan for {content_type}"
        assert plan["schema"] == PLAN_SCHEMA
        assert plan["status"] == PLAN_STATUS
        assert plan["content_identity"]["content_type"] == content_type
        assert plan["source_identity"]["binding_preview_sha256"] == preview["preview_sha256"]
        assert plan["canvas_target"]["width"] == 720 and plan["canvas_target"]["height"] == 1280
        assert plan["canvas_target"]["canvas_semantics"] == "DELIVERY_TARGET_ONLY_NOT_CAPTURE_OR_RENDER_AUTHORIZATION"
        assert plan["truth_and_telemetry"] == {"simulation_truth": "NOT_BOUND", "derived_telemetry": "NOT_BOUND"}
        assert len(plan["text_elements"]) == expected_visible_counts[content_type]
        assert validate_logical_composition_plan(plan, preview, envelope, ROOT) is True
        assert all(element["language"] == plan["localization"]["locale"] for element in plan["text_elements"])
        assert all(element["content_binding"] == "DIRECT_CANONICAL_EDITORIAL_VALUE" for element in plan["text_elements"])
        assert all(element["target_mapping_state"] == "PROPOSED_NOT_APPROVED" for element in plan["text_elements"])
        boundary = plan["execution_boundary"]
        assert boundary == {
            "composition_mode": "IN_MEMORY_SEMANTIC_REVIEW_ONLY",
            "renderer_input_emitted": False,
            "renderer_dispatch_invoked": False,
            "renderer_activation": False,
            "production_execution": False,
            "media_output_created": False,
            "output_artifact_path": None,
            "d4_8": "BLOCKED",
            "release_authority": "NONE",
            "c11c_source_mutation": False,
        }
        # Each intended visible property must carry the exact, canonical editorial value.
        source_values = {item["source_field"]: item["value"] for item in preview["editorial_binding_preview"]}
        element_values = {item["source_field"]: item["text_value"] for item in plan["text_elements"]}
        expected_values = {key: value for key, value in source_values.items() if key != "language"}
        assert element_values == expected_values
        assert all(item["text_sha256"] == sha256_json(item["text_value"]) for item in plan["text_elements"])
        assert set(plan) == set(schema_doc["required"])
        schema_checked += 1
        if jsonschema is not None:
            jsonschema.Draft202012Validator(schema_doc).validate(plan)
            full_schema_checked += 1
        fixtures[content_type] = (envelope, preview, plan)
        positive += 1
        deterministic += 1
        editorial_flow += 1

    # A real title edit must change the intended element value, not only provenance metadata.
    loop_selection = _representative_selections()["visual_loops"]
    base_envelope = _envelope(loop_selection, "D-LOGICAL-EDITORIAL-DELTA", title="Editorial A")
    changed_envelope = _envelope(loop_selection, "D-LOGICAL-EDITORIAL-DELTA", title="Editorial B")
    base_preview = build_renderer_binding_preview(base_envelope, ROOT)
    changed_preview = build_renderer_binding_preview(changed_envelope, ROOT)
    base_plan = build_logical_composition_plan(base_preview, base_envelope, ROOT)
    changed_plan = build_logical_composition_plan(changed_preview, changed_envelope, ROOT)
    base_title = next(item for item in base_plan["text_elements"] if item["source_field"] == "title")
    changed_title = next(item for item in changed_plan["text_elements"] if item["source_field"] == "title")
    assert base_title["text_value"] == "Editorial A"
    assert changed_title["text_value"] == "Editorial B"
    assert base_title["text_sha256"] != changed_title["text_sha256"]
    assert base_plan["composition_sha256"] != changed_plan["composition_sha256"]
    assert base_plan["seed_isolation"] == changed_plan["seed_isolation"]

    # Changing only music seed does not change editorial composition elements.
    music_envelope, music_preview, music_plan = _fixture("visual_loops", "D-LOGICAL-MUSIC-SEED", seed=12345, music_seed=840002)
    assert music_plan["text_elements"] == fixtures["visual_loops"][2]["text_elements"]
    assert music_plan["seed_isolation"]["cross_domain_seed_sharing"] == "FORBIDDEN"
    assert music_plan["seed_isolation"]["scene_elements_seed_derived"] is False

    negative = 0
    original_envelope, original_preview, original_plan = fixtures["visual_loops"]

    tamper_text = copy.deepcopy(original_plan)
    next(item for item in tamper_text["text_elements"] if item["source_field"] == "title")["text_value"] = "Forged text"
    _reseal_plan(tamper_text)
    _must_reject("tampered element value even when self-hash resealed", lambda: validate_logical_composition_plan(tamper_text, original_preview, original_envelope, ROOT)); negative += 1

    approved_mapping = copy.deepcopy(original_plan)
    approved_mapping["text_elements"][0]["target_mapping_state"] = "APPROVED"
    _reseal_plan(approved_mapping)
    _must_reject("candidate mapping cannot self-promote to approved", lambda: validate_logical_composition_plan(approved_mapping, original_preview, original_envelope, ROOT)); negative += 1

    activated = copy.deepcopy(original_plan)
    activated["execution_boundary"]["renderer_activation"] = True
    _reseal_plan(activated)
    _must_reject("renderer activation escalation", lambda: validate_logical_composition_plan(activated, original_preview, original_envelope, ROOT)); negative += 1

    emitted = copy.deepcopy(original_plan)
    emitted["execution_boundary"]["renderer_input_emitted"] = True
    _reseal_plan(emitted)
    _must_reject("renderer-native input claim", lambda: validate_logical_composition_plan(emitted, original_preview, original_envelope, ROOT)); negative += 1

    media = copy.deepcopy(original_plan)
    media["execution_boundary"]["media_output_created"] = True
    _reseal_plan(media)
    _must_reject("media output escalation", lambda: validate_logical_composition_plan(media, original_preview, original_envelope, ROOT)); negative += 1

    release = copy.deepcopy(original_plan)
    release["execution_boundary"]["release_authority"] = "APPROVED"
    _reseal_plan(release)
    _must_reject("release authority escalation", lambda: validate_logical_composition_plan(release, original_preview, original_envelope, ROOT)); negative += 1

    unknown_top = copy.deepcopy(original_plan)
    unknown_top["uncontracted_dispatch"] = True
    _reseal_plan(unknown_top)
    _must_reject("unknown top-level property", lambda: validate_logical_composition_plan(unknown_top, original_preview, original_envelope, ROOT)); negative += 1

    bad_hash = copy.deepcopy(original_plan)
    bad_hash["composition_sha256"] = "0" * 64
    _must_reject("composition hash tamper", lambda: validate_logical_composition_plan(bad_hash, original_preview, original_envelope, ROOT)); negative += 1

    wrong_source = _envelope(_representative_selections()["visual_loops"], "D-LOGICAL-WRONG-SOURCE", title="Different source")
    _must_reject("plan bound to a different adapter source", lambda: validate_logical_composition_plan(original_plan, original_preview, wrong_source, ROOT)); negative += 1

    element_removed = copy.deepcopy(original_plan)
    element_removed["text_elements"].pop()
    _reseal_plan(element_removed)
    _must_reject("missing text element", lambda: validate_logical_composition_plan(element_removed, original_preview, original_envelope, ROOT)); negative += 1

    element_duplicated = copy.deepcopy(original_plan)
    element_duplicated["text_elements"].append(copy.deepcopy(element_duplicated["text_elements"][0]))
    _reseal_plan(element_duplicated)
    _must_reject("duplicate text element", lambda: validate_logical_composition_plan(element_duplicated, original_preview, original_envelope, ROOT)); negative += 1

    localization = copy.deepcopy(original_plan)
    localization["localization"]["locale"] = "zz"
    _reseal_plan(localization)
    _must_reject("localization source mismatch", lambda: validate_logical_composition_plan(localization, original_preview, original_envelope, ROOT)); negative += 1

    slot_changed = copy.deepcopy(original_plan)
    slot_changed["text_elements"][0]["source_preview_slot_id"] = "unauthorized.slot"
    _reseal_plan(slot_changed)
    _must_reject("unknown source preview slot", lambda: validate_logical_composition_plan(slot_changed, original_preview, original_envelope, ROOT)); negative += 1

    tampered_envelope = copy.deepcopy(original_envelope)
    tampered_envelope["binding_preview"]["editorial_bindings"]["title"] = "Envelope forgery"
    # Deliberately do not reseal: the upstream adapter validator must catch this.
    _must_reject("tampered source envelope", lambda: build_logical_composition_plan(original_preview, tampered_envelope, ROOT)); negative += 1

    unknown = copy.deepcopy(original_envelope)
    unknown["content_identity"]["content_type"] = "longform"
    _reseal_adapter(unknown)
    _must_reject("unsupported Longform", lambda: build_renderer_binding_preview(unknown, ROOT)); negative += 1

    # Candidate contract cannot self-approve. Copy only contract dependencies to an isolated root.
    with tempfile.TemporaryDirectory(prefix="c11d_logical_comp_contract_lock_") as temp_dir:
        temp_root = Path(temp_dir)
        for rel in (CONTRACT_REL, OUTPUT_SCHEMA_REL, BINDING_CONTRACT_REL):
            dest = temp_root / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / rel, dest)
        contract_path = temp_root / CONTRACT_REL
        doc = json.loads(contract_path.read_text(encoding="utf-8"))
        doc["approval_state"]["renderer_baseline_approved"] = True
        contract_path.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
        _must_reject("composition contract self-approval", lambda: _load_contract(temp_root)); negative += 1

    with tempfile.TemporaryDirectory(prefix="c11d_logical_comp_target_tamper_") as temp_dir:
        temp_root = Path(temp_dir)
        for rel in (CONTRACT_REL, OUTPUT_SCHEMA_REL, BINDING_CONTRACT_REL):
            dest = temp_root / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / rel, dest)
        contract_path = temp_root / CONTRACT_REL
        doc = json.loads(contract_path.read_text(encoding="utf-8"))
        doc["field_targets"]["title"]["target_region"] = "FOOTER"
        contract_path.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
        _must_reject("unreviewed semantic target mutation", lambda: _load_contract(temp_root)); negative += 1

    assert positive == 3, positive
    assert deterministic == 3, deterministic
    assert editorial_flow == 3, editorial_flow
    assert negative == 17, negative
    return {"content_types": positive, "determinism": deterministic, "editorial_flow": editorial_flow, "negative": negative, "schema": schema_checked, "jsonschema": full_schema_checked}


def main() -> int:
    counts = run_checks()
    schema_label = f"schema={counts['schema']}/3"
    full_schema_label = f"jsonschema={counts['jsonschema']}/3" if counts["jsonschema"] else "jsonschema=NOT_INSTALLED (strict structural checks PASS)"
    print(
        "C11-D RENDERER CANDIDATE LOGICAL COMPOSITION PASS | "
        f"content_types={counts['content_types']}/3 | deterministic={counts['determinism']}/3 | "
        f"editorial_flow={counts['editorial_flow']}/3 | negative={counts['negative']}/17 | {schema_label} | {full_schema_label} | "
        "renderer_input=NOT_EMITTED | renderer=OFF | media_created=false | "
        "D4.8=BLOCKED | release_authority=NONE"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
