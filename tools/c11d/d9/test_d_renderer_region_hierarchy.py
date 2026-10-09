"""Focused tests for D renderer region hierarchy reconciliation; no media or dispatch."""
from __future__ import annotations
import copy
import json
from pathlib import Path
from typing import Any

from d_renderer_region_hierarchy import (
    DRendererRegionHierarchyError,
    build_region_hierarchy_reconciliation,
    validate_region_hierarchy_reconciliation,
)

ROOT = Path(__file__).resolve().parents[3]
SUPPORTED = ("challenges", "visual_loops", "visual_drills")

def _reject(label: str, fn) -> None:
    try:
        fn()
    except (DRendererRegionHierarchyError, KeyError, TypeError, ValueError):
        return
    raise AssertionError(f"Negative control failed to reject: {label}")

def run_checks() -> dict[str, int]:
    content_checks = deterministic_checks = family_checks = 0
    schema_checks = jsonschema_checks = 0
    expected_regions = [
        {"region_id": "HEADER", "x": 0, "y": 0, "width": 540, "height": 144, "units": "LOGICAL_PRESENTATION_COORDINATES", "authority": "D1.5_EXISTING"},
        {"region_id": "BODY", "x": 0, "y": 144, "width": 540, "height": 672, "units": "LOGICAL_PRESENTATION_COORDINATES", "authority": "D1.5_EXISTING"},
        {"region_id": "FOOTER", "x": 0, "y": 816, "width": 540, "height": 144, "units": "LOGICAL_PRESENTATION_COORDINATES", "authority": "D1.5_EXISTING"},
    ]
    outputs = []
    for ctype in SUPPORTED:
        a = build_region_hierarchy_reconciliation(ctype, ROOT)
        b = build_region_hierarchy_reconciliation(ctype, ROOT)
        assert a == b, f"non-deterministic reconciliation for {ctype}"
        validate_region_hierarchy_reconciliation(a, ROOT)
        assert a["shared_regions"] == expected_regions
        assert a["logical_canvas"] == {"width": 540, "height": 960, "units": "LOGICAL_PRESENTATION_COORDINATES"}
        assert a["status"] == "PREPARATION_ONLY_RECONCILIATION_NOT_RENDERER_INPUT"
        assert a["content_type"] == ctype
        content_checks += 1
        deterministic_checks += 1
        outputs.append(a)

    canonical_names = ["Geometric Waves", "Fractal Bloom", "Sacred Symmetry", "Living Particles", "Invisible Forces"]
    canonical_ids = ["geometric", "fractal", "kaleidoscope", "particle_flow", "vector_field"]
    canonical_runtimes = ["geometric", "fractal", "sacred_symmetry", "living_particles", "invisible_forces"]
    for out in outputs:
        assert [family["artistic_name"] for family in out["visual_loop_families"]] == canonical_names
        assert [family["technical_id"] for family in out["visual_loop_families"]] == canonical_ids
        assert [family["runtime_id"] for family in out["visual_loop_families"]] == canonical_runtimes
        family_checks += 1
    assert all(len(out["visual_loop_families"]) == 5 for out in outputs)

    # The optional schema package is an enhancement; strict structural and exact-contract
    # validation always runs on supported Python installations.
    schema_path = ROOT / "definitions/c11d/production/D_RENDERER_REGION_HIERARCHY_RECONCILIATION_SCHEMA_V1.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    for out in outputs:
        assert set(out) == set(schema["required"])
        assert schema["additionalProperties"] is False
        schema_checks += 1
    try:
        from jsonschema import Draft202012Validator
    except ImportError:
        jsonschema_checks = 0
    else:
        validator = Draft202012Validator(schema)
        for out in outputs:
            errors = list(validator.iter_errors(out))
            if errors:
                raise AssertionError("JSON Schema rejection: " + "; ".join(str(e.message) for e in errors))
            jsonschema_checks += 1

    base = outputs[0]
    mutations: list[tuple[str, Any]] = []
    x = copy.deepcopy(base); x["shared_regions"][0]["width"] = 999; mutations.append(("custom header geometry", x))
    x = copy.deepcopy(base); x["shared_regions"][1]["y"] = 705; mutations.append(("normalized content-stage replacement", x))
    x = copy.deepcopy(base); x["shared_regions"][1]["region_id"] = "CONTENT_STAGE"; mutations.append(("relabel BODY as CONTENT_STAGE", x))
    x = copy.deepcopy(base); x["previous_proposal_disposition"]["numeric_bounds_are_canonical"] = True; mutations.append(("promote exploratory numeric bounds", x))
    x = copy.deepcopy(base); x["previous_proposal_disposition"]["may_drive_temporal_schedule"] = True; mutations.append(("schedule uses unapproved proposal", x))
    x = copy.deepcopy(base); x["temporal_schedule"]["state"] = "APPROVED"; mutations.append(("temporal self-approval", x))
    x = copy.deepcopy(base); x["temporal_schedule"]["durations_emitted"] = True; mutations.append(("invented durations", x))
    x = copy.deepcopy(base); x["execution_boundary"]["renderer_native_input_emitted"] = True; mutations.append(("renderer-native input escalation", x))
    x = copy.deepcopy(base); x["execution_boundary"]["renderer_dispatch_invoked"] = True; mutations.append(("dispatch escalation", x))
    x = copy.deepcopy(base); x["execution_boundary"]["renderer_activation"] = True; mutations.append(("renderer activation", x))
    x = copy.deepcopy(base); x["execution_boundary"]["media_output_created"] = True; mutations.append(("media creation", x))
    x = copy.deepcopy(base); x["execution_boundary"]["d4_8"] = "AUTHORIZED"; mutations.append(("D4.8 escalation", x))
    x = copy.deepcopy(base); x["execution_boundary"]["release_authority"] = "GRANTED"; mutations.append(("release authority escalation", x))
    x = copy.deepcopy(base); x["manifest_sha256"] = "0" * 64; mutations.append(("manifest lineage tamper", x))
    x = copy.deepcopy(base); x["visual_loop_families"].pop(); mutations.append(("family omission", x))
    x = copy.deepcopy(base); x["visual_loop_families"][0]["artistic_name"] = "Other Family"; mutations.append(("family identity mutation", x))
    x = copy.deepcopy(base); x["content_type"] = "longform"; mutations.append(("unsupported content type", x))
    x = copy.deepcopy(base); x["unexpected"] = True; mutations.append(("unknown output field", x))
    x = copy.deepcopy(base); x["reconciliation_sha256"] = "f" * 64; mutations.append(("report hash mutation", x))
    for label, candidate in mutations:
        _reject(label, lambda candidate=candidate: validate_region_hierarchy_reconciliation(candidate, ROOT))

    _reject("direct longform build", lambda: build_region_hierarchy_reconciliation("longform", ROOT))
    _reject("unknown content build", lambda: build_region_hierarchy_reconciliation("mystery", ROOT))
    negatives = len(mutations) + 2
    return {
        "content_types": content_checks,
        "deterministic": deterministic_checks,
        "family_catalog": family_checks,
        "negative": negatives,
        "schema": schema_checks,
        "jsonschema": jsonschema_checks,
    }

def main() -> int:
    r = run_checks()
    print(
        "C11-D RENDERER REGION HIERARCHY RECONCILIATION PASS"
        f" | content_types={r['content_types']}/3"
        f" | deterministic={r['deterministic']}/3"
        f" | family_catalog={r['family_catalog']}/3"
        f" | negative={r['negative']}/21"
        f" | schema={r['schema']}/3"
        + (f" | jsonschema={r['jsonschema']}/3" if r['jsonschema'] == 3 else " | jsonschema=NOT_INSTALLED (strict structural checks PASS)")
        + " | frame=D1.5_EXISTING"
        + " | family_geometry=EXISTING_PROFILE_AND_RENDERER"
        + " | normalized_proposal=UNAPPROVED_NONCANONICAL"
        + " | frame_schedule=NOT_DEFINED"
        + " | renderer_input=NOT_EMITTED"
        + " | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE"
    )
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
