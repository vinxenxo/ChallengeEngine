from __future__ import annotations

import json
import math
import unittest
from pathlib import Path
from typing import Any

import d_renderer_challenge_coordinate_projection as contract

ROOT = contract.project_root()


def make_report() -> dict[str, Any]:
    facts = contract.projection_facts()
    target = contract.project_point([850.0, 960.0], facts)
    assets = []
    for role, size in contract.EXPECTED_SIZES.items():
        assets.append({
            "role": role,
            "resource_path": "res://assets/c6/" + {"BACKGROUND": "garage_background.svg", "ANIMATED_OBJECT": "car.svg", "TARGET": "parking_target.svg"}[role],
            "sha256": {"BACKGROUND": contract.EXPECTED_SOURCE_PINS["assets/c6/garage_background.svg"], "ANIMATED_OBJECT": contract.EXPECTED_SOURCE_PINS["assets/c6/car.svg"], "TARGET": contract.EXPECTED_SOURCE_PINS["assets/c6/parking_target.svg"]}[role],
            "intrinsic_size": list(size),
            "projected_delivery_base_size": contract.projected_asset_size(size, facts),
            "declared_scale_preserved_separately": 1.0 if role == "BACKGROUND" else 0.85,
            "declared_offset_source": [0.0, 0.0],
            "declared_offset_delivery": [0.0, 0.0],
            "loaded_as_texture2d": True,
        })
    return {
        "schema": contract.REPORT_ID,
        "schema_version": "1.0",
        "status": "IN_MEMORY_REVIEW_ONLY_PROJECTION_PREVIEW_NOT_RENDERER_INPUT",
        "frozen_c11c_manifest_sha256": contract.FROZEN_MANIFEST_SHA256,
        "challenge_source_sha256": contract.EXPECTED_SOURCE_PINS["challenges/CHALLENGE_004.json"],
        "projection": {
            "policy_id": "C11D_CHALLENGE_COORDINATE_PROJECTION_1080_TO_540_TO_REVIEW720_V1",
            "state": "PROPOSED_NOT_APPROVED",
            "source_coordinate_space": "CANVAS_1080X1920",
            "source_size": {"width": 1080, "height": 1920},
            "presentation_source_canvas": {"width": 540, "height": 960},
            "presentation_master_output": {"width": 1080, "height": 1920},
            "delivery_size": {"width": 720, "height": 1280},
            "stage_scales": [facts["source_to_presentation_scale"], facts["presentation_to_delivery_scale"]],
            "combined_scale": facts["combined_scale"],
            "target_position": target,
            "transform_semantics": "POSITIONS_AND_INTRINSIC_BASE_DIMENSIONS_PROJECTED; LOCAL_SIMULATION_SCALE_ROTATION_OPACITY_TEXTURE_INDEX_VARIANT_ID_PRESERVED",
            "sampling_or_interpolation": "UNRESOLVED_NOT_APPLIED",
        },
        "source_timeline": {"fps": 60, "total_frames": 900, "duration_seconds": 15.0, "game_frame_count": 420},
        "delivery_profile": {"profile_id": "REVIEW_720", "fps": 30, "width": 720, "height": 1280, "total_frames": 450, "duration_seconds": 15.0},
        "projected_frames": {
            "source_records": 420,
            "projected_records": 420,
            "source_records_sha256": "a" * 64,
            "projected_records_sha256": "b" * 64,
            "order_preserved": True,
            "local_scale_preserved": True,
            "other_snapshot_fields_preserved": True,
        },
        "assets": assets,
        "determinism": {"runtime_repeat_equal": True, "projection_repeat_equal": True, "source_frame_signature_repeat_equal": True},
        "simulation_invariance": {"frame_signature_unchanged": True, "winning_frame_unchanged": True, "metrics_unchanged": True, "frame_count_unchanged": True},
        "execution_boundary": {"mode": "GODOT_HEADLESS_IN_MEMORY_REVIEW_ONLY", "source_mutation": False, "projected_payload_written": False, "renderer_native_input_emitted": False, "renderer_dispatch_invoked": False, "renderer_activation": False, "media_created": False, "d4_8": "BLOCKED", "release_authority": "NONE"},
        "source_lineage": [{"path": p, "sha256": s} for p, s in contract.EXPECTED_SOURCE_PINS.items()] + [{"path": "release/C11C_FREEZE_PACKAGE_MANIFEST.json", "sha256": contract.FROZEN_MANIFEST_SHA256}],
    }


class CoordinateProjectionTests(unittest.TestCase):
    def test_contract_identity_and_unapproved_state(self) -> None:
        summary = contract.validate_contract_and_sources(ROOT)
        self.assertEqual(summary["source_hash_pins"], len(contract.EXPECTED_SOURCE_PINS))
        raw = contract.read_json(ROOT / contract.CONTRACT_REL)
        self.assertEqual(raw["status"], "PROPOSED_NOT_APPROVED_NOT_FROZEN")
        self.assertFalse(raw["projection"]["state"] == "APPROVED")

    def test_source_pin_registry(self) -> None:
        raw = contract.read_json(ROOT / contract.CONTRACT_REL)
        self.assertEqual(raw["source_pins"], [{"path": p, "sha256": h} for p, h in contract.EXPECTED_SOURCE_PINS.items()])

    def test_mapper_scale_half(self) -> None:
        facts = contract.projection_facts()
        self.assertEqual(facts["source_to_presentation_scale"], [0.5, 0.5])

    def test_delivery_scale_four_thirds(self) -> None:
        facts = contract.projection_facts()
        self.assertTrue(all(contract.nearly_equal(v, 4 / 3) for v in facts["presentation_to_delivery_scale"]))

    def test_composed_scale_two_thirds(self) -> None:
        facts = contract.projection_facts()
        self.assertTrue(all(contract.nearly_equal(v, 2 / 3) for v in facts["combined_scale"]))

    def test_corner_mapping_preserves_canvas(self) -> None:
        facts = contract.projection_facts()
        self.assertEqual(contract.project_point([0, 0], facts)["delivery"], [0.0, 0.0])
        self.assertTrue(all(contract.nearly_equal(a, b) for a, b in zip(contract.project_point([1080, 1920], facts)["delivery"], [720, 1280])))

    def test_target_position_mapping(self) -> None:
        facts = contract.projection_facts()
        target = contract.project_point([850, 960], facts)
        self.assertEqual(target["presentation_canvas"], [425.0, 480.0])
        self.assertTrue(contract.nearly_equal(target["delivery"][0], 566.6666666667))
        self.assertTrue(contract.nearly_equal(target["delivery"][1], 640.0))

    def test_aspect_ratio_is_preserved(self) -> None:
        facts = contract.projection_facts()
        self.assertTrue(contract.nearly_equal(1080 / 1920, 540 / 960))
        self.assertTrue(contract.nearly_equal(540 / 960, 720 / 1280))
        self.assertTrue(contract.nearly_equal(facts["combined_scale"][0], facts["combined_scale"][1]))

    def test_intrinsic_sizes_are_projected_separately(self) -> None:
        facts = contract.projection_facts()
        self.assertEqual(contract.projected_asset_size((1080, 1920), facts), [720.0, 1280.0])
        car = contract.projected_asset_size((160, 320), facts)
        self.assertTrue(contract.nearly_equal(car[0], 106.6666666667))
        self.assertTrue(contract.nearly_equal(car[1], 213.3333333333))

    def test_nonuniform_source_transform_rejected(self) -> None:
        with self.assertRaises(contract.CoordinateProjectionError):
            contract.projection_facts(source_size=(1080, 1900), presentation_size=(540, 960))

    def test_nonuniform_delivery_transform_rejected(self) -> None:
        with self.assertRaises(contract.CoordinateProjectionError):
            contract.projection_facts(delivery_size=(720, 1200))

    def test_nonfinite_positions_rejected(self) -> None:
        with self.assertRaises(contract.CoordinateProjectionError):
            contract.project_point([math.nan, 10], contract.projection_facts())

    def test_empty_invalid_dimensions_rejected(self) -> None:
        with self.assertRaises(contract.CoordinateProjectionError):
            contract.projection_facts(source_size=(0, 1920))
        with self.assertRaises(contract.CoordinateProjectionError):
            contract.projected_asset_size((0, 320), contract.projection_facts())

    def test_report_schema_valid(self) -> None:
        report = make_report()
        self.assertTrue(contract.validate_report_shape(report, ROOT))

    def test_report_rejects_changed_source_frame_count(self) -> None:
        report = make_report()
        report["projected_frames"]["projected_records"] = 419
        with self.assertRaises(contract.CoordinateProjectionError):
            contract.validate_report_shape(report, ROOT)

    def test_report_rejects_approved_self_transition(self) -> None:
        report = make_report()
        report["projection"]["state"] = "APPROVED"
        with self.assertRaises(contract.CoordinateProjectionError):
            contract.validate_report_shape(report, ROOT)

    def test_report_rejects_renderer_activation(self) -> None:
        report = make_report()
        report["execution_boundary"]["renderer_activation"] = True
        with self.assertRaises(contract.CoordinateProjectionError):
            contract.validate_report_shape(report, ROOT)

    def test_godot_single_precision_delivery_position_tolerance(self) -> None:
        source = (ROOT / "tools/c11d/d9/review_challenge_coordinate_projection_in_memory.gd").read_text(encoding="utf-8")
        self.assertIn("_near(target_delivery.x, 850.0 * 2.0 / 3.0, 0.0001)", source)
        self.assertIn("Canonical target position projected incorrectly: source=", source)

    def test_harness_static_boundary(self) -> None:
        source = (ROOT / "tools/c11d/d9/review_challenge_coordinate_projection_in_memory.gd").read_text(encoding="utf-8")
        self.assertIn("CoordinateMapper.map_position", source)
        self.assertIn("PROPOSED_NOT_APPROVED", source)
        self.assertIn("renderer_native_input_emitted\": false", source)
        self.assertNotIn("RenderingServer.", source)
        self.assertNotIn("SubViewport", source)
        self.assertNotIn("Image.save_png", source)
        self.assertNotIn("FileAccess.WRITE", source)
        self.assertNotIn("FileAccess.open(", source)


if __name__ == "__main__":
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(CoordinateProjectionTests))
    if not result.wasSuccessful():
        raise SystemExit(1)
    try:
        summary = contract.static_contract_summary(ROOT)
    except Exception as exc:
        raise SystemExit(f"C11-D coordinate projection contract FAIL | {exc}") from exc
    print(
        "C11-D RENDERER CHALLENGE COORDINATE PROJECTION CONTRACT PASS "
        f"| source_hash_pins={summary['source_hash_pins']}/{len(contract.EXPECTED_SOURCE_PINS)} "
        "| transform_stages=2/2 | target_position=PASS | assets=3/3 "
        "| unit_tests=19/19 | schema=1/1 | jsonschema=1/1 "
        "| godot_harness=NOT_RUN_BY_PYTHON | policy=PROPOSED_NOT_APPROVED "
        "| renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE"
    )
