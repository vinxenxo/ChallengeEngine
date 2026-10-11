from __future__ import annotations

import hashlib
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = ROOT / "tools/c11d/d9/d_renderer_candidate_identity_inventory.py"
sys.path.insert(0, str(MODULE_PATH.parent))
import d_renderer_candidate_identity_inventory as inventory  # noqa: E402

CONTRACT_REL = "definitions/c11d/production/D_RENDERER_CANDIDATE_IDENTITY_INVENTORY_V1.json"
SCHEMA_REL = "definitions/c11d/production/D_RENDERER_CANDIDATE_IDENTITY_INVENTORY_SCHEMA_V1.json"


class RendererCandidateIdentityInventoryTests(unittest.TestCase):
    def test_contract_pins_at_least_one_hundred_unique_sorted_sources(self):
        contract = json.loads((ROOT / CONTRACT_REL).read_text(encoding="utf-8"))
        paths = [row["path"] for row in contract["source_inventory"]]
        self.assertGreaterEqual(len(paths), 100)
        self.assertEqual(paths, sorted(paths))
        self.assertEqual(len(paths), len(set(paths)))
        self.assertEqual(contract["status"], "READ_ONLY_CANDIDATE_IDENTITY_ONLY_NOT_APPROVAL_OR_FREEZE")

    def test_build_is_deterministic_and_self_hashes(self):
        first = inventory.build_inventory(ROOT, probe_godot=False)
        second = inventory.build_inventory(ROOT, probe_godot=False)
        self.assertEqual(first, second)
        unsigned = {k: v for k, v in first.items() if k != "report_sha256"}
        self.assertEqual(first["report_sha256"], inventory.sha256_json(unsigned))
        self.assertEqual(first["source_fingerprint"], inventory.sha256_json(first["source_inventory"]))

    def test_manifest_and_governance_stay_locked(self):
        report = inventory.build_inventory(ROOT, probe_godot=False)
        self.assertTrue(report["protected_reference"]["matches_expected"])
        locks = report["governance"]
        self.assertEqual(locks["renderer_implementation"], "NOT_IMPLEMENTED")
        self.assertEqual(locks["renderer_build_artifact"], "NONE")
        self.assertFalse(locks["renderer_input_emitted"])
        self.assertFalse(locks["renderer_dispatch_invoked"])
        self.assertEqual(locks["renderer_activation"], "OFF")
        self.assertFalse(locks["media_created"])
        self.assertEqual(locks["d4_8"], "BLOCKED")
        self.assertEqual(locks["release_authority"], "NONE")
        self.assertFalse(locks["freeze_eligible"])
        self.assertEqual(len(report["required_candidate_blockers"]), 5)

    def test_report_schema_is_strict_and_validates(self):
        report = inventory.build_inventory(ROOT, probe_godot=False)
        schema = json.loads((ROOT / SCHEMA_REL).read_text(encoding="utf-8"))
        self.assertIs(schema.get("additionalProperties"), False)
        self.assertEqual(schema.get("$schema"), "https://json-schema.org/draft/2020-12/schema")
        try:
            from jsonschema import Draft202012Validator
        except ImportError:
            self.assertTrue(set(schema["required"]).issubset(report))
        else:
            Draft202012Validator(schema).validate(report)

    def test_pinned_source_tamper_fails_closed(self):
        contract = json.loads((ROOT / CONTRACT_REL).read_text(encoding="utf-8"))
        context_paths = contract["report_context_paths"]
        packet_paths = [entry["path"] for entry in contract["review_packet_components"]]
        all_paths = [CONTRACT_REL, SCHEMA_REL, str(inventory.RUNNER_REL), str(inventory.TEST_REL)]
        all_paths += [row["path"] for row in contract["source_inventory"]] + context_paths + packet_paths
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            for rel in set(all_paths):
                src = ROOT / rel
                dst = temp_root / rel
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)
            pinned = temp_root / contract["source_inventory"][0]["path"]
            pinned.write_bytes(pinned.read_bytes() + b"tamper")
            with self.assertRaisesRegex(inventory.CandidateInventoryError, "SHA-256 mismatch"):
                inventory.build_inventory(temp_root, probe_godot=False)

    def test_contract_cannot_self_approve(self):
        contract = json.loads((ROOT / CONTRACT_REL).read_text(encoding="utf-8"))
        contract["status"] = "APPROVED_AND_FROZEN"
        with self.assertRaisesRegex(inventory.CandidateInventoryError, "cannot claim approval or freeze"):
            inventory._validate_contract(contract)

    def test_contract_hash_drift_fails_closed(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            for rel in (CONTRACT_REL, SCHEMA_REL):
                dst = temp_root / rel
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(ROOT / rel, dst)
            contract_file = temp_root / CONTRACT_REL
            contract_file.write_bytes(contract_file.read_bytes() + b"\n")
            with self.assertRaisesRegex(inventory.CandidateInventoryError, "contract SHA-256 mismatch"):
                inventory.build_inventory(temp_root, probe_godot=False)

    def test_unknown_or_escaping_paths_rejected(self):
        for value in ("../release/file.json", "/absolute/file.json", "C:/absolute/file.json", "a\\b.json"):
            with self.subTest(value=value), self.assertRaises(inventory.CandidateInventoryError):
                inventory._relative_path(value)

    def test_inventory_does_not_persist_reports_or_touch_protected_inputs(self):
        before_manifest = hashlib.sha256((ROOT / "release/C11C_FREEZE_PACKAGE_MANIFEST.json").read_bytes()).hexdigest()
        before_timebase = hashlib.sha256((ROOT / "definitions/c11d/production/D_RENDERER_UNIFIED_DELIVERY_TIMEBASE_POLICY_PROPOSAL_V1.json").read_bytes()).hexdigest()
        files_before = {str(p.relative_to(ROOT)) for p in ROOT.rglob("*") if p.is_file()}
        inventory.build_inventory(ROOT, probe_godot=False)
        files_after = {str(p.relative_to(ROOT)) for p in ROOT.rglob("*") if p.is_file()}
        self.assertEqual(files_before, files_after)
        self.assertEqual(before_manifest, hashlib.sha256((ROOT / "release/C11C_FREEZE_PACKAGE_MANIFEST.json").read_bytes()).hexdigest())
        self.assertEqual(before_timebase, hashlib.sha256((ROOT / "definitions/c11d/production/D_RENDERER_UNIFIED_DELIVERY_TIMEBASE_POLICY_PROPOSAL_V1.json").read_bytes()).hexdigest())


if __name__ == "__main__":
    unittest.main(verbosity=2)
