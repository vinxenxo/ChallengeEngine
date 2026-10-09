"""Read-only reconciliation of D renderer layout hierarchy with existing C11 frame contracts."""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping

CONTRACT_REL = Path("definitions/c11d/production/D_RENDERER_REGION_HIERARCHY_RECONCILIATION_V1.json")
SCHEMA_REL = Path("definitions/c11d/production/D_RENDERER_REGION_HIERARCHY_RECONCILIATION_SCHEMA_V1.json")
MANIFEST_REL = Path("release/C11C_FREEZE_PACKAGE_MANIFEST.json")
CATALOG_REL = Path("profiles/presentation/c11c_visual_family_catalog.json")
LEGACY_REGION_PROPOSAL_REL = Path("definitions/c11d/production/D_RENDERER_SEMANTIC_REGION_PROPOSAL_V1.json")
CONTRACT_ID = "C11-D-RENDERER-REGION-HIERARCHY-RECONCILIATION-CONTRACT-V1"
OUTPUT_SCHEMA = "C11-D-D9-RENDERER-REGION-HIERARCHY-RECONCILIATION-V1"
OUTPUT_STATUS = "PREPARATION_ONLY_RECONCILIATION_NOT_RENDERER_INPUT"
EXPECTED_MANIFEST_SHA256 = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
SUPPORTED_CONTENT = ("challenges", "visual_loops", "visual_drills")

class DRendererRegionHierarchyError(ValueError):
    """Invalid source contract, lineage or reconciliation report."""

def _root(project_root: Path | str | None = None) -> Path:
    return Path(project_root).resolve() if project_root is not None else Path(__file__).resolve().parents[3]

def _read_json(root: Path, rel: Path) -> dict[str, Any]:
    path = root / rel
    try:
        value = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        raise DRendererRegionHierarchyError(f"Cannot read JSON input {rel}: {exc}") from exc
    if not isinstance(value, dict):
        raise DRendererRegionHierarchyError(f"Expected JSON object at {rel}")
    return value

def _sha_file(path: Path) -> str:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except Exception as exc:
        raise DRendererRegionHierarchyError(f"Cannot hash {path}: {exc}") from exc

def _canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True, allow_nan=False)

def _sha_json(value: Any) -> str:
    return hashlib.sha256(_canonical(value).encode("utf-8")).hexdigest()

def _validate_sources(root: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    contract = _read_json(root, CONTRACT_REL)
    schema = _read_json(root, SCHEMA_REL)
    if contract.get("schema") != CONTRACT_ID or contract.get("schema_version") != "1.0":
        raise DRendererRegionHierarchyError("Region-hierarchy contract identity mismatch")
    if contract.get("status") != "PREPARATION_ONLY_RECONCILIATION_NOT_RENDERER_INPUT":
        raise DRendererRegionHierarchyError("Region-hierarchy contract was promoted beyond preparation-only")
    if contract.get("required_locks") != {
        "source_adapter_mode": "PREPARE_ONLY",
        "existing_c11c_source_mutation": False,
        "frozen_manifest_mutation": False,
        "geometry_approved_by_this_contract": False,
        "pixel_coordinates_emitted": False,
        "frame_schedule_defined": False,
        "renderer_native_input_emitted": False,
        "renderer_dispatch_invoked": False,
        "renderer_activation": False,
        "production_execution": False,
        "media_output_created": False,
        "output_artifact_path": None,
        "d4_8": "BLOCKED",
        "release_authority": "NONE",
        "d9_14_full_acceptance": "BLOCKED_AS_REQUIRED",
        "d9_16_full_acceptance": "BLOCKED_AS_REQUIRED",
        "d9_17_closure": "BLOCKED_NO_GO",
        "d10": "BLOCKED",
    }:
        raise DRendererRegionHierarchyError("Region-hierarchy governance lock mismatch")
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema" or schema.get("$id") != "urn:c11d:renderer-region-hierarchy-reconciliation:v1" or schema.get("additionalProperties") is not False:
        raise DRendererRegionHierarchyError("Reconciliation output schema identity/strictness mismatch")

    manifest_sha = _sha_file(root / MANIFEST_REL)
    if manifest_sha != EXPECTED_MANIFEST_SHA256 or contract.get("source_of_truth", {}).get("frozen_c11c_manifest_sha256") != EXPECTED_MANIFEST_SHA256:
        raise DRendererRegionHierarchyError("Immutable C11-C manifest hash does not match the locked reference")

    expected_canvas = {"width": 540, "height": 960, "units": "LOGICAL_PRESENTATION_COORDINATES"}
    expected_regions = [
        {"region_id": "HEADER", "x": 0, "y": 0, "width": 540, "height": 144, "units": "LOGICAL_PRESENTATION_COORDINATES", "authority": "D1.5_EXISTING"},
        {"region_id": "BODY", "x": 0, "y": 144, "width": 540, "height": 672, "units": "LOGICAL_PRESENTATION_COORDINATES", "authority": "D1.5_EXISTING"},
        {"region_id": "FOOTER", "x": 0, "y": 816, "width": 540, "height": 144, "units": "LOGICAL_PRESENTATION_COORDINATES", "authority": "D1.5_EXISTING"},
    ]
    frame_contract = contract.get("delivery_and_logical_frame", {})
    if frame_contract.get("logical_canvas") != expected_canvas or frame_contract.get("shared_regions") != expected_regions:
        raise DRendererRegionHierarchyError("The reconciliation must preserve the exact existing D1.5 shared-frame geometry")
    proposal = contract.get("previous_normalized_region_proposal", {})
    if proposal.get("numeric_bounds_are_canonical") is not False or proposal.get("may_drive_temporal_schedule") is not False or proposal.get("may_emit_pixel_coordinates") is not False or proposal.get("may_drive_renderer_dispatch") is not False:
        raise DRendererRegionHierarchyError("The exploratory normalized proposal must remain noncanonical and non-executable")

    required_sources = [
        "docs/current/d/D1.5_PLATFORM_LAYOUT_TEMPLATE_CONTRACT.md",
        "profiles/delivery/c11c_video_delivery_profiles.json",
        "profiles/presentation/c11c_visual_family_catalog.json",
        "core/presentation/PresentationProfile.gd",
        "core/presentation/VisualLoopPresentationBinder.gd",
        "core/presentation/rendering/VisualLoopRenderer.gd",
        "definitions/c11d/production/D_RENDERER_SEMANTIC_REGION_PROPOSAL_V1.json",
    ]
    for rel_text in required_sources:
        if not (root / rel_text).is_file():
            raise DRendererRegionHierarchyError(f"Required layout source is missing: {rel_text}")

    d15 = (root / "docs/current/d/D1.5_PLATFORM_LAYOUT_TEMPLATE_CONTRACT.md").read_text(encoding="utf-8-sig")
    for marker in (
        "Rect2(0, 0, 540, 144)",
        "Rect2(0, 144, 540, 672)",
        "Rect2(0, 816, 540, 144)",
        "BodyUIOverlay",
        "CTA geometry",
        "remain UNKNOWN",
    ):
        if marker not in d15:
            raise DRendererRegionHierarchyError(f"D1.5 layout evidence changed/missing: {marker}")

    profile = (root / "core/presentation/PresentationProfile.gd").read_text(encoding="utf-8-sig")
    for marker in ("func get_composition_geometry()", "func get_social_regions()", "safe_area", '"body_rect"'):
        if marker not in profile:
            raise DRendererRegionHierarchyError(f"Existing PresentationProfile geometry contract missing: {marker}")
    binder = (root / "core/presentation/VisualLoopPresentationBinder.gd").read_text(encoding="utf-8-sig")
    if 'model["geometry"] = profile.get_composition_geometry()' not in binder or 'model["visual_frame_state"]' not in binder:
        raise DRendererRegionHierarchyError("Existing Visual Loop binder geometry/payload routing changed")
    router = (root / "core/presentation/rendering/VisualLoopRenderer.gd").read_text(encoding="utf-8-sig")
    for marker in ("FractalRendererClass", "VectorFieldRendererClass", "ParticleFlowRendererClass", "KaleidoscopeRendererClass", "GeometricRendererClass"):
        if marker not in router:
            raise DRendererRegionHierarchyError(f"Existing five-family render route missing: {marker}")

    legacy = _read_json(root, LEGACY_REGION_PROPOSAL_REL)
    if legacy.get("status") != "PREPARATION_ONLY_NOT_APPROVED_NOT_FROZEN":
        raise DRendererRegionHierarchyError("Earlier normalized region proposal was unexpectedly promoted")
    if legacy.get("required_locks", {}).get("region_layout_approved") is not False:
        raise DRendererRegionHierarchyError("Earlier normalized region proposal self-asserts layout approval")

    catalog = _read_json(root, CATALOG_REL)
    families = catalog.get("families")
    if not isinstance(families, list) or len(families) != 5:
        raise DRendererRegionHierarchyError("Visual Loop family catalog must keep the canonical five-family identity list")
    expected_names = ["Geometric Waves", "Fractal Bloom", "Sacred Symmetry", "Living Particles", "Invisible Forces"]
    if [item.get("artistic_name") for item in families] != expected_names:
        raise DRendererRegionHierarchyError("Visual Loop family names/order drifted from the canonical catalog")
    canonical_identities = contract.get("visual_loop_families", {}).get("canonical_identities")
    family_keys = ("technical_id", "artistic_name", "production_id", "runtime_id")
    source_identities = [{key: item.get(key) for key in family_keys} for item in families]
    if canonical_identities != source_identities:
        raise DRendererRegionHierarchyError("Visual Loop family technical/production/runtime aliases drifted")
    return contract, catalog

def _build_expected(content_type: str, root: Path, contract: Mapping[str, Any], catalog: Mapping[str, Any]) -> dict[str, Any]:
    if content_type not in SUPPORTED_CONTENT:
        raise DRendererRegionHierarchyError("Unsupported content type; Longform and unknown types fail closed")
    region_frame = contract["delivery_and_logical_frame"]
    families = [
        {key: family[key] for key in ("technical_id", "artistic_name", "production_id", "runtime_id")}
        for family in catalog["families"]
    ]
    raw: dict[str, Any] = {
        "schema": OUTPUT_SCHEMA,
        "schema_version": "1.0",
        "status": OUTPUT_STATUS,
        "content_type": content_type,
        "contract_sha256": _sha_file(root / CONTRACT_REL),
        "manifest_sha256": _sha_file(root / MANIFEST_REL),
        "logical_canvas": copy.deepcopy(region_frame["logical_canvas"]),
        "shared_regions": copy.deepcopy(region_frame["shared_regions"]),
        "visual_loop_families": families,
        "previous_proposal_disposition": {
            "status": "RETAINED_AS_UNAPPROVED_EXPLORATORY_PROPOSAL_ONLY",
            "numeric_bounds_are_canonical": False,
            "may_drive_temporal_schedule": False,
        },
        "temporal_schedule": {
            "state": "NOT_DEFINED",
            "frame_indices_emitted": False,
            "durations_emitted": False,
            "transitions_emitted": False,
        },
        "execution_boundary": {
            "source_adapter_mode": "PREPARE_ONLY",
            "renderer_native_input_emitted": False,
            "renderer_dispatch_invoked": False,
            "renderer_activation": False,
            "media_output_created": False,
            "d4_8": "BLOCKED",
            "release_authority": "NONE",
        },
    }
    raw["reconciliation_sha256"] = _sha_json(raw)
    return raw

def build_region_hierarchy_reconciliation(content_type: str, project_root: Path | str | None = None) -> dict[str, Any]:
    root = _root(project_root)
    contract, catalog = _validate_sources(root)
    result = _build_expected(content_type, root, contract, catalog)
    validate_region_hierarchy_reconciliation(result, project_root=root)
    return result

def validate_region_hierarchy_reconciliation(candidate: Mapping[str, Any], project_root: Path | str | None = None) -> None:
    if not isinstance(candidate, Mapping):
        raise DRendererRegionHierarchyError("Reconciliation candidate must be a mapping")
    root = _root(project_root)
    contract, catalog = _validate_sources(root)
    ctype = candidate.get("content_type")
    expected = _build_expected(str(ctype), root, contract, catalog)
    if dict(candidate) != expected:
        raise DRendererRegionHierarchyError("Reconciliation mismatch, mutation, stale lineage or attempted authority escalation")

    schema = _read_json(root, SCHEMA_REL)
    required = schema.get("required", [])
    if set(candidate.keys()) != set(required):
        raise DRendererRegionHierarchyError("Reconciliation report shape does not match strict schema required fields")
    for region in candidate.get("shared_regions", []):
        if region["x"] < 0 or region["y"] < 0 or region["width"] <= 0 or region["height"] <= 0:
            raise DRendererRegionHierarchyError("Invalid shared region geometry")
        if region["x"] + region["width"] > 540 or region["y"] + region["height"] > 960:
            raise DRendererRegionHierarchyError("Shared region exceeds the existing logical canvas")

