from dataclasses import dataclass, field


@dataclass
class Parameter:
    id: str
    name: str
    type: str
    state: str = "READ_ONLY"
    description: str = ""
    default: object = None
    value: object = None
    min: object = None
    max: object = None
    step: object = None
    unit: object = None
    options: list = field(default_factory=list)
    source: str = ""
    family: object = None
    grammar: object = None

    @property
    def editable(self):
        return self.state == "USER_CONFIGURABLE"
