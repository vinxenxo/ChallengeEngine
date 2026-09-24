from dataclasses import dataclass, field


@dataclass
class Parameter:
    id: str
    name: str
    type: str = "unknown"
    state: str = "READ_ONLY"
    description: str = ""
    default: object = None
    value: object = None
    minimum: object = None
    maximum: object = None
    step: object = None
    unit: str | None = None
    options: list = field(default_factory=list)
    source: str = ""
    family: str | None = None
    grammar: str | None = None

    @property
    def editable(self):
        return self.state in {"USER_CONFIGURABLE", "EXPERIMENTAL"}
