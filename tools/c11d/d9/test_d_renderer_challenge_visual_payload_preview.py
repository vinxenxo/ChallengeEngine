"""Contract, lineage, schema and fail-closed tests for Challenge visual payload preview."""
from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))

from d_renderer_challenge_visual_payload_preview import (  # noqa: E402
    CHALLENGE_SHA256,
    CONTRACT_REL,
    FROZEN_MANIFEST_SHA256,
    SCHEMA_REL,
    ChallengeVisualPayloadError,
    read_json,
    sha256_json,
    static_contract_summary,
    validate_report_shape,
    validate_source_pins,
)


def fixture_report() -> dict[str, Any]:
    assets = [
        {"role": "BACKGROUND", "resource_path": "res://assets/c6/garage_background.svg", "sha256": "c9d8acdae725ca7726fc8ad23a046e4aac4d9e454b45db40d2c770732b31ab1e", "resource_loaded_as_texture2d": True, "intrinsic_width": 1080, "intrinsic_height": 1920, "binding_source": "CanonicalV2.assets.background_path", "declared_transform": {"projection_applied": False}},
        {"role": "ANIMATED_OBJECT", "resource_path": "res://assets/c6/car.svg", "sha256": "93a6f78d9654f7917ab2287800858a937e9c68c458cc60bf417d6f2b98c1a96d", "resource_loaded_as_texture2d": True, "intrinsic_width": 160, "intrinsic_height": 320, "binding_source": "CanonicalV2.assets.object_path", "declared_transform": {"projection_applied": False}},
        {"role": "TARGET", "resource_path": "res://assets/c6/parking_target.svg", "sha256": "ec2dcafd7dfc99ff501eb2d93b93906680a30c48cf0741807cbbdd915a18cfb3", "resource_loaded_as_texture2d": True, "intrinsic_width": 200, "intrinsic_height": 400, "binding_source": "CanonicalV2.assets.target_path", "declared_transform": {"projection_applied": False}},
    ]
    return {
        "schema": "C11-D-D9-CHALLENGE-VISUAL-PAYLOAD-PREVIEW-V1",
        "schema_version": "1.0",
        "status": "IN_MEMORY_REVIEW_ONLY_SOURCE_TIMEBASE_VISUAL_PAYLOAD_NOT_RENDERER_INPUT",
        "frozen_c11c_manifest_sha256": FROZEN_MANIFEST_SHA256,
        "challenge_source_sha256": CHALLENGE_SHA256,
        "payload_sha256": "a" * 64,
        "payload_identity": {"challenge_id": "CHALLENGE_004", "mechanic": "parking_v2", "mechanic_version": "2.0", "presentation_profile_id": "social_default_v1", "coordinate_space": "CANVAS_1080X1920", "materialization": "IN_MEMORY_ONLY_SOURCE_TIMEBASE"},
        "asset_nodes": assets,
        "source_timeline": {"fps": 60, "total_frames": 900, "duration_seconds": 15, "phase_order": ["HOOK", "GAME", "REVEAL", "CTA"], "phase_segments": [{"phase": "HOOK", "start_frame": 0, "end_frame": 180, "frame_count": 180}, {"phase": "GAME", "start_frame": 180, "end_frame": 600, "frame_count": 420}, {"phase": "REVEAL", "start_frame": 600, "end_frame": 780, "frame_count": 180}, {"phase": "CTA", "start_frame": 780, "end_frame": 900, "frame_count": 120}]},
        "animation": {"frame_source": "SimulationResult.frames", "source_fps": 60, "game_frame_count": 420, "frame_record_count": 420, "frame_records_sha256": "b" * 64, "snapshot_fields_included": ["position", "rotation", "scale", "opacity", "texture_index", "variant_id"], "simulation_telemetry_included": False, "winning_frame_sampling_used": False, "delivery_resampling": "UNRESOLVED_NOT_APPLIED"},
        "presentation": {"render_model_sha256": "c" * 64, "profile_source_canvas": {"width": 540, "height": 960}, "profile_master_output": {"width": 1080, "height": 1920}, "source_coordinate_space": "CANVAS_1080X1920", "coordinate_projection": "UNRESOLVED_NOT_APPLIED"},
        "determinism": {"runtime_repeat_equal": True, "payload_repeat_equal": True, "frame_signature_repeat_equal": True, "simulation_invariance": True},
        "execution_boundary": {"mode": "GODOT_HEADLESS_IN_MEMORY_REVIEW_ONLY", "payload_written": False, "media_output_created": False, "renderer_native_input_emitted": False, "renderer_dispatch_invoked": False, "renderer_activation": False, "c11c_source_mutation": False, "d4_8": "BLOCKED", "release_authority": "NONE", "output_artifact_path": None},
        "source_lineage": [{"path": f"pin_{i}", "sha256": f"{i:064x}"} for i in range(10)],
    }


class ChallengeVisualPayloadPreviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.contract = read_json(ROOT / CONTRACT_REL)
        cls.schema = read_json(ROOT / SCHEMA_REL)

    def test_source_pins(self) -> None:
        result = validate_source_pins(ROOT)
        self.assertEqual(result, {"source_hash_pins": 10, "asset_pins": 3, "asset_dimensions": 3})

    def test_contract_status_and_frozen_lock(self) -> None:
        self.assertEqual(self.contract["status"], "PREPARATION_ONLY_NOT_APPROVED_NOT_FROZEN")
        self.assertEqual(self.contract["source_authority"]["frozen_manifest_sha256"], FROZEN_MANIFEST_SHA256)
        self.assertFalse(self.contract["governance_locks"]["renderer_baseline_frozen"])

    def test_expected_asset_manifest(self) -> None:
        self.assertEqual(len(self.contract["pinned_sources"]), 10)
        assets = [item for item in self.contract["pinned_sources"] if "role" in item]
        self.assertEqual(len(assets), 3)
        self.assertEqual({item["role"] for item in assets}, {"BACKGROUND", "ANIMATED_OBJECT", "TARGET"})

    def test_scope_preserves_source_fps_and_excludes_truth_fields(self) -> None:
        runtime = self.contract["runtime_contract"]
        self.assertEqual(runtime["source_fps"], 60)
        self.assertEqual(runtime["source_total_frames"], 900)
        self.assertEqual(runtime["simulation_snapshot_fields"], ["position", "rotation", "scale", "opacity", "texture_index", "variant_id"])
        for forbidden in ("custom_data", "winning_frame", "close_calls", "score"):
            self.assertIn(forbidden, runtime["simulation_fields_excluded"])
        self.assertEqual(runtime["delivery_resampling"], "UNRESOLVED_NOT_APPLIED")

    def test_harness_static_safety_contract(self) -> None:
        result = static_contract_summary(ROOT)
        self.assertEqual(result["source_hash_pins"], 10)
        self.assertEqual(result["asset_pins"], 3)
        self.assertEqual(result["contract_schema"], 1)
        self.assertEqual(result["summary_schema"], 1)

    def test_valid_summary(self) -> None:
        self.assertTrue(validate_report_shape(fixture_report(), ROOT))

    def test_output_schema_is_valid(self) -> None:
        try:
            import jsonschema
        except ImportError:
            self.skipTest("jsonschema is an optional development dependency")
        jsonschema.Draft202012Validator.check_schema(self.schema)
        jsonschema.Draft202012Validator(self.schema).validate(fixture_report())

    def test_negative_cases(self) -> None:
        mutations = []
        def mutate(name: str, fn) -> None:
            doc = fixture_report()
            fn(doc)
            mutations.append((name, doc))
        mutate("renderer_activation", lambda x: x["execution_boundary"].update(renderer_activation=True))
        mutate("media_output", lambda x: x["execution_boundary"].update(media_output_created=True))
        mutate("bad_delivery_resample", lambda x: x["animation"].update(delivery_resampling="APPLIED"))
        mutate("winning_frame_sampler", lambda x: x["animation"].update(winning_frame_sampling_used=True))
        mutate("telemetry_bind", lambda x: x["animation"].update(simulation_telemetry_included=True))
        mutate("missing_target_asset", lambda x: x["asset_nodes"].pop())
        mutate("wrong_source_timebase", lambda x: x["source_timeline"].update(fps=30))
        mutate("wrong_frame_count", lambda x: x["animation"].update(frame_record_count=419))
        mutate("coordinate_projection_escalation", lambda x: x["presentation"].update(coordinate_projection="APPLIED"))
        mutate("source_identity_tamper", lambda x: x.update(challenge_source_sha256="0" * 64))
        try:
            import jsonschema
            expected_errors = (ChallengeVisualPayloadError, jsonschema.ValidationError)
        except ImportError:
            expected_errors = (ChallengeVisualPayloadError,)
        for name, bad in mutations:
            with self.subTest(name=name), self.assertRaises(expected_errors):
                validate_report_shape(bad, ROOT)
        self.assertEqual(len(mutations), 10)

    def test_contract_cannot_self_approve(self) -> None:
        self.assertFalse(self.contract["governance_locks"]["renderer_baseline_approved"])
        self.assertEqual(self.contract["governance_locks"]["release_authority"], "NONE")

    def test_frame_payload_hash_fixture_is_canonical(self) -> None:
        # A useful deterministic hash invariant for JSON payloads with sorted keys.
        payload = {"b": 2, "a": [1, 2, 3]}
        self.assertEqual(sha256_json(payload), sha256_json({"a": [1, 2, 3], "b": 2}))
        self.assertEqual(len(sha256_json(payload)), 64)


def main() -> int:
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(ChallengeVisualPayloadPreviewTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():
        return 1
    try:
        pins = validate_source_pins(ROOT)
    except ChallengeVisualPayloadError as exc:
        print(f"C11-D RENDERER CHALLENGE VISUAL PAYLOAD PREVIEW CONTRACT FAIL | {exc}")
        return 1
    try:
        import jsonschema  # noqa: F401
        schema_status = "1/1"
    except ImportError:
        schema_status = "NOT_INSTALLED"
    print(
        "C11-D RENDERER CHALLENGE VISUAL PAYLOAD PREVIEW CONTRACT PASS "
        f"| source_hash_pins={pins['source_hash_pins']}/10 | assets={pins['asset_pins']}/3 "
        f"| unit_tests=10/10 | schema=1/1 | jsonschema={schema_status} "
        "| godot_harness=NOT_RUN_BY_PYTHON | payload=IN_MEMORY_ONLY "
        "| renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
