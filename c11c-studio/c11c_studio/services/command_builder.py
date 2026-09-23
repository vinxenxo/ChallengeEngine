from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class CommandSpec:
    executable: str
    arguments: list = field(default_factory=list)
    working_directory: object = None
    environment: dict = field(default_factory=dict)
    display_command: str = ""

    def __post_init__(self):
        if not self.display_command:
            parts = []
            for a in [self.executable, *self.arguments]:
                if " " in a:
                    parts.append('"' + a + '"')
                else:
                    parts.append(a)
            self.display_command = " ".join(parts)


def _ps(powershell, script, args=()):
    argv = ["-NoProfile", "-ExecutionPolicy", "Bypass",
            "-File", str(script), *args]
    return CommandSpec(executable=powershell, arguments=argv,
                       working_directory=str(script.parent))


def _array_flag(flag, values):
    # Pass each value as its own argument so PowerShell's parameter binder
    # collects them into [int[]] / [string[]]. -File mode does NOT evaluate
    # the comma operator, so "1,2,3" cannot be cast to int[].
    out = [flag]
    out.extend(str(v) for v in values)
    return out


class CommandBuilder:
    def __init__(self, ctx):
        self.ctx = ctx
        self.ps = ctx.powershell_path or "powershell.exe"

    def validate_powershell(self):
        s = self.ctx.paths.bulk_tools / "validate_c11c_powershell.ps1"
        return _ps(self.ps, s)

    def validate_delivery(self):
        s = self.ctx.paths.bulk_tools / "validate_c11c_delivery_configuration.ps1"
        return _ps(self.ps, s)

    def review_5x5(self, seeds, families, audio=True):
        s = self.ctx.paths.bulk_tools / "run_c11c_art_direction_review.ps1"
        argv = []
        argv += _array_flag("-Seeds", seeds)
        argv += _array_flag("-Families", families)
        if not audio:
            argv.append("-NoSound")
        return _ps(self.ps, s, argv)

    def production_single(self, family, seed, audio=True,
                          grammar=None, allow_grammar=False):
        s = self.ctx.paths.bulk_tools / "run_c11c_production.ps1"
        argv = ["-Family", family, "-Seed", str(seed)]
        if allow_grammar and grammar:
            argv += ["-Grammar", grammar]
        if not audio:
            argv.append("-NoSound")
        return _ps(self.ps, s, argv)

    def production_5x5(self, seeds, families, audio=True,
                       grammar=None, allow_grammar=False):
        s = self.ctx.paths.bulk_tools / "run_c11c_production_bulk.ps1"
        argv = []
        argv += _array_flag("-Seeds", seeds)
        argv += _array_flag("-Families", families)
        if allow_grammar and grammar:
            argv += ["-Grammar", grammar]
        if not audio:
            argv.append("-NoSound")
        return _ps(self.ps, s, argv)

    def reproduce_family(self, family_folder, seed,
                         grammar=None, allow_grammar=False):
        s = self.ctx.paths.prototypes / family_folder / "run_prototype.ps1"
        argv = ["-Seed", str(seed)]
        if allow_grammar and grammar:
            argv += ["-Grammar", grammar]
        return _ps(self.ps, s, argv)
