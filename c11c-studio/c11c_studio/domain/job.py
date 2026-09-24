from dataclasses import dataclass, field, asdict
from enum import Enum
from pathlib import Path


class JobState(str, Enum):
    QUEUED="QUEUED"; STARTING="STARTING"; RUNNING="RUNNING"; RENDERING="RENDERING"; AUDIO="AUDIO"; MUXING="MUXING"; VALIDATING="VALIDATING"; PUBLISHED="PUBLISHED"; PASS="PASS"; FAILED="FAILED"; CANCEL_REQUESTED="CANCEL_REQUESTED"; CANCELLED="CANCELLED"; SKIPPED="SKIPPED"; BLOCKED="BLOCKED"


@dataclass
class Job:
    id: str
    batch_id: str | None
    job_type: str
    family: str | None
    seed: int | None
    state: JobState
    stage: str = "QUEUED"
    progress: int = 0
    started_at: str | None = None
    finished_at: str | None = None
    command: list = field(default_factory=list)
    cwd: str | None = None
    exit_code: int | None = None
    log_path: Path | None = None
    stdout: str = ""
    stderr: str = ""
    errors: list[str] = field(default_factory=list)
    output_paths: list[str] = field(default_factory=list)
    display_command: str = ""

    def serializable(self):
        d=asdict(self)
        d["state"]=self.state.value
        d["log_path"]=str(self.log_path) if self.log_path else None
        return d
