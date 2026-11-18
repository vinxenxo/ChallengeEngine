from __future__ import annotations

import copy
import importlib
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

PROJECT_ROOT = Path(__file__).resolve().parents[3]
D9_DIR = PROJECT_ROOT / "tools" / "c11d" / "d9"
sys.path.insert(0, str(D9_DIR))
review = importlib.import_module("c11e_e6_ch004_semantic_noninterference_review_v2")


class HistoricalJsonTests(unittest.TestCase):
    def setUp(self):
        self.old = {
            "schema": "editorial-v1",
            "content_types": {
                "challenges": {"state": "ACTIVE", "request_plan_compatibility": "CURRENT_D4_CHALLENGE_REQUEST_ONLY", "editable_fields": ["title", "subtitle"]},
                "visual_loops": {"state": "ACTIVE_MODEL_ONLY", "editable_fields": ["title"]},
                "visual_drills": {"state": "ACTIVE_MODEL_ONLY", "editable_fields": ["subtitle"]},
            },
            "profiles": {"challenge": {"font": "Inter"}},
        }
        self.current = copy.deepcopy(self.old)
        self.current["content_types"]["visual_loops"].update({"d9_9_plan_compatible": True, "d4_executable_compatible": False})
        self.current["content_types"]["visual_drills"].update({"d9_9_plan_compatible": True, "d4_executable_compatible": False})

    def test_exact_four_loop_drill_flags_are_the_only_model_delta(self):
        result = review.verify_model_semantic_delta(json.dumps(self.old).encode(), json.dumps(self.current).encode())
        self.assertEqual(result["status"], "PASS_ONLY_FOUR_LOOP_DRILL_COMPATIBILITY_FLAGS_ADDED")
        self.assertTrue(result["challenge_declaration_identical"])
        self.assertEqual(len(result["allowed_differences"]), 4)

    def test_challenge_model_change_blocks(self):
        altered = copy.deepcopy(self.current)
        altered["content_types"]["challenges"]["request_plan_compatibility"] = "CHANGED"
        with self.assertRaisesRegex(review.ReviewError, "D98_MODEL_CHANGED_OUTSIDE"):
            review.verify_model_semantic_delta(json.dumps(self.old).encode(), json.dumps(altered).encode())

    def test_unapproved_loop_flag_value_blocks(self):
        altered = copy.deepcopy(self.current)
        altered["content_types"]["visual_loops"]["d4_executable_compatible"] = True
        with self.assertRaisesRegex(review.ReviewError, "D98_MODEL_CURRENT_FLAG_VALUE_MISMATCH"):
            review.verify_model_semantic_delta(json.dumps(self.old).encode(), json.dumps(altered).encode())

    def test_unapproved_extra_model_key_blocks(self):
        altered = copy.deepcopy(self.current)
        altered["content_types"]["visual_drills"]["renderer_enabled"] = True
        with self.assertRaisesRegex(review.ReviewError, "D98_MODEL_CHANGED_OUTSIDE"):
            review.verify_model_semantic_delta(json.dumps(self.old).encode(), json.dumps(altered).encode())

    def test_historical_json_must_not_already_have_compatibility_flags(self):
        altered_old = copy.deepcopy(self.old)
        altered_old["content_types"]["visual_loops"]["d9_9_plan_compatible"] = False
        with self.assertRaisesRegex(review.ReviewError, "D98_MODEL_HISTORICAL_PREIMAGE_ALREADY_HAS_NEW_FLAG"):
            review.verify_model_semantic_delta(json.dumps(altered_old).encode(), json.dumps(self.current).encode())


class ResolverParityTests(unittest.TestCase):
    class OldResolver:
        @staticmethod
        def resolve_selection(selection, root):
            return {"selection": copy.deepcopy(selection), "scope_keys": {"family": "parking_v2", "variant": selection["variant_id"]}, "request_plan_compatible": True}

        @staticmethod
        def resolve_editorial_values(selection, profile=None, production_override=None, project_root=None):
            return {"values": {"title": "same", "call_to_action": (production_override or {}).get("call_to_action", "FOLLOW AGAIN")}, "request_plan_compatible": True, "request_plan_state": "CURRENT_D4_CHALLENGE_PATH"}

    class NewResolver(OldResolver):
        @staticmethod
        def resolve_selection(selection, root):
            result = ResolverParityTests.OldResolver.resolve_selection(selection, root)
            result.update({"d9_9_plan_compatible": True, "d4_executable_compatible": True})
            return result

        @staticmethod
        def resolve_editorial_values(selection, profile=None, production_override=None, project_root=None):
            result = ResolverParityTests.OldResolver.resolve_editorial_values(selection, profile, production_override, project_root)
            result.update({"d9_9_plan_compatible": True, "d4_executable_compatible": True})
            return result

    def test_six_challenge_selectors_preserve_d4_and_editorial_resolution(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            rows = review.challenge_selector_parity(self.OldResolver, self.NewResolver, root, root)
        self.assertEqual(len(rows), 6)
        self.assertTrue(all(row["status"] == "PASS" for row in rows))
        self.assertTrue(all(row["current_d4_path"] == "CURRENT_D4_CHALLENGE_PATH" for row in rows))

    def test_selection_drift_is_not_filtered(self):
        class BadResolver(self.NewResolver):
            @staticmethod
            def resolve_selection(selection, root):
                result = ResolverParityTests.NewResolver.resolve_selection(selection, root)
                result["selection"]["variant_id"] = "CHALLENGE_WRONG"
                return result
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            with self.assertRaisesRegex(review.ReviewError, "D98_CHALLENGE_RESOLVE_SELECTION_DRIFT"):
                review.challenge_selector_parity(self.OldResolver, BadResolver, root, root)

    def test_plan_state_drift_is_not_filtered(self):
        class BadResolver(self.NewResolver):
            @staticmethod
            def resolve_editorial_values(selection, profile=None, production_override=None, project_root=None):
                result = ResolverParityTests.NewResolver.resolve_editorial_values(selection, profile, production_override, project_root)
                result["request_plan_state"] = "D9_9_UNIVERSAL_EDITORIAL_INTENT_PLAN_ONLY"
                return result
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            with self.assertRaisesRegex(review.ReviewError, "D98_CHALLENGE_EDITORIAL_VALUE_DRIFT"):
                review.challenge_selector_parity(self.OldResolver, BadResolver, root, root)


class SourceIdentityTests(unittest.TestCase):
    def _rows(self):
        rows = []
        for i in range(12):
            rows.append({"path": f"stable/{i}.py", "bytes": 100 + i, "sha256": f"{i:064x}"})
        rows[1] = {"path": "tools/c11d/d9/universal_editorial_model.py", "bytes": 26574, "sha256": review.SOURCES["tools/c11d/d9/universal_editorial_model.py"]["pre_sha"]}
        rows[3] = {"path": "definitions/c11d/personalization/C11D_UNIVERSAL_EDITORIAL_MODEL_V1.json", "bytes": 12692, "sha256": review.SOURCES["definitions/c11d/personalization/C11D_UNIVERSAL_EDITORIAL_MODEL_V1.json"]["pre_sha"]}
        return rows

    def test_only_resolver_and_transitive_json_hashes_may_change(self):
        old = {"source_identity": {"source_pins": self._rows()}}
        current_rows = copy.deepcopy(old["source_identity"]["source_pins"])
        current_rows[1]["sha256"] = review.SOURCES["tools/c11d/d9/universal_editorial_model.py"]["current_sha"]
        current_rows[1]["bytes"] = review.SOURCES["tools/c11d/d9/universal_editorial_model.py"]["current_bytes"]
        current_rows[3]["sha256"] = review.SOURCES["definitions/c11d/personalization/C11D_UNIVERSAL_EDITORIAL_MODEL_V1.json"]["current_sha"]
        current_rows[3]["bytes"] = review.SOURCES["definitions/c11d/personalization/C11D_UNIVERSAL_EDITORIAL_MODEL_V1.json"]["current_bytes"]
        new = {"source_identity": {"source_pins": current_rows}}
        result = review.compare_source_identity(old, new)
        self.assertTrue(result["source_pin_paths_identical"])
        self.assertEqual(len(result["only_expected_historical_paths_changed"]), 2)

    def test_service_or_challenge_source_pin_drift_blocks(self):
        old = {"source_identity": {"source_pins": self._rows()}}
        current_rows = copy.deepcopy(old["source_identity"]["source_pins"])
        current_rows[0]["sha256"] = "f" * 64
        current_rows[1]["sha256"] = review.SOURCES["tools/c11d/d9/universal_editorial_model.py"]["current_sha"]
        current_rows[1]["bytes"] = review.SOURCES["tools/c11d/d9/universal_editorial_model.py"]["current_bytes"]
        current_rows[3]["sha256"] = review.SOURCES["definitions/c11d/personalization/C11D_UNIVERSAL_EDITORIAL_MODEL_V1.json"]["current_sha"]
        current_rows[3]["bytes"] = review.SOURCES["definitions/c11d/personalization/C11D_UNIVERSAL_EDITORIAL_MODEL_V1.json"]["current_bytes"]
        with self.assertRaisesRegex(review.ReviewError, "CHALLENGE_SOURCE_IDENTITY_UNEXPECTED_DELTA"):
            review.compare_source_identity(old, {"source_identity": {"source_pins": current_rows}})

    def test_known_dependency_hash_with_wrong_byte_count_blocks(self):
        old = {"source_identity": {"source_pins": self._rows()}}
        current_rows = copy.deepcopy(old["source_identity"]["source_pins"])
        current_rows[1]["sha256"] = review.SOURCES["tools/c11d/d9/universal_editorial_model.py"]["current_sha"]
        current_rows[1]["bytes"] = review.SOURCES["tools/c11d/d9/universal_editorial_model.py"]["current_bytes"] + 1
        current_rows[3]["sha256"] = review.SOURCES["definitions/c11d/personalization/C11D_UNIVERSAL_EDITORIAL_MODEL_V1.json"]["current_sha"]
        current_rows[3]["bytes"] = review.SOURCES["definitions/c11d/personalization/C11D_UNIVERSAL_EDITORIAL_MODEL_V1.json"]["current_bytes"]
        with self.assertRaisesRegex(review.ReviewError, "CHALLENGE_SOURCE_IDENTITY_UNEXPECTED_DELTA"):
            review.compare_source_identity(old, {"source_identity": {"source_pins": current_rows}})

    def test_other_source_identity_metadata_must_remain_identical(self):
        old = {"source_identity": {"c11c_manifest": {"sha256": "e" * 64}, "source_pins": self._rows()}}
        current = copy.deepcopy(old)
        current["source_identity"]["source_pins"][1]["sha256"] = review.SOURCES["tools/c11d/d9/universal_editorial_model.py"]["current_sha"]
        current["source_identity"]["source_pins"][1]["bytes"] = review.SOURCES["tools/c11d/d9/universal_editorial_model.py"]["current_bytes"]
        current["source_identity"]["source_pins"][3]["sha256"] = review.SOURCES["definitions/c11d/personalization/C11D_UNIVERSAL_EDITORIAL_MODEL_V1.json"]["current_sha"]
        current["source_identity"]["source_pins"][3]["bytes"] = review.SOURCES["definitions/c11d/personalization/C11D_UNIVERSAL_EDITORIAL_MODEL_V1.json"]["current_bytes"]
        current["source_identity"]["c11c_manifest"]["sha256"] = "f" * 64
        with self.assertRaisesRegex(review.ReviewError, "CHALLENGE_SOURCE_IDENTITY_METADATA_CHANGED_OUTSIDE_ALLOWED_PINS"):
            review.compare_source_identity(old, current)

    def test_source_pin_order_cannot_change(self):
        old_rows = self._rows()
        new_rows = copy.deepcopy(old_rows)
        new_rows[0], new_rows[2] = new_rows[2], new_rows[0]
        with self.assertRaisesRegex(review.ReviewError, "CHALLENGE_SOURCE_PIN_PATH_SET_OR_ORDER_CHANGED"):
            review.compare_source_identity({"source_identity": {"source_pins": old_rows}}, {"source_identity": {"source_pins": new_rows}})


class IntentAndGovernanceTests(unittest.TestCase):
    def test_intent_projection_ignores_only_seal_and_source_metadata(self):
        value = {"service_version": "old", "intent_sha256": "a", "source_identity": {"x": 1}, "identity": {"intent_hash": "b", "request_hash": "c"}, "request": {"content_type": "challenges"}}
        expected = {"identity": {"request_hash": "c"}, "request": {"content_type": "challenges"}}
        self.assertEqual(review._intent_projection(value), expected)

    def test_e4b_service_intermediate_is_distinct_from_current_e4c_postimage(self):
        self.assertEqual(review.E4B_SERVICE_INTERMEDIATE_SHA, "08ab5a278de8ebb55795a57391c83a27207ce01920704c419b8e28be25ddcf65")
        self.assertNotEqual(review.E4B_SERVICE_INTERMEDIATE_SHA, review.SOURCES["c11c-suite/c11c-producer/c11e_production_service.py"]["current_sha"])

    def test_e4b_backup_slots_cover_all_three_transitive_dependencies(self):
        self.assertEqual(set(review.E4B_V3_BACKUP_PATHS), set(review.SOURCES))
        self.assertEqual(set(review.E4B_V3_BACKUP_PATHS.values()), {"01.bak", "04.bak", "05.bak"})

    def test_smoke18_reconciliation_is_not_media_authorization(self):
        report_source = Path(review.__file__).read_text(encoding="utf-8")
        for required in ('"automatic_e6_acceptance": False', '"d4_8_overridden": False', '"release_authority": "NONE"'):
            self.assertIn(required, report_source)

    def test_source_module_has_no_media_process_invocations(self):
        tree = __import__("ast").parse(Path(review.__file__).read_text(encoding="utf-8"))
        names = [node.name for node in tree.body if isinstance(node, __import__("ast").FunctionDef)]
        self.assertIn("run_audit", names)
        self.assertFalse(any(name in {"subprocess", "Popen", "run", "godot", "ffmpeg", "ffprobe"} for name in names))


class PathSafetyTests(unittest.TestCase):
    def test_safe_relative_project_path(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "nested").mkdir()
            result = review.safe_path(root, "nested/file.txt")
            self.assertEqual(result, root.resolve() / "nested/file.txt")

    def test_absolute_path_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaisesRegex(review.ReviewError, "UNSAFE_PROJECT_PATH"):
                review.safe_path(Path(temp), "/outside/file")

    def test_parent_traversal_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaisesRegex(review.ReviewError, "UNSAFE_PROJECT_PATH"):
                review.safe_path(Path(temp), "../outside")

    def test_windows_drive_path_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaisesRegex(review.ReviewError, "UNSAFE_PROJECT_PATH"):
                review.safe_path(Path(temp), "C:/outside/file")

    def test_reparse_ancestor_rejected_without_os_symlink(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "junction").mkdir()
            with mock.patch.object(review, "_is_reparse", side_effect=lambda p: Path(p).name == "junction"):
                with self.assertRaisesRegex(review.ReviewError, "REPARSE_POINT_IN_PROJECT_PATH"):
                    review.safe_path(root, "junction/escape.txt")


class DiffAndSchemaTests(unittest.TestCase):
    def test_diff_review_requires_all_three_dependencies(self):
        text = "universal_editorial_model.py c11e_production_service.py request_plan_state visual_loops visual_drills"
        self.assertTrue(all(x in text for x in ("universal_editorial_model.py", "c11e_production_service.py", "request_plan_state", "visual_loops", "visual_drills")))

    def test_challenge_id_matrix_is_exactly_six(self):
        self.assertEqual(review.CHALLENGE_IDS, ["CHALLENGE_001", "CHALLENGE_002", "CHALLENGE_004", "CHALLENGE_005", "CHALLENGE_006", "CHALLENGE_007"])

    def test_old_e1_service_version_is_explicitly_pinned(self):
        self.assertEqual(review._historical_raw_request.__name__, "_historical_raw_request")
        source = Path(review.__file__).read_text(encoding="utf-8")
        self.assertIn('"0.2.0-E3.2"', source)
        self.assertIn('"0.4.0-E4C"', source)

if __name__ == "__main__":
    unittest.main(verbosity=2)
