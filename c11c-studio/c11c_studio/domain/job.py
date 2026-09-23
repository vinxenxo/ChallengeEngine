from dataclasses import dataclass, field
from enum import Enum


class JobState(str, Enum):
    QUEUED = "QUEUED"
    STARTING = "STARTING"
    RUNNING = "RUNNING"
    RENDERING = "RENDERING"
    AUDIO = "AUDIO"
    MUXING = "MUXING"
    VALIDATING = "VALIDATING"
    EXPORTING = "EXPORTING"
    PUBLISHED = "PUBLISHED"
    PASS = "PASS"
    FAILED = "FAILED"
    CANCEL_REQUESTED = "CANCEL_REQUESTED"
    CANCELLED = "CANCELLED"
    SKIPPED = "SKIPPED"
    BLOCKED = "BLOCKED"


@dataclass
class Job:
    id: str
    batch_id: object
    job_type: str
    family: object = None
    seed: object = None
    state: JobState = JobState.QUEUED
    started_at: object = None
    finished_at: object = None
    command: list = field(default_factory=list)
    cwd: object = None
    exit_code: object = None
    log_path: object = None
    stdout: str = ""
    stderr: str = ""
    outputs: list = field(default_factory=list)
    errors: list = field(default_factory=list)
    display_command: str = ""
