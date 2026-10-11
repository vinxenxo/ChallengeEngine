from __future__ import annotations

import contextlib
import copy
import io
import json
import subprocess
import sys
import unittest
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from d_renderer_editorial_field_routing_visibility_reconciliation import EXPECTED_FIELDS
from d_renderer_request_scoped_editorial_value_carrier import (
    CONTRACT_REL,
    INPUT_SCHEMA_REL,
    SCHEMA_REL,
    CONTENT_TYPES,
    INPUT_SCHEMA_ID,
    EditorialValueCarrierError,
    _canonical,
    _sha_json,
    build_carrier,
    load_override_file,
    run_materialization_review,
    validate_carrier,
)
from d_renderer_request_scoped_payload_materialization_binding import HARNESS_SPECS
from test_d_renderer_visual_payload_materialization_preview import _record as visual_fixture_report
from test_d_renderer_challenge_visual_payload_preview import fixture_report as challenge_fixture_report


def _fake_process_runner(command: list[str], **kwargs: Any) -> subprocess.CompletedProcess[str]:
    script_arg = command[command.index("--script") + 1].removeprefix("res://")
    if script_arg == HARNESS_SPECS["visual_loop_drill_materialization"]["script"]:
        name = "visual_loop_drill_materialization"
        report = visual_fixture_report()
    elif script_arg == HARNESS_SPECS["challenge_visual_payload_materialization"]["script"]:
        name = "challenge_visual_payload_materialization"
        report = challenge_fixture_report()
    else:
        raise AssertionError(f"Unexpected Godot harness command: {script_arg}")
    spec = HARNESS_SPECS[name]
    output = spec["pass_marker"] + " | fixture=mocked_for_unit_test\n" + spec["summary_prefix"] + _canonical(report) + "\n"
    return subprocess.CompletedProcess(command, 0, stdout=output, stderr=None)


class RequestScopedEditorialValueCarrierTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        with contextlib.redirect_stdout(io.StringIO()):
            cls.materialization_receipt = run_materialization_review(
                ROOT,
                executable="fake-godot-4.7.1",
                process_runner=_fake_process_runner,
            )
            cls.carrier = build_carrier(cls.materialization_receipt, root=ROOT)

    def test_contract_source_pins_and_strict_schemas(self) -> None:
        contract = json.loads((ROOT / CONTRACT_REL).read_text(encoding="utf-8-sig"))
        output_schema = json.loads((ROOT / SCHEMA_REL).read_text(encoding="utf-8-sig"))
        input_schema = json.loads((ROOT / INPUT_SCHEMA_REL).read_text(encoding="utf-8-sig"))
        self.assertEqual(contract["status"], "PREPARATION_ONLY_HASH_BOUND_EDITORIAL_SIDECAR_NOT_VISUAL_CONSUMPTION")
        self.assertGreaterEqual(len(contract["source_lineage"]), 18)
        self.assertEqual(contract["source_lineage"][0]["path"], "release/C11C_FREEZE_PACKAGE_MANIFEST.json")
        self.assertEqual(len({row["path"] for row in contract["source_lineage"]}), len(contract["source_lineage"]))
        self.assertIs(output_schema["additionalProperties"], False)
        self.assertIs(input_schema["additionalProperties"], False)
        try:
            import jsonschema  # type: ignore
        except ImportError:
            self.skipTest("jsonschema not installed; runtime has structural validation")
        jsonschema.Draft202012Validator.check_schema(output_schema)
        jsonschema.Draft202012Validator.check_schema(input_schema)
        jsonschema.Draft202012Validator(output_schema).validate(self.__class__.carrier)

    def test_all_fourteen_canonical_values_are_hash_bound_but_not_visually_consumed(self) -> None:
        receipt = self.__class__.carrier
        self.assertEqual([row["content_type"] for row in receipt["content_bindings"]], list(CONTENT_TYPES))
        self.assertEqual(receipt["summary"], {
            "content_types": 3,
            "enabled_editorial_field_instances": 14,
            "hash_bound_sidecar_field_values": 14,
            "visual_text_values_in_sidecar": 11,
            "metadata_only_values_in_sidecar": 3,
            "visual_payload_text_consumed": 0,
            "payload_member_injection": False,
            "all_changes_editorial_only": True,
            "video_render_ready": False,
        })
        for binding in receipt["content_bindings"]:
            self.assertTrue(binding["editorial_only_delta_from_base_request"])
            self.assertTrue(binding["selection_seed_profile_match"])
            self.assertFalse(binding["payload_mutated"])
            self.assertFalse(binding["editorial_values_injected_into_visual_payload"])
            self.assertFalse(binding["visual_payload_consumed_editorial_text"])
            self.assertTrue(binding["request_hash_matches_base_materialization_request"])
            self.assertEqual([field["field_name"] for field in binding["fields"]], list(EXPECTED_FIELDS[binding["content_type"]]))
        self.assertEqual(receipt["carrier_sha256"], _sha_json({key: value for key, value in receipt.items() if key != "carrier_sha256"}))

    def test_language_is_metadata_and_challenge_phase_fields_are_not_aliases(self) -> None:
        receipt = self.__class__.carrier
        for binding in receipt["content_bindings"]:
            language = next(item for item in binding["fields"] if item["field_name"] == "language")
            self.assertEqual(language["field_kind"], "METADATA_ONLY")
            self.assertIsNone(language["semantic_region_id"])
            self.assertIsNone(language["visibility_window"])
            self.assertFalse(language["presentation_applied"])
        challenge = receipt["content_bindings"][0]
        self.assertEqual([item["field_name"] for item in challenge["fields"]], ["title", "subtitle", "call_to_action", "language", "player_name", "challenge_label"])

    def test_dynamic_editorial_override_changes_only_carrier_and_request_hash(self) -> None:
        overrides = {
            "schema": INPUT_SCHEMA_ID,
            "schema_version": "1.0",
            "values_by_content_type": {
                "visual_loops": {"title": "  Alternate Loop Title  ", "language": " EN "},
                "challenges": {"player_name": "MARTA"},
            },
        }
        normalized = {
            "visual_loops": {"title": "  Alternate Loop Title  ", "language": " EN "},
            "challenges": {"player_name": "MARTA"},
        }
        input_digest = _sha_json({"schema": INPUT_SCHEMA_ID, "schema_version": "1.0", "values_by_content_type": normalized})
        changed = build_carrier(
            self.__class__.materialization_receipt,
            root=ROOT,
            overrides=normalized,
            override_input_sha256=input_digest,
        )
        base_rows = {row["content_type"]: row for row in self.__class__.carrier["content_bindings"]}
        changed_rows = {row["content_type"]: row for row in changed["content_bindings"]}
        loop_fields = {item["field_name"]: item for item in changed_rows["visual_loops"]["fields"]}
        challenge_fields = {item["field_name"]: item for item in changed_rows["challenges"]["fields"]}
        self.assertEqual(loop_fields["title"]["value"], "Alternate Loop Title")
        self.assertEqual(loop_fields["language"]["value"], "en")
        self.assertEqual(challenge_fields["player_name"]["value"], "MARTA")
        for content_type in CONTENT_TYPES:
            self.assertEqual(changed_rows[content_type]["payload_instance_sha256"], base_rows[content_type]["payload_instance_sha256"])
            self.assertFalse(changed_rows[content_type]["payload_mutated"])
            self.assertFalse(changed_rows[content_type]["editorial_values_injected_into_visual_payload"])
        self.assertNotEqual(changed_rows["visual_loops"]["canonical_request_sha256"], changed_rows["visual_loops"]["base_materialization_request_sha256"])
        self.assertFalse(changed_rows["visual_loops"]["request_hash_matches_base_materialization_request"])
        self.assertEqual(changed_rows["visual_drills"]["canonical_request_sha256"], changed_rows["visual_drills"]["base_materialization_request_sha256"])
        self.assertEqual(changed["carrier_sha256"], _sha_json({key: value for key, value in changed.items() if key != "carrier_sha256"}))

    def test_override_input_file_is_read_only_and_canonical_digest_is_reproducible(self) -> None:
        input_obj = {
            "schema": INPUT_SCHEMA_ID,
            "schema_version": "1.0",
            "values_by_content_type": {"visual_drills": {"title": "  Drill Title  "}},
        }
        path = ROOT / "tools" / "c11d" / "d9" / ".temp_editorial_values_test_input.json"
        try:
            path.write_text(json.dumps(input_obj), encoding="utf-8")
            overrides, digest = load_override_file(path, ROOT)
            self.assertEqual(overrides, {"visual_drills": {"title": "  Drill Title  "}})
            self.assertEqual(digest, _sha_json(input_obj))
        finally:
            path.unlink(missing_ok=True)

    def test_reject_unknown_disabled_and_non_editorial_input_fields(self) -> None:
        cases = [
            {"visual_loops": {"hook": "Not an alias"}},
            {"challenges": {"cta": "No alias"}},
            {"challenges": {"reveal": "No alias"}},
            {"visual_drills": {"show_title": "true"}},
            {"longform": {"title": "Unsupported"}},
            {"visual_loops": {"fps": "60"}},
            {"visual_loops": {"title": 17}},
            {"visual_loops": {"title": "x" * 161}},
        ]
        for value_map in cases:
            with self.subTest(value_map=value_map):
                raw = {"schema": INPUT_SCHEMA_ID, "schema_version": "1.0", "values_by_content_type": value_map}
                with self.assertRaises((EditorialValueCarrierError, ValueError, TypeError)):
                    build_carrier(self.__class__.materialization_receipt, root=ROOT, overrides=value_map)

    def test_negative_receipt_mutations_fail_closed(self) -> None:
        mutations = [
            ("promote candidate input", lambda x: x.update(candidate_input_admissible=True)),
            ("claim visual consumption", lambda x: x["summary"].update(visual_payload_text_consumed=14)),
            ("claim payload mutation", lambda x: x["content_bindings"][0].update(payload_mutated=True)),
            ("inject values into payload", lambda x: x["content_bindings"][1].update(editorial_values_injected_into_visual_payload=True)),
            ("forge payload hash", lambda x: x["content_bindings"][0].update(payload_instance_sha256="0" * 64)),
            ("forge request hash", lambda x: x["content_bindings"][1].update(canonical_request_sha256="0" * 64)),
            ("forge field text", lambda x: x["content_bindings"][0]["fields"][0].update(value="Forged")),
            ("forge field digest", lambda x: x["content_bindings"][0]["fields"][0].update(value_sha256="0" * 64)),
            ("apply geometry", lambda x: x["content_bindings"][0]["fields"][0].update(layout_geometry={"x": 1, "y": 2})),
            ("apply visibility window", lambda x: x["content_bindings"][1]["fields"][0].update(visibility_window={"start": 0, "end": 1})),
            ("promote title role", lambda x: x["content_bindings"][1]["fields"][0].update(semantic_region_id="HEADER")),
            ("misclassify language", lambda x: x["content_bindings"][0]["fields"][3].update(field_kind="VISUAL_TEXT")),
            ("append unknown field", lambda x: x["content_bindings"][1]["fields"].append({"field_name": "hook"})),
            ("mutate receipt hash", lambda x: x.update(carrier_sha256="0" * 64)),
        ]
        for label, mutate in mutations:
            with self.subTest(label=label):
                changed = copy.deepcopy(self.__class__.carrier)
                mutate(changed)
                with self.assertRaises((EditorialValueCarrierError, ValueError, TypeError, KeyError)):
                    validate_carrier(changed, self.__class__.materialization_receipt, root=ROOT)

    def test_materialization_receipt_must_be_hash_valid_and_not_render_ready(self) -> None:
        for mutate in (
            lambda x: x.update(candidate_input_admissible=True),
            lambda x: x["content_bindings"][0].update(payload_instance_sha256="0" * 64),
            lambda x: x["execution_boundary"].update(renderer_native_input_emitted=True),
            lambda x: x["readiness"].update(video_render_ready=True),
        ):
            with self.subTest(mutation=mutate):
                receipt = copy.deepcopy(self.__class__.materialization_receipt)
                mutate(receipt)
                with self.assertRaises((EditorialValueCarrierError, ValueError, TypeError, KeyError)):
                    build_carrier(receipt, root=ROOT)

    def test_runner_is_console_only_and_has_no_dispatch_or_write_path(self) -> None:
        source = (HERE / "d_renderer_request_scoped_editorial_value_carrier.py").read_text(encoding="utf-8")
        self.assertNotIn("write_text(", source)
        self.assertNotIn("write_bytes(", source)
        self.assertNotIn("FileAccess.WRITE", source)
        self.assertNotIn("MovieWriter", source)
        self.assertNotIn("render_video", source)
        self.assertIn("run_materialization_review", source)
        self.assertIn("renderer_native_input_emitted", source)


def main() -> int:
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(RequestScopedEditorialValueCarrierTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():
        return 1
    print(
        "C11-D REQUEST-SCOPED EDITORIAL VALUE CARRIER CONTRACT PASS"
        " | tests=9/9 | canonical_values=14/14 | hash_bound_sidecar=14/14"
        " | visual_payload_consumed=0/14 | renderer_input=NOT_EMITTED | renderer=OFF"
        " | media_created=false | D4.8=BLOCKED | release_authority=NONE"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
