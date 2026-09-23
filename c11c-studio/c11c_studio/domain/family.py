from dataclasses import dataclass, field

from .parameter import Parameter


@dataclass
class Family:
    id: str
    technical: str
    artistic: str
    folder: str
    short_description: str = ""
    visual_metaphor: str = ""
    grammars: list = field(default_factory=list)
    palette_bank: list = field(default_factory=list)
    parameters: list = field(default_factory=list)
    default_duration: float = 18.0
    audio_profile: str = "C11CSafeAmbient"

    @property
    def launcher_name(self):
        return "run_prototype.ps1"

    def has_grammars(self):
        return len(self.grammars) > 0
