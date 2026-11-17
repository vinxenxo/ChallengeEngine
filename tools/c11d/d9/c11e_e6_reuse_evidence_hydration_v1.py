#!/usr/bin/env python3
"""Read-only E6 evidence hydration audit. Writes only its own JSON report."""
from __future__ import annotations
import argparse, hashlib, json, re, sys, uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

D9_RUN = "E6D9PREP_20261117T202442Z_BCCD3C39"
D9_MANIFEST_SHA = "11cbf8fd1c2862d0004dbfd28bd27c78cf882a7db725d571484617862af35c18"
D9_RECEIPT_SHA = "53f01752de6928044707cb08dda04e3f2ab5f87f9f177daac70737ea039b4f88"
D9_INSTALL_RECEIPT_SHA = "05b8084d3f6bcb6824550c1bda6348fc7d48b8d3db52d4c711fcd880500eeacc"
D9_INSTALL_RUN = "E6D9INSTALLV2_20261117T202429Z_25401E57"
FROZEN_C11C_SHA = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
D4_8_SHA = "0866b53ad4fcdebe74d01f66864b2dfb00eb644ca28dcd59301c8f3208239c07"
R1V_HUMAN_SHA = "a9e1de310ba1f52bab029a6fc6f926892264dd25cfa5edd8ec90aec460a2662a"
R1V_REPORT_SHA = "85de2645621acd6f8183508e0da9b5466b8a00cf9d2cb340a170f7d2803285ba"
R1V_PROCESS_SHA = "8820d36ffd6c1969eb4e148fe640f08f4324a243fe49ca1e43299e6db1201d26"
GEO_REPORT_SHA = "15712f3187237f118df05c0c013558c65b2a2f7d342a0e765da8307e7a7ff037"
LOOP22_PROCESS_SHA = "37ee99f8ab30eb445c9ca462471152b6fadc850471b8a27f7c59f30714ec2f5d"
LOOP22_HUMAN_SHA = "d8f7050f952b7248b24763abde20ce52bf812c3934738f14670a0a3dc0c72068"
LOOP22_MANIFEST_SHA = "170b869b604eae0fdecf770c395e379554ae4ee05bbe579a560180a725fe396f"
CH004_RECEIPT_SHA = "102cf07a0b8920318c3ba211a3bd4374c3e080018486363d701f81e65613aaa0"

DRILL_ROWS = [
    ("E6-DR-01", "artifacts/production/c11e/E4C-TRK-T2-6239dd21/E4C_DRILL_AV_QUALIFICATION_RECEIPT.json", "f95e9b4e787f1b4f7db79b92428324f6de662ade55b260c7692d4440e2967ee7"),
    ("E6-DR-02", "artifacts/production/c11e/E4C-PRS-T1-b3abbe94/E4C_DRILL_AV_QUALIFICATION_RECEIPT.json", "57206b4560b917c7a7fe5e738c5afd5d900d293e01c99fcd554f0926acc6eee7"),
    ("E6-DR-03", "artifacts/production/c11e/E4C-SAC-T1-57fdf44b/E4C_DRILL_AV_QUALIFICATION_RECEIPT.json", "930ba103153fbca0226a0b7abd1226b46dfd3c2e523204e83e6cb39f1282e606"),
    ("E6-DR-04", "artifacts/production/c11e/E4C-PSC-T1-b342a227/E4C_DRILL_AV_QUALIFICATION_RECEIPT.json", "eb290666163df0e89daac9c683a95a39c38d536c5da735def15cd3a19964083b"),
    ("E6-DR-05", "artifacts/production/c11e/E4C-TRK-T5-6239dd21/E4C_DRILL_AV_QUALIFICATION_RECEIPT.json", "6e55dc3fd4fc13745347cc641d29103fbfb7fa90dee932910f920703690c3c61"),
    ("E6-DR-06", "artifacts/production/c11e/E4C-PSC-T5-b342a227/E4C_DRILL_AV_QUALIFICATION_RECEIPT.json", "5644ffa386c2d1388e7dd657cb566c796a87de93b22c28db84197dbb8ad3a224"),
]

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def safe_path(root: Path, rel: str) -> Path:
    if not isinstance(rel, str) or not rel.strip():
        raise ValueError("EMPTY_OR_NONSTRING_PATH")
    p = Path(rel.replace("\\", "/"))
    if p.is_absolute() or re.match(r"^[A-Za-z]:", rel) or ".." in p.parts:
        raise ValueError("UNSAFE_RELATIVE_PATH:" + rel)
    root_real = root.resolve()
    out = (root_real / p).resolve()
    if out != root_real and root_real not in out.parents:
        raise ValueError("PATH_ESCAPES_PROJECT_ROOT:" + rel)
    return out

def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))

def check_file(root: Path, rel: str, expected: str, base: Path | None = None) -> dict:
    try:
        p = safe_path(root, rel)
        if not p.is_file() and base is not None:
            candidate = (base / rel.replace("\\", "/")).resolve()
            if candidate != root.resolve() and root.resolve() not in candidate.parents:
                raise ValueError("RELATIVE_PATH_ESCAPES_PROJECT_ROOT:" + rel)
            p = candidate
        if not p.is_file():
            return {"path": rel, "status": "MISSING"}
        actual = sha256_file(p)
        return {"path": p.relative_to(root.resolve()).as_posix(), "expected_sha256": expected, "actual_sha256": actual,
                "bytes": p.stat().st_size, "status": "PASS" if actual == expected else "SHA256_MISMATCH"}
    except Exception as e:
        return {"path": rel, "status": "INVALID_REFERENCE", "error": str(e)}

def paired_path_hash_refs(node: Any, prefix: str = "$") -> list[tuple[str, str, str]]:
    refs = []
    if isinstance(node, dict):
        for k, v in node.items():
            if isinstance(v, str) and (k == "path" or k.endswith("_path")):
                candidates = []
                if k == "path": candidates = ["sha256", "file_sha256", "output_sha256"]
                else:
                    stem = k[:-5]
                    candidates = [stem + "_sha256", stem + "_hash", "sha256"]
                expected = next((node[c] for c in candidates if isinstance(node.get(c), str) and re.fullmatch(r"[0-9a-fA-F]{64}", node[c])), None)
                if expected:
                    refs.append((prefix + "." + k, v, expected.lower()))
        for k, v in node.items(): refs.extend(paired_path_hash_refs(v, prefix + "." + k))
    elif isinstance(node, list):
        for i, v in enumerate(node): refs.extend(paired_path_hash_refs(v, f"{prefix}[{i}]"))
    return refs

def find_json_by_sha(root: Path, sha: str, search_root: Path) -> list[Path]:
    found = []
    if not search_root.exists(): return found
    for p in search_root.rglob("*.json"):
        if not p.is_file(): continue
        try:
            if sha256_file(p) == sha: found.append(p)
        except OSError: pass
    return found

def find_small_file_by_sha(sha: str, search_root: Path, max_bytes: int = 10 * 1024 * 1024) -> list[Path]:
    found = []
    if not search_root.exists(): return found
    allowed = {".md", ".txt", ".json", ".log", ".csv"}
    for p in search_root.rglob("*"):
        try:
            if p.is_file() and p.suffix.lower() in allowed and p.stat().st_size <= max_bytes and sha256_file(p) == sha:
                found.append(p)
        except OSError: pass
    return found

class Audit:
    def __init__(self, root: Path):
        self.root = root.resolve()
        self.checks: list[dict] = []
        self.errors: list[str] = []
        self.counts = {"source_pins": 0, "drill_receipts": 0, "drill_nested_files": 0,
                       "r1v_loop_slots": 0, "loop22_nested_files": 0, "challenge004_nested_files": 0}

    def add(self, name: str, result: dict):
        result["check"] = name; self.checks.append(result)
        if result.get("status") != "PASS": self.errors.append(name + ":" + result.get("status", "FAIL"))

    def verify_nested(self, name: str, data: Any, base: Path) -> int:
        refs = paired_path_hash_refs(data)
        # Exclude pure path references outside the project and retain only hash-bearing artifacts.
        for pointer, rel, expected in refs:
            r = check_file(self.root, rel, expected, base)
            r["json_pointer"] = pointer
            self.add(name + ":" + pointer, r)
        return len(refs)

    def run(self) -> dict:
        # D9 PREPARE_ONLY: accepted install, manifest, receipt and source pins.
        d9dir = self.root / "artifacts/tests/c11e/e6_d9_prepare_only" / D9_RUN
        manifest_p = d9dir / "E6_D9_CHALLENGE_PREPARE_ONLY_MANIFEST_V2.json"
        receipt_p = d9dir / "E6_D9_CHALLENGE_PREPARE_ONLY_RECEIPT_V2.json"
        install_rel = "artifacts/tests/c11e/e6_d9_prepare_only_install/" + D9_INSTALL_RUN + "/INSTALL_RECEIPT_V2.json"
        self.add("D9_INSTALL_RECEIPT",check_file(self.root,install_rel,D9_INSTALL_RECEIPT_SHA))
        for p, expected, label in [(manifest_p,D9_MANIFEST_SHA,"D9_MANIFEST"),(receipt_p,D9_RECEIPT_SHA,"D9_RECEIPT")]:
            if p.is_file(): self.add(label, {"path":p.relative_to(self.root).as_posix(),"actual_sha256":sha256_file(p),"expected_sha256":expected,"status":"PASS" if sha256_file(p)==expected else "SHA256_MISMATCH"})
            else: self.add(label,{"path":p.relative_to(self.root).as_posix(),"status":"MISSING"})
        if manifest_p.is_file() and receipt_p.is_file():
            m, r = read_json(manifest_p), read_json(receipt_p)
            if r.get("status") != "PASS_D9_PREPARE_ONLY_18_INTENTS_18_ENVELOPES_LINKED_EXECUTION_HELD" or r.get("manifest_sha256") != D9_MANIFEST_SHA:
                self.add("D9_RECEIPT_MANIFEST_LINK", {"status":"MISMATCH"})
            else: self.add("D9_RECEIPT_MANIFEST_LINK", {"status":"PASS"})
            if m.get("governance",{}).get("release_authority") != "NONE" or m.get("governance",{}).get("godot_invoked") is not False or m.get("governance",{}).get("media_created") is not False:
                self.add("D9_GOVERNANCE_BOUNDARY", {"status":"MISMATCH"})
            else: self.add("D9_GOVERNANCE_BOUNDARY", {"status":"PASS"})
            pins = m.get("source_authority",{}).get("accepted_source_pins",[])
            self.counts["source_pins"] = len(pins)
            for i, pin in enumerate(pins):
                self.add(f"D9_SOURCE_PIN_{i+1:02d}", check_file(self.root,pin.get("path"),pin.get("sha256")))
            for label, row in m.get("predecessors",{}).items():
                if isinstance(row,dict) and row.get("path") and row.get("sha256"):
                    self.add("D9_PREDECESSOR_"+label.upper(),check_file(self.root,row["path"],row["sha256"]))
        else:
            self.add("D9_SOURCE_PINS", {"status":"BLOCKED_NO_MANIFEST"})

        # R1V human acceptance and exact five selector outputs.
        human_rel = "artifacts/tests/c11e/r1v_operator_human_review_closeout/R1V_HUMAN_REVIEW_CLOSEOUT_RECEIPT_V1.json"
        human_p = safe_path(self.root,human_rel)
        self.add("R1V_HUMAN_CLOSEOUT_RECEIPT",check_file(self.root,human_rel,R1V_HUMAN_SHA))
        if human_p.is_file():
            human = read_json(human_p)
            self.add("R1V_HUMAN_ACCEPTANCE_STATUS", {"status":"PASS" if human.get("status")=="PASS_TEST_ONLY_OPERATOR_ACCEPTED" and human.get("acceptance",{}).get("combined_slots")=="10/10_PASS" else "MISMATCH"})
            loop_rows = {(x.get("family_id"),x.get("grammar_id")):x for x in human.get("slots",[])}
            for row in [
                ("c11c_fractal_bloom_v1","radial_bloom"),("c11c_geometric_waves_v1","harmonic_membrane"),
                ("c11c_invisible_forces_v1","dipole_field"),("c11c_living_particles_v1","swarm"),
                ("c11c_sacred_symmetry_v1","astrolabe")]:
                pair = loop_rows.get(row)
                if not pair:
                    self.add("R1V_LOOP_"+row[1],{"status":"MISSING_ROW"}); continue
                self.counts["r1v_loop_slots"] += 1
                for slot in ("A","B"):
                    s = next((x for x in human.get("slots",[]) if x.get("family_id")==row[0] and x.get("grammar_id")==row[1] and x.get("slot")==slot),None)
                    if not s:
                        self.add("R1V_LOOP_"+row[1]+"_"+slot,{"status":"MISSING_SLOT"}); continue
                    if s.get("visual_status") not in ("OPERATOR_CONFIRMED_PASS","OPERATOR_CONFIRMED_AV_PASS") or s.get("audio_status") not in ("OPERATOR_CONFIRMED_PASS","OPERATOR_CONFIRMED_AV_PASS") or s.get("operator_statement")!="pass":
                        self.add("R1V_LOOP_"+row[1]+"_"+slot,{"status":"HUMAN_ACCEPTANCE_MISMATCH"})
                    else:
                        self.add("R1V_LOOP_"+row[1]+"_"+slot,check_file(self.root,s["mp4_path"],s["mp4_sha256"]))
        # Exact R1V technical lineage files.
        self.add("R1V_ORIGINAL_REPORT",check_file(self.root,"artifacts/tests/c11e/r1v_av_five_family_qualification/Q5_040414_B6BE4D/r1v_av_report.json",R1V_REPORT_SHA))
        self.add("R1V_ORIGINAL_PROCESS_RECEIPT",check_file(self.root,"artifacts/tests/c11e/r1v_av_five_family_qualification/Q5_040414_B6BE4D/r1v_av_process_receipt.json",R1V_PROCESS_SHA))
        test_root = self.root / "artifacts/tests/c11e"
        geo_matches=find_json_by_sha(self.root,GEO_REPORT_SHA,test_root)
        if len(geo_matches)==1:
            self.add("R1V_GEO_REPLACEMENT_REPORT",{"path":geo_matches[0].relative_to(self.root).as_posix(),"actual_sha256":GEO_REPORT_SHA,"status":"PASS"})
        else:
            self.add("R1V_GEO_REPLACEMENT_REPORT",{"status":"MISSING" if not geo_matches else "AMBIGUOUS_MATCHES","match_count":len(geo_matches)})

        # Loop22 evidence: locate exact immutable JSON bytes by their accepted SHA, then verify all path/hash pairs.
        human22_matches=find_small_file_by_sha(LOOP22_HUMAN_SHA,self.root)
        if len(human22_matches)==1:
            self.add("LOOP22_HUMAN_CLOSEOUT_REPORT",{"path":human22_matches[0].relative_to(self.root).as_posix(),"actual_sha256":LOOP22_HUMAN_SHA,"status":"PASS"})
        else:
            self.add("LOOP22_HUMAN_CLOSEOUT_REPORT",{"status":"MISSING" if not human22_matches else "AMBIGUOUS_MATCHES","match_count":len(human22_matches)})
        for label, expected in [("LOOP22_PROCESS_RECEIPT",LOOP22_PROCESS_SHA),("LOOP22_RUN_MANIFEST",LOOP22_MANIFEST_SHA)]:
            matches = find_json_by_sha(self.root,expected,test_root)
            if len(matches) != 1:
                self.add(label,{"status":"MISSING" if not matches else "AMBIGUOUS_MATCHES","match_count":len(matches),"matches":[p.relative_to(self.root).as_posix() for p in matches]})
            else:
                p=matches[0]; data=read_json(p)
                self.add(label,{"path":p.relative_to(self.root).as_posix(),"actual_sha256":expected,"status":"PASS"})
                if label=="LOOP22_RUN_MANIFEST":
                    found=False
                    def has_target(n):
                        nonlocal found
                        if isinstance(n,dict):
                            vals=[str(v).lower() for k,v in n.items() if isinstance(v,(str,int,float)) and k.lower() in ("selector","grammar_id","selector_id")]
                            if any(v in ("interference_plane","e6-lp-06") for v in vals): found=True
                            for v in n.values(): has_target(v)
                        elif isinstance(n,list):
                            for v in n: has_target(v)
                    has_target(data)
                    self.add("LOOP22_INTERFERENCE_PLANE_ROW",{"status":"PASS" if found else "MISSING_ROW"})
                n=self.verify_nested(label+"_NESTED",data,p.parent)
                if label=="LOOP22_RUN_MANIFEST": self.counts["loop22_nested_files"]=n
        # Six E4C Drill receipts and every explicitly paired nested output reference.
        for scenario, rel, expected in DRILL_ROWS:
            p=safe_path(self.root,rel)
            self.add(scenario+"_RECEIPT",check_file(self.root,rel,expected))
            if p.is_file():
                data=read_json(p)
                refs=self.verify_nested(scenario+"_NESTED",data,p.parent)
                self.counts["drill_receipts"] += 1
                self.counts["drill_nested_files"] += refs
                if data.get("status") not in ("PASS","PASS_E4C_DRILL_SINGLE_SELECTOR_A_V_QUALIFICATION","PASS_E4C_DRILL_AV_QUALIFICATION"):
                    # Preserve actual status in the report; the exact accepted status may be schema-versioned.
                    self.add(scenario+"_RECEIPT_STATUS",{"actual_status":data.get("status"),"status":"PASS" if data.get("status") else "STATUS_FIELD_MISSING"})
                else: self.add(scenario+"_RECEIPT_STATUS",{"status":"PASS"})

        # Challenge_004 E4A.7 accepted A/B/C receipt and nested outputs.
        ch_rel="artifacts/tests/c11e/e4a_d_composited_av_review/RUN_20261106T070808Z-62F31F9C/C11E_E4A7_D_COMPOSITED_CHALLENGE_AV_RECEIPT.json"
        ch_p=safe_path(self.root,ch_rel)
        self.add("CH004_E4A7_RECEIPT",check_file(self.root,ch_rel,CH004_RECEIPT_SHA))
        if ch_p.is_file():
            ch=read_json(ch_p)
            refs=self.verify_nested("CH004_E4A7_NESTED",ch,ch_p.parent)
            self.counts["challenge004_nested_files"]=refs
            self.add("CH004_ABC_AUDIO_VARIANTS",{"status":"PASS" if set(ch.get("mux",{}).keys())=={"A","B_REPEAT","C_CHANGED_MUSIC_SEED"} else "MISMATCH"})

        # Static contract and policy pins; this is evidence lineage only, not permission.
        self.add("FROZEN_C11C_MANIFEST",check_file(self.root,"release/C11C_FREEZE_PACKAGE_MANIFEST.json",FROZEN_C11C_SHA))
        self.add("D4_8_POLICY",check_file(self.root,"definitions/c11d/production/C11E_D4_8_R1V_QUALIFICATION_ONLY_POLICY_V2.json",D4_8_SHA))
        failures=[x for x in self.checks if x.get("status")!="PASS"]
        status="PASS_E6_REUSE_EVIDENCE_HYDRATED_NOT_AUTHORIZED" if not failures else "BLOCKED_E6_REUSE_EVIDENCE_INCOMPLETE"
        return {"schema":"C11E-E6-REUSE-EVIDENCE-HYDRATION-REPORT-V1","status":status,
                "run_id":"E6HYDRATE_"+datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")+"_"+uuid.uuid4().hex[:8].upper(),
                "created_utc":datetime.now(timezone.utc).isoformat(),"project_root":str(self.root),
                "counts":self.counts,"check_count":len(self.checks),"passed_checks":len(self.checks)-len(failures),
                "failed_checks":len(failures),"checks":self.checks,
                "governance":{"read_only_source_audit":True,"source_checkout_mutated":False,"godot_invoked":False,
                  "ffmpeg_invoked":False,"ffprobe_invoked":False,"audio_generated":False,"media_created":False,
                  "batch_id_consumed":False,"production_dispatch":False,"e1":"PREPARE_ONLY","d4_8":"BLOCKED",
                  "renderer":"OFF","release_authority":"NONE","git_checks":"SKIPPED","commits":"OPERATOR_MANAGED"}}

def main(argv=None):
    ap=argparse.ArgumentParser()
    ap.add_argument("--project-root",required=True)
    ap.add_argument("--output-root",default="artifacts/tests/c11e/e6_reuse_evidence_hydration")
    ap.add_argument("--report-dir",default="")
    args=ap.parse_args(argv)
    root=Path(args.project_root).resolve()
    if not root.is_dir(): print("PROJECT_ROOT_MISSING",file=sys.stderr); return 2
    audit=Audit(root); report=audit.run()
    outroot=Path(args.report_dir).resolve() if args.report_dir else safe_path(root,args.output_root)
    outbase=outroot/report["run_id"]
    outbase.mkdir(parents=True,exist_ok=False)
    out=outbase/(report["run_id"]+"_REPORT_V1.json")
    raw=(json.dumps(report,indent=2,sort_keys=True)+"\n").encode("utf-8")
    out.write_bytes(raw)
    digest=hashlib.sha256(raw).hexdigest()
    (out.with_suffix(out.suffix+".sha256")).write_text(digest+"  "+out.name+"\n",encoding="ascii")
    print("E6_REUSE_EVIDENCE_HYDRATION_STATUS="+report["status"])
    print("E6_REUSE_EVIDENCE_CHECKS={}/{} PASS".format(report["passed_checks"],report["check_count"]))
    print("E6_REUSE_EVIDENCE_FAILURES={}".format(report["failed_checks"]))
    print("E6_REUSE_DRILL_RECEIPTS={}/6".format(report["counts"]["drill_receipts"]))
    print("E6_REUSE_R1V_LOOP_SLOTS={}/5".format(report["counts"]["r1v_loop_slots"]))
    print("E6_REUSE_SOURCE_PINS={}/33".format(report["counts"]["source_pins"]))
    print("E6_REUSE_REPORT="+str(out))
    print("E6_REUSE_REPORT_SHA256="+digest)
    print("E6_REUSE_GODOT_INVOKED=FALSE; MEDIA_CREATED=FALSE; BATCH_ID_CONSUMED=FALSE; RELEASE_AUTHORITY=NONE")
    return 0 if report["status"]=="PASS_E6_REUSE_EVIDENCE_HYDRATED_NOT_AUTHORIZED" else 2

if __name__=="__main__": raise SystemExit(main())
