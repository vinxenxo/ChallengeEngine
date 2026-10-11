from __future__ import annotations
import json
import math
import tempfile
import unittest
from pathlib import Path

from d_renderer_challenge_coordinate_sample_composition import (
    CompositionContractError, compose_projected_records, project_point,
    selected_source_indices, validate_contract,
)

ROOT = Path(__file__).resolve().parents[3]


class CoordinateSampleCompositionProposalTests(unittest.TestCase):
    def test_contract_lineage_schema_and_policy_state(self):
        result = validate_contract(ROOT)
        self.assertEqual(len(result["selected_indexes"]), 210)
        self.assertEqual(result["selected_indexes"][:3], [0, 2, 4])
        self.assertEqual(result["selected_indexes"][-1], 418)
        self.assertEqual(result["contract"]["status"], "PROPOSED_NOT_APPROVED_NOT_FROZEN")

    def test_uniform_1080_to_720_coordinate_mapping(self):
        self.assertEqual(project_point((0, 0)), (0.0, 0.0))
        self.assertEqual(project_point((1080, 0)), (720.0, 0.0))
        self.assertEqual(project_point((0, 1920)), (0.0, 1280.0))
        self.assertEqual(project_point((1080, 1920)), (720.0, 1280.0))
        x, y = project_point((850, 960))
        self.assertAlmostEqual(x, 566.6666666667, delta=1e-4)
        self.assertAlmostEqual(y, 640.0, delta=1e-4)

    def test_even_local_indices_are_exact_2_to_1_cadence(self):
        indexes = selected_source_indices(420, stride=2)
        self.assertEqual(len(indexes), 210)
        self.assertEqual(indexes, list(range(0, 420, 2)))

    def test_winning_frame_is_selected_and_maps_to_delivery_anchor(self):
        indexes = selected_source_indices(420, stride=2)
        winning_local = 394
        delivery_local = indexes.index(winning_local)
        self.assertEqual(delivery_local, 197)
        self.assertEqual(180 + winning_local, 574)
        self.assertEqual(90 + delivery_local, 287)

    def test_project_then_select_equals_select_then_project(self):
        source = [(float(i), float(2 * i + 1)) for i in range(420)]
        composed = compose_projected_records(source, stride=2)
        selected_then_projected = [project_point(source[i]) for i in selected_source_indices(420, stride=2)]
        self.assertEqual(len(composed), 210)
        self.assertEqual(composed, selected_then_projected)

    def test_projection_is_non_temporal_and_does_not_consume_close_calls(self):
        result = validate_contract(ROOT)
        case = result["contract"]["case"]
        self.assertEqual(case["close_calls"], 1)
        self.assertFalse(result["contract"]["composition"]["selection_uses_close_calls_as_timing"])
        self.assertFalse(result["contract"]["composition"]["selection_uses_winning_frame_as_input"])

    def test_proposal_cannot_claim_policy_or_renderer_approval(self):
        result = validate_contract(ROOT)
        locks = result["contract"]["governance_locks"]
        self.assertFalse(locks["policy_approved"])
        self.assertFalse(locks["sample_selection_policy_approved"])
        self.assertFalse(locks["coordinate_projection_policy_approved"])
        self.assertFalse(locks["renderer_input_emitted"])
        self.assertFalse(locks["renderer_activation"])
        self.assertFalse(locks["media_created"])
        self.assertEqual(locks["d4_8"], "BLOCKED")
        self.assertEqual(locks["release_authority"], "NONE")

    def test_negative_nonpositive_snapshot_count(self):
        with self.assertRaises(CompositionContractError):
            selected_source_indices(0, stride=2)

    def test_negative_zero_stride(self):
        with self.assertRaises(CompositionContractError):
            selected_source_indices(420, stride=0)

    def test_negative_origin_outside_source(self):
        with self.assertRaises(CompositionContractError):
            selected_source_indices(420, stride=2, origin=420)

    def test_negative_nonfinite_coordinates(self):
        with self.assertRaises(CompositionContractError):
            project_point((math.inf, 0))

    def test_negative_non_two_dimensional_coordinate(self):
        with self.assertRaises(CompositionContractError):
            project_point((1, 2, 3))

    def test_negative_rejects_mutated_contract_hash_pin(self):
        original = (ROOT / "definitions/c11d/production/D_RENDERER_CHALLENGE_COORDINATE_SAMPLE_COMPOSITION_PROPOSAL_V1.json").read_text(encoding="utf-8")
        mutated = json.loads(original)
        mutated["authority"]["coordinate_projection_contract_sha256"] = "0" * 64
        with tempfile.TemporaryDirectory() as tmp:
            import shutil
            tmp_root = Path(tmp)
            shutil.copytree(ROOT / "definitions", tmp_root / "definitions")
            shutil.copytree(ROOT / "release", tmp_root / "release")
            # keep the contract and schema independent from the live checkout
            contract_path = tmp_root / "definitions/c11d/production/D_RENDERER_CHALLENGE_COORDINATE_SAMPLE_COMPOSITION_PROPOSAL_V1.json"
            contract_path.write_text(json.dumps(mutated), encoding="utf-8")
            with self.assertRaises(CompositionContractError):
                validate_contract(tmp_root)

    def _mutated_root(self, mutation):
        import shutil
        self._tmp = tempfile.TemporaryDirectory()
        root = Path(self._tmp.name)
        shutil.copytree(ROOT / "definitions", root / "definitions")
        shutil.copytree(ROOT / "release", root / "release")
        contract_path = root / "definitions/c11d/production/D_RENDERER_CHALLENGE_COORDINATE_SAMPLE_COMPOSITION_PROPOSAL_V1.json"
        data = json.loads(contract_path.read_text(encoding="utf-8"))
        mutation(data)
        contract_path.write_text(json.dumps(data), encoding="utf-8")
        return root

    def test_negative_policy_state_cannot_be_promoted(self):
        root = self._mutated_root(lambda data: data.update(status="APPROVED"))
        with self.assertRaises(CompositionContractError):
            validate_contract(root)
        self._tmp.cleanup()

    def test_negative_delivery_record_count_mismatch(self):
        def mutation(data):
            data["composition"]["composed_delivery_record_count"] = 209
        root = self._mutated_root(mutation)
        with self.assertRaises(CompositionContractError):
            validate_contract(root)
        self._tmp.cleanup()

    def test_negative_spatial_offset_is_not_zero(self):
        def mutation(data):
            data["spatial_projection"]["combined_offset"] = [1.0, 0.0]
        root = self._mutated_root(mutation)
        with self.assertRaises(CompositionContractError):
            validate_contract(root)
        self._tmp.cleanup()

    def test_negative_source_lineage_digest_mismatch(self):
        def mutation(data):
            data["source_lineage"][1]["sha256"] = "0" * 64
        root = self._mutated_root(mutation)
        with self.assertRaises(CompositionContractError):
            validate_contract(root)
        self._tmp.cleanup()

    def test_negative_policy_approval_lock_cannot_be_enabled(self):
        def mutation(data):
            data["governance_locks"]["policy_approved"] = True
        root = self._mutated_root(mutation)
        with self.assertRaises(CompositionContractError):
            validate_contract(root)
        self._tmp.cleanup()


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(CoordinateSampleCompositionProposalTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    print("C11-D RENDERER CHALLENGE COORDINATE+SAMPLE COMPOSITION PROPOSAL " + ("PASS" if result.wasSuccessful() else "FAIL") + " | source=420@60FPS | delivery=210@30FPS | scale=2/3 | winning_frame=574_TO_287 | policy=PROPOSED_NOT_APPROVED | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE")
    raise SystemExit(not result.wasSuccessful())
