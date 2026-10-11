"""Join canonical D9.9 requests to the existing bounded in-memory payload fixtures.

This is a fixture-specific, console-only review bridge. It never persists payloads,
creates renderer-native input, dispatches a renderer, or authorizes production.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import shutil
import subprocess
import sys
from collections.abc import Mapping
from pathlib import Path
from typing import Any, Callable

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from universal_producer import REQUEST_SCHEMA_ID, evaluate_universal_request
from editorial_render_bridge import build_bridge_planning_record
from d_render_adapter import prepare_d_only_adapter_envelope
from d_renderer_request_scoped_payload_binding import (
    build_request_scoped_payload_binding,
    validate_request_scoped_payload_binding,
)
from d_renderer_visual_payload_materialization_preview import (
    GDSCRIPT_REL as VISUAL_HARNESS_REL,
    MANIFEST_SHA256,
    VisualPayloadPreviewError,
    validate_preview_contract,
    validate_preview_record,
)
from d_renderer_challenge_visual_payload_preview import (
    ChallengeVisualPayloadError,
    FROZEN_MANIFEST_SHA256,
    validate_report_shape as validate_challenge_report,
    validate_source_pins as validate_challenge_source_pins,
)

CONTRACT_REL = Path("definitions/c11d/production/D_RENDERER_REQUEST_SCOPED_PAYLOAD_MATERIALIZATION_BINDING_V1.json")
SCHEMA_REL = Path("definitions/c11d/production/D_RENDERER_REQUEST_SCOPED_PAYLOAD_MATERIALIZATION_BINDING_SCHEMA_V1.json")
MANIFEST_REL = Path("release/C11C_FREEZE_PACKAGE_MANIFEST.json")
CONTRACT_ID = "C11-D-RENDERER-REQUEST-SCOPED-PAYLOAD-MATERIALIZATION-BINDING-CONTRACT-V1"
OUTPUT_SCHEMA = "C11-D-D9-RENDERER-REQUEST-SCOPED-PAYLOAD-MATERIALIZATION-BINDING-V1"
STATUS = "IN_MEMORY_REVIEW_ONLY_REQUEST_SCOPED_PAYLOAD_BINDINGS_NOT_RENDERER_INPUT"
EXPECTED_MANIFEST_SHA256 = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"

HARNESS_SPECS: dict[str, dict[str, str]] = {
    "visual_loop_drill_materialization": {
        "script": "tools/c11d/d9/materialize_visual_payloads_in_memory.gd",
        "pass_marker": "C11-D RENDERER VISUAL PAYLOAD MATERIALIZATION PREVIEW PASS",
        "summary_prefix": "C11-D VISUAL PAYLOAD PREVIEW SUMMARY=",
    },
    "challenge_visual_payload_materialization": {
        "script": "tools/c11d/d9/materialize_challenge_visual_payload_in_memory.gd",
        "pass_marker": "C11-D RENDERER CHALLENGE VISUAL PAYLOAD PREVIEW PASS",
        "summary_prefix": "C11-D CHALLENGE VISUAL PAYLOAD PREVIEW SUMMARY=",
    },
}
ERROR_MARKERS = (
    "SCRIPT ERROR:",
    "ERROR:",
    "RENDERER VISUAL PAYLOAD MATERIALIZATION PREVIEW FAIL",
    "CHALLENGE VISUAL PAYLOAD PREVIEW FAIL",
)

class RequestScopedMaterializationBindingError(ValueError):
    """Raised when the fixed request fixture, source lineage or safety boundary drifts."""


def _root(project_root: Path | str | None = None) -> Path:
    return Path(project_root).resolve() if project_root is not None else Path(__file__).resolve().parents[3]


def _canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def _sha_json(value: Any) -> str:
    return hashlib.sha256(_canonical(value).encode("utf-8")).hexdigest()


def _sha_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _sha_file(path: Path) -> str:
    try:
        return _sha_bytes(path.read_bytes())
    except OSError as exc:
        raise RequestScopedMaterializationBindingError(f"Cannot hash required file {path}: {exc}") from exc


def _read_json(root: Path, rel: str | Path) -> dict[str, Any]:
    try:
        value = json.loads((root / rel).read_text(encoding="utf-8-sig"))
    except Exception as exc:
        raise RequestScopedMaterializationBindingError(f"Cannot parse JSON source {rel}: {exc}") from exc
    if not isinstance(value, dict):
        raise RequestScopedMaterializationBindingError(f"Expected JSON object at {rel}")
    return value


def _load_contract(root: Path) -> tuple[dict[str, Any], dict[str, Any], list[dict[str, str]]]:
    contract = _read_json(root, CONTRACT_REL)
    schema = _read_json(root, SCHEMA_REL)
    if contract.get("schema") != CONTRACT_ID or contract.get("schema_version") != "1.0":
        raise RequestScopedMaterializationBindingError("Request-scoped materialization contract identity/version mismatch")
    if contract.get("status") != "PREPARATION_ONLY_FIXED_REVIEW_FIXTURES_REQUEST_BOUND_NOT_RENDERER_INPUT":
        raise RequestScopedMaterializationBindingError("Contract cannot self-promote beyond fixed fixture review")
    if contract.get("candidate_input_admissible") is not False:
        raise RequestScopedMaterializationBindingError("Contract must keep candidate input inadmissible")
    if contract.get("source_of_truth", {}).get("frozen_c11c_manifest_sha256") != EXPECTED_MANIFEST_SHA256:
        raise RequestScopedMaterializationBindingError("Contract frozen manifest pin mismatch")
    if _sha_file(root / MANIFEST_REL) != EXPECTED_MANIFEST_SHA256:
        raise RequestScopedMaterializationBindingError("Frozen C11-C manifest physical bytes mismatch")
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema" or schema.get("$id") != "urn:c11d:renderer-request-scoped-payload-materialization-binding:v1" or schema.get("additionalProperties") is not False:
        raise RequestScopedMaterializationBindingError("Receipt schema identity/strictness mismatch")
    if set(schema.get("required", [])) != set(schema.get("properties", {})):
        raise RequestScopedMaterializationBindingError("Receipt schema top-level required/properties mismatch")
    expected_locks = {
        "payload_files_written": False,
        "renderer_native_input_emitted": False,
        "renderer_dispatch_invoked": False,
        "renderer_activation": False,
        "production_execution": False,
        "media_output_created": False,
        "output_artifact_path": None,
        "c11c_source_mutation": False,
        "d4_8": "BLOCKED",
        "release_authority": "NONE",
        "d9_14": "BLOCKED_AS_REQUIRED",
        "d9_16": "BLOCKED_AS_REQUIRED",
        "d9_17": "BLOCKED_NO_GO",
        "d10": "BLOCKED",
    }
    if contract.get("execution_boundary") != expected_locks:
        raise RequestScopedMaterializationBindingError("Execution/governance boundary has drifted")
    expected_approval = {
        "materialization_binding_contract_approved": False,
        "selected_payload_instances_approved": False,
        "renderer_baseline_approved": False,
        "renderer_baseline_frozen": False,
        "d4_8_authorized": False,
        "d9_14_full_acceptance": "BLOCKED_AS_REQUIRED",
        "d9_16_full_acceptance": "BLOCKED_AS_REQUIRED",
        "d9_17_closure": "BLOCKED_NO_GO",
        "d10": "BLOCKED",
        "release_authority": "NONE",
    }
    if contract.get("approval_state") != expected_approval:
        raise RequestScopedMaterializationBindingError("The materialization receipt must not approve/freeze/authorize")
    raw = contract.get("source_lineage")
    if not isinstance(raw, list) or len(raw) < 25:
        raise RequestScopedMaterializationBindingError("Pinned source lineage must contain at least 25 entries")
    checked: list[dict[str, str]] = []
    seen: set[str] = set()
    for row in raw:
        if not isinstance(row, Mapping) or set(row) != {"path", "sha256"}:
            raise RequestScopedMaterializationBindingError("Malformed source-lineage row")
        rel, expected = str(row["path"]), str(row["sha256"])
        path = Path(rel)
        if path.is_absolute() or ".." in path.parts or rel in seen or len(expected) != 64:
            raise RequestScopedMaterializationBindingError(f"Unsafe, duplicate or malformed source pin: {rel}")
        actual = _sha_file(root / path)
        if actual != expected:
            raise RequestScopedMaterializationBindingError(f"Pinned source drift: {rel}")
        seen.add(rel)
        checked.append({"path": path.as_posix(), "sha256": actual})
    if not checked or checked[0]["path"] != MANIFEST_REL.as_posix() or checked[0]["sha256"] != EXPECTED_MANIFEST_SHA256:
        raise RequestScopedMaterializationBindingError("Frozen manifest must be first in source lineage")
    harness_rows = contract.get("harnesses")
    if not isinstance(harness_rows, list) or len(harness_rows) != 2:
        raise RequestScopedMaterializationBindingError("Exactly two bounded in-memory harnesses are required")
    seen_harnesses: set[str] = set()
    for item in harness_rows:
        if not isinstance(item, Mapping):
            raise RequestScopedMaterializationBindingError("Malformed harness declaration")
        name = str(item.get("name", ""))
        expected = HARNESS_SPECS.get(name)
        if not expected or name in seen_harnesses:
            raise RequestScopedMaterializationBindingError(f"Unknown or duplicate harness: {name}")
        if item.get("script") != expected["script"] or item.get("pass_marker") != expected["pass_marker"] or item.get("summary_prefix") != expected["summary_prefix"]:
            raise RequestScopedMaterializationBindingError(f"Harness declaration drift: {name}")
        seen_harnesses.add(name)
        script = root / expected["script"]
        if not script.is_file():
            raise RequestScopedMaterializationBindingError(f"Harness script missing: {expected['script']}")
        source = script.read_text(encoding="utf-8-sig")
        for token in item.get("required_fixture_tokens", []):
            if token not in source:
                raise RequestScopedMaterializationBindingError(f"Harness no longer pins its bounded fixture token: {token}")
    return contract, schema, checked


def _fixture_requests(root: Path) -> dict[str, dict[str, Any]]:
    challenge_source = _read_json(root, "challenges/CHALLENGE_004.json")
    challenge_seed = challenge_source.get("generation", {}).get("seed")
    if not isinstance(challenge_seed, int) or isinstance(challenge_seed, bool) or challenge_seed <= 0:
        raise RequestScopedMaterializationBindingError("CHALLENGE_004 must supply a positive canonical generation seed")
    expected = {
        "challenges": {
            "request_id": "D-PAYLOAD-BIND-CHALLENGES",
            "selection": {"content_type": "challenges", "family_id": "parking_v2", "variant_id": "CHALLENGE_004"},
            "seed": challenge_seed,
        },
        "visual_loops": {
            "request_id": "D-PAYLOAD-BIND-VISUAL_LOOPS",
            "selection": {"content_type": "visual_loops", "family_id": "c11c_geometric_waves_v1", "subtype_id": "harmonic_membrane"},
            "seed": 12345,
        },
        "visual_drills": {
            "request_id": "D-PAYLOAD-BIND-VISUAL_DRILLS",
            "selection": {"content_type": "visual_drills", "family_id": "tracking", "variant_id": "tier-2"},
            "seed": 12345,
        },
    }
    if challenge_seed != 314159:
        # V1 is pinned to the canonical CHALLENGE_004 runtime fixture; seed changes need a new reviewed contract.
        raise RequestScopedMaterializationBindingError("CHALLENGE_004 source seed differs from the pinned V1 review fixture")
    return expected


def _request(raw: Mapping[str, Any], root: Path) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    result = evaluate_universal_request(raw, root)
    if result.get("status") != "PLANNED":
        raise RequestScopedMaterializationBindingError(f"Canonical D9.9 request did not produce a PLANNED result: {result.get('error')}")
    bridge = build_bridge_planning_record(result, root)
    envelope = prepare_d_only_adapter_envelope(result, bridge, root)
    source_binding = build_request_scoped_payload_binding(result, bridge, envelope, root)
    validate_request_scoped_payload_binding(source_binding, result, bridge, envelope, root)
    return result, bridge, envelope, source_binding


def _raw_request(fixture: Mapping[str, Any]) -> dict[str, Any]:
    selection = copy.deepcopy(dict(fixture["selection"]))
    is_challenge = selection["content_type"] == "challenges"
    return {
        "schema": REQUEST_SCHEMA_ID,
        "schema_version": "1.0",
        "request_id": str(fixture["request_id"]),
        "mode": "REVIEW",
        "selection": selection,
        "seed": int(fixture["seed"]),
        "music_seed": 840001,
        "delivery_profile_id": "REVIEW_720",
        "presentation_profile_id": "social_default_v1",
        "variation_index": 0,
        "audio_enabled": True,
        "personalization_enabled": True,
        "editorial_profile": {},
        "production_override": {
            "title": "D10 request-scoped materialization review",
            "subtitle": "In-memory review only",
            "call_to_action": "Continuar",
            "language": "ES",
            **({"player_name": "ANA", "challenge_label": "RETO"} if is_challenge else {}),
        },
        "provenance": {"source_revision": "C11D-D9.9-0.11.1", "request_origin": "TEST"},
    }


def _build_request_chains(root: Path, contract: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    fixtures = _fixture_requests(root)
    contract_fixtures = contract.get("fixed_request_fixtures")
    if not isinstance(contract_fixtures, list):
        raise RequestScopedMaterializationBindingError("Fixed fixture matrix missing")
    normalized_contract: dict[str, dict[str, Any]] = {}
    for row in contract_fixtures:
        if not isinstance(row, Mapping) or row.get("content_type") not in fixtures:
            raise RequestScopedMaterializationBindingError("Unknown/malformed request fixture declaration")
        key = str(row["content_type"])
        if key in normalized_contract:
            raise RequestScopedMaterializationBindingError("Duplicate request fixture type")
        normalized_contract[key] = dict(row)
    if set(normalized_contract) != set(fixtures):
        raise RequestScopedMaterializationBindingError("Fixed fixture matrix must cover the three supported types")

    chains: dict[str, dict[str, Any]] = {}
    for content_type, fixture in fixtures.items():
        row = normalized_contract[content_type]
        expected_fixture = {
            "content_type": content_type,
            "request_id": fixture["request_id"],
            "selection": fixture["selection"],
            "gameplay_seed": fixture["seed"],
            "music_seed": 840001,
            "variation_index": 0,
            "presentation_profile_id": "social_default_v1",
            "delivery_profile_id": "REVIEW_720",
        }
        if row != expected_fixture:
            raise RequestScopedMaterializationBindingError(f"Fixed request fixture differs from V1 materializer contract: {content_type}")
        raw = _raw_request(fixture)
        result, bridge, envelope, source_binding = _request(raw, root)
        request = result["canonical_request"]
        canonical_selection = request.get("selection", {})
        normalized_selection = {key: canonical_selection.get(key) for key in fixture["selection"]}
        if normalized_selection != fixture["selection"] or request.get("seed") != fixture["seed"]:
            raise RequestScopedMaterializationBindingError(f"Canonical D9.9 request failed fixture identity: {content_type}")
        if request.get("music_seed") != 840001 or request.get("variation_index") != 0:
            raise RequestScopedMaterializationBindingError(f"Seed/variation fixture drift: {content_type}")
        if request.get("presentation_profile_id") != "social_default_v1" or request.get("delivery_profile_id") != "REVIEW_720":
            raise RequestScopedMaterializationBindingError(f"Profile fixture drift: {content_type}")
        if request.get("seed") == request.get("music_seed"):
            raise RequestScopedMaterializationBindingError("Gameplay and music seed domains must remain distinct")
        chains[content_type] = {
            "fixture": expected_fixture,
            "raw_request": raw,
            "result": result,
            "bridge": bridge,
            "envelope": envelope,
            "source_binding": source_binding,
        }
    return chains


def _parse_summary(output: str, prefix: str, name: str) -> dict[str, Any]:
    records = [line[len(prefix):] for line in output.splitlines() if line.startswith(prefix)]
    if len(records) != 1:
        raise RequestScopedMaterializationBindingError(f"{name}: expected exactly one JSON summary; found {len(records)}")
    try:
        report = json.loads(records[0])
    except json.JSONDecodeError as exc:
        raise RequestScopedMaterializationBindingError(f"{name}: summary was not valid JSON") from exc
    if not isinstance(report, dict):
        raise RequestScopedMaterializationBindingError(f"{name}: summary root must be an object")
    return report


def _run_harness(
    name: str,
    root: Path,
    executable: str,
    timeout_seconds: int,
    process_runner: Callable[..., Any] | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    spec = HARNESS_SPECS.get(name)
    if spec is None:
        raise RequestScopedMaterializationBindingError(f"Unknown bounded harness: {name}")
    script_rel = spec["script"]
    script_path = root / script_rel
    if not script_path.is_file():
        raise RequestScopedMaterializationBindingError(f"Harness script missing: {script_rel}")
    runner = process_runner or subprocess.run
    command = [executable, "--headless", "--path", str(root), "--script", "res://" + script_rel.replace("\\", "/")]
    try:
        completed = runner(
            command,
            cwd=str(root),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout_seconds,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise RequestScopedMaterializationBindingError(f"Could not execute {name} Godot harness: {exc}") from exc
    output = completed.stdout or ""
    print(f"\n--- D10 in-memory payload harness: {name} ---", flush=True)
    if output:
        print(output, end="" if output.endswith("\n") else "\n", flush=True)
    if int(completed.returncode) != 0:
        raise RequestScopedMaterializationBindingError(f"{name}: Godot exited {completed.returncode}")
    if spec["pass_marker"] not in output:
        raise RequestScopedMaterializationBindingError(f"{name}: PASS marker missing")
    bad = [line for line in output.splitlines() if any(marker in line for marker in ERROR_MARKERS)]
    if bad:
        raise RequestScopedMaterializationBindingError(f"{name}: runtime error log present despite PASS: {' | '.join(bad[:3])}")
    report = _parse_summary(output, spec["summary_prefix"], name)
    evidence = {
        "name": name,
        "script": script_rel,
        "script_sha256": _sha_file(script_path),
        "exit_code": int(completed.returncode),
        "pass_marker_seen": True,
        "runtime_error_log_seen": False,
        "summary_sha256": _sha_json(report),
    }
    return report, evidence


def _validate_reports(root: Path, reports: Mapping[str, Mapping[str, Any]]) -> tuple[dict[str, dict[str, Any]], dict[str, Any]]:
    visual_key = "visual_loop_drill_materialization"
    challenge_key = "challenge_visual_payload_materialization"
    if set(reports) != {visual_key, challenge_key}:
        raise RequestScopedMaterializationBindingError("Exactly the two contracted materialization report types are required")
    try:
        visual_contract = validate_preview_contract(root)
        visual_report = copy.deepcopy(dict(reports[visual_key]))
        validate_preview_record(visual_report, root)
        challenge_source_pins = validate_challenge_source_pins(root)
        challenge_report = copy.deepcopy(dict(reports[challenge_key]))
        validate_challenge_report(challenge_report, root)
    except (VisualPayloadPreviewError, ChallengeVisualPayloadError, ValueError, TypeError, KeyError) as exc:
        raise RequestScopedMaterializationBindingError(f"Underlying in-memory payload report rejected: {exc}") from exc
    instances = {str(item["content_type"]): dict(item) for item in visual_report["instances"]}
    if set(instances) != {"visual_loops", "visual_drills"}:
        raise RequestScopedMaterializationBindingError("Existing materializer did not produce exactly Loop + Drill")
    if challenge_report.get("payload_identity", {}).get("challenge_id") != "CHALLENGE_004":
        raise RequestScopedMaterializationBindingError("Challenge payload instance is not the exact CHALLENGE_004 fixture")
    challenge_source = _read_json(root, "challenges/CHALLENGE_004.json")
    actual_seed = challenge_source.get("generation", {}).get("seed")
    if actual_seed != challenge_report.get("source_seed", actual_seed):
        raise RequestScopedMaterializationBindingError("Challenge report source seed differs from canonical source")
    if not isinstance(challenge_report.get("payload_sha256"), str) or len(challenge_report["payload_sha256"]) != 64:
        raise RequestScopedMaterializationBindingError("Challenge payload hash missing/malformed")
    for content_type, expected in (("visual_loops", ("harmonic_membrane", 12345)), ("visual_drills", ("tier-2", 12345))):
        item = instances[content_type]
        selected = item.get("selection", {})
        actual_variant = selected.get("subtype_id") if content_type == "visual_loops" else selected.get("variant_id")
        if actual_variant != expected[0] or item.get("seed") != expected[1] or item.get("variation_index") != 0:
            raise RequestScopedMaterializationBindingError(f"Materialized request fixture mismatch: {content_type}")
        if item.get("deterministic_repeat_pass") is not True or item.get("materialization") != "IN_MEMORY_ONLY":
            raise RequestScopedMaterializationBindingError(f"Instance is not deterministic, memory-only: {content_type}")
    challenge_determinism = challenge_report.get("determinism", {})
    if challenge_determinism.get("runtime_repeat_equal") is not True or challenge_determinism.get("payload_repeat_equal") is not True or challenge_determinism.get("frame_signature_repeat_equal") is not True:
        raise RequestScopedMaterializationBindingError("Challenge payload determinism is not established")
    if visual_contract["contract"].get("required_locks", {}).get("challenge_instance_materialized") is not False:
        raise RequestScopedMaterializationBindingError("Original visual-only materializer contract must remain Challenge-neutral")
    if challenge_source_pins.get("source_hash_pins") != 10 or challenge_source_pins.get("asset_pins") != 3:
        raise RequestScopedMaterializationBindingError("Challenge payload source/asset pins incomplete")
    return instances, {"visual": visual_report, "challenge": challenge_report}


def _binding_record(content_type: str, chain: Mapping[str, Any], item: Mapping[str, Any], payload_type: str, source_seed: int) -> dict[str, Any]:
    result = chain["result"]
    bridge = chain["bridge"]
    envelope = chain["envelope"]
    source_binding = chain["source_binding"]
    request = result["canonical_request"]
    if item.get("seed", source_seed) != source_seed:
        raise RequestScopedMaterializationBindingError(f"Materialized seed does not match source seed: {content_type}")
    if int(request["seed"]) != source_seed:
        raise RequestScopedMaterializationBindingError(f"Canonical request seed does not bind the materialized source: {content_type}")
    selection = copy.deepcopy(dict(chain["fixture"]["selection"]))
    canonical_selection = request.get("selection", {})
    if {key: canonical_selection.get(key) for key in selection} != selection:
        raise RequestScopedMaterializationBindingError(f"Canonical request selector differs from fixture: {content_type}")
    if content_type == "visual_loops":
        if selection != {"content_type":"visual_loops","family_id":"c11c_geometric_waves_v1","subtype_id":"harmonic_membrane"}:
            raise RequestScopedMaterializationBindingError("Loop selector is outside fixed V1 review fixture")
        if item.get("selection") != {"family_id":"c11c_geometric_waves_v1","subtype_id":"harmonic_membrane"}:
            raise RequestScopedMaterializationBindingError("Loop payload selection does not match canonical request")
        payload_id = str(item.get("instance_id", ""))
        payload_hash = str(item.get("payload_instance_sha256", ""))
        instance_seed = int(item.get("seed", -1))
    elif content_type == "visual_drills":
        if selection != {"content_type":"visual_drills","family_id":"tracking","variant_id":"tier-2"}:
            raise RequestScopedMaterializationBindingError("Drill selector is outside fixed V1 review fixture")
        if item.get("selection") != {"family_id":"tracking","variant_id":"tier-2"}:
            raise RequestScopedMaterializationBindingError("Drill payload selection does not match canonical request")
        payload_id = str(item.get("instance_id", ""))
        payload_hash = str(item.get("payload_instance_sha256", ""))
        instance_seed = int(item.get("seed", -1))
    else:
        if selection != {"content_type":"challenges","family_id":"parking_v2","variant_id":"CHALLENGE_004"}:
            raise RequestScopedMaterializationBindingError("Challenge selector is outside fixed V1 review fixture")
        report = item
        identity = report.get("payload_identity", {})
        if identity.get("challenge_id") != "CHALLENGE_004" or identity.get("mechanic") != "parking_v2":
            raise RequestScopedMaterializationBindingError("Challenge payload selection does not match canonical request")
        payload_hash = str(report.get("payload_sha256", ""))
        payload_id = "D-CHALLENGE-CHALLENGE_004-" + payload_hash[:16]
        instance_seed = source_seed
    if len(payload_hash) != 64 or any(c not in "0123456789abcdef" for c in payload_hash):
        raise RequestScopedMaterializationBindingError(f"Malformed payload instance hash: {content_type}")
    if not payload_id or (content_type != "challenges" and not payload_id.startswith(("D-VLP-", "D-VDP-"))):
        raise RequestScopedMaterializationBindingError(f"Payload identity missing/invalid: {content_type}")
    unresolved = [
        "FIXED_V1_REVIEW_FIXTURE_ONLY_DYNAMIC_REQUEST_TRANSPORT_NOT_IMPLEMENTED",
        "EDITORIAL_VALUE_TO_VISUAL_PAYLOAD_EFFECT_NOT_PROVEN_BY_MATERIALIZATION_HARNESS",
        "VARIATION_INDEX_IS_METADATA_ONLY_AND_NOT_APPLIED_TO_VARIANT_GENERATION",
        "DELIVERY_REVIEW_720_IS_REQUEST_METADATA_NOT_RENDERED_DELIVERY_EVIDENCE",
        "TEMPORAL_SAMPLING_AND_INTERPOLATION_POLICY_PROPOSED_NOT_APPLIED",
        "COORDINATE_PROJECTION_AND_SEMANTIC_REGION_GEOMETRY_UNRESOLVED_NOT_APPLIED",
        "EDITORIAL_FIELD_VISIBILITY_WINDOWS_UNRESOLVED_NOT_APPLIED",
        "AUDIO_MUSIC_MATERIALIZATION_AND_QA_NOT_PERFORMED",
        "FRAME_SCHEDULE_AND_RENDERER_NATIVE_INPUT_NOT_EMITTED",
        "RENDERER_BASELINE_APPROVAL_FREEZE_AND_D4_8_AUTHORIZATION_MISSING",
    ]
    if content_type == "challenges":
        unresolved.extend([
            "CHALLENGE_RUNTIME_USES_FROZEN_SOURCE_SEED_AND_SOURCE_TIMEBASE_NOT_REVIEW_DELIVERY_SEED_MAPPING",
            "CHALLENGE_VARIATION_INDEX_IS_NOT_CONSUMED_BY_FROZEN_RUNTIME_HARNESS",
            "CHALLENGE_PAYLOAD_ID_IS_DERIVED_RECEIPT_ALIAS_NOT_RUNTIME_INSTANCE_FIELD",
        ])
    payload = {
        "content_type": content_type,
        "request_id": request["request_id"],
        "canonical_request_sha256": result["request_hash"],
        "producer_plan_sha256": result["plan_hash"],
        "bridge_record_sha256": bridge["record_hash"],
        "adapter_envelope_sha256": envelope["envelope_hash"],
        "request_source_binding_sha256": source_binding["binding_sha256"],
        "selection": selection,
        "gameplay_seed": int(request["seed"]),
        "music_seed": int(request["music_seed"]),
        "variation_index": int(request["variation_index"]),
        "presentation_profile_id": str(request["presentation_profile_id"]),
        "delivery_profile_id": str(request["delivery_profile_id"]),
        "source_seed": int(instance_seed),
        "source_seed_matches_request": int(instance_seed) == int(request["seed"]),
        "payload_instance_id": payload_id,
        "payload_instance_sha256": payload_hash,
        "payload_type": payload_type,
        "materialization": "IN_MEMORY_ONLY",
        "deterministic_repeat_pass": True,
        "request_identity_binding": "EXACT_FIXED_FIXTURE_SELECTOR_AND_SEED_JOINED_IN_IN_MEMORY_RECEIPT",
        "video_render_ready": False,
        "unresolved_requirements": unresolved,
    }
    payload["binding_sha256"] = _sha_json(payload)
    return payload


def build_receipt(
    root: Path | str | None,
    observations: Mapping[str, tuple[Mapping[str, Any], Mapping[str, Any]]],
) -> dict[str, Any]:
    project_root = _root(root)
    contract, schema, lineage = _load_contract(project_root)
    chains = _build_request_chains(project_root, contract)
    reports = {name: pair[0] for name, pair in observations.items()}
    evidence = {name: dict(pair[1]) for name, pair in observations.items()}
    instances, validated_reports = _validate_reports(project_root, reports)
    if set(evidence) != set(HARNESS_SPECS):
        raise RequestScopedMaterializationBindingError("Harness evidence must cover exactly both materializers")
    for name, row in evidence.items():
        spec = HARNESS_SPECS[name]
        if row.get("name") != name or row.get("script") != spec["script"] or row.get("script_sha256") != _sha_file(project_root / spec["script"]):
            raise RequestScopedMaterializationBindingError(f"Harness evidence identity/hash mismatch: {name}")
        if row.get("exit_code") != 0 or row.get("pass_marker_seen") is not True or row.get("runtime_error_log_seen") is not False:
            raise RequestScopedMaterializationBindingError(f"Harness execution evidence not PASS/clean: {name}")
        if row.get("summary_sha256") != _sha_json(reports[name]):
            raise RequestScopedMaterializationBindingError(f"Harness summary digest mismatch: {name}")
    challenge_source = _read_json(project_root, "challenges/CHALLENGE_004.json")
    binding_rows = [
        _binding_record("challenges", chains["challenges"], validated_reports["challenge"], "SOURCE_TIMEBASE_CHALLENGE_VISUAL_PAYLOAD", int(challenge_source["generation"]["seed"])),
        _binding_record("visual_loops", chains["visual_loops"], instances["visual_loops"], "C11C_VISUAL_LOOP_AUTHORING_PAYLOAD", 12345),
        _binding_record("visual_drills", chains["visual_drills"], instances["visual_drills"], "C11C_VISUAL_DRILL_AUTHORING_PAYLOAD", 12345),
    ]
    if [row["content_type"] for row in binding_rows] != ["challenges", "visual_loops", "visual_drills"]:
        raise RequestScopedMaterializationBindingError("Receipt content binding order/coverage is not canonical")
    runtime_identity = {
        "contract_path": CONTRACT_REL.as_posix(),
        "contract_sha256": _sha_file(project_root / CONTRACT_REL),
        "schema_path": SCHEMA_REL.as_posix(),
        "schema_sha256": _sha_file(project_root / SCHEMA_REL),
        "orchestrator_path": Path(__file__).resolve().relative_to(project_root).as_posix(),
        "orchestrator_sha256": _sha_file(Path(__file__).resolve()),
        "test_path": "tools/c11d/d9/test_d_renderer_request_scoped_payload_materialization_binding.py",
        "test_sha256": _sha_file(project_root / "tools/c11d/d9/test_d_renderer_request_scoped_payload_materialization_binding.py"),
    }
    receipt: dict[str, Any] = {
        "schema": OUTPUT_SCHEMA,
        "schema_version": "1.0",
        "status": STATUS,
        "frozen_c11c_manifest_sha256": EXPECTED_MANIFEST_SHA256,
        "candidate_input_admissible": False,
        "runtime_identity": runtime_identity,
        "content_bindings": binding_rows,
        "harness_evidence": [evidence["visual_loop_drill_materialization"], evidence["challenge_visual_payload_materialization"]],
        "unresolved_policy_gates": list(contract["unresolved_policy_gates"]),
        "source_lineage": lineage,
        "readiness": {
            "request_scoped_payload_instances_materialized": True,
            "bound_content_types": 3,
            "total_content_types": 3,
            "all_three_bound": True,
            "video_render_ready": False,
        },
        "execution_boundary": {
            "mode": "IN_MEMORY_REVIEW_ONLY",
            "payload_files_written": False,
            "renderer_native_input_emitted": False,
            "renderer_dispatch_invoked": False,
            "renderer_activation": False,
            "production_execution": False,
            "media_output_created": False,
            "output_artifact_path": None,
            "c11c_source_mutation": False,
            "d4_8": "BLOCKED",
            "release_authority": "NONE",
            "d9_14": "BLOCKED_AS_REQUIRED",
            "d9_16": "BLOCKED_AS_REQUIRED",
            "d9_17": "BLOCKED_NO_GO",
            "d10": "BLOCKED",
        },
    }
    receipt["receipt_sha256"] = _sha_json(receipt)
    _validate_schema(receipt, schema)
    return receipt


def _validate_schema(receipt: Mapping[str, Any], schema: Mapping[str, Any]) -> None:
    if set(receipt) != set(schema.get("required", [])) or set(receipt) != set(schema.get("properties", {})):
        raise RequestScopedMaterializationBindingError("Receipt top-level shape differs from strict schema")
    if receipt.get("schema") != OUTPUT_SCHEMA or receipt.get("schema_version") != "1.0" or receipt.get("status") != STATUS:
        raise RequestScopedMaterializationBindingError("Receipt identity/status mismatch")
    if receipt.get("frozen_c11c_manifest_sha256") != EXPECTED_MANIFEST_SHA256 or receipt.get("candidate_input_admissible") is not False:
        raise RequestScopedMaterializationBindingError("Receipt manifest/admission boundary mismatch")
    if _sha_json({k: v for k, v in receipt.items() if k != "receipt_sha256"}) != receipt.get("receipt_sha256"):
        raise RequestScopedMaterializationBindingError("Receipt SHA-256 mismatch")
    bindings = receipt.get("content_bindings")
    if not isinstance(bindings, list) or len(bindings) != 3 or {b.get("content_type") for b in bindings} != {"challenges", "visual_loops", "visual_drills"}:
        raise RequestScopedMaterializationBindingError("Receipt must bind exactly one instance for each supported content type")
    for binding in bindings:
        if set(binding) != set(schema["properties"]["content_bindings"]["items"]["required"]):
            raise RequestScopedMaterializationBindingError("Content binding shape differs from strict schema")
        if _sha_json({k: v for k, v in binding.items() if k != "binding_sha256"}) != binding.get("binding_sha256"):
            raise RequestScopedMaterializationBindingError("Content binding SHA-256 mismatch")
        if binding.get("source_seed_matches_request") is not True or binding.get("video_render_ready") is not False or binding.get("materialization") != "IN_MEMORY_ONLY":
            raise RequestScopedMaterializationBindingError("Content binding incorrectly claims a mismatched seed or render readiness")
        for key in ("canonical_request_sha256", "producer_plan_sha256", "bridge_record_sha256", "adapter_envelope_sha256", "request_source_binding_sha256", "payload_instance_sha256"):
            value = binding.get(key)
            if not isinstance(value, str) or len(value) != 64 or any(c not in "0123456789abcdef" for c in value):
                raise RequestScopedMaterializationBindingError(f"Malformed content binding hash: {key}")
    if receipt.get("readiness") != {"request_scoped_payload_instances_materialized": True, "bound_content_types": 3, "total_content_types": 3, "all_three_bound": True, "video_render_ready": False}:
        raise RequestScopedMaterializationBindingError("Readiness must distinguish materialized in-memory fixtures from render readiness")
    expected_boundary = {
        "mode":"IN_MEMORY_REVIEW_ONLY", "payload_files_written":False, "renderer_native_input_emitted":False,
        "renderer_dispatch_invoked":False, "renderer_activation":False, "production_execution":False,
        "media_output_created":False, "output_artifact_path":None, "c11c_source_mutation":False,
        "d4_8":"BLOCKED", "release_authority":"NONE", "d9_14":"BLOCKED_AS_REQUIRED",
        "d9_16":"BLOCKED_AS_REQUIRED", "d9_17":"BLOCKED_NO_GO", "d10":"BLOCKED",
    }
    if receipt.get("execution_boundary") != expected_boundary:
        raise RequestScopedMaterializationBindingError("Receipt execution/governance boundary drift")
    try:
        import jsonschema  # type: ignore
    except ImportError:
        jsonschema = None
    if jsonschema is not None:
        jsonschema.Draft202012Validator(schema).validate(dict(receipt))


def validate_receipt(
    receipt: Mapping[str, Any],
    root: Path | str | None,
    observations: Mapping[str, tuple[Mapping[str, Any], Mapping[str, Any]]],
) -> bool:
    project_root = _root(root)
    _, schema, _ = _load_contract(project_root)
    _validate_schema(receipt, schema)
    expected = build_receipt(project_root, observations)
    if dict(receipt) != expected:
        raise RequestScopedMaterializationBindingError("Receipt differs from reproducible request/source/materializer join")
    return True


def run_review(
    root: Path | str | None = None,
    *,
    executable: str | None = None,
    timeout_seconds: int = 120,
    process_runner: Callable[..., Any] | None = None,
) -> dict[str, Any]:
    project_root = _root(root)
    if timeout_seconds < 1 or timeout_seconds > 900:
        raise RequestScopedMaterializationBindingError("Timeout must be in 1..900 seconds")
    _load_contract(project_root)
    executable = executable or os.environ.get("C11D_GODOT_EXECUTABLE") or shutil.which("godot") or "godot"
    observations: dict[str, tuple[Mapping[str, Any], Mapping[str, Any]]] = {}
    for name in HARNESS_SPECS:
        report, evidence = _run_harness(name, project_root, executable, timeout_seconds, process_runner=process_runner)
        observations[name] = (report, evidence)
    # build_receipt constructs, hashes, and validates the receipt in one pass.
    # Avoid a second independent rebuild of the canonical request chains here.
    return build_receipt(project_root, observations)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate fixed, in-memory D9 visual payload fixtures against canonical D9.9 requests; no renderer dispatch or output files.")
    parser.add_argument("--godot", default=os.environ.get("C11D_GODOT_EXECUTABLE") or shutil.which("godot") or "godot", help="Godot 4.7.1 console executable or command on PATH")
    parser.add_argument("--timeout", type=int, default=120, help="Per-harness timeout seconds (1..900)")
    args = parser.parse_args()
    try:
        receipt = run_review(executable=args.godot, timeout_seconds=args.timeout)
    except (RequestScopedMaterializationBindingError, VisualPayloadPreviewError, ChallengeVisualPayloadError, ValueError, TypeError, KeyError, OSError) as exc:
        print(f"C11-D REQUEST-SCOPED PAYLOAD MATERIALIZATION/BINDING FAIL | {exc}", file=sys.stderr)
        return 1
    print(
        "C11-D REQUEST-SCOPED PAYLOAD MATERIALIZATION/BINDING PASS"
        f" | content_types={receipt['readiness']['bound_content_types']}/3"
        f" | harnesses={len(receipt['harness_evidence'])}/2"
        f" | deterministic={sum(1 for item in receipt['content_bindings'] if item['deterministic_repeat_pass'])}/3"
        " | receipt=IN_MEMORY_CONSOLE_ONLY"
        " | candidate_input_admissible=false | renderer_input=NOT_EMITTED | renderer=OFF"
        " | media_created=false | D4.8=BLOCKED | release_authority=NONE"
    )
    print("C11-D REQUEST-SCOPED MATERIALIZATION BINDING RECEIPT=" + _canonical(receipt))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
