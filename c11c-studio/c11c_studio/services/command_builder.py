import subprocess
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class CommandSpec:
    executable: str
    arguments: list[str] = field(default_factory=list)
    working_directory: str | None = None
    environment: dict = field(default_factory=dict)
    display_command: str = ""

    def __post_init__(self):
        if not self.display_command:
            try:
                self.display_command = subprocess.list2cmdline([self.executable, *map(str, self.arguments)])
            except Exception:
                self.display_command = " ".join([self.executable, *map(str, self.arguments)])


def _ps(powershell, script, args=()):
    return CommandSpec(
        str(powershell),
        ["-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(script), *map(str, args)],
        str(Path(script).parent),
    )


def _arr(flag, values):
    return [flag, *[str(v) for v in values]]


class CommandBuilder:
    def __init__(self, ctx, catalog=None):
        self.ctx = ctx
        self.catalog = catalog
        self.ps = ctx.powershell_path or "powershell.exe"

    def _require(self, script):
        if not script.exists():
            raise FileNotFoundError(str(script))

    def _supported(self, script, param):
        return bool(self.catalog and self.catalog.script_supports(script, param))

    def _param_names(self, script) -> set[str]:
        cap = self.catalog.scripts.get(str(script)) if self.catalog else None
        return set(cap.parameters) if cap else set()

    def validate_powershell(self):
        return _ps(self.ps, self.ctx.paths.bulk_tools / "validate_c11c_powershell.ps1")

    def validate_delivery(self):
        return _ps(self.ps, self.ctx.paths.bulk_tools / "validate_c11c_delivery_configuration.ps1")

    def validate_preflight(self):
        p = self.ctx.paths.bulk_tools / "validate_c11c_preflight.ps1"
        return _ps(self.ps, p) if p.exists() else None

    def review(self, seeds, families, audio=True, reset=False, footer=True):
        p = self.ctx.paths.bulk_tools / "run_c11c_art_direction_review.ps1"
        self._require(p)
        params = self._param_names(p)
        args = _arr("-Seeds", seeds)
        if "Families" in params:
            args += _arr("-Families", families)
        else:
            canonical = {
                "c11c_geometric_waves_v1",
                "c11c_fractal_bloom_v1",
                "c11c_sacred_symmetry_v1",
                "c11c_living_particles_v1",
                "c11c_invisible_forces_v1",
            }
            if set(families) != canonical:
                raise ValueError(
                    "The canonical Art Direction Review launcher does not expose -Families. "
                    "Select all five canonical families for this operation."
                )
        for flag, enabled, param in (
            ("-NoSound", not audio, "NoSound"),
            ("-ResetReviewAssets", reset, "ResetReviewAssets"),
            ("-NoFooter", not footer, "NoFooter"),
        ):
            if enabled and self._supported(p, param):
                args.append(flag)
        return _ps(self.ps, p, args)

    def production_single(self, family, seed, audio=True, footer=True, force=False, grammar=None):
        p = self.ctx.paths.bulk_tools / "run_c11c_production.ps1"
        self._require(p)
        args = ["-Family", family, "-Seed", seed]
        for flag, enabled, param in (
            ("-NoSound", not audio, "NoSound"),
            ("-NoFooter", not footer, "NoFooter"),
            ("-Force", force, "Force"),
        ):
            if enabled and self._supported(p, param):
                args.append(flag)
        if grammar and self._supported(p, "Grammar"):
            args += ["-Grammar", grammar]
        return _ps(self.ps, p, args)

    def production_25(self, seeds, audio=True, footer=True, force=False):
        p = self.ctx.paths.bulk_tools / "run_c11c_production_25.ps1"
        self._require(p)
        args = _arr("-Seeds", seeds)
        for flag, enabled, param in (
            ("-NoSound", not audio, "NoSound"),
            ("-NoFooter", not footer, "NoFooter"),
            ("-Force", force, "Force"),
        ):
            if enabled and self._supported(p, param):
                args.append(flag)
        return _ps(self.ps, p, args)

    def production_family_bulk(self, family, seeds, audio=True, footer=True, force=False):
        p = self.ctx.paths.bulk_tools / "run_c11c_production_bulk.ps1"
        self._require(p)
        args = ["-Family", family] + _arr("-Seeds", seeds)
        for flag, enabled, param in (
            ("-NoSound", not audio, "NoSound"),
            ("-NoFooter", not footer, "NoFooter"),
            ("-Force", force, "Force"),
        ):
            if enabled and self._supported(p, param):
                args.append(flag)
        return _ps(self.ps, p, args)

    def all_families(self, seed, audio=True, footer=True):
        p = self.ctx.paths.bulk_tools / "run_all_c11c_visual_loops.ps1"
        self._require(p)
        args = ["-Seed", seed]
        if not audio and self._supported(p, "NoSound"):
            args.append("-NoSound")
        if not footer and self._supported(p, "NoFooter"):
            args.append("-NoFooter")
        return _ps(self.ps, p, args)

    def cleanup(self, apply=False):
        p = self.ctx.paths.bulk_tools / "clean_c11c_artifacts.ps1"
        self._require(p)
        return _ps(self.ps, p, ["-Apply"] if apply else [])

    def reset(self, apply=False):
        p = self.ctx.paths.bulk_tools / "reset_c11c_artifacts.ps1"
        self._require(p)
        return _ps(self.ps, p, ["-Apply"] if apply else [])

    def export_review_assets(self, seeds=None):
        p = self.ctx.paths.bulk_tools / "export_all_review_assets.ps1"
        self._require(p)
        return _ps(self.ps, p, _arr("-Seeds", seeds) if seeds else [])

    def reproduce_prototype(self, family, seed):
        p = self.ctx.paths.family_dir(family) / "run_prototype.ps1"
        self._require(p)
        return _ps(self.ps, p, ["-Seed", seed])
