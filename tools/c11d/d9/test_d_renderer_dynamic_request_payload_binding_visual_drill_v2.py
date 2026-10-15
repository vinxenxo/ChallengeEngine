"""Focused source-chain tests for the additive V2 Visual Drill request matrix.

This test intentionally does not invoke or mock Godot and cannot accept the runtime gate.
"""
from __future__ import annotations

import copy
import json
import re
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import d_renderer_dynamic_request_payload_binding as binder  # noqa: E402
from d_renderer_temporal_bound_preview import build_temporal_bound_preview  # noqa: E402

ROOT = Path(__file__).resolve().parents[3]
FAMILIES = ("peripheral_scan", "pursuit", "saccade", "tracking")
TIERS = tuple(f"tier-{i}" for i in range(1, 6))


class VisualDrillDynamicRequestV2SourceChainTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.contract, cls.input_schema, cls.output_schema, cls.lineage = binder._load_visual_drill_v2_contract(ROOT)
        cls._canonical_chain_cache: dict[str, dict[str, Any]] | None = None

    @classmethod
    def _canonical_chains(cls) -> dict[str, dict[str, Any]]:
        if cls._canonical_chain_cache is None:
            cls._canonical_chain_cache = {}
            for raw in binder._visual_drill_matrix_raw_requests():
                key = f"{raw['selection']['family_id']}/{raw['selection']['variant_id']}"
                cls._canonical_chain_cache[key] = binder._build_canonical_chain(raw, ROOT, allow_visual_drill_matrix=True)
        return cls._canonical_chain_cache

    def test_all_common_authoring_dependencies_are_pinned_in_v2_contract(self) -> None:
        by_path = {row["path"]: row["sha256"] for row in self.lineage}
        self.assertEqual(67, len(self.lineage))
        validator_path = "core/authoring/VisualAuthoringRequestValidator.gd"
        self.assertIn(validator_path, by_path)
        self.assertEqual(
            "85eb9ec5050a78133bacb54d34a4a5464f014a41feff3599e5a2f8e76a14a30c",
            by_path[validator_path],
        )
        self.assertEqual(binder._sha_file(ROOT / validator_path), by_path[validator_path])
        self.assertTrue(set(binder.DRILL_V2_COMMON_AUTHORING_PATHS).issubset(by_path))

    def test_exact_twenty_pair_matrix_and_schema_binding(self) -> None:
        rows = binder._visual_drill_matrix_raw_requests()
        expected_pairs = {(family, tier) for family in FAMILIES for tier in TIERS}
        actual_pairs = {(raw["selection"]["family_id"], raw["selection"]["variant_id"]) for raw in rows}
        self.assertEqual(20, len(rows))
        self.assertEqual(expected_pairs, actual_pairs)
        self.assertEqual(20, len({raw["request_id"] for raw in rows}))

        try:
            import jsonschema  # type: ignore
        except ImportError:
            jsonschema = None

        canonical_chains = self._canonical_chains()
        for raw in rows:
            with self.subTest(selection=raw["selection"]):
                key = f"{raw['selection']['family_id']}/{raw['selection']['variant_id']}"
                chain = canonical_chains[key]
                selection = chain["result"]["plan"]["selection"]
                request = chain["result"]["canonical_request"]
                self.assertEqual(raw["selection"], binder._canonical_selection(selection))
                self.assertEqual(request["request_id"], chain["bridge"]["request_id"])
                self.assertEqual(request["request_id"], chain["envelope"]["source_identity"]["request_id"])
                self.assertEqual(request["request_id"], chain["source_binding"]["source_identity"]["request_id"])
                self.assertEqual(request["selection"], selection)
                self.assertEqual(selection, chain["source_binding"]["content_selection"]["selection"])

                family = raw["selection"]["family_id"]
                tier = raw["selection"]["variant_id"]
                expected_canonical = f"definitions/visual_drill_{family}_canonical.json"
                expected_policy = f"profiles/difficulty/visual_drill_{family}.json"
                source_binding = chain["source_binding"]["source_binding"]
                self.assertEqual(expected_canonical, source_binding["definition_reference"]["path"])
                self.assertEqual(binder._sha_file(ROOT / expected_canonical), source_binding["definition_reference"]["sha256"])
                self.assertEqual(tier, f"tier-{source_binding['resolved_identity']['selected_tier']}")
                self.assertIs(source_binding["selected_tier_materialized"], False)
                self.assertIs(source_binding["exact_request_payload_instance_materialized"], False)
                lineage_paths = {row["path"] for row in self.lineage}
                self.assertIn(expected_canonical, lineage_paths)
                self.assertIn(expected_policy, lineage_paths)

                temporal = build_temporal_bound_preview("visual_drills", ROOT, selection=selection)
                self.assertEqual(expected_canonical, temporal["source_identity"]["source_path"])
                self.assertEqual(family, temporal["source_identity"]["subtype"])
                self.assertIs(temporal["schedule_validation"]["simulation_truth_used"], False)
                self.assertIs(temporal["execution_boundary"]["renderer_activation"], False)

                godot_input = binder._godot_input(chain, self.contract)
                if jsonschema is not None:
                    jsonschema.Draft202012Validator(self.input_schema).validate(godot_input)

    def test_twenty_canonical_chain_resolutions_are_deterministic(self) -> None:
        first_chains = self._canonical_chains()
        for raw in binder._visual_drill_matrix_raw_requests():
            with self.subTest(selection=raw["selection"]):
                key = f"{raw['selection']['family_id']}/{raw['selection']['variant_id']}"
                first = first_chains[key]
                second = binder._build_canonical_chain(copy.deepcopy(raw), ROOT, allow_visual_drill_matrix=True)
                for key in ("request_hash", "plan_hash", "editorial_hash"):
                    self.assertEqual(first["result"][key], second["result"][key])
                self.assertEqual(first["bridge"]["record_hash"], second["bridge"]["record_hash"])
                self.assertEqual(first["envelope"]["envelope_hash"], second["envelope"]["envelope_hash"])
                self.assertEqual(first["source_binding"]["binding_sha256"], second["source_binding"]["binding_sha256"])
                self.assertEqual(first["source_binding"]["source_identity"], second["source_binding"]["source_identity"])

    def test_unknown_or_malformed_selector_fail_closed(self) -> None:
        cases: list[dict[str, Any]] = []
        base = binder._visual_drill_matrix_raw_requests()[0]
        for family in ("unknown_drill", "tracking ", ""):
            altered = copy.deepcopy(base)
            altered["request_id"] = f"NEGATIVE-UNKNOWN-{len(cases)}"
            altered["selection"]["family_id"] = family
            cases.append(altered)
        for tier in ("tier-0", "tier-6", "tier-01", "2", "tier-x"):
            altered = copy.deepcopy(base)
            altered["request_id"] = f"NEGATIVE-TIER-{len(cases)}"
            altered["selection"]["variant_id"] = tier
            cases.append(altered)
        altered = copy.deepcopy(base)
        altered["request_id"] = "NEGATIVE-SUBTYPE"
        altered["selection"]["subtype_id"] = "tracking"
        cases.append(altered)
        altered = copy.deepcopy(base)
        altered["request_id"] = "NEGATIVE-EXTRA-SELECTOR-FIELD"
        altered["selection"]["unapproved"] = True
        cases.append(altered)

        for raw in cases:
            with self.subTest(request_id=raw["request_id"]):
                with self.assertRaises(Exception):
                    binder._build_canonical_chain(raw, ROOT, allow_visual_drill_matrix=True)

    def test_godot_harness_pins_are_closed_over_v2_contract_lineage(self) -> None:
        # Prevent runtime-only GDScript pins from drifting away from source bytes.
        harness_rel = Path(self.contract["harness"]["path"])
        harness_text = (ROOT / harness_rel).read_text(encoding="utf-8")
        match = re.search(
            r"const SOURCE_PINS\s*:=\s*\{(?P<body>.*?)^\}",
            harness_text,
            flags=re.DOTALL | re.MULTILINE,
        )
        self.assertIsNotNone(match, "Godot harness SOURCE_PINS dictionary is missing")
        assert match is not None
        pin_rows = re.findall(
            r'^\s*"([^"]+)"\s*:\s*"([^"]+)"\s*,?\s*$',
            match.group("body"),
            flags=re.MULTILINE,
        )
        self.assertGreater(len(pin_rows), 0)
        harness_pins = dict(pin_rows)
        self.assertEqual(len(pin_rows), len(harness_pins), "Duplicate path in SOURCE_PINS")
        contract_pins = {row["path"]: row["sha256"] for row in self.lineage}
        for path, expected_sha in harness_pins.items():
            with self.subTest(path=path):
                self.assertRegex(expected_sha, r"^[0-9a-f]{64}$")
                source_path = ROOT / path
                self.assertTrue(source_path.is_file(), "Harness-pinned source is missing")
                self.assertEqual(binder._sha_file(source_path), expected_sha, "Harness pin does not match source bytes")
                if path in contract_pins:
                    self.assertEqual(contract_pins[path], expected_sha, "Harness/contract source pin drift")

    def test_source_pin_hash_mutation_fails_closed_in_isolated_temp_tree(self) -> None:
        # Keep the operator checkout read-only even while testing tamper rejection.
        v1_contract = json.loads((ROOT / binder.CONTRACT_REL).read_text(encoding="utf-8-sig"))
        required_paths = {
            binder.MANIFEST_REL,
            binder.CONTRACT_REL,
            binder.INPUT_SCHEMA_REL,
            binder.OUTPUT_SCHEMA_REL,
            binder.GODOT_HARNESS_REL,
            binder.DRILL_V2_CONTRACT_REL,
            binder.DRILL_V2_INPUT_SCHEMA_REL,
            binder.DRILL_V2_OUTPUT_SCHEMA_REL,
        }
        required_paths.update(Path(row["path"]) for row in v1_contract.get("source_lineage", []))
        required_paths.update(Path(row["path"]) for row in self.lineage)
        with tempfile.TemporaryDirectory(prefix="c11d_v2_pin_drift_") as temp_dir:
            temp_root = Path(temp_dir)
            for relative in sorted(required_paths):
                source = ROOT / relative
                self.assertTrue(source.is_file(), f"missing source for isolated pin-drift fixture: {relative}")
                destination = temp_root / relative
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source, destination)
            contract_path = temp_root / binder.DRILL_V2_CONTRACT_REL
            original = contract_path.read_bytes()
            mutated = json.loads(original.decode("utf-8-sig"))
            self.assertGreaterEqual(len(mutated.get("source_lineage", [])), 2)
            mutated["source_lineage"][1]["sha256"] = "0" * 64
            contract_path.write_text(json.dumps(mutated, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            with self.assertRaises(binder.DynamicRequestPayloadBindingError):
                binder._load_visual_drill_v2_contract(temp_root)
            contract_path.write_bytes(original)
            self.assertEqual(original, contract_path.read_bytes())
            binder._load_visual_drill_v2_contract(temp_root)

    def test_v2_receipts_require_verified_runtime_evidence(self) -> None:
        raw = binder._visual_drill_matrix_raw_requests()[0]
        chain = binder._build_canonical_chain(raw, ROOT, allow_visual_drill_matrix=True)
        with self.assertRaises(Exception):
            binder._build_receipt(chain, {}, ROOT, self.contract, self.lineage, (self.contract, self.input_schema, self.output_schema, self.lineage), repeat_summary=None)


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(VisualDrillDynamicRequestV2SourceChainTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():
        raise SystemExit(1)
    print(
        "C11-D DYNAMIC REQUEST PAYLOAD BINDING V2 SOURCE-CHAIN CONTRACT PASS "
        "| source_pairs=20/20 | deterministic_chain_pairs=20/20 "
        "| malformed_selector_negatives=10 | runtime_receipts=NOT_TESTED "
        "| renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE"
    )
