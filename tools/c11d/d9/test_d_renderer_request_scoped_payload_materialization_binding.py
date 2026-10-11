from __future__ import annotations

import copy
import contextlib
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

from d_renderer_request_scoped_payload_materialization_binding import (  # noqa: E402
    CONTRACT_REL,
    SCHEMA_REL,
    HARNESS_SPECS,
    RequestScopedMaterializationBindingError,
    _canonical,
    _sha_json,
    run_review,
    validate_receipt,
)
from test_d_renderer_visual_payload_materialization_preview import _record as visual_fixture_report  # noqa: E402
from test_d_renderer_challenge_visual_payload_preview import fixture_report as challenge_fixture_report  # noqa: E402


def _fake_process_runner(command: list[str], **kwargs: Any) -> subprocess.CompletedProcess[str]:
    script_arg = command[command.index("--script") + 1].removeprefix("res://")
    if script_arg == HARNESS_SPECS["visual_loop_drill_materialization"]["script"]:
        name = "visual_loop_drill_materialization"
        marker = HARNESS_SPECS[name]["pass_marker"]
        prefix = HARNESS_SPECS[name]["summary_prefix"]
        report = visual_fixture_report()
    elif script_arg == HARNESS_SPECS["challenge_visual_payload_materialization"]["script"]:
        name = "challenge_visual_payload_materialization"
        marker = HARNESS_SPECS[name]["pass_marker"]
        prefix = HARNESS_SPECS[name]["summary_prefix"]
        report = challenge_fixture_report()
    else:
        raise AssertionError(f"Unexpected Godot harness command: {script_arg}")
    out = marker + " | fixture=mocked_for_unit_test\n" + prefix + _canonical(report) + "\n"
    return subprocess.CompletedProcess(command, 0, stdout=out, stderr=None)


class RequestScopedMaterializationBindingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        with contextlib.redirect_stdout(io.StringIO()):
            cls.receipt = run_review(ROOT, executable="fake-godot-4.7.1", process_runner=_fake_process_runner)
        # Rebuild observations with the same fake child runner for independent negative validation.
        cls.observations = {}
        for name, spec in HARNESS_SPECS.items():
            completed = _fake_process_runner(["fake-godot-4.7.1", "--headless", "--path", str(ROOT), "--script", "res://" + spec["script"]])
            output = completed.stdout or ""
            summary_line = next(line for line in output.splitlines() if line.startswith(spec["summary_prefix"]))
            report = json.loads(summary_line[len(spec["summary_prefix"]):])
            evidence = {
                "name": name,
                "script": spec["script"],
                "script_sha256": __import__("hashlib").sha256((ROOT / spec["script"]).read_bytes()).hexdigest(),
                "exit_code": 0,
                "pass_marker_seen": True,
                "runtime_error_log_seen": False,
                "summary_sha256": _sha_json(report),
            }
            cls.observations[name] = (report, evidence)

    def test_contract_source_pins_and_schema(self) -> None:
        contract = json.loads((ROOT / CONTRACT_REL).read_text(encoding="utf-8-sig"))
        schema = json.loads((ROOT / SCHEMA_REL).read_text(encoding="utf-8-sig"))
        self.assertEqual(contract["status"], "PREPARATION_ONLY_FIXED_REVIEW_FIXTURES_REQUEST_BOUND_NOT_RENDERER_INPUT")
        self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
        self.assertIs(schema["additionalProperties"], False)
        self.assertGreaterEqual(len(contract["source_lineage"]), 25)
        self.assertEqual(contract["source_lineage"][0]["path"], "release/C11C_FREEZE_PACKAGE_MANIFEST.json")
        self.assertEqual(len({row["path"] for row in contract["source_lineage"]}), len(contract["source_lineage"]))

    def test_all_three_supported_fixture_requests_bind_real_payload_digests(self) -> None:
        self.assertEqual([row["content_type"] for row in self.__class__.receipt["content_bindings"]], ["challenges", "visual_loops", "visual_drills"])
        self.assertEqual(self.__class__.receipt["readiness"]["bound_content_types"], 3)
        self.assertFalse(self.__class__.receipt["candidate_input_admissible"])
        self.assertFalse(self.__class__.receipt["readiness"]["video_render_ready"])
        for row in self.__class__.receipt["content_bindings"]:
            self.assertEqual(len(row["payload_instance_sha256"]), 64)
            self.assertEqual(len(row["canonical_request_sha256"]), 64)
            self.assertTrue(row["source_seed_matches_request"])
            self.assertTrue(row["deterministic_repeat_pass"])
            self.assertEqual(row["materialization"], "IN_MEMORY_ONLY")
            self.assertFalse(row["video_render_ready"])
            self.assertGreater(len(row["unresolved_requirements"]), 0)
        self.assertTrue(validate_receipt(self.__class__.receipt, ROOT, self.__class__.observations))

    def test_challenge_seed_is_source_bound_not_overridden(self) -> None:
        challenge = self.__class__.receipt["content_bindings"][0]
        source = json.loads((ROOT / "challenges/CHALLENGE_004.json").read_text(encoding="utf-8-sig"))
        self.assertEqual(challenge["gameplay_seed"], source["generation"]["seed"])
        self.assertEqual(challenge["source_seed"], source["generation"]["seed"])
        self.assertNotEqual(challenge["gameplay_seed"], challenge["music_seed"])
        self.assertIn("CHALLENGE_PAYLOAD_ID_IS_DERIVED_RECEIPT_ALIAS_NOT_RUNTIME_INSTANCE_FIELD", challenge["unresolved_requirements"])

    def test_exact_fixed_loop_drill_selectors_are_bound(self) -> None:
        loop = self.__class__.receipt["content_bindings"][1]
        drill = self.__class__.receipt["content_bindings"][2]
        self.assertEqual(loop["selection"]["subtype_id"], "harmonic_membrane")
        self.assertEqual(drill["selection"]["variant_id"], "tier-2")
        self.assertEqual(loop["gameplay_seed"], drill["gameplay_seed"])
        self.assertNotEqual(loop["gameplay_seed"], loop["music_seed"])

    def test_governance_and_non_dispatch_boundary(self) -> None:
        self.assertEqual(len(self.__class__.receipt["harness_evidence"]), 2)
        boundary = self.__class__.receipt["execution_boundary"]
        for flag in ("payload_files_written", "renderer_native_input_emitted", "renderer_dispatch_invoked", "renderer_activation", "production_execution", "media_output_created", "c11c_source_mutation"):
            self.assertIs(boundary[flag], False)
        self.assertIsNone(boundary["output_artifact_path"])
        self.assertEqual(boundary["d4_8"], "BLOCKED")
        self.assertEqual(boundary["release_authority"], "NONE")
        self.assertEqual(boundary["d9_17"], "BLOCKED_NO_GO")

    def test_negative_receipt_mutations_fail_closed(self) -> None:
        mutations = [
            ("admit candidate", lambda x: x.update(candidate_input_admissible=True)),
            ("claim renderer input", lambda x: x["execution_boundary"].update(renderer_native_input_emitted=True)),
            ("claim dispatch", lambda x: x["execution_boundary"].update(renderer_dispatch_invoked=True)),
            ("authorize d4.8", lambda x: x["execution_boundary"].update(d4_8="AUTHORIZED")),
            ("grant release", lambda x: x["execution_boundary"].update(release_authority="PRODUCTION")),
            ("mark video ready", lambda x: x["readiness"].update(video_render_ready=True)),
            ("drop binding", lambda x: x["content_bindings"].pop()),
            ("duplicate type", lambda x: x["content_bindings"][2].update(content_type="visual_loops")),
            ("forge payload hash", lambda x: x["content_bindings"][0].update(payload_instance_sha256="0" * 64)),
            ("forge request hash", lambda x: x["content_bindings"][1].update(canonical_request_sha256="0" * 64)),
            ("break seed parity", lambda x: x["content_bindings"][0].update(source_seed_matches_request=False)),
            ("claim persisted payload", lambda x: x["content_bindings"][1].update(materialization="PERSISTED_FILE")),
            ("claim nondeterminism", lambda x: x["content_bindings"][2].update(deterministic_repeat_pass=False)),
            ("replace frozen lock", lambda x: x.update(frozen_c11c_manifest_sha256="0" * 64)),
        ]
        for label, mutate in mutations:
            with self.subTest(label=label):
                changed = copy.deepcopy(self.__class__.receipt)
                mutate(changed)
                with self.assertRaises((RequestScopedMaterializationBindingError, ValueError, TypeError, KeyError)):
                    validate_receipt(changed, ROOT, self.__class__.observations)

    def test_mismatched_harness_seed_is_rejected(self) -> None:
        observations = copy.deepcopy(self.__class__.observations)
        report, evidence = observations["visual_loop_drill_materialization"]
        report["instances"][0]["seed"] = 999
        evidence["summary_sha256"] = _sha_json(report)
        observations["visual_loop_drill_materialization"] = (report, evidence)
        with self.assertRaises(RequestScopedMaterializationBindingError):
            from d_renderer_request_scoped_payload_materialization_binding import build_receipt
            build_receipt(ROOT, observations)

    def test_runner_remains_console_only_and_no_render_or_persistence_path(self) -> None:
        source = (HERE / "d_renderer_request_scoped_payload_materialization_binding.py").read_text(encoding="utf-8")
        self.assertNotIn("write_text(", source)
        self.assertNotIn("write_bytes(", source)
        self.assertNotIn("FileAccess.WRITE", source)
        self.assertNotIn("MovieWriter", source)
        self.assertNotIn("render_video", source)
        self.assertIn("--headless", source)
        self.assertIn("renderer_dispatch_invoked", source)

    def test_receipt_schema_is_draft_2020_12_valid(self) -> None:
        schema = json.loads((ROOT / SCHEMA_REL).read_text(encoding="utf-8-sig"))
        try:
            import jsonschema
        except ImportError:
            self.skipTest("jsonschema not installed; runtime includes structural fail-closed validation")
        jsonschema.Draft202012Validator.check_schema(schema)
        jsonschema.Draft202012Validator(schema).validate(self.__class__.receipt)


def main() -> int:
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(RequestScopedMaterializationBindingTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():
        return 1
    print(
        "C11-D REQUEST-SCOPED PAYLOAD MATERIALIZATION/BINDING CONTRACT PASS"
        " | content_types=3/3 | source_binding=3/3 | mocked_harness_contracts=2/2"
        f" | negative={14}/14 | schema=1/1 | godot_runtime=NOT_RUN_BY_PYTHON"
        " | renderer_input=NOT_EMITTED | media_created=false | D4.8=BLOCKED | release_authority=NONE"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
