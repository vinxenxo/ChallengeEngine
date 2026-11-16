from __future__ import annotations
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = PROJECT_ROOT / "tools" / "c11d" / "d9" / "c11e_e4c_peripheral_scan_tier_batch.py"
spec = importlib.util.spec_from_file_location("c11e_e4c_peripheral_scan_tier_batch", MODULE_PATH)
assert spec and spec.loader
batch = importlib.util.module_from_spec(spec)
spec.loader.exec_module(batch)


class PeripheralScanTierBatchTests(unittest.TestCase):
    def setUp(self):
        self.base = {
            "schema": "C11-D-D9.9-UNIVERSAL-PRODUCER-REQUEST-V1", "schema_version": "1.0",
            "request_id": "ACCEPTED-TRACKING-TIER-1", "mode": "PRODUCTION",
            "selection": {"content_type": "visual_drills", "family_id": "tracking", "variant_id": "tier-1"},
            "seed": 12345, "music_seed": 840001, "variation_index": 0,
            "audio_enabled": True, "personalization_enabled": True,
            "delivery_profile_id": "REVIEW_720", "presentation_profile_id": "social_default_v1",
            "production_override": {"title": "SEGUIMIENTO VISUAL · NIVEL 1",
                "subtitle": "Sigue la trayectoria del objetivo en movimiento",
                "call_to_action": "Mantén el objetivo a la vista", "language": "es"},
            "provenance": {"request_origin": "CLI", "source_revision": "C11D-D9.10-PRODUCER-0.11.1"},
        }

    def _project_root(self, root: Path):
        fixture = Path(__file__).resolve().parent / "fixtures" / "visual_drill_peripheral_scan_canonical.json"
        target = root / batch.PERIPHERAL_SCAN_CANONICAL_REL
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(fixture, target)

    def _source_inventory(self, root: Path):
        inventory = []
        folder = root / "source_pin_fixture"
        folder.mkdir(parents=True, exist_ok=True)
        for index in range(91):
            body = f"peripheral_scan-source-pin-{index:03d}".encode("ascii")
            rel = f"source_pin_fixture/{index:03d}.bin"
            path = root / rel
            path.write_bytes(body)
            inventory.append({"path": rel, "bytes": len(body), "sha256": hashlib.sha256(body).hexdigest()})
        return inventory

    def _final_fixture(self, frames=690, duration=23.0, pix_fmt="yuv420p", drift=0.0):
        streams = [
            {"codec_type":"video", "codec_name":"h264", "profile":"High", "width":720,
             "height":1280, "pix_fmt":pix_fmt, "color_range":"tv", "avg_frame_rate":"30/1", "nb_read_frames":str(frames)},
            {"codec_type":"audio", "codec_name":"aac", "profile":"LC", "sample_rate":"48000", "channels":2, "channel_layout":"stereo"},
        ]
        return {"duration_seconds":duration, "av_start_delta_seconds":drift, "ffprobe":{"streams":streams}}

    def _qualification_fixture(self, root: Path, tier=1, request_id="E4C-PSC-T1-a1b2c3d4"):
        self._project_root(root)
        pins = self._source_inventory(root)
        out = root / "artifacts" / "production" / "c11e" / request_id
        out.mkdir(parents=True, exist_ok=True)
        def put(name, body):
            path=out/name; path.write_bytes(body); return str(path), hashlib.sha256(body).hexdigest()
        wa, was = put("music_A.wav", b"wav-a")
        wb, wbs = put("music_B.wav", b"wav-a")
        wc, wcs = put("music_C.wav", b"wav-c")
        ma, mas = put("final_A.mp4", b"video-a")
        mc, mcs = put("final_C.mp4", b"video-c")
        final=self._final_fixture()
        receipt={
            "status":"PASS_E4C_DRILL_SINGLE_SELECTOR_A_V_QUALIFICATION", "request_id":request_id,
            "request_origin":"CLI", "family":"peripheral_scan", "tier":tier, "gameplay_seed":12345,
            "music_seed_a":840001, "music_seed_b":840001, "family_music_profile":"ORBITAL_RITUAL",
            "family_adapter_preparation_status":"NOT_CONNECTED_E1", "release_authority":"NONE",
            "production_dispatch":False, "production_release":False, "c11c_frozen_manifest_unchanged":True,
            "c11c_manifest_sha256":batch.FROZEN_MANIFEST_SHA256, "c11c_source_mutation":False,
            "renderer_invoked":True, "d_postcomposition":True, "ffmpeg_decode_encode_mux":True,
            "audio_generated":True, "source_pins_pre_post_equal":True, "source_pin_count":91,
            "source_pins_pre_execution":pins, "source_pins_immediately_pre_renderer":pins, "source_pins_post_execution":pins,
            "family_adapter_execution":{"shared_entrypoint":"c11e_e4c_drill_execution.py"},
            "e1_gui_cli_parity":{"status":"PASS_E1_SHARED_GUI_CLI_INTENT_PARITY","semantic_identity_equal":True},
            "e1_validation":{"status":"PASS_E1_PREPARATION_ONLY"},
            "native_timeline":{"fps":30,"total_frames":690,"gameplay_frames":510,"duration_seconds":23.0,"pre_roll_frames":90,"end_cta_frames":90},
            "d_composition":{"frames_composed":690,"frames_expected":690,"phase_counts":{"PRE_ROLL":90,"GAME":510,"END_CTA":90}},
            "d_editorial_visible_fields":["title","subtitle","call_to_action"],
            "family_music":{"route":"C11_C_FAMILY_MUSIC_V4","profile_id":"ORBITAL_RITUAL","same_seed_ab_identical":True,
                "changed_seed_c_distinct":True,"A":{"path":wa,"sha256":was},"B":{"path":wb,"sha256":wbs},"C":{"path":wc,"sha256":wcs}},
            "bitstream_isolation":{"video_stream_identical":True,"audio_stream_changed":True,
                "video_stream_sha256_A":"a"*64,"video_stream_sha256_C":"a"*64,
                "audio_stream_sha256_A":"b"*64,"audio_stream_sha256_C":"c"*64},
            "final_A":{"path":ma,"sha256":mas,**final}, "final_C_changed_music":{"path":mc,"sha256":mcs,**final},
        }
        rp=out/"E4C_DRILL_AV_QUALIFICATION_RECEIPT.json"; rp.write_text(json.dumps(receipt),encoding="utf-8")
        summary={"status":receipt["status"],"request_id":request_id,"selector":f"peripheral_scan/tier-{tier}",
                 "family_music_profile":"ORBITAL_RITUAL","receipt":str(rp)}
        sp=root/"artifacts"/"tests"/"c11e"/"batch"/(request_id+".CLI_EXECUTION_RESULT.json")
        sp.parent.mkdir(parents=True,exist_ok=True); sp.write_text(json.dumps(summary),encoding="utf-8")
        return batch.create_request(self.base,tier,request_id),sp,rp

    def test_plan_contains_exactly_five_peripheral_scan_tiers(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); self._project_root(root)
            rows=batch.batch_plan("E4C-PERIPHERAL-SCAN-T1-5-20261116T010000Z-a1b2c3d4",root)
        self.assertEqual([x["selector"] for x in rows],[f"peripheral_scan/tier-{i}" for i in range(1,6)])
        self.assertEqual(len({x["request_id"] for x in rows}),5)
        self.assertTrue(all(x["family_music_profile"]=="ORBITAL_RITUAL" and x["expected_frames"]==690 for x in rows))

    def test_plan_rejects_malformed_or_other_family_batch_ids(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); self._project_root(root)
            for bid in ("E4C-PURSUIT-T2-5-20261115T111111Z-a1b2c3d4","E4C-PERIPHERAL-SCAN-T2-5-20261116T010000Z-a1b2c3d4","bad-id"):
                with self.subTest(bid=bid), self.assertRaises(batch.BatchError): batch.batch_plan(bid,root)

    def test_request_is_selector_specific_and_uses_orbital_ritual(self):
        r=batch.create_request(self.base,3,"E4C-PSC-T3-a1b2c3d4")
        self.assertEqual(r["selection"],{"content_type":"visual_drills","family_id":"peripheral_scan","variant_id":"tier-3"})
        self.assertEqual(r["seed"],12345); self.assertEqual(r["music_seed"],840001)
        self.assertEqual(r["production_override"]["title"],"ESCANEO PERIFÉRICO · NIVEL 3")
        self.assertEqual(r["production_override"]["subtitle"],"Mantén la mirada en el ancla central")
        self.assertTrue(r["audio_enabled"] and r["personalization_enabled"])

    def test_request_does_not_mutate_tracking_template(self):
        before=json.dumps(self.base,sort_keys=True)
        batch.create_request(self.base,5,"E4C-PSC-T5-a1b2c3d4")
        self.assertEqual(json.dumps(self.base,sort_keys=True),before)

    def test_exact_38_runtime_source_pins_are_declared(self):
        self.assertEqual(len(batch.SOURCE_PINS),38)
        self.assertEqual(batch.SOURCE_PINS[batch.PURSUIT_CANONICAL_REL],batch.PURSUIT_CANONICAL_SHA256)
        self.assertEqual(batch.SOURCE_PINS[batch.SACCADE_CANONICAL_REL],batch.SACCADE_CANONICAL_SHA256)
        self.assertEqual(batch.SOURCE_PINS[batch.PERIPHERAL_SCAN_CANONICAL_REL],batch.PERIPHERAL_SCAN_CANONICAL_SHA256)
        self.assertEqual(batch.SOURCE_PINS["release/C11C_FREEZE_PACKAGE_MANIFEST.json"],batch.FROZEN_MANIFEST_SHA256)
        self.assertEqual(batch.SOURCE_PINS[batch.EXECUTOR_REL],"b7cbf7bd97f76f4c2e339840fc694d3f5b0e50186ba2456e45ff00e585751abe")

    def test_peripheral_scan_timeline_derives_17s_510_frames_plus_180_editorial_frames(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); self._project_root(root); t=batch.peripheral_scan_timeline_contract(root)
        self.assertEqual(t["gameplay_frames"],510); self.assertEqual(t["gameplay_duration_seconds"],17.0)
        self.assertEqual(t["total_frames"],690); self.assertEqual(t["duration_seconds"],23.0)
        self.assertEqual(t["phase_counts"],{"PRE_ROLL":90,"GAME":510,"END_CTA":90})

    def test_peripheral_scan_canonical_hash_mismatch_fails_closed(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); self._project_root(root)
            p=root/batch.PERIPHERAL_SCAN_CANONICAL_REL; p.write_text(p.read_text()+" ",encoding="utf-8")
            with self.assertRaisesRegex(batch.BatchError,"SHA_MISMATCH"): batch.peripheral_scan_timeline_contract(root)

    def test_ffprobe_accepts_690_frame_23_second_h264_aac(self):
        batch.verify_ffprobe_contract(self._final_fixture(),"PERIPHERAL_SCAN",{"total_frames":690,"duration_seconds":23.0,"fps":30})

    def test_ffprobe_rejects_tracking_810_frame_27_second_fixture(self):
        with self.assertRaises(batch.BatchError): batch.verify_ffprobe_contract(self._final_fixture(810,27.0),"PERIPHERAL_SCAN",{"total_frames":690,"duration_seconds":23.0,"fps":30})

    def test_ffprobe_rejects_wrong_pixel_format(self):
        with self.assertRaises(batch.BatchError): batch.verify_ffprobe_contract(self._final_fixture(pix_fmt="yuv444p"),"PERIPHERAL_SCAN",{"total_frames":690,"duration_seconds":23.0,"fps":30})

    def test_ffprobe_rejects_av_start_drift(self):
        with self.assertRaises(batch.BatchError): batch.verify_ffprobe_contract(self._final_fixture(drift=0.02),"PERIPHERAL_SCAN",{"total_frames":690,"duration_seconds":23.0,"fps":30})

    def test_91_pin_snapshots_require_three_equal_inventories(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); pins=self._source_inventory(root)
            receipt={"source_pin_count":91,"source_pins_pre_post_equal":True,"source_pins_pre_execution":pins,
                "source_pins_immediately_pre_renderer":pins,"source_pins_post_execution":pins}
            self.assertEqual(len(batch.verify_91_pin_snapshots(root,receipt,"peripheral_scan/tier-1")),64)

    def test_91_pin_inventory_rejects_posix_and_windows_traversal(self):
        base=[{"path":f"ok/{i}.bin","bytes":1,"sha256":"a"*64} for i in range(90)]
        for bad in ("../outside.bin",r"..\outside.bin",r"C:\outside.bin"):
            arr=base+[{"path":bad,"bytes":1,"sha256":"a"*64}]
            with self.subTest(path=bad), self.assertRaises(batch.BatchError): batch._normalized_pin_inventory(arr,"TEST")

    def test_91_pin_inventory_rejects_duplicate_paths(self):
        arr=[{"path":f"ok/{i}.bin","bytes":1,"sha256":"a"*64} for i in range(90)]
        arr.append({"path":"ok/0.bin","bytes":1,"sha256":"a"*64})
        with self.assertRaises(batch.BatchError): batch._normalized_pin_inventory(arr,"TEST")

    def test_91_pin_inventory_rejects_wrong_cardinality(self):
        with self.assertRaises(batch.BatchError): batch._normalized_pin_inventory([],"TEST")

    def test_91_pin_snapshot_detects_physical_source_drift(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); pins=self._source_inventory(root); (root/pins[0]["path"]).write_bytes(b"drift")
            receipt={"source_pin_count":91,"source_pins_pre_post_equal":True,"source_pins_pre_execution":pins,
                "source_pins_immediately_pre_renderer":pins,"source_pins_post_execution":pins}
            with self.assertRaises(batch.BatchError): batch.verify_91_pin_snapshots(root,receipt,"peripheral_scan/tier-1")

    def test_full_qualification_accepts_peripheral_scan_orbital_ritual_contract(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); req,summary,_=self._qualification_fixture(root)
            result=batch.validate_qualification(root,req,summary,1)
        self.assertEqual(result["selector"],"peripheral_scan/tier-1")
        self.assertEqual(result["native_total_frames"],690)
        self.assertEqual(result["music_A_B_sha256"],hashlib.sha256(b"wav-a").hexdigest())

    def test_full_qualification_rejects_wrong_family_music_profile(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); req,summary,rp=self._qualification_fixture(root)
            receipt=json.loads(rp.read_text()); receipt["family_music_profile"]="ORGANIC_BLOOM"
            rp.write_text(json.dumps(receipt)); summary_data=json.loads(summary.read_text()); summary_data["family_music_profile"]="ORGANIC_BLOOM"; summary.write_text(json.dumps(summary_data))
            with self.assertRaises(batch.BatchError): batch.validate_qualification(root,req,summary,1)

    def test_full_qualification_rejects_wrong_family_selector(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); req,summary,_=self._qualification_fixture(root)
            req["selection"]["family_id"]="pursuit"
            with self.assertRaises(batch.BatchError): batch.validate_qualification(root,req,summary,1)

    def test_output_collision_fails_before_attempt_reservation(self):
        from unittest import mock
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); self._project_root(root)
            out=root/"artifacts/production/c11e/E4C-PSC-T1-a1b2c3d4"; out.mkdir(parents=True)
            with mock.patch.object(batch,"verify_pins",return_value={}), \
                 mock.patch.object(batch,"verify_environment",return_value={}), \
                 mock.patch.object(batch,"validate_base",return_value=self.base):
                with self.assertRaisesRegex(batch.BatchError,"OUTPUT_COLLISION"):
                    batch.execute_batch(root,Path("/missing/python"),"E4C-PERIPHERAL-SCAN-T1-5-20261116T010000Z-a1b2c3d4",3600)
            evidence=root/"artifacts/tests/c11e/e4c_peripheral_scan_tier_batch/E4C-PERIPHERAL-SCAN-T1-5-20261116T010000Z-a1b2c3d4"
            self.assertFalse(evidence.exists(),"collision must fail before one-shot authorization or evidence reservation")

    def test_consumed_batch_evidence_directory_is_never_reused(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            evidence=root/"artifacts/tests/c11e/e4c_peripheral_scan_tier_batch/E4C-PERIPHERAL-SCAN-T1-5-20261116T010000Z-a1b2c3d4"
            evidence.mkdir(parents=True)
            with self.assertRaisesRegex(batch.BatchError,"BATCH_EVIDENCE_COLLISION"):
                batch._new_batch_evidence(root,evidence.name)

    def test_no_pursuit_t1_recovery_is_embedded(self):
        source=MODULE_PATH.read_text(encoding="utf-8")
        self.assertNotIn("recover_failed_tier1",source)
        self.assertNotIn("REUSED_EXISTING_T1",source)
        self.assertIn("All five Peripheral Scan tiers are independent",source)


    def test_reserved_batch_id_is_written_to_stderr_after_persistent_one_shot_lock(self):
        source = MODULE_PATH.read_text(encoding="utf-8")
        marker = 'print(f"BATCH_RESERVED_ID={batch_id}", file=sys.stderr, flush=True)'
        self.assertIn(marker, source)
        lock = source.index('write_json_exclusive(lock_path, {')
        authorization = source.index('write_json_exclusive(authorization_path, {', lock)
        emitted = source.index(marker)
        self.assertLess(lock, emitted)
        self.assertLess(authorization, emitted)


if __name__ == "__main__":
    unittest.main(verbosity=2)
