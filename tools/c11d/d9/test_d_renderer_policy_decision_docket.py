import unittest
from d_renderer_policy_decision_docket import (
    EXPECTED_DECISIONS,
    EXPECTED_LOCKS,
    FIXED_PINS,
    load_packet,
    validate_packet,
    verify_source_pins,
)

class PolicyDecisionDocketTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.packet = load_packet()
        cls.validation_errors = validate_packet(cls.packet)
        cls.source_errors = verify_source_pins(cls.packet)

    def test_packet_contract_passes(self):
        self.assertEqual([], self.validation_errors)

    def test_all_source_pins_match_checkout(self):
        self.assertEqual([], self.source_errors)

    def test_source_inventory_has_unique_paths(self):
        pins = self.packet["source_pins"]
        paths = [item["path"] for item in pins]
        self.assertEqual(len(paths), len(set(paths)))
        self.assertEqual(len(pins), self.packet["source_pin_count"])
        self.assertGreater(len(pins), 100)

    def test_all_operator_decisions_are_pending(self):
        self.assertEqual(
            EXPECTED_DECISIONS,
            {item["id"] for item in self.packet["decisions"]},
        )
        for item in self.packet["decisions"]:
            self.assertEqual("PENDING_OPERATOR_DECISION", item["status"])
            for field in ("disposition", "operator", "decided_utc", "rationale"):
                self.assertIsNone(item[field])

    def test_governance_locks_remain_closed(self):
        self.assertEqual(EXPECTED_LOCKS, self.packet["locks"])

    def test_frozen_manifest_pin_is_exact(self):
        item = next(
            item for item in self.packet["source_pins"]
            if item["path"] == "release/C11C_FREEZE_PACKAGE_MANIFEST.json"
        )
        self.assertEqual(FIXED_PINS[item["path"]], item["sha256"])

    def test_all_fixed_anchor_pins_are_present(self):
        by_path = {item["path"]: item["sha256"] for item in self.packet["source_pins"]}
        for path, expected in FIXED_PINS.items():
            self.assertEqual(expected, by_path.get(path), path)

    def test_editorial_windows_remain_unevaluated(self):
        readiness = self.packet["editorial_readiness"]
        self.assertEqual(14, readiness["editorial_field_instances"])
        self.assertEqual(11, readiness["candidate_window_rules"])
        self.assertEqual(0, readiness["evaluated_windows"])
        self.assertFalse(readiness["universal_editorial_policy_approved"])
        self.assertFalse(readiness["consumer_authorized"])

    def test_challenge_duration_conflict_is_explicitly_pending(self):
        item = next(
            item for item in self.packet["decisions"]
            if item["id"] == "CHALLENGE_008_009_DURATION_CONFLICT"
        )
        self.assertEqual("PENDING_OPERATOR_DECISION", item["status"])
        self.assertIsNone(item["disposition"])

    def test_no_render_authorization_is_claimed(self):
        self.assertEqual("OFF", self.packet["locks"]["renderer"])
        self.assertFalse(self.packet["locks"]["media_created"])
        self.assertFalse(self.packet["locks"]["candidate_input_admissible"])
        self.assertEqual("NONE", self.packet["locks"]["release_authority"])

if __name__ == "__main__":
    unittest.main(verbosity=2)