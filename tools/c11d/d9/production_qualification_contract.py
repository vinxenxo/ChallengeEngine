from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

AUTH_REL = Path("definitions/c11d/production/D9_14_PRODUCTION_QUALIFICATION_AUTHORIZATION_V1.json")
C_MANIFEST_REL = Path("release/C11C_FREEZE_PACKAGE_MANIFEST.json")
EXPECTED_C_MANIFEST_SHA256 = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
REPORT_SCHEMA = "C11-D-D9.14-PRODUCTION-QUALIFICATION-REPORT-V1"
BASELINE_SCHEMA = "C11-D-PRODUCTION-QUALIFICATION-BASELINE-V1"


class QualificationContractError(RuntimeError):
    pass


def _canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        raise QualificationContractError(f"Cannot read JSON {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise QualificationContractError(f"Expected JSON object: {path}")
    return data


def validate_authorization(project_root: Path, token: str) -> dict[str, Any]:
    root = project_root.resolve()
    auth_path = root / AUTH_REL
    auth = read_json(auth_path)
    if auth.get("schema") != "C11-D-D9.14-PRODUCTION-QUALIFICATION-AUTHORIZATION-V1":
        raise QualificationContractError("qualification authorization schema mismatch")
    if auth.get("status") != "AUTHORIZED_BOUNDED_QUALIFICATION_ONLY":
        raise QualificationContractError("qualification authorization is not active")
    if token != auth.get("authorization_token"):
        raise QualificationContractError("explicit bounded qualification token mismatch")
    if auth.get("immutable_reference", {}).get("manifest_sha256") != EXPECTED_C_MANIFEST_SHA256:
        raise QualificationContractError("authorization does not pin the frozen C11-C manifest")
    manifest = root / C_MANIFEST_REL
    if not manifest.is_file() or sha256_file(manifest) != EXPECTED_C_MANIFEST_SHA256:
        raise QualificationContractError("frozen C11-C manifest is missing or changed")
    forbidden = auth.get("not_authorized", {})
    required_forbidden = (
        "d4_8_global_activation", "general_d_renderer_activation", "unbounded_production_execution",
        "release_or_publishing", "D9_14_FULL_GUI_CERTIFICATION", "D9_15_ACCEPTANCE_CLOSURE",
        "D9_16_FULL_ACCEPTANCE_CLOSURE", "D9_17_CLOSURE", "final_D_BASELINE_FREEZE",
        "C11C_SOURCE_OR_MANIFEST_MUTATION",
    )
    if any(forbidden.get(key) is not True for key in required_forbidden):
        raise QualificationContractError("authorization scope was broadened")
    if auth.get("governance", {}).get("release_authority") != "NONE":
        raise QualificationContractError("qualification cannot grant release authority")
    if auth.get("governance", {}).get("renderer_activation_for_general_D_requests") is not False:
        raise QualificationContractError("general D renderer activation must stay disabled")
    return auth


def validate_report_shape(report: dict[str, Any], project_root: Path) -> dict[str, Any]:
    root = project_root.resolve()
    if report.get("schema") != REPORT_SCHEMA:
        raise QualificationContractError("production qualification report schema mismatch")
    if report.get("status") != "BOUNDED_PRODUCTION_QUALIFICATION_PASS_NOT_D9_14_CLOSURE":
        raise QualificationContractError("qualification status is not a bounded qualification pass")
    if report.get("d9_14_full_acceptance") != "NOT_CLOSED":
        raise QualificationContractError("bounded qualification must not close D9.14")
    if report.get("d9_15") != "WAIVED_NOT_EVIDENCED_FOR_CANDIDATE_ONLY":
        raise QualificationContractError("D9.15 waiver scope changed")
    if report.get("d9_16") != "BLOCKED_PENDING_FULL_ACCEPTANCE":
        raise QualificationContractError("D9.16 must remain blocked")
    if report.get("d9_17") != "BLOCKED":
        raise QualificationContractError("D9.17 must remain blocked")
    if report.get("d4_8") != "LIMITED_QUALIFICATION_ONLY_NOT_GLOBAL_ACTIVATION":
        raise QualificationContractError("D4.8 scope changed")
    if report.get("release_authority") != "NONE":
        raise QualificationContractError("release authority must remain NONE")
    if report.get("c11c_manifest_sha256") != EXPECTED_C_MANIFEST_SHA256:
        raise QualificationContractError("report C11-C manifest reference mismatch")
    auth_path = root / AUTH_REL
    if not auth_path.is_file() or sha256_file(auth_path) != report.get("authorization_checkpoint_sha256"):
        raise QualificationContractError("qualification authorization checkpoint identity mismatch")
    if report.get("source_tree_sha256_before") != report.get("source_tree_sha256_after"):
        raise QualificationContractError("source tree changed during qualification")
    required_checks = {
        "challenge_video": "PASS",
        "visual_loop_video": "PASS",
        "visual_drill_video": "PASS",
        "same_seed_loop_video_replay": "PASS",
        "music_seed_changes_audio_identity": "PASS",
        "a_v_streams_and_duration": "PASS",
        "protected_source_unchanged": "PASS",
    }
    checks = report.get("checks", {})
    for name, expected in required_checks.items():
        if checks.get(name) != expected:
            raise QualificationContractError(f"required production qualification check not PASS: {name}")
    if checks.get("c11d_editorial_renderer_binding") != "NOT_CERTIFIED_BY_THIS_RUN":
        raise QualificationContractError("C11-D editorial renderer binding must not be certified by this runner")
    for item in report.get("media_outputs", []):
        media_path = Path(str(item.get("path", ""))).resolve()
        try:
            media_path.relative_to(root / "artifacts" / "production" / "c11d_qualification")
        except ValueError as exc:
            raise QualificationContractError(f"media escaped qualification root: {media_path}") from exc
        if not media_path.is_file():
            raise QualificationContractError(f"media output missing: {media_path}")
        if sha256_file(media_path) != item.get("sha256"):
            raise QualificationContractError(f"media SHA-256 mismatch: {media_path}")
        if media_path.stat().st_size <= 1024:
            raise QualificationContractError(f"media output implausibly small: {media_path}")
        # Re-probe the actual bytes. The report cannot pass by supplying synthetic probe metadata.
        try:
            completed = subprocess.run(
                ["ffprobe", "-v", "error", "-count_frames", "-show_streams", "-show_format", "-of", "json", str(media_path)],
                check=False, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise QualificationContractError(f"cannot execute ffprobe on media: {media_path}: {exc}") from exc
        if completed.returncode != 0:
            raise QualificationContractError(f"ffprobe failed on media: {media_path}: {completed.stderr.strip()}")
        try:
            actual = json.loads(completed.stdout)
            streams = actual.get("streams", [])
            video = next(row for row in streams if row.get("codec_type") == "video")
            audio = next(row for row in streams if row.get("codec_type") == "audio")
            fps_n, fps_d = (int(part) for part in str(video.get("r_frame_rate", "")).split("/", 1))
            fps = fps_n / fps_d
            duration = float(actual.get("format", {}).get("duration", 0))
            frames = int(video.get("nb_read_frames", 0))
        except (ValueError, TypeError, StopIteration, ZeroDivisionError) as exc:
            raise QualificationContractError(f"media stream metadata invalid: {media_path}") from exc
        if int(video.get("width", 0)) != 720 or int(video.get("height", 0)) != 1280:
            raise QualificationContractError(f"actual media resolution mismatch: {media_path}")
        if video.get("codec_name") != "h264" or video.get("pix_fmt") not in {"yuv420p", "yuvj420p"}:
            raise QualificationContractError(f"actual video codec/pixel format mismatch: {media_path}")
        if not (24 <= fps <= 60) or frames <= 1 or duration < 3:
            raise QualificationContractError(f"actual video timing/frame contract failed: {media_path}")
        if int(audio.get("channels", 0)) != 2 or int(audio.get("sample_rate", 0)) <= 0:
            raise QualificationContractError(f"actual stereo audio contract failed: {media_path}")
        try:
            video_duration = float(video.get("duration", duration))
            audio_duration = float(audio.get("duration", duration))
        except (ValueError, TypeError) as exc:
            raise QualificationContractError(f"actual A/V duration metadata invalid: {media_path}") from exc
        if abs(video_duration - audio_duration) > 0.20:
            raise QualificationContractError(f"actual A/V duration mismatch: {media_path}")
        reported_probe = item.get("probe", {})
        checks_numeric = (
            ("width", int(video.get("width", 0)), 0),
            ("height", int(video.get("height", 0)), 0),
            ("frames", frames, 0),
            ("audio_channels", int(audio.get("channels", 0)), 0),
            ("audio_sample_rate", int(audio.get("sample_rate", 0)), 0),
        )
        for key, actual_value, _ in checks_numeric:
            if int(reported_probe.get(key, -1)) != actual_value:
                raise QualificationContractError(f"reported probe {key} disagrees with actual media: {media_path}")
        if reported_probe.get("video_codec") != video.get("codec_name") or reported_probe.get("audio_codec") != audio.get("codec_name"):
            raise QualificationContractError(f"reported codec disagrees with actual media: {media_path}")
        if reported_probe.get("pixel_format") != video.get("pix_fmt"):
            raise QualificationContractError(f"reported pixel format disagrees with actual media: {media_path}")
        if abs(float(reported_probe.get("fps", -1)) - fps) > 0.01 or abs(float(reported_probe.get("duration_seconds", -1)) - duration) > 0.15:
            raise QualificationContractError(f"reported timing disagrees with actual media: {media_path}")
    if len(report.get("media_outputs", [])) < 4:
        raise QualificationContractError("expected challenge, two loop variants and visual drill media")
    det = report.get("determinism_evidence", {})
    if int(det.get("loop_frame_count", 0)) <= 1 or det.get("loop_frame_sequence_sha256_a") != det.get("loop_frame_sequence_sha256_b"):
        raise QualificationContractError("same-seed loop frame replay evidence is invalid")
    frame_evidence = det.get("loop_frame_sequences", [])
    if len(frame_evidence) != 2:
        raise QualificationContractError("two normalized loop frame-sequence files are required")
    normalized_sequences = []
    for item in frame_evidence:
        evidence_path = Path(str(item.get("path", ""))).resolve()
        try:
            evidence_path.relative_to(root / "artifacts" / "production" / "c11d_qualification")
        except ValueError as exc:
            raise QualificationContractError("frame-sequence evidence escaped qualification root") from exc
        if not evidence_path.is_file() or sha256_file(evidence_path) != item.get("sha256"):
            raise QualificationContractError(f"frame-sequence evidence hash mismatch: {evidence_path}")
        rows = evidence_path.read_text(encoding="utf-8").splitlines()
        if len(rows) != int(det.get("loop_frame_count", 0)) or any(len(row) != 32 or any(c not in "0123456789abcdef" for c in row) for row in rows):
            raise QualificationContractError(f"normalized frame-sequence file is malformed: {evidence_path}")
        normalized_sequences.append(rows)
    if normalized_sequences[0] != normalized_sequences[1]:
        raise QualificationContractError("same-seed decoded loop frames differ")
    if sha256_file(Path(frame_evidence[0]["path"])) != det.get("loop_frame_sequence_sha256_a") or sha256_file(Path(frame_evidence[1]["path"])) != det.get("loop_frame_sequence_sha256_b"):
        raise QualificationContractError("frame-sequence report identity mismatch")
    seeds = report.get("seeds", {})
    if seeds.get("loop_gameplay") is None or seeds.get("music_a") == seeds.get("music_b"):
        raise QualificationContractError("gameplay/music seed separation evidence is invalid")
    audio_evidence = det.get("music_seed_audio", [])
    if len(audio_evidence) != 2:
        raise QualificationContractError("two decoded music-seed audio evidence files are required")
    wav_hashes = []
    pcm_hashes = []
    for item in audio_evidence:
        for path_key, hash_key in (("source_wav_path", "source_wav_sha256"), ("decoded_pcm_path", "decoded_pcm_sha256")):
            evidence_path = Path(str(item.get(path_key, ""))).resolve()
            try:
                evidence_path.relative_to(root / "artifacts" / "production" / "c11d_qualification")
            except ValueError as exc:
                raise QualificationContractError("music evidence escaped qualification root") from exc
            if not evidence_path.is_file() or sha256_file(evidence_path) != item.get(hash_key):
                raise QualificationContractError(f"music evidence hash mismatch: {evidence_path}")
        wav_hashes.append(item["source_wav_sha256"])
        pcm_hashes.append(item["decoded_pcm_sha256"])
    if wav_hashes[0] == wav_hashes[1] or pcm_hashes[0] == pcm_hashes[1]:
        raise QualificationContractError("different music seeds must change source and decoded final audio bytes")
    return {"status": "PASS", "checks": len(required_checks), "media_outputs": len(report["media_outputs"])}


def finalize(report_path: Path, project_root: Path) -> dict[str, Any]:
    root = project_root.resolve()
    report_path = report_path.resolve()
    report = read_json(report_path)
    validate_report_shape(report, root)
    report.pop("report_sha256", None)
    report["report_sha256"] = _sha_bytes(_canonical(report))
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    validated = audit_report(report_path, root)
    baseline = {
        "schema": BASELINE_SCHEMA,
        "schema_version": "1.0",
        "baseline_id": "C11-D-PRODUCTION-QUALIFICATION-BASELINE-0.1",
        "status": "SEALED_QUALIFICATION_BASELINE_NOT_RELEASE_BASELINE",
        "run_id": report.get("run_id"),
        "source_tree_sha256": report.get("source_tree_sha256_after"),
        "c11c_manifest_sha256": EXPECTED_C_MANIFEST_SHA256,
        "qualification_report": str(report_path),
        "qualification_report_sha256": sha256_file(report_path),
        "media_outputs": report.get("media_outputs", []),
        "checks": report.get("checks", {}),
        "governance": {
            "renderer_activation_for_general_D_requests": False,
            "D4_8": "LIMITED_QUALIFICATION_ONLY_NOT_GLOBAL_ACTIVATION",
            "D9_14_full_acceptance": "NOT_CLOSED",
            "D9_15": "WAIVED_NOT_EVIDENCED_FOR_CANDIDATE_ONLY",
            "D9_16": "BLOCKED_PENDING_FULL_ACCEPTANCE",
            "D9_17": "BLOCKED",
            "freeze_eligible_for_release": False,
            "release_authority": "NONE",
            "c11c_reference_mutated": False,
        },
    }
    baseline["baseline_sha256"] = _sha_bytes(_canonical(baseline))
    baseline_path = report_path.parent / "C11D_PRODUCTION_QUALIFICATION_BASELINE_V1.json"
    baseline_path.write_text(json.dumps(baseline, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    baseline_validation = audit_baseline(baseline_path, root)
    return {"report": str(report_path), "report_sha256": report["report_sha256"], "baseline": str(baseline_path), "baseline_sha256": baseline["baseline_sha256"], **validated, "baseline_audit": baseline_validation["status"]}


def audit_report(report_path: Path, project_root: Path) -> dict[str, Any]:
    report = read_json(report_path)
    supplied = report.get("report_sha256")
    unsigned = dict(report)
    unsigned.pop("report_sha256", None)
    if supplied != _sha_bytes(_canonical(unsigned)):
        raise QualificationContractError("qualification report seal mismatch")
    result = validate_report_shape(report, project_root)
    return {**result, "report_sha256": supplied}


def audit_baseline(baseline_path: Path, project_root: Path) -> dict[str, Any]:
    baseline = read_json(baseline_path)
    supplied = baseline.get("baseline_sha256")
    unsigned = dict(baseline)
    unsigned.pop("baseline_sha256", None)
    if supplied != _sha_bytes(_canonical(unsigned)):
        raise QualificationContractError("qualification baseline seal mismatch")
    if baseline.get("schema") != BASELINE_SCHEMA or baseline.get("status") != "SEALED_QUALIFICATION_BASELINE_NOT_RELEASE_BASELINE":
        raise QualificationContractError("qualification baseline schema/status mismatch")
    gov = baseline.get("governance", {})
    expected = {
        "renderer_activation_for_general_D_requests": False,
        "D4_8": "LIMITED_QUALIFICATION_ONLY_NOT_GLOBAL_ACTIVATION",
        "D9_14_full_acceptance": "NOT_CLOSED",
        "D9_15": "WAIVED_NOT_EVIDENCED_FOR_CANDIDATE_ONLY",
        "D9_16": "BLOCKED_PENDING_FULL_ACCEPTANCE",
        "D9_17": "BLOCKED",
        "freeze_eligible_for_release": False,
        "release_authority": "NONE",
        "c11c_reference_mutated": False,
    }
    for key, value in expected.items():
        if gov.get(key) != value:
            raise QualificationContractError(f"qualification baseline governance mismatch: {key}")
    report_path = Path(str(baseline.get("qualification_report", ""))).resolve()
    try:
        report_path.relative_to((project_root.resolve() / "artifacts" / "production" / "c11d_qualification"))
    except ValueError as exc:
        raise QualificationContractError("qualification report escaped qualification root") from exc
    if not report_path.is_file() or sha256_file(report_path) != baseline.get("qualification_report_sha256"):
        raise QualificationContractError("qualification report identity mismatch in baseline")
    report_result = audit_report(report_path, project_root)
    if report_result.get("report_sha256") != read_json(report_path).get("report_sha256"):
        raise QualificationContractError("qualification report seal mismatch from baseline")
    if baseline.get("source_tree_sha256") != read_json(report_path).get("source_tree_sha256_after"):
        raise QualificationContractError("qualification baseline source identity mismatch")
    return {"status": "PASS", "baseline_id": baseline.get("baseline_id"), "baseline_sha256": supplied, "report_sha256": baseline.get("qualification_report_sha256"), **report_result}


def main() -> int:
    parser = argparse.ArgumentParser(description="C11-D bounded production qualification contract")
    sub = parser.add_subparsers(dest="command", required=True)
    p_auth = sub.add_parser("authorize-check")
    p_auth.add_argument("--project-root", required=True)
    p_auth.add_argument("--token", required=True)
    p_finalize = sub.add_parser("finalize")
    p_finalize.add_argument("--report", required=True)
    p_finalize.add_argument("--project-root", required=True)
    p_audit = sub.add_parser("audit")
    p_audit.add_argument("--report", required=True)
    p_audit.add_argument("--project-root", required=True)
    p_baseline = sub.add_parser("audit-baseline")
    p_baseline.add_argument("--baseline", required=True)
    p_baseline.add_argument("--project-root", required=True)
    args = parser.parse_args()
    try:
        if args.command == "authorize-check":
            auth = validate_authorization(Path(args.project_root), args.token)
            print(f"C11-D D9.14 BOUNDED QUALIFICATION AUTHORIZATION PASS | status={auth['status']} | release_authority=NONE")
            return 0
        if args.command == "finalize":
            result = finalize(Path(args.report), Path(args.project_root))
            print(json.dumps(result, ensure_ascii=False, indent=2))
            print("C11-D PRODUCTION QUALIFICATION BASELINE SEALED | status=QUALIFICATION_ONLY_NOT_RELEASE | release_authority=NONE")
            return 0
        if args.command == "audit-baseline":
            result = audit_baseline(Path(args.baseline), Path(args.project_root))
            print(json.dumps(result, ensure_ascii=False, indent=2))
            print("C11-D PRODUCTION QUALIFICATION BASELINE AUDIT PASS | qualification_only=true | release_authority=NONE")
            return 0
        result = audit_report(Path(args.report), Path(args.project_root))
        print(json.dumps(result, ensure_ascii=False, indent=2))
        print("C11-D PRODUCTION QUALIFICATION REPORT AUDIT PASS | d9_14=NOT_CLOSED | release_authority=NONE")
        return 0
    except QualificationContractError as exc:
        print(json.dumps({"status": "FAIL_CLOSED", "error": str(exc)}, ensure_ascii=False))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
