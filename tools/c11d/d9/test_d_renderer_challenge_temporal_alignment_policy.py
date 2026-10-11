from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from d_renderer_challenge_temporal_alignment_policy import (
    CONTRACT_REL,
    SCHEMA_REL,
    EXPECTED_LINEAGE,
    ChallengeTemporalAlignmentError,
    build_preview,
    load_contract,
    project_boundary,
    validate_preview,
)
ROOT = Path(__file__).resolve().parents[3]

class ChallengeTemporalAlignmentPolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract, cls.schema = load_contract(ROOT)
        cls.preview = build_preview(ROOT)

    def reject_contract(self, mutate):
        tmp = copy.deepcopy(self.contract)
        mutate(tmp)
        # Unit mutation checks enforce the same static guards without modifying the pinned source files.
        from d_renderer_challenge_temporal_alignment_policy import _validate_static_facts
        with self.assertRaises(ChallengeTemporalAlignmentError):
            _validate_static_facts(tmp)

    def test_contract_schema_lineage_and_proposal_state(self):
        self.assertEqual(self.contract["schema"], "C11-D-D9-RENDERER-CHALLENGE-TEMPORAL-ALIGNMENT-POLICY-PROPOSAL-V1")
        self.assertEqual(len(self.contract["source_lineage"]), 8)
        self.assertEqual(tuple((x["path"], x["sha256"]) for x in self.contract["source_lineage"]), EXPECTED_LINEAGE)
        self.assertEqual(self.contract["policy"]["state"], "PROPOSED_NOT_APPROVED")
        try:
            from jsonschema import Draft202012Validator
        except ImportError:
            return
        Draft202012Validator.check_schema(self.schema)
        Draft202012Validator(self.schema).validate(self.contract)

    def test_source_to_delivery_boundaries_are_exact(self):
        self.assertEqual([project_boundary(x) for x in [0, 180, 600, 780, 900]], [0, 90, 300, 390, 450])
        self.assertEqual(self.preview["summary_facts"]["phase_boundaries_exact"], True)
        self.assertEqual([p["boundary_exact"] for p in self.preview["phase_alignment"]], [True] * 4)

    def test_phase_ranges_are_half_open_contiguous_and_complete(self):
        phases = self.contract["phase_alignment"]
        self.assertEqual([p["phase"] for p in phases], ["HOOK", "GAME", "REVEAL", "CTA"])
        self.assertEqual(phases[0]["source_range"][0], 0)
        self.assertEqual(phases[-1]["source_range"][1], 900)
        self.assertEqual(phases[0]["delivery_range"][0], 0)
        self.assertEqual(phases[-1]["delivery_range"][1], 450)
        for left, right in zip(phases, phases[1:]):
            self.assertEqual(left["source_range"][1], right["source_range"][0])
            self.assertEqual(left["delivery_range"][1], right["delivery_range"][0])
        self.assertEqual([p["source_frames"] for p in phases], [180, 420, 180, 120])
        self.assertEqual([p["delivery_frames"] for p in phases], [90, 210, 90, 60])

    def test_duration_is_preserved(self):
        f = self.contract["fixture"]
        self.assertEqual(f["source_total_frames"] / f["source_fps"], 15)
        self.assertEqual(f["delivery_boundaries"][-1] / f["delivery_fps"], 15)
        self.assertTrue(self.preview["summary_facts"]["duration_preserved"])

    def test_winning_anchor_maps_without_becoming_selection_input(self):
        a = self.contract["winning_anchor_reference"]
        self.assertEqual(a["source_absolute_frame_index"], 574)
        self.assertEqual(a["source_game_local_index"], 394)
        self.assertEqual(a["delivery_game_local_index"], 197)
        self.assertEqual(a["delivery_absolute_frame_index"], 287)
        self.assertTrue(a["selected_by_even_local_index_cadence"])
        self.assertFalse(a["winning_frame_mutated"])
        self.assertFalse(a["close_calls_used_for_timing"])

    def test_editorial_ranges_match_explicit_proposal_and_empty_reveal_suppressed(self):
        w = self.contract["editorial_windows_reference"]
        self.assertEqual(w["expected_field_ranges"], {"hook": [0, 90], "reveal": None, "cta": [390, 450]})
        self.assertTrue(w["phase_ranges_are_not_implicitly_text_visibility"])
        self.assertEqual(w["state"], "PROPOSED_NOT_APPROVED")

    def test_contract_does_not_emit_delivery_candidate_or_renderer_input(self):
        b = self.contract["execution_boundary"]
        for key in ("c11c_source_mutation", "payload_files_written", "persistent_report_written", "renderer_native_input_emitted", "renderer_dispatch_invoked", "renderer_activation", "production_execution", "media_created", "video_render_ready"):
            self.assertFalse(b[key], key)
        self.assertEqual(b["d4_8"], "BLOCKED")
        self.assertEqual(b["release_authority"], "NONE")
        self.assertFalse(self.preview["summary_facts"]["delivery_candidate_materialized"])

    def test_half_up_boundary_arithmetic_supported_case(self):
        self.assertEqual(project_boundary(1, 60, 30), 1)
        self.assertEqual(project_boundary(3, 60, 30), 2)
        self.assertEqual(project_boundary(180, 60, 30), 90)

    def test_rejects_unsupported_timebase(self):
        with self.assertRaises(ChallengeTemporalAlignmentError):
            project_boundary(180, 60, 24)

    def test_rejects_invalid_boundary_and_fps_values(self):
        for args in [(-1, 60, 30), (1, 0, 30), (1, 60, 0), (True, 60, 30), (1, True, 30), (1, 60, False)]:
            with self.subTest(args=args), self.assertRaises(ChallengeTemporalAlignmentError):
                project_boundary(*args)

    def test_negative_phase_boundary_change(self):
        self.reject_contract(lambda x: x["fixture"].update(source_boundaries=[0,180,599,780,900]))

    def test_negative_delivery_phase_count_change(self):
        self.reject_contract(lambda x: x["fixture"].update(delivery_phase_frame_counts=[90,211,89,60]))

    def test_negative_phase_gap(self):
        self.reject_contract(lambda x: x["phase_alignment"][1].update(source_range=[181,600]))

    def test_negative_phase_overlap(self):
        self.reject_contract(lambda x: x["phase_alignment"][2].update(delivery_range=[299,390]))

    def test_negative_phase_frame_count_mismatch(self):
        self.reject_contract(lambda x: x["phase_alignment"][1].update(delivery_frames=211))

    def test_negative_duration_drift(self):
        self.reject_contract(lambda x: x["fixture"].update(delivery_boundaries=[0,90,300,390,451]))

    def test_negative_winning_anchor_shift(self):
        self.reject_contract(lambda x: x["winning_anchor_reference"].update(delivery_absolute_frame_index=288))

    def test_negative_winning_anchor_forced_into_selection(self):
        self.reject_contract(lambda x: x["winning_anchor_reference"].update(selected_by_even_local_index_cadence=False))

    def test_negative_close_calls_as_timing(self):
        self.reject_contract(lambda x: x["winning_anchor_reference"].update(close_calls_used_for_timing=True))

    def test_negative_phase_name_inferred_as_text_window(self):
        self.reject_contract(lambda x: x["editorial_windows_reference"].update(phase_ranges_are_not_implicitly_text_visibility=False))

    def test_negative_editorial_policy_approved(self):
        self.reject_contract(lambda x: x["editorial_windows_reference"].update(state="APPROVED"))

    def test_negative_sampling_policy_approved(self):
        self.reject_contract(lambda x: x["sample_selection_reference"].update(state="APPROVED"))

    def test_negative_temporal_policy_approved(self):
        self.reject_contract(lambda x: x["policy"].update(state="APPROVED"))

    def test_negative_contract_status_promoted(self):
        self.reject_contract(lambda x: x.update(status="RENDERER_INPUT_READY"))

    def test_negative_boundary_formula_changed(self):
        self.reject_contract(lambda x: x["policy"]["boundary_projection"].update(formula="round(source_boundary / 2)"))

    def test_negative_sampling_counts_changed(self):
        self.reject_contract(lambda x: x["sample_selection_reference"].update(delivery_game_snapshots=211))

    def test_negative_acceptance_gate_promoted(self):
        self.reject_contract(lambda x: x["approval_state"].update(d9_16_full_acceptance="PASS_CLOSED"))

    def test_negative_renderer_activation(self):
        self.reject_contract(lambda x: x["execution_boundary"].update(renderer_activation=True))

    def test_negative_d4_8_authorized(self):
        self.reject_contract(lambda x: x["execution_boundary"].update(d4_8="AUTHORIZED"))

    def test_negative_release_authority_granted(self):
        self.reject_contract(lambda x: x["execution_boundary"].update(release_authority="GRANTED"))

    def test_negative_lineage_digest_mismatch(self):
        self.reject_contract(lambda x: x["source_lineage"][0].update(sha256="0" * 64))

    def test_preview_is_deterministic_and_not_persisted(self):
        self.assertEqual(build_preview(ROOT), build_preview(ROOT))
        self.assertEqual(self.preview["status"], "REVIEW_ONLY_PROPOSAL_NOT_RENDERER_INPUT")
        self.assertEqual(self.preview["source_timeline"]["boundaries"], [0,180,600,780,900])
        self.assertEqual(self.preview["delivery_timeline"]["boundaries"], [0,90,300,390,450])

    def test_preview_validator_accepts_canonical_preview(self):
        validate_preview(self.preview, ROOT)

    def test_preview_validator_rejects_mutated_boundary(self):
        changed = copy.deepcopy(self.preview)
        changed["delivery_timeline"]["boundaries"][-1] = 451
        with self.assertRaises(ChallengeTemporalAlignmentError):
            validate_preview(changed, ROOT)

if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(ChallengeTemporalAlignmentPolicyTests)
    result = unittest.TextTestRunner(verbosity=2, stream=sys.stdout).run(suite)
    if not result.wasSuccessful():
        raise SystemExit(1)
    print(
        "C11-D RENDERER CHALLENGE TEMPORAL ALIGNMENT POLICY PROPOSAL PASS"
        " | source=900@60FPS | delivery=450@30FPS | phase_boundaries=5/5_EXACT"
        " | segments=4/4 | winning_frame=574_TO_287 | editorial_windows=EXPLICIT_PROPOSAL_ONLY"
        " | interpolation=NONE | policy=PROPOSED_NOT_APPROVED | renderer=OFF"
        " | media_created=false | D4.8=BLOCKED | release_authority=NONE",
        flush=True,
    )
