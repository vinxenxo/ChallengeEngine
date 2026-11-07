#!/usr/bin/env python3
"""Verify and repackage an existing C11-E E4B R1P run without rerunning Godot."""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
import os
import re
import sys
import zipfile
from pathlib import Path, PurePosixPath
from typing import Any

EXPECTED_RUN_ID = "E4B_R1P_20261107_032743_5F75045C"
EXPECTED_REPORT_STATUS = "PASS_R1P_PARAMETER_PAYLOADS_27_OF_27"
EXPECTED_PREPARE_STATUS = "PASS_D9_9_D9_10_PARENT_PREPARATION_27_OF_27"
EXPECTED_FROZEN_MANIFEST_SHA256 = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
EXPECTED_STATIC_AUDIT_SHA256 = "600c22dafe2e377cb02b4a69f8823a44745d705b71cdb0d6bcec38da52df3e92"
EMPTY_SHA256 = hashlib.sha256(b"").hexdigest()


class VerificationError(RuntimeError):
    pass


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def canonical(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(k): canonical(value[k]) for k in sorted(value, key=lambda item: str(item))}
    if isinstance(value, (list, tuple)):
        return [canonical(v) for v in value]
    return value


def canonical_json(value: Any) -> str:
    return json.dumps(canonical(value), ensure_ascii=False, separators=(",", ":"), allow_nan=False)


def canonical_sha256(value: Any) -> str:
    return sha256_bytes(canonical_json(value).encode("utf-8"))


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:  # noqa: BLE001 - report exact artifact failure
        raise VerificationError(f"Invalid JSON at {path}: {exc}") from exc


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def sidecar_token(path: Path) -> str:
    require(path.is_file(), f"Missing SHA-256 sidecar: {path}")
    tokens = path.read_text(encoding="ascii").strip().split()
    require(bool(tokens) and re.fullmatch(r"[0-9a-f]{64}", tokens[0]) is not None,
            f"Malformed SHA-256 sidecar: {path}")
    return tokens[0]


def verify_raw_sidecar(target: Path, sidecar: Path) -> str:
    observed = sha256_file(target)
    expected = sidecar_token(sidecar)
    require(observed == expected, f"Raw-byte SHA-256 mismatch: {target.name}")
    return observed


def verify_process_log(output_dir: Path, process_receipt: dict[str, Any], key: str,
                       stdout_name: str, stderr_name: str) -> dict[str, Any]:
    item = process_receipt.get(key)
    require(isinstance(item, dict), f"Missing process evidence: {key}")
    require(int(item.get("exit_code", -1)) == 0, f"Non-zero process exit: {key}")
    stdout_path = output_dir / stdout_name
    stderr_path = output_dir / stderr_name
    require(stdout_path.is_file() and stderr_path.is_file(), f"Missing captured logs for {key}")
    stdout_hash = sha256_file(stdout_path)
    stderr_hash = sha256_file(stderr_path)
    require(stdout_hash == item.get("stdout_sha256"), f"stdout SHA mismatch: {key}")
    require(stderr_hash == item.get("stderr_sha256"), f"stderr SHA mismatch: {key}")
    return {"exit_code": 0, "stdout_sha256": stdout_hash, "stderr_sha256": stderr_hash}


def normalized_archive_name(name: str) -> str:
    return name.replace("\\", "/").lstrip("/")


def verify_archive_matches_output(archive_path: Path, output_dir: Path) -> dict[str, Any]:
    require(archive_path.is_file(), f"Original R1P archive is missing: {archive_path}")
    local_files = sorted(p for p in output_dir.rglob("*") if p.is_file())
    expected_names = {p.relative_to(output_dir).as_posix() for p in local_files}
    require(len(local_files) >= 70, f"Output folder unexpectedly sparse: {len(local_files)} files")
    with zipfile.ZipFile(archive_path, "r") as archive:
        corrupt = archive.testzip()
        require(corrupt is None, f"Original ZIP CRC failure: {corrupt}")
        entries = [info for info in archive.infolist() if not info.is_dir()]
        normalized = [normalized_archive_name(info.filename) for info in entries]
        require(len(normalized) == len(set(normalized)), "Original ZIP has duplicate paths after separator normalization")
        observed_names = set(normalized)
        require(observed_names == expected_names,
                f"Original ZIP entry set differs from run folder: ZIP={len(observed_names)} folder={len(expected_names)}")
        entry_by_normalized = {normalized_archive_name(info.filename): info for info in entries}
        for path in local_files:
            name = path.relative_to(output_dir).as_posix()
            archived = archive.read(entry_by_normalized[name])
            require(sha256_bytes(archived) == sha256_file(path), f"Original ZIP member bytes differ: {name}")
        selector_receipts = [n for n in normalized if re.fullmatch(r"receipts/[^/]+\.json", n)]
        receipt_sidecars = [n for n in normalized if re.fullmatch(r"receipts/[^/]+\.json\.sha256", n)]
        backslash_entries = sum("\\" in info.filename for info in entries)
        require(len(selector_receipts) == 27, f"Original ZIP normalized selector receipt count is {len(selector_receipts)}, expected 27")
        require(len(receipt_sidecars) == 27, f"Original ZIP normalized receipt sidecar count is {len(receipt_sidecars)}, expected 27")
        return {
            "path": str(archive_path),
            "sha256": sha256_file(archive_path),
            "entry_count": len(entries),
            "normalized_selector_receipt_count": len(selector_receipts),
            "normalized_receipt_sidecar_count": len(receipt_sidecars),
            "entries_with_backslash_separator": backslash_entries,
            "path_separator_false_negative_reproduced": backslash_entries > 0,
            "byte_for_byte_member_match": True,
        }


def create_recovered_archive(output_dir: Path, recovered_path: Path) -> dict[str, Any]:
    require(not recovered_path.exists(), f"Recovered archive collision; refusing overwrite: {recovered_path}")
    local_files = sorted(p for p in output_dir.rglob("*") if p.is_file())
    expected_names = {p.relative_to(output_dir).as_posix() for p in local_files}
    recovered_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with zipfile.ZipFile(recovered_path, "x", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
            for path in local_files:
                archive.write(path, arcname=path.relative_to(output_dir).as_posix())
        with zipfile.ZipFile(recovered_path, "r") as archive:
            corrupt = archive.testzip()
            require(corrupt is None, f"Recovered ZIP CRC failure: {corrupt}")
            names = [info.filename for info in archive.infolist() if not info.is_dir()]
            require(all("\\" not in name for name in names), "Recovered ZIP still contains a backslash path separator")
            require(set(names) == expected_names, "Recovered ZIP entry set differs from R1P output folder")
            receipts = [n for n in names if re.fullmatch(r"receipts/[^/]+\.json", n)]
            sidecars = [n for n in names if re.fullmatch(r"receipts/[^/]+\.json\.sha256", n)]
            require(len(receipts) == 27 and len(sidecars) == 27,
                    f"Recovered ZIP counts invalid: receipts={len(receipts)} sidecars={len(sidecars)}")
            for path in local_files:
                name = path.relative_to(output_dir).as_posix()
                require(sha256_bytes(archive.read(name)) == sha256_file(path), f"Recovered ZIP member mismatch: {name}")
    except Exception:
        if recovered_path.exists():
            recovered_path.unlink()
        raise
    return {
        "path": str(recovered_path),
        "sha256": sha256_file(recovered_path),
        "bytes": recovered_path.stat().st_size,
        "entry_count": len(local_files),
        "selector_receipt_count": 27,
        "receipt_sidecar_count": 27,
        "slash_normalized": True,
        "byte_for_byte_member_match": True,
    }


def verify_run(project_root: Path, run_id: str) -> dict[str, Any]:
    require(sys.version_info[:2] == (3, 13), f"Python 3.13 required; running {sys.version.split()[0]}")
    require(re.fullmatch(r"E4B_R1P_[A-Z0-9_]+", run_id) is not None, "Unsafe run ID")
    output_dir = project_root / "artifacts" / "tests" / "c11e" / "e4b_r1p" / run_id
    require(output_dir.is_dir(), f"R1P output directory not found: {output_dir}")
    require(output_dir.resolve().is_relative_to(project_root.resolve()), "Output directory escapes ProjectRoot")

    report_path = output_dir / "r1p_report.json"
    prepare_path = output_dir / "prepare_report.json"
    parent_path = output_dir / "parent_bindings.json"
    source_manifest_path = output_dir / "source_manifest.json"
    process_path = output_dir / "runner_process_receipt.json"
    for path in (report_path, prepare_path, parent_path, source_manifest_path, process_path):
        require(path.is_file(), f"Required R1P evidence missing: {path.name}")

    report = load_json(report_path)
    stored_report_hash = report.get("report_sha256")
    report_for_hash = dict(report)
    report_for_hash.pop("report_sha256", None)
    observed_report_hash = canonical_sha256(report_for_hash)
    require(stored_report_hash == observed_report_hash, "R1P aggregate report canonical SHA-256 mismatch")
    require(sidecar_token(output_dir / "r1p_report.sha256") == observed_report_hash,
            "R1P aggregate report sidecar mismatch")
    require(report.get("status") == EXPECTED_REPORT_STATUS, "R1P report status is not PASS 27/27")
    require(report.get("run_id") == run_id, "R1P report run_id mismatch")
    require(report.get("case_count") == 27 and report.get("grammar_count") == 27
            and report.get("family_count") == 5 and report.get("receipt_count") == 27,
            "R1P report counts are not 27 cases / 27 grammars / 5 families")

    prepare = load_json(prepare_path)
    parents = load_json(parent_path)
    source_manifest = load_json(source_manifest_path)
    process = load_json(process_path)
    require(prepare.get("status") == EXPECTED_PREPARE_STATUS and prepare.get("run_id") == run_id,
            "D9.9/D9.10 preparation report is not PASS 27/27")
    require(parents.get("run_id") == run_id and len(parents.get("cases", [])) == 27,
            "D9.9/D9.10 parent bindings do not contain 27 cases")
    require(source_manifest.get("run_id") == run_id, "Source manifest run_id mismatch")
    require(sha256_file(source_manifest_path) == report.get("source_manifest_sha256")
            == prepare.get("source_manifest_sha256"), "Source manifest raw SHA-256 mismatch")
    require(sha256_file(parent_path) == report.get("parent_bindings_sha256")
            == prepare.get("parent_bindings_sha256"), "Parent binding raw SHA-256 mismatch")
    require(sha256_file(output_dir / "godot_input.json") == prepare.get("godot_input_sha256"),
            "Godot input raw SHA-256 mismatch")

    source_pins = source_manifest.get("source_pins")
    require(isinstance(source_pins, dict) and len(source_pins) == 30,
            f"Source manifest must contain 30 pins; got {len(source_pins) if isinstance(source_pins, dict) else 'invalid'}")
    require(report.get("source_pins") == source_pins, "Report/source manifest source pins differ")
    require(source_manifest.get("static_audit", {}).get("status") == "PASS_STATIC_SOURCE_MAPPING",
            "Embedded static-audit status is not PASS_STATIC_SOURCE_MAPPING")
    require(source_pins.get("release/C11C_FREEZE_PACKAGE_MANIFEST.json", {}).get("sha256")
            == EXPECTED_FROZEN_MANIFEST_SHA256, "Frozen C11-C manifest pin differs from authority")
    require(source_pins.get("tools/c11d/d9/test_c11e_e4b_r1p_family_grammar_static_audit.py", {}).get("sha256")
            == EXPECTED_STATIC_AUDIT_SHA256, "Static-audit source pin differs from operator's accepted audit")

    source_pin_results: list[dict[str, Any]] = []
    for rel, pin in sorted(source_pins.items()):
        require(not Path(rel).is_absolute() and ".." not in PurePosixPath(rel).parts,
                f"Unsafe source pin path: {rel}")
        path = project_root.joinpath(*PurePosixPath(rel).parts)
        require(path.is_file(), f"Pinned source file is missing from active checkout: {rel}")
        observed_bytes = path.stat().st_size
        observed_sha = sha256_file(path)
        require(observed_bytes == int(pin.get("bytes", -1)) and observed_sha == pin.get("sha256"),
                f"Active-checkout source pin mismatch: {rel}")
        source_pin_results.append({"path": rel, "bytes": observed_bytes, "sha256": observed_sha})

    require(prepare.get("case_count") == 27 and prepare.get("explicit_selector_count") == 27
            and prepare.get("family_count") == 5 and prepare.get("seed_relation_count") == 27,
            "Preparation report count fields are not 27/27/5/27")
    require(len(prepare.get("request_ids", [])) == 27 and len(set(prepare["request_ids"])) == 27,
            "Preparation report request IDs are incomplete or duplicated")
    require(report.get("scope_limits", {}).get("parameter_payload_materialized_in_memory") is True,
            "R1P scope limit does not confirm in-memory parameter materialization")
    for field in ("actual_c11c_frame_buffers_created", "frame_inventory_materialized", "pixels_created",
                  "renderer_native_input_emitted", "prototype_nodes_instantiated", "family_launchers_invoked",
                  "audio_or_d3_invoked", "ffmpeg_invoked", "media_created"):
        require(report.get("scope_limits", {}).get(field) is False, f"R1P scope boundary changed: {field}")
    expected_governance = {
        "renderer": "OFF", "D4.8": "BLOCKED", "D9.10": "PREPARE_ONLY", "D9.14": "BLOCKED",
        "D9.16": "BLOCKED", "D9.17": "BLOCKED_NO_GO", "D10": "BLOCKED_FOR_PROMOTION",
        "release_authority": "NONE",
    }
    require(report.get("governance") == expected_governance, "R1P report governance locks differ from required state")

    process_sidecar_hash = verify_raw_sidecar(process_path, output_dir / "runner_process_receipt.sha256")
    require(process.get("schema") == "C11E-E4B-R1P-RUNNER-PROCESS-RECEIPT-V1"
            and process.get("run_id") == run_id, "Runner process receipt identity/schema mismatch")
    require(process.get("process_success") is True and process.get("checkout_source_files_written") is False
            and process.get("renderer_or_media_invoked") is False,
            "Runner process receipt does not preserve the expected no-render/no-source-write boundary")
    require(str(process.get("powershell_version", "")).startswith("5.1."), "Runner did not use Windows PowerShell 5.1")
    require(str(process.get("python_version", "")).startswith("Python 3.13."), "Runner did not use Python 3.13")
    require(str(process.get("godot_version", "")).startswith("4.7.1."), "Runner did not use Godot 4.7.1")
    runtime_executable_pins: dict[str, Any] = {}
    for label, path_key, hash_key in (
        ("python_launcher", "python_launcher", "python_launcher_sha256"),
        ("godot_executable", "godot_executable", "godot_executable_sha256"),
    ):
        executable_path = str(process.get(path_key, ""))
        executable_hash = str(process.get(hash_key, ""))
        require(re.fullmatch(r"[0-9a-f]{64}", executable_hash) is not None,
                f"Malformed {label} SHA-256 pin in process receipt")
        if os.name == "nt":
            live_executable = Path(executable_path)
            require(live_executable.is_file(), f"Pinned runtime executable is missing: {executable_path}")
            live_hash = sha256_file(live_executable)
            require(live_hash == executable_hash, f"Pinned runtime executable SHA-256 mismatch: {label}")
            runtime_executable_pins[label] = {"path": executable_path, "sha256": live_hash, "status": "PASS_LIVE_EXECUTABLE_PIN"}
        else:
            runtime_executable_pins[label] = {"path": executable_path, "sha256": executable_hash, "status": "NOT_CHECKED_NON_WINDOWS_SNAPSHOT_REVIEW"}

    process_logs = {
        "python_version_process": ("python_version.stdout.log", "python_version.stderr.log"),
        "python_prepare": ("python_prepare_stdout.log", "python_prepare_stderr.log"),
        "godot_version_process": ("godot_version.stdout.log", "godot_version.stderr.log"),
        "godot_materializer": ("godot_stdout.log", "godot_stderr.log"),
        "python_finalize": ("python_finalize.stdout.log", "python_finalize.stderr.log"),
    }
    verified_processes: dict[str, Any] = {}
    for key, (stdout_name, stderr_name) in process_logs.items():
        verified_processes[key] = verify_process_log(output_dir, process, key, stdout_name, stderr_name)
    process_evidence = report.get("process_evidence", {})
    require(process_evidence.get("godot_exit_code") == 0 and process_evidence.get("python_prepare_exit_code") == 0,
            "Aggregate report contains a non-zero Godot/Python prepare exit code")
    require(process_evidence.get("godot_stdout_sha256") == verified_processes["godot_materializer"]["stdout_sha256"]
            and process_evidence.get("godot_stderr_sha256") == verified_processes["godot_materializer"]["stderr_sha256"],
            "Aggregate Godot process hashes do not match captured logs")
    require(process_evidence.get("python_prepare_stdout_sha256") == verified_processes["python_prepare"]["stdout_sha256"]
            and process_evidence.get("python_prepare_stderr_sha256") == verified_processes["python_prepare"]["stderr_sha256"],
            "Aggregate Python preparation hashes do not match captured logs")
    final_stdout = (output_dir / "python_finalize.stdout.log").read_text(encoding="utf-8-sig")
    require(EXPECTED_REPORT_STATUS in final_stdout and '"receipt_hash_verification": "PASS_27_OF_27"' in final_stdout,
            "Python finalizer stdout does not contain the 27/27 PASS receipt")

    family_rows = source_manifest["static_audit"]["families"]
    expected_selectors: dict[tuple[str, str, int], dict[str, Any]] = {}
    for family in family_rows:
        for selector in family.get("selectors", []):
            key = (family["family_id"], selector["grammar_id"], int(selector["grammar_index"]))
            require(key not in expected_selectors, f"Duplicate static-audit selector: {key}")
            expected_selectors[key] = family
    require(len(expected_selectors) == 27 and len(family_rows) == 5, "Static audit does not define 27 selectors across 5 families")

    receipt_dir = output_dir / "receipts"
    receipt_files = sorted(receipt_dir.glob("*.json"))
    sidecar_files = sorted(receipt_dir.glob("*.json.sha256"))
    require(len(receipt_files) == 27 and len(sidecar_files) == 27,
            f"Receipt file counts invalid: JSON={len(receipt_files)} sidecar={len(sidecar_files)}")
    parent_rows = parents["cases"]
    parent_by_case = {row.get("case_id"): row for row in parent_rows}
    require(len(parent_by_case) == 27 and None not in parent_by_case, "Parent case IDs are missing/duplicated")
    seen_case_ids: set[str] = set()
    seen_selectors: set[tuple[str, str, int]] = set()
    seen_gameplay: set[int] = set()
    seen_music: set[int] = set()
    canonical_receipt_hashes: list[str] = []
    family_counts: collections.Counter[str] = collections.Counter()
    receipt_summaries: list[dict[str, Any]] = []

    for receipt_path in receipt_files:
        receipt = load_json(receipt_path)
        stored_hash = receipt.get("receipt_sha256")
        hash_input = dict(receipt)
        hash_input.pop("receipt_sha256", None)
        observed_hash = canonical_sha256(hash_input)
        require(stored_hash == observed_hash, f"Receipt canonical SHA-256 mismatch: {receipt_path.name}")
        require(sidecar_token(receipt_path.with_name(receipt_path.name + ".sha256")) == observed_hash,
                f"Receipt sidecar mismatch: {receipt_path.name}")
        require(receipt.get("schema") == "C11E-E4B-R1P-LOOP-FAMILY-PARAMETER-RECEIPT-V1"
                and receipt.get("status") == "PASS_PARAMETER_PAYLOAD_MATERIALIZED_IN_MEMORY_NOT_RENDERER_INPUT",
                f"Receipt schema/status invalid: {receipt_path.name}")
        require(receipt.get("run_id") == run_id, f"Receipt run_id mismatch: {receipt_path.name}")
        case_id = str(receipt.get("case_id", ""))
        require(case_id not in seen_case_ids and case_id in parent_by_case, f"Receipt case ID missing/duplicate: {case_id}")
        require(case_id in prepare["request_ids"], f"Receipt case ID absent from D9.9/D9.10 prepare: {case_id}")
        seen_case_ids.add(case_id)

        selection = receipt.get("selection", {})
        selector_key = (str(selection.get("family_id")), str(selection.get("grammar_id")), int(selection.get("grammar_index", -1)))
        require(selector_key in expected_selectors and selector_key not in seen_selectors,
                f"Unexpected/duplicate family selector in receipt: {selector_key}")
        seen_selectors.add(selector_key)
        family_counts[selector_key[0]] += 1

        parent_row = parent_by_case[case_id]
        require(receipt.get("request_identity") == parent_row.get("request_identity"),
                f"Receipt request identity is not bound to its D9.9/D9.10 parent: {case_id}")
        require(receipt.get("request_identity", {}).get("request_id") == case_id,
                f"Receipt request_id identity mismatch: {case_id}")

        pins = receipt.get("case_source_pins", {})
        for pin_name, hash_key in (("launcher", "sha256"), ("prototype", "prototype_sha256")):
            row = pins.get(pin_name, {})
            rel = row.get("path")
            require(rel in source_pins and source_pins[rel].get("sha256") == row.get(hash_key),
                    f"Receipt {pin_name} pin is not bound to source manifest: {case_id}")
        require(receipt.get("source_pins") == source_pins, f"Receipt global source pins differ: {case_id}")

        seed_domains = receipt.get("seed_domains", {})
        gameplay_seed = int(seed_domains.get("gameplay_seed", -1))
        music_seed = int(seed_domains.get("music_seed", -1))
        require(gameplay_seed == 100000 + int(case_id[-2:]), f"Gameplay seed does not match selector sequence: {case_id}")
        require(music_seed == 500000 + int(case_id[-2:]), f"Music seed does not match selector sequence: {case_id}")
        require(seed_domains.get("music_seed_consumed_by_visual_parameters") is False
                and seed_domains.get("visual_parameters_use") == "request.seed"
                and seed_domains.get("automatic_seed_generation") is False
                and seed_domains.get("runtime_seed_derivation") is False,
                f"Seed-domain separation contract invalid: {case_id}")
        require(gameplay_seed not in seen_gameplay and music_seed not in seen_music and gameplay_seed != music_seed,
                f"Gameplay/music seed collision: {case_id}")
        seen_gameplay.add(gameplay_seed)
        seen_music.add(music_seed)

        payload_hash = receipt.get("payload_sha256")
        repeat_hash = receipt.get("repeat_payload_sha256")
        require(payload_hash == repeat_hash and re.fullmatch(r"[0-9a-f]{64}", str(payload_hash)) is not None,
                f"Deterministic repeat hash mismatch: {case_id}")
        visual_text = receipt.get("visual_parameters_canonical_json")
        require(isinstance(visual_text, str) and sha256_bytes(visual_text.encode("utf-8")) == receipt.get("visual_parameters_sha256"),
                f"Canonical visual-parameter hash mismatch: {case_id}")
        timing = receipt.get("timing", {})
        require(int(timing.get("fps", 0)) == 30 and float(timing.get("duration_seconds", 0)) in (20.0, 22.0, 23.0)
                and int(timing.get("frame_count", 0)) == int(timing["fps"]) * int(timing["duration_seconds"]),
                f"R1P timing descriptor invalid: {case_id}")
        governance = receipt.get("governance", {})
        receipt_governance = {
            "renderer": "OFF", "D4.8": "BLOCKED", "D9.10": "PREPARE_ONLY",
            "D9.17": "BLOCKED_NO_GO", "D10": "BLOCKED_FOR_PROMOTION", "release_authority": "NONE",
        }
        for key, value in receipt_governance.items():
            require(governance.get(key) == value, f"Receipt governance lock changed: {case_id} {key}")
        materialization = receipt.get("materialization", {})
        require(materialization.get("parameter_payload_materialized_in_memory") is True
                and materialization.get("deterministic_repeat_pass") is True,
                f"Receipt does not confirm in-memory deterministic parameter payload: {case_id}")
        for key in ("frame_buffers_materialized", "frame_inventory_materialized", "pixel_payload_materialized",
                    "renderer_native_input_emitted", "renderer_instantiated", "prototype_node_instantiated",
                    "launcher_invoked", "audio_or_d3_invoked", "ffmpeg_invoked", "media_created"):
            require(materialization.get(key) is False, f"Receipt scope boundary changed: {case_id} {key}")

        canonical_receipt_hashes.append(observed_hash)
        receipt_summaries.append({
            "case_id": case_id, "family_id": selector_key[0], "grammar_id": selector_key[1],
            "grammar_index": selector_key[2], "receipt_sha256": observed_hash,
            "payload_sha256": payload_hash, "gameplay_seed": gameplay_seed, "music_seed": music_seed,
        })

    require(len(seen_case_ids) == 27 and len(seen_selectors) == 27,
            f"Final receipt set incomplete: cases={len(seen_case_ids)} selectors={len(seen_selectors)}")
    require(seen_selectors == set(expected_selectors), "Receipt selector set differs from the accepted static grammar mapping")
    require(canonical_sha256(canonical_receipt_hashes) == report.get("receipt_hash_set_sha256"),
            "Aggregate receipt hash-set digest mismatch")
    require(len(seen_gameplay) == 27 and len(seen_music) == 27, "Seed domains are not independently unique across 27 cases")
    require(sum(family_counts.values()) == 27 and len(family_counts) == 5,
            "Family receipt distribution does not cover all five families")

    original_zip_path = output_dir.with_suffix(".zip")
    original_archive = verify_archive_matches_output(original_zip_path, output_dir)
    recovered_path = output_dir.parent / f"{run_id}_RECOVERED.zip"
    recovered_archive = create_recovered_archive(output_dir, recovered_path)

    recovery_dir = project_root / "artifacts" / "tests" / "c11e" / "e4b_r1p_recovery" / run_id
    recovery_dir.mkdir(parents=True, exist_ok=False)
    result = {
        "schema": "C11E-E4B-R1P-ARCHIVE-RECOVERY-REPORT-V1",
        "status": "PASS_R1P_ARCHIVE_RECOVERED_AND_PAYLOADS_REVALIDATED_27_OF_27",
        "run_id": run_id,
        "python_version": sys.version.split()[0],
        "project_root": str(project_root),
        "output_root": str(output_dir),
        "r1p_report_sha256": observed_report_hash,
        "source_manifest_sha256": report["source_manifest_sha256"],
        "parent_bindings_sha256": report["parent_bindings_sha256"],
        "runner_process_receipt_sha256": process_sidecar_hash,
        "receipt_json_count": len(receipt_files),
        "receipt_sidecar_count": len(sidecar_files),
        "selector_count": len(seen_selectors),
        "family_count": len(family_counts),
        "family_counts": dict(sorted(family_counts.items())),
        "deterministic_repeat_hashes": 27,
        "d9_9_d9_10_parent_bindings": 27,
        "source_pins_verified_against_active_checkout": len(source_pin_results),
        "source_pins": source_pin_results,
        "processes": verified_processes,
        "runtime_executable_pins": runtime_executable_pins,
        "governance": expected_governance,
        "original_archive": original_archive,
        "recovered_archive": recovered_archive,
        "root_cause": {
            "classification": "WINDOWS_ZIP_ENTRY_BACKSLASH_SEPARATOR_FALSE_NEGATIVE",
            "faulty_predicate": "^receipts/[^/]+\\.json$",
            "observed_entry_example": "receipts\\\\01_<run_id>_01.json",
            "normalized_entry_example": "receipts/01_<run_id>_01.json",
            "recipes_missing": False,
            "receipt_payloads_regenerated": False,
            "godot_rerun": False,
        },
        "scope": {
            "parameter_payload_verification_only": True,
            "frame_inventory_materialized": False,
            "pixels_created": False,
            "renderer_dispatch_invoked": False,
            "audio_or_d3_invoked": False,
            "ffmpeg_invoked": False,
            "media_created": False,
            "checkout_source_files_modified": False,
        },
        "receipt_summaries": sorted(receipt_summaries, key=lambda row: row["case_id"]),
    }
    report_out = recovery_dir / "archive_recovery_report.json"
    raw = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False) + "\n"
    report_out.write_text(raw, encoding="utf-8", newline="\n")
    report_hash = sha256_file(report_out)
    (recovery_dir / "archive_recovery_report.sha256").write_text(
        f"{report_hash}  archive_recovery_report.json\n", encoding="ascii"
    )
    result["recovery_report_path"] = str(report_out)
    result["recovery_report_sha256"] = report_hash
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", required=True, type=Path)
    parser.add_argument("--run-id", default=EXPECTED_RUN_ID)
    args = parser.parse_args()
    try:
        project_root = args.project_root.resolve(strict=True)
        require(project_root.is_dir(), f"ProjectRoot is not a directory: {project_root}")
        result = verify_run(project_root, args.run_id)
        print(json.dumps({
            "status": result["status"], "run_id": result["run_id"],
            "receipts": f"{result['receipt_json_count']}/27",
            "source_pins": f"{result['source_pins_verified_against_active_checkout']}/30",
            "runtime_executable_pins": {k: v["status"] for k, v in result["runtime_executable_pins"].items()},
            "family_counts": result["family_counts"],
            "original_zip_sha256": result["original_archive"]["sha256"],
            "original_backslash_entries": result["original_archive"]["entries_with_backslash_separator"],
            "recovered_zip": result["recovered_archive"]["path"],
            "recovered_zip_sha256": result["recovered_archive"]["sha256"],
            "recovery_report": result["recovery_report_path"],
            "recovery_report_sha256": result["recovery_report_sha256"],
        }, ensure_ascii=False, sort_keys=True))
        return 0
    except Exception as exc:  # noqa: BLE001 - CLI must produce a concise failure
        print(json.dumps({"status": "FAIL_R1P_ARCHIVE_RECOVERY", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
