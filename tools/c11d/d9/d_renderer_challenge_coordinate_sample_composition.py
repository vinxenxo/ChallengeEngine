"""Proposal-only validation for spatial coordinate projection + temporal sample selection.

This module does not produce renderer input. It validates the declared contract, its
source lineage, the composed 420->210 frame mapping, and geometric projection facts.
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
from typing import Any, Iterable, Sequence

CONTRACT_REL = Path("definitions/c11d/production/D_RENDERER_CHALLENGE_COORDINATE_SAMPLE_COMPOSITION_PROPOSAL_V1.json")
SCHEMA_REL = Path("definitions/c11d/production/D_RENDERER_CHALLENGE_COORDINATE_SAMPLE_COMPOSITION_SCHEMA_V1.json")
EXPECTED_FROZEN_MANIFEST_SHA256 = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
EXPECTED_COORDINATE_CONTRACT_SHA256 = "c1caf8e640595bc89957f17ef8bbd7abe80a92cac18cf77974633a1ddde0e264"
EXPECTED_SAMPLE_CONTRACT_SHA256 = "3e278481afe9d66458f05f29c15275819af49f9b68120b6a0b39dda2e9715cf3"
FLOAT_TOLERANCE = 1e-4


class CompositionContractError(ValueError):
    """Raised when a proposal or one of its source identities is inconsistent."""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise CompositionContractError(f"cannot read valid JSON: {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise CompositionContractError(f"JSON root must be an object: {path}")
    return value


def project_point(point: Sequence[float], scale: Sequence[float] = (2.0 / 3.0, 2.0 / 3.0), offset: Sequence[float] = (0.0, 0.0)) -> tuple[float, float]:
    if len(point) != 2 or len(scale) != 2 or len(offset) != 2:
        raise CompositionContractError("point, scale and offset must be 2D values")
    values = tuple(float(v) for v in (*point, *scale, *offset))
    if not all(math.isfinite(v) for v in values):
        raise CompositionContractError("coordinate transform values must be finite")
    return (values[0] * values[2] + values[4], values[1] * values[3] + values[5])


def selected_source_indices(source_count: int, stride: int = 2, origin: int = 0) -> list[int]:
    if source_count <= 0:
        raise CompositionContractError("source_count must be > 0")
    if stride <= 0:
        raise CompositionContractError("stride must be > 0")
    if origin < 0 or origin >= source_count:
        raise CompositionContractError("origin must identify an index inside the source segment")
    return list(range(origin, source_count, stride))


def compose_projected_records(points: Iterable[Sequence[float]], *, stride: int = 2) -> list[tuple[float, float]]:
    """Detached toy/reference composition: project all points, then select cadence indices."""
    projected = [project_point(point) for point in points]
    indexes = selected_source_indices(len(projected), stride=stride)
    return [projected[index] for index in indexes]


def validate_contract(root: Path) -> dict[str, Any]:
    root = root.resolve()
    contract = load_json(root / CONTRACT_REL)
    schema = load_json(root / SCHEMA_REL)
    if contract.get("schema") != "C11-D-D9-RENDERER-CHALLENGE-COORDINATE-SAMPLE-COMPOSITION-PROPOSAL-V1":
        raise CompositionContractError("unexpected composition proposal schema identity")
    if contract.get("status") != "PROPOSED_NOT_APPROVED_NOT_FROZEN":
        raise CompositionContractError("composition policy must remain proposal-only")
    try:
        import jsonschema  # type: ignore
        jsonschema.Draft202012Validator(schema).validate(contract)
    except ImportError as exc:
        raise CompositionContractError("jsonschema is required for contract validation") from exc
    except Exception as exc:
        raise CompositionContractError(f"JSON Schema validation failed: {exc}") from exc

    authority = contract["authority"]
    if authority.get("frozen_c11c_manifest_sha256") != EXPECTED_FROZEN_MANIFEST_SHA256:
        raise CompositionContractError("authority frozen-manifest SHA-256 pin mismatch")
    if authority.get("coordinate_projection_contract_sha256") != EXPECTED_COORDINATE_CONTRACT_SHA256:
        raise CompositionContractError("authority coordinate-projection contract SHA-256 pin mismatch")
    if authority.get("sample_selection_contract_sha256") != EXPECTED_SAMPLE_CONTRACT_SHA256:
        raise CompositionContractError("authority sample-selection contract SHA-256 pin mismatch")
    expected_sources = {
        authority["frozen_c11c_manifest_path"]: EXPECTED_FROZEN_MANIFEST_SHA256,
        authority["coordinate_projection_contract_path"]: EXPECTED_COORDINATE_CONTRACT_SHA256,
        authority["sample_selection_contract_path"]: EXPECTED_SAMPLE_CONTRACT_SHA256,
    }
    for rel, expected in expected_sources.items():
        source = root / rel
        if not source.is_file():
            raise CompositionContractError(f"required lineage source is missing: {rel}")
        if sha256_file(source) != expected:
            raise CompositionContractError(f"source SHA-256 mismatch: {rel}")
    expected_lineage = {(str(path), digest) for path, digest in expected_sources.items()}
    actual_lineage = {(row.get("path"), row.get("sha256")) for row in contract["source_lineage"]}
    if actual_lineage != expected_lineage:
        raise CompositionContractError("source_lineage entries do not match the exact three pinned sources")

    case = contract["case"]
    proj = contract["spatial_projection"]
    composition = contract["composition"]
    facts = contract["expected_review_facts"]
    if case["source_game_snapshot_count"] != case["game_source_end_frame_exclusive"] - case["game_source_start_frame"]:
        raise CompositionContractError("source GAME range/count mismatch")
    if case["delivery_game_snapshot_count"] != case["game_delivery_end_frame_exclusive"] - case["game_delivery_start_frame"]:
        raise CompositionContractError("delivery GAME range/count mismatch")
    if case["source_fps"] != case["delivery_fps"] * case["source_to_delivery_stride"]:
        raise CompositionContractError("source/delivery frame-rate ratio is not the declared integer stride")
    indexes = selected_source_indices(case["source_game_snapshot_count"], case["source_to_delivery_stride"])
    if len(indexes) != case["delivery_game_snapshot_count"]:
        raise CompositionContractError("selected frame count does not match delivery GAME count")
    if indexes[0] != case["first_selected_source_local_index"] or indexes[-1] != case["last_selected_source_local_index"]:
        raise CompositionContractError("selected index endpoints mismatch")
    if case["winning_frame_local_game_index"] not in indexes:
        raise CompositionContractError("winning frame is not an exact selected sample")
    local_delivery_winner = indexes.index(case["winning_frame_local_game_index"])
    absolute_source_winner = case["game_source_start_frame"] + case["winning_frame_local_game_index"]
    absolute_delivery_winner = case["game_delivery_start_frame"] + local_delivery_winner
    if absolute_source_winner != case["winning_frame_absolute_source_index"]:
        raise CompositionContractError("absolute source winning-frame mapping mismatch")
    if local_delivery_winner != case["winning_frame_delivery_local_game_index"] or absolute_delivery_winner != case["winning_frame_absolute_delivery_index"]:
        raise CompositionContractError("winning-frame delivery mapping mismatch")
    if len(indexes) != composition["composed_delivery_record_count"] or case["source_game_snapshot_count"] != composition["spatial_projection_record_count"]:
        raise CompositionContractError("composition source/delivery record counts mismatch")
    if proj["combined_scale"] != [2.0 / 3.0, 2.0 / 3.0] or proj["combined_offset"] != [0.0, 0.0]:
        raise CompositionContractError("spatial transform must remain uniform 2/3 with zero offset")
    target = project_point(facts["source_target_position"], proj["combined_scale"], proj["combined_offset"])
    expected_target = facts["delivery_target_position"]
    if any(abs(actual - expected) > FLOAT_TOLERANCE for actual, expected in zip(target, expected_target)):
        raise CompositionContractError("projected target coordinate mismatch")
    if not (contract["governance_locks"]["policy_approved"] is False and contract["governance_locks"]["coordinate_projection_policy_approved"] is False and contract["governance_locks"]["sample_selection_policy_approved"] is False):
        raise CompositionContractError("proposal approval locks must remain false")
    if contract["governance_locks"]["renderer_activation"] or contract["governance_locks"]["renderer_input_emitted"] or contract["governance_locks"]["media_created"]:
        raise CompositionContractError("renderer/media governance locks must remain closed")
    return {"contract": contract, "schema": schema, "selected_indexes": indexes, "projected_target_position": target, "winning_delivery_local_game_index": local_delivery_winner, "winning_delivery_absolute_index": absolute_delivery_winner}


def status_line(result: dict[str, Any]) -> str:
    c = result["contract"]
    case = c["case"]
    return (
        "C11-D RENDERER CHALLENGE COORDINATE+SAMPLE COMPOSITION PROPOSAL PASS"
        f" | spatial_projection={case['source_game_snapshot_count']}_RECORDS"
        f" | delivery_selection={case['source_game_snapshot_count']}TO{case['delivery_game_snapshot_count']}"
        f" | scale=2/3_UNIFORM"
        f" | winning_frame={case['winning_frame_absolute_source_index']}_TO_{case['winning_frame_absolute_delivery_index']}"
        " | interpolation=NONE"
        " | policy=PROPOSED_NOT_APPROVED"
        " | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE"
    )
