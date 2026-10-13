from __future__ import annotations
import ast
import hashlib
import json
import sys
import tempfile
from pathlib import Path
from types import SimpleNamespace

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import d_renderer_visual_drill_selector_authoring_coverage as module


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _fake_receipts(root: Path, matrix: list[dict]) -> list[dict]:
    rows=[]
    for item in matrix:
        fam=item["selection"]["family_id"]
        tier=item["selection"]["variant_id"]
        core={"family":fam,"tier":tier,"seed":12345}
        alt={"family":fam,"tier":tier,"seed":54321}
        base=module._sha_json(core); alt_hash=module._sha_json(alt)
        visual=module._sha_json({"visual":core}); visual_alt=module._sha_json({"visual":alt})
        rows.append({**item,"base_seed":12345,"alternate_seed":54321,
            "payload_sha256":base,"repeat_payload_sha256":base,"alternate_seed_payload_sha256":alt_hash,
            "visual_state_sha256":visual,"repeat_visual_state_sha256":visual,"alternate_seed_visual_state_sha256":visual_alt,
            "deterministic_repeat_pass":True,"visual_seed_change_observed":True,
            "selection_identity_matches":True,"policy_tier_resolved":True})
    return rows


def run_checks():
    contract,schema,lineage=module._validate_contract_sources(ROOT)
    assert len(lineage)==24 and lineage[0]["path"]=="release/C11C_FREEZE_PACKAGE_MANIFEST.json"
    assert len({row["path"] for row in lineage})==24
    import jsonschema
    jsonschema.Draft202012Validator.check_schema(schema)
    matrix=module._canonical_catalog(ROOT,contract)
    assert len(matrix)==20
    assert {row["selection"]["family_id"] for row in matrix}==set(module.EXPECTED_FAMILIES)
    assert {row["selection"]["variant_id"] for row in matrix}=={f"tier-{tier}" for tier in module.EXPECTED_TIERS}
    assert len({(row["selection"]["family_id"],row["selection"]["variant_id"]) for row in matrix})==20
    assert {row["canonical_duration_seconds"] for row in matrix}=={17.0,21.0}
    report=module._build_report(contract,lineage,matrix,_fake_receipts(ROOT,matrix),schema)
    assert report["catalog_summary"]["selector_count"]==20
    assert report["catalog_summary"]["dynamic_request_payload_binding"]=="NOT_COVERED_BY_THIS_AUDIT"
    assert report["governance"]["renderer_activation"]=="OFF" and report["governance"]["freeze_eligible"] is False
    assert report["report_sha256"]==module._sha_json({k:v for k,v in report.items() if k!="report_sha256"})

    # Missing, duplicate, wrong-tier, false determinism and seed influence must fail closed.
    good=_fake_receipts(ROOT,matrix)
    for name,mutation in [
        ("missing selector",lambda rows: rows.pop()),
        ("duplicate selector",lambda rows: rows.__setitem__(1,dict(rows[0]))),
        ("unsupported tier",lambda rows: rows[0]["selection"].update(variant_id="tier-6")),
        ("payload non-determinism",lambda rows: rows[0].update(repeat_payload_sha256="0"*64)),
        ("seed has no effect",lambda rows: rows[0].update(alternate_seed_visual_state_sha256=rows[0]["visual_state_sha256"])),
        ("source drift",lambda rows: rows[0].update(canonical_source_sha256="0"*64)),
    ]:
        rows=json.loads(json.dumps(good)); mutation(rows)
        try: module._validate_runtime_receipts(rows,matrix,module._sha_json(lineage))
        except module.VisualDrillCoverageError: pass
        else: raise AssertionError(f"Expected fail-closed rejection: {name}")

    # Runtime runner and Godot harness must not introduce rendering/persistence/dispatch paths.
    tree=ast.parse((HERE/'d_renderer_visual_drill_selector_authoring_coverage.py').read_text(encoding='utf-8'))
    for node in ast.walk(tree):
        if isinstance(node,ast.Call) and isinstance(node.func,ast.Attribute):
            assert node.func.attr not in {"write_text","write_bytes","unlink","mkdir","makedirs","remove","rename","replace"}, f"runner persistence/mutation call: {node.func.attr}"
    harness=(ROOT/module.HARNESS_REL).read_text(encoding='utf-8')
    # Godot JSON arrays are untyped Variants; normalize them before comparing to typed constants.
    for required_guard in (
        'var family_ids_value: Variant = matrix.get("family_ids", null)',
        'var tiers_value: Variant = matrix.get("tiers", null)',
        'var matrix_family_ids: Array[String] = []',
        'var matrix_tiers: Array[int] = []',
        'for family_index in range(EXPECTED_FAMILIES.size()):',
        'for tier_index in range(EXPECTED_TIERS.size()):',
    ):
        assert required_guard in harness, f"missing normalized matrix guard: {required_guard}"
    assert 'matrix.get("family_ids", []) != EXPECTED_FAMILIES' not in harness
    assert 'matrix.get("tiers", []) != EXPECTED_TIERS' not in harness
    for forbidden in ["FileAccess.WRITE","store_buffer(","store_string(","FFmpeg","SubViewport","RenderingServer","rendering_device","renderer_native_input_emitted = true","renderer_dispatch_invoked = true"]:
        assert forbidden not in harness, f"unexpected rendering/persistence path: {forbidden}"

    # A disposable mirror with modified source bytes must be rejected by the source pin check.
    with tempfile.TemporaryDirectory(prefix="c11d_visual_drill_coverage_drift_") as tmp:
        mirror=Path(tmp)
        for row in lineage:
            src=ROOT/row["path"]; dst=mirror/row["path"]
            dst.parent.mkdir(parents=True,exist_ok=True); dst.write_bytes(src.read_bytes())
        for rel in (module.CONTRACT_REL.as_posix(),module.SCHEMA_REL.as_posix()):
            src=ROOT/rel; dst=mirror/rel
            dst.parent.mkdir(parents=True,exist_ok=True); dst.write_bytes(src.read_bytes())
        drift=mirror/"profiles/difficulty/visual_drill_tracking.json"
        drift.write_bytes(drift.read_bytes()+b"\n")
        try: module._validate_contract_sources(mirror)
        except module.VisualDrillCoverageError as exc: assert "Pinned source drift" in str(exc)
        else: raise AssertionError("Pinned difficulty-profile drift must fail closed")
    return {"source_pins":len(lineage),"families":4,"selectors":len(matrix),"durations":2,"negative":6,"source_drift":1,"renderer_boundary":1}

if __name__=="__main__":
    counts=run_checks()
    print("C11-D VISUAL DRILL SELECTOR AUTHORING COVERAGE CONTRACT PASS | source_pins=%d/%d | families=%d/4 | canonical_selectors=%d/20 | canonical_durations=%d | fail_closed_negatives=%d/6 | source_drift=1/1 | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE" % (counts["source_pins"],counts["source_pins"],counts["families"],counts["selectors"],counts["durations"],counts["negative"]))
