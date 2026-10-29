#!/usr/bin/env python3
"""Phase P live source-pin reconciliation regression; no Godot/runtime invocation."""
from __future__ import annotations
import hashlib
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CONTRACT_PATH = ROOT / "definitions/c11d/production/D_RENDERER_PHASE_P_SOURCE_VALUE_VS_FRAME_VALUE_PROVENANCE_CONTRACT_V1.json"
AUDIT_PATH = ROOT / "tools/c11d/d9/audit_d_renderer_phase_p_source_value_frame_value_provenance_20261028.py"
MANIFEST_PATH = ROOT / "release/C11C_FREEZE_PACKAGE_MANIFEST.json"
EXPECTED_CONTRACT_SHA256 = "a237e950953e70406cecd4ef94460eb8617482d1d27feebce03e3ef2f6afbb6a"
EXPECTED_MANIFEST_SHA256 = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
EXPECTED_MANIFEST_BYTES = 796318
EXPECTED_PINS = {
    "AGENTS.md": {"sha256": "67c5f237035c121f27733c24f3b2fe2da2bb104eaaa5f95e4c7a88b573071599", "bytes": 4851},
    ".continue/rules/CONTINUE.md": {"sha256": "8ee4f47588acbc981bd11400ad4186a598e052e279b8f2e2cc0bd87cb6b21c71", "bytes": 3599},
}
EXPECTED_LOCKS = {
    "renderer": "OFF", "media_created": False, "payload_materialized": False,
    "candidate_input_admissible": False, "seed_domains_complete_for_candidate_input": False,
    "automatic_seed_generation": False, "master_seed": "NOT_ADOPTED",
    "D4.8": "BLOCKED", "D9.10": "PREPARE_ONLY", "D9.14": "BLOCKED",
    "D9.16": "BLOCKED", "D9.17": "BLOCKED_NO_GO", "D10": "BLOCKED_FOR_PROMOTION",
    "baseline_approval": "MISSING", "freeze_eligible": False, "release_authority": "NONE",
}

def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

class PhasePLiveSourcePinTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract_bytes = CONTRACT_PATH.read_bytes()
        cls.contract = json.loads(cls.contract_bytes.decode("utf-8-sig"))
        cls.audit_text = AUDIT_PATH.read_text(encoding="utf-8-sig")
        cls.pins = cls.contract.get("source_pins", [])

    def test_01_contract_identity_and_hash_are_pinned_by_auditor(self):
        self.assertEqual(self.contract.get("schema"), "C11D-PHASE-P-SOURCE-VALUE-FRAME-VALUE-PROVENANCE-CONTRACT-V1")
        self.assertEqual(sha(self.contract_bytes), EXPECTED_CONTRACT_SHA256)
        self.assertIn(f'EXPECTED_PHASE_P_CONTRACT_SHA256 = "{EXPECTED_CONTRACT_SHA256}"', self.audit_text)

    def test_02_agents_pin_matches_current_v25_file(self):
        pin = next((p for p in self.pins if p.get("path") == "AGENTS.md"), None)
        data = (ROOT / "AGENTS.md").read_bytes()
        self.assertIsNotNone(pin)
        self.assertEqual(pin, {"path": "AGENTS.md", **EXPECTED_PINS["AGENTS.md"]})
        self.assertEqual(len(data), EXPECTED_PINS["AGENTS.md"]["bytes"])
        self.assertEqual(sha(data), EXPECTED_PINS["AGENTS.md"]["sha256"])

    def test_03_continue_pin_matches_current_v25_file(self):
        rel = ".continue/rules/CONTINUE.md"
        pin = next((p for p in self.pins if p.get("path") == rel), None)
        data = (ROOT / rel).read_bytes()
        self.assertIsNotNone(pin)
        self.assertEqual(pin, {"path": rel, **EXPECTED_PINS[rel]})
        self.assertEqual(len(data), EXPECTED_PINS[rel]["bytes"])
        self.assertEqual(sha(data), EXPECTED_PINS[rel]["sha256"])

    def test_04_all_source_pins_match_live_checkout_hash_and_bytes(self):
        mismatches = []
        for pin in self.pins:
            rel = pin.get("path")
            path = ROOT / str(rel)
            try:
                data = path.read_bytes()
            except OSError as exc:
                mismatches.append(f"{rel}:MISSING:{type(exc).__name__}")
                continue
            actual_sha = sha(data)
            actual_bytes = len(data)
            if actual_sha != pin.get("sha256") or actual_bytes != pin.get("bytes"):
                mismatches.append(f"{rel}:sha={actual_sha}:bytes={actual_bytes}:expected_sha={pin.get('sha256')}:expected_bytes={pin.get('bytes')}")
        self.assertEqual(mismatches, [], "SOURCE_PIN_RECONCILIATION_FAILED: " + " | ".join(mismatches))

    def test_05_pin_count_and_paths_are_stable(self):
        paths = [p.get("path") for p in self.pins]
        self.assertEqual(self.contract.get("source_pin_count"), 95)
        self.assertEqual(len(self.pins), 95)
        self.assertEqual(len(set(paths)), 95)

    def test_06_live_canonical_c11c_manifest_is_unchanged(self):
        data = MANIFEST_PATH.read_bytes()
        self.assertEqual(len(data), EXPECTED_MANIFEST_BYTES)
        self.assertEqual(sha(data), EXPECTED_MANIFEST_SHA256)
        pin = next((p for p in self.pins if p.get("path") == "release/C11C_FREEZE_PACKAGE_MANIFEST.json"), None)
        self.assertEqual(pin, {"path": "release/C11C_FREEZE_PACKAGE_MANIFEST.json", "sha256": EXPECTED_MANIFEST_SHA256, "bytes": EXPECTED_MANIFEST_BYTES})

    def test_07_governance_locks_and_zero_binding_approval_remain(self):
        locks = self.contract.get("governance_locks", {})
        for key, value in EXPECTED_LOCKS.items():
            self.assertEqual(locks.get(key), value, f"governance lock drift: {key}")
        semantic = self.contract.get("semantic_binding_policy", {})
        self.assertEqual(semantic.get("approved_bindings"), 0)
        self.assertEqual(semantic.get("approved_custom_data_bindings"), 0)
        self.assertEqual(semantic.get("approved_renderer_projection_bindings"), 0)

if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(PhasePLiveSourcePinTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if result.wasSuccessful():
        print("C11D_PHASE_P_LIVE_SOURCE_PIN_RECONCILIATION=PASS_7_OF_7")
        raise SystemExit(0)
    print("C11D_PHASE_P_LIVE_SOURCE_PIN_RECONCILIATION=FAIL")
    raise SystemExit(1)
