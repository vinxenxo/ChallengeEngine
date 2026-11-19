from __future__ import annotations
import copy
import hashlib
import unittest
from pathlib import Path
import sys

TOOLS_ROOT = Path(__file__).resolve().parents[1] / "tools" / "c11d" / "d9"
sys.path.insert(0, str(TOOLS_ROOT))
import c11e_e6_challenge_editorial_binding_prepare_only_v1 as binding

class ZeroWindowSemanticsTests(unittest.TestCase):
    def envelope(self, hook_frames: int, cta_frames: int):
        total = hook_frames + 240 + 60 + cta_frames
        phases = [
            {"phase":"HOOK","start_frame":0,"end_frame":hook_frames,"timebase":"SOURCE_FPS_HALF_OPEN"},
            {"phase":"GAME","start_frame":hook_frames,"end_frame":hook_frames+240,"timebase":"SOURCE_FPS_HALF_OPEN"},
            {"phase":"REVEAL","start_frame":hook_frames+240,"end_frame":hook_frames+300,"timebase":"SOURCE_FPS_HALF_OPEN"},
            {"phase":"CTA","start_frame":hook_frames+300,"end_frame":total,"timebase":"SOURCE_FPS_HALF_OPEN"},
        ]
        rows=[]
        windows=binding.EXPECTED_WINDOWS
        for name in binding.EXPECTED_FIELDS:
            ranges=[]
            for phase in windows[name]:
                source=next(p for p in phases if p['phase']==phase)
                ranges.append({"phase":phase,"start_frame":source['start_frame'],"end_frame":source['end_frame'],"timebase":"SOURCE_FPS_HALF_OPEN"})
            disposition = binding.OMITTED
            region=binding.EXPECTED_REGIONS[name]
            rows.append({
                "field":name,"region":region,"source_phase_windows":windows[name],
                "source_frame_ranges":ranges,"disposition":disposition,"effective_value":"",
                "value_sha256":binding.EMPTY_SHA256,"policy_sha256":"p"*64,"layout_contract_sha256":"l"*64,
            })
        return {
            "schema":"C11E-CHALLENGE-LIVE-EDITORIAL-ENVELOPE-V1",
            "status":"PREPARED_E1_NOT_DISPATCHED","content_type":"challenges",
            "source_timebase":{"fps":60,"total_frames":total},"source_phase_ranges":phases,
            "policy_sha256":"p"*64,"layout_contract_sha256":"l"*64,"fields":rows,
            "e1_intent":{"status":"PREPARED_E1_NOT_DISPATCHED","editorial":{"title":"UNKNOWN","subtitle":"UNKNOWN","call_to_action":"UNKNOWN"}},
            "intent_hash":"i"*64,
        }

    def values(self):
        return {"title":"E6 · DESAFÍO EN PRUEBA","subtitle":"RITMO Y PRECISIÓN EN PRUEBA","call_to_action":"PROBAR DESAFÍO"}

    def bind(self, hook, cta):
        return binding.bind_envelope(self.envelope(hook,cta), self.values(), "p"*64, "l"*64)

    def disposition(self, result, name):
        return next(x for x in result["fields"] if x["field"]==name)

    def test_01_zero_hook_suppresses_title_and_subtitle_without_fallback(self):
        result, summary=self.bind(0,120)
        self.assertEqual(self.disposition(result,"title")["disposition"],binding.OMITTED)
        self.assertEqual(self.disposition(result,"subtitle")["disposition"],binding.OMITTED)
        self.assertEqual(self.disposition(result,"call_to_action")["disposition"],binding.READY)
        self.assertEqual(self.disposition(result,"title")["source_phase_windows"],["HOOK"])
        self.assertEqual(summary["suppressed_zero_window_fields"],["title","subtitle"])

    def test_02_zero_cta_suppresses_cta_without_fallback(self):
        result, summary=self.bind(180,0)
        self.assertEqual(self.disposition(result,"title")["disposition"],binding.READY)
        self.assertEqual(self.disposition(result,"subtitle")["disposition"],binding.READY)
        self.assertEqual(self.disposition(result,"call_to_action")["disposition"],binding.OMITTED)
        self.assertEqual(self.disposition(result,"call_to_action")["source_phase_windows"],["CTA"])
        self.assertEqual(summary["suppressed_zero_window_fields"],["call_to_action"])

    def test_03_positive_hook_and_cta_bind_all_three(self):
        result, summary=self.bind(180,120)
        self.assertEqual(summary["visible_fields"],["title","subtitle","call_to_action"])
        self.assertEqual(summary["suppressed_zero_window_fields"],[])

    def test_04_zero_hook_and_cta_suppress_all_three(self):
        result, summary=self.bind(0,0)
        self.assertEqual(summary["visible_fields"],[])
        self.assertEqual(summary["suppressed_zero_window_fields"],["title","subtitle","call_to_action"])

    def test_05_zero_window_never_moves_into_game(self):
        result, _=self.bind(0,120)
        title=self.disposition(result,"title")
        self.assertEqual(title["source_phase_windows"],["HOOK"])
        self.assertEqual(title["source_frame_ranges"][0]["phase"],"HOOK")
        self.assertEqual(title["effective_value"],"")

    def test_06_zero_window_has_empty_value_hash(self):
        result, _=self.bind(0,0)
        for name in binding.RENDERABLE_FIELDS:
            row=self.disposition(result,name)
            if row["disposition"]==binding.OMITTED:
                self.assertEqual(row["effective_value"],"")
                self.assertEqual(row["value_sha256"],binding.EMPTY_SHA256)

    def test_07_positive_window_has_exact_fixture_hash(self):
        result, _=self.bind(180,120)
        for name,value in self.values().items():
            row=self.disposition(result,name)
            self.assertEqual(row["effective_value"],value)
            self.assertEqual(row["value_sha256"],hashlib.sha256(value.encode("utf-8")).hexdigest())

    def test_08_original_input_is_not_mutated(self):
        original=self.envelope(0,120)
        before=copy.deepcopy(original)
        binding.bind_envelope(original,self.values(),"p"*64,"l"*64)
        self.assertEqual(original,before)

    def test_09_e1_intent_unknown_values_are_preserved(self):
        result,_=self.bind(180,120)
        self.assertEqual(result["e1_intent"]["editorial"],{"title":"UNKNOWN","subtitle":"UNKNOWN","call_to_action":"UNKNOWN"})

    def test_10_player_and_challenge_identity_remain_nonvisual(self):
        result,_=self.bind(180,120)
        for name in ("player_name","challenge_label"):
            self.assertEqual(self.disposition(result,name)["disposition"],binding.OMITTED)

    def test_11_zero_width_interval_is_accepted_as_empty_not_invalid(self):
        result,summary=self.bind(0,120)
        phase=binding.phase_index(result)
        self.assertEqual(phase["HOOK"]["start_frame"],phase["HOOK"]["end_frame"])
        self.assertEqual(summary["hook_frames"],0)

    def test_12_negative_or_reversed_ranges_fail_closed(self):
        env=self.envelope(180,120)
        env["source_phase_ranges"][0]["end_frame"]=-1
        with self.assertRaises(binding.BindingError):
            binding.bind_envelope(env,self.values(),"p"*64,"l"*64)

    def test_13_policy_window_cannot_be_widened(self):
        env=self.envelope(180,120)
        next(x for x in env["fields"] if x["field"]=="title")["source_phase_windows"]=["HOOK","GAME"]
        with self.assertRaises(binding.BindingError):
            binding.bind_envelope(env,self.values(),"p"*64,"l"*64)

    def test_14_layout_and_policy_pins_are_mandatory(self):
        env=self.envelope(180,120)
        with self.assertRaises(binding.BindingError):
            binding.bind_envelope(env,self.values(),"x"*64,"l"*64)

    def test_15_only_challenge_envelopes_are_accepted(self):
        env=self.envelope(180,120)
        env["content_type"]="visual_loop"
        with self.assertRaises(binding.BindingError):
            binding.bind_envelope(env,self.values(),"p"*64,"l"*64)

    def test_16_only_exact_six_fields_are_accepted(self):
        env=self.envelope(180,120)
        env["fields"].pop()
        with self.assertRaises(binding.BindingError):
            binding.bind_envelope(env,self.values(),"p"*64,"l"*64)

    def test_17_duplicate_fields_fail_closed(self):
        env=self.envelope(180,120)
        env["fields"][-1]=copy.deepcopy(env["fields"][0])
        with self.assertRaises(binding.BindingError):
            binding.bind_envelope(env,self.values(),"p"*64,"l"*64)

    def test_18_fixture_values_must_be_nonempty(self):
        with self.assertRaises(binding.BindingError):
            binding.bind_envelope(self.envelope(180,120),{"title":"","subtitle":"S","call_to_action":"C"},"p"*64,"l"*64)

    def test_19_source_range_must_match_exact_phase(self):
        env=self.envelope(180,120)
        title=self.disposition(env,"title")
        title["source_frame_ranges"][0]["phase"]="GAME"
        with self.assertRaises(binding.BindingError):
            binding.bind_envelope(env,self.values(),"p"*64,"l"*64)

    def test_20_seed_isolation_A_B_repeat_C_music_changed(self):
        binding.validate_seed_isolation({"A":{"gameplay":314159,"music":840001},"B_REPEAT":{"gameplay":314159,"music":840001},"C_CHANGED_MUSIC_SEED":{"gameplay":314159,"music":840002}})

    def test_21_gameplay_seed_change_fails(self):
        with self.assertRaises(binding.BindingError):
            binding.validate_seed_isolation({"A":{"gameplay":314159,"music":840001},"B_REPEAT":{"gameplay":314160,"music":840001},"C_CHANGED_MUSIC_SEED":{"gameplay":314159,"music":840002}})

    def test_22_A_B_music_seed_change_fails(self):
        with self.assertRaises(binding.BindingError):
            binding.validate_seed_isolation({"A":{"gameplay":314159,"music":840001},"B_REPEAT":{"gameplay":314159,"music":840003},"C_CHANGED_MUSIC_SEED":{"gameplay":314159,"music":840002}})

    def test_23_C_music_seed_must_change(self):
        with self.assertRaises(binding.BindingError):
            binding.validate_seed_isolation({"A":{"gameplay":314159,"music":840001},"B_REPEAT":{"gameplay":314159,"music":840001},"C_CHANGED_MUSIC_SEED":{"gameplay":314159,"music":840001}})

    def test_24_no_release_or_renderer_authority_in_module(self):
        source=Path(binding.__file__).read_text(encoding="utf-8")
        self.assertIn('governance["renderer"] != "OFF"',source)
        self.assertIn('governance["release_authority"] != "NONE"',source)
        self.assertIn('"batch_id_consumed":False',source)

if __name__ == "__main__":
    unittest.main(verbosity=2)
