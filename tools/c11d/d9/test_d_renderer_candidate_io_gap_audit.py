from __future__ import annotations
import copy, json, sys, unittest
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
from d_renderer_candidate_io_gap_audit import (  # noqa: E402
    CONTRACT_REL, EXPECTED_MANIFEST_SHA256, IOGapAuditError, build_audit, validate_audit,
    _sha_file,
)

class RendererCandidateIOGapAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = build_audit(ROOT)

    def test_all_ten_required_io_groups_are_assessed_and_fail_closed(self):
        report = self.__class__.report
        self.assertEqual(len(report["input_groups"]), 10)
        self.assertEqual(report["summary"]["complete_groups"], 0)
        self.assertEqual(report["summary"]["partial_groups"], 6)
        self.assertEqual(report["summary"]["blocked_groups"], 4)
        self.assertTrue(all(row["complete_for_input_emission"] is False for row in report["input_groups"]))

    def test_payload_and_editorial_status_are_not_overstated(self):
        rows = {row["group"]: row for row in self.__class__.report["input_groups"]}
        self.assertEqual(rows["payload_instance"]["state"], "PARTIAL_REQUEST_BOUND_MANIFEST_FOR_PINNED_SELECTOR_MATRIX")
        self.assertIn("hash-closed request-specific payload manifest", rows["payload_instance"]["finding"])
        self.assertEqual(rows["source_lineage"]["state"], "PARTIAL_REQUEST_BOUND_LINEAGE_MANIFEST_FOR_PINNED_MATRIX")
        self.assertEqual(rows["editorial"]["state"], "PARTIAL_HASH_BOUND_SIDECAR_NOT_VISUALLY_CONSUMED")
        self.assertIn("0/14", rows["editorial"]["finding"])
        self.assertIn("request_payload_manifest_sha256", " ".join(rows["payload_instance"]["evidence"]))

    def test_report_and_governance_are_deterministic_and_locked(self):
        report = self.__class__.report
        self.assertEqual(build_audit(ROOT), report)
        self.assertTrue(validate_audit(report, ROOT))
        self.assertEqual(report["status"], "READ_ONLY_SOURCE_PINNED_GAP_AUDIT_PASS_NOT_READINESS_PASS")
        self.assertFalse(report["candidate_input_admissible"])
        self.assertFalse(report["summary"]["input_instance_emitted"])
        self.assertFalse(report["summary"]["output_manifest_created"])
        self.assertFalse(report["summary"]["renderer_implementation_added"])
        self.assertFalse(report["summary"]["renderer_dispatch_invoked"])
        self.assertFalse(report["summary"]["media_created"])
        self.assertEqual(report["governance"]["d4_8"], "BLOCKED")
        self.assertEqual(report["governance"]["release_authority"], "NONE")

    def test_frozen_c11c_manifest_is_first_exact_pin(self):
        first = self.__class__.report["source_pins"][0]
        self.assertEqual(first["path"], "release/C11C_FREEZE_PACKAGE_MANIFEST.json")
        self.assertEqual(first["sha256"], EXPECTED_MANIFEST_SHA256)
        self.assertEqual(_sha_file(ROOT / first["path"]), EXPECTED_MANIFEST_SHA256)

    def test_negative_report_mutations_are_rejected(self):
        mutations = [
            lambda x: x.update(candidate_input_admissible=True),
            lambda x: x["summary"].update(input_instance_emitted=True),
            lambda x: x["summary"].update(renderer_dispatch_invoked=True),
            lambda x: x["input_groups"][5].update(complete_for_input_emission=True),
            lambda x: x["input_groups"].pop(),
            lambda x: x["governance"].update(release_authority="GRANTED"),
            lambda x: x["source_pins"][0].update(sha256="0" * 64),
        ]
        for mutate in mutations:
            with self.subTest(mutate=mutate):
                candidate = copy.deepcopy(self.__class__.report)
                mutate(candidate)
                with self.assertRaises((IOGapAuditError, ValueError, TypeError, KeyError)):
                    validate_audit(candidate, ROOT)

    def test_source_drift_fails_closed_and_test_restores_bytes_exactly(self):
        path = ROOT / "definitions/c11d/production/D_RENDERER_CANDIDATE_IO_CONTRACT_V1.json"
        original = path.read_bytes()
        try:
            path.write_bytes(original + b" ")
            with self.assertRaises(IOGapAuditError):
                build_audit(ROOT)
        finally:
            path.write_bytes(original)
        self.assertEqual(path.read_bytes(), original)
        self.assertEqual(build_audit(ROOT), self.__class__.report)

    def test_contract_pins_are_safe_unique_and_complete(self):
        contract = json.loads((ROOT / CONTRACT_REL).read_text(encoding="utf-8"))
        pins = contract["source_pins"]
        paths = [row["path"] for row in pins]
        self.assertGreaterEqual(len(paths), 33)
        self.assertEqual(len(paths), len(set(paths)))
        for row in pins:
            self.assertNotIn("..", Path(row["path"]).parts)
            self.assertEqual(len(row["sha256"]), 64)

    def test_accepted_visual_drill_v2_sources_remain_hash_bound(self):
        contract = json.loads((ROOT / CONTRACT_REL).read_text(encoding="utf-8"))
        pins = {row["path"]: row["sha256"] for row in contract["source_pins"]}
        expected_paths = {
            "tools/c11d/d9/d_renderer_dynamic_request_payload_binding.py",
            "definitions/c11d/production/D_RENDERER_DYNAMIC_REQUEST_PAYLOAD_BINDING_V2.json",
            "tools/c11d/d9/materialize_visual_drill_dynamic_request_payload_in_memory_v2.gd",
            "tools/c11d/d9/test_d_renderer_dynamic_request_payload_binding_visual_drill_v2.py",
        }
        self.assertTrue(expected_paths.issubset(pins))
        for rel in expected_paths:
            actual = _sha_file(ROOT / rel)
            self.assertEqual(pins[rel], actual, f"stale source pin: {rel}")
        expected_seed_audit_paths = {
            "definitions/c11d/production/D_RENDERER_VISUAL_DRILL_SEED_DOMAIN_AUDIT_V1.json",
            "definitions/c11d/production/D_RENDERER_VISUAL_DRILL_SEED_DOMAIN_AUDIT_SCHEMA_V1.json",
            "tools/c11d/d9/d_renderer_visual_drill_seed_domain_audit.py",
            "tools/c11d/d9/test_d_renderer_visual_drill_seed_domain_audit.py",
        }
        self.assertTrue(expected_seed_audit_paths.issubset(pins))
        for rel in expected_seed_audit_paths:
            self.assertEqual(pins[rel], _sha_file(ROOT / rel), f"stale seed audit pin: {rel}")
        cross_type_seed_audit_paths = {
            "definitions/c11d/production/D_RENDERER_CANDIDATE_SEED_DOMAIN_AUDIT_V1.json",
            "definitions/c11d/production/D_RENDERER_CANDIDATE_SEED_DOMAIN_AUDIT_SCHEMA_V1.json",
            "tools/c11d/d9/d_renderer_candidate_seed_domain_audit.py",
            "tools/c11d/d9/test_d_renderer_candidate_seed_domain_audit.py",
        }
        self.assertTrue(cross_type_seed_audit_paths.issubset(pins))
        for rel in cross_type_seed_audit_paths:
            self.assertEqual(pins[rel], _sha_file(ROOT / rel), f"stale cross-type seed audit pin: {rel}")
        self.assertEqual(len(contract["source_pins"]), 54)
        seed_group = {row["group"]: row for row in contract["input_group_assessments"]}["seed_domains"]
        self.assertEqual(seed_group["state"], "PARTIAL_FIXED_SEED_DOMAINS")
        self.assertIn("full catalog", " ".join(seed_group["unclosed_requirements"]))
        payload = {row["group"]: row for row in self.__class__.report["input_groups"]}["payload_instance"]
        self.assertEqual(payload["state"], "PARTIAL_REQUEST_BOUND_MANIFEST_FOR_PINNED_SELECTOR_MATRIX")
        self.assertFalse(payload["complete_for_input_emission"])
        groups = {row["group"]: row for row in contract["input_group_assessments"]}
        identity_finding = groups["content_identity"]["finding"]
        self.assertIn("all 20 canonical Visual Drill type/tier pairs", identity_finding)
        self.assertNotIn("Drill types/tiers are still outside the admitted matrix", identity_finding)
        seed_finding = groups["seed_domains"]["finding"]
        self.assertIn("operator reports PASS", seed_finding)
        self.assertIn("Visual Drill seed-domain runtime PASS", " ".join(groups["seed_domains"]["evidence"]))
        self.assertIn("explicit-seed/collision rejection audit", seed_finding)
        self.assertIn("evidence-capture repair", seed_finding)
        self.assertFalse(groups["seed_domains"]["complete_for_input_emission"])

    def test_tool_is_stdout_only_and_has_no_production_dispatch_path(self):
        source = (HERE / "d_renderer_candidate_io_gap_audit.py").read_text(encoding="utf-8")
        self.assertNotIn("write_text(", source)
        self.assertNotIn("write_bytes(", source)
        self.assertNotIn("MovieWriter", source)
        self.assertNotIn("render_video(", source)
        self.assertIn("--full-report", source)
        self.assertIn("renderer_input_instance_emitted", source)


def main() -> int:
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(RendererCandidateIOGapAuditTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():
        return 1
    summary = RendererCandidateIOGapAuditTests.report["summary"] if hasattr(RendererCandidateIOGapAuditTests, "report") else build_audit(ROOT)["summary"]
    print("C11-D CANDIDATE I/O CONFORMANCE GAP AUDIT CONTRACT PASS"
          f" | tests={result.testsRun}/{result.testsRun} | groups={summary['schema_groups']}/10 | partial={summary['partial_groups']}"
          f" | blocked={summary['blocked_groups']} | source_pins={summary['source_pins_verified']}/{summary['source_pins_verified']}"
          " | candidate_input_admissible=false | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
