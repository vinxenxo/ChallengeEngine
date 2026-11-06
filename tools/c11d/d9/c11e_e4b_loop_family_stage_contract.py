"""E4B Loop family-stage contract builder (D-only, pure preparation).

Consumes the canonical D9.9 plan and D9.10 bridge record, validates the existing
D-only adapter envelope, and prepares an inspectable family-specific C11-C visual
launcher contract plus the approved Loop editorial composition specification.
It never invokes C11-C, Godot, FFmpeg, D3, audio, or media creation.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import sys
from pathlib import Path
from typing import Any, Mapping

SCHEMA = "C11E-E4B-LOOP-FAMILY-STAGE-CONTRACT-V1"
PRODUCER_SCHEMA_REL = Path("c11c-suite/c11c-producer/producer_schema.json")
MUSIC_REGISTRY_REL = Path("profiles/presentation/c11c_visual_music_profiles.json")
A1_REL = Path("definitions/c11d/production/D_RENDERER_UNIFIED_PRESENTATION_REGION_POLICY_PROPOSAL_V1.json")
A3_REL = Path("definitions/c11d/production/D_RENDERER_LOOP_DRILL_EDITORIAL_FIELD_WINDOW_PROPOSAL_V1.json")
COMPOSITION_REL = Path("definitions/c11d/production/C11E_E4B_LOOP_EDITORIAL_COMPOSITION_PROPOSAL_V1.json")
TIMEBASE_REL = Path("definitions/c11d/production/D_RENDERER_UNIFIED_DELIVERY_TIMEBASE_POLICY_PROPOSAL_V1.json")
AUDIO_REL = Path("definitions/c11d/production/D_RENDERER_UNIFIED_AUDIO_MUSIC_DELIVERY_POLICY_PROPOSAL_V1.json")
SEED_MIN = 1
SEED_MAX = 2147483646


class LoopFamilyContractError(ValueError):
    pass


def _sha256(value: Any) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def _read(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        raise LoopFamilyContractError(f"Cannot read JSON {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise LoopFamilyContractError(f"Expected JSON object: {path}")
    return value


def _load(name: str, path: Path):
    key = "_c11e_loop_contract_" + name
    if key in sys.modules:
        return sys.modules[key]
    spec = importlib.util.spec_from_file_location(key, path)
    if spec is None or spec.loader is None:
        raise LoopFamilyContractError(f"Cannot load D boundary module: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[key] = module
    spec.loader.exec_module(module)
    return module


def _integer(value: Any, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or not SEED_MIN <= value <= SEED_MAX:
        raise LoopFamilyContractError(f"{name} must be an explicit integer in {SEED_MIN}..{SEED_MAX}")
    return value


def _canonical_identity(result: Mapping[str, Any], bridge: Mapping[str, Any]) -> None:
    from editorial_render_bridge import sha256 as d_hash
    from editorial_render_bridge import RECORD_SCHEMA

    if result.get("status") != "PLANNED":
        raise LoopFamilyContractError("Only a canonical D9.9 PLANNED result is accepted")
    plan, request = result.get("plan"), result.get("canonical_request")
    if not isinstance(plan, Mapping) or not isinstance(request, Mapping):
        raise LoopFamilyContractError("Canonical request and plan objects are required")
    if result.get("request_hash") != d_hash(request) or result.get("plan_hash") != d_hash(plan):
        raise LoopFamilyContractError("D9.9 canonical request/plan hash mismatch")
    editorial_hash = d_hash({"selection": plan.get("selection"), "editorial": plan.get("editorial")})
    if result.get("editorial_hash") != editorial_hash:
        raise LoopFamilyContractError("D9.9 editorial hash mismatch")
    if not isinstance(bridge, Mapping) or bridge.get("schema") != RECORD_SCHEMA:
        raise LoopFamilyContractError("A canonical D9.10 bridge record is required")
    if bridge.get("status") != "PLANNING_ONLY_NOT_RENDERABLE":
        raise LoopFamilyContractError("D9.10 bridge must remain planning-only")
    if bridge.get("record_hash") != d_hash({k: v for k, v in bridge.items() if k != "record_hash"}):
        raise LoopFamilyContractError("D9.10 bridge record hash mismatch")
    for key in ("request_hash", "editorial_hash", "plan_hash"):
        if bridge.get("identity", {}).get(key) != result.get(key):
            raise LoopFamilyContractError(f"D9.10 bridge identity mismatch: {key}")
    if bridge.get("selection") != dict(plan.get("selection", {})):
        raise LoopFamilyContractError("D9.10 bridge selection mismatch")


def build_loop_family_stage_contract(
    result: Mapping[str, Any],
    bridge_record: Mapping[str, Any],
    project_root: str | Path | None = None,
) -> dict[str, Any]:
    """Build an in-memory, non-dispatchable family contract from real D9.9/D9.10 records."""
    root = Path(project_root).resolve() if project_root is not None else Path(__file__).resolve().parents[3]
    _canonical_identity(result, bridge_record)
    plan = result["plan"]
    request = result["canonical_request"]
    selection = plan["selection"]
    if selection.get("content_type") != "visual_loops":
        raise LoopFamilyContractError("This contract builder is restricted to Visual Loops")
    if plan.get("plan_kind") != "UNIVERSAL_EDITORIAL_INTENT_PLAN_ONLY":
        raise LoopFamilyContractError("Loop plan must remain universal editorial-intent plan-only")
    if plan.get("renderer_activation") is not False or plan.get("production_execution") is not False or plan.get("release_authority") != "NONE":
        raise LoopFamilyContractError("D9.9 plan attempts to exceed its execution authority")
    if plan.get("d4_8") != "BLOCKED":
        raise LoopFamilyContractError("D4.8 must remain BLOCKED")

    gameplay_seed = _integer(request.get("seed"), "request.seed")
    music_seed = _integer(request.get("music_seed"), "request.music_seed")
    if gameplay_seed == music_seed:
        raise LoopFamilyContractError("Gameplay and music seed values must be isolated in this D adapter contract")
    if plan.get("seed") != gameplay_seed or plan.get("music_seed") != music_seed:
        raise LoopFamilyContractError("Plan seed-domain values differ from the canonical request")

    schema = _read(root / PRODUCER_SCHEMA_REL)
    family_id = selection.get("family_id")
    grammar_id = selection.get("subtype_id")
    family = schema.get("families", {}).get(family_id)
    if not isinstance(family, Mapping):
        raise LoopFamilyContractError(f"Unknown C11-C Loop family: {family_id!r}")
    grammar_ids = [item[0] for item in family.get("grammars", []) if isinstance(item, list) and len(item) >= 1 and item[0] != "auto"]
    if not isinstance(grammar_id, str) or grammar_id not in grammar_ids:
        raise LoopFamilyContractError(f"Grammar is not an explicit member of family {family_id}: {grammar_id!r}")
    launcher = family.get("prototype")
    if not isinstance(launcher, str) or not launcher.endswith("/run_prototype.ps1"):
        raise LoopFamilyContractError("Family launcher path is not the canonical run_prototype.ps1 entry point")
    launcher_path = root / launcher
    if not launcher_path.is_file():
        raise LoopFamilyContractError(f"Family launcher missing: {launcher}")
    launcher_text = launcher_path.read_text(encoding="utf-8-sig")
    header_end = launcher_text.find("$ErrorActionPreference")
    header = launcher_text[:header_end if header_end >= 0 else min(len(launcher_text), 12000)]
    for parameter in ("$Seed", "$Grammar", "$NoSound", "$OutputRoot", "$OutputTag"):
        if parameter.lower() not in header.lower():
            raise LoopFamilyContractError(f"Launcher missing required parameter: {parameter}")

    music_registry = _read(root / MUSIC_REGISTRY_REL)
    internal = family.get("internal")
    music = music_registry.get("bindings", {}).get(f"visual_loop/{internal}")
    if not isinstance(music, Mapping):
        raise LoopFamilyContractError(f"Frozen C11-C music binding missing for family: {internal}")
    music_profile = music.get("profile")
    profile_ids = {item.get("id") for item in music_registry.get("profiles", []) if isinstance(item, Mapping)}
    if music_profile not in profile_ids or music.get("music_semantic_inputs") != ["seed", "visual_grammar"]:
        raise LoopFamilyContractError("Frozen family music profile contract is inconsistent")

    a1 = _read(root / A1_REL)
    a3 = _read(root / A3_REL)
    composition = _read(root / COMPOSITION_REL)
    timebase = _read(root / TIMEBASE_REL)
    audio = _read(root / AUDIO_REL)
    expected = {
        "A1": "101092bb32127bb8854a501a9215c0b6cf69581594383903716907d49719c01a",
        "A3": "609a4d183aac07c2cbe1abaf41444160fdd137217faffbead3aef618320d57dc",
        "COMPOSITION": "9e206704665ea85226ecc10854be9f679c32fe9ed7efb690a829f6e8456d43da",
        "TIMEBASE": "41a62b0766db47cd99772f28642ef67766314f20f0f7891789d6b7497bbfee85",
        "AUDIO": "3dd4874e1b6506de6d9ddbe6ad1b567a284b94cc00ef1bac0d35d1731af05e23",
    }
    for label, path, value in (("A1", A1_REL, a1), ("A3", A3_REL, a3), ("COMPOSITION", COMPOSITION_REL, composition), ("TIMEBASE", TIMEBASE_REL, timebase), ("AUDIO", AUDIO_REL, audio)):
        digest = hashlib.sha256((root / path).read_bytes()).hexdigest()
        if digest != expected[label]:
            raise LoopFamilyContractError(f"Approved proposal drift: {label}")

    editorial = plan.get("editorial")
    if not isinstance(editorial, Mapping) or set(editorial) != {"title", "subtitle", "call_to_action", "language"}:
        raise LoopFamilyContractError("Loop editorial values must match the exact D9.8 allowlist")
    a1_map = a1.get("policy", {}).get("field_region_targets", {})
    a3_map = {item.get("field_id"): item for item in a3.get("mapping_policy", {}).get("visible_fields", [])}
    visual_fields = ("title", "subtitle", "call_to_action")
    field_contracts = []
    visible_count = 0
    for field in visual_fields:
        value = editorial.get(field)
        if not isinstance(value, str) or len(value) > 160:
            raise LoopFamilyContractError(f"Editorial field must be a string of at most 160 codepoints: {field}")
        target = a1_map.get(field, {}).get("target_region")
        window = a3_map.get(field)
        if not target or not isinstance(window, Mapping):
            raise LoopFamilyContractError(f"Approved field mapping/window missing: {field}")
        visible = bool(value.strip()) and value.strip().upper() != "UNKNOWN"
        visible_count += int(visible)
        field_contracts.append({
            "field": field,
            "value": value,
            "value_sha256": hashlib.sha256(value.encode("utf-8")).hexdigest(),
            "target_semantic_region": target,
            "target_composition_band": "TOP_EDITORIAL_BAND" if target == "HEADER" else "BOTTOM_EDITORIAL_BAND",
            "visible": visible,
            "visibility_window": "[0, ACTUAL_C11C_PAYLOAD.frame_count)" if visible else None,
            "window_rule": window.get("window_rule"),
            "empty_or_unknown_rule": "SUPPRESS_FIELD_NO_WINDOW",
        })
    language = editorial.get("language")
    if not isinstance(language, str) or len(language) > 160:
        raise LoopFamilyContractError("Editorial language metadata must be a string of at most 160 codepoints")

    geom = composition.get("geometry", {})
    canvas = geom.get("canvas", {})
    viewport = geom.get("source_frame_viewport", {})
    top = geom.get("top_editorial_band", {})
    bottom = geom.get("bottom_editorial_band", {})
    transform = geom.get("source_frame_transform", {})
    if (canvas.get("width"), canvas.get("height"), geom.get("delivery_profile_id")) != (720, 1280, "REVIEW_720"):
        raise LoopFamilyContractError("Approved Loop composition geometry identity mismatch")
    if (viewport.get("x"), viewport.get("y"), viewport.get("width"), viewport.get("height")) != (108, 192, 504, 896):
        raise LoopFamilyContractError("Approved Loop source viewport changed")
    if top.get("height") != 192 or bottom.get("y") != 1088 or bottom.get("height") != 192:
        raise LoopFamilyContractError("Approved Loop editorial band geometry changed")
    if transform.get("cropping") is not False or transform.get("nonuniform_stretch") is not False or transform.get("temporal_resampling") is not False or transform.get("source_frame_count_mutation") is not False or transform.get("source_frame_order_mutation") is not False:
        raise LoopFamilyContractError("Loop source-frame preservation invariant changed")
    fps = timebase.get("policy", {}).get("target_fps")
    if fps != 30:
        raise LoopFamilyContractError("Approved Loop delivery timebase is not 30 FPS")
    audio_profile = audio.get("target_audio_profile", {})
    audio_policy = audio.get("policy", {})
    if audio_policy.get("music_asset_policy") != "OUT_OF_SCOPE_NOT_SELECTED_NOT_EMITTED" or audio_policy.get("mixing_policy") != "OUT_OF_SCOPE_NOT_DEFINED_NOT_APPLIED":
        raise LoopFamilyContractError("D.1 audio policy exclusions changed")

    from d_render_adapter import prepare_d_only_adapter_envelope
    adapter_envelope = prepare_d_only_adapter_envelope(result, bridge_record, root)

    request_id = str(request.get("request_id", "loop"))
    output_tag = re.sub(r"[^A-Za-z0-9_.-]+", "_", request_id).strip("._-")[:80] or "loop"
    arguments = ["-Seed", str(gameplay_seed), "-Grammar", grammar_id, "-NoSound", "-OutputRoot", "<FRESH_ISOLATED_TEST_ROOT>", "-OutputTag", output_tag]
    report: dict[str, Any] = {
        "schema": SCHEMA,
        "schema_version": "1.0",
        "status": "FAMILY_BOUND_PREPARATION_NOT_DISPATCHABLE",
        "request_identity": {
            "request_id": request_id,
            "request_hash": result["request_hash"],
            "plan_hash": result["plan_hash"],
            "editorial_hash": result["editorial_hash"],
            "bridge_record_hash": bridge_record["record_hash"],
            "d_only_adapter_envelope_hash": adapter_envelope["envelope_hash"],
        },
        "content_identity": {"content_type": "visual_loops", "family_id": family_id, "family_internal_id": internal, "grammar_id": grammar_id},
        "family_visual_stage": {
            "launcher_path": launcher,
            "argument_vector": arguments,
            "audio_switch": "-NoSound",
            "gameplay_seed": gameplay_seed,
            "music_seed": music_seed,
            "music_seed_passed_to_visual_launcher": False,
            "frozen_c11c_music_profile_id": music_profile,
            "family_registry_semantic_inputs": music.get("music_semantic_inputs"),
            "launcher_execution": False,
            "reason_not_executed": "D4.8_BLOCKED_AND_NO_RENDERER_EXECUTION_AUTHORITY",
        },
        "editorial": {
            "values_preserved_exactly": True,
            "language_metadata": language,
            "fields": field_contracts,
            "visible_visual_field_count": visible_count,
            "activation": "INSET_CONTAIN_COMPOSITION" if visible_count else "UNCHANGED_FULL_FRAME_PASSTHROUGH",
            "static_for_entire_source_sequence": True,
            "layout_measurement": "NOT_PROVEN_UNTIL_ISOLATED_GODOT_VISUAL_REVIEW",
        },
        "composition": {
            "delivery_profile_id": "REVIEW_720",
            "canvas": canvas,
            "background_rgb_hex": geom.get("background_rgb_hex"),
            "top_editorial_band": top,
            "source_frame_viewport": viewport,
            "bottom_editorial_band": bottom,
            "source_frame_transform": transform,
            "text_blocks": geom.get("editorial_text_blocks"),
            "overflow_policy": geom.get("overflow_policy"),
            "source_frame_count_source": "REQUEST_SCOPED_MATERIALIZED_C11C_PAYLOAD_ONLY",
            "source_frame_window": "[0, ACTUAL_C11C_PAYLOAD.frame_count)",
            "source_fps": "ACTUAL_C11C_PAYLOAD.fps",
            "delivery_fps": fps,
            "frame_order": "IDENTITY_NO_RESAMPLING",
            "materialized_payload_receipt_required": True,
        },
        "audio_delivery_envelope": {
            "codec": audio_profile.get("audio_codec"),
            "profile": audio_profile.get("audio_profile"),
            "bitrate_kbps": audio_profile.get("audio_bitrate_kbps"),
            "sample_rate_hz": audio_profile.get("audio_sample_rate_hz"),
            "channels": audio_profile.get("audio_channels"),
            "music_asset_policy": audio_policy.get("music_asset_policy"),
            "mixing_policy": audio_policy.get("mixing_policy"),
            "audio_asset_selected": False,
            "audio_generated": False,
            "pcm_samples_emitted": False,
            "audio_payload_materialized": False,
            "mux_invoked": False,
            "music_seed_domain": "request.music_seed; RESERVED_FOR_FUTURE_APPROVED_EXISTING_FAMILY_MUSIC_ROUTE",
            "d3_v5_invoked": False,
        },
        "governance": {
            "family_stage_contract_created_in_memory": True,
            "renderer_native_input_emitted": False,
            "renderer_dispatch_invoked": False,
            "launcher_invoked": False,
            "godot_invoked": False,
            "ffmpeg_invoked": False,
            "media_created": False,
            "c11c_source_mutation": False,
            "d4_8": "BLOCKED",
            "d9_10": "PREPARE_ONLY",
            "release_authority": "NONE",
        },
    }
    report["contract_sha256"] = _sha256(report)
    return report


def validate_loop_family_stage_contract(contract: Mapping[str, Any]) -> bool:
    if not isinstance(contract, Mapping) or contract.get("schema") != SCHEMA:
        raise LoopFamilyContractError("Unsupported Loop family-stage contract schema")
    if contract.get("status") != "FAMILY_BOUND_PREPARATION_NOT_DISPATCHABLE":
        raise LoopFamilyContractError("Family-stage contract status is not non-dispatchable")
    expected = _sha256({k: v for k, v in contract.items() if k != "contract_sha256"})
    if contract.get("contract_sha256") != expected:
        raise LoopFamilyContractError("Family-stage contract SHA-256 mismatch")
    governance = contract.get("governance", {})
    for field in ("renderer_native_input_emitted", "renderer_dispatch_invoked", "launcher_invoked", "godot_invoked", "ffmpeg_invoked", "media_created", "c11c_source_mutation"):
        if governance.get(field) is not False:
            raise LoopFamilyContractError(f"Governance lock changed: {field}")
    if governance.get("d4_8") != "BLOCKED" or governance.get("release_authority") != "NONE":
        raise LoopFamilyContractError("Permanent governance boundary changed")
    launch = contract.get("family_visual_stage", {})
    if launch.get("audio_switch") != "-NoSound" or launch.get("music_seed_passed_to_visual_launcher") is not False:
        raise LoopFamilyContractError("Visual launcher must be silent and may not consume music_seed")
    if launch.get("launcher_execution") is not False:
        raise LoopFamilyContractError("Family launcher may not execute in this stage")
    audio = contract.get("audio_delivery_envelope", {})
    for field in ("audio_asset_selected", "audio_generated", "pcm_samples_emitted", "audio_payload_materialized", "mux_invoked", "d3_v5_invoked"):
        if audio.get(field) is not False:
            raise LoopFamilyContractError(f"D.1 non-execution boundary changed: {field}")
    return True
