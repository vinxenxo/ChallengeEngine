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
    grammars: list[str] = field(default_factory=list)
    palettes: list[str] = field(default_factory=list)
    parameters: list[Parameter] = field(default_factory=list)
    launcher_path: object = None
    shader_path: object = None
    scene_path: object = None
    capabilities: set[str] = field(default_factory=set)

    @property
    def default_duration(self):
        return 18.0
