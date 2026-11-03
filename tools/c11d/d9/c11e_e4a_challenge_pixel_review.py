#!/usr/bin/env python3
"""C11-E E4A Challenge pixel-proof runner (test-only; no production dispatch/media)."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

ROOT = Path(__file__).resolve().parents[3]
SERVICE_REL = Path("c11c-suite/c11c-producer/c11e_production_service.py")
MATERIALIZER_REL = Path("tools/c11d/d9/materialize_challenge_visual_payload_in_memory.gd")
TEST_REL = Path("tools/c11d/d9/test_c11e_e4a_challenge_pixel_review.py")
APPROVAL_REL = Path("definitions/c11d/production/C11E_E4A_CHALLENGE_EDITORIAL_PRESENTATION_POLICY_APPROVAL_V1.json")
LAYOUT_REL = Path("docs/current/d/D1.5_PLATFORM_LAYOUT_TEMPLATE_CONTRACT.md")
MANIFEST_REL = Path("release/C11C_FREEZE_PACKAGE_MANIFEST.json")
APPROVAL_SHA256 = "764629384896a255cf992da89fa427c19f60f9b2e623b81ad17d909674b466b5"
LAYOUT_SHA256 = "3a8e7bfc13a369acaf9d5abe9583f3e93e0990a3b1262b8a839e81ee873c6461"
MANIFEST_SHA256 = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
CHALLENGE_SHA256 = "6a674c02c2d8831a872691954f1cc40e2492193f9b136f60656730a7be686b71"
EXPECTED_FIELDS = {
    "title", "subtitle", "call_to_action", "language", "player_name", "challenge_label"
}


class E4APixelReviewError(RuntimeError):
    pass


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict):
        raise E4APixelReviewError(f"Expected JSON object: {path}")
    return value


def validate_static_authorities(root: Path = ROOT) -> dict[str, str]:
    pins = {
        "frozen_manifest": (MANIFEST_REL, MANIFEST_SHA256),
        "challenge_004": (Path("challenges/CHALLENGE_004.json"), CHALLENGE_SHA256),
        "approved_policy": (APPROVAL_REL, APPROVAL_SHA256),
        "d1_5_layout": (LAYOUT_REL, LAYOUT_SHA256),
    }
    observed: dict[str, str] = {}
    for label, (relative, expected) in pins.items():
        path = root / relative
        if not path.is_file():
            raise E4APixelReviewError(f"Required authority file is missing: {relative.as_posix()}")
        actual = sha256_file(path)
        if actual != expected:
            raise E4APixelReviewError(f"Authority pin mismatch for {relative.as_posix()}: {actual}")
        observed[label] = actual

    approval = load_json(root / APPROVAL_REL)
    if approval.get("schema") != "C11E-E4A-CHALLENGE-EDITORIAL-PRESENTATION-POLICY-APPROVAL-V1":
        raise E4APixelReviewError("Approved E4A policy schema mismatch")
    if approval.get("status") != "APPROVED_BY_OPERATOR_FOR_CHALLENGE_SEMANTIC_MAPPING":
        raise E4APixelReviewError("E4A policy approval marker is absent")
    if approval.get("render_test_authorization", {}).get("isolated_e4a_test_rendering") != "AUTHORIZED_BY_OPERATOR_CURRENT_INSTRUCTION":
        raise E4APixelReviewError("Isolated E4A test-render authorization is absent")
    if approval.get("render_test_authorization", {}).get("production_dispatch") != "NOT_AUTHORIZED":
        raise E4APixelReviewError("Policy unexpectedly authorizes production dispatch")
    fields = {row.get("field"): row for row in approval.get("fields", []) if isinstance(row, dict)}
    if set(fields) != EXPECTED_FIELDS:
        raise E4APixelReviewError("Approved E4A policy field matrix is not the exact six-field Challenge allowlist")
    expected_mapping = {
        "title": ("HEADER", ["HOOK"]),
        "subtitle": ("HEADER", ["HOOK"]),
        "player_name": ("CHALLENGE_OVERLAY", ["HOOK", "GAME"]),
        "challenge_label": ("CHALLENGE_OVERLAY", ["HOOK", "GAME"]),
        "call_to_action": ("FOOTER", ["CTA"]),
        "language": (None, []),
    }
    for name, (region, windows) in expected_mapping.items():
        if fields[name].get("region") != region or fields[name].get("source_phase_windows") != windows:
            raise E4APixelReviewError(f"Approved policy mapping drift: {name}")
    layout_text = (root / LAYOUT_REL).read_text(encoding="utf-8-sig")
    required_geometry = (
        "Logical width: 540", "Logical height: 960",
        "Rect2(0, 0, 540, 144)", "Rect2(0, 144, 540, 672)", "Rect2(0, 816, 540, 144)",
    )
    if any(token not in layout_text for token in required_geometry):
        raise E4APixelReviewError("D1.5 region geometry does not match the hash-pinned layout contract")
    return observed


def load_service(root: Path = ROOT):
    path = root / SERVICE_REL
    if not path.is_file():
        raise E4APixelReviewError(f"Shared E1 production service is missing: {SERVICE_REL.as_posix()}")
    module_name = "c11e_e4a_pixel_review_service"
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise E4APixelReviewError("Cannot load the existing shared E1 production service")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def validate_e1_intent(intent: Mapping[str, Any], variant_id: str) -> None:
    if intent.get("schema") != "C11-E-PRODUCTION-INTENT-V1" or intent.get("status") != "PREPARED_E1_NOT_DISPATCHED":
        raise E4APixelReviewError(f"Variant {variant_id}: not a sealed, non-dispatched E1 intent")
    if intent.get("service_version") != "0.2.0-E3.2":
        raise E4APixelReviewError(f"Variant {variant_id}: shared E1 service version drift")
    request = intent.get("request", {})
    selection = request.get("selection", {}) if isinstance(request, Mapping) else {}
    if request.get("content_type") != "challenges" or selection.get("content_type") != "challenges":
        raise E4APixelReviewError(f"Variant {variant_id}: content type is not Challenge")
    if selection.get("variant_id") != "CHALLENGE_004" or selection.get("family_id") != "parking_v2":
        raise E4APixelReviewError(f"Variant {variant_id}: selector is not parking_v2/CHALLENGE_004")
    if request.get("mode") != "REVIEW" or intent.get("request_origin") != "TEST":
        raise E4APixelReviewError(f"Variant {variant_id}: request mode/origin mismatch")
    delivery = intent.get("delivery", {})
    if delivery.get("resolved_profile_id") != "REVIEW_720" or delivery.get("presentation_profile_id") != "social_default_v1":
        raise E4APixelReviewError(f"Variant {variant_id}: delivery/presentation identity mismatch")
    if delivery.get("audio_enabled") is not False:
        raise E4APixelReviewError(f"Variant {variant_id}: audio must remain disabled in this pixel test")
    seeds = intent.get("seed_domains", {})
    if seeds.get("gameplay", {}).get("value") != 314159 or seeds.get("music", {}).get("value") != 840001:
        raise E4APixelReviewError(f"Variant {variant_id}: fixed independent seed domains drifted")
    if seeds.get("independent_domains") is not True or intent.get("output", {}).get("created") is not False:
        raise E4APixelReviewError(f"Variant {variant_id}: seed/output governance mismatch")
    boundary = intent.get("execution_boundary", {})
    for field in ("dispatch_authorized", "renderer_input_emitted", "renderer_dispatch_invoked", "renderer_activation", "production_execution", "media_created"):
        if boundary.get(field) is not False:
            raise E4APixelReviewError(f"Variant {variant_id}: E1 intent boundary was crossed: {field}")
    if boundary.get("release_authority") != "NONE" or boundary.get("d4_8") != "BLOCKED":
        raise E4APixelReviewError(f"Variant {variant_id}: governance locks drifted")
    editorial = intent.get("editorial", {})
    if not isinstance(editorial, Mapping) or set(editorial) != EXPECTED_FIELDS:
        raise E4APixelReviewError(f"Variant {variant_id}: D9.9 effective editorial allowlist mismatch")
    identity = intent.get("identity", {})
    for key in ("request_hash", "editorial_hash", "plan_hash", "intent_hash"):
        if not re.fullmatch(r"[0-9a-f]{64}", str(identity.get(key, ""))):
            raise E4APixelReviewError(f"Variant {variant_id}: invalid E1 identity hash {key}")
    consumption = intent.get("editorial_field_consumption", {})
    if set(consumption) != EXPECTED_FIELDS or any(row.get("consumer_status") != "NOT_CONSUMED_E1" for row in consumption.values()):
        raise E4APixelReviewError(f"Variant {variant_id}: E1 consumption status unexpectedly changed")


def _intent_raw_request(request_id: str, editorial_values: Mapping[str, str], resolver: Any) -> dict[str, Any]:
    return {
        "schema": resolver.REQUEST_SCHEMA_ID,
        "schema_version": "1.0",
        "request_id": request_id,
        "mode": "REVIEW",
        "selection": {
            "content_type": "challenges",
            "family_id": "parking_v2",
            "variant_id": "CHALLENGE_004",
        },
        "seed": 314159,
        "music_seed": 840001,
        "delivery_profile_id": "REVIEW_720",
        "presentation_profile_id": "social_default_v1",
        "variation_index": 0,
        "audio_enabled": False,
        "personalization_enabled": True,
        "editorial_profile": {},
        "production_override": dict(editorial_values),
        "provenance": {
            "source_revision": "C11E-E4A-CHALLENGE-PIXEL-REVIEW-V1",
            "request_origin": "TEST",
        },
    }


def build_three_e1_intents(root: Path = ROOT) -> list[dict[str, Any]]:
    service = load_service(root)
    resolver = service._load_d9_resolver(root)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:8].upper()
    variants = [
        ("A", {field: "" for field in EXPECTED_FIELDS}),
        ("B", {
            "title": "E4A PIXEL TITLE TEST",
            "subtitle": "D9.9 editorial subtitle",
            "call_to_action": "FOLLOW FOR MORE",
            "language": "es",
            "player_name": "PLAYER PIXEL TEST",
            "challenge_label": "PARKING CHALLENGE",
        }),
        ("C", {
            "title": "E4A PIXEL TITLE TEST",
            "subtitle": "D9.9 editorial subtitle",
            "call_to_action": "FOLLOW FOR MORE",
            "language": "en",
            "player_name": "",
            "challenge_label": "",
        }),
    ]
    output: list[dict[str, Any]] = []
    for variant_id, values in variants:
        request_id = f"E4A-CH004-PIXEL-{variant_id}-{stamp}"
        raw_request = _intent_raw_request(request_id, values, resolver)
        prepared = service.prepare_c11e_production_intent(raw_request, root, request_origin="TEST", resolver_module=resolver)
        intent = prepared.get("intent")
        if not isinstance(intent, Mapping):
            raise E4APixelReviewError(f"Variant {variant_id}: shared E1 service returned no intent")
        intent_dict = dict(intent)
        validate_e1_intent(intent_dict, variant_id)
        output.append({"id": variant_id, "intent": intent_dict})
    # The test changes editorial only; request/selection/seed/profile/audiovisual controls stay fixed.
    a, b, c = [item["intent"] for item in output]
    for intent in (b, c):
        if intent["seed_domains"] != a["seed_domains"] or intent["delivery"] != a["delivery"] or intent["request"]["selection"] != a["request"]["selection"]:
            raise E4APixelReviewError("A/B/C requests do not preserve selector, seed, and delivery identity")
    be, ce = b["editorial"], c["editorial"]
    for field in ("title", "subtitle", "call_to_action"):
        if be[field] != ce[field]:
            raise E4APixelReviewError(f"Variant C changed visual field {field} relative to B")
    if be["language"] == ce["language"] or be["player_name"] == ce["player_name"] or be["challenge_label"] == ce["challenge_label"]:
        raise E4APixelReviewError("B/C controls did not isolate language and unresolved Challenge-only fields")
    return output


def _godot_executable(value: str | None) -> str:
    candidate = value or os.environ.get("C11D_GODOT_EXECUTABLE") or shutil.which("godot") or shutil.which("godot.exe")
    if not candidate:
        raise E4APixelReviewError("Godot 4.7.1 executable not found; set C11D_GODOT_EXECUTABLE or pass --godot")
    resolved = shutil.which(candidate) or candidate
    if not Path(resolved).is_file():
        raise E4APixelReviewError(f"Godot executable does not exist: {resolved}")
    return str(Path(resolved).resolve())


def _png_dimensions(data: bytes) -> tuple[int, int]:
    if len(data) < 24 or data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        raise E4APixelReviewError("Pixel artifact is not a valid PNG header")
    return int.from_bytes(data[16:20], "big"), int.from_bytes(data[20:24], "big")


def run(root: Path = ROOT, godot_arg: str | None = None) -> int:
    authorities = validate_static_authorities(root)
    test_path = root / TEST_REL
    test_run = subprocess.run(
        [sys.executable, "-B", str(test_path)], cwd=str(root), capture_output=True,
        text=True, encoding="utf-8", errors="replace", check=False,
    )
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S") + "_" + uuid.uuid4().hex[:8]
    evidence_dir = root / "artifacts" / "tests" / "c11e" / "e4a_pixel_review" / ("RUN_" + stamp)
    evidence_dir.mkdir(parents=True, exist_ok=False)
    (evidence_dir / "python_tests.stdout.txt").write_text(test_run.stdout, encoding="utf-8")
    (evidence_dir / "python_tests.stderr.txt").write_text(test_run.stderr, encoding="utf-8")
    if test_run.returncode != 0:
        raise E4APixelReviewError(f"E4A Python focused tests failed (exit {test_run.returncode}); evidence: {evidence_dir}")

    intents = build_three_e1_intents(root)
    for item in intents:
        write_json(evidence_dir / f"e1_intent_{item['id']}.json", item["intent"])
    config_path = evidence_dir / "pixel_test_config.json"
    config = {
        "schema": "C11E-E4A-CHALLENGE-PIXEL-TEST-CONFIG-V1",
        "output_dir": str(evidence_dir.resolve()),
        "variants": intents,
        "authorities": authorities,
    }
    write_json(config_path, config)

    godot = _godot_executable(godot_arg)
    version = subprocess.run([godot, "--version"], cwd=str(root), capture_output=True, text=True, encoding="utf-8", errors="replace", check=False)
    (evidence_dir / "godot_version.stdout.txt").write_text(version.stdout, encoding="utf-8")
    (evidence_dir / "godot_version.stderr.txt").write_text(version.stderr, encoding="utf-8")
    if version.returncode != 0 or "4.7.1" not in (version.stdout + version.stderr):
        raise E4APixelReviewError(f"Expected Godot 4.7.1; version probe exit={version.returncode}, output={version.stdout.strip()} {version.stderr.strip()}")

    command = [
        godot, "--path", str(root), "--script", "res://tools/c11d/d9/materialize_challenge_visual_payload_in_memory.gd",
        "--", "--e4a-config", str(config_path.resolve()),
    ]
    process = subprocess.run(command, cwd=str(root), capture_output=True, text=True, encoding="utf-8", errors="replace", check=False)
    (evidence_dir / "godot.stdout.txt").write_text(process.stdout, encoding="utf-8")
    (evidence_dir / "godot.stderr.txt").write_text(process.stderr, encoding="utf-8")
    combined = process.stdout + "\n" + process.stderr
    if process.returncode != 0:
        raise E4APixelReviewError(f"E4A Godot pixel test failed (exit {process.returncode}); evidence: {evidence_dir}\n{combined[-5000:]}")
    if "C11E E4A CHALLENGE EDITORIAL PIXEL RENDER PASS" not in process.stdout:
        raise E4APixelReviewError(f"Godot exited 0 without the E4A pixel PASS marker; evidence: {evidence_dir}")
    if re.search(r"(?i)(SCRIPT ERROR:|ERROR:)", combined):
        raise E4APixelReviewError(f"Godot pixel test emitted an error marker; evidence: {evidence_dir}")

    report_path = evidence_dir / "C11E_E4A_PIXEL_RENDER_REPORT.json"
    if not report_path.is_file():
        raise E4APixelReviewError(f"Godot did not write its pixel report: {evidence_dir}")
    report = load_json(report_path)
    if report.get("schema") != "C11E-E4A-CHALLENGE-PIXEL-RENDER-REPORT-V1" or report.get("status") != "PASS_ISOLATED_EDITORIAL_PIXEL_PROOF_TEST_ONLY":
        raise E4APixelReviewError("Godot report schema/status is not accepted")
    if report.get("game_frame_record_count") != 420 or report.get("game_frame_records_sha256") == "":
        raise E4APixelReviewError("Source frame identity is incomplete")
    if len(report.get("pixel_artifacts", [])) != 18 or len(report.get("pixel_comparisons", [])) != 12:
        raise E4APixelReviewError("Expected 18 rendered PNGs and 12 pixel comparisons")
    for artifact in report["pixel_artifacts"]:
        relative = Path(str(artifact.get("path", "")))
        if relative.is_absolute() or ".." in relative.parts:
            raise E4APixelReviewError("Pixel report contains unsafe artifact path")
        image_path = root / relative
        if not image_path.is_file():
            raise E4APixelReviewError(f"Pixel PNG missing: {relative}")
        data = image_path.read_bytes()
        if sha256_bytes(data) != artifact.get("sha256"):
            raise E4APixelReviewError(f"Pixel PNG hash mismatch: {relative}")
        width, height = _png_dimensions(data)
        if (width, height) != (540, 960) or artifact.get("width") != 540 or artifact.get("height") != 960:
            raise E4APixelReviewError(f"Pixel PNG has unexpected dimensions: {relative}")
    dispositions = {row.get("field"): row.get("disposition") for row in report.get("field_dispositions", []) if isinstance(row, dict)}
    required_dispositions = {
        "title": "READY_FOR_ISOLATED_TEST_PIXEL_DRAW",
        "subtitle": "READY_FOR_ISOLATED_TEST_PIXEL_DRAW",
        "call_to_action": "READY_FOR_ISOLATED_TEST_PIXEL_DRAW",
        "player_name": "BLOCKED_GEOMETRY_UNRESOLVED",
        "challenge_label": "BLOCKED_GEOMETRY_UNRESOLVED",
        "language": "METADATA_ONLY",
    }
    if dispositions != required_dispositions:
        raise E4APixelReviewError(f"Unexpected D1.5/policy field dispositions: {dispositions}")

    receipt = {
        "schema": "C11E-E4A-CHALLENGE-PIXEL-REVIEW-RUNNER-RECEIPT-V1",
        "schema_version": "1.0",
        "status": "PASS_ISOLATED_TEST_PIXEL_RENDER_ONLY",
        "godot": {"executable": godot, "version": (version.stdout + version.stderr).strip(), "version_exit_code": version.returncode},
        "command": command,
        "godot_exit_code": process.returncode,
        "python_test_exit_code": test_run.returncode,
        "stdout_sha256": sha256_file(evidence_dir / "godot.stdout.txt"),
        "stderr_sha256": sha256_file(evidence_dir / "godot.stderr.txt"),
        "pixel_report_path": str(report_path.relative_to(root)).replace("\\", "/"),
        "pixel_report_sha256": sha256_file(report_path),
        "pixel_png_count": len(report["pixel_artifacts"]),
        "pixel_comparison_count": len(report["pixel_comparisons"]),
        "source_authorities": authorities,
        "governance": {
            "production_renderer_activation": False,
            "production_dispatch": False,
            "production_media_created": False,
            "c11c_source_mutation": False,
            "d4_8": "BLOCKED",
            "d9_10": "PREPARE_ONLY",
            "d9_14": "BLOCKED",
            "d9_16": "BLOCKED",
            "d9_17": "BLOCKED_NO_GO",
            "d10": "BLOCKED_FOR_PROMOTION",
            "release_authority": "NONE",
        },
    }
    receipt_path = evidence_dir / "C11E_E4A_PIXEL_REVIEW_RUNNER_RECEIPT.json"
    write_json(receipt_path, receipt)
    sums = []
    for path in sorted(evidence_dir.iterdir()):
        if path.is_file() and path.name != "SHA256SUMS.txt":
            sums.append(f"{sha256_file(path)}  {path.name}")
    for artifact in report["pixel_artifacts"]:
        image_path = root / str(artifact["path"])
        sums.append(f"{sha256_file(image_path)}  {artifact['path']}")
    (evidence_dir / "SHA256SUMS.txt").write_text("\n".join(sums) + "\n", encoding="utf-8")
    print("C11E_E4A_CHALLENGE_PIXEL_REVIEW=PASS_ISOLATED_TEST_ONLY")
    print(f"GODOT_VERSION={(version.stdout + version.stderr).strip()}")
    print("PYTHON_FOCUSED_TESTS=PASS")
    print("PIXEL_PNGS=18/18 @ 540x960")
    print("PIXEL_COMPARISONS=12/12")
    print("FIELD_DISPOSITIONS=title/subtitle/CTA=PIXEL_TEST; player_name/challenge_label=BLOCKED_GEOMETRY; language=METADATA_ONLY")
    print("PRODUCTION_RENDERER=false")
    print("PRODUCTION_DISPATCH=false")
    print("PRODUCTION_MEDIA=false")
    print("D4.8=BLOCKED")
    print("D9.10=PREPARE_ONLY")
    print("RELEASE_AUTHORITY=NONE")
    print(f"EVIDENCE_DIR={evidence_dir}")
    print(f"RECEIPT_SHA256={sha256_file(receipt_path)}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--godot", help="Path to Godot 4.7.1 executable; defaults to C11D_GODOT_EXECUTABLE or PATH")
    args = parser.parse_args()
    try:
        return run(ROOT, args.godot)
    except Exception as exc:
        print(f"C11E_E4A_CHALLENGE_PIXEL_REVIEW=FAIL {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
