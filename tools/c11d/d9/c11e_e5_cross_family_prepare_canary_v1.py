from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import subprocess
import sys
import traceback
import uuid
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any, Mapping

CONTRACT_REL = "definitions/c11d/production/C11E_E5_CROSS_FAMILY_CANARY_CONTRACT_V1.json"
CLI_REL = "c11c-suite/c11c-producer/c11e_production_cli.py"
GUI_REL = "c11c-suite/c11c-producer/main.py"
SERVICE_REL = "c11c-suite/c11c-producer/c11e_production_service.py"
FROZEN_SHA256 = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
FROZEN_BYTES = 796318


class E5CanaryError(RuntimeError):
    pass


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def write_json_once(path: Path, value: Any) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False) + "\n").encode("utf-8")
    fd = os.open(str(path), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
    except Exception:
        try:
            path.unlink(missing_ok=True)
        except Exception:
            pass
        raise
    return sha256_bytes(data)


def replace_json(path: Path, value: Any) -> str:
    data = (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False) + "\n").encode("utf-8")
    temp = path.parent / (".e5-" + uuid.uuid4().hex[:10] + ".tmp")
    fd = os.open(str(temp), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(str(temp), str(path))
    finally:
        try:
            temp.unlink(missing_ok=True)
        except Exception:
            pass
    return sha256_bytes(data)


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict):
        raise E5CanaryError(f"JSON root must be an object: {path}")
    return value


def safe_project_path(root: Path, relative: str) -> Path:
    rel = PurePosixPath(relative)
    if rel.is_absolute() or ".." in rel.parts or "\\" in relative or ":" in relative:
        raise E5CanaryError(f"Unsafe project-relative path: {relative}")
    candidate = root.joinpath(*rel.parts)
    resolved = candidate.resolve(strict=False)
    try:
        resolved.relative_to(root.resolve())
    except Exception as exc:
        raise E5CanaryError(f"Path escapes project root: {relative}") from exc
    return candidate


def verify_pin(root: Path, row: Mapping[str, Any]) -> dict[str, Any]:
    rel = str(row["path"])
    path = safe_project_path(root, rel)
    if not path.is_file() or path.is_symlink():
        raise E5CanaryError(f"Pinned source is missing or not a regular file: {rel}")
    data = path.read_bytes()
    actual = {"path": rel, "bytes": len(data), "sha256": sha256_bytes(data)}
    expected = {"path": rel, "bytes": int(row["bytes"]), "sha256": str(row["sha256"])}
    if actual != expected:
        raise E5CanaryError(f"Source pin mismatch: {rel}: expected={expected} actual={actual}")
    return actual


def verify_static_pins(root: Path, contract: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = contract.get("source_pins")
    if not isinstance(rows, list) or len(rows) < 20:
        raise E5CanaryError("Contract source-pin inventory is incomplete")
    result = [verify_pin(root, row) for row in rows]
    by_path = {row["path"]: row for row in result}
    frozen = by_path.get("release/C11C_FREEZE_PACKAGE_MANIFEST.json")
    if frozen != {"path": "release/C11C_FREEZE_PACKAGE_MANIFEST.json", "bytes": FROZEN_BYTES, "sha256": FROZEN_SHA256}:
        raise E5CanaryError("C11-C frozen manifest pin differs from the frozen authority")
    return sorted(result, key=lambda row: row["path"])


def verify_history_refs(root: Path, contract: Mapping[str, Any]) -> list[dict[str, Any]]:
    refs = contract.get("historical_evidence", {})
    output = []
    for key, value in refs.items():
        row = {"path": value["path"], "bytes": None, "sha256": value["sha256"]}
        path = safe_project_path(root, row["path"])
        if not path.is_file():
            raise E5CanaryError(f"Accepted historical evidence is missing: {row['path']}")
        data = path.read_bytes()
        row["bytes"] = len(data)
        row["sha256_actual"] = sha256_bytes(data)
        if row["sha256_actual"] != row["sha256"]:
            raise E5CanaryError(f"Historical evidence hash mismatch: {row['path']}")
        row["role"] = key
        output.append(row)
    return output


def build_request(family_key: str, probe: str, batch_token: str, contract: Mapping[str, Any]) -> dict[str, Any]:
    family = contract["families"][family_key]
    seeds = family["seeds"]
    gameplay = int(seeds["gameplay"])
    music = int(seeds["music"])
    if probe == "C":
        music = int(seeds["music_changed"])
    elif probe == "D":
        gameplay = int(seeds["gameplay_changed"])
    elif probe not in {"A", "B"}:
        raise E5CanaryError(f"Unknown probe: {probe}")

    family_tag = {"challenge": "CH", "loop": "LOOP", "drill": "DRILL"}[family_key]
    request_id = f"E5-{batch_token}-{family_tag}-{probe}"
    raw: dict[str, Any] = {
        "schema": "C11-D-D9.9-UNIVERSAL-PRODUCER-REQUEST-V1",
        "schema_version": "1.0",
        "request_id": request_id,
        "mode": family["mode"],
        "selection": copy.deepcopy(family["selection"]),
        "seed": gameplay,
        "music_seed": music,
        "delivery_profile_id": "REVIEW_720",
        "presentation_profile_id": "social_default_v1",
        "variation_index": 0,
        "audio_enabled": True,
        "personalization_enabled": True,
        "editorial_profile": {},
        "provenance": {"source_revision": "C11E-E5-CROSS-FAMILY-CANARY-V1"},
    }
    return raw


def static_gui_wiring_check(root: Path) -> dict[str, Any]:
    source = safe_project_path(root, GUI_REL).read_text(encoding="utf-8-sig")
    required = [
        "def _run_d9_universal_plan(self)",
        "prepare_c11e_production_intent(",
        'request_origin="GUI"',
        "e1_intent",
    ]
    missing = [item for item in required if item not in source]
    if missing:
        raise E5CanaryError(f"Current Producer GUI E1 service wiring is missing tokens: {missing}")
    return {"status": "PASS_GUI_STATIC_SERVICE_WIRING", "path": GUI_REL, "checks": required, "actual_qt_ui_invoked": False}


def import_service(root: Path):
    producer_dir = root / "c11c-suite" / "c11c-producer"
    if str(producer_dir) not in sys.path:
        sys.path.insert(0, str(producer_dir))
    import c11e_production_service  # type: ignore
    return c11e_production_service


def validate_intent_shape(intent: Mapping[str, Any], family_key: str, probe: str, contract: Mapping[str, Any]) -> dict[str, Any]:
    family = contract["families"][family_key]
    expected = family["music"]
    request = intent.get("request", {})
    selection = request.get("selection", {})
    if request.get("content_type") != family["content_type"]:
        raise E5CanaryError(f"{family_key}/{probe}: wrong content_type")
    if selection.get("family_id") != family["selection"].get("family_id") or selection.get("variant_id") != family["selection"].get("variant_id") or selection.get("subtype_id") != family["selection"].get("subtype_id"):
        raise E5CanaryError(f"{family_key}/{probe}: canonical selector identity drift")
    seeds = intent.get("seed_domains", {})
    raw_expected = build_request(family_key, probe, "validation", contract)
    if seeds.get("gameplay", {}).get("value") != raw_expected["seed"] or seeds.get("music", {}).get("value") != raw_expected["music_seed"]:
        raise E5CanaryError(f"{family_key}/{probe}: seed domain values differ from probe contract")
    if seeds.get("gameplay", {}).get("field") != "request.seed" or seeds.get("music", {}).get("field") != "request.music_seed":
        raise E5CanaryError(f"{family_key}/{probe}: seed-field names changed")
    if seeds.get("independent_domains") is not True or seeds.get("cross_domain_sharing") != "FORBIDDEN" or seeds.get("automatic_generation") is not False or seeds.get("runtime_derivation") is not False:
        raise E5CanaryError(f"{family_key}/{probe}: seed domain governance changed")
    if intent.get("family_adapter", {}).get("status") != "NOT_CONNECTED_E1":
        raise E5CanaryError(f"{family_key}/{probe}: family adapter crossed the E1 boundary")
    boundary = intent.get("execution_boundary", {})
    for key in ("dispatch_authorized", "renderer_input_emitted", "renderer_dispatch_invoked", "renderer_activation", "production_execution", "media_created"):
        if boundary.get(key) is not False:
            raise E5CanaryError(f"{family_key}/{probe}: E1 execution boundary changed at {key}")
    if boundary.get("d4_8") != "BLOCKED" or boundary.get("release_authority") != "NONE":
        raise E5CanaryError(f"{family_key}/{probe}: governance boundary changed")
    if intent.get("delivery", {}).get("resolved_profile_id") != "REVIEW_720" or intent.get("delivery", {}).get("presentation_profile_id") != "social_default_v1" or intent.get("delivery", {}).get("audio_enabled") is not True:
        raise E5CanaryError(f"{family_key}/{probe}: delivery contract drift")

    music = intent.get("music_contract", {})
    if music.get("music_seed") != raw_expected["music_seed"] or music.get("dispatchable") is not False or music.get("dispatch_authorized") is not False or music.get("engine_invoked") is not False or music.get("audio_created") is not False:
        raise E5CanaryError(f"{family_key}/{probe}: music contract crossed its E1 boundary")

    profile_id = None
    profile_route = music.get("route")
    preparation = intent.get("d9_boundary_preparation")
    if family_key == "challenge":
        profile_id = music.get("style_profile", {}).get("profile_id")
        if profile_id != expected["profile_id"] or profile_route != expected["route"]:
            raise E5CanaryError("Challenge D3 V5 route/profile mismatch")
        if preparation is not None:
            raise E5CanaryError("Challenge unexpectedly received a Loop/Drill boundary preparation")
        if intent.get("request", {}).get("presentation_options") != {"show_hook_countdown": True}:
            raise E5CanaryError("Challenge hook/countdown E1 default changed")
        boundary_kind = "CHALLENGE_D3_V5_PLANNING_BINDING_ONLY"
    elif family_key == "loop":
        if not isinstance(preparation, Mapping) or "loop_family_stage_contract" not in preparation or "drill_family_stage_contract" in preparation:
            raise E5CanaryError("Loop request did not stay on its existing Loop family boundary")
        stage = preparation["loop_family_stage_contract"]
        visual = stage.get("family_visual_stage", {})
        profile_id = visual.get("frozen_c11c_music_profile_id")
        args = visual.get("argument_vector", [])
        if profile_id != expected["profile_id"] or music.get("route") != expected["route"]:
            raise E5CanaryError("Loop family music profile/route mismatch")
        if visual.get("launcher_execution") is not False or visual.get("music_seed_passed_to_visual_launcher") is not False or visual.get("audio_switch") != "-NoSound":
            raise E5CanaryError("Loop visual launcher boundary or seed isolation changed")
        if "-Seed" not in args or str(raw_expected["seed"]) not in args:
            raise E5CanaryError("Loop visual launcher does not bind the gameplay seed")
        if stage.get("timeline") is not None or stage.get("timebase") is not None:
            raise E5CanaryError("Loop E1 preparation must not invent a materialized timeline")
        if stage.get("governance", {}).get("renderer_native_input_emitted") is not False or stage.get("governance", {}).get("media_created") is not False:
            raise E5CanaryError("Loop stage crossed its no-render boundary")
        boundary_kind = "EXISTING_E4B_LOOP_FAMILY_STAGE_CONTRACT"
    elif family_key == "drill":
        if not isinstance(preparation, Mapping) or "drill_family_stage_contract" not in preparation or "loop_family_stage_contract" in preparation:
            raise E5CanaryError("Drill request did not stay on its existing Drill family boundary")
        stage = preparation["drill_family_stage_contract"]
        visual = stage.get("family_visual_stage", {})
        native_music = stage.get("native_family_music", {})
        profile_id = native_music.get("profile_id")
        args = visual.get("argument_vector", [])
        if profile_id != expected["profile_id"] or native_music.get("route") != expected["route"]:
            raise E5CanaryError("Drill native family music profile/route mismatch")
        if visual.get("launcher_execution") is not False or visual.get("music_seed_passed_to_visual_launcher") is not False or visual.get("audio_switch") != "-NoSound":
            raise E5CanaryError("Drill visual launcher boundary or seed isolation changed")
        if "-Seed" not in args or str(raw_expected["seed"]) not in args:
            raise E5CanaryError("Drill visual launcher does not bind the gameplay seed")
        if native_music.get("request_music_seed_field") != "request.music_seed" or native_music.get("d3_v5_invoked") is not False:
            raise E5CanaryError("Drill native family music seed route changed")
        if stage.get("timeline") is not None or stage.get("native_timeline") is not None:
            raise E5CanaryError("Drill E1 preparation must not invent a materialized timeline")
        phase = preparation.get("native_phase_and_end_cta_contract", {})
        seq = phase.get("phase_sequence", [])
        if [x.get("phase") for x in seq] != ["PRE_ROLL", "GAME", "END_CTA", "DONE"]:
            raise E5CanaryError("Drill native phase ordering changed")
        if seq[0].get("duration_seconds") != 3.0 or seq[2].get("duration_seconds") != 3.0:
            raise E5CanaryError("Drill native 3-second PRE_ROLL/END_CTA contract changed")
        if phase.get("end_cta_precedence", {}).get("native_cta_header_authoritative") is not True or phase.get("end_cta_precedence", {}).get("d_adapter_may_override_native_cta") is not False:
            raise E5CanaryError("Drill END_CTA precedence changed")
        if stage.get("governance", {}).get("renderer_native_input_emitted") is not False or stage.get("governance", {}).get("media_created") is not False:
            raise E5CanaryError("Drill stage crossed its no-render boundary")
        boundary_kind = "EXISTING_E4C_DRILL_V2_BINDER_AND_PHASE_CONTRACT"
    else:
        raise E5CanaryError(f"Unknown family key: {family_key}")

    return {
        "family": family_key,
        "probe": probe,
        "selector": copy.deepcopy(selection),
        "profile_id": profile_id,
        "music_route": profile_route,
        "boundary_contract": boundary_kind,
        "gameplay_seed": raw_expected["seed"],
        "music_seed": raw_expected["music_seed"],
        "family_adapter": "NOT_CONNECTED_E1",
        "media_created": False,
        "renderer_invoked": False,
        "delivery_profile": "REVIEW_720",
    }


def _strip_request_scoped_identity(value: Any) -> Any:
    # Family bridge/adapter planning records are content-bound by design. Their hashes
    # include request_id and therefore differ for a semantically identical A/B replay.
    # Remove only those request-scoped identity fields; retain selectors, profiles,
    # music/gameplay contracts, source pins, vectors and all non-identity semantics.
    identity_keys = {
        "request_id", "request_hash", "plan_hash", "record_hash", "bridge_record_hash",
        "d_only_adapter_envelope_hash", "envelope_hash", "contract_sha256",
        "preparation_sha256", "preview_sha256", "request_scoped_source_binding_sha256",
        "drill_dynamic_binding_preview_sha256",
    }
    if isinstance(value, Mapping):
        normalized = {}
        for key, item in value.items():
            name = str(key)
            if name in identity_keys:
                continue
            if name == "argument_vector" and isinstance(item, list):
                sanitized = []
                skip_next = False
                for token in item:
                    if skip_next:
                        skip_next = False
                        continue
                    if token == "-OutputTag":
                        skip_next = True
                        continue
                    sanitized.append(token)
                normalized[name] = sanitized
            else:
                normalized[name] = _strip_request_scoped_identity(item)
        return normalized
    if isinstance(value, list):
        return [_strip_request_scoped_identity(item) for item in value]
    if isinstance(value, tuple):
        return [_strip_request_scoped_identity(item) for item in value]
    return copy.deepcopy(value)


def _projection_without_request_specific_hashes(intent: Mapping[str, Any]) -> dict[str, Any]:
    projection = {
        "mode": intent.get("request", {}).get("mode"),
        "content_type": intent.get("request", {}).get("content_type"),
        "selection": copy.deepcopy(intent.get("request", {}).get("selection")),
        "variation_index": intent.get("request", {}).get("variation_index"),
        "presentation_options": copy.deepcopy(intent.get("request", {}).get("presentation_options")),
        "delivery": copy.deepcopy(intent.get("delivery")),
        "editorial": copy.deepcopy(intent.get("editorial")),
        "music_contract": copy.deepcopy(intent.get("music_contract")),
        "seed_domains": copy.deepcopy(intent.get("seed_domains")),
        "d9_boundary_preparation": copy.deepcopy(intent.get("d9_boundary_preparation")),
    }
    return _strip_request_scoped_identity(projection)


def visual_projection(intent: Mapping[str, Any], family_key: str) -> dict[str, Any]:
    prep = intent.get("d9_boundary_preparation")
    if not isinstance(prep, Mapping):
        return {"family": family_key, "boundary": "NO_FAMILY_STAGE_IN_E1"}
    stage_key = "loop_family_stage_contract" if family_key == "loop" else "drill_family_stage_contract"
    stage = copy.deepcopy(prep.get(stage_key, {}))
    visual = stage.get("family_visual_stage", {})
    args = list(visual.get("argument_vector", []))
    sanitized = []
    skip_next = False
    for token in args:
        if skip_next:
            skip_next = False
            continue
        if token in {"-OutputRoot", "-OutputTag"}:
            skip_next = True
            continue
        sanitized.append(token)
    return {
        "content_identity": stage.get("content_identity"),
        "launcher_path": visual.get("launcher_path"),
        "argument_vector_without_output_paths": sanitized,
        "gameplay_seed": visual.get("gameplay_seed"),
        "audio_switch": visual.get("audio_switch"),
        "music_seed_passed_to_visual_launcher": visual.get("music_seed_passed_to_visual_launcher"),
        "music_profile": visual.get("frozen_c11c_music_profile_id") or stage.get("native_family_music", {}).get("profile_id"),
        "music_route": stage.get("native_family_music", {}).get("route"),
        "composition_delivery_profile": stage.get("composition", {}).get("delivery_profile_id"),
    }


def verify_probe_relationships(results: Mapping[tuple[str, str], Mapping[str, Any]], contract: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for family_key in ("challenge", "loop", "drill"):
        intents = {probe: results[(family_key, probe)]["gui_intent"] for probe in "ABCD"}
        a, b, c, d = intents["A"], intents["B"], intents["C"], intents["D"]
        # A/B replay: the only difference is the unique request ID; prepared semantic projection is equal.
        pa = _projection_without_request_specific_hashes(a)
        pb = _projection_without_request_specific_hashes(b)
        if pa != pb:
            raise E5CanaryError(f"{family_key}: A/B semantic replay differs")
        if a["seed_domains"] != b["seed_domains"]:
            raise E5CanaryError(f"{family_key}: A/B seed pair differs")
        # C: music seed alone changes.
        raw_a = results[(family_key, "A")]["raw_request"]
        raw_c = results[(family_key, "C")]["raw_request"]
        diff_ac = {k for k in set(raw_a) | set(raw_c) if raw_a.get(k) != raw_c.get(k)} - {"request_id", "music_seed"}
        if diff_ac:
            raise E5CanaryError(f"{family_key}: C changed more than music seed/request ID: {sorted(diff_ac)}")
        if a["seed_domains"]["gameplay"] != c["seed_domains"]["gameplay"] or a["seed_domains"]["music"] == c["seed_domains"]["music"]:
            raise E5CanaryError(f"{family_key}: C music-only seed change not isolated")
        # D: gameplay seed alone changes.
        raw_d = results[(family_key, "D")]["raw_request"]
        diff_ad = {k for k in set(raw_a) | set(raw_d) if raw_a.get(k) != raw_d.get(k)} - {"request_id", "seed"}
        if diff_ad:
            raise E5CanaryError(f"{family_key}: D changed more than gameplay seed/request ID: {sorted(diff_ad)}")
        if a["seed_domains"]["music"] != d["seed_domains"]["music"] or a["seed_domains"]["gameplay"] == d["seed_domains"]["gameplay"]:
            raise E5CanaryError(f"{family_key}: D gameplay-only seed change not isolated")
        # For current Loop/Drill preparation, C must not influence the visual launch command; D must change its gameplay seed.
        visual_a = visual_projection(a, family_key)
        visual_c = visual_projection(c, family_key)
        if family_key in {"loop", "drill"} and visual_a != visual_c:
            raise E5CanaryError(f"{family_key}: music-only variation leaked into the gameplay visual stage")
        visual_d = visual_projection(d, family_key)
        if family_key in {"loop", "drill"} and visual_d.get("gameplay_seed") != d["seed_domains"]["gameplay"]["value"]:
            raise E5CanaryError(f"{family_key}: gameplay-only variation did not reach its family visual stage")
        profile_ids = {results[(family_key, p)]["row_receipt"]["gui"]["shape"]["profile_id"] for p in "ABCD"}
        if profile_ids != {contract["families"][family_key]["music"]["profile_id"]}:
            raise E5CanaryError(f"{family_key}: family music profile leaked or changed")
        rows.append({
            "family": family_key,
            "status": "PASS_SEED_DOMAIN_AND_REPLAY_RELATIONS",
            "A_B_semantic_replay": "PASS",
            "C_music_seed_only": "PASS",
            "D_gameplay_seed_only": "PASS",
            "C_visual_stage_isolation": "PASS" if family_key in {"loop", "drill"} else "NOT_MATERIALIZED_E1",
            "profile_id": next(iter(profile_ids)),
            "media_comparison": "NOT_RUN_PREPARE_ONLY",
        })
    return rows


def run_cli(root: Path, request: Mapping[str, Any], cli_dir: Path, label: str, row_root: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    req_path = row_root / "CLI_REQUEST.json"
    result_path = row_root / "CLI_RESULT.json"
    write_json_once(req_path, request)
    command = [
        sys.executable,
        str(cli_dir),
        "--request", str(req_path),
        "--origin", "CLI",
        "--output", str(result_path),
    ]
    try:
        completed = subprocess.run(
            command,
            cwd=str(root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=120,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        (row_root / "CLI_STDOUT.log").write_text(exc.stdout or "", encoding="utf-8")
        (row_root / "CLI_STDERR.log").write_text(exc.stderr or "", encoding="utf-8")
        raise E5CanaryError(f"{label}: CLI child timeout after 120 seconds") from exc
    (row_root / "CLI_STDOUT.log").write_text(completed.stdout or "", encoding="utf-8")
    (row_root / "CLI_STDERR.log").write_text(completed.stderr or "", encoding="utf-8")
    exit_code = int(completed.returncode)
    if exit_code != 0:
        raise E5CanaryError(f"{label}: CLI child exit code {exit_code}; see preserved CLI logs")
    if not result_path.is_file():
        raise E5CanaryError(f"{label}: CLI exited 0 without result JSON")
    payload = load_json(result_path)
    if payload.get("status") != "PASS_E1_PREPARATION_ONLY" or payload.get("validation", {}).get("status") != "PASS_E1_PREPARATION_ONLY":
        raise E5CanaryError(f"{label}: CLI result status is not PASS_E1_PREPARATION_ONLY")
    return payload, {"exit_code": exit_code, "stdout_sha256": sha256_file(row_root / "CLI_STDOUT.log"), "stderr_sha256": sha256_file(row_root / "CLI_STDERR.log"), "result_sha256": sha256_file(result_path)}


def run_batch(project_root: Path, contract_path: Path, result_receipt_path: Path, fixed_batch_id: str | None = None) -> dict[str, Any]:
    root = project_root.resolve(strict=True)
    contract = load_json(contract_path)
    if contract.get("schema") != "C11E-E5-CROSS-FAMILY-PREPARE-CANARY-CONTRACT-V1":
        raise E5CanaryError("E5 canary contract schema mismatch")
    if contract_path.resolve() != safe_project_path(root, CONTRACT_REL).resolve():
        raise E5CanaryError("Contract path is not the installed project-relative contract")
    if not result_receipt_path.parent.is_dir():
        raise E5CanaryError("ResultReceiptPath parent must already exist")
    if result_receipt_path.exists():
        raise E5CanaryError("ResultReceiptPath already exists")
    if result_receipt_path.parent.resolve() == root:
        raise E5CanaryError("ResultReceiptPath may not be the project root")

    static_pins_pre = verify_static_pins(root, contract)
    history_pre = verify_history_refs(root, contract)
    gui_static = static_gui_wiring_check(root)
    service = import_service(root)
    cli_path = safe_project_path(root, CLI_REL)
    if not cli_path.is_file():
        raise E5CanaryError("Shared production-intent CLI is missing")

    now = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    token = uuid.uuid4().hex[:8].upper()
    batch_id = fixed_batch_id or f"E5-XF-PREP-{now}-{token}"
    if not isinstance(batch_id, str) or not batch_id.startswith("E5-XF-PREP-") or any(ch not in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_." for ch in batch_id):
        raise E5CanaryError("BatchId has an invalid E5 namespace")
    batch_base = root / "artifacts" / "tests" / "c11e" / "e5_cross_family_prepare_canary"
    if not batch_base.parent.is_dir():
        raise E5CanaryError("Existing artifacts/tests/c11e parent is absent")
    batch_root = batch_base / batch_id

    raw_map: dict[tuple[str, str], dict[str, Any]] = {}
    request_roots: list[str] = []
    preflight_rows = []
    for family_key in ("challenge", "loop", "drill"):
        for probe in "ABCD":
            raw = build_request(family_key, probe, token, contract)
            output_root = root / "artifacts" / "production" / "c11e" / raw["request_id"]
            if output_root.exists():
                raise E5CanaryError(f"Production output collision: {raw['request_id']}")
            raw_map[(family_key, probe)] = raw
            request_roots.append(str(output_root.relative_to(root)))
            # Non-mutating preflight validates every probe before the one-shot lock exists.
            for origin in ("GUI", "CLI"):
                prepared = service.prepare_c11e_production_intent(raw, root, request_origin=origin)
                intent = prepared["intent"]
                validation = service.validate_c11e_production_intent(intent, root)
                if validation.get("status") != "PASS_E1_PREPARATION_ONLY":
                    raise E5CanaryError(f"Preflight validation failed: {family_key}/{probe}/{origin}")
                shape = validate_intent_shape(intent, family_key, probe, contract)
                preflight_rows.append({"family": family_key, "probe": probe, "origin": origin, "intent_hash": intent["identity"]["intent_hash"], "shape": shape, "intent": intent})

    # The E1 service builds source inventories per family. Union and verify every path now.
    dynamic_pin_map: dict[str, dict[str, Any]] = {}
    for row in preflight_rows:
        prepared = row["intent"]
        for pin in prepared["source_identity"]["source_pins"]:
            current = {"path": pin["path"], "bytes": pin["bytes"], "sha256": pin["sha256"]}
            previous = dynamic_pin_map.get(pin["path"])
            if previous is not None and previous != current:
                raise E5CanaryError(f"Family source pin differs between preparation rows: {pin['path']}")
            dynamic_pin_map[pin["path"]] = current
    dynamic_pins_pre = [verify_pin(root, dynamic_pin_map[path]) for path in sorted(dynamic_pin_map)]

    # All static and dynamic preflight gates are now complete. Create the E5 evidence parent,
    # then reserve one fresh one-shot BatchId. No directory is created before the full preflight.
    if batch_root.exists() or any(batch_base.parent.joinpath(batch_base.name).glob(batch_id + "*")):
        raise E5CanaryError("E5 BatchId evidence collision found; BatchIds are one-shot")
    batch_base.mkdir(parents=False, exist_ok=True)
    batch_root.mkdir(parents=False, exist_ok=False)
    (batch_root / "rows").mkdir()
    (batch_root / "requests").mkdir()
    lock = {
        "schema": "C11E-E5-CROSS-FAMILY-PREPARE-ATTEMPT-LOCK-V1",
        "batch_id": batch_id,
        "created_utc": utc_now(),
        "state": "ATTEMPT_RESERVED",
        "authorization_scope": "E5_PREPARE_ONLY_CROSS_FAMILY_CANARY",
        "production_execution_authorized": False,
        "media_execution_authorized": False,
        "release_authority": "NONE",
        "one_shot": True,
    }
    lock_sha = write_json_once(batch_root / "ATTEMPT_RESERVED.lock.json", lock)
    auth = {
        "schema": "C11E-E5-PREPARE-ONLY-AUTHORIZATION-ONCE-V1",
        "batch_id": batch_id,
        "authorization": "ONE_SHOT_PREPARE_ONLY_TEST_BATCH",
        "operator_approval_record": "CONVERSATION_APPROVAL_2026-11-16",
        "production_dispatch": False,
        "media_created": False,
        "release_authority": "NONE",
    }
    auth_sha = write_json_once(batch_root / "PREPARE_ONLY_AUTHORIZED_ONCE.json", auth)
    print(f"E5_BATCH_ID_RESERVED={batch_id}", file=sys.stderr, flush=True)

    progress = {"schema": "C11E-E5-CROSS-FAMILY-PREPARE-PROGRESS-V1", "batch_id": batch_id, "completed_rows": 0, "expected_rows": 24, "status": "RUNNING", "updated_utc": utc_now()}
    replace_json(batch_root / "BATCH_PROGRESS.json", progress)
    write_json_once(batch_root / "SOURCE_PINS_PRE.json", {"static_pins": static_pins_pre, "dynamic_pins": dynamic_pins_pre, "historical_evidence": history_pre})
    write_json_once(batch_root / "GUI_STATIC_WIRING.json", gui_static)
    write_json_once(batch_root / "PREFLIGHT_RECEIPT.json", {
        "schema": "C11E-E5-CROSS-FAMILY-PREFLIGHT-RECEIPT-V1",
        "batch_id": batch_id,
        "status": "PASS_ALL_12_PROBE_REQUESTS_PREPARED_IN_MEMORY",
        "preflight_pair_count": len(preflight_rows),
        "unique_request_count": len(raw_map),
        "output_roots_absent": request_roots,
        "source_pin_union_count": len(dynamic_pins_pre),
        "gui_static_wiring": gui_static,
        "production_dispatch": False,
        "media_created": False,
        "release_authority": "NONE",
    })

    results: dict[tuple[str, str], dict[str, Any]] = {}
    row_index = 0
    try:
        for family_key in ("challenge", "loop", "drill"):
            for probe in "ABCD":
                raw = raw_map[(family_key, probe)]
                row_index += 1
                label = f"{family_key.upper()}-{probe}"
                row_root = batch_root / "rows" / label
                row_root.mkdir()
                write_json_once(batch_root / "requests" / f"{label}.json", raw)

                gui_prepared = service.prepare_c11e_production_intent(raw, root, request_origin="GUI")
                gui_intent = gui_prepared["intent"]
                gui_validation = service.validate_c11e_production_intent(gui_intent, root)
                if gui_validation.get("status") != "PASS_E1_PREPARATION_ONLY":
                    raise E5CanaryError(f"{label}: GUI-origin service validation failed")
                gui_shape = validate_intent_shape(gui_intent, family_key, probe, contract)
                write_json_once(row_root / "GUI_INTENT.json", gui_intent)
                write_json_once(row_root / "GUI_VALIDATION.json", gui_validation)

                cli_payload, cli_meta = run_cli(root, raw, cli_path, label, row_root)
                cli_intent = cli_payload.get("intent")
                if not isinstance(cli_intent, Mapping):
                    raise E5CanaryError(f"{label}: CLI intent missing")
                cli_shape = validate_intent_shape(cli_intent, family_key, probe, contract)
                if cli_intent.get("request_origin") != "CLI" or gui_intent.get("request_origin") != "GUI":
                    raise E5CanaryError(f"{label}: request-origin provenance was not preserved")
                if gui_intent.get("identity", {}).get("intent_hash") != cli_intent.get("identity", {}).get("intent_hash"):
                    raise E5CanaryError(f"{label}: GUI/CLI semantic intent hash mismatch")
                if gui_intent.get("d9_boundary_preparation") != cli_intent.get("d9_boundary_preparation"):
                    raise E5CanaryError(f"{label}: GUI/CLI family boundary preparation mismatch")
                if gui_intent.get("intent_sha256") == cli_intent.get("intent_sha256"):
                    raise E5CanaryError(f"{label}: origin-bound intent SHA unexpectedly collapsed")
                if gui_shape != cli_shape:
                    raise E5CanaryError(f"{label}: GUI/CLI family shape differs")

                # Ensure the shared service did not materialize a production root.
                planned = root / "artifacts" / "production" / "c11e" / raw["request_id"]
                if planned.exists():
                    raise E5CanaryError(f"{label}: E1 created a production output root")
                row_receipt = {
                    "schema": "C11E-E5-CROSS-FAMILY-PREPARE-ROW-RECEIPT-V1",
                    "batch_id": batch_id,
                    "row": row_index,
                    "family": family_key,
                    "probe": probe,
                    "request_id": raw["request_id"],
                    "status": "PASS_GUI_CLI_E1_PARITY",
                    "gui": {"intent_sha256": gui_intent["intent_sha256"], "intent_hash": gui_intent["identity"]["intent_hash"], "validation": gui_validation["status"], "shape": gui_shape},
                    "cli": {"intent_sha256": cli_intent["intent_sha256"], "intent_hash": cli_intent["identity"]["intent_hash"], "validation": cli_payload["validation"]["status"], "shape": cli_shape, **cli_meta},
                    "intent_semantics_match": True,
                    "boundary_preparations_match": True,
                    "origin_bound_hashes_differ_as_expected": True,
                    "media_created": False,
                    "renderer_invoked": False,
                    "production_dispatch": False,
                    "release_authority": "NONE",
                }
                write_json_once(row_root / "ROW_RECEIPT.json", row_receipt)
                results[(family_key, probe)] = {"raw_request": raw, "gui_intent": gui_intent, "cli_intent": dict(cli_intent), "row_receipt": row_receipt}
                progress["completed_rows"] = row_index
                progress["updated_utc"] = utc_now()
                replace_json(batch_root / "BATCH_PROGRESS.json", progress)

        seed_rows = verify_probe_relationships(results, contract)
        static_pins_post = verify_static_pins(root, contract)
        history_post = verify_history_refs(root, contract)
        dynamic_pins_post = [verify_pin(root, dynamic_pin_map[path]) for path in sorted(dynamic_pin_map)]
        if static_pins_pre != static_pins_post or dynamic_pins_pre != dynamic_pins_post or history_pre != history_post:
            raise E5CanaryError("Pre/post source pins or accepted historical evidence differ")
        write_json_once(batch_root / "SOURCE_PINS_POST.json", {"static_pins": static_pins_post, "dynamic_pins": dynamic_pins_post, "historical_evidence": history_post, "pre_post_equal": True})
        family_profiles = {key: contract["families"][key]["music"]["profile_id"] for key in ("challenge", "loop", "drill")}
        if len(set(family_profiles.values())) != 3:
            raise E5CanaryError("Cross-family music profile identities are not distinct")
        batch_result = {
            "schema": "C11E-E5-CROSS-FAMILY-PREPARE-ONLY-BATCH-RESULT-V1",
            "batch_id": batch_id,
            "created_utc": utc_now(),
            "status": "PASS_E5_PREPARE_ONLY_CROSS_FAMILY",
            "phase": "E5",
            "qualification_stage": "OPENING_CROSS_FAMILY_PREPARE_ONLY_CANARY",
            "families": ["challenge", "loop", "drill"],
            "family_selectors": {
                "challenge": "challenges/parking_v2/CHALLENGE_004",
                "loop": "visual_loops/c11c_fractal_bloom_v1/radial_bloom",
                "drill": "visual_drills/tracking/tier-2",
            },
            "expected_service_origin_rows": 24,
            "completed_service_origin_rows": 24,
            "completed_probe_pairs": 12,
            "gui_cli_service_semantic_parity": "PASS_12_OF_12",
            "actual_qt_gui_runtime": "NOT_RUN_OPERATOR_UI_SESSION_REQUIRED",
            "seed_and_replay_relations": seed_rows,
            "family_music_profiles": family_profiles,
            "profile_non_leakage": "PASS_3_DISTINCT_PROFILE_BINDINGS",
            "source_pin_counts": {"static": len(static_pins_post), "dynamic_union": len(dynamic_pins_post)},
            "source_pins_pre_post_equal": True,
            "historical_evidence_pins": "PASS",
            "family_timebase_contracts": {
                "challenge": {"canonical": "15s sum of 3+7+3+2 at 60fps", "accepted_delivery_reference": "450 frames / 15s at 30fps", "materialized": False},
                "loop": {"accepted_native_source_reference": "660 frames / 22s at 30fps", "materialized": False},
                "drill": {"canonical_gameplay": "630 frames / 21s at 30fps", "native_phase_contract": "3s PRE_ROLL + 21s GAME + 3s END_CTA = 810 frames / 27s at 30fps", "materialized": False},
            },
            "e1_family_adapter": "NOT_CONNECTED_E1",
            "av_media_gate": "BLOCKED_FAMILY_ADAPTER_NOT_CONNECTED_E1",
            "media_outputs": 0,
            "renderer_invoked": False,
            "godot_invoked": False,
            "ffmpeg_invoked": False,
            "production_dispatch": False,
            "release_authority": "NONE",
            "e5_overall": "OPEN_MEDIA_QUALIFICATION_REQUIRED",
            "next_gate": "GOVERNED_E1_FAMILY_ADAPTER_CONNECTION_AND_SEPARATE_AV_CANARY_AUTHORIZATION",
        }
        batch_sha = write_json_once(batch_root / "BATCH_RESULT.json", batch_result)
        launch_receipt = {
            "schema": "C11E-E5-CROSS-FAMILY-PREPARE-RUNNER-LAUNCH-RECEIPT-V1",
            "batch_id": batch_id,
            "batch_result_path": str((batch_root / "BATCH_RESULT.json").relative_to(root)).replace("\\", "/"),
            "batch_result_sha256": batch_sha,
            "evidence_root": str(batch_root.relative_to(root)).replace("\\", "/"),
            "service_origin_rows": 24,
            "technical_status": batch_result["status"],
            "source_pins_pre_post_equal": True,
            "production_dispatch": False,
            "release_authority": "NONE",
            "created_utc": utc_now(),
        }
        launch_sha = write_json_once(batch_root / "RUNNER_LAUNCH_RECEIPT.json", launch_receipt)
        progress["status"] = "PASS_E5_PREPARE_ONLY_CROSS_FAMILY"
        progress["updated_utc"] = utc_now()
        progress["batch_result_sha256"] = batch_sha
        replace_json(batch_root / "BATCH_PROGRESS.json", progress)
        runner_result = {
            "schema": "C11E-E5-CROSS-FAMILY-PREPARE-RUNNER-RESULT-V1",
            "status": "PASS_E5_PREPARE_ONLY_CROSS_FAMILY",
            "batch_id": batch_id,
            "batch_result_path": str((batch_root / "BATCH_RESULT.json").resolve()),
            "batch_result_sha256": batch_sha,
            "runner_launch_receipt_path": str((batch_root / "RUNNER_LAUNCH_RECEIPT.json").resolve()),
            "runner_launch_receipt_sha256": launch_sha,
            "evidence_root": str(batch_root.resolve()),
            "e5_overall": "OPEN_MEDIA_QUALIFICATION_REQUIRED",
            "av_media_gate": "BLOCKED_FAMILY_ADAPTER_NOT_CONNECTED_E1",
            "release_authority": "NONE",
        }
        result_receipt_sha = write_json_once(result_receipt_path, runner_result)
        print(json.dumps({**runner_result, "result_receipt_sha256": result_receipt_sha}, ensure_ascii=False, sort_keys=True))
        return runner_result
    except Exception as exc:
        fail = {
            "schema": "C11E-E5-CROSS-FAMILY-PREPARE-ONLY-FAILURE-V1",
            "batch_id": batch_id,
            "status": "FAIL_E5_PREPARE_ONLY_CROSS_FAMILY",
            "failed_utc": utc_now(),
            "completed_rows": row_index,
            "expected_rows": 24,
            "error": str(exc),
            "traceback": traceback.format_exc(),
            "attempt_reserved_lock_path": str((batch_root / "ATTEMPT_RESERVED.lock.json").resolve()),
            "attempt_reserved_lock_sha256": lock_sha,
            "prepare_only_authorization_sha256": auth_sha,
            "production_dispatch": False,
            "release_authority": "NONE",
        }
        try:
            write_json_once(batch_root / "BATCH_FAILURE.json", fail)
        except Exception:
            pass
        progress["status"] = "FAIL_E5_PREPARE_ONLY_CROSS_FAMILY"
        progress["updated_utc"] = utc_now()
        progress["failure"] = str(exc)
        try:
            replace_json(batch_root / "BATCH_PROGRESS.json", progress)
        except Exception:
            pass
        fail_result = {
            "schema": "C11E-E5-CROSS-FAMILY-PREPARE-RUNNER-RESULT-V1",
            "status": "FAIL_E5_PREPARE_ONLY_CROSS_FAMILY",
            "batch_id": batch_id,
            "batch_failure_path": str((batch_root / "BATCH_FAILURE.json").resolve()),
            "evidence_root": str(batch_root.resolve()),
            "attempt_reserved_lock_sha256": lock_sha,
            "error": str(exc),
            "release_authority": "NONE",
        }
        try:
            write_json_once(result_receipt_path, fail_result)
        except Exception:
            pass
        raise


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="C11-E E5 cross-family PREPARE_ONLY canary.")
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--contract", required=True)
    parser.add_argument("--result-receipt", required=True)
    parser.add_argument("--batch-id", help="Only for isolated developer tests; the installer must omit it.")
    args = parser.parse_args(argv)
    try:
        run_batch(Path(args.project_root), Path(args.contract), Path(args.result_receipt), args.batch_id)
        return 0
    except Exception as exc:
        print(f"E5_CANARY_FAILED: {exc}", file=sys.stderr, flush=True)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
