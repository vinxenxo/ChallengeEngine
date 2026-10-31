"""Build a fail-closed C11-E E2 Challenge title A/B pair.

This module prepares only the two request/sidecar/config packages. The PowerShell
E2 runner owns the narrowly authorized physical Movie Maker/FFmpeg invocation.
The original C challenge definition and all C runtime sources remain read-only.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Mapping

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PRODUCER = ROOT / "c11c-suite" / "c11c-producer"
if str(PRODUCER) not in sys.path:
    sys.path.insert(0, str(PRODUCER))

from c11e_production_service import (  # noqa: E402
    C11EProductionServiceError,
    prepare_c11e_production_intent,
    validate_c11e_production_intent,
)

EXPECTED_MANIFEST_SHA256 = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
EXPECTED_MANIFEST_BYTES = 796318
EXPECTED_CHALLENGE_ID = "CHALLENGE_001"
EXPECTED_FAMILY_ID = "key"
SIDECAR_SCHEMA = "C11E-CHALLENGE-EDITORIAL-SIDECAR-V1"


class E2PairError(ValueError):
    """Raised when the E2 A/B request pair is not safe or semantically equivalent."""


def _canonical(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(k): _canonical(value[k]) for k in sorted(value, key=lambda x: str(x))}
    if isinstance(value, (list, tuple)):
        return [_canonical(v) for v in value]
    return value


def canonical_json(value: Any) -> str:
    return json.dumps(_canonical(value), ensure_ascii=False, separators=(",", ":"), allow_nan=False)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def _safe_title(value: Any, field: str) -> str:
    if not isinstance(value, str):
        raise E2PairError(f"{field} must be a string")
    result = value.strip()
    if not result or result == "UNKNOWN":
        raise E2PairError(f"{field} must be a non-empty resolved editorial title")
    if len(result) > 160:
        raise E2PairError(f"{field} exceeds the D9.8 160-character limit")
    if any(ord(ch) < 32 for ch in result):
        raise E2PairError(f"{field} contains control characters")
    return result


def build_raw_request(request_id: str, seed: int, music_seed: int, title: str) -> dict[str, Any]:
    title = _safe_title(title, "title")
    if isinstance(seed, bool) or not isinstance(seed, int) or not 1 <= seed <= 2147483646:
        raise E2PairError("gameplay seed must be an explicit integer in [1, 2147483646]")
    if isinstance(music_seed, bool) or not isinstance(music_seed, int) or not 1 <= music_seed <= 2147483646:
        raise E2PairError("music seed must be an explicit integer in [1, 2147483646]")
    if not isinstance(request_id, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,159}", request_id):
        raise E2PairError("request_id is not a safe canonical D9.9 identity")
    return {
        "schema": "C11-D-D9.9-UNIVERSAL-PRODUCER-REQUEST-V1",
        "schema_version": "1.0",
        "request_id": request_id,
        "mode": "REVIEW",
        "selection": {
            "content_type": "challenges",
            "family_id": EXPECTED_FAMILY_ID,
            "variant_id": EXPECTED_CHALLENGE_ID,
        },
        "seed": seed,
        "music_seed": music_seed,
        "delivery_profile_id": "REVIEW_720",
        "presentation_profile_id": "social_default_v1",
        "variation_index": 0,
        "audio_enabled": False,
        "personalization_enabled": True,
        "editorial_profile": {},
        "production_override": {"title": title},
        "provenance": {
            "source_revision": "C11D-D9.9-PRODUCER-0.11.0",
            "request_origin": "CLI",
        },
    }


def resolve_intent_pair(
    root: Path | str,
    request_id: str,
    seed: int,
    music_seed: int,
    title_a: str,
    title_b: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Resolve and validate both E1 intents before any output directory is created."""
    root = Path(root).resolve()
    title_a = _safe_title(title_a, "title_a")
    title_b = _safe_title(title_b, "title_b")
    if title_a == title_b:
        raise E2PairError("A/B titles must differ")

    request_a = build_raw_request(request_id, seed, music_seed, title_a)
    request_b = copy.deepcopy(request_a)
    request_b["production_override"]["title"] = title_b

    # Both prepares run while the E1 output root is still absent. The same request_id
    # deliberately makes the requests identical except for production_override.title.
    prepared_a = prepare_c11e_production_intent(request_a, root, request_origin="CLI")
    prepared_b = prepare_c11e_production_intent(request_b, root, request_origin="CLI")
    validation_a = validate_c11e_production_intent(prepared_a["intent"], root)
    validation_b = validate_c11e_production_intent(prepared_b["intent"], root)
    _validate_intent_pair(prepared_a["intent"], prepared_b["intent"])

    return (
        {"raw_request": request_a, "prepared": prepared_a, "validation": validation_a},
        {"raw_request": request_b, "prepared": prepared_b, "validation": validation_b},
    )


def _validate_intent_pair(a: Mapping[str, Any], b: Mapping[str, Any]) -> None:
    if a.get("schema") != "C11-E-PRODUCTION-INTENT-V1" or b.get("schema") != "C11-E-PRODUCTION-INTENT-V1":
        raise E2PairError("Both records must be validated E1 production intents")
    for key in ("request", "seed_domains", "delivery", "source_identity"):
        if a.get(key) != b.get(key):
            raise E2PairError(f"A/B invariance failed for intent.{key}")
    editorial_a = a.get("editorial")
    editorial_b = b.get("editorial")
    if not isinstance(editorial_a, Mapping) or not isinstance(editorial_b, Mapping):
        raise E2PairError("Resolved editorial maps are missing")
    if set(editorial_a) != set(editorial_b):
        raise E2PairError("A/B editorial field set changed")
    for key in editorial_a:
        if key != "title" and editorial_a[key] != editorial_b[key]:
            raise E2PairError(f"A/B changed an editorial field other than title: {key}")
    if editorial_a.get("title") == editorial_b.get("title"):
        raise E2PairError("A/B resolved titles must differ")
    for field in ("request_hash", "editorial_hash", "plan_hash", "intent_hash"):
        if a.get("identity", {}).get(field) == b.get("identity", {}).get(field):
            raise E2PairError(f"A/B {field} must differ when title differs")
    if a.get("execution_boundary", {}).get("renderer_dispatch_invoked") is not False:
        raise E2PairError("E1 intent must remain preparation-only before E2 test dispatch")
    if a.get("execution_boundary", {}).get("release_authority") != "NONE":
        raise E2PairError("E1 intent may not grant release authority")


def build_effective_challenge_config(source: Mapping[str, Any], seed: int) -> dict[str, Any]:
    if str(source.get("challenge_id", "")) != EXPECTED_CHALLENGE_ID:
        raise E2PairError("Challenge source identity must be CHALLENGE_001")
    if isinstance(seed, bool) or not isinstance(seed, int) or not 1 <= seed <= 2147483646:
        raise E2PairError("Invalid gameplay seed")
    effective = copy.deepcopy(dict(source))
    generation = effective.get("generation")
    if not isinstance(generation, dict) or "seed" not in generation:
        raise E2PairError("Challenge source has no canonical generation.seed")
    generation["seed"] = seed
    return effective


def build_editorial_sidecar(
    intent: Mapping[str, Any],
    challenge_source_sha256: str,
    effective_config_sha256: str,
) -> dict[str, Any]:
    request = intent.get("request", {})
    selection = request.get("selection", {})
    if request.get("content_type") != "challenges" or selection.get("variant_id") != EXPECTED_CHALLENGE_ID:
        raise E2PairError("E2 sidecar only supports CHALLENGE_001")
    title = _safe_title(intent.get("editorial", {}).get("title"), "resolved title")
    seed_domains = copy.deepcopy(intent.get("seed_domains", {}))
    identity = copy.deepcopy(intent.get("identity", {}))
    source_identity = intent.get("source_identity", {})
    manifest = source_identity.get("c11c_manifest", {})
    if manifest.get("sha256") != EXPECTED_MANIFEST_SHA256 or manifest.get("bytes") != EXPECTED_MANIFEST_BYTES:
        raise E2PairError("E2 sidecar C11-C manifest reference mismatch")
    if not re.fullmatch(r"[a-f0-9]{64}", challenge_source_sha256):
        raise E2PairError("Challenge source hash is malformed")
    if not re.fullmatch(r"[a-f0-9]{64}", effective_config_sha256):
        raise E2PairError("Effective Challenge config hash is malformed")
    gameplay_seed = seed_domains.get("gameplay", {}).get("value")
    if isinstance(gameplay_seed, bool) or not isinstance(gameplay_seed, int):
        raise E2PairError("E2 sidecar gameplay seed is malformed")
    return {
        "schema": SIDECAR_SCHEMA,
        "schema_version": "1.0",
        "request_id": request.get("request_id"),
        "content_type": "challenges",
        "challenge_id": EXPECTED_CHALLENGE_ID,
        "selection": copy.deepcopy(selection),
        "editorial": {"title": title},
        "visual_target": {
            "slot_id": "header.editorial_title",
            "region": "HEADER",
            "bounds_logical_540x960": {"x": 24, "y": 24, "width": 496, "height": 104},
            "visibility": "ALL_CHALLENGE_FRAMES",
            "semantic_separation": "TITLE_IS_NOT_HOOK_CTA_OR_GAMEPLAY",
        },
        "seed_domains": seed_domains,
        "identity": identity,
        "source_identity": {
            "c11c_manifest_sha256": EXPECTED_MANIFEST_SHA256,
            "challenge_source_sha256": challenge_source_sha256,
            "effective_config_sha256": effective_config_sha256,
            "intent_sha256": intent.get("intent_sha256"),
        },
        "execution_boundary": {
            "renderer_input_is_e2_test_only": True,
            "release_authority": "NONE",
            "baseline_promotion": False,
            "audio_enabled": False,
        },
    }


def _write_json(path: Path, value: Any) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False) + "\n"
    data = raw.encode("utf-8")
    # Exclusive creation prevents silent overwrites in an evidence run.
    with path.open("xb") as stream:
        stream.write(data)
    return sha256_bytes(data)


def prepare_e2_pair(
    root: Path | str,
    request_id: str,
    seed: int,
    music_seed: int,
    title_a: str,
    title_b: str,
) -> dict[str, Any]:
    root = Path(root).resolve()
    pair = resolve_intent_pair(root, request_id, seed, music_seed, title_a, title_b)
    intent_a = pair[0]["prepared"]["intent"]
    intent_b = pair[1]["prepared"]["intent"]
    output_rel = str(intent_a["output"]["planned_root"])
    expected_output_rel = f"artifacts/production/c11e/{request_id}"
    if output_rel.replace("\\", "/") != expected_output_rel:
        raise E2PairError("E1 planned output root differs from the E2 allowlisted destination")
    output_root = root / "artifacts" / "production" / "c11e" / request_id
    output_parent = output_root.parent
    for component in (root / "artifacts", root / "artifacts" / "production", output_parent):
        if component.is_symlink():
            raise E2PairError(f"E2 output path contains a symlink: {component.relative_to(root)}")
        if component.exists() and not component.is_dir():
            raise E2PairError(f"E2 output path component is not a directory: {component.relative_to(root)}")
    try:
        output_parent.resolve(strict=False).relative_to(root)
    except ValueError as exc:
        raise E2PairError("E2 output root escapes repository root through a parent path") from exc
    if output_root.exists() or output_root.is_symlink():
        raise E2PairError(f"E2 output root already exists; overwrite forbidden: {output_rel}")

    challenge_path = root / "challenges" / f"{EXPECTED_CHALLENGE_ID}.json"
    challenge_bytes = challenge_path.read_bytes()
    challenge_sha = sha256_bytes(challenge_bytes)
    effective = build_effective_challenge_config(
        json.loads(challenge_bytes.decode("utf-8-sig")), seed
    )
    effective_raw = (json.dumps(effective, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    effective_sha = sha256_bytes(effective_raw)
    if pair[0]["prepared"]["intent"]["seed_domains"] != pair[1]["prepared"]["intent"]["seed_domains"]:
        raise E2PairError("A/B gameplay or music seed domains diverged")

    # All contract/hash validation completed before the first output write.
    output_root.mkdir(parents=True, exist_ok=False)
    try:
        output_root.resolve(strict=True).relative_to(root)
    except ValueError as exc:
        raise E2PairError("Created E2 output root resolves outside repository root") from exc
    run_records: dict[str, Any] = {}
    for label, item in (("A", pair[0]), ("B", pair[1])):
        run_dir = output_root / label
        run_dir.mkdir(exist_ok=False)
        request_hash = _write_json(run_dir / "request.raw.json", item["raw_request"])
        _write_json(run_dir / "intent.json", {
            "intent": item["prepared"]["intent"],
            "resolver_result": item["prepared"]["resolver_result"],
            "validation": item["validation"],
        })
        effective_path = run_dir / "challenge_effective.json"
        with effective_path.open("xb") as stream:
            stream.write(effective_raw)
        sidecar = build_editorial_sidecar(
            item["prepared"]["intent"], challenge_sha, effective_sha
        )
        sidecar_hash = _write_json(run_dir / "editorial.sidecar.json", sidecar)
        run_records[label] = {
            "directory": str(run_dir.relative_to(root)).replace("\\", "/"),
            "request_file_sha256": request_hash,
            "effective_config_sha256": effective_sha,
            "sidecar_sha256": sidecar_hash,
            "intent_sha256": item["prepared"]["intent"]["intent_sha256"],
            "request_hash": item["prepared"]["intent"]["identity"]["request_hash"],
            "editorial_hash": item["prepared"]["intent"]["identity"]["editorial_hash"],
            "plan_hash": item["prepared"]["intent"]["identity"]["plan_hash"],
            "title": item["prepared"]["intent"]["editorial"]["title"],
            "gameplay_seed": seed,
            "music_seed": music_seed,
        }

    if run_records["A"]["effective_config_sha256"] != run_records["B"]["effective_config_sha256"]:
        raise E2PairError("Effective C configs are not byte-identical across A/B")
    pair_receipt = {
        "schema": "C11E-E2-CHALLENGE-AB-PREPARED-V1",
        "status": "PAIR_PREPARED_NOT_YET_RENDERED",
        "request_id": request_id,
        "selection": {"content_type": "challenges", "family_id": EXPECTED_FAMILY_ID, "variant_id": EXPECTED_CHALLENGE_ID},
        "seed_domains": {"gameplay": seed, "music": music_seed, "independent": True},
        "c11c_manifest_sha256": EXPECTED_MANIFEST_SHA256,
        "challenge_source_sha256": challenge_sha,
        "runs": run_records,
        "only_request_difference": "production_override.title",
        "visual_slot": "header.editorial_title",
        "render_authority": "C11E_E2_TWO_CHALLENGE_AB_TESTS_ONLY",
        "release_authority": "NONE",
        "baseline_promotion": False,
        "audio_enabled": False,
    }
    pair_receipt_path = output_root / "E2_PAIR_PREPARED.json"
    receipt_hash = _write_json(pair_receipt_path, pair_receipt)
    return {
        "output_root": str(output_root),
        "output_root_relative": output_rel,
        "pair_receipt": str(pair_receipt_path),
        "pair_receipt_sha256": receipt_hash,
        "runs": run_records,
        "source_fps": int(effective["video"]["fps"]),
        "source_frames": sum(
            int(round(float(effective["video"].get(key, 0.0)) * int(effective["video"]["fps"])))
            for key in ("hook_duration", "game_duration", "reveal_duration", "cta_duration")
        ),
        "effective_config_sha256": effective_sha,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Prepare a C11-E E2 CHALLENGE_001 title A/B pair.")
    parser.add_argument("--root", required=True)
    parser.add_argument("--request-id", required=True)
    parser.add_argument("--seed", required=True, type=int)
    parser.add_argument("--music-seed", required=True, type=int)
    parser.add_argument("--title-a", required=True)
    parser.add_argument("--title-b", required=True)
    args = parser.parse_args(argv)
    try:
        result = prepare_e2_pair(
            args.root, args.request_id, args.seed, args.music_seed, args.title_a, args.title_b
        )
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        print("C11-E E2 CHALLENGE PAIR PREPARATION PASS | renderer=NOT_YET_INVOKED | media_created=false")
        return 0
    except Exception as exc:
        print(f"C11-E E2 PAIR PREPARATION ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
