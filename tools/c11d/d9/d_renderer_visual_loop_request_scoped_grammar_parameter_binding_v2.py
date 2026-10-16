"""Preparation-only request-bound grammar parameter matrix V2; stdout-only, no renderer/media."""
from __future__ import annotations
import argparse, base64, copy, hashlib, importlib.util, json, math, re, subprocess, sys
from pathlib import Path
from typing import Any, Callable, Mapping
try:
    from jsonschema import Draft202012Validator
except ImportError as exc:
    raise RuntimeError("jsonschema is required for the request-scoped grammar parameter matrix contract") from exc

CONTRACT_REL = Path("definitions/c11d/production/D_RENDERER_VISUAL_LOOP_REQUEST_SCOPED_GRAMMAR_PARAMETER_BINDING_V2.json")
CONTRACT_SCHEMA_REL = Path("definitions/c11d/production/D_RENDERER_VISUAL_LOOP_REQUEST_SCOPED_GRAMMAR_PARAMETER_BINDING_SCHEMA_V2.json")
INPUT_SCHEMA_REL = Path("definitions/c11d/production/D_RENDERER_VISUAL_LOOP_REQUEST_SCOPED_GRAMMAR_PARAMETER_INPUT_SCHEMA_V2.json")
REPORT_SCHEMA_REL = Path("definitions/c11d/production/D_RENDERER_VISUAL_LOOP_REQUEST_SCOPED_GRAMMAR_PARAMETER_REPORT_SCHEMA_V2.json")
RUNNER_REL = Path("tools/c11d/d9/d_renderer_visual_loop_request_scoped_grammar_parameter_binding_v2.py")
HARNESS_REL = Path("tools/c11d/d9/materialize_visual_loop_grammar_parameter_matrix_v2_in_memory.gd")
MANIFEST_REL = Path("release/C11C_FREEZE_PACKAGE_MANIFEST.json")
EXPECTED_MANIFEST = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
EXPECTED_GODOT_VERSION = "4.7.1.stable.mono.official.a13da4feb"
PROBE_PREFIX = "C11D_VISUAL_LOOP_GRAMMAR_PARAMETER_MATRIX_V2_PROBE="
REPORT_PREFIX = "C11D_VISUAL_LOOP_REQUEST_SCOPED_GRAMMAR_PARAMETER_BINDING_V2_REPORT="
STATUS = "PREPARATION_ONLY_REQUEST_BOUND_GRAMMAR_PARAMETER_INSTANCES_5_OF_5_NOT_EXACT_VISUAL_PAYLOAD_NOT_APPROVED"
GRAMMARS = (
    ("harmonic_membrane", 0, "field_harmonic_membrane"),
    ("interference_plane", 1, "field_interference_plane"),
    ("parametric_ribbon", 2, "field_parametric_ribbon"),
    ("lattice_wave", 3, "field_lattice_wave"),
    ("orbital_wave", 4, "field_orbital_wave"),
)
STYLE_KEYS = ("grammar_mode", "palette_mode", "morph", "wave_frequency", "line_width", "glow_strength", "polygon_sides", "wave_ratio", "shape_rotation", "layer_spread", "radial_wave_amplitude", "liss_x_frequency", "liss_y_frequency", "interference_scale", "hero_scale", "perspective_strength", "depth_strength", "secondary_phase", "color_phase", "stroke_scale")
BOUNDARY = {
    "request_input_persisted": False,
    "parameter_payload_files_written": False,
    "receipt_files_written": False,
    "renderer_instance_created": False,
    "renderer_native_input_emitted": False,
    "renderer_dispatch_invoked": False,
    "shader_executed": False,
    "media_created": False,
    "c11c_source_mutation": False,
    "candidate_input_admissible": False,
    "renderer": "OFF",
    "D4.8": "BLOCKED",
    "D9.10": "PREPARE_ONLY",
    "release_authority": "NONE",
    "D9.17": "BLOCKED_NO_GO",
    "D10": "BLOCKED",
}
PROBE_BOUNDARY = {
    "request_input_persisted": False,
    "parameter_payload_files_written": False,
    "receipt_files_written": False,
    "renderer_instance_created": False,
    "renderer_native_input_emitted": False,
    "renderer_dispatch_invoked": False,
    "shader_executed": False,
    "media_created": False,
    "c11c_source_mutation": False,
    "candidate_input_admissible": False,
    "renderer": "OFF",
    "d4_8": "BLOCKED",
    "release_authority": "NONE",
    "d9_17": "BLOCKED_NO_GO",
    "d10": "BLOCKED",
}

class GrammarParameterBindingError(ValueError):
    pass

def canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)

def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()

def file_sha(path: Path) -> str:
    if not path.is_file():
        raise GrammarParameterBindingError(f"Missing pinned source: {path}")
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def read_json(root: Path, rel: str | Path) -> dict[str, Any]:
    try:
        value = json.loads((root / rel).read_text(encoding="utf-8-sig"))
    except Exception as exc:
        raise GrammarParameterBindingError(f"Cannot read JSON source {rel}: {exc}") from exc
    if not isinstance(value, dict):
        raise GrammarParameterBindingError(f"Expected JSON object at {rel}")
    return value

def _root(value=None) -> Path:
    return Path(value).resolve() if value is not None else Path(__file__).resolve().parents[3]

def _load_module(path: Path, name: str):
    if not path.is_file():
        raise GrammarParameterBindingError(f"Missing parent implementation: {path}")
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise GrammarParameterBindingError(f"Cannot load parent implementation: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    sibling = str(path.parent)
    if sibling in sys.path:
        sys.path.remove(sibling)
    sys.path.insert(0, sibling)
    spec.loader.exec_module(module)
    return module

def _load_contract(root: Path):
    contract = read_json(root, CONTRACT_REL)
    schema = read_json(root, CONTRACT_SCHEMA_REL)
    input_schema = read_json(root, INPUT_SCHEMA_REL)
    report_schema = read_json(root, REPORT_SCHEMA_REL)
    for item in (schema, input_schema, report_schema):
        if item.get("$schema") != "https://json-schema.org/draft/2020-12/schema" or item.get("additionalProperties") is not False:
            raise GrammarParameterBindingError("All schemas must be strict JSON Schema Draft 2020-12")
        Draft202012Validator.check_schema(item)
    try:
        Draft202012Validator(schema).validate(contract)
    except Exception as exc:
        raise GrammarParameterBindingError(f"Contract schema rejected V2: {getattr(exc, 'message', str(exc))}") from exc
    if contract.get("schema") != "C11-D-D9-VISUAL-LOOP-REQUEST-SCOPED-GRAMMAR-PARAMETER-BINDING-CONTRACT-V2" or contract.get("schema_version") != "2.0":
        raise GrammarParameterBindingError("Contract identity/version mismatch")
    if contract.get("status") != STATUS:
        raise GrammarParameterBindingError("Contract tried to self-promote")
    if file_sha(root / MANIFEST_REL) != EXPECTED_MANIFEST or contract.get("authority", {}).get("frozen_c11c_manifest_sha256") != EXPECTED_MANIFEST:
        raise GrammarParameterBindingError("Frozen C11-C manifest mismatch")
    authority = contract.get("authority", {})
    for path_key, sha_key in (("parent_binding_matrix_contract_path", "parent_binding_matrix_contract_sha256"), ("parent_reference_carrier_contract_path", "parent_reference_carrier_contract_sha256")):
        if not isinstance(authority.get(path_key), str) or authority.get(sha_key) != file_sha(root / authority[path_key]):
            raise GrammarParameterBindingError(f"Parent contract hash mismatch: {path_key}")
    scope = contract.get("scope", {})
    observed = [(row.get("grammar_id"), row.get("grammar_index"), row.get("shader_branch")) for row in scope.get("grammar_matrix", [])]
    if tuple(observed) != GRAMMARS:
        raise GrammarParameterBindingError("Five-grammar order/identity mismatch")
    if scope.get("exact_selector_visual_payload_materialized") is not False or scope.get("parameter_instance_scope") != "REQUEST_BOUND_IN_MEMORY_STYLE_PARAMETERS_ONLY":
        raise GrammarParameterBindingError("Contract crossed the explicit parameter-only scope boundary")
    if contract.get("reference_boundary", {}).get("policy_values_consumed") is not False or contract.get("reference_boundary", {}).get("policy_reference_count_per_selector") != 9:
        raise GrammarParameterBindingError("Timing/review policy metadata boundary changed")
    approval = contract.get("approval_state", {})
    if approval.get("approval_assertions_checked") != 19 or approval.get("approvals_granted") != 0:
        raise GrammarParameterBindingError("Policy approval count is not locked at 0/19")
    for flag, value in approval.items():
        if flag.endswith("_approved") or flag.endswith("_authorized") or flag in {"candidate_io_contract_complete", "renderer_baseline_frozen"}:
            if value is not False:
                raise GrammarParameterBindingError(f"Approval gate unexpectedly promoted: {flag}")
    if approval.get("release_authority") != "NONE":
        raise GrammarParameterBindingError("Release authority must remain NONE")
    if contract.get("execution_boundary") != BOUNDARY:
        raise GrammarParameterBindingError("Execution/governance boundary changed")
    harness_record = contract.get("harness", {})
    if harness_record.get("path") != HARNESS_REL.as_posix() or harness_record.get("sha256") != file_sha(root / HARNESS_REL):
        raise GrammarParameterBindingError("Godot harness path/hash does not match the pinned contract")

    pins = contract.get("source_lineage")
    if not isinstance(pins, list) or len(pins) < 40 or pins[0].get("path") != MANIFEST_REL.as_posix() or pins[0].get("sha256") != EXPECTED_MANIFEST:
        raise GrammarParameterBindingError("Incomplete direct source lineage; frozen C11-C manifest must be first")
    seen = set()
    for index, row in enumerate(pins):
        if not isinstance(row, dict) or set(row) != {"path", "sha256"}:
            raise GrammarParameterBindingError("Malformed source lineage row")
        rel, expected = row["path"], row["sha256"]
        p = Path(rel)
        if not isinstance(rel, str) or p.is_absolute() or ".." in p.parts or "\\" in rel or rel in seen:
            raise GrammarParameterBindingError(f"Unsafe/duplicate source pin: {rel!r}")
        if not isinstance(expected, str) or re.fullmatch(r"[0-9a-f]{64}", expected) is None:
            raise GrammarParameterBindingError(f"Malformed source pin hash: {rel}")
        actual = file_sha(root / rel)
        if actual != expected:
            raise GrammarParameterBindingError(f"Pinned source drift: {rel}; expected={expected}; actual={actual}")
        if index > 1 and rel <= pins[index - 1]["path"]:
            raise GrammarParameterBindingError("Source pins after frozen manifest must be lexicographically ordered")
        seen.add(rel)
    # Source-lineage closure must include every V2 parent source pin, unchanged.
    parent_matrix_contract = read_json(root, "definitions/c11d/production/D_RENDERER_VISUAL_LOOP_REQUEST_SCOPED_BINDING_MATRIX_V2.json")
    parent_paths = {row["path"]: row["sha256"] for row in parent_matrix_contract.get("source_lineage", [])}
    local_paths = {row["path"]: row["sha256"] for row in pins}
    for rel, expected in parent_paths.items():
        if local_paths.get(rel) != expected:
            raise GrammarParameterBindingError(f"Parent matrix source pin was omitted or altered: {rel}")
    return contract, schema, input_schema, report_schema, pins

def _build_parent_chain(root: Path, grammar: str, matrix_mod, binder, carrier_report: Mapping[str, Any]):
    result, bridge, envelope = matrix_mod._request_for_grammar(root, grammar)
    request = result.get("canonical_request", {})
    plan = result.get("plan", {})
    if result.get("status") != "PLANNED":
        raise GrammarParameterBindingError(f"Canonical D9.9 request not PLANNED for {grammar}")
    selection = plan.get("selection", {})
    if selection.get("subtype_id") != grammar or selection.get("family_id") != "c11c_geometric_waves_v1" or selection.get("content_type") != "visual_loops" or selection.get("variant_id") is not None:
        raise GrammarParameterBindingError(f"Canonical request selector drift for {grammar}")
    relation = next((x for x in carrier_report.get("relations", []) if x.get("selector", {}).get("grammar_id") == grammar), None)
    if not isinstance(relation, Mapping):
        raise GrammarParameterBindingError(f"Missing request-bound reference relation for {grammar}")
    identity = relation.get("request_identity", {})
    if identity.get("request_id") != request.get("request_id") or identity.get("request_hash") != result.get("request_hash") or identity.get("plan_hash") != result.get("plan_hash"):
        raise GrammarParameterBindingError(f"Request/plan identity differs from reference carrier for {grammar}")
    ref = relation.get("reference_identity", {})
    if ref.get("reference_count") != 9 or relation.get("locks", {}).get("policy_values_consumed") is not False or relation.get("locks", {}).get("candidate_input_admissible") is not False:
        raise GrammarParameterBindingError(f"Reference or admission boundary changed for {grammar}")
    # Same narrow in-memory family matrix already used by the preparation V2 audit;
    # the returned record remains family-source resolution, never a grammar payload.
    v1_contract, v1_schema, v1_lineage = binder._load_contract(root)
    extended = copy.deepcopy(v1_contract)
    extended["representative_source_matrix"]["visual_loops"] = {
        "required_selection": {"content_type": "visual_loops", "family_id": "c11c_geometric_waves_v1"},
        "payload_source_path": "definitions/visual_loop_geometric_canonical.json",
    }
    source_binding = binder._build_core(result, bridge, envelope, root, extended, v1_schema, v1_lineage, False)
    if source_binding.get("readiness", {}).get("request_scoped_visual_payload_instance_bound") is not False or source_binding.get("readiness", {}).get("video_render_ready") is not False:
        raise GrammarParameterBindingError(f"Parent source binding escalated readiness for {grammar}")

    canonical_selection = {
        "content_type": selection["content_type"],
        "family_id": selection["family_id"],
        "subtype_id": selection["subtype_id"],
        "variant_id": selection.get("variant_id"),
    }
    request_input = {
        "schema": "C11-D-D9-DYNAMIC-REQUEST-PAYLOAD-INPUT-V1",
        "schema_version": "1.0",
        "request_id": request["request_id"],
        "request_hash": result["request_hash"],
        "selection": canonical_selection,
        "seed": request["seed"],
        "music_seed": request["music_seed"],
        "variation_index": request["variation_index"],
        "presentation_profile_id": request["presentation_profile_id"],
        "delivery_profile_id": request["delivery_profile_id"],
    }
    canonical_chain = {
        "plan_hash": result["plan_hash"],
        "editorial_hash": result["editorial_hash"],
        "bridge_record_hash": bridge["record_hash"],
        "adapter_envelope_hash": envelope["envelope_hash"],
        "source_binding_sha256": source_binding["binding_sha256"],
    }
    timing_review = {
        "carrier_report_sha256": carrier_report["report_sha256"],
        "selector_envelope_sha256": ref["selector_envelope_sha256"],
        "shared_policy_reference_set_sha256": ref["shared_reference_set_sha256"],
        "policy_reference_count": int(ref["reference_count"]),
        "policy_values_consumed": False,
    }
    return result, request_input, canonical_chain, timing_review

def _build_input(root: Path, contract: Mapping[str, Any], input_schema: Mapping[str, Any], request_input: Mapping[str, Any], canonical_chain: Mapping[str, Any], timing_review: Mapping[str, Any]) -> dict[str, Any]:
    value = {
        "schema": "C11-D-D9-VISUAL-LOOP-GRAMMAR-PARAMETER-MATRIX-INPUT-V2",
        "schema_version": "2.0",
        "contract_sha256": file_sha(root / CONTRACT_REL),
        "frozen_c11c_manifest_sha256": EXPECTED_MANIFEST,
        "request": dict(request_input),
        "canonical_chain": dict(canonical_chain),
        "timing_review_reference": dict(timing_review),
    }
    try:
        Draft202012Validator(input_schema).validate(value)
    except Exception as exc:
        raise GrammarParameterBindingError(f"Strict probe input schema rejected input: {getattr(exc, 'message', str(exc))}") from exc
    return value

def _validate_probe(report: Mapping[str, Any], probe_input: Mapping[str, Any], contract: Mapping[str, Any]) -> dict[str, Any]:
    if not isinstance(report, Mapping):
        raise GrammarParameterBindingError("Godot probe receipt must be an object")
    request = probe_input["request"]
    selection = request["selection"]
    grammar = selection["subtype_id"]
    row = next((x for x in contract["scope"]["grammar_matrix"] if x["grammar_id"] == grammar), None)
    if row is None:
        raise GrammarParameterBindingError("Receipt selector is outside the exact five-grammar matrix")
    expected = {
        "schema": "C11-D-D9-VISUAL-LOOP-GRAMMAR-PARAMETER-MATRIX-PROBE-V2",
        "schema_version": "2.0",
        "status": "PREPARATION_ONLY_REQUEST_BOUND_GRAMMAR_PARAMETER_INSTANCE_IN_MEMORY_NOT_EXACT_VISUAL_PAYLOAD",
        "contract_sha256": probe_input["contract_sha256"],
        "request_id": request["request_id"],
        "request_hash": request["request_hash"],
        "selection": selection,
        "gameplay_seed": request["seed"],
        "music_seed": request["music_seed"],
        "variation_index": request["variation_index"],
        "presentation_profile_id": request["presentation_profile_id"],
        "delivery_profile_id": request["delivery_profile_id"],
        "canonical_chain": probe_input["canonical_chain"],
        "timing_review_reference": probe_input["timing_review_reference"],
        "repeat_deterministic": True,
        "source_checks_passed": True,
        **PROBE_BOUNDARY,
    }
    for key, value in expected.items():
        if report.get(key) != value:
            raise GrammarParameterBindingError(f"Godot probe receipt mismatch at {key}: expected={value!r}, actual={report.get(key)!r}")
    if set(report) != set(expected) | {"parameter_instance"}:
        raise GrammarParameterBindingError("Godot probe receipt has unknown or missing keys")
    instance = report.get("parameter_instance")
    if not isinstance(instance, Mapping):
        raise GrammarParameterBindingError("parameter_instance must be an object")
    required_instance_keys = {
        "schema", "schema_version", "selection", "grammar_id", "grammar_index", "shader_branch", "shader_uniform",
        "style_parameter_count", "style_parameters", "gameplay_seed", "request_hash", "style_parameters_sha256", "parameter_instance_sha256",
    }
    if set(instance) != required_instance_keys:
        raise GrammarParameterBindingError("Parameter instance key set mismatch")
    if instance.get("schema") != "C11-D-D9-VISUAL-LOOP-GRAMMAR-PARAMETER-INSTANCE-V2" or instance.get("schema_version") != "2.0":
        raise GrammarParameterBindingError("Parameter instance contract identity mismatch")
    if instance.get("selection") != selection or instance.get("grammar_id") != grammar or instance.get("grammar_index") != row["grammar_index"] or instance.get("shader_branch") != row["shader_branch"] or instance.get("shader_uniform") != "grammar_mode":
        raise GrammarParameterBindingError("Parameter instance does not match exact grammar/branch/index mapping")
    if instance.get("gameplay_seed") != request["seed"] or instance.get("request_hash") != request["request_hash"] or instance.get("style_parameter_count") != 20:
        raise GrammarParameterBindingError("Parameter instance is detached from request identity/seed or style count")
    style = instance.get("style_parameters")
    if not isinstance(style, Mapping) or set(style) != set(STYLE_KEYS) or len(style) != 20:
        raise GrammarParameterBindingError("Style parameter projection must contain exactly 20 named values")
    for key, value in style.items():
        if isinstance(value, bool) or not isinstance(value, (float, int)) or not math.isfinite(float(value)):
            raise GrammarParameterBindingError(f"Style value is not a finite numeric value: {key}")
    if style.get("grammar_mode") != row["grammar_index"]:
        raise GrammarParameterBindingError("Projected grammar_mode differs from selected grammar index")
    if not isinstance(instance.get("style_parameters_sha256"), str) or digest(style) != instance["style_parameters_sha256"]:
        raise GrammarParameterBindingError("Style parameter hash mismatch")
    instance_core = {key: value for key, value in instance.items() if key not in {"style_parameters_sha256", "parameter_instance_sha256"}}
    if not isinstance(instance.get("parameter_instance_sha256"), str) or digest(instance_core) != instance["parameter_instance_sha256"]:
        raise GrammarParameterBindingError("Parameter-instance hash mismatch")
    return dict(report)

def _run_one(root: Path, godot: str, timeout: float, contract: Mapping[str, Any], input_schema: Mapping[str, Any], request_input: Mapping[str, Any], canonical_chain: Mapping[str, Any], timing_review: Mapping[str, Any], process_runner: Callable[..., Any]) -> dict[str, Any]:
    probe_input = _build_input(root, contract, input_schema, request_input, canonical_chain, timing_review)
    encoded = base64.b64encode(canonical(probe_input).encode("utf-8")).decode("ascii")
    command = [godot, "--headless", "--path", str(root), "--script", "res://" + HARNESS_REL.as_posix(), "--", encoded]
    try:
        completed = process_runner(command, cwd=str(root), text=True, capture_output=True, timeout=timeout, check=False)
    except Exception as exc:
        raise GrammarParameterBindingError(f"Godot probe invocation failed for {request_input['selection']['subtype_id']}: {exc}") from exc
    stdout = str(getattr(completed, "stdout", "") or "")
    stderr = str(getattr(completed, "stderr", "") or "")
    combined = stdout + "\n" + stderr
    code = int(getattr(completed, "returncode", -1))
    if code != 0 or "SCRIPT ERROR:" in combined or "ERROR:" in combined or "VISUAL LOOP GRAMMAR PARAMETER MATRIX V2 PROBE FAIL" in combined:
        raise GrammarParameterBindingError(f"Godot probe failed for {request_input['selection']['subtype_id']} (exit={code}): {combined[-4500:]}")
    rows = [line[len(PROBE_PREFIX):] for line in combined.splitlines() if line.startswith(PROBE_PREFIX)]
    if len(rows) != 1:
        raise GrammarParameterBindingError(f"Expected one probe receipt for {request_input['selection']['subtype_id']}; got {len(rows)}")
    try:
        report = json.loads(rows[0])
    except json.JSONDecodeError as exc:
        raise GrammarParameterBindingError("Godot probe receipt is invalid JSON") from exc
    if not isinstance(report, dict):
        raise GrammarParameterBindingError("Godot probe receipt root must be an object")
    return _validate_probe(report, probe_input, contract)

def _case_receipt(probe: Mapping[str, Any], canonical_chain: Mapping[str, Any], timing_review: Mapping[str, Any]) -> dict[str, Any]:
    req = {
        "request_id": probe["request_id"], "request_hash": probe["request_hash"], "selection": probe["selection"],
        "gameplay_seed": probe["gameplay_seed"], "music_seed": probe["music_seed"], "variation_index": probe["variation_index"],
        "presentation_profile_id": probe["presentation_profile_id"], "delivery_profile_id": probe["delivery_profile_id"],
    }
    inst = probe["parameter_instance"]
    binding_core = {
        "request_identity": req, "canonical_chain": dict(canonical_chain), "timing_review_reference": dict(timing_review),
        "parameter_instance_sha256": inst["parameter_instance_sha256"], "frozen_c11c_manifest_sha256": EXPECTED_MANIFEST,
    }
    return {
        "request_identity": req,
        "canonical_chain": dict(canonical_chain),
        "timing_review_reference": dict(timing_review),
        "parameter_instance": dict(inst),
        "request_parameter_binding_sha256": digest(binding_core),
        "evidence": {
            "canonical_request_chain_verified": True,
            "direct_source_pins_verified": True,
            "in_memory_profile_repeat_deterministic": True,
            "exact_grammar_parameter_instance_bound": True,
            "exact_selector_visual_payload_materialized": False,
            "timing_review_policy_values_consumed": False,
        },
    }

def _build_report(root: Path, godot: str, timeout: float, process_runner: Callable[..., Any] = subprocess.run) -> dict[str, Any]:
    contract, _schema, input_schema, report_schema, pins = _load_contract(root)
    try:
        version_result = process_runner([godot, "--version"], cwd=str(root), text=True, capture_output=True, timeout=min(timeout, 20), check=False)
    except Exception as exc:
        raise GrammarParameterBindingError(f"Cannot invoke the pinned Godot console executable: {exc}") from exc
    version_out = str(getattr(version_result, "stdout", "") or "") + "\n" + str(getattr(version_result, "stderr", "") or "")
    if int(getattr(version_result, "returncode", -1)) != 0 or EXPECTED_GODOT_VERSION not in version_out:
        raise GrammarParameterBindingError(f"Expected Godot {EXPECTED_GODOT_VERSION}; actual version command output: {version_out.strip()!r}")
    parent_matrix = _load_module(root / "tools/c11d/d9/d_renderer_visual_loop_request_scoped_binding_matrix_v2.py", "_c11d_param_binding_parent_matrix_v2")
    parent_report = parent_matrix.build_report(root)
    ps = parent_report.get("summary", {})
    if ps.get("request_plans") != "5/5" or ps.get("request_reference_joins") != "5/5" or ps.get("policy_reference_pairs") != "45/45" or ps.get("approvals_granted") != 0 or ps.get("selected_grammar_payload_instances_bound") != "0/5":
        raise GrammarParameterBindingError("Parent request/source matrix changed scope or governance lock")
    carrier_mod = _load_module(root / "tools/c11d/d9/d_renderer_visual_loop_timing_review_request_bound_reference_carrier.py", "_c11d_param_binding_carrier_v1")
    carrier_report = carrier_mod.build_report(root)
    cs = carrier_report.get("summary", {})
    if cs.get("request_identity_joins") != "5/5" or cs.get("policy_reference_pairs") != "45/45" or cs.get("approvals_granted") != 0 or cs.get("candidate_input_admissible") is not False:
        raise GrammarParameterBindingError("Parent reference carrier changed scope or governance lock")
    binder = _load_module(root / "tools/c11d/d9/d_renderer_request_scoped_payload_binding.py", "_c11d_param_binding_v1_core")
    cases = []
    for row in contract["scope"]["grammar_matrix"]:
        chain_result, request_input, canonical_chain, timing_review = _build_parent_chain(root, row["grammar_id"], parent_matrix, binder, carrier_report)
        probe = _run_one(root, godot, timeout, contract, input_schema, request_input, canonical_chain, timing_review, process_runner)
        if probe["selection"]["subtype_id"] != row["grammar_id"] or probe["parameter_instance"]["grammar_index"] != row["grammar_index"]:
            raise GrammarParameterBindingError(f"Returned parameter instance crossed selectors: {row['grammar_id']}")
        cases.append(_case_receipt(probe, canonical_chain, timing_review))
    if len(cases) != 5 or len({row["request_identity"]["request_hash"] for row in cases}) != 5 or len({row["canonical_chain"]["plan_hash"] for row in cases}) != 5 or len({row["parameter_instance"]["parameter_instance_sha256"] for row in cases}) != 5:
        raise GrammarParameterBindingError("Five selector-specific request/plan/parameter instance identities must be distinct")
    if len({row["timing_review_reference"]["shared_policy_reference_set_sha256"] for row in cases}) != 1 or len({row["timing_review_reference"]["selector_envelope_sha256"] for row in cases}) != 5:
        raise GrammarParameterBindingError("Shared policy set or selector-specific envelope digest cardinality changed")
    if sum(row["timing_review_reference"]["policy_reference_count"] for row in cases) != 45:
        raise GrammarParameterBindingError("Expected exactly 45 policy-reference pairs")
    if any(row["evidence"]["exact_selector_visual_payload_materialized"] for row in cases):
        raise GrammarParameterBindingError("Parameter matrix may not claim exact visual payload materialization")
    report = {
        "schema": "C11-D-D9-VISUAL-LOOP-REQUEST-SCOPED-GRAMMAR-PARAMETER-BINDING-REPORT-V2",
        "schema_version": "2.0",
        "status": STATUS,
        "contract_sha256": file_sha(root / CONTRACT_REL),
        "input_schema_sha256": file_sha(root / INPUT_SCHEMA_REL),
        "report_schema_sha256": file_sha(root / REPORT_SCHEMA_REL),
        "source_lineage": pins,
        "source_lineage_sha256": digest(pins),
        "parent_matrix_report_sha256": parent_report["report_sha256"],
        "parent_reference_carrier_report_sha256": carrier_report["report_sha256"],
        "cases": cases,
        "summary": {
            "direct_source_pins": f"{len(pins)}/{len(pins)}",
            "request_plans": "5/5",
            "request_parameter_bindings": "5/5",
            "parameter_instances": "5/5",
            "exact_grammar_identity": "5/5",
            "deterministic_repeats": "5/5",
            "policy_reference_pairs": "45/45",
            "unique_request_hashes": "5/5",
            "unique_plan_hashes": "5/5",
            "unique_parameter_instance_hashes": "5/5",
            "selected_grammar_parameter_instances_bound": "5/5",
            "selected_grammar_payload_instances_bound": "0/5",
            "exact_selector_visual_payload_materialized": False,
            "approval_assertions_checked": 19,
            "approvals_granted": 0,
            "candidate_input_admissible": False,
        },
        "governance": {
            "approval_assertions_checked": 19,
            "approvals_granted": 0,
            "pending_approval_assertions": 19,
            "grammar_parameter_binding_v2_approved": False,
            "visual_loop_binding_matrix_v2_approved": False,
            "canonical_request_selector_matrix_approved": False,
            "exact_selector_payload_approved": False,
            "timing_review_inheritance_approved": False,
            "all_nine_shared_policy_sources_approved": False,
            "candidate_io_contract_complete": False,
            "renderer_baseline_approved": False,
            "renderer_baseline_frozen": False,
            "d4_8_authorized": False,
            "request_input_persisted": False,
            "parameter_payload_files_written": False,
            "receipt_files_written": False,
            "renderer_native_input_emitted": False,
            "renderer_dispatch_invoked": False,
            "media_created": False,
            "c11c_source_mutation": False,
            "candidate_input_admissible": False,
            "renderer": "OFF",
            "D4.8": "BLOCKED",
            "release_authority": "NONE",
            "D9.10": "PREPARE_ONLY",
            "D9.17": "BLOCKED_NO_GO",
            "D10": "BLOCKED",
        },
        "execution_boundary": dict(BOUNDARY),
    }
    report["report_sha256"] = digest(report)
    try:
        Draft202012Validator(report_schema).validate(report)
    except Exception as exc:
        raise GrammarParameterBindingError(f"Report JSON Schema rejected receipt: {getattr(exc, 'message', str(exc))}") from exc
    if digest({key: value for key, value in report.items() if key != "report_sha256"}) != report["report_sha256"]:
        raise GrammarParameterBindingError("Report self-hash mismatch")
    return report

def build_report(project_root=None, godot: str | None = None, timeout: float = 120, process_runner: Callable[..., Any] = subprocess.run) -> dict[str, Any]:
    root = _root(project_root)
    if not godot:
        raise GrammarParameterBindingError("An explicit Godot 4.7.1 console executable is required for runtime evidence")
    return _build_report(root, godot, timeout, process_runner)

def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True)
    parser.add_argument("--godot", required=True, help="Path to Godot 4.7.1 console executable")
    parser.add_argument("--timeout", type=float, default=120)
    parser.add_argument("--full-report", action="store_true")
    args = parser.parse_args(argv)
    try:
        report = build_report(args.root, args.godot, args.timeout)
        s = report["summary"]
        print("C11-D VISUAL LOOP REQUEST-SCOPED GRAMMAR PARAMETER BINDING V2 AUDIT PASS | direct_source_pins=" + s["direct_source_pins"] + " | request_plans=" + s["request_plans"] + " | request_parameter_bindings=" + s["request_parameter_bindings"] + " | parameter_instances=" + s["parameter_instances"] + " | exact_grammar_identity=" + s["exact_grammar_identity"] + " | deterministic_repeats=" + s["deterministic_repeats"] + " | policy_reference_pairs=" + s["policy_reference_pairs"] + " | selected_grammar_parameter_instances_bound=" + s["selected_grammar_parameter_instances_bound"] + " | selected_grammar_payload_instances_bound=" + s["selected_grammar_payload_instances_bound"] + " | exact_selector_visual_payload_materialized=false | approval_assertions_checked=19 | approvals_granted=0 | candidate_input_admissible=false | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE")
        print(REPORT_PREFIX + canonical(report))
        if args.full_report:
            print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    except Exception as exc:
        print("C11-D VISUAL LOOP REQUEST-SCOPED GRAMMAR PARAMETER BINDING V2 AUDIT FAIL | " + str(exc) + " | candidate_input_admissible=false | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE")
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
