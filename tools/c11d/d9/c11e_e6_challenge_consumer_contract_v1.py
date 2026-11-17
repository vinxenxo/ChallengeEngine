#!/usr/bin/env python3
"""Read-only static preflight for the E6 six-selector Challenge D consumer contract.

This module validates already accepted E1 intents and D envelopes against the
pinned GDScript consumer contract. It deliberately does not invoke Godot,
FFmpeg, FFprobe, audio, mux, render, dispatch, or reserve a BatchId.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import re
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Tuple

PLAN_RUN_ID = "E6CHPLAN_20261117T001949Z_D87FADA4"
PLAN_ROOT = Path("artifacts/tests/c11e/e6_challenge_plan_only") / PLAN_RUN_ID
PLAN_RECEIPT_REL = PLAN_ROOT / "E6_CHALLENGE_PLAN_ONLY_RECEIPT_V1.json"
PLAN_JSON_REL = PLAN_ROOT / "E6_CHALLENGE_SIX_SELECTOR_PLAN_V1.json"
PLAN_RECEIPT_SHA256 = "8fcd63fcfd04df9446f20c5ea8dd1646f169051403f2ee04a356997cd3dd257e"
PLAN_JSON_SHA256 = "ef86fe532cd6c92c3c2dc9937a65d149dc699fcd6c0295382a135413f04af6ae"
RECOVERY_RECEIPT_REL = Path("artifacts/tests/c11e/e6_challenge_plan_only_install/E6CHREC2_20261117T001937Z_659245DC/E6_CHALLENGE_PLAN_ONLY_RECOVERY_RECEIPT_V2.json")
RECOVERY_RECEIPT_SHA256 = "bee886f606a57c3e5f7fce5cd9b3a7f289f868338830f32b930d5f0bd28ddf62"
PREDECESSOR_AUDIT_REL = Path("artifacts/tests/c11e/e6_smoke18_audit/E6AUDITV2_20261116T235057Z_B7FA0492/E6_SMOKE18_READONLY_AUDIT_RECEIPT_V2.json")
PREDECESSOR_AUDIT_SHA256 = "054ed52aefe45cc4d986c4621adbbdb6ca7cf36dc1c4a12cbd76238de86e21fd"
C11C_MANIFEST_SHA256 = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
D4_8_POLICY_SHA256 = "0866b53ad4fcdebe74d01f66864b2dfb00eb644ca28dcd59301c8f3208239c07"
E4A_POLICY_SHA256 = "764629384896a255cf992da89fa427c19f60f9b2e623b81ad17d909674b466b5"
D15_LAYOUT_SHA256 = "3a8e7bfc13a369acaf9d5abe9583f3e93e0990a3b1262b8a839e81ee873c6461"
CONSUMER_SHA256 = "eba81fff4c24ca75033c8f963665df1961136046c41fee0e88681fe55a631203"
ADAPTER_SHA256 = "d17568882eb63ba2eb48649cb9cd46edafe122d72c0c5ed29275e79b8d6d5846"
GENERATOR_SHA256 = "d42782e8f5bb94ff0ede653a1c4624dc91541cc8203abf136b09a8fc288a7d82"
E4A6_BUILDER_SHA256 = "9ea0219f681a912760de3bcdf2469f8a3812a7afe7fb3f5ac569664f354ac18e"
E4A7_WORKER_SHA256 = "a31083dcad457b2621610ae68d180a9797cdeb12537a300150e53ec880ee06de"
E3_AUDIO_PIPELINE_SHA256 = "46b087683a3dcb460601c925373b84e390999d44d73141328285e6c8a633ba5d"
PRODUCER_SCHEMA_SHA256 = "564f11fb4fee9221910dc373550650172eda4f106d6dc25532cc43cb8e6314a0"
E1_SERVICE_SHA256 = "e5dbf9baa72d4c066ff8ba24006df954700d72a5b0f11f9f88aec653e84dce87"
PLAN_BUILDER_SHA256 = "a81ac55ec6ff5f0222c744c9e23f0f140141ca63e35a41df22e3d87c92fe3e64"
PLAN_TEST_SHA256 = "a0bc94acfe5c932bae4516b4822ef94ec5c6ee70d16d16d473ad75fc808dd2e8"
PLAN_RUNNER_SHA256 = "866a3e584356c8a01f5d00a1dbe7df537ceb4d0e0f81512b5d3e393bb04d5c45"

SELECTED_IDS = [
    "CHALLENGE_001", "CHALLENGE_002", "CHALLENGE_004",
    "CHALLENGE_005", "CHALLENGE_006", "CHALLENGE_007",
]
VARIANTS = {
    "A": {"label": "A", "music_seed": 840001},
    "B_REPEAT": {"label": "B_REPEAT", "music_seed": 840001},
    "C_CHANGED_MUSIC_SEED": {"label": "C_CHANGED_MUSIC_SEED", "music_seed": 840002},
}
EXPECTED_FIELDS = ["title", "subtitle", "player_name", "challenge_label", "call_to_action", "language"]
EXPECTED_WINDOWS = {
    "title": ["HOOK"],
    "subtitle": ["HOOK"],
    "player_name": ["HOOK", "GAME"],
    "challenge_label": ["HOOK", "GAME"],
    "call_to_action": ["CTA"],
    "language": [],
}
EXPECTED_REGIONS = {
    "title": "HEADER",
    "subtitle": "HEADER",
    "player_name": "CHALLENGE_OVERLAY",
    "challenge_label": "CHALLENGE_OVERLAY",
    "call_to_action": "FOOTER",
    "language": "METADATA",
}
EXPECTED_MECHANICS = {
    "CHALLENGE_001": ("key", 193847),
    "CHALLENGE_002": ("parking", 987654),
    "CHALLENGE_004": ("parking_v2", 314159),
    "CHALLENGE_005": ("hit_v1", 998877),
    "CHALLENGE_006": ("catch_v1", 884422),
    "CHALLENGE_007": ("find_v1", 7770001),
}

# The 20 source/evidence pins inherited from the accepted Challenge plan receipt.
PINNED_20 = {
    "release/C11C_FREEZE_PACKAGE_MANIFEST.json": C11C_MANIFEST_SHA256,
    "definitions/c11d/production/C11E_D4_8_R1V_QUALIFICATION_ONLY_POLICY_V2.json": D4_8_POLICY_SHA256,
    str(PREDECESSOR_AUDIT_REL).replace("\\", "/"): PREDECESSOR_AUDIT_SHA256,
    "definitions/c11d/production/C11E_E4A_CHALLENGE_EDITORIAL_PRESENTATION_POLICY_APPROVAL_V1.json": E4A_POLICY_SHA256,
    "docs/current/d/D1.5_PLATFORM_LAYOUT_TEMPLATE_CONTRACT.md": D15_LAYOUT_SHA256,
    "tools/c11d/d9/C11EChallengeLiveEditorialConsumer.gd": CONSUMER_SHA256,
    "tools/c11d/d9/c11e_e4a6_challenge_live_editorial_envelope.py": E4A6_BUILDER_SHA256,
    "tools/c11d/d9/c11e_e4a_challenge_av_review.py": E4A7_WORKER_SHA256,
    "c11c-suite/c11c-producer/c11e_e3_audio_pipeline.py": E3_AUDIO_PIPELINE_SHA256,
    "c11c-suite/c11c-producer/producer_schema.json": PRODUCER_SCHEMA_SHA256,
    "c11c-suite/c11c-producer/c11e_production_service.py": E1_SERVICE_SHA256,
    "artifacts/tests/c11e/e4a_d_composited_av_review/RUN_20261106T070808Z-62F31F9C/C11E_E4A7_D_COMPOSITED_CHALLENGE_AV_RECEIPT.json": "102cf07a0b8920318c3ba211a3bd4374c3e080018486363d701f81e65613aaa0",
    "GeneradorMaestro.gd": GENERATOR_SHA256,
    "challenges/CHALLENGE_001.json": "ec8925fa5b4ab996a791c8cf7f5b139470774720f57880c5b01b2d0aa5b57bea",
    "challenges/CHALLENGE_002.json": "db5d70a28c460e986e785c6787447529372ac5ea3b5a7ff0507667decbe2a160",
    "challenges/CHALLENGE_003.json": "38cb0166482c5ba4862deef8ab75dad4a6e1524590b6850312bab5238f078419",
    "challenges/CHALLENGE_004.json": "6a674c02c2d8831a872691954f1cc40e2492193f9b136f60656730a7be686b71",
    "challenges/CHALLENGE_005.json": "e173736fcbb0e340cd250be1111fa9d38489934d55cc0e0c93835c66f9596e30",
    "challenges/CHALLENGE_006.json": "2d7d7397cbb0a2109f300859a5d7c0830ded0553522a5120f61750f5bc0b5694",
    "challenges/CHALLENGE_007.json": "269f9588e5a6b7d253e2e944440cc41dc3a9db8967775ffa819edebe729a3a61",
}
PINNED_EXTRA = {
    "tools/c11d/d9/c11e_challenge_editorial_presentation_adapter.gd": ADAPTER_SHA256,
    "tools/c11d/d9/c11e_e6_challenge_plan_only_v1.py": PLAN_BUILDER_SHA256,
    "tools/c11d/d9/test_c11e_e6_challenge_plan_only_v1.py": PLAN_TEST_SHA256,
    "tools/c11d/d9/RUN_C11E_E6_CHALLENGE_PLAN_ONLY_V1.ps1": PLAN_RUNNER_SHA256,
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def assert_sha(path: Path, expected: str, label: str) -> str:
    require(path.is_file(), f"MISSING_FILE:{label}:{path}")
    actual = sha256_file(path)
    require(actual == expected, f"SHA_MISMATCH:{label}:expected={expected}:actual={actual}")
    return actual


def load_sidecar(path: Path) -> str:
    sidecar = Path(str(path) + ".sha256")
    require(sidecar.is_file(), f"MISSING_SIDECAR:{path.name}")
    token = sidecar.read_text(encoding="ascii", errors="strict").strip().split()[0].lower()
    require(re.fullmatch(r"[0-9a-f]{64}", token) is not None, f"INVALID_SIDECAR:{sidecar.name}")
    return token


def build_phase_ranges(row: Mapping[str, Any]) -> List[Dict[str, Any]]:
    ranges: List[Dict[str, Any]] = []
    cursor = 0
    for phase in ("HOOK", "GAME", "REVEAL", "CTA"):
        matches = [x for x in row["phase_ranges"] if x.get("phase") == phase]
        require(len(matches) == 1, f"PLAN_PHASE_MISSING_OR_DUPLICATE:{row.get('challenge_id')}:{phase}")
        source = matches[0]
        start = int(source["start_frame"])
        end = int(source["end_frame"])
        require(start == cursor, f"PLAN_PHASE_CURSOR_GAP:{row.get('challenge_id')}:{phase}")
        ranges.append({
            "phase": phase,
            "start_frame": start,
            "end_frame": end,
            "timebase": "SOURCE_FPS_HALF_OPEN",
        })
        cursor = end
    require(cursor == int(row["source_frames"]), f"PLAN_PHASE_TOTAL_MISMATCH:{row.get('challenge_id')}")
    return ranges


def validate_consumer_source(project_root: Path) -> Dict[str, Any]:
    consumer_path = project_root / "tools/c11d/d9/C11EChallengeLiveEditorialConsumer.gd"
    adapter_path = project_root / "tools/c11d/d9/c11e_challenge_editorial_presentation_adapter.gd"
    generator_path = project_root / "GeneradorMaestro.gd"
    consumer = consumer_path.read_text(encoding="utf-8")
    adapter = adapter_path.read_text(encoding="utf-8")
    generator = generator_path.read_text(encoding="utf-8")

    required_consumer_fragments = [
        'const EnvelopeSchema := "C11E-CHALLENGE-LIVE-EDITORIAL-ENVELOPE-V1"',
        f'const ApprovedPolicySha := "{E4A_POLICY_SHA256}"',
        f'const LayoutContractSha := "{D15_LAYOUT_SHA256}"',
        'const ExpectedFields := ["title", "subtitle", "player_name", "challenge_label", "call_to_action", "language"]',
        '"title": ["HOOK"]', '"subtitle": ["HOOK"]',
        '"player_name": ["HOOK", "GAME"]', '"challenge_label": ["HOOK", "GAME"]',
        '"call_to_action": ["CTA"]', '"language": []',
        '"title": "HEADER"', '"subtitle": "HEADER"',
        '"player_name": "CHALLENGE_OVERLAY"', '"challenge_label": "CHALLENGE_OVERLAY"',
        '"call_to_action": "FOOTER"', '"language": "METADATA"',
        'str(envelope.get("challenge_id", "")) != challenge_id',
        'str(selection.get("variant_id", "")) != challenge_id',
        'int(timebase.get("fps", -1)) != timeline.fps',
        'int(timebase.get("total_frames", -1)) != timeline.total_frames',
        'str(timebase.get("kind", "")) != "SOURCE_FRAME_INDEX"',
        'governance.get("renderer_input_emitted") != false',
        'str(governance.get("release_authority", "")) != "NONE"',
    ]
    missing = [fragment for fragment in required_consumer_fragments if fragment not in consumer]
    require(not missing, f"CONSUMER_CONTRACT_SOURCE_DRIFT:{missing}")

    required_adapter_fragments = [
        'static func resolve_hook_countdown_option(intent: Dictionary) -> Dictionary:',
        'str(request.get("content_type", "")) != "challenges"',
        'str(selection_value.get("content_type", "")) != "challenges"',
    ]
    missing_adapter = [fragment for fragment in required_adapter_fragments if fragment not in adapter]
    require(not missing_adapter, f"ADAPTER_SOURCE_DRIFT:{missing_adapter}")
    require("CHALLENGE_004" not in adapter, "ADAPTER_IS_NOT_SELECTOR_GENERIC_ANYMORE")

    require('load("res://tools/c11d/d9/C11EChallengeLiveEditorialConsumer.gd")' in generator,
            "GENERATOR_NO_LONGER_LOADS_PINNED_D_CONSUMER")
    require("--c11e-editorial-envelope" in generator, "GENERATOR_ENVELOPE_CLI_ARGUMENT_MISSING")
    require("configure_from_file(" in generator, "GENERATOR_NO_LONGER_CONFIGURES_CONSUMER")
    require(generator.count("_apply_c11e_live_editorial_after_native_bind(rm)") == 4,
            "GENERATOR_PHASE_APPLICATION_COUNT_NOT_FOUR")
    require(generator.count("social_ui_binder.bind_render_model(rm)") >= 4,
            "GENERATOR_NATIVE_BINDER_PHASE_CALLS_MISSING")
    require("func _expected_phase_ranges(timeline: VideoTimeline)" in consumer,
            "CONSUMER_PHASE_RANGE_FUNCTION_MISSING")

    # The three legacy media helpers remain scoped; don't mistake the generic
    # live consumer for an audiovisual batch executor.
    e4a6 = (project_root / "tools/c11d/d9/c11e_e4a6_challenge_live_editorial_envelope.py").read_text(encoding="utf-8")
    e4a7 = (project_root / "tools/c11d/d9/c11e_e4a_challenge_av_review.py").read_text(encoding="utf-8")
    e3 = (project_root / "c11c-suite/c11c-producer/c11e_e3_audio_pipeline.py").read_text(encoding="utf-8")
    require('CHALLENGE_004' in e4a6, "E4A6_SCOPE_PIN_NOT_VISIBLE")
    require('CHALLENGE_004' in e4a7, "E4A7_SCOPE_PIN_NOT_VISIBLE")
    require('CHALLENGE_001' in e3, "E3_AUDIO_SCOPE_PIN_NOT_VISIBLE")
    return {
        "consumer_dynamic_challenge_identity": True,
        "consumer_exact_six_field_contract": True,
        "consumer_native_timebase_and_phase_contract": True,
        "adapter_challenge_only_option_contract": True,
        "generator_existing_optional_envelope_path": True,
        "generator_native_bind_then_d_apply_four_phases": True,
        "legacy_e4a6_scope": "CHALLENGE_004_ONLY",
        "legacy_e4a7_scope": "CHALLENGE_004_ONLY",
        "legacy_e3_audio_scope": "CHALLENGE_001_ONLY",
        "godot_runtime": "NOT_RUN_NOT_PROVEN",
    }


def validate_intent(intent: Mapping[str, Any], row: Mapping[str, Any], variant: str,
                    expected_request_id: str) -> None:
    challenge_id = str(row["challenge_id"])
    require(intent.get("schema") == "C11-E-PRODUCTION-INTENT-V1", f"INTENT_SCHEMA:{challenge_id}:{variant}")
    require(intent.get("status") == "PREPARED_E1_NOT_DISPATCHED", f"INTENT_STATUS:{challenge_id}:{variant}")
    require(intent.get("request_origin") == "TEST", f"INTENT_ORIGIN:{challenge_id}:{variant}")
    req = intent.get("request") or {}
    selection = req.get("selection") or {}
    require(req.get("request_id") == expected_request_id, f"INTENT_REQUEST_ID:{challenge_id}:{variant}")
    require(req.get("content_type") == "challenges" and req.get("mode") == "REVIEW", f"INTENT_REQUEST_SCOPE:{challenge_id}:{variant}")
    require(selection.get("content_type") == "challenges", f"INTENT_SELECTION_TYPE:{challenge_id}:{variant}")
    require(selection.get("variant_id") == challenge_id, f"INTENT_SELECTOR:{challenge_id}:{variant}")
    require(selection.get("family_id") == row["family_id"], f"INTENT_FAMILY:{challenge_id}:{variant}")
    require(selection.get("variant_scope_id") == f"challenge:{challenge_id}", f"INTENT_VARIANT_SCOPE:{challenge_id}:{variant}")
    require(req.get("presentation_options") == {"show_hook_countdown": True}, f"INTENT_PRESENTATION_OPTIONS:{challenge_id}:{variant}")
    require(int(req.get("variation_index", -1)) == 0, f"INTENT_VARIATION:{challenge_id}:{variant}")
    identity = intent.get("identity") or {}
    intent_hash = str(identity.get("intent_hash", ""))
    require(re.fullmatch(r"[0-9a-f]{64}", intent_hash) is not None, f"INTENT_IDENTITY_HASH:{challenge_id}:{variant}")
    seeds = intent.get("seed_domains") or {}
    require(seeds.get("independent_domains") is True, f"SEED_DOMAINS_NOT_INDEPENDENT:{challenge_id}:{variant}")
    require(seeds.get("cross_domain_sharing") == "FORBIDDEN", f"SEED_DOMAIN_SHARING:{challenge_id}:{variant}")
    require((seeds.get("gameplay") or {}).get("field") == "request.seed", f"GAMEPLAY_SEED_FIELD:{challenge_id}:{variant}")
    require(int((seeds.get("gameplay") or {}).get("value", -1)) == int(row["gameplay_seed"]), f"GAMEPLAY_SEED:{challenge_id}:{variant}")
    exp_music = VARIANTS[variant]["music_seed"]
    require((seeds.get("music") or {}).get("field") == "request.music_seed", f"MUSIC_SEED_FIELD:{challenge_id}:{variant}")
    require(int((seeds.get("music") or {}).get("value", -1)) == exp_music, f"MUSIC_SEED:{challenge_id}:{variant}")
    require(seeds.get("automatic_generation") is False and seeds.get("runtime_derivation") is False,
            f"SEED_AUTO_DERIVATION:{challenge_id}:{variant}")
    execution = intent.get("execution_boundary") or {}
    require(execution.get("d4_8") == "BLOCKED", f"INTENT_D4_8:{challenge_id}:{variant}")
    for flag in ("dispatch_authorized", "media_created", "production_execution", "renderer_activation",
                 "renderer_dispatch_invoked", "renderer_input_emitted"):
        require(execution.get(flag) is False, f"INTENT_EXECUTION_FLAG:{challenge_id}:{variant}:{flag}")
    require(execution.get("release_authority") == "NONE", f"INTENT_RELEASE_AUTHORITY:{challenge_id}:{variant}")
    adapter = intent.get("family_adapter") or {}
    require(adapter.get("status") == "NOT_CONNECTED_E1", f"INTENT_ADAPTER_BOUNDARY:{challenge_id}:{variant}")
    music = intent.get("music_contract") or {}
    require(music.get("status") == "PLANNED_NOT_RENDERED", f"MUSIC_STATUS:{challenge_id}:{variant}")
    require(music.get("engine_invoked") is False and music.get("audio_created") is False,
            f"MUSIC_ENGINE_INVOKED:{challenge_id}:{variant}")
    require(music.get("ffmpeg_mux_invoked") is False and music.get("dispatch_authorized") is False,
            f"MUSIC_MUX_OR_DISPATCH:{challenge_id}:{variant}")
    engine_request = music.get("engine_request") or {}
    require(engine_request.get("tempo_bpm") is None and engine_request.get("duration_seconds") is None,
            f"MUSIC_PARAMETERS_NOT_UNRESOLVED:{challenge_id}:{variant}")
    require(music.get("unresolved_engine_parameters") == ["tempo_bpm", "duration_seconds"],
            f"MUSIC_UNRESOLVED_LIST:{challenge_id}:{variant}")
    output = intent.get("output") or {}
    require(output.get("created") is False and output.get("planned_root_exists") is False,
            f"OUTPUT_CREATED:{challenge_id}:{variant}")


def validate_envelope(envelope: Mapping[str, Any], row: Mapping[str, Any], intent: Mapping[str, Any],
                       variant: str) -> None:
    challenge_id = str(row["challenge_id"])
    require(envelope.get("schema") == "C11E-CHALLENGE-LIVE-EDITORIAL-ENVELOPE-V1", f"ENVELOPE_SCHEMA:{challenge_id}:{variant}")
    require(envelope.get("schema_version") == "1.0", f"ENVELOPE_SCHEMA_VERSION:{challenge_id}:{variant}")
    require(envelope.get("status") == "PREPARED_E1_NOT_DISPATCHED", f"ENVELOPE_STATUS:{challenge_id}:{variant}")
    require(envelope.get("content_type") == "challenges", f"ENVELOPE_CONTENT_TYPE:{challenge_id}:{variant}")
    require(envelope.get("challenge_id") == challenge_id, f"ENVELOPE_CHALLENGE_ID:{challenge_id}:{variant}")
    nested = envelope.get("e1_intent") or {}
    require(nested == intent, f"ENVELOPE_NESTED_INTENT_MISMATCH:{challenge_id}:{variant}")
    req = nested.get("request") or {}
    require(envelope.get("request_id") == req.get("request_id"), f"ENVELOPE_REQUEST_ID:{challenge_id}:{variant}")
    require(envelope.get("intent_hash") == (nested.get("identity") or {}).get("intent_hash"), f"ENVELOPE_INTENT_HASH:{challenge_id}:{variant}")
    require(envelope.get("presentation_options") == req.get("presentation_options"), f"ENVELOPE_PRESENTATION_OPTIONS:{challenge_id}:{variant}")

    timebase = envelope.get("source_timebase") or {}
    require(timebase.get("kind") == "SOURCE_FRAME_INDEX", f"TIMEBASE_KIND:{challenge_id}:{variant}")
    require(int(timebase.get("fps", -1)) == int(row["source_fps"]) == 60, f"TIMEBASE_FPS:{challenge_id}:{variant}")
    require(int(timebase.get("total_frames", -1)) == int(row["source_frames"]), f"TIMEBASE_FRAMES:{challenge_id}:{variant}")
    expected_ranges = build_phase_ranges(row)
    actual_ranges = envelope.get("source_phase_ranges")
    require(actual_ranges == expected_ranges, f"PHASE_RANGES:{challenge_id}:{variant}")

    require(envelope.get("policy_sha256") == E4A_POLICY_SHA256, f"POLICY_SHA:{challenge_id}:{variant}")
    require(envelope.get("layout_contract_sha256") == D15_LAYOUT_SHA256, f"LAYOUT_SHA:{challenge_id}:{variant}")
    fields = envelope.get("fields")
    require(isinstance(fields, list) and len(fields) == len(EXPECTED_FIELDS), f"FIELD_COUNT:{challenge_id}:{variant}")
    by_name = {}
    for field in fields:
        require(isinstance(field, dict), f"FIELD_ROW_TYPE:{challenge_id}:{variant}")
        name = field.get("field")
        require(name in EXPECTED_FIELDS and name not in by_name, f"FIELD_NAME_DUPLICATE_OR_UNKNOWN:{challenge_id}:{variant}:{name}")
        by_name[name] = field
    require(set(by_name) == set(EXPECTED_FIELDS), f"FIELD_ALLOWLIST:{challenge_id}:{variant}")
    for name in EXPECTED_FIELDS:
        field = by_name[name]
        require(field.get("region") == EXPECTED_REGIONS[name], f"FIELD_REGION:{challenge_id}:{variant}:{name}")
        require(field.get("source_phase_windows") == EXPECTED_WINDOWS[name], f"FIELD_WINDOWS:{challenge_id}:{variant}:{name}")
        require(field.get("policy_sha256") == E4A_POLICY_SHA256, f"FIELD_POLICY_SHA:{challenge_id}:{variant}:{name}")
        require(field.get("layout_contract_sha256") == D15_LAYOUT_SHA256, f"FIELD_LAYOUT_SHA:{challenge_id}:{variant}:{name}")
        effective = str(field.get("effective_value", ""))
        require(effective == "", f"FIELD_NOT_EMPTY_IN_PREFLIGHT:{challenge_id}:{variant}:{name}")
        require(field.get("disposition") == "OMITTED_EMPTY", f"FIELD_DISPOSITION:{challenge_id}:{variant}:{name}")
        require(field.get("value_sha256") == sha256_bytes(effective.encode("utf-8")), f"FIELD_VALUE_SHA:{challenge_id}:{variant}:{name}")
        require(field.get("source_value_sha256") == sha256_bytes(b"UNKNOWN"), f"FIELD_SOURCE_VALUE_SHA:{challenge_id}:{variant}:{name}")
        wanted = []
        for phase in EXPECTED_WINDOWS[name]:
            wanted.extend(x for x in expected_ranges if x["phase"] == phase)
        require(field.get("source_frame_ranges") == wanted, f"FIELD_FRAME_RANGES:{challenge_id}:{variant}:{name}")

    gov = envelope.get("governance") or {}
    for flag in ("renderer_input_emitted", "production_dispatch", "media_created"):
        require(gov.get(flag) is False, f"ENVELOPE_GOVERNANCE_FLAG:{challenge_id}:{variant}:{flag}")
    require(gov.get("release_authority") == "NONE", f"ENVELOPE_RELEASE_AUTHORITY:{challenge_id}:{variant}")
    require(gov.get("d4_8") == "BLOCKED", f"ENVELOPE_D4_8:{challenge_id}:{variant}")
    require(gov.get("d9_10") == "PREPARE_ONLY", f"ENVELOPE_D9_10:{challenge_id}:{variant}")


def check_canonical_row(project_root: Path, row: Mapping[str, Any]) -> None:
    challenge_id = str(row["challenge_id"])
    canonical = load_json(project_root / str(row["canonical_source"]))
    mechanic, seed = EXPECTED_MECHANICS[challenge_id]
    require(canonical.get("challenge_id") == challenge_id, f"CANONICAL_ID:{challenge_id}")
    require(canonical.get("mechanic") == mechanic == row.get("mechanic"), f"CANONICAL_MECHANIC:{challenge_id}")
    require(int((canonical.get("generation") or {}).get("seed", -1)) == seed == int(row["gameplay_seed"]), f"CANONICAL_SEED:{challenge_id}")
    video = canonical.get("video") or {}
    fps = int(video.get("fps", -1))
    require(fps == 60 == int(row["source_fps"]), f"CANONICAL_FPS:{challenge_id}")
    cursor = 0
    expected_phases = []
    for phase in ("HOOK", "GAME", "REVEAL", "CTA"):
        key = {"HOOK": "hook_duration", "GAME": "game_duration", "REVEAL": "reveal_duration", "CTA": "cta_duration"}[phase]
        duration = float(video.get(key, 0.0))
        frames = int(round(duration * fps))
        expected_phases.append((phase, duration, cursor, cursor + frames))
        cursor += frames
    observed = [(x["phase"], float(x["duration_seconds"]), int(x["start_frame"]), int(x["end_frame"])) for x in row["phase_ranges"]]
    require(observed == expected_phases, f"CANONICAL_PHASE_TIMELINE:{challenge_id}")
    require(cursor == int(row["source_frames"]), f"CANONICAL_SOURCE_FRAMES:{challenge_id}")
    require(float(row["phase_sum_seconds"]) == cursor / fps, f"CANONICAL_PHASE_SUM:{challenge_id}")
    require(int(row["proposed_review_fps"]) == 30, f"REVIEW_FPS_PROPOSAL:{challenge_id}")
    require(int(row["proposed_review_frames"]) == cursor // 2, f"REVIEW_FRAME_DERIVATION:{challenge_id}")


def check_file_and_sidecar(path: Path, expected: str, label: str) -> str:
    actual = assert_sha(path, expected, label)
    side_sha = load_sidecar(path)
    require(side_sha == expected, f"SIDECAR_SHA_MISMATCH:{label}:expected={expected}:sidecar={side_sha}")
    return actual


def perform_audit(project_root: Path, run_id: str) -> Dict[str, Any]:
    project_root = project_root.resolve()
    source_rows = []
    for rel, expected in {**PINNED_20, **PINNED_EXTRA}.items():
        path = project_root / rel
        actual = sha256_file(path) if path.is_file() else None
        source_rows.append({"path": rel, "expected_sha256": expected, "actual_sha256": actual,
                            "status": "PASS" if actual == expected else ("MISSING" if actual is None else "MISMATCH")})
    failures = [f"SOURCE_PIN_{x['status']}:{x['path']}:{x['actual_sha256']}" for x in source_rows if x["status"] != "PASS"]

    plan_receipt_path = project_root / PLAN_RECEIPT_REL
    plan_json_path = project_root / PLAN_JSON_REL
    recovery_path = project_root / RECOVERY_RECEIPT_REL
    predecessor_path = project_root / PREDECESSOR_AUDIT_REL
    plan_receipt: Dict[str, Any] = {}
    plan_json: Dict[str, Any] = {}
    recovery: Dict[str, Any] = {}
    predecessor: Dict[str, Any] = {}
    d4_policy: Dict[str, Any] = {}
    try:
        check_file_and_sidecar(plan_receipt_path, PLAN_RECEIPT_SHA256, "PLAN_RECEIPT")
        check_file_and_sidecar(plan_json_path, PLAN_JSON_SHA256, "PLAN_JSON")
        check_file_and_sidecar(recovery_path, RECOVERY_RECEIPT_SHA256, "RECOVERY_RECEIPT")
        assert_sha(predecessor_path, PREDECESSOR_AUDIT_SHA256, "PREDECESSOR_E6_AUDIT")
        plan_receipt = load_json(plan_receipt_path)
        plan_json = load_json(plan_json_path)
        recovery = load_json(recovery_path)
        predecessor = load_json(predecessor_path)
        d4_policy = load_json(project_root / "definitions/c11d/production/C11E_D4_8_R1V_QUALIFICATION_ONLY_POLICY_V2.json")
    except Exception as exc:
        failures.append(f"EVIDENCE_LOAD_OR_PIN_FAILURE:{exc}")

    consumer_status: Dict[str, Any] = {}
    try:
        consumer_status = validate_consumer_source(project_root)
    except Exception as exc:
        failures.append(f"CONSUMER_SOURCE_CONTRACT_FAILURE:{exc}")

    detail_rows: List[Dict[str, Any]] = []
    intent_pass = 0
    envelope_pass = 0
    try:
        require(plan_receipt.get("run_id") == PLAN_RUN_ID, "PLAN_RECEIPT_RUN_ID")
        require(plan_receipt.get("status") == "PASS_E1_AND_D_ENVELOPE_PLANS_18_OF_18_EXECUTION_HELD", "PLAN_RECEIPT_STATUS")
        require(plan_receipt.get("c11c_frozen_manifest_sha256") == C11C_MANIFEST_SHA256, "PLAN_RECEIPT_C11C_SHA")
        require(plan_receipt.get("d4_8_policy_sha256") == D4_8_POLICY_SHA256, "PLAN_RECEIPT_D4_8_SHA")
        require(plan_receipt.get("source_pins", {}).get("expected") == 20 and plan_receipt.get("source_pins", {}).get("passed") == 20, "PLAN_RECEIPT_SOURCE_PINS")
        require(plan_receipt.get("e1_intents", {}).get("expected") == 18 and plan_receipt.get("e1_intents", {}).get("passed") == 18, "PLAN_RECEIPT_INTENT_COUNTS")
        require(plan_receipt.get("d_envelopes", {}).get("expected") == 18 and plan_receipt.get("d_envelopes", {}).get("passed") == 18, "PLAN_RECEIPT_ENVELOPE_COUNTS")
        require(plan_receipt.get("predecessor_e6_audit", {}).get("receipt_sha256") == PREDECESSOR_AUDIT_SHA256, "PREDECESSOR_AUDIT_LINK")
        require(recovery.get("status") == "PASS_ADD_ONLY_IDEMPOTENT_RECOVERY", "RECOVERY_RECEIPT_STATUS")
        require(recovery.get("run_id") == "E6CHREC2_20261117T001937Z_659245DC", "RECOVERY_RUN_ID")
        require(recovery.get("files_expected") == 7 and recovery.get("files_final_verified") == 7 and recovery.get("files_added") == 0 and recovery.get("files_skipped_identical") == 7, "RECOVERY_FILE_COUNTS")
        require(predecessor.get("status") == "PASS_AUDIT_READ_ONLY_EVIDENCE_RECONCILED_EXECUTION_HELD", "PREDECESSOR_AUDIT_STATUS")
        d4_forbidden = d4_policy.get("forbidden", {})
        d4_allowances = d4_policy.get("allowances", {})
        d4_governance = d4_policy.get("governance", {})
        require(d4_forbidden.get("smoke18_or_matrix99") is True, "D4_8_DOES_NOT_EXPLICITLY_FORBID_SMOKE18")
        require(d4_forbidden.get("d3_music_engine") is True and d4_forbidden.get("pcm_audio_generation") is True, "D4_8_AUDIO_FORBIDDEN_FLAGS_CHANGED")
        require(d4_forbidden.get("ffmpeg_filter_or_mux") is True, "D4_8_FFMPEG_FILTER_MUX_FORBIDDEN_FLAG_CHANGED")
        require(d4_allowances.get("audio_or_music_generation") is False and d4_allowances.get("ffmpeg_filters") is False and d4_allowances.get("ffmpeg_mux") is False, "D4_8_MEDIA_ALLOWANCES_CHANGED")
        require(d4_allowances.get("d9_10_renderer_consumer_dispatch") is False, "D4_8_RENDERER_DISPATCH_ALLOWANCE_CHANGED")
        require(d4_governance.get("d4_8_general_production") == "BLOCKED" and d4_governance.get("d_renderer_dispatch") == "OFF", "D4_8_GOVERNANCE_CHANGED")
        require(d4_governance.get("release_authority") == "NONE", "D4_8_RELEASE_AUTHORITY_CHANGED")

        pool = plan_receipt.get("challenge_matrix", {}).get("candidate_pool", [])
        require(len(pool) == 7, "CANONICAL_CANDIDATE_POOL_COUNT")
        by_id = {str(x.get("challenge_id")): x for x in pool}
        require(set(by_id) == {"CHALLENGE_001", "CHALLENGE_002", "CHALLENGE_003", "CHALLENGE_004", "CHALLENGE_005", "CHALLENGE_006", "CHALLENGE_007"}, "CANONICAL_CANDIDATE_POOL_IDS")
        require(by_id["CHALLENGE_003"].get("selection_disposition") == "EXCLUDED_PILOT_DUPLICATE_GAMEPLAY_SEED", "CHALLENGE_003_EXCLUSION")
        require("CHALLENGE_008" not in by_id and "CHALLENGE_009" not in by_id, "CHALLENGE_008_009_POOL_EXCLUSION")
        selected = plan_receipt.get("challenge_matrix", {}).get("selected_rows", [])
        require([x.get("challenge_id") for x in selected] == SELECTED_IDS, "SELECTED_MATRIX_ORDER")
        require(plan_json.get("selected_ids") == SELECTED_IDS and plan_json.get("status") == "PREPARED_PLAN_ONLY_NOT_FROZEN_FOR_MEDIA", "PLAN_JSON_STATUS_OR_IDS")
        require(plan_json.get("execution", {}).get("e6_test_only_authorized") is False, "PLAN_JSON_MEDIA_AUTHORITY")
        require(plan_json.get("music_test_fixture_proposal", {}).get("status") == "PROPOSED_E6_TEST_ONLY_NOT_PRODUCT_DEFAULT", "MUSIC_FIXTURE_STATUS")
        require(plan_json.get("music_test_fixture_proposal", {}).get("e1_contract_remains_unresolved") == ["tempo_bpm", "duration_seconds"], "MUSIC_PARAMETERS_UNRESOLVED")

        e1_rows = {(x["challenge_id"], x["label"]): x for x in plan_receipt.get("e1_intents", {}).get("rows", [])}
        d_rows = {(x["challenge_id"], x["label"]): x for x in plan_receipt.get("d_envelopes", {}).get("rows", [])}
        require(len(e1_rows) == 18 and len(d_rows) == 18, "PLAN_ROW_UNIQUENESS")
        for row in selected:
            challenge_id = row["challenge_id"]
            check_canonical_row(project_root, row)
            for variant, meta in VARIANTS.items():
                key = (challenge_id, variant)
                erow = e1_rows.get(key)
                drow = d_rows.get(key)
                require(erow is not None and drow is not None, f"PLAN_MATRIX_ROW_MISSING:{challenge_id}:{variant}")
                intent_path = project_root / erow["intent_path"]
                envelope_path = project_root / drow["envelope_path"]
                intent_expected_sha = str(erow["intent_sha256"])
                envelope_expected_sha = str(drow["envelope_sha256"])
                check_file_and_sidecar(intent_path, intent_expected_sha, f"INTENT:{challenge_id}:{variant}")
                check_file_and_sidecar(envelope_path, envelope_expected_sha, f"ENVELOPE:{challenge_id}:{variant}")
                intent = load_json(intent_path)
                envelope = load_json(envelope_path)
                validate_intent(intent, row, variant, erow["request_id"])
                validate_envelope(envelope, row, intent, variant)
                require(drow.get("intent_hash") == (intent.get("identity") or {}).get("intent_hash"), f"PLAN_D_ROW_INTENT_HASH:{challenge_id}:{variant}")
                require(drow.get("source_fps") == row["source_fps"] and drow.get("source_frames") == row["source_frames"], f"PLAN_D_ROW_TIMEBASE:{challenge_id}:{variant}")
                intent_pass += 1
                envelope_pass += 1
                detail_rows.append({"challenge_id": challenge_id, "variant": variant, "intent_sha256": intent_expected_sha,
                                    "envelope_sha256": envelope_expected_sha, "gameplay_seed": row["gameplay_seed"],
                                    "music_seed": meta["music_seed"], "source_fps": row["source_fps"],
                                    "source_frames": row["source_frames"], "status": "PASS_STATIC_CONTRACT"})

        # Cross-variant relations: A and B repeat the same independent domains;
        # C changes only music seed while preserving gameplay identity.
        for challenge_id in SELECTED_IDS:
            variants = {}
            for variant in VARIANTS:
                erow = e1_rows[(challenge_id, variant)]
                variants[variant] = load_json(project_root / erow["intent_path"])
            seeds = {v: (obj["seed_domains"]["gameplay"]["value"], obj["seed_domains"]["music"]["value"]) for v, obj in variants.items()}
            require(seeds["A"] == (seeds["B_REPEAT"][0], seeds["B_REPEAT"][1]), f"AB_SEED_REPEAT:{challenge_id}")
            require(seeds["A"][0] == seeds["C_CHANGED_MUSIC_SEED"][0], f"C_GAMEPLAY_SEED_CHANGED:{challenge_id}")
            require(seeds["A"][1] != seeds["C_CHANGED_MUSIC_SEED"][1], f"C_MUSIC_SEED_NOT_CHANGED:{challenge_id}")
        selected_gameplay_seeds = [int(x["gameplay_seed"]) for x in selected]
        require(len(set(selected_gameplay_seeds)) == 6, "SELECTED_GAMEPLAY_SEEDS_NOT_DISTINCT")
    except Exception as exc:
        failures.append(f"PLAN_OR_ENVELOPE_CONTRACT_FAILURE:{exc}")

    blockers = [
        "STATIC_PREFLIGHT_DOES_NOT_PROVE_GODOT_RUNTIME_FOR_SIX_CHALLENGE_TIMELINES",
        "FAMILY_OWNED_MULTI_SELECTOR_CHALLENGE_AV_EXECUTOR_NOT_PROVEN",
        "MUSIC_FIXTURE_840001_840002_104BPM_REMAINS_PROPOSAL_ONLY;TEMPO_AND_DURATION_UNRESOLVED",
        "D4_8_R1V_V2_UNCHANGED_AND_PROHIBITS_SMOKE18_AUDIO_AND_FFMPEG_MUX",
    ]
    status = "PASS_STATIC_CONSUMER_CONTRACT_18_OF_18_EXECUTION_HELD" if not failures else "FAIL_STATIC_CONSUMER_CONTRACT_PREFLIGHT"
    receipt = {
        "schema": "C11E-E6-CHALLENGE-CONSUMER-CONTRACT-PREFLIGHT-RECEIPT-V1",
        "schema_version": "1.0",
        "run_id": run_id,
        "created_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "status": status,
        "project_root": str(project_root),
        "plan_run_id": PLAN_RUN_ID,
        "plan_receipt_sha256": PLAN_RECEIPT_SHA256,
        "plan_json_sha256": PLAN_JSON_SHA256,
        "predecessor_e6_audit_receipt_sha256": PREDECESSOR_AUDIT_SHA256,
        "recovery_receipt_sha256": RECOVERY_RECEIPT_SHA256,
        "source_pins": {"expected": 24, "passed": sum(1 for x in source_rows if x["status"] == "PASS"), "rows": source_rows},
        "consumer_static_contract": consumer_status,
        "e1_intents": {"expected": 18, "passed": intent_pass},
        "d_envelopes": {"expected": 18, "passed": envelope_pass},
        "negative_control_tests": "see focused unittest results",
        "selected_ids": SELECTED_IDS,
        "selected_rows": detail_rows,
        "executor_scope": {
            "generic_gdscript_consumer": "DYNAMIC_CHALLENGE_IDENTITY_STATICALLY_VERIFIED",
            "generic_d_presentation_adapter": "CHALLENGE_ONLY_OPTION_CONTRACT_STATICALLY_VERIFIED",
            "e4a6_envelope_builder": "CHALLENGE_004_ONLY",
            "e4a7_av_worker": "CHALLENGE_004_ONLY",
            "e3_audio_pipeline": "CHALLENGE_001_ONLY",
            "family_owned_multi_selector_av_executor": "NOT_PROVEN",
            "godot_runtime": "NOT_RUN",
        },
        "music_fixture": {
            "music_seed_a_b": 840001,
            "music_seed_c": 840002,
            "tempo_bpm": 104,
            "status": "PROPOSAL_ONLY_NOT_PRODUCT_DEFAULT_NOT_AUTHORIZED",
            "unresolved_engine_parameters": ["tempo_bpm", "duration_seconds"],
        },
        "blockers": blockers,
        "failures": failures,
        "execution": {
            "godot_invoked": False,
            "ffmpeg_invoked": False,
            "ffprobe_invoked": False,
            "audio_generated": False,
            "mux_invoked": False,
            "renderer_invoked": False,
            "media_created": False,
            "new_batch_id_consumed": False,
            "production_dispatch": False,
            "release_authority": "NONE",
        },
    }
    return receipt


def write_receipt(project_root: Path, run_id: str, receipt: Mapping[str, Any]) -> Tuple[Path, str]:
    out_dir = project_root / "artifacts/tests/c11e/e6_challenge_consumer_contract" / run_id
    out_dir.mkdir(parents=True, exist_ok=False)
    path = out_dir / "E6_CHALLENGE_CONSUMER_CONTRACT_PREFLIGHT_RECEIPT_V1.json"
    raw = (json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
    path.write_bytes(raw)
    digest = sha256_bytes(raw)
    (Path(str(path) + ".sha256")).write_text(f"{digest}  {path.name}\n", encoding="ascii")
    return path, digest


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--run-id", required=True)
    args = parser.parse_args(argv)
    project_root = Path(args.project_root)
    print("E6_CHALLENGE_CONSUMER_CONTRACT_STAGE=STATIC_SOURCE_AND_PLAN_RECONCILIATION")
    try:
        receipt = perform_audit(project_root, args.run_id)
    except Exception as exc:  # diagnostic failure is still receipted where possible
        receipt = {
            "schema": "C11E-E6-CHALLENGE-CONSUMER-CONTRACT-PREFLIGHT-RECEIPT-V1",
            "schema_version": "1.0",
            "run_id": args.run_id,
            "status": "FAIL_STATIC_CONSUMER_CONTRACT_PREFLIGHT",
            "failures": [f"UNHANDLED_AUDIT_FAILURE:{type(exc).__name__}:{exc}"],
            "traceback": traceback.format_exc(),
            "execution": {"godot_invoked": False, "media_created": False, "new_batch_id_consumed": False,
                          "production_dispatch": False, "release_authority": "NONE"},
        }
    try:
        path, digest = write_receipt(project_root, args.run_id, receipt)
    except Exception as exc:
        print(f"E6_CONTRACT_RECEIPT_WRITE=FAIL:{type(exc).__name__}:{exc}")
        return 3
    print(f"E6_CHALLENGE_CONSUMER_CONTRACT_STATUS={receipt.get('status')}")
    print(f"E6_CHALLENGE_CONSUMER_SOURCE_PINS={receipt.get('source_pins', {}).get('passed', 0)}/24")
    print(f"E6_CHALLENGE_CONSUMER_E1_INTENTS={receipt.get('e1_intents', {}).get('passed', 0)}/18")
    print(f"E6_CHALLENGE_CONSUMER_D_ENVELOPES={receipt.get('d_envelopes', {}).get('passed', 0)}/18")
    print("E6_CHALLENGE_GODOT_RUNTIME=NOT_RUN")
    print("E6_MEDIA_INVOKED=FALSE")
    print("NEW_BATCH_ID_CONSUMED=FALSE")
    print("PRODUCTION_DISPATCH=FALSE")
    print("RELEASE_AUTHORITY=NONE")
    print(f"E6_CHALLENGE_CONSUMER_CONTRACT_RECEIPT={path}")
    print(f"E6_CHALLENGE_CONSUMER_CONTRACT_RECEIPT_SHA256={digest}")
    if receipt.get("failures"):
        for failure in receipt["failures"]:
            print(f"E6_CONTRACT_FAILURE={failure}")
    return 0 if receipt.get("status") == "PASS_STATIC_CONSUMER_CONTRACT_18_OF_18_EXECUTION_HELD" else 2


if __name__ == "__main__":
    raise SystemExit(main())
