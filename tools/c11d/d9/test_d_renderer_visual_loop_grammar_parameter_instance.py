from __future__ import annotations
import base64, copy, hashlib, json, math, shutil, tempfile, unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock
import sys
ROOT=Path(__file__).resolve().parents[3]
TOOL_DIR=Path(__file__).resolve().parent
sys.path.insert(0,str(TOOL_DIR))
import d_renderer_visual_loop_grammar_parameter_instance as audit

class GrammarParameterInstanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract,cls.contract_schema,cls.input_schema,cls.output_schema,cls.lineage=audit.load_contract(ROOT)

    def _style(self, seed):
        # Deterministic mocked style evidence: seed affects visible style, metadata does not.
        base=float(seed%7)/10.0
        return {
            "grammar_mode":0,"palette_mode":int(seed%5),"morph":base,"wave_frequency":5.0+base,
            "line_width":0.01+base,"glow_strength":base,"polygon_sides":5.0+float(seed%4),
            "wave_ratio":min(0.6+base,1.05),"shape_rotation":base,"layer_spread":base/10.0,
            "radial_wave_amplitude":0.008+base/100.0,"liss_x_frequency":3.0+float(seed%10),
            "liss_y_frequency":2.0+float(seed%8),"interference_scale":0.65+base,
            "hero_scale":min(0.76+base,1.06),"perspective_strength":0.2+base,"depth_strength":0.2+base,
            "secondary_phase":base,"color_phase":base+0.1,"stroke_scale":0.72+base
        }

    def _probe_report(self, data):
        req=data["request"]; style=self._style(req["seed"])
        instance={"schema":"C11-D-D9-VISUAL-LOOP-GRAMMAR-PARAMETER-INSTANCE-V1","schema_version":"1.0","selection":audit.SELECTED,"grammar_id":"harmonic_membrane","grammar_index":0,"shader_branch":"field_harmonic_membrane","shader_uniform":"grammar_mode","style_parameter_count":20,"style_parameters":style}
        # Hashes are mocked digests. Repeat checks are tested by comparing across the matrix.
        instance["style_parameters_sha256"]=hashlib.sha256(json.dumps(style,sort_keys=True,separators=(",",":"),allow_nan=False).encode()).hexdigest()
        core={k:v for k,v in instance.items() if k not in ("style_parameters_sha256","parameter_instance_sha256")}
        instance["parameter_instance_sha256"]=hashlib.sha256(json.dumps(core,sort_keys=True,separators=(",",":"),allow_nan=False).encode()).hexdigest()
        return {"schema":"C11-D-D9-VISUAL-LOOP-GRAMMAR-PARAMETER-PROBE-V1","schema_version":"1.0","status":"PREPARATION_ONLY_EXACT_GRAMMAR_PARAMETER_INSTANCE_IN_MEMORY_NOT_RENDERER_INPUT","contract_sha256":data["contract_sha256"],"request_id":req["request_id"],"request_hash":req["request_hash"],"selection":audit.SELECTED,"gameplay_seed":req["seed"],"music_seed":req["music_seed"],"variation_index":req["variation_index"],"presentation_profile_id":req["presentation_profile_id"],"delivery_profile_id":req["delivery_profile_id"],"canonical_chain":data["canonical_chain"],"parameter_instance":instance,"repeat_deterministic":True,"source_checks_passed":True,"renderer_native_input_emitted":False,"renderer_instance_created":False,"renderer_dispatch_invoked":False,"shader_executed":False,"media_created":False,"disk_writes":False,"c11c_source_mutation":False,"candidate_input_admissible":False,"renderer":"OFF","d4_8":"BLOCKED","release_authority":"NONE","d9_17":"BLOCKED_NO_GO","d10":"BLOCKED"}

    def test_contract_schemas_and_governance_are_strict(self):
        self.assertEqual(self.contract["schema_version"],"1.0")
        self.assertEqual(len(self.lineage),18)
        self.assertEqual(self.contract["scope"]["style_parameter_order"],list(audit.STYLE_KEYS))
        self.assertFalse(self.contract["approval_state"]["renderer_baseline_approved"])
        self.assertFalse(self.contract["execution_boundary"]["renderer_native_input_emitted"])

    def test_all_pinned_c11c_sources_match_frozen_manifest(self):
        manifest=json.loads((ROOT/audit.MANIFEST_REL).read_text(encoding="utf-8-sig"))
        frozen={r["path"]:r["sha256"] for r in manifest["source_files"]}
        pins={r["path"]:r["sha256"] for r in self.lineage}
        for path in audit.PROTECTED_C11C_PATHS:
            self.assertEqual(pins[path],frozen[path],path)

    def test_canonical_six_case_matrix_is_fixed_and_distinct(self):
        raws=audit._raw_cases()
        self.assertEqual(tuple(cid for cid,_ in raws),audit.EXPECTED_CASE_IDS)
        self.assertEqual(len({r["request_id"] for _,r in raws}),6)
        self.assertEqual({r["selection"]["subtype_id"] for _,r in raws},{"harmonic_membrane"})

    def test_dynamic_upstream_exact_visual_payload_claim_stays_false(self):
        self.assertEqual(audit.dynamic.EXPECTED_SCOPE["visual_loops"],("VISUAL_LOOP_FAMILY_ENVELOPE_GRAMMAR_INSTANCE_UNRESOLVED",False))
        self.assertFalse(self.contract["materialization_semantics"]["exact_selector_visual_payload_materialized"])

    def test_input_schema_rejects_longform_or_wrong_selector(self):
        raws=audit._raw_cases()
        chain=audit.dynamic._build_canonical_chain(raws[0][1],ROOT)
        data=audit._build_probe_input(chain,ROOT,self.contract)
        validator=audit.Draft202012Validator(self.input_schema)
        for mutation in ("selector", "longform"):
            candidate=copy.deepcopy(data)
            if mutation == "selector":
                candidate["request"]["selection"]["subtype_id"]="interference_plane"
            else:
                candidate["request"]["selection"]["content_type"]="longform"
            with self.subTest(mutation=mutation), self.assertRaises(Exception):
                validator.validate(candidate)
        self.assertEqual(audit.SELECTED["subtype_id"],"harmonic_membrane")

    def test_frozen_geometric_profile_grammar_ids_are_multiline_and_complete(self):
        profile=(ROOT/"tools/prototypes/c11c_common/C11CVariationProfile.gd").read_text(encoding="utf-8-sig")
        geometric_start=profile.find("static func _geometric(seed_value: int) -> Dictionary:")
        fractal_start=profile.find("static func _fractal(seed_value: int) -> Dictionary:",geometric_start+1)
        self.assertGreaterEqual(geometric_start,0)
        self.assertGreater(fractal_start,geometric_start)
        geometric=profile[geometric_start:fractal_start]
        ids=("harmonic_membrane","interference_plane","parametric_ribbon","lattice_wave","orbital_wave")
        self.assertIn("var grammar_modes: Array[String] = [",geometric)
        positions=[geometric.index('"'+item+'"') for item in ids]
        self.assertEqual(positions,sorted(positions))
        self.assertNotIn('var grammar_modes: Array[String] = ["harmonic_membrane"',geometric)

    def test_harness_source_checks_are_multiline_safe_and_diagnostic(self):
        harness=(ROOT/audit.HARNESS_REL).read_text(encoding="utf-8")
        self.assertIn("func _source_checks_error() -> String:",harness)
        self.assertIn("var geometric_profile := profile.substr(geometric_start, fractal_start - geometric_start)",harness)
        self.assertIn('return "geometric profile block missing token: " + token',harness)
        self.assertNotIn('var grammar_modes: Array[String] = ["harmonic_membrane", "interference_plane"',harness)

    def test_profile_alias_glow_is_mapped_to_glow_strength(self):
        harness=(ROOT/audit.HARNESS_REL).read_text(encoding="utf-8")
        self.assertIn('"glow_strength": clamp(float(value["glow"]), 0.0, 1.0)',harness)
        self.assertIn('"glow", "polygon_sides"',harness)

    def test_harness_is_stdout_only_and_does_not_create_rendering_objects(self):
        source=(ROOT/audit.HARNESS_REL).read_text(encoding="utf-8")
        for token in ("Profile.build(\"geometric\"", "parameter_instance", "exact grammar index"):
            self.assertIn(token.lower(),source.lower())
        for banned in ("ShaderMaterial.new", "GeometricWavesRenderer.new", "DirAccess.make_dir", "FileAccess.open("):
            self.assertNotIn(banned,source)

    def test_valid_probe_report_is_bound_to_canonical_request_chain(self):
        raws=audit._raw_cases(); chain=audit.dynamic._build_canonical_chain(raws[0][1],ROOT)
        contract,_,ins,_,_=audit.load_contract(ROOT)
        data=audit._build_probe_input(chain,ROOT,contract)
        report=self._probe_report(data)
        parsed=audit._validate_probe(report,data)
        self.assertEqual(parsed["parameter_instance"]["grammar_index"],0)

    def test_probe_rejects_wrong_grammar_or_renderer_activation(self):
        raws=audit._raw_cases(); chain=audit.dynamic._build_canonical_chain(raws[0][1],ROOT)
        data=audit._build_probe_input(chain,ROOT,self.contract)
        for field,value in (("renderer_native_input_emitted",True),("shader_executed",True),("media_created",True)):
            report=self._probe_report(data); report[field]=value
            with self.subTest(field=field),self.assertRaises(audit.GrammarParameterInstanceError): audit._validate_probe(report,data)
        report=self._probe_report(data); report["parameter_instance"]["grammar_index"]=1
        with self.assertRaises(audit.GrammarParameterInstanceError): audit._validate_probe(report,data)

    def test_mocked_matrix_enforces_seed_change_and_metadata_orthogonality(self):
        calls=[]
        def fake_process(command,**kwargs):
            encoded=command[-1]; data=json.loads(base64.b64decode(encoded).decode())
            report=self._probe_report(data); calls.append((data,report))
            return SimpleNamespace(returncode=0,stdout=audit.PROBE_PREFIX+json.dumps(report,separators=(",",":"))+"\n",stderr="")
        receipt=audit.run_matrix("C:/Godot/Godot_v4.7.1-stable_win64_console.exe",30,ROOT,fake_process)
        self.assertEqual(len(calls),6); self.assertEqual(len(receipt["cases"]),6)
        self.assertTrue(receipt["findings"]["metadata_orthogonality_passed"])
        self.assertFalse(receipt["findings"]["exact_selector_visual_payload_materialized"])

    def test_receipt_hash_and_schema_reject_mutation(self):
        raws=audit._raw_cases(); contract,_,ins,outs,lineage=audit.load_contract(ROOT)
        rows=[]
        for cid,raw in raws:
            chain=audit.dynamic._build_canonical_chain(raw,ROOT); data=audit._build_probe_input(chain,ROOT,contract)
            report=self._probe_report(data); parsed=audit._validate_probe(report,data); rows.append(audit._case_receipt(cid,chain,parsed))
        receipt=audit.build_receipt(rows,ROOT,contract,lineage,outs)
        self.assertTrue(audit._validate_receipt(receipt,ROOT,outs))
        receipt["execution_boundary"]["renderer_native_input_emitted"]=True
        with self.assertRaises(audit.GrammarParameterInstanceError): audit._validate_receipt(receipt,ROOT,outs)

    def test_metadata_only_case_with_different_parameter_hash_fails_closed(self):
        raws=audit._raw_cases(); contract,_,_,outs,lineage=audit.load_contract(ROOT)
        rows=[]
        for cid,raw in raws:
            chain=audit.dynamic._build_canonical_chain(raw,ROOT); data=audit._build_probe_input(chain,ROOT,contract)
            report=self._probe_report(data); parsed=audit._validate_probe(report,data); rows.append(audit._case_receipt(cid,chain,parsed))
        target=next(r for r in rows if r["case_id"]=="MUSIC_SEED_ONLY")
        target["parameter_instance"]["parameter_instance_sha256"]="f"*64
        with self.assertRaises(audit.GrammarParameterInstanceError): audit.build_receipt(rows,ROOT,contract,lineage,outs)

    def test_resealed_receipt_cannot_hide_metadata_contamination(self):
        raws=audit._raw_cases(); contract,_,_,outs,lineage=audit.load_contract(ROOT)
        rows=[]
        for cid,raw in raws:
            chain=audit.dynamic._build_canonical_chain(raw,ROOT); data=audit._build_probe_input(chain,ROOT,contract)
            report=self._probe_report(data); parsed=audit._validate_probe(report,data); rows.append(audit._case_receipt(cid,chain,parsed))
        receipt=audit.build_receipt(rows,ROOT,contract,lineage,outs)
        target=next(r for r in receipt["cases"] if r["case_id"]=="MUSIC_SEED_ONLY")
        instance=target["parameter_instance"]
        instance["style_parameters"]["morph"] += 0.01
        instance["style_parameters_sha256"]=audit._sha_json(instance["style_parameters"])
        core={k:v for k,v in instance.items() if k not in ("style_parameters_sha256","parameter_instance_sha256")}
        instance["parameter_instance_sha256"]=audit._sha_json(core)
        bind_core={"case_id":target["case_id"],"request_identity":target["request_identity"],"canonical_chain":target["canonical_chain"],"parameter_instance_sha256":instance["parameter_instance_sha256"],"frozen_c11c_manifest_sha256":audit.EXPECTED_MANIFEST_SHA256}
        target["request_parameter_binding_sha256"]=audit._sha_json(bind_core)
        receipt["receipt_sha256"]=audit._sha_json({k:v for k,v in receipt.items() if k!="receipt_sha256"})
        with self.assertRaises(audit.GrammarParameterInstanceError):
            audit._validate_receipt(receipt,ROOT,outs)

    def test_source_drift_fails_closed_without_modifying_checkout(self):
        with tempfile.TemporaryDirectory(prefix="c11d-grammar-param-drift-") as tmp:
            target=Path(tmp)
            for rel in (audit.CONTRACT_REL,audit.CONTRACT_SCHEMA_REL,audit.INPUT_SCHEMA_REL,audit.OUTPUT_SCHEMA_REL):
                dest=target/rel; dest.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(ROOT/rel,dest)
            for row in self.contract["source_lineage"]:
                dest=target/row["path"]; dest.parent.mkdir(parents=True,exist_ok=True)
                if not dest.exists(): shutil.copy2(ROOT/row["path"],dest)
            p=target/"tools/prototypes/c11c_geometric_waves_v1/GeometricWaves.gdshader"
            original=p.read_bytes(); p.write_bytes(original+b"\n// drift\n")
            with self.assertRaises(audit.GrammarParameterInstanceError): audit.load_contract(target)
            self.assertEqual(p.read_bytes(),original+b"\n// drift\n")

    def test_cli_requires_real_godot_and_no_persistence_path(self):
        source=(ROOT/audit.RUNNER_REL).read_text(encoding="utf-8")
        self.assertIn('parser.add_argument("--godot"',source)
        for banned in ("write_text(","write_bytes(","os.replace(","ffmpeg"):
            self.assertNotIn(banned.lower(),source.lower())

if __name__=="__main__": unittest.main(verbosity=2)
