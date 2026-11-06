#!/usr/bin/env python3
"""D-owned E4B Loop populated GUI/CLI parity helper; preparation-only."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
import unicodedata
from pathlib import Path
from typing import Any

FIELDS = ("title", "subtitle", "call_to_action", "language")
EXPECTED_EDITORIAL = {
    "title": "T\u00edtulo editorial Loop \u2014 composici\u00f3n arm\u00f3nica en movimiento",
    "subtitle": "Explora el patr\u00f3n geom\u00e9trico, observa sus ciclos y descubre c\u00f3mo evoluciona la forma",
    "call_to_action": "Guarda este loop y comparte tu patr\u00f3n favorito",
    "language": "es",
}
MOJIBAKE_CODEPOINTS = {0x00C2, 0x00C3, 0x00E2, 0xFFFD}


class ParityError(ValueError):
    """Raised when GUI/CLI populated editorial parity is not proven."""


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict):
        raise ParityError(f"JSON object required: {path}")
    return value


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rendered = json.dumps(value, ensure_ascii=False, indent=2, sort_keys=False) + "\n"
    path.write_text(rendered, encoding="utf-8", newline="\n")


def assert_no_mojibake(value: str, label: str) -> None:
    if any(ord(char) in MOJIBAKE_CODEPOINTS for char in value):
        raise ParityError(f"{label} contains a UTF-8/ANSI mojibake marker")
    if "\u00c3\u00ad" in value or "\u00c3\u00b3" in value or "\u00c3\u00a1" in value:
        raise ParityError(f"{label} contains a double-encoded Spanish sequence")
    if unicodedata.normalize("NFC", value) != value:
        raise ParityError(f"{label} is not Unicode NFC normalized")


def validate_editorial(editorial: Any, label: str) -> dict[str, str]:
    if not isinstance(editorial, dict):
        raise ParityError(f"{label} must be an object")
    if set(editorial) != set(FIELDS):
        raise ParityError(f"{label} must contain exactly {list(FIELDS)}")
    result: dict[str, str] = {}
    for field in FIELDS:
        value = editorial[field]
        if not isinstance(value, str):
            raise ParityError(f"{label}.{field} must be a string")
        if len(value) > 160:
            raise ParityError(f"{label}.{field} exceeds 160 codepoints")
        assert_no_mojibake(value, f"{label}.{field}")
        result[field] = value
    if result != EXPECTED_EDITORIAL:
        raise ParityError(f"{label} does not equal the versioned populated Loop fixture")
    return result


def _load_gui_bundle(gui_root: Path) -> dict[str, Any]:
    gui_root = gui_root.resolve(strict=True)
    required = {
        "request": gui_root / "request.json",
        "canonical": gui_root / "canonical_request.json",
        "editorial_resolution": gui_root / "editorial_resolution.json",
        "plan": gui_root / "universal_plan.json",
        "bridge": gui_root / "editorial_render_bridge_plan.json",
        "adapter": gui_root / "d_render_adapter_envelope.json",
        "producer_receipt": gui_root / "producer_universal_receipt.json",
        "e1_receipt": gui_root / "c11e_production_intent_receipt.json",
        "parity": gui_root / "gui_cli_parity.json",
        "lifecycle": gui_root / "cross_suite_lifecycle_receipt.json",
    }
    missing = [str(path) for path in required.values() if not path.is_file()]
    if missing:
        raise ParityError("GUI evidence is incomplete: " + "; ".join(missing))
    return {key: read_json(path) for key, path in required.items()} | {"root": gui_root}


def _gui_editorial(bundle: dict[str, Any]) -> dict[str, str]:
    request = bundle["request"]
    canonical = bundle["canonical"]
    resolution = bundle["editorial_resolution"]
    plan = bundle["plan"]
    if request.get("provenance", {}).get("request_origin") != "GUI":
        raise ParityError("Source D99 request must preserve request_origin=GUI")
    if request.get("selection") != {
        "content_type": "visual_loops",
        "family_id": "c11c_geometric_waves_v1",
        "subtype_id": "harmonic_membrane",
    }:
        raise ParityError("GUI request selection is not the admitted Loop parity fixture")
    editorial = validate_editorial(request.get("production_override"), "GUI request production_override")
    if validate_editorial(canonical.get("editorial"), "GUI canonical_request.editorial") != editorial:
        raise ParityError("GUI canonical_request.editorial differs from raw GUI overrides")
    if canonical.get("request_id") != request.get("request_id"):
        raise ParityError("GUI canonical request identity differs from raw request")
    if canonical.get("selection", {}).get("content_type") != "visual_loops":
        raise ParityError("GUI canonical request content type is not visual_loops")
    if canonical.get("seed") != request.get("seed") or canonical.get("music_seed") != request.get("music_seed"):
        raise ParityError("GUI canonical request seed values differ from raw request")
    if resolution.get("values") != editorial:
        raise ParityError("GUI editorial_resolution.values differs from request overrides")
    if plan.get("editorial") != editorial:
        raise ParityError("GUI universal_plan.editorial differs from request overrides")
    if resolution.get("request_plan_state") != "PENDING_D9_9_UNIVERSAL_REQUEST_ADAPTER":
        raise ParityError("Expected current D9.9 Loop adapter pending state changed")
    if resolution.get("request_plan_compatible") is not False:
        raise ParityError("Loop editorial resolution unexpectedly claims request-plan compatibility")
    if plan.get("selection", {}).get("content_type") != "visual_loops":
        raise ParityError("GUI plan content type mismatch")
    parity = bundle["parity"]
    if parity.get("status") != "PASS" or not parity.get("checks") or not all(parity.get("checks", {}).values()):
        raise ParityError("GUI internal D9 parity receipt is not fully PASS")
    e1_checks = parity.get("e1_shared_service", {}).get("checks", {})
    if parity.get("e1_shared_service", {}).get("status") != "PASS" or not e1_checks or not all(e1_checks.values()):
        raise ParityError("GUI internal E1 shared-service parity receipt is not fully PASS")
    e1_receipt = bundle["e1_receipt"]
    producer_receipt = bundle["producer_receipt"]
    for field in ("request_hash", "editorial_hash"):
        if e1_receipt.get(field) != plan.get(field):
            raise ParityError(f"GUI E1 receipt identity differs from plan: {field}")
    if e1_receipt.get("plan_hash") != producer_receipt.get("plan_hash"):
        raise ParityError("GUI E1 receipt plan_hash differs from Producer receipt")
    if producer_receipt.get("result") != "PASS_BRIDGE_PLANNING_ONLY":
        raise ParityError("GUI D9.10 producer receipt is not planning PASS")
    if producer_receipt.get("request_hash") != plan.get("request_hash") or producer_receipt.get("editorial_hash") != plan.get("editorial_hash"):
        raise ParityError("GUI producer receipt identity differs from plan")
    bridge = bundle["bridge"]
    if bridge.get("status") != "PLANNING_ONLY_NOT_RENDERABLE" or producer_receipt.get("bridge_record_hash") != bridge.get("record_hash"):
        raise ParityError("GUI bridge record identity/status mismatch")
    for field in ("request_hash", "editorial_hash"):
        if bridge.get("identity", {}).get(field) != plan.get(field):
            raise ParityError(f"GUI bridge identity differs from plan: {field}")
    if bridge.get("identity", {}).get("plan_hash") != producer_receipt.get("plan_hash"):
        raise ParityError("GUI bridge plan_hash differs from Producer receipt")
    adapter = bundle["adapter"]
    if adapter.get("status") != "PREPARED_NOT_DISPATCHED_RENDERER_DISABLED":
        raise ParityError("GUI D-only adapter envelope is not prepare-only")
    if producer_receipt.get("d_only_adapter_envelope_hash") != adapter.get("envelope_hash"):
        raise ParityError("GUI producer receipt adapter hash mismatch")
    adapter_identity = adapter.get("source_identity", {})
    for field in ("request_hash", "editorial_hash"):
        if adapter_identity.get(field) != plan.get(field):
            raise ParityError(f"GUI adapter source identity differs from plan: {field}")
    if adapter_identity.get("plan_hash") != producer_receipt.get("plan_hash"):
        raise ParityError("GUI adapter plan_hash differs from Producer receipt")
    if adapter_identity.get("bridge_record_hash") != bridge.get("record_hash"):
        raise ParityError("GUI adapter bridge_record_hash differs from bridge")
    if e1_receipt.get("status") != "PASS_E1_PREPARATION_ONLY":
        raise ParityError("GUI E1 receipt is not PASS_E1_PREPARATION_ONLY")
    lifecycle = bundle["lifecycle"]
    if lifecycle.get("status") != "PASS_PLAN_ONLY" or len(lifecycle.get("stages", [])) != 5:
        raise ParityError("GUI D9.13 lifecycle must be PASS_PLAN_ONLY across five stages")
    if any(not str(stage.get("status", "")).startswith("PASS_") for stage in lifecycle.get("stages", [])):
        raise ParityError("GUI D9.13 lifecycle contains a non-PASS stage")
    return editorial


def prepare_cli_request(gui_root: Path, output_path: Path, request_id: str, preparation_receipt: Path) -> dict[str, Any]:
    bundle = _load_gui_bundle(gui_root)
    editorial = _gui_editorial(bundle)
    gui_request = bundle["request"]
    request = copy.deepcopy(gui_request)
    request["request_id"] = request_id
    provenance = request.get("provenance")
    if not isinstance(provenance, dict):
        raise ParityError("GUI request provenance must be an object")
    provenance["source_revision"] = "C11E-E4B-LOOP-CLI-GUI-PARITY-V2"
    provenance["request_origin"] = "CLI"
    write_json(output_path, request)

    # Re-read bytes from disk; this catches encoding/serialization regressions before either CLI runs.
    round_trip = read_json(output_path)
    round_trip_editorial = validate_editorial(round_trip.get("production_override"), "CLI request round-trip")
    if round_trip_editorial != editorial:
        raise ParityError("CLI request UTF-8 round-trip changed populated editorial values")
    if round_trip.get("provenance", {}).get("request_origin") != "CLI":
        raise ParityError("CLI request origin was not set to CLI")
    if round_trip.get("request_id") != request_id:
        raise ParityError("CLI request ID round-trip mismatch")

    record = {
        "schema": "C11E-E4B-LOOP-CLI-REQUEST-PREPARATION-RECEIPT-V2",
        "status": "PASS_UTF8_REQUEST_PREPARED",
        "gui_request_id": gui_request.get("request_id"),
        "cli_request_id": request_id,
        "gui_request_file_sha256": sha256_file(bundle["root"] / "request.json"),
        "cli_request_file_sha256": sha256_file(output_path),
        "editorial_fields": list(FIELDS),
        "editorial": editorial,
        "unicode": {
            "source": "GUI_EXPORTED_JSON_UTF8",
            "serialization": "PYTHON_UTF8_ENSURE_ASCII_FALSE_NO_BOM",
            "round_trip": "PASS",
            "normalization": "NFC",
            "mojibake_markers": "ABSENT",
        },
        "request_origin": "CLI",
        "renderer": False,
        "media_created": False,
        "release_authority": "NONE",
    }
    write_json(preparation_receipt, record)
    return record


def verify_parity(
    gui_root: Path,
    cli_request_path: Path,
    d9_result_path: Path,
    e1_result_path: Path,
    receipt_path: Path,
) -> dict[str, Any]:
    bundle = _load_gui_bundle(gui_root)
    gui_editorial = _gui_editorial(bundle)
    gui_request = bundle["request"]
    gui_plan = bundle["plan"]
    d9 = read_json(d9_result_path)
    e1_result = read_json(e1_result_path)
    cli_request = read_json(cli_request_path)

    cli_editorial = validate_editorial(cli_request.get("production_override"), "CLI request")
    if cli_editorial != gui_editorial:
        raise ParityError("GUI/CLI request editorial values differ")
    if cli_request.get("provenance", {}).get("request_origin") != "CLI":
        raise ParityError("CLI request provenance is not CLI")
    if cli_request.get("selection") != gui_request.get("selection"):
        raise ParityError("GUI/CLI selection differs")
    for field in (
        "mode", "seed", "music_seed", "delivery_profile_id", "presentation_profile_id",
        "variation_index", "audio_enabled", "personalization_enabled", "editorial_profile",
    ):
        if cli_request.get(field) != gui_request.get(field):
            raise ParityError(f"GUI/CLI request field differs: {field}")

    if d9.get("status") != "PLANNED":
        raise ParityError("D9.9 CLI did not return PLANNED")
    canonical = d9.get("canonical_request", {})
    d9_plan = d9.get("plan", {})
    canonical_selection = canonical.get("selection", {})
    gui_selection = gui_request.get("selection", {})
    for key in ("content_type", "family_id", "subtype_id"):
        if canonical_selection.get(key) != gui_selection.get(key):
            raise ParityError(f"D9.9 canonical selection differs from GUI: {key}")
    if validate_editorial(canonical.get("editorial"), "D9.9 canonical editorial") != gui_editorial:
        raise ParityError("D9.9 canonical editorial values differ from GUI")
    if validate_editorial(d9_plan.get("editorial"), "D9.9 plan editorial") != gui_editorial:
        raise ParityError("D9.9 plan editorial values differ from GUI")
    gui_editorial_hash = gui_plan.get("editorial_hash")
    if not gui_editorial_hash or d9.get("editorial_hash") != gui_editorial_hash:
        raise ParityError("D9.9 CLI editorial hash does not match GUI editorial hash")
    if d9_plan.get("editorial_hash") != gui_editorial_hash:
        raise ParityError("D9.9 CLI plan editorial hash mismatch")
    if d9.get("request_hash") != d9_plan.get("request_hash"):
        raise ParityError("D9.9 CLI request hash does not match plan")
    if not d9.get("plan_hash"):
        raise ParityError("D9.9 CLI plan hash missing")

    bridge = d9.get("bridge_planning_record", {})
    adapter = d9.get("d_only_adapter_envelope", {})
    if bridge.get("status") != "PLANNING_ONLY_NOT_RENDERABLE":
        raise ParityError("D9.10 bridge is not planning-only")
    if bridge.get("route", {}).get("route_id") != "FUTURE_D_NATIVE_VISUAL_LOOP_ADAPTER_REQUIRED":
        raise ParityError("D9.10 Loop route identity changed")
    if adapter.get("status") != "PREPARED_NOT_DISPATCHED_RENDERER_DISABLED":
        raise ParityError("D-only adapter envelope status changed")

    if e1_result.get("status") != "PASS_E1_PREPARATION_ONLY":
        raise ParityError("E1 CLI did not return PASS_E1_PREPARATION_ONLY")
    intent = e1_result.get("intent", {})
    identity = intent.get("identity", {})
    if intent.get("request_origin") != "CLI":
        raise ParityError("E1 CLI origin is not preserved")
    if validate_editorial(intent.get("editorial"), "E1 editorial") != gui_editorial:
        raise ParityError("E1 editorial values differ from GUI")
    if identity.get("editorial_hash") != gui_editorial_hash or identity.get("editorial_hash") != d9.get("editorial_hash"):
        raise ParityError("E1/D9/GUI editorial hashes differ")
    if identity.get("request_hash") != d9.get("request_hash"):
        raise ParityError("E1/D9 request hashes differ")
    if identity.get("plan_hash") != d9.get("plan_hash"):
        raise ParityError("E1/D9 plan hashes differ")

    for field in FIELDS:
        consumption = intent.get("editorial_field_consumption", {}).get(field, {})
        if consumption.get("consumer_status") != "NOT_CONSUMED_E1" or consumption.get("required_gate") != "E4":
            raise ParityError(f"E1 field consumption state changed: {field}")
    family_adapter = intent.get("family_adapter", {})
    if family_adapter.get("adapter_id") != "c11e_visual_loops_adapter" or family_adapter.get("status") != "NOT_CONNECTED_E1":
        raise ParityError("E1 Loop family adapter boundary changed")
    music = intent.get("music_contract", {})
    if music.get("route") != "PRESERVE_EXISTING_C11C_FAMILY_MUSIC_PATH" or music.get("status") != "PROTECTED_FAMILY_NOT_REWIRED":
        raise ParityError("Protected C11-C Loop music route changed")
    if music.get("music_seed") != gui_request.get("music_seed") or music.get("engine_invoked") is not False or music.get("ffmpeg_mux_invoked") is not False:
        raise ParityError("E1 music boundary changed")
    seeds = intent.get("seed_domains", {})
    if seeds.get("independent_domains") is not True or seeds.get("cross_domain_sharing") != "FORBIDDEN":
        raise ParityError("E1 seed-domain boundary changed")
    if seeds.get("gameplay", {}).get("value") != gui_request.get("seed") or seeds.get("music", {}).get("value") != gui_request.get("music_seed"):
        raise ParityError("E1 seed values differ from GUI request")

    governance_checks = {
        "d9.renderer": d9.get("renderer") is False,
        "d9.execution": d9.get("execution") is False,
        "d9.adapter_dispatch": adapter.get("renderer_dispatch_invoked") is False,
        "d9.adapter_input": adapter.get("renderer_input_emitted") is False,
        "e1.renderer": intent.get("execution_boundary", {}).get("renderer_activation") is False,
        "e1.dispatch": intent.get("execution_boundary", {}).get("renderer_dispatch_invoked") is False,
        "e1.media": intent.get("execution_boundary", {}).get("media_created") is False,
        "e1.production": intent.get("execution_boundary", {}).get("production_execution") is False,
        "e1.d4_8": intent.get("execution_boundary", {}).get("d4_8") == "BLOCKED",
        "e1.release": intent.get("execution_boundary", {}).get("release_authority") == "NONE",
    }
    if not all(governance_checks.values()):
        failed = [key for key, passed in governance_checks.items() if not passed]
        raise ParityError("Governance assertion failed: " + ", ".join(failed))

    result = {
        "schema": "C11E-E4B-LOOP-GUI-CLI-POPULATED-PARITY-RECEIPT-V2",
        "status": "PASS_GUI_CLI_EDITORIAL_PARITY_ONLY",
        "gui": {
            "request_id": gui_request.get("request_id"),
            "request_file_sha256": sha256_file(bundle["root"] / "request.json"),
            "request_hash": gui_plan.get("request_hash"),
            "editorial_hash": gui_editorial_hash,
            "plan_hash": bundle["producer_receipt"].get("plan_hash"),
        },
        "cli": {
            "request_id": cli_request.get("request_id"),
            "request_file_sha256": sha256_file(cli_request_path),
            "request_hash": d9.get("request_hash"),
            "editorial_hash": d9.get("editorial_hash"),
            "plan_hash": d9.get("plan_hash"),
            "bridge_record_hash": bridge.get("record_hash"),
            "adapter_envelope_hash": adapter.get("envelope_hash"),
            "e1_intent_hash": intent.get("intent_sha256"),
        },
        "parity": {
            "all_four_editorial_values_equal": True,
            "all_four_values_match_versioned_unicode_fixture": True,
            "unicode_nfc_and_utf8_round_trip": True,
            "gui_cli_editorial_hash_equal": True,
            "e1_d9_editorial_hash_equal": True,
            "e1_d9_request_hash_equal": True,
            "e1_d9_plan_hash_equal": True,
            "selection_and_seed_values_equal": True,
            "request_hashes_expected_to_differ_due_request_identity_and_origin": gui_plan.get("request_hash") != d9.get("request_hash"),
        },
        "editorial": gui_editorial,
        "e1_editorial_consumption": "NOT_CONSUMED_E1; REQUIRED_GATE=E4",
        "loop_family_adapter": family_adapter,
        "family_music": {
            "route": music.get("route"),
            "status": music.get("status"),
            "music_seed": music.get("music_seed"),
            "engine_invoked": music.get("engine_invoked"),
            "ffmpeg_mux_invoked": music.get("ffmpeg_mux_invoked"),
        },
        "governance_checks": governance_checks,
        "governance": {
            "renderer": False,
            "renderer_dispatch_invoked": False,
            "production_execution": False,
            "media_created": False,
            "d4_8": "BLOCKED",
            "release_authority": "NONE",
        },
        "source_evidence": {
            "gui_evidence_root": str(bundle["root"]),
            "gui_evidence_id": gui_request.get("request_id"),
            "cli_request_id": cli_request.get("request_id"),
        },
    }
    write_json(receipt_path, result)
    return result


def run_tests() -> int:
    import unittest

    class ParityHelperTests(unittest.TestCase):
        def test_expected_fixture_is_nfc_and_not_mojibake(self):
            for key, value in EXPECTED_EDITORIAL.items():
                if key == "language":
                    continue
                assert_no_mojibake(value, key)
                self.assertEqual(unicodedata.normalize("NFC", value), value)

        def test_fixture_contains_expected_accents(self):
            self.assertIn(chr(0x00ED), EXPECTED_EDITORIAL["title"])
            self.assertIn(chr(0x2014), EXPECTED_EDITORIAL["title"])
            self.assertIn(chr(0x00F3), EXPECTED_EDITORIAL["subtitle"])
            self.assertIn(chr(0x00E9), EXPECTED_EDITORIAL["subtitle"])

        def test_mojibake_is_rejected(self):
            with self.assertRaises(ParityError):
                assert_no_mojibake("T\u00c3\u00adtulo", "bad_title")

        def test_exact_field_set_required(self):
            with self.assertRaises(ParityError):
                validate_editorial({"title": EXPECTED_EDITORIAL["title"]}, "incomplete")

        def test_fixture_field_values_are_exact(self):
            self.assertEqual(validate_editorial(dict(EXPECTED_EDITORIAL), "fixture"), EXPECTED_EDITORIAL)

    suite = unittest.defaultTestLoader.loadTestsFromTestCase(ParityHelperTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    prepare = sub.add_parser("prepare")
    prepare.add_argument("--gui-evidence-root", required=True, type=Path)
    prepare.add_argument("--output-request", required=True, type=Path)
    prepare.add_argument("--request-id", required=True)
    prepare.add_argument("--preparation-receipt", required=True, type=Path)
    verify = sub.add_parser("verify")
    verify.add_argument("--gui-evidence-root", required=True, type=Path)
    verify.add_argument("--cli-request", required=True, type=Path)
    verify.add_argument("--d9-result", required=True, type=Path)
    verify.add_argument("--e1-result", required=True, type=Path)
    verify.add_argument("--receipt-output", required=True, type=Path)
    tests = sub.add_parser("test")
    args = parser.parse_args(argv)
    try:
        if args.command == "prepare":
            result = prepare_cli_request(args.gui_evidence_root, args.output_request, args.request_id, args.preparation_receipt)
        elif args.command == "verify":
            result = verify_parity(args.gui_evidence_root, args.cli_request, args.d9_result, args.e1_result, args.receipt_output)
        else:
            return run_tests()
    except Exception as exc:
        print(f"E4B LOOP GUI/CLI PARITY ERROR: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
