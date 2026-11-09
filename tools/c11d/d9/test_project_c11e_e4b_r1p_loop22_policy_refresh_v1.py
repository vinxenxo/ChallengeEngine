import sys
import unittest
import tempfile
import hashlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import project_c11e_e4b_r1p_loop22_policy_refresh_v1 as mod


class Loop22R1PProjectionTests(unittest.TestCase):
    def make_receipt(self, family="c11c_geometric_waves_v1", grammar="interference_plane", cycles=3, seed=100002, music_seed=500002):
        return {
            "schema": "C11E-E4B-R1P-LOOP-FAMILY-PARAMETER-RECEIPT-V1",
            "receipt_index": 2,
            "receipt_sha256": "a" * 64,
            "status": "PASS_PARAMETER_PAYLOAD_MATERIALIZED_IN_MEMORY_NOT_RENDERER_INPUT",
            "payload_sha256": "b" * 64,
            "repeat_payload_sha256": "b" * 64,
            "family_music_profile_id": mod.FAMILY_PROFILES[family],
            "selection": {"content_type": "visual_loops", "family_id": family, "grammar_id": grammar},
            "seed_domains": {
                "gameplay_seed": seed, "music_seed": music_seed,
                "automatic_seed_generation": False, "runtime_seed_derivation": False,
                "music_seed_consumed_by_visual_parameters": False, "visual_parameters_use": "request.seed",
            },
            "timing": {"loop_cycles": cycles, "duration_seconds": mod.CYCLE_SECONDS[cycles], "fps": 30, "frame_count": mod.CYCLE_SECONDS[cycles] * 30},
            "visual_parameters": {"family_id": family, "variation_recipe": {"grammar_name": grammar, "loop_cycles": float(cycles)}},
            "request_identity": {k: "c" * 64 for k in mod.REQUIRED_REQUEST_IDENTITY},
            "case_source_pins": {
                "prototype": {"path": "prototype.gd", "prototype_sha256": "d" * 64},
                "launcher": {"path": "launcher.ps1", "sha256": "e" * 64},
            },
            "source_pins": {"fixture": {"sha256": "f" * 64}},
            "materialization": {
                "parameter_payload_materialized_in_memory": True,
                "launcher_invoked": False, "prototype_node_instantiated": False,
                "renderer_instantiated": False, "renderer_native_input_emitted": False,
                "frame_buffers_materialized": False, "frame_inventory_materialized": False,
                "pixel_payload_materialized": False, "media_created": False,
                "ffmpeg_invoked": False, "audio_or_d3_invoked": False,
            },
        }

    def test_01_canonical_digest_accepts_receipt_style(self):
        d = {"x": 1, "receipt_sha256": ""}
        d["receipt_sha256"] = mod.sha256_bytes(mod.canonical_json_bytes({"x": 1}))
        self.assertEqual(mod.canonical_digest(d, "receipt_sha256"), d["receipt_sha256"])

    def test_02_canonical_digest_rejects_tamper(self):
        with self.assertRaises(mod.AuditError):
            mod.canonical_digest({"x": 2, "receipt_sha256": "0" * 64}, "receipt_sha256")

    def test_03_receipt_accepts_plan_only_identity(self):
        r = self.make_receipt()
        pins = {"prototype.gd": {"sha256": "d" * 64}, "launcher.ps1": {"sha256": "e" * 64}}
        # Production receipt repeats the full source pin map; the fixture aligns with it.
        r["source_pins"] = pins
        row = mod.validate_receipt(r, pins)
        self.assertEqual(row["grammar_id"], "interference_plane")
        self.assertEqual(row["request_compatibility"], "PLAN_ONLY_NOT_D4_EXECUTABLE_COMPATIBILITY")

    def test_04_receipt_rejects_music_seed_leakage(self):
        r = self.make_receipt()
        r["seed_domains"]["music_seed_consumed_by_visual_parameters"] = True
        pins = {"prototype.gd": {"sha256": "d" * 64}, "launcher.ps1": {"sha256": "e" * 64}}
        r["source_pins"] = pins
        with self.assertRaisesRegex(mod.AuditError, "SEED_DOMAIN_LEAKAGE"):
            mod.validate_receipt(r, pins)

    def test_05_receipt_rejects_renderer_native_input(self):
        r = self.make_receipt()
        r["materialization"]["renderer_native_input_emitted"] = True
        pins = {"prototype.gd": {"sha256": "d" * 64}, "launcher.ps1": {"sha256": "e" * 64}}
        r["source_pins"] = pins
        with self.assertRaisesRegex(mod.AuditError, "EXCEEDS_PLAN_ONLY_BOUNDARY"):
            mod.validate_receipt(r, pins)

    def test_06_projection_produces_exact_22_complement(self):
        rows = []
        ids = [
            ("c11c_geometric_waves_v1", "harmonic_membrane"),
            ("c11c_fractal_bloom_v1", "radial_bloom"),
            ("c11c_sacred_symmetry_v1", "astrolabe"),
            ("c11c_living_particles_v1", "swarm"),
            ("c11c_invisible_forces_v1", "dipole_field"),
        ]
        ids += [("c11c_geometric_waves_v1", x) for x in ("interference_plane", "parametric_ribbon", "lattice_wave", "orbital_wave")]
        ids += [("c11c_fractal_bloom_v1", x) for x in ("dendritic_tunnel", "spiral_fractal", "fractal_filigree", "nested_worlds")]
        ids += [("c11c_sacred_symmetry_v1", x) for x in ("gear_train", "polygon_orrery", "origami_mandala", "celestial_chart")]
        ids += [("c11c_living_particles_v1", x) for x in ("vortex", "collision_cloud", "organic_pulse", "magnetic_filament_cloud")]
        ids += [("c11c_invisible_forces_v1", x) for x in ("vortex_field", "saddle_field", "quadrupole_field", "gravitational_lens", "topographic_basin", "scalar_potential")]
        for index, (family, grammar) in enumerate(ids, 1):
            cycles = 1 if grammar in {"lattice_wave", "dendritic_tunnel", "spiral_fractal", "fractal_filigree", "magnetic_filament_cloud", "quadrupole_field", "gravitational_lens"} else (2 if grammar in {"nested_worlds", "gear_train", "polygon_orrery", "organic_pulse", "topographic_basin"} else 3)
            rows.append({
                "family_id": family, "grammar_id": grammar,
                "music_profile": mod.FAMILY_PROFILES[family],
                "gameplay_seed": 100000 + index, "music_seed": 500000 + index,
                "loop_cycles": cycles, "duration_seconds": mod.CYCLE_SECONDS[cycles],
                "fps": 30, "frame_count": mod.CYCLE_SECONDS[cycles] * 30,
                "receipt_index": index, "receipt_sha256": f"{index:064x}",
            })
        expected = {"remaining_selector_rows": []}
        for r in rows:
            if (r["family_id"], r["grammar_id"]) not in mod.PILOT:
                expected["remaining_selector_rows"].append({
                    k: r[k] for k in ("family_id", "grammar_id", "music_profile", "gameplay_seed", "music_seed", "loop_cycles", "duration_seconds", "fps", "frame_count")
                })
        result = mod.compare_projection(expected, rows)
        self.assertEqual(len(result), 22)
        self.assertEqual(sum(1 for r in result if r["family_id"] == "c11c_invisible_forces_v1"), 6)

    def test_07_projection_rejects_seed_drift(self):
        rows = []
        ids = [(f, g) for f, gs in {
            "c11c_geometric_waves_v1": ["harmonic_membrane", "interference_plane", "parametric_ribbon", "lattice_wave", "orbital_wave"],
            "c11c_fractal_bloom_v1": ["radial_bloom", "dendritic_tunnel", "spiral_fractal", "fractal_filigree", "nested_worlds"],
            "c11c_sacred_symmetry_v1": ["astrolabe", "gear_train", "polygon_orrery", "origami_mandala", "celestial_chart"],
            "c11c_living_particles_v1": ["swarm", "vortex", "collision_cloud", "organic_pulse", "magnetic_filament_cloud"],
            "c11c_invisible_forces_v1": ["dipole_field", "vortex_field", "saddle_field", "quadrupole_field", "gravitational_lens", "topographic_basin", "scalar_potential"],
        }.items() for g in gs]
        for i, (f, g) in enumerate(ids, 1):
            c = 1 if g in {"lattice_wave", "dendritic_tunnel", "spiral_fractal", "fractal_filigree", "magnetic_filament_cloud", "quadrupole_field", "gravitational_lens"} else (2 if g in {"nested_worlds", "gear_train", "polygon_orrery", "organic_pulse", "topographic_basin"} else 3)
            rows.append({"family_id": f, "grammar_id": g, "music_profile": mod.FAMILY_PROFILES[f], "gameplay_seed": 100000+i, "music_seed": 500000+i, "loop_cycles": c, "duration_seconds": mod.CYCLE_SECONDS[c], "fps": 30, "frame_count": mod.CYCLE_SECONDS[c]*30, "receipt_index": i, "receipt_sha256": f"{i:064x}"})
        expected = {"remaining_selector_rows": [{k:r[k] for k in ("family_id", "grammar_id", "music_profile", "gameplay_seed", "music_seed", "loop_cycles", "duration_seconds", "fps", "frame_count")} for r in rows if (r["family_id"],r["grammar_id"]) not in mod.PILOT]}
        expected["remaining_selector_rows"][0]["gameplay_seed"] += 1
        with self.assertRaisesRegex(mod.AuditError, "MATRIX_FIELD_MISMATCH"):
            mod.compare_projection(expected, rows)

    def test_08_docket_requires_hash_specific_operator_decisions(self):
        policies = [{"group": k, "label": v["label"], "path": v["path"], "sha256": f"{i:064x}", "bytes": 100+i, "matches_r1p_archive_pin": True, "decision_gate": v["decision_gate"], "decision": "PENDING_OPERATOR_DECISION", "sha_confirmed": "PENDING_OPERATOR_HASH_CONFIRMATION"} for i,(k,v) in enumerate(mod.POLICIES.items(),1)]
        docket = mod.build_docket(policies, "TEST", {"closeout_sha256":"a"*64})
        self.assertIn("does not substitute for confirming the exact proposal fingerprint", docket)
        self.assertEqual(docket.count("**PENDING**"), 10)  # decision + SHA confirmation for each of five policies
        self.assertIn("renderer-native input", docket)

    def test_09_independent_prior_audit_pin_set_rechecks_17_rows(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            pins = {}
            for i in range(30):
                rel = f"r1p_source_{i:02d}.txt"
                data = f"source-{i}".encode("ascii")
                (root / rel).write_bytes(data)
                pins[rel] = {"sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}
            prior_rows = []
            for i in range(15):
                rel = f"r1p_source_{i:02d}.txt"
                prior_rows.append({"path": rel, "sha256": pins[rel]["sha256"], "stable": True})
            for rel, data in (("later_music_generator.py", b"later-music"), ("v7_plan.md", b"v7-plan")):
                (root / rel).write_bytes(data)
                prior_rows.append({"path": rel, "sha256": hashlib.sha256(data).hexdigest(), "stable": True})
            audit = {"source_pins_before_after": {"stable": True, "rows": prior_rows}}
            results, drift, prior = mod.verify_checkout_source_pins(root, audit, {"source_pins": pins})
            self.assertEqual(len(results), 30)
            self.assertEqual(len(prior), 17)
            self.assertEqual(drift, [])
            self.assertEqual(sum(row["status"] == "PASS" for row in results), 30)
            self.assertEqual(sum(row["status"] == "PASS" for row in prior), 17)

    def test_10_r1p_pin_drift_is_reported_fail_closed(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            pins = {}
            for i in range(30):
                rel = f"source_{i:02d}.txt"
                data = f"source-{i}".encode("ascii")
                (root / rel).write_bytes(data)
                pins[rel] = {"sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}
            prior_rows = []
            for i in range(15):
                rel = f"source_{i:02d}.txt"
                prior_rows.append({"path": rel, "sha256": pins[rel]["sha256"], "stable": True})
            for rel, data in (("later_music_generator.py", b"later-music"), ("v7_plan.md", b"v7-plan")):
                (root / rel).write_bytes(data)
                prior_rows.append({"path": rel, "sha256": hashlib.sha256(data).hexdigest(), "stable": True})
            (root / "source_00.txt").write_bytes(b"mutated")
            audit = {"source_pins_before_after": {"stable": True, "rows": prior_rows}}
            results, drift, prior = mod.verify_checkout_source_pins(root, audit, {"source_pins": pins})
            self.assertTrue(any(row["path"] == "source_00.txt" for row in drift))



if __name__ == "__main__":
    unittest.main(verbosity=2)
