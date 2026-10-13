from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import shared_production_context_gui_editorial_draft as draft
from shared_production_context_gui_reactive_selection import (
    initialize_gui_reactive_selection_state,
    transition_gui_reactive_selection_state,
)


def selected_snapshot(content_type: str, mode: str = 'REVIEW') -> dict:
    snapshot = initialize_gui_reactive_selection_state(mode=mode, project_root=ROOT)
    snapshot = transition_gui_reactive_selection_state(
        snapshot['state'], {'action': 'select_content_type', 'content_type': content_type}, ROOT
    )
    if snapshot['available']['families']:
        family = snapshot['available']['families'][0]
        snapshot = transition_gui_reactive_selection_state(
            snapshot['state'], {'action': 'select_family', 'family_id': family['id']}, ROOT
        )
        concrete = [row for row in snapshot['available']['selectors'] if row.get('concrete_variant') is True]
        if not concrete:
            concrete = [row for row in snapshot['available']['selectors'] if row.get('selection_mode') is False]
        if not concrete:
            raise AssertionError(f'No selectable concrete selector for {content_type}/{family["id"]}')
        snapshot = transition_gui_reactive_selection_state(
            snapshot['state'], {'action': 'select_selector', 'selector_id': concrete[0]['id']}, ROOT
        )
    return snapshot


def next_snapshot(snapshot: dict, action: str, **kwargs) -> dict:
    return transition_gui_reactive_selection_state(
        snapshot['state'], {'action': action, **kwargs}, ROOT
    )


class GUIEditorialDraftLifecycleTests(unittest.TestCase):
    def test_contract_source_pins_and_schemas(self):
        report = draft.audit_gui_editorial_draft_contract(ROOT)
        self.assertEqual(report['source_pins'], 10)
        self.assertEqual(report['parent_reactive_selection_source_pins'], 9)
        self.assertFalse(report['media_created'])
        self.assertEqual(report['release_authority'], 'NONE')

    def test_incomplete_selection_does_not_resolve_editorial_values(self):
        snapshot = initialize_gui_reactive_selection_state(project_root=ROOT)
        state = draft.initialize_gui_editorial_draft_state(snapshot, project_root=ROOT)
        preview = draft.preview_gui_editorial_draft(state, ROOT)
        self.assertEqual(preview['status'], 'SELECTION_INCOMPLETE')
        self.assertIsNone(preview['effective_values'])
        self.assertEqual(preview['active_fields'], [])
        self.assertFalse(preview['execution_boundary']['canonical_production_request_created'])

    def test_common_overrides_survive_content_family_and_selector_transitions(self):
        snapshot = selected_snapshot('visual_loops')
        state = draft.initialize_gui_editorial_draft_state(snapshot, project_root=ROOT)
        for field, value in [('title', ' Shared title '), ('subtitle', 'Shared subtitle'),
                             ('call_to_action', 'Explore more'), ('language', 'ES')]:
            state = draft.set_gui_editorial_draft_override(state, field, value, ROOT)
        first_families = snapshot['available']['families']
        if len(first_families) > 1:
            alternate = next(row for row in first_families if row['id'] != snapshot['state']['selection']['family_id'])
            snapshot = next_snapshot(snapshot, 'select_family', family_id=alternate['id'])
            state = draft.transition_gui_editorial_draft_state(state, snapshot, ROOT)
            self.assertEqual(state['overrides']['title'], ' Shared title ')
            self.assertEqual(state['overrides']['subtitle'], 'Shared subtitle')
            self.assertEqual(state['overrides']['call_to_action'], 'Explore more')
            self.assertEqual(state['overrides']['language'], 'ES')
            selector = next(row for row in snapshot['available']['selectors'] if row.get('concrete_variant') is True)
            snapshot = next_snapshot(snapshot, 'select_selector', selector_id=selector['id'])
            state = draft.transition_gui_editorial_draft_state(state, snapshot, ROOT)
            self.assertEqual(state['overrides']['title'], ' Shared title ')
        else:
            self.assertTrue(state['overrides'])

    def test_challenge_only_overrides_exist_only_for_challenges(self):
        snapshot = selected_snapshot('challenges')
        state = draft.initialize_gui_editorial_draft_state(snapshot, project_root=ROOT)
        state = draft.set_gui_editorial_draft_override(state, 'player_name', 'Ada', ROOT)
        state = draft.set_gui_editorial_draft_override(state, 'challenge_label', 'Find the key', ROOT)
        preview = draft.preview_gui_editorial_draft(state, ROOT)
        self.assertIn('player_name', preview['active_fields'])
        self.assertIn('challenge_label', preview['active_fields'])
        self.assertEqual(preview['effective_values']['player_name'], 'Ada')

    def test_type_switch_preserves_shared_and_drops_challenge_only_overrides(self):
        snapshot = selected_snapshot('challenges')
        state = draft.initialize_gui_editorial_draft_state(snapshot, project_root=ROOT)
        state = draft.set_gui_editorial_draft_override(state, 'title', 'Persistent', ROOT)
        state = draft.set_gui_editorial_draft_override(state, 'player_name', 'Ada', ROOT)
        loop_snapshot = next_snapshot(snapshot, 'select_content_type', content_type='visual_loops')
        state = draft.transition_gui_editorial_draft_state(state, loop_snapshot, ROOT)
        self.assertEqual(state['overrides'], {'title': 'Persistent'})
        self.assertNotIn('player_name', state['overrides'])
        self.assertNotIn('challenge_label', state['overrides'])

    def test_challenge_only_overrides_are_not_restored_when_returning_to_challenges(self):
        challenge_snapshot = selected_snapshot('challenges')
        state = draft.initialize_gui_editorial_draft_state(challenge_snapshot, project_root=ROOT)
        state = draft.set_gui_editorial_draft_override(state, 'player_name', 'Ada', ROOT)
        loop_snapshot = next_snapshot(challenge_snapshot, 'select_content_type', content_type='visual_loops')
        state = draft.transition_gui_editorial_draft_state(state, loop_snapshot, ROOT)
        challenge_again = next_snapshot(loop_snapshot, 'select_content_type', content_type='challenges')
        state = draft.transition_gui_editorial_draft_state(state, challenge_again, ROOT)
        self.assertNotIn('player_name', state['overrides'])
        self.assertNotIn('challenge_label', state['overrides'])

    def test_challenge_only_edit_rejected_for_visual_loop(self):
        state = draft.initialize_gui_editorial_draft_state(selected_snapshot('visual_loops'), project_root=ROOT)
        with self.assertRaises(draft.SharedProductionGUIEditorialDraftError):
            draft.set_gui_editorial_draft_override(state, 'player_name', 'Not allowed', ROOT)

    def test_clear_override_inherits_profile_value(self):
        snapshot = selected_snapshot('challenges')
        profile = {'global': {'title': 'Profile title', 'subtitle': 'Profile subtitle'}}
        state = draft.initialize_gui_editorial_draft_state(snapshot, profile, ROOT)
        state = draft.set_gui_editorial_draft_override(state, 'title', 'Draft title', ROOT)
        preview = draft.preview_gui_editorial_draft(state, ROOT)
        self.assertEqual(preview['effective_values']['title'], 'Draft title')
        state = draft.clear_gui_editorial_draft_override(state, 'title', ROOT)
        preview = draft.preview_gui_editorial_draft(state, ROOT)
        self.assertEqual(preview['effective_values']['title'], 'Profile title')

    def test_empty_override_uses_canonical_unknown_not_profile_fallback(self):
        snapshot = selected_snapshot('challenges')
        state = draft.initialize_gui_editorial_draft_state(snapshot, {'global': {'title': 'Profile title'}}, ROOT)
        state = draft.set_gui_editorial_draft_override(state, 'title', '', ROOT)
        preview = draft.preview_gui_editorial_draft(state, ROOT)
        self.assertEqual(preview['effective_values']['title'], 'UNKNOWN')

    def test_reserved_unknown_and_overlong_fields_rejected(self):
        state = draft.initialize_gui_editorial_draft_state(selected_snapshot('visual_drills'), project_root=ROOT)
        with self.assertRaises(draft.SharedProductionGUIEditorialDraftError):
            draft.set_gui_editorial_draft_override(state, 'hook', 'disabled', ROOT)
        with self.assertRaises(draft.SharedProductionGUIEditorialDraftError):
            draft.set_gui_editorial_draft_override(state, 'fps', '30', ROOT)
        with self.assertRaises(draft.SharedProductionGUIEditorialDraftError):
            draft.set_gui_editorial_draft_override(state, 'title', 'x' * 161, ROOT)
        with self.assertRaises(draft.SharedProductionGUIEditorialDraftError):
            draft.set_gui_editorial_draft_override(state, 'language', 'x' * 33, ROOT)

    def test_draft_hash_detects_tampering(self):
        state = draft.initialize_gui_editorial_draft_state(selected_snapshot('challenges'), project_root=ROOT)
        tampered = copy.deepcopy(state)
        tampered['overrides']['title'] = 'Tampered'
        with self.assertRaises(draft.SharedProductionGUIEditorialDraftError):
            draft.preview_gui_editorial_draft(tampered, ROOT)

    def test_challenge_fields_in_nonchallenge_state_rejected_by_schema_and_validator(self):
        state = draft.initialize_gui_editorial_draft_state(selected_snapshot('visual_loops'), project_root=ROOT)
        tampered = copy.deepcopy(state)
        tampered.pop('state_sha256')
        tampered['overrides']['player_name'] = 'Stale challenge value'
        tampered['state_sha256'] = draft.canonical_sha256(tampered)
        with self.assertRaises(draft.SharedProductionGUIEditorialDraftError):
            draft.preview_gui_editorial_draft(tampered, ROOT)

    def test_stale_snapshot_hash_rejected(self):
        snapshot = selected_snapshot('challenges')
        tampered = copy.deepcopy(snapshot)
        tampered['identity']['snapshot_sha256'] = '0' * 64
        with self.assertRaises(draft.SharedProductionGUIEditorialDraftError):
            draft.initialize_gui_editorial_draft_state(tampered, project_root=ROOT)

    def test_catalog_change_requires_explicit_refresh(self):
        snapshot = selected_snapshot('challenges')
        state = draft.initialize_gui_editorial_draft_state(snapshot, project_root=ROOT)
        altered = copy.deepcopy(state)
        altered.pop('state_sha256')
        altered['selection_binding']['catalog_sha256'] = '0' * 64
        altered['state_sha256'] = draft.canonical_sha256(altered)
        with self.assertRaises(draft.SharedProductionGUIEditorialDraftError):
            draft.transition_gui_editorial_draft_state(altered, snapshot, ROOT)

    def test_cli_audit_emits_machine_readable_ascii_json(self):
        proc = subprocess.run(
            [sys.executable, '-B', str(HERE / 'shared_production_context_gui_editorial_draft.py'), '--audit-only', '--project-root', str(ROOT)],
            cwd=ROOT, capture_output=True, timeout=90,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr.decode('utf-8', errors='replace'))
        self.assertTrue(proc.stdout)
        self.assertTrue(all(byte < 128 for byte in proc.stdout), 'CLI machine JSON must be ASCII-safe')
        payload = json.loads(proc.stdout.decode('ascii'))
        self.assertEqual(payload['result'], 'PASS')
        self.assertEqual(payload['audit']['source_pins'], 10)

    def test_source_drift_fails_closed_and_restores_exact_bytes(self):
        target = ROOT / 'tools/c11d/d9/universal_editorial_model.py'
        original = target.read_bytes()
        try:
            target.write_bytes(original + b'\n# temporary drift test\n')
            with self.assertRaises(draft.SharedProductionGUIEditorialDraftError):
                draft.audit_gui_editorial_draft_contract(ROOT)
        finally:
            target.write_bytes(original)
        self.assertEqual(target.read_bytes(), original)
        self.assertEqual(hashlib.sha256(target.read_bytes()).hexdigest(), '5c575be1942ba0613d66579d14db5cf9d7786e7062dfb001bd7be8a2e9c18ae5')


if __name__ == '__main__':
    unittest.main(verbosity=2)
