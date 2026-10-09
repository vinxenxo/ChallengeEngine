"""Automated offscreen runtime acceptance for the existing C11-D test/operator GUI.

Instantiates the real PySide6 Producer MainWindow, selects Challenge/Loop/Drill,
clicks the existing plan/bridge action, and audits each resulting request/plan/bridge/
D-only adapter envelope. It requires no screenshots and never invokes renderer/media
production. The Qt runtime is exercised offscreen; this is not the definitive GUI.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import re
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

EXPECTED_C11C_MANIFEST_SHA256 = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
CONTENT_TYPES = ("challenges", "visual_loops", "visual_drills")
REQUIRED_ARTIFACTS = (
    "canonical_request.json",
    "editorial_resolution.json",
    "universal_plan.json",
    "editorial_render_bridge_plan.json",
    "d_render_adapter_envelope.json",
    "d4_subplan_evidence.json",
    "gui_cli_parity.json",
    "producer_universal_receipt.json",
    "cross_suite_lifecycle_receipt.json",
)


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def _validate_run_id(value: str) -> str:
    value = value.strip()
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{2,79}", value):
        raise ValueError("run-id must be 3-80 simple filename characters")
    return value


def _load_producer_main(root: Path):
    producer_dir = root / "c11c-suite" / "c11c-producer"
    d9_dir = root / "tools" / "c11d" / "d9"
    for path in (str(producer_dir), str(d9_dir)):
        if path not in sys.path:
            sys.path.insert(0, path)
    module_path = producer_dir / "main.py"
    spec = importlib.util.spec_from_file_location("c11d_d910_runtime_test_producer_main", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load test GUI entrypoint: {module_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _run_gui_cases(root: Path) -> list[dict[str, Any]]:
    # Deliberately force Qt's offscreen platform: no screenshots or visible operator UI
    # are needed to exercise the real widget signals and callback path.
    os.environ["QT_QPA_PLATFORM"] = "offscreen"
    os.environ["C11C_PROJECT_ROOT"] = str(root)

    try:
        from PySide6.QtWidgets import QApplication
    except Exception as exc:
        raise RuntimeError(f"PySide6 unavailable; cannot exercise real Qt GUI runtime: {exc}") from exc

    app = QApplication.instance() or QApplication(["C11D-D9.10-runtime-acceptance"])
    app.setQuitOnLastWindowClosed(False)
    module = _load_producer_main(root)
    from d_render_adapter import validate_d_only_adapter_envelope
    warnings: list[str] = []

    class _NonModalMessageBox:
        @staticmethod
        def warning(_parent, title, message, *_args, **_kwargs):
            warnings.append(f"{title}: {message}")
            return 0

    # Prevent a failing callback from blocking unattended acceptance on a modal warning.
    module.QMessageBox = _NonModalMessageBox
    window = None
    results: list[dict[str, Any]] = []
    try:
        window = module.MainWindow()
        window.show()
        app.processEvents()
        if not hasattr(window, "d9_validate") or not hasattr(window, "d9_adapter_view"):
            raise RuntimeError("Test GUI does not expose the D9.10 plan/adapter controls")

        for content_type in CONTENT_TYPES:
            warning_start = len(warnings)
            index = window.d9_content_type.findData(content_type)
            if index < 0:
                raise RuntimeError(f"Test GUI has no selector entry for {content_type}")
            window.d9_content_type.setCurrentIndex(index)
            app.processEvents()

            # Keep an explicit editorial mutation in the GUI for every type; values must
            # arrive through the canonical plan and the D-only binding-preview envelope.
            if not window.d9_personalization.isChecked():
                window.d9_personalization.setChecked(True)
            override_index = window.d9_scope.findData("production_override")
            if override_index >= 0:
                window.d9_scope.setCurrentIndex(override_index)
            app.processEvents()
            title = f"D9.10 runtime acceptance · {content_type}"
            window.d9_title.setText(title)
            window.d9_seed.setValue(41001 + len(results))
            window.d9_music_seed.setValue(840101 + len(results))
            if window.d9_seed.value() == window.d9_music_seed.value():
                raise RuntimeError(f"Seed domains crossed for {content_type}")

            window.d9_validate.click()
            app.processEvents()
            if len(warnings) != warning_start:
                raise RuntimeError(f"Qt GUI callback raised a modal warning for {content_type}: {warnings[-1]}")
            status_text = window.statusBar().currentMessage()
            if "LIFECYCLE PASS" not in status_text or content_type not in status_text:
                raise RuntimeError(f"GUI callback did not report lifecycle PASS for {content_type}: {status_text}")

            label = window.d9_evidence_label.text()
            prefix = "Evidencia D9.9/D9.10/D9.13 (adaptador preparado, dispatch OFF): "
            if not label.startswith(prefix) or " · lifecycle=" not in label:
                raise RuntimeError(f"GUI evidence label does not identify the generated run root for {content_type}")
            run_root = Path(label[len(prefix):].split(" · lifecycle=", 1)[0]).resolve()
            try:
                run_root.relative_to(root.resolve())
            except ValueError as exc:
                raise RuntimeError(f"GUI evidence path escaped repository root: {run_root}") from exc
            if not run_root.is_dir():
                raise RuntimeError(f"GUI evidence run directory missing: {run_root}")
            missing = [name for name in REQUIRED_ARTIFACTS if not (run_root / name).is_file()]
            if missing:
                raise RuntimeError(f"GUI evidence package incomplete for {content_type}: {missing}")

            def read_json(name: str) -> dict[str, Any]:
                payload = json.loads((run_root / name).read_text(encoding="utf-8-sig"))
                if not isinstance(payload, dict):
                    raise RuntimeError(f"Expected JSON object: {run_root / name}")
                return payload

            request = read_json("canonical_request.json")
            plan = read_json("universal_plan.json")
            bridge = read_json("editorial_render_bridge_plan.json")
            envelope = read_json("d_render_adapter_envelope.json")
            parity = read_json("gui_cli_parity.json")
            if validate_d_only_adapter_envelope(envelope, root) is not True:
                raise RuntimeError(f"D-only adapter envelope validation failed for {content_type}")
            receipt = read_json("producer_universal_receipt.json")
            if request.get("selection", {}).get("content_type") != content_type:
                raise RuntimeError(f"Canonical request content type mismatch for {content_type}")
            if plan.get("selection", {}).get("content_type") != content_type:
                raise RuntimeError(f"Canonical plan content type mismatch for {content_type}")
            if bridge.get("content_type") != content_type or envelope.get("content_identity", {}).get("content_type") != content_type:
                raise RuntimeError(f"Bridge/adapter content identity mismatch for {content_type}")
            if envelope.get("binding_preview", {}).get("editorial_bindings", {}).get("title") != title:
                raise RuntimeError(f"GUI editorial override did not reach the D-only envelope for {content_type}")
            if parity.get("status") != "PASS" or not all(parity.get("checks", {}).values()):
                raise RuntimeError(f"GUI/CLI parity failed for {content_type}")
            expected_locks = {
                "status": "PREPARED_NOT_DISPATCHED_RENDERER_DISABLED",
                "renderer_dispatch_invoked": False,
                "renderer_input_emitted": False,
                "renderer_activation": False,
                "production_execution": False,
                "media_output_created": False,
                "output_artifact_path": None,
                "d4_8": "BLOCKED",
                "release_authority": "NONE",
                "c11c_source_mutation": False,
            }
            for key, expected in expected_locks.items():
                if envelope.get(key) != expected:
                    raise RuntimeError(f"D-only adapter governance lock mismatch for {content_type}: {key}")
            if receipt.get("result") != "PASS_BRIDGE_PLANNING_ONLY" or receipt.get("renderer_dispatch_invoked") is not False:
                raise RuntimeError(f"Producer receipt does not confirm prepare-only behavior for {content_type}")

            results.append({
                "content_type": content_type,
                "status": "PASS",
                "request_id": request.get("request_id"),
                "run_root": run_root.relative_to(root).as_posix(),
                "request_hash": parity.get("gui_request_hash"),
                "plan_hash": parity.get("gui_plan_hash"),
                "bridge_record_hash": parity.get("bridge_record_hash"),
                "d_only_adapter_envelope_hash": parity.get("d_only_adapter_envelope_hash"),
                "editorial_override_propagated": True,
                "gui_cli_parity": "PASS",
                "renderer_dispatch_invoked": False,
                "media_output_created": False,
            })
    finally:
        if window is not None:
            window.close()
            app.processEvents()
        app.quit()
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-id", default="D910_QT_" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"))
    parser.add_argument("--output-root", default="artifacts/tests/c11d_d9/d910_gui_runtime_acceptance")
    args = parser.parse_args()
    run_id = _validate_run_id(args.run_id)
    root = Path(__file__).resolve().parents[3]
    output_base = (root / args.output_root).resolve()
    try:
        output_base.relative_to(root.resolve())
    except ValueError:
        parser.error("output-root must stay within the repository")
    run_root = output_base / run_id
    if run_root.exists():
        parser.error(f"run output already exists; choose a new --run-id: {run_root}")
    run_root.mkdir(parents=True, exist_ok=False)

    manifest_path = root / "release" / "C11C_FREEZE_PACKAGE_MANIFEST.json"
    manifest_hash = _sha256_bytes(manifest_path.read_bytes()) if manifest_path.is_file() else None
    started = datetime.now(timezone.utc).isoformat()
    results: list[dict[str, Any]] = []
    error = None
    try:
        results = _run_gui_cases(root)
    except Exception as exc:
        error = f"{type(exc).__name__}: {exc}"
        (run_root / "exception.txt").write_text(traceback.format_exc(), encoding="utf-8")

    all_pass = len(results) == len(CONTENT_TYPES) and all(item.get("status") == "PASS" for item in results)
    manifest_match = manifest_hash == EXPECTED_C11C_MANIFEST_SHA256
    report: dict[str, Any] = {
        "schema": "C11-D-D9.10-QT-GUI-RUNTIME-ACCEPTANCE-V1",
        "schema_version": "1.0",
        "run_id": run_id,
        "started_at_utc": started,
        "completed_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": "PASS" if all_pass and manifest_match else "FAIL",
        "scope": "Offscreen runtime exercise of the existing test/operator Producer Qt window; three content types, explicit editorial override propagation, GUI/CLI parity, D-only adapter locks; no screenshots or media.",
        "qt_gui_runtime_exercised": bool(all_pass),
        "operator_interactive_visual_observation": False,
        "screenshots_required": False,
        "checks": results,
        "error": error,
        "governance": {
            "c11c_frozen_manifest_sha256": manifest_hash,
            "c11c_frozen_manifest_expected_sha256": EXPECTED_C11C_MANIFEST_SHA256,
            "c11c_frozen_manifest_match": manifest_match,
            "supported_content_types": list(CONTENT_TYPES),
            "content_type_checks": f"{len(results)}/{len(CONTENT_TYPES)}",
            "editorial_override_propagation_required": True,
            "qt_platform": "offscreen",
            "screenshot_collection_required": False,
            "renderer_dispatch_invoked": False,
            "renderer_input_emitted": False,
            "renderer_activation": False,
            "production_execution": False,
            "media_output_created": False,
            "d4_8": "BLOCKED",
            "release_authority": "NONE",
            "definitive_gui": "DEFERRED_UNTIL_FINAL_D_BASELINE_FROZEN",
        },
        "outputs": {
            "relative_run_root": run_root.relative_to(root).as_posix(),
            "report_file": "D9_10_QT_GUI_RUNTIME_ACCEPTANCE_REPORT.json",
            "media_created": False,
        },
    }
    report["report_hash"] = hashlib.sha256(_canonical(report).encode("utf-8")).hexdigest()
    (run_root / "D9_10_QT_GUI_RUNTIME_ACCEPTANCE_REPORT.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(
        "C11-D D9.10 QT GUI RUNTIME ACCEPTANCE " + report["status"]
        + f" | content_types={len(results)}/{len(CONTENT_TYPES)}"
        + f" | C11-C_manifest_match={str(manifest_match).lower()}"
        + f" | screenshots=NOT_REQUIRED | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE"
        + f" | report={run_root.relative_to(root).as_posix()}/D9_10_QT_GUI_RUNTIME_ACCEPTANCE_REPORT.json"
    )
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
