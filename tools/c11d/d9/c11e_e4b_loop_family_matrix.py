"""E4B plan-only matrix across every existing C11-C Visual Loop grammar.

This is a D-owned verification harness, not a renderer, binder or Producer.
It exercises the already-canonical D9.9 -> D9.10 bridge -> D-only prepare
adapter -> C11-E E1 intent path. No Godot, C11-C generator, music engine,
FFmpeg, renderer or media is invoked.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import re
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

SCHEMA = "C11E-E4B-LOOP-FAMILY-MATRIX-RECEIPT-V1"
EXPECTED_EDITORIAL_FIELDS = ["call_to_action", "language", "subtitle", "title"]
EXPECTED_FAMILY_GRAMMAR_COUNTS = {
    "c11c_geometric_waves_v1": 5,
    "c11c_fractal_bloom_v1": 5,
    "c11c_sacred_symmetry_v1": 5,
    "c11c_living_particles_v1": 5,
    "c11c_invisible_forces_v1": 7,
}
EXPECTED_FAMILY_MUSIC_PROFILES = {
    "c11c_geometric_waves_v1": "CIRCUIT_PULSE",
    "c11c_fractal_bloom_v1": "ORGANIC_BLOOM",
    "c11c_sacred_symmetry_v1": "ORBITAL_RITUAL",
    "c11c_living_particles_v1": "ORGANIC_BLOOM",
    "c11c_invisible_forces_v1": "FLOWING_VECTOR",
}
SCENARIOS = (
    ("BASELINE", "baseline"),
    ("GAMEPLAY_SEED_ONLY_CHANGED", "gameplay"),
    ("MUSIC_SEED_ONLY_CHANGED", "music"),
)


class LoopFamilyMatrixError(RuntimeError):
    pass


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _canonical(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): _canonical(value[key]) for key in sorted(value, key=lambda item: str(item))}
    if isinstance(value, (list, tuple)):
        return [_canonical(item) for item in value]
    return value


def _sha256_json(value: Any) -> str:
    encoded = json.dumps(_canonical(value), ensure_ascii=False, separators=(",", ":"), allow_nan=False).encode("utf-8")
    return _sha256_bytes(encoded)


def _read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        raise LoopFamilyMatrixError(f"Invalid JSON {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise LoopFamilyMatrixError(f"Expected JSON object: {path}")
    return value


def _load_module(name: str, path: Path):
    module_key = f"_c11e_e4b_loop_matrix_{name}"
    existing = sys.modules.get(module_key)
    if existing is not None:
        return existing
    spec = importlib.util.spec_from_file_location(module_key, path)
    if spec is None or spec.loader is None:
        raise LoopFamilyMatrixError(f"Cannot load module: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_key] = module
    try:
        spec.loader.exec_module(module)
    except Exception:
        sys.modules.pop(module_key, None)
        raise
    return module


def _load_backend(root: Path) -> dict[str, Any]:
    d9_dir = root / "tools" / "c11d" / "d9"
    e1_dir = root / "c11c-suite" / "c11c-producer"
    for path in (str(d9_dir), str(e1_dir)):
        if path not in sys.path:
            sys.path.insert(0, path)
    d9 = _load_module("universal_producer", d9_dir / "universal_producer.py")
    bridge = _load_module("editorial_render_bridge", d9_dir / "editorial_render_bridge.py")
    adapter = _load_module("d_render_adapter", d9_dir / "d_render_adapter.py")
    e1 = _load_module("production_service", e1_dir / "c11e_production_service.py")
    return {"d9": d9, "bridge": bridge, "adapter": adapter, "e1": e1}


def enumerate_loop_selectors(root: Path) -> list[dict[str, str]]:
    """Read the existing Producer schema and D9.8 catalog; never duplicate IDs."""
    schema = _read_json(root / "c11c-suite" / "c11c-producer" / "producer_schema.json")
    families = schema.get("families")
    if not isinstance(families, dict):
        raise LoopFamilyMatrixError("C11-C Producer family registry is missing")
    if set(families) != set(EXPECTED_FAMILY_GRAMMAR_COUNTS):
        raise LoopFamilyMatrixError(
            "Loop family registry identity drift: "
            f"expected={sorted(EXPECTED_FAMILY_GRAMMAR_COUNTS)} actual={sorted(families)}"
        )

    profile_doc = _read_json(root / "profiles" / "presentation" / "c11c_visual_music_profiles.json")
    bindings = profile_doc.get("bindings", {})
    selectors: list[dict[str, str]] = []
    for family_id in sorted(families):
        declaration = families[family_id]
        grammars = declaration.get("grammars") if isinstance(declaration, dict) else None
        if not isinstance(grammars, list):
            raise LoopFamilyMatrixError(f"Malformed family grammar registry: {family_id}")
        concrete = [row for row in grammars if isinstance(row, list) and len(row) >= 2 and str(row[0]) != "auto"]
        expected_count = EXPECTED_FAMILY_GRAMMAR_COUNTS[family_id]
        if len(concrete) != expected_count:
            raise LoopFamilyMatrixError(f"Grammar count drift in {family_id}: expected={expected_count} actual={len(concrete)}")
        internal = str(declaration.get("internal", ""))
        binding = bindings.get(f"visual_loop/{internal}")
        if not isinstance(binding, dict):
            raise LoopFamilyMatrixError(f"Missing C11-C family music binding: visual_loop/{internal}")
        profile_id = str(binding.get("profile", ""))
        expected_profile = EXPECTED_FAMILY_MUSIC_PROFILES[family_id]
        if profile_id != expected_profile:
            raise LoopFamilyMatrixError(f"Music profile drift for {family_id}: expected={expected_profile} actual={profile_id}")
        for grammar_row in concrete:
            grammar_id = str(grammar_row[0])
            label = str(grammar_row[1])
            selectors.append({
                "family_id": family_id,
                "family_internal_id": internal,
                "family_label": str(declaration.get("name", family_id)),
                "subtype_id": grammar_id,
                "subtype_label": label,
                "music_profile_id": profile_id,
            })
    selectors.sort(key=lambda row: (row["family_id"], row["subtype_id"]))
    if len(selectors) != 27 or len({(row["family_id"], row["subtype_id"]) for row in selectors}) != 27:
        raise LoopFamilyMatrixError(f"Expected 27 unique concrete Loop selectors; got {len(selectors)}")
    return selectors


def _validate_template(template: Mapping[str, Any], origin: str) -> dict[str, Any]:
    if not isinstance(template, Mapping):
        raise LoopFamilyMatrixError("Matrix request template must be an object")
    request = copy.deepcopy(dict(template))
    if request.get("schema") != "C11-D-D9.9-UNIVERSAL-PRODUCER-REQUEST-V1" or request.get("schema_version") != "1.0":
        raise LoopFamilyMatrixError("Template is not the canonical D9.9 V1 request")
    if request.get("mode") != "REVIEW":
        raise LoopFamilyMatrixError("Full-family E4B matrix only permits REVIEW mode")
    selection = request.get("selection")
    if not isinstance(selection, Mapping) or selection.get("content_type") != "visual_loops":
        raise LoopFamilyMatrixError("Template content_type must be visual_loops")
    if "presentation_options" in request:
        raise LoopFamilyMatrixError("Challenge-only presentation_options is forbidden for Loop")
    seed = request.get("seed")
    music_seed = request.get("music_seed")
    if isinstance(seed, bool) or not isinstance(seed, int) or seed < 1 or seed > 2147483646:
        raise LoopFamilyMatrixError("Template gameplay seed is outside D9.9 bounds")
    if isinstance(music_seed, bool) or not isinstance(music_seed, int) or music_seed < 1 or music_seed > 2147483646:
        raise LoopFamilyMatrixError("Template music seed is outside D9.9 bounds")
    if seed == music_seed:
        raise LoopFamilyMatrixError("Gameplay/music seed domains must use distinct values")
    if request.get("audio_enabled") is not True:
        raise LoopFamilyMatrixError("E4B family matrix requires audio_enabled=true as a planning input")
    if request.get("personalization_enabled") is not True:
        raise LoopFamilyMatrixError("E4B family matrix requires personalization_enabled=true")
    provenance = request.get("provenance")
    if not isinstance(provenance, Mapping):
        provenance = {}
    provenance = dict(provenance)
    if set(provenance) - {"source_revision", "request_origin"}:
        raise LoopFamilyMatrixError("Unknown provenance fields in matrix template")
    provenance["request_origin"] = origin
    provenance.setdefault("source_revision", "C11E-E4B-LOOP-FAMILY-MATRIX-V1")
    request["provenance"] = provenance
    return request


def _build_case_request(template: Mapping[str, Any], selector: Mapping[str, str], scenario: str, case_index: int, base_seed: int, base_music_seed: int) -> dict[str, Any]:
    request = copy.deepcopy(dict(template))
    request["request_id"] = f"E4B_LOOP_MATRIX_{case_index:03d}_{scenario}"
    request["selection"] = {
        "content_type": "visual_loops",
        "family_id": selector["family_id"],
        "subtype_id": selector["subtype_id"],
    }
    if scenario == "BASELINE":
        request["seed"] = base_seed
        request["music_seed"] = base_music_seed
    elif scenario == "GAMEPLAY_SEED_ONLY_CHANGED":
        request["seed"] = base_seed + 1
        request["music_seed"] = base_music_seed
    elif scenario == "MUSIC_SEED_ONLY_CHANGED":
        request["seed"] = base_seed
        request["music_seed"] = base_music_seed + 1
    else:
        raise LoopFamilyMatrixError(f"Unknown seed scenario: {scenario}")
    return request


def _evaluate_one(root: Path, backend: Mapping[str, Any], request: Mapping[str, Any], selector: Mapping[str, str], scenario: str, origin: str) -> dict[str, Any]:
    d9 = backend["d9"]
    bridge_module = backend["bridge"]
    adapter_module = backend["adapter"]
    e1_module = backend["e1"]

    first = d9.evaluate_universal_request(request, root)
    if first.get("status") != "PLANNED":
        raise LoopFamilyMatrixError(f"D9.9 did not plan {selector['family_id']}/{selector['subtype_id']} ({scenario})")
    canonical = first["canonical_request"]
    plan = first["plan"]
    if canonical.get("selection", {}).get("content_type") != "visual_loops":
        raise LoopFamilyMatrixError("D9.9 canonical content_type drifted")
    if canonical.get("selection", {}).get("family_id") != selector["family_id"]:
        raise LoopFamilyMatrixError("D9.9 canonical family_id drifted")
    if canonical.get("selection", {}).get("subtype_id") != selector["subtype_id"]:
        raise LoopFamilyMatrixError("D9.9 canonical subtype_id drifted")
    editorial = canonical.get("editorial")
    if not isinstance(editorial, Mapping) or set(editorial) != set(EXPECTED_EDITORIAL_FIELDS):
        raise LoopFamilyMatrixError(f"D9.8 Loop editorial keyset mismatch: {selector['family_id']}/{selector['subtype_id']}")
    for field, value in editorial.items():
        if not isinstance(value, str):
            raise LoopFamilyMatrixError(f"Editorial field is not a string: {field}")
        if unicodedata.normalize("NFC", value) != value:
            raise LoopFamilyMatrixError(f"Editorial value is not NFC-normalized: {field}")
        if "Ã" in value or "�" in value:
            raise LoopFamilyMatrixError(f"Mojibake detected in editorial field: {field}")
    if plan.get("plan_kind") != "UNIVERSAL_EDITORIAL_INTENT_PLAN_ONLY":
        raise LoopFamilyMatrixError("Loop plan_kind must remain intent-plan-only")
    if plan.get("d4_subplan_status") != "NOT_APPLICABLE_NO_D4_LOOP_DRILL_CONTRACT":
        raise LoopFamilyMatrixError("Loop must not claim a D4 Challenge subplan")

    bridge = bridge_module.build_bridge_planning_record(first, root)
    if bridge.get("status") != "PLANNING_ONLY_NOT_RENDERABLE":
        raise LoopFamilyMatrixError("D9.10 bridge is not planning-only")
    adapter = adapter_module.prepare_d_only_adapter_envelope(first, bridge, root)
    if adapter.get("status") != "PREPARED_NOT_DISPATCHED_RENDERER_DISABLED":
        raise LoopFamilyMatrixError("D-only adapter did not remain prepare-only")

    e1_prepared = e1_module.prepare_c11e_production_intent(
        request, root, request_origin=origin, resolver_module=d9
    )
    intent = e1_prepared["intent"]
    e1_resolved = e1_prepared["resolver_result"]
    if e1_resolved.get("request_hash") != first.get("request_hash") or e1_resolved.get("plan_hash") != first.get("plan_hash"):
        raise LoopFamilyMatrixError("E1 and direct D9.9 request/plan identities diverged")
    if intent.get("status") != "PREPARED_E1_NOT_DISPATCHED":
        raise LoopFamilyMatrixError("E1 intent did not remain prepare-only")
    if intent.get("request_origin") != origin:
        raise LoopFamilyMatrixError("E1 request origin was not preserved")
    if intent.get("editorial") != dict(editorial):
        raise LoopFamilyMatrixError("E1 editorial values differ from D9.9")
    if set(intent.get("editorial_field_consumption", {})) != set(EXPECTED_EDITORIAL_FIELDS):
        raise LoopFamilyMatrixError("E1 did not retain all four Loop editorial fields")
    if any(row.get("consumer_status") != "NOT_CONSUMED_E1" or row.get("required_gate") != "E4" for row in intent["editorial_field_consumption"].values()):
        raise LoopFamilyMatrixError("E1 Loop editorial consumption gate/status drift")
    family_adapter = intent.get("family_adapter", {})
    if family_adapter.get("status") != "NOT_CONNECTED_E1" or family_adapter.get("target_gate") != "E4":
        raise LoopFamilyMatrixError("E1 family adapter gate/status drift")
    music = intent.get("music_contract", {})
    expected_music = {
        "route": "PRESERVE_EXISTING_C11C_FAMILY_MUSIC_PATH",
        "status": "PROTECTED_FAMILY_NOT_REWIRED",
        "music_seed_field": "request.music_seed",
        "music_seed": request["music_seed"],
        "dispatchable": False,
        "dispatch_authorized": False,
        "engine_invoked": False,
        "audio_created": False,
        "renderer_invoked": False,
        "ffmpeg_mux_invoked": False,
        "release_authority": "NONE",
    }
    for key, expected in expected_music.items():
        if music.get(key) != expected:
            raise LoopFamilyMatrixError(f"Protected Loop music contract mismatch: {key}")
    if intent.get("seed_domains", {}).get("independent_domains") is not True:
        raise LoopFamilyMatrixError("E1 seed domains are not marked independent")
    if intent.get("seed_domains", {}).get("gameplay", {}).get("value") != request["seed"]:
        raise LoopFamilyMatrixError("E1 gameplay seed mismatch")
    if intent.get("seed_domains", {}).get("music", {}).get("value") != request["music_seed"]:
        raise LoopFamilyMatrixError("E1 music seed mismatch")

    governance_checks = {
        "adapter_renderer_input_emitted": adapter.get("renderer_input_emitted") is False,
        "adapter_renderer_dispatch_invoked": adapter.get("renderer_dispatch_invoked") is False,
        "adapter_production_execution": adapter.get("production_execution") is False,
        "adapter_media_output_created": adapter.get("media_output_created") is False,
        "adapter_d4_8_blocked": adapter.get("d4_8") == "BLOCKED",
        "adapter_release_none": adapter.get("release_authority") == "NONE",
        "e1_renderer_input_emitted": intent.get("execution_boundary", {}).get("renderer_input_emitted") is False,
        "e1_renderer_dispatch_invoked": intent.get("execution_boundary", {}).get("renderer_dispatch_invoked") is False,
        "e1_production_execution": intent.get("execution_boundary", {}).get("production_execution") is False,
        "e1_media_created": intent.get("execution_boundary", {}).get("media_created") is False,
        "e1_d4_8_blocked": intent.get("execution_boundary", {}).get("d4_8") == "BLOCKED",
        "e1_release_none": intent.get("execution_boundary", {}).get("release_authority") == "NONE",
    }
    if not all(governance_checks.values()):
        raise LoopFamilyMatrixError(f"Governance check failed: {governance_checks}")

    # Deterministic repeat at the canonical D9.9 / D9.10 / D-only envelope layers.
    second = d9.evaluate_universal_request(request, root)
    bridge_second = bridge_module.build_bridge_planning_record(second, root)
    adapter_second = adapter_module.prepare_d_only_adapter_envelope(second, bridge_second, root)
    deterministic = {
        "request_hash": first["request_hash"] == second["request_hash"],
        "editorial_hash": first["editorial_hash"] == second["editorial_hash"],
        "plan_hash": first["plan_hash"] == second["plan_hash"],
        "bridge_hash": bridge["record_hash"] == bridge_second["record_hash"],
        "adapter_envelope_hash": adapter["envelope_hash"] == adapter_second["envelope_hash"],
    }
    if not all(deterministic.values()):
        raise LoopFamilyMatrixError(f"Deterministic repeat mismatch: {deterministic}")

    return {
        "case_id": request["request_id"],
        "family_id": selector["family_id"],
        "family_internal_id": selector["family_internal_id"],
        "family_label": selector["family_label"],
        "subtype_id": selector["subtype_id"],
        "subtype_label": selector["subtype_label"],
        "scenario": scenario,
        "gameplay_seed": request["seed"],
        "music_seed": request["music_seed"],
        "music_profile_id_from_frozen_c11c_profile_registry": selector["music_profile_id"],
        "d9_catalog_request_plan_compatible_flag": False,
        "d9_actual_plan_status": first["status"],
        "d9_plan_kind": plan["plan_kind"],
        "canonical_request_hash": first["request_hash"],
        "editorial_hash": first["editorial_hash"],
        "plan_hash": first["plan_hash"],
        "bridge_hash": bridge["record_hash"],
        "adapter_envelope_hash": adapter["envelope_hash"],
        "e1_intent_hash": intent["identity"]["intent_hash"],
        "e1_intent_sha256": intent["intent_sha256"],
        "e1_request_hash": intent["identity"]["request_hash"],
        "e1_plan_hash": intent["identity"]["plan_hash"],
        "editorial_fields": {field: editorial[field] for field in EXPECTED_EDITORIAL_FIELDS},
        "editorial_fields_preserved": True,
        "e1_editorial_consumer_status": "NOT_CONSUMED_E1",
        "e1_adapter_status": family_adapter["status"],
        "music_route": music["route"],
        "music_engine_invoked": music["engine_invoked"],
        "music_audio_created": music["audio_created"],
        "renderer_invoked": music["renderer_invoked"],
        "ffmpeg_mux_invoked": music["ffmpeg_mux_invoked"],
        "deterministic_repeat": deterministic,
        "governance": governance_checks,
    }


def _compare_gui_report(gui_report: Mapping[str, Any], cli_cases: list[dict[str, Any]]) -> dict[str, Any]:
    if gui_report.get("schema") != SCHEMA or gui_report.get("status") != "PASS_LOOP_FAMILY_PLAN_MATRIX_ONLY":
        raise LoopFamilyMatrixError("GUI matrix evidence is not a valid PASS V1 report")
    gui_cases = gui_report.get("cases")
    if not isinstance(gui_cases, list):
        raise LoopFamilyMatrixError("GUI matrix evidence has no case list")
    by_key = {(row.get("family_id"), row.get("subtype_id"), row.get("scenario")): row for row in gui_cases if isinstance(row, Mapping)}
    parity_rows = []
    for cli in cli_cases:
        key = (cli["family_id"], cli["subtype_id"], cli["scenario"])
        gui = by_key.get(key)
        if gui is None:
            raise LoopFamilyMatrixError(f"Missing GUI matrix case: {key}")
        checks = {
            "selection_equal": gui.get("family_id") == cli["family_id"] and gui.get("subtype_id") == cli["subtype_id"],
            "editorial_hash_equal": gui.get("editorial_hash") == cli["editorial_hash"],
            "editorial_fields_equal": gui.get("editorial_fields") == cli["editorial_fields"],
            "gameplay_seed_equal": gui.get("gameplay_seed") == cli["gameplay_seed"],
            "music_seed_equal": gui.get("music_seed") == cli["music_seed"],
            "music_profile_equal": gui.get("music_profile_id_from_frozen_c11c_profile_registry") == cli["music_profile_id_from_frozen_c11c_profile_registry"],
            "plan_kind_equal": gui.get("d9_plan_kind") == cli["d9_plan_kind"],
        }
        if not all(checks.values()):
            raise LoopFamilyMatrixError(f"GUI/CLI matrix parity mismatch {key}: {checks}")
        parity_rows.append({"family_id": key[0], "subtype_id": key[1], "scenario": key[2], "checks": checks})
    if len(parity_rows) != 81:
        raise LoopFamilyMatrixError(f"Expected 81 GUI/CLI parity rows, got {len(parity_rows)}")
    return {"status": "PASS_GUI_CLI_ALL_27_SELECTOR_PARITY_ONLY", "case_count": len(parity_rows), "cases": parity_rows}


def run_loop_family_matrix(
    project_root: Path | str,
    request_template: Mapping[str, Any],
    *,
    request_origin: str,
    output_root: Path | str | None = None,
    compare_gui_report: Mapping[str, Any] | None = None,
    run_id: str | None = None,
) -> dict[str, Any]:
    root = Path(project_root).resolve()
    if request_origin not in {"GUI", "CLI"}:
        raise LoopFamilyMatrixError("request_origin must be GUI or CLI")
    template = _validate_template(request_template, request_origin)
    backend = _load_backend(root)
    selectors = enumerate_loop_selectors(root)
    base_seed = int(template["seed"])
    base_music_seed = int(template["music_seed"])
    if base_seed >= 2147483646 or base_music_seed >= 2147483646:
        raise LoopFamilyMatrixError("Seed fixture cannot be incremented for orthogonality cases")

    cases: list[dict[str, Any]] = []
    case_index = 0
    for selector in selectors:
        for scenario, _ in SCENARIOS:
            case_index += 1
            request = _build_case_request(template, selector, scenario, case_index, base_seed, base_music_seed)
            cases.append(_evaluate_one(root, backend, request, selector, scenario, request_origin))

    # The seed-domain assertions operate on the same canonical plans, but never
    # infer that visual payloads or music have been materialized.
    by_selector: dict[tuple[str, str], dict[str, dict[str, Any]]] = {}
    for case in cases:
        by_selector.setdefault((case["family_id"], case["subtype_id"]), {})[case["scenario"]] = case
    seed_relations = []
    for key, rows in sorted(by_selector.items()):
        base = rows["BASELINE"]
        gameplay = rows["GAMEPLAY_SEED_ONLY_CHANGED"]
        music = rows["MUSIC_SEED_ONLY_CHANGED"]
        checks = {
            "gameplay_seed_mutates_request_identity": base["canonical_request_hash"] != gameplay["canonical_request_hash"],
            "gameplay_seed_mutates_plan_identity": base["plan_hash"] != gameplay["plan_hash"],
            "gameplay_seed_preserves_music_seed": base["music_seed"] == gameplay["music_seed"],
            "music_seed_mutates_request_identity": base["canonical_request_hash"] != music["canonical_request_hash"],
            "music_seed_mutates_plan_identity": base["plan_hash"] != music["plan_hash"],
            "music_seed_preserves_gameplay_seed": base["gameplay_seed"] == music["gameplay_seed"],
            "editorial_hash_orthogonal_to_both_seed_changes": base["editorial_hash"] == gameplay["editorial_hash"] == music["editorial_hash"],
            "music_seed_reaches_e1_family_music_contract": music["music_seed"] == base_music_seed + 1 and music["music_route"] == "PRESERVE_EXISTING_C11C_FAMILY_MUSIC_PATH",
        }
        if not all(checks.values()):
            raise LoopFamilyMatrixError(f"Seed-domain orthogonality failed for {key}: {checks}")
        seed_relations.append({"family_id": key[0], "subtype_id": key[1], "checks": checks})

    family_counts: dict[str, int] = {}
    for selector in selectors:
        family_counts[selector["family_id"]] = family_counts.get(selector["family_id"], 0) + 1
    report: dict[str, Any] = {
        "schema": SCHEMA,
        "status": "PASS_LOOP_FAMILY_PLAN_MATRIX_ONLY",
        "run_id": run_id or ("E4B_LOOP_" + request_origin + "_" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "request_origin": request_origin,
        "scope": {
            "content_type": "visual_loops",
            "family_count": len(family_counts),
            "grammar_count": len(selectors),
            "seed_scenarios_per_grammar": 3,
            "case_count": len(cases),
            "deterministic_repeats": len(cases),
            "family_grammar_counts": family_counts,
            "family_music_profile_map": EXPECTED_FAMILY_MUSIC_PROFILES,
            "pipeline": ["D9.9_CANONICAL_PLAN", "D9.10_BRIDGE_PLANNING", "D_ONLY_ADAPTER_PREPARE_ONLY", "E1_INTENT_PREPARATION"],
            "execution_class": "IN_MEMORY_PLAN_AND_IDENTITY_VALIDATION_ONLY",
            "renderer_input": False,
            "family_visual_payload_materialized": False,
            "music_generator_invoked": False,
            "audio_created": False,
            "ffmpeg_mux_invoked": False,
        },
        "request_template": {
            "mode": template["mode"],
            "seed": base_seed,
            "music_seed": base_music_seed,
            "delivery_profile_id": template.get("delivery_profile_id"),
            "presentation_profile_id": template.get("presentation_profile_id"),
            "variation_index": template.get("variation_index"),
            "audio_enabled": template.get("audio_enabled"),
            "personalization_enabled": template.get("personalization_enabled"),
            "editorial": cases[0]["editorial_fields"] if cases else {},
            "editorial_template_sha256": _sha256_json({"editorial_profile": template.get("editorial_profile", {}), "production_override": template.get("production_override", {})}),
        },
        "seed_domain_relations": seed_relations,
        "cases": cases,
        "gui_cli_parity": None,
        "governance": {
            "renderer": False,
            "renderer_input_emitted": False,
            "renderer_dispatch_invoked": False,
            "production_execution": False,
            "media_created": False,
            "godot_invoked": False,
            "c11c_family_visual_generators_invoked": False,
            "c11c_family_music_generator_invoked": False,
            "d3_v5_invoked": False,
            "ffmpeg_invoked": False,
            "c11c_baseline_modified": False,
            "release_authority": "NONE",
            "d4_8": "BLOCKED",
            "d9_10": "PREPARE_ONLY",
            "d9_14": "BLOCKED",
            "d9_16": "BLOCKED",
            "d9_17": "BLOCKED_NO_GO",
            "d10": "BLOCKED_FOR_PROMOTION",
        },
    }
    if compare_gui_report is not None:
        report["gui_cli_parity"] = _compare_gui_report(compare_gui_report, cases)
    report["report_sha256"] = _sha256_json(report)

    if output_root is not None:
        output = Path(output_root).resolve()
        if output.exists():
            raise LoopFamilyMatrixError(f"Output root already exists; overwrite denied: {output}")
        output.mkdir(parents=True, exist_ok=False)
        template_path = output / "matrix_request_template.json"
        report_path = output / "matrix_report.json"
        template_path.write_text(json.dumps(template, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (output / "matrix_request_template.sha256").write_text(_sha256_bytes(template_path.read_bytes()) + "  matrix_request_template.json\n", encoding="ascii")
        (output / "matrix_report.sha256").write_text(_sha256_bytes(report_path.read_bytes()) + "  matrix_report.json\n", encoding="ascii")
    return report


def _default_cli_template(root: Path) -> dict[str, Any]:
    return {
        "schema": "C11-D-D9.9-UNIVERSAL-PRODUCER-REQUEST-V1",
        "schema_version": "1.0",
        "request_id": "E4B_LOOP_MATRIX_TEMPLATE",
        "mode": "REVIEW",
        "selection": {"content_type": "visual_loops", "family_id": "c11c_geometric_waves_v1", "subtype_id": "harmonic_membrane"},
        "seed": 314159,
        "music_seed": 840001,
        "delivery_profile_id": "REVIEW_720",
        "presentation_profile_id": "social_default_v1",
        "variation_index": 0,
        "audio_enabled": True,
        "personalization_enabled": True,
        "editorial_profile": {"global": {}, "content_type": {}, "family": {}, "subtype": {}, "variant": {}},
        "production_override": {
            "title": "Título editorial Loop — composición armónica en movimiento",
            "subtitle": "Explora el patrón geométrico, observa sus ciclos y descubre cómo evoluciona la forma",
            "call_to_action": "Guarda este loop y comparte tu patrón favorito",
            "language": "es",
        },
        "provenance": {"source_revision": "C11E-E4B-LOOP-FAMILY-MATRIX-V1", "request_origin": "CLI"},
    }


def _load_gui_matrix(root: Path, gui_evidence_root: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    template_path = gui_evidence_root / "matrix_request_template.json"
    report_path = gui_evidence_root / "matrix_report.json"
    if not template_path.is_file() or not report_path.is_file():
        raise LoopFamilyMatrixError("GUI matrix evidence must include matrix_request_template.json and matrix_report.json")
    template = _read_json(template_path)
    gui_report = _read_json(report_path)
    for filename, target in (("matrix_request_template.sha256", template_path), ("matrix_report.sha256", report_path)):
        sidecar_path = gui_evidence_root / filename
        if not sidecar_path.is_file():
            raise LoopFamilyMatrixError(f"GUI matrix evidence is missing integrity sidecar: {filename}")
        declared = sidecar_path.read_text(encoding="ascii").strip().split()[0]
        actual = _sha256_bytes(target.read_bytes())
        if declared != actual:
            raise LoopFamilyMatrixError(f"GUI matrix integrity sidecar mismatch: {filename}")
    if gui_report.get("status") != "PASS_LOOP_FAMILY_PLAN_MATRIX_ONLY" or gui_report.get("request_origin") != "GUI":
        raise LoopFamilyMatrixError("GUI matrix report is not an accepted GUI-origin plan-only report")
    return template, gui_report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="C11-E E4B Loop full-family plan-only matrix")
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--origin", choices=("GUI", "CLI"), default="CLI")
    parser.add_argument("--output-root", required=True)
    parser.add_argument("--gui-evidence-root", default="")
    args = parser.parse_args(argv)
    root = Path(args.project_root).resolve()
    output_root = Path(args.output_root).resolve()
    if args.origin == "CLI":
        if not args.gui_evidence_root:
            raise LoopFamilyMatrixError("CLI parity requires --gui-evidence-root from the GUI matrix run")
        template, gui_report = _load_gui_matrix(root, Path(args.gui_evidence_root).resolve())
        template = _validate_template(template, "CLI")
        report = run_loop_family_matrix(root, template, request_origin="CLI", output_root=output_root, compare_gui_report=gui_report)
    else:
        template = _default_cli_template(root)
        report = run_loop_family_matrix(root, template, request_origin="GUI", output_root=output_root)
    print("C11E_E4B_LOOP_FAMILY_MATRIX=PASS_LOOP_FAMILY_PLAN_MATRIX_ONLY")
    print(f"FAMILIES={report['scope']['family_count']}; GRAMMARS={report['scope']['grammar_count']}; CASES={report['scope']['case_count']}")
    print(f"DETERMINISTIC_REPEATS={report['scope']['deterministic_repeats']}; SEED_RELATIONS={len(report['seed_domain_relations'])}")
    print(f"ORIGIN={report['request_origin']}; EDITORIAL_FIELDS=4/4; MUSIC_ROUTE=PRESERVE_EXISTING_C11C_FAMILY_MUSIC_PATH")
    if report.get("gui_cli_parity"):
        print(f"GUI_CLI_PARITY={report['gui_cli_parity']['status']}; CASES={report['gui_cli_parity']['case_count']}")
    print(f"REPORT={output_root / 'matrix_report.json'}")
    print("RENDERER=OFF; DISPATCH=FALSE; MEDIA=FALSE; GODOT=NOT_INVOKED; D3_V5=NOT_INVOKED; FFMPEG=NOT_INVOKED; RELEASE_AUTHORITY=NONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
