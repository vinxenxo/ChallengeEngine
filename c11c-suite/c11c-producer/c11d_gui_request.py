"""Thin C11-D Production Request helpers for the existing C11-C Producer GUI.

This module deliberately contains no request-normalization, personalization, or
Production Plan rules. Those remain owned by the canonical D4 adapters.
"""
from __future__ import annotations

import copy
import importlib.util
import json
import math
import sys
from pathlib import Path
from typing import Any

APP_INTEGRATION_VERSION = "D9.5.1"
PHASE_KEYS = ("hook_duration", "game_duration", "reveal_duration", "cta_duration")
EDITORIAL_KEYS = ("title", "subtitle", "call_to_action", "language", "player_name", "challenge_label")


def resolve_delivery_profile_data(profile_id: str, delivery_config: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    """Resolve the existing central delivery registry including aliases."""
    profiles = delivery_config.get("profiles", {})
    seen: set[str] = set()
    current = str(profile_id)
    while True:
        if current in seen:
            raise ValueError(f"Delivery profile alias cycle: {profile_id}")
        seen.add(current)
        profile = profiles.get(current)
        if not isinstance(profile, dict):
            raise ValueError(f"Unknown delivery profile: {current}")
        target = profile.get("alias_of")
        if not target:
            return current, profile
        current = str(target)


def calculate_challenge_duration(challenge_document: dict[str, Any]) -> float:
    """Mirror the canonical challenge runner's frame rounding, not Python round()."""
    video = challenge_document.get("video") or {}
    fps = int(video.get("fps", 0))
    if fps <= 0:
        raise ValueError("Challenge video.fps must be positive")
    total_frames = 0
    for key in PHASE_KEYS:
        seconds = float(video.get(key, 0.0))
        if seconds < 0:
            raise ValueError(f"Challenge timeline contains negative duration: {key}")
        total_frames += max(0, int(math.floor((seconds * fps) + 0.5)))
    if total_frames <= 0:
        raise ValueError("Challenge timeline must contain at least one frame")
    if int(math.floor((float(video.get("game_duration", 0.0)) * fps) + 0.5)) <= 0:
        raise ValueError("Challenge game_duration must be greater than zero")
    return total_frames / float(fps)


def build_production_request(
    *,
    request_id: str,
    mode: str,
    challenge_document: dict[str, Any],
    delivery_profile_id: str,
    resolved_delivery_profile: dict[str, Any],
    presentation_profile_id: str | None = None,
    seed: int,
    music_seed: int,
    audio_enabled: bool,
    variation_index: int,
    personalization_enabled: bool,
    editorial_values: dict[str, str],
    source_revision: str = "C11D-D9.5.1",
) -> dict[str, Any]:
    """Map GUI state into the D4.1 request vocabulary; D4 owns validation."""
    challenge_id = str(challenge_document.get("challenge_id", "UNKNOWN"))
    presentation = challenge_document.get("presentation") or {}
    selected_presentation_profile = presentation_profile_id or str(presentation.get("profile", "UNKNOWN"))
    values = {key: str(editorial_values.get(key, "")) for key in EDITORIAL_KEYS}
    if personalization_enabled:
        personalization = {
            "enabled": True,
            "profile_id": "editorial_text_v1",
            "values": {key: values[key] for key in EDITORIAL_KEYS},
        }
    else:
        personalization = {"enabled": False, "profile_id": "none_v1", "values": {}}

    return {
        "request_id": str(request_id),
        "schema_version": "1.0",
        "mode": str(mode),
        "challenge_id": challenge_id,
        # mechanic_version is not interchangeable with challenge_version.
        "challenge_version": "UNKNOWN",
        "seed": int(seed),
        "music_seed": int(music_seed),
        "delivery_profile_id": str(delivery_profile_id),
        "presentation_profile_id": str(selected_presentation_profile),
        "duration_seconds": calculate_challenge_duration(challenge_document),
        "variation_index": int(variation_index),
        "personalization": personalization,
        "editorial": {
            "title": values["title"],
            "subtitle": values["subtitle"],
            "language": values["language"],
            "call_to_action": values["call_to_action"],
        },
        "output": {
            "container": "mp4",
            "width": int(resolved_delivery_profile["width"]),
            "height": int(resolved_delivery_profile["height"]),
            "fps": int(resolved_delivery_profile["fps"]),
            "audio_enabled": bool(audio_enabled),
        },
        "provenance": {
            "source_revision": str(source_revision),
            "request_origin": "GUI",
            "parent_request_id": "UNKNOWN",
        },
    }


def _load_module(name: str, path: Path):
    cache_key = f"_c11d_gui_request_{name}"
    if cache_key in sys.modules:
        return sys.modules[cache_key]
    spec = importlib.util.spec_from_file_location(cache_key, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load canonical module: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[cache_key] = module
    spec.loader.exec_module(module)
    return module


def evaluate_gui_request(request: dict[str, Any], project_root: Path) -> dict[str, Any]:
    """Use D4.6 and D4.5's shared canonical components and prove plan parity."""
    project_root = Path(project_root).resolve()
    d4 = project_root / "tools" / "c11d" / "d4"
    gui_adapter = _load_module("gui_production_adapter", d4 / "gui_production_adapter.py")
    cli_adapter = _load_module("production_cli", d4 / "production_cli.py")

    gui_result = gui_adapter.generate_plan(copy.deepcopy(request))
    cli_raw = copy.deepcopy(request)
    cli_raw.setdefault("provenance", {})["request_origin"] = "CLI"
    schema, registry = gui_adapter.load_pipeline_inputs()
    cli_canonical_unresolved = gui_adapter.normalize_request(cli_raw, schema)
    canonical_request_equal = (
        gui_adapter.NORMALIZER.canonical_json(gui_result["canonical_request"])
        == gui_adapter.NORMALIZER.canonical_json(cli_canonical_unresolved)
    )
    gui_request_hash = gui_result["request_hash"]
    cli_request_hash = gui_adapter.NORMALIZER.request_hash(cli_canonical_unresolved)

    cli_canonical_resolved, cli_plan, cli_plan_hash = cli_adapter.process_request(cli_raw, schema, registry)
    plan_equal = gui_result["plan"] == cli_plan
    plan_hash_equal = gui_result["plan_hash"] == cli_plan_hash
    request_hash_equal = gui_request_hash == cli_request_hash

    plan = gui_result["plan"]
    guard_checks = {
        "runtime_authority_none": plan.get("runtime_authority") == "NONE",
        "renderer_activation_false": plan.get("renderer_activation") is False,
        "gui_activation_false": plan.get("gui_activation") is False,
        "orchestrator_execution_false": plan.get("orchestrator_execution") is False,
        "simulation_truth_mutation_false": plan.get("simulation_truth_mutation") is False,
        "winning_frame_mutation_false": plan.get("winning_frame_mutation") is False,
        "close_calls_mutation_false": plan.get("close_calls_mutation") is False,
        "gameplay_rng_consumption_false": plan.get("gameplay_rng_consumption") is False,
        "structural_rng_consumption_false": plan.get("structural_rng_consumption") is False,
    }
    parity = {
        "schema": "C11-D-D9.5.1-GUI-CLI-PARITY-V1",
        "status": "PASS" if canonical_request_equal and request_hash_equal and plan_equal and plan_hash_equal and all(guard_checks.values()) else "FAIL",
        "gui_request_hash": gui_request_hash,
        "cli_request_hash": cli_request_hash,
        "request_hash_equal": request_hash_equal,
        "canonical_request_equal": canonical_request_equal,
        "gui_plan_hash": gui_result["plan_hash"],
        "cli_plan_hash": cli_plan_hash,
        "plan_equal": plan_equal,
        "plan_hash_equal": plan_hash_equal,
        "guard_checks": guard_checks,
        "execution": False,
        "renderer": False,
        "release_authority": "NONE",
    }
    if parity["status"] != "PASS":
        failed = [key for key, value in guard_checks.items() if not value]
        raise AssertionError(
            "D4 GUI/CLI parity/authority check failed: "
            f"canonical={canonical_request_equal}, request_hash={request_hash_equal}, "
            f"plan={plan_equal}, plan_hash={plan_hash_equal}, guards={failed}"
        )

    return {
        "status": "PLANNED",
        "request": copy.deepcopy(request),
        "canonical_request": gui_result["canonical_request"],
        "resolved_personalization": gui_result["resolved_personalization"],
        "plan": plan,
        "request_hash": gui_request_hash,
        "plan_hash": gui_result["plan_hash"],
        "personalization_hash": gui_adapter.PERSONALIZATION.digest(gui_result["resolved_personalization"]),
        "parity": parity,
        "cli_canonical_request_resolved": cli_canonical_resolved,
        "cli_plan": cli_plan,
        "cli_plan_hash": cli_plan_hash,
        "execution": False,
        "renderer": False,
        "release_authority": "NONE",
    }
