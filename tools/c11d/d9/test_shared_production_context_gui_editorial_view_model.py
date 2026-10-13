from __future__ import annotations

import copy
import hashlib
import io
import json
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
D9 = ROOT / "tools" / "c11d" / "d9"
if str(D9) not in sys.path:
    sys.path.insert(0, str(D9))

import shared_production_context_gui_editorial_draft as draft
import shared_production_context_gui_editorial_view_model as vm
from shared_production_context_gui_reactive_selection import (
    initialize_gui_reactive_selection_state,
    transition_gui_reactive_selection_state,
)
from shared_production_context_gui_state import build_canonical_request_from_gui_state


def selected_snapshot(content_type: str, mode: str = "REVIEW") -> dict:
    snapshot = initialize_gui_reactive_selection_state(mode=mode, project_root=ROOT)
    snapshot = transition_gui_reactive_selection_state(
        snapshot["state"], {"action": "select_content_type", "content_type": content_type}, ROOT
    )
    families = snapshot["available"]["families"]
    if not families:
        return snapshot
    family = families[0]
    snapshot = transition_gui_reactive_selection_state(
        snapshot["state"], {"action": "select_family", "family_id": family["id"]}, ROOT
    )
    selectors = snapshot["available"]["selectors"]
    concrete = [row for row in selectors if row.get("concrete_variant") is True]
    if not concrete:
        concrete = [row for row in selectors if row.get("selection_mode") is False]
    if not concrete:
        raise AssertionError(f"No concrete selector for {content_type}/{family['id']}")
    snapshot = transition_gui_reactive_selection_state(
        snapshot["state"], {"action": "select_selector", "selector_id": concrete[0]["id"]}, ROOT
    )
    return snapshot


def make_inputs(content_type: str) -> tuple[dict, dict]:
    snapshot = selected_snapshot(content_type)
    draft_state = draft.initialize_gui_editorial_draft_state(
        snapshot,
        {"global": {"title": "Profile inherited title", "subtitle": "Profile inherited subtitle"}},
        ROOT,
    )
    binding = draft_state["selection_binding"]
    selector_field = binding["selector_field"]
    selection = {
        "content_type": content_type,
        "family_id": binding["family_id"],
        selector_field: binding["selector_id"],
    }
    draft_state = draft.set_gui_editorial_draft_override(draft_state, "title", f"GUI draft {content_type}", ROOT)
    draft_state = draft.set_gui_editorial_draft_override(draft_state, "call_to_action", "Continue", ROOT)
    if content_type == "challenges":
        draft_state = draft.set_gui_editorial_draft_override(draft_state, "player_name", "Ada", ROOT)
        draft_state = draft.set_gui_editorial_draft_override(draft_state, "challenge_label", "Find the key", ROOT)
    # These stale values intentionally prove the shared draft is the explicit editorial source.
    gui_state = {
        "schema": "C11-D-SHARED-GUI-PRODUCTION-STATE-V1",
        "schema_version": "1.0",
        "request_id": f"GUI-EDITORIAL-VM-{content_type.upper()}",
        "mode": "REVIEW",
        "selection": selection,
        "production": {
            "seed": 12345,
            "music_seed": 840001,
            "delivery_profile_id": "REVIEW_720",
            "presentation_profile_id": "social_default_v1",
            "variation_index": 0,
            "audio_enabled": True,
            "personalization_enabled": True,
        },
        "editorial": {"profile": {}, "overrides": {"title": "STALE-UI-COPY"}},
    }
    return gui_state, draft_state


class GUIEditorialViewModelTests(unittest.TestCase):
    def test_parent_contract_source_pins_and_governance(self):
        report = vm.audit_gui_editorial_view_model_contract(ROOT)
        self.assertGreaterEqual(report["source_pins"], 25)
        self.assertEqual(report["supported_content_types"], 3)
        self.assertFalse(report["media_created"])
        self.assertEqual(report["d4_8"], "BLOCKED")
        self.assertEqual(report["release_authority"], "NONE")

    def test_all_three_types_resolve_draft_to_same_canonical_gui_and_cli_context(self):
        counts = {}
        for content_type in ("challenges", "visual_loops", "visual_drills"):
            gui_state, draft_state = make_inputs(content_type)
            gui_before = copy.deepcopy(gui_state)
            draft_before = copy.deepcopy(draft_state)
            model = vm.build_gui_editorial_view_model(gui_state, draft_state, ROOT)
            self.assertEqual(gui_state, gui_before)
            self.assertEqual(draft_state, draft_before)
            self.assertEqual(model["identity"]["content_type"], content_type)
            self.assertEqual(model["editorial"]["effective_values"]["title"], f"GUI draft {content_type}")
            self.assertEqual(model["editorial"]["effective_values"]["subtitle"], "Profile inherited subtitle")
            self.assertNotEqual(model["canonical_request_preview"]["production_override"].get("title"), "STALE-UI-COPY")
            self.assertEqual(model["canonical_request_preview"]["production_override"], draft_state["overrides"])
            self.assertEqual(model["canonical_request_preview"]["editorial_profile"], draft_state["profile"])
            self.assertFalse(model["readiness"]["renderer_input_admissible"])
            self.assertFalse(model["readiness"]["render_ready"])
            self.assertFalse(model["execution_boundary"]["media_created"])
            self.assertFalse(model["execution_boundary"]["renderer_native_input_emitted"])
            self.assertEqual(model["identity"]["request_sha256"], model["shared_context_record"]["identity"]["request_sha256"])
            self.assertTrue(model["controls"]["family_options"])
            self.assertTrue(model["controls"]["selector_options"])
            if content_type == "challenges":
                self.assertIn("player_name", model["editorial"]["active_fields"])
                self.assertEqual(model["editorial"]["effective_values"]["player_name"], "Ada")
                self.assertTrue(model["selection"]["request_plan_compatible"])
            else:
                self.assertNotIn("player_name", model["editorial"]["effective_values"])
                self.assertFalse(model["selection"]["request_plan_compatible"])
            counts[content_type] = 1
        self.assertEqual(counts, {"challenges": 1, "visual_loops": 1, "visual_drills": 1})

    def test_cli_emits_exact_ascii_safe_view_model_for_all_types(self):
        # Exercise the actual CLI entry point without spawning repeated child
        # processes; the input-file/argparse/ASCII-stdout path is identical.
        # A separate Windows acceptance block can invoke the script as a process.
        for content_type in ("challenges", "visual_loops", "visual_drills"):
            gui_state, draft_state = make_inputs(content_type)
            with tempfile.TemporaryDirectory(prefix="c11d_editorial_vm_cli_") as folder:
                folder_path = Path(folder)
                gui_file = folder_path / "gui-state.json"
                draft_file = folder_path / "editorial-draft.json"
                gui_file.write_text(json.dumps(gui_state, ensure_ascii=True), encoding="utf-8")
                draft_file.write_text(json.dumps(draft_state, ensure_ascii=True), encoding="utf-8")
                stdout = io.StringIO()
                with redirect_stdout(stdout):
                    code = vm.main([
                        "--project-root", str(ROOT), "--inputs",
                        "--gui-state", str(gui_file),
                        "--editorial-draft", str(draft_file),
                    ])
                encoded = stdout.getvalue()
                self.assertEqual(code, 0, encoded)
                self.assertEqual(encoded.encode("ascii").decode("ascii"), encoded)
                actual = json.loads(encoded)
                self.assertEqual(actual["identity"]["content_type"], content_type)
                self.assertEqual(actual["editorial"]["effective_values"]["title"], f"GUI draft {content_type}")
                self.assertEqual(actual["identity"]["request_sha256"], actual["shared_context_record"]["identity"]["request_sha256"])
                self.assertFalse(actual["readiness"]["render_ready"])
                self.assertFalse(actual["execution_boundary"]["renderer_native_input_emitted"])
                self.assertEqual(
                    sorted(path.name for path in folder_path.iterdir()),
                    ["editorial-draft.json", "gui-state.json"],
                )

    def test_selection_mismatch_and_incomplete_draft_fail_closed(self):
        gui_state, draft_state = make_inputs("challenges")
        altered = copy.deepcopy(gui_state)
        altered["selection"]["family_id"] = "not-the-draft-family"
        with self.assertRaises(vm.SharedProductionGUIEditorialViewModelError):
            vm.build_gui_editorial_view_model(altered, draft_state, ROOT)

        incomplete_snapshot = initialize_gui_reactive_selection_state(project_root=ROOT)
        incomplete_draft = draft.initialize_gui_editorial_draft_state(incomplete_snapshot, project_root=ROOT)
        blank_gui = copy.deepcopy(gui_state)
        with self.assertRaises(vm.SharedProductionGUIEditorialViewModelError):
            vm.build_gui_editorial_view_model(blank_gui, incomplete_draft, ROOT)

    def test_loop_and_drill_production_modes_are_rejected_by_canonical_catalog_gate(self):
        for content_type in ("visual_loops", "visual_drills"):
            gui_state, draft_state = make_inputs(content_type)
            gui_state = copy.deepcopy(gui_state)
            gui_state["mode"] = "PRODUCTION"
            draft_without_hash = {k: copy.deepcopy(v) for k, v in draft_state.items() if k != "state_sha256"}
            draft_without_hash["selection_binding"]["mode"] = "PRODUCTION"
            draft_state = draft._seal_state(draft_without_hash)
            with self.subTest(content_type=content_type):
                with self.assertRaises(vm.SharedProductionGUIEditorialViewModelError):
                    vm.build_gui_editorial_view_model(gui_state, draft_state, ROOT)

    def test_override_change_updates_canonical_identity_without_changing_seed_domains(self):
        gui_state, draft_state = make_inputs("visual_drills")
        first = vm.build_gui_editorial_view_model(gui_state, draft_state, ROOT)
        changed_draft = draft.set_gui_editorial_draft_override(draft_state, "title", "Changed title", ROOT)
        second = vm.build_gui_editorial_view_model(gui_state, changed_draft, ROOT)
        self.assertNotEqual(first["identity"]["request_sha256"], second["identity"]["request_sha256"])
        self.assertNotEqual(first["identity"]["editorial_sha256"], second["identity"]["editorial_sha256"])
        self.assertEqual(first["controls"]["production"]["seed"], second["controls"]["production"]["seed"])
        self.assertEqual(first["controls"]["production"]["music_seed"], second["controls"]["production"]["music_seed"])
        self.assertEqual(first["shared_context_record"]["shared_context_binding"]["presentation_binding"],
                         second["shared_context_record"]["shared_context_binding"]["presentation_binding"])

    def test_view_model_hash_and_schema_detect_tampering(self):
        gui_state, draft_state = make_inputs("visual_loops")
        model = vm.build_gui_editorial_view_model(gui_state, draft_state, ROOT)
        tampered = copy.deepcopy(model)
        tampered["editorial"]["effective_values"]["title"] = "Tampered"
        with self.assertRaises(Exception):
            vm.validate_gui_editorial_view_model(tampered, gui_state, draft_state, ROOT)

    def test_source_drift_fails_closed_on_minimal_source_mirror(self):
        contract = json.loads((ROOT / vm.CONTRACT_REL).read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory(prefix="c11d_editorial_vm_drift_") as folder:
            mirror = Path(folder)
            for row in contract["source_lineage"]:
                source = ROOT / row["path"]
                target = mirror / row["path"]
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source, target)
            target = mirror / "tools/c11d/d9/shared_production_context_gui_state.py"
            target.write_bytes(target.read_bytes() + b"\n# test-only source drift\n")
            with self.assertRaises(vm.SharedProductionGUIEditorialViewModelError):
                vm.audit_gui_editorial_view_model_contract(mirror)


if __name__ == "__main__":
    unittest.main(verbosity=2)
