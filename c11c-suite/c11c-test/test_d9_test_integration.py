from __future__ import annotations
import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MAIN = ROOT / "c11c-suite/c11c-test/main.py"
MANIFEST = ROOT / "c11c-suite/c11c-test/BUILD_MANIFEST.json"
SHELL = ROOT / "c11c-suite/main.py"

REQUIRED_ROUTES = {
    "D2 ASSET FAMILY / BINDING REGISTRY": ("ps", "tools/c11d/d2/validate_d2_1_registry.ps1"),
    "D2 ASSET ROLE / EVIDENCE": ("ps", "tools/c11d/d2/validate_d2_2_asset_role_evidence_v2.ps1"),
    "D3 MUSIC V5 DETERMINISM": ("ps", "tools/c11d/d3/run_d3_2_deterministic_music.ps1"),
    "D4 REQUEST / PERSONALIZATION ACCEPTANCE": ("python", "tools/c11d/d4/d4_full_acceptance.py"),
    "D4 GUI/CLI PLAN PARITY": ("ps", "tools/c11d/d4/run_d4_7_gui_cli_parity.ps1"),
    "D4.8 ACTIVATION GOVERNANCE (BLOCKED GATE)": ("ps", "tools/c11d/d4/run_d4_8_activation_governance.ps1"),
    "D5 PROVENANCE / ARTIFACT LIFECYCLE": ("python", "tools/c11d/d5/full_d5_acceptance.py"),
    "D6 SEED GOVERNANCE / ISOLATION": ("python", "tools/c11d/d6/full_d6_acceptance.py"),
    "D7 CATALOG IDENTITY / PROVENANCE": ("ps", "tools/c11d/d7/run_d7_4_catalog_identity_provenance.ps1"),
    "CATALOG 0.2.0 SELF-TEST": ("python", "./c11c-suite/c11c-catalog/self_test.py"),
    "D8 VISUAL MEDIA QA": ("ps", "tools/c11d/d8/run_d8_2_visual_qa.ps1"),
    "D8 AUDIO MEDIA QA": ("ps", "tools/c11d/d8/run_d8_3_audio_qa.ps1"),
    "D8 RELEASE DRY-RUN (NO RELEASE)": ("ps", "tools/c11d/d8/run_d8_6_release_dry_run.ps1"),
    "D9.8 UNIVERSAL EDITORIAL MODEL": ("python", "tools/c11d/d9/test_universal_editorial_model.py"),
    "D9.9 UNIVERSAL PRODUCER / GUI-CLI": ("python", "tools/c11d/d9/test_universal_producer.py"),
    "D9.10 EDITORIAL-RENDER BRIDGE (PLAN ONLY)": ("python", "tools/c11d/d9/test_editorial_render_bridge.py"),
    "D9.11 MAINTENANCE 0.2.0": ("python", "tools/c11d/d9/test_maintenance.py"),
    "D9 NEGATIVE ACCEPTANCE BUNDLE": ("python", "tools/c11d/d9/test_d9_negative_acceptance.py"),
    "D9 GUI/CLI PARITY BUNDLE": ("python", "tools/c11d/d9/test_d9_gui_cli_parity.py"),
    "D9 REAL-MEDIA GUI CERTIFICATION PREFLIGHT (NO MEDIA)": ("python", "tools/c11d/d9/test_gui_e2e_certification_plan.py"),
    "D9.12 TEST 0.2.0 INTEGRATION CONTRACT": ("python", "./c11c-suite/c11c-test/test_d9_test_integration.py"),
    "D9.13 CROSS-SUITE LIFECYCLE CHAIN": ("python", "tools/c11d/d9/test_cross_suite_lifecycle.py"),
}


def parse_assign(tree: ast.AST, name: str):
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name for t in node.targets):
            return ast.literal_eval(node.value)
    raise AssertionError(f"Registry {name} not found")


def run_checks() -> dict[str, int]:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8-sig"))
    if manifest.get("suite_id") != "c11c-test" or manifest.get("version") != "0.2.0":
        raise AssertionError("c11c-test BUILD_MANIFEST identity/version mismatch")
    if manifest.get("renderer_activation") is not False or manifest.get("media_creation") is not False or manifest.get("release_authority") != "NONE":
        raise AssertionError("Test 0.2.0 governance flags drifted")
    source = MAIN.read_text(encoding="utf-8-sig")
    rows = parse_assign(ast.parse(source), "C11_COMMANDS")
    by_name = {row[0]: row for row in rows}
    if len(by_name) != len(rows):
        raise AssertionError("Duplicate C11_COMMANDS route names")
    missing = sorted(set(REQUIRED_ROUTES) - set(by_name))
    if missing:
        raise AssertionError(f"Required D routes missing from Test GUI: {missing}")
    for name, (kind, expected_path) in REQUIRED_ROUTES.items():
        row = by_name[name]
        if row[1] != kind or not row[2] or row[2][0].replace("\\", "/") != expected_path:
            raise AssertionError(f"Route target drift: {name}: {row[1:]}")
        candidate = (ROOT / expected_path.removeprefix("./")).resolve()
        if not candidate.is_file() or ROOT.resolve() not in candidate.parents:
            raise AssertionError(f"Route target missing/outside repository: {name} -> {candidate}")
    route_names = set(by_name)
    if "D9 REAL-MEDIA GUI CERTIFICATION PREFLIGHT (NO MEDIA)" not in route_names:
        raise AssertionError("Real-media GUI certification preflight route not registered")
    cert_row = by_name["D9 REAL-MEDIA GUI CERTIFICATION PREFLIGHT (NO MEDIA)"]
    if "no-media" not in cert_row[3].lower() and "no media" not in cert_row[3].lower():
        raise AssertionError("GUI certification route must be explicit that it does not create media")
    shell_rows = parse_assign(ast.parse(SHELL.read_text(encoding="utf-8-sig")), "APPS")
    expected_surfaces = {
        "c11c-test/main.py", "c11c-producer/main.py", "c11c-catalog/main.py",
        "c11c-config/main.py", "c11c-maintenance/main.py",
    }
    if len(shell_rows) != 5 or {row[1] for row in shell_rows} != expected_surfaces:
        raise AssertionError("C11C Suite topology must remain exactly the five canonical surfaces")
    if any("c11d-control" in str(row).lower() for row in rows):
        raise AssertionError("Legacy c11d-control must not be exposed in Test routes")
    for rel in manifest.get("tests", []):
        if not (ROOT / rel).is_file():
            raise AssertionError(f"Manifest test missing: {rel}")
    manifest_route_names = {route["name"] for route in manifest.get("gui_routes", [])}
    if manifest_route_names != set(REQUIRED_ROUTES):
        raise AssertionError("Build manifest GUI route index does not match the Test GUI registry")
    return {"routes": len(REQUIRED_ROUTES), "all_routes": len(rows), "surfaces": len(shell_rows), "tests": len(manifest.get("tests", []))}


if __name__ == "__main__":
    counts = run_checks()
    print(
        "C11C_TEST_GUI_CONTRACT PASS | version=0.2.0 | "
        f"D2-D9 routes={counts['routes']}/{counts['routes']} | all_gui_routes={counts['all_routes']} | "
        f"canonical_surfaces={counts['surfaces']}/5 | manifest_tests={counts['tests']} | "
        "renderer=false | media_created=false | release_authority=NONE"
    )
