from ..core.project_context import ProjectContext
from ..domain.family import Family
from ..domain.parameter import Parameter


_CANONICAL = [
    {
        "id": "c11c_geometric_waves_v1",
        "technical": "geometric",
        "artistic": "Geometric Waves",
        "folder": "c11c_geometric_waves_v1",
        "short_description": "Harmonic loom. Liquid architecture.",
        "visual_metaphor": "Wave interference; tension/release; deterministic geometry",
        "grammars": [],
        "palette_bank": ["cyan", "magenta", "white"],
        "parameters": [
            ("frequency", "float", "SEED_DERIVED"),
            ("phase", "float", "SEED_DERIVED"),
            ("amplitude", "float", "SEED_DERIVED"),
            ("morph", "float", "SEED_DERIVED"),
            ("polygon_order", "integer", "SEED_DERIVED"),
            ("layer_count", "integer", "SEED_DERIVED"),
            ("palette_anchor", "color", "SEED_DERIVED"),
        ],
    },
    {
        "id": "c11c_fractal_bloom_v1",
        "technical": "fractal",
        "artistic": "Fractal Bloom",
        "folder": "c11c_fractal_bloom_v1",
        "short_description": "Mycelium, neural synapses, infinite universe.",
        "visual_metaphor": "z(n+1) = z(n)^2 + c; radial nucleus; controlled zoom",
        "grammars": ["RADIAL BLOOM", "DENDRITIC TUNNEL", "SPIRAL FRACTAL",
                     "FRACTAL FILIGREE", "NESTED WORLDS"],
        "palette_bank": ["indigo", "violet", "cyan"],
        "parameters": [
            ("julia_constant", "float", "SEED_DERIVED"),
            ("detail", "float", "SEED_DERIVED"),
            ("branching", "float", "SEED_DERIVED"),
            ("zoom", "float", "SEED_DERIVED"),
            ("domain_warp", "float", "SEED_DERIVED"),
            ("depth_layers", "integer", "SEED_DERIVED"),
            ("color_diversity", "float", "SEED_DERIVED"),
        ],
    },
    {
        "id": "c11c_sacred_symmetry_v1",
        "technical": "kaleidoscope",
        "artistic": "Sacred Symmetry",
        "folder": "c11c_sacred_symmetry_v1",
        "short_description": "Generative astrolabe. Celestial mechanism.",
        "visual_metaphor": "Radial symmetry; clockwork motion; precision",
        "grammars": [],
        "palette_bank": ["gold", "amber", "copper"],
        "parameters": [
            ("symmetry_order", "integer", "SEED_DERIVED"),
            ("ring_count", "integer", "SEED_DERIVED"),
            ("gear_count", "integer", "SEED_DERIVED"),
            ("gear_ratio", "string", "SEED_DERIVED"),
            ("rotation_phase", "float", "SEED_DERIVED"),
        ],
    },
    {
        "id": "c11c_living_particles_v1",
        "technical": "particle_flow",
        "artistic": "Living Particles",
        "folder": "c11c_living_particles_v1",
        "short_description": "Magnetic dust, ink in fluid, attractors, eddies.",
        "visual_metaphor": "Emergent flow; collisions; trail persistence",
        "grammars": [],
        "palette_bank": ["emerald", "sea-green", "turquoise"],
        "parameters": [
            ("particle_count", "integer", "SEED_DERIVED"),
            ("density", "float", "SEED_DERIVED"),
            ("flow", "float", "SEED_DERIVED"),
            ("attractors", "integer", "SEED_DERIVED"),
            ("collisions", "boolean", "SEED_DERIVED"),
            ("trail_persistence", "float", "SEED_DERIVED"),
        ],
    },
    {
        "id": "c11c_invisible_forces_v1",
        "technical": "vector_field",
        "artistic": "Invisible Forces",
        "folder": "c11c_invisible_forces_v1",
        "short_description": "Solar wind, gravitational topography, field traces.",
        "visual_metaphor": "No ves la fuerza, solo su rastro",
        "grammars": ["TOPOGRAPHIC_BASIN"],
        "palette_bank": ["crimson", "orange", "yellow"],
        "parameters": [
            ("field_config", "string", "SEED_DERIVED"),
            ("trace_count", "integer", "SEED_DERIVED"),
            ("pulse_speed", "float", "SEED_DERIVED"),
            ("field_phase", "float", "SEED_DERIVED"),
            ("trace_curvature", "float", "SEED_DERIVED"),
        ],
    },
]


def _to_parameter(t):
    pid, ptype, pstate = t
    return Parameter(id=pid, name=pid.replace("_", " ").title(),
                     type=ptype, state=pstate, source="canonical")


class FamilyRegistry:
    def __init__(self, ctx):
        self.ctx = ctx
        self._families = []

    def load(self):
        canonical_by_folder = {c["folder"]: c for c in _CANONICAL}
        discovered = []

        protos = self.ctx.paths.prototypes
        if protos.exists():
            for d in sorted(protos.iterdir()):
                if not d.is_dir() or not d.name.startswith("c11c_"):
                    continue
                if d.name in ("c11c_bulk", "c11c_common", "c11c_review_assets"):
                    continue
                meta = canonical_by_folder.get(d.name)
                if meta:
                    discovered.append(self._from_meta(meta))
                else:
                    stem = d.name.replace("c11c_", "").replace("_v1", "")
                    discovered.append(Family(
                        id=d.name, technical=stem,
                        artistic=stem.replace("_", " ").title(),
                        folder=d.name,
                        short_description="Discovered family."))

        if not discovered:
            discovered = [self._from_meta(m) for m in _CANONICAL]

        self._families = discovered
        return discovered

    def _from_meta(self, meta):
        return Family(
            id=meta["id"],
            technical=meta["technical"],
            artistic=meta["artistic"],
            folder=meta["folder"],
            short_description=meta.get("short_description", ""),
            visual_metaphor=meta.get("visual_metaphor", ""),
            grammars=list(meta.get("grammars", [])),
            palette_bank=list(meta.get("palette_bank", [])),
            parameters=[_to_parameter(t) for t in meta.get("parameters", [])],
        )

    @property
    def families(self):
        return self._families
