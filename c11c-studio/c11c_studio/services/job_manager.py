import json
import uuid
from datetime import datetime
from pathlib import Path
from PySide6.QtCore import QObject, QProcess, QProcessEnvironment, Signal
from ..domain.job import Job, JobState
from .log_parser import parse


class JobManager(QObject):
    job_started = Signal(str)
    job_output = Signal(str, str, str)
    job_state_changed = Signal(str, str)
    job_finished = Signal(str, int)

    def __init__(self, workspace, parent=None):
        super().__init__(parent)
        self.workspace = Path(workspace)
        self.log_dir = self.workspace
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.jobs = {}
        self.current_id = None
        self.process = None
        self.cancel_requested = False
        self._load()

    def _load(self):
        for p in self.log_dir.glob("*.json"):
            try:
                d = json.loads(p.read_text(encoding="utf-8"))
                j = Job(
                    d["id"], d.get("batch_id"), d.get("job_type", "unknown"),
                    d.get("family"), d.get("seed"), JobState(d.get("state", "FAILED")),
                    d.get("stage", "FAILED"), int(d.get("progress", 0)),
                    d.get("started_at"), d.get("finished_at"), d.get("command", []),
                    d.get("cwd"), d.get("exit_code"),
                    Path(d["log_path"]) if d.get("log_path") else None,
                    d.get("stdout", ""), d.get("stderr", ""), d.get("errors", []),
                    d.get("output_paths", []), d.get("display_command", ""),
                )
                self.jobs[j.id] = j
            except Exception:
                continue

    def start(self, job_type, spec, family=None, seed=None, batch_id=None):
        if self.process is not None:
            raise RuntimeError("A generation job is already running.")
        if not spec or not spec.executable:
            raise ValueError("Cannot start an empty command specification.")

        jid = uuid.uuid4().hex[:10]
        log = self.log_dir / (jid + "_" + job_type + ".log")
        j = Job(
            jid, batch_id, job_type, family, seed, JobState.STARTING,
            started_at=datetime.now().isoformat(timespec="seconds"),
            command=[spec.executable, *spec.arguments],
            cwd=spec.working_directory,
            log_path=log,
            display_command=spec.display_command,
        )
        self.jobs[jid] = j
        self.current_id = jid
        self.cancel_requested = False
        self.process = QProcess(self)
        if spec.working_directory:
            self.process.setWorkingDirectory(spec.working_directory)
        env = QProcessEnvironment.systemEnvironment()
        for k, v in spec.environment.items():
            env.insert(k, str(v))
        self.process.setProcessEnvironment(env)
        self.process.setProgram(spec.executable)
        self.process.setArguments(spec.arguments)
        self.process.readyReadStandardOutput.connect(lambda: self._read(False))
        self.process.readyReadStandardError.connect(lambda: self._read(True))
        self.process.started.connect(self._started)
        self.process.finished.connect(self._finished)
        self.process.errorOccurred.connect(self._error)
        self._state(JobState.STARTING, "STARTING")
        self.job_started.emit(jid)
        self.process.start()
        return j

    def _started(self):
        if self.current_id and self.current_id in self.jobs:
            self._state(JobState.RUNNING, "RUNNING")

    def cancel_current(self):
        if self.process is None:
            return
        self.cancel_requested = True
        self._state(JobState.CANCEL_REQUESTED, "CANCEL_REQUESTED")
        self.process.kill()

    def _read(self, is_err):
        if self.process is None or not self.current_id:
            return
        raw = self.process.readAllStandardError() if is_err else self.process.readAllStandardOutput()
        text = bytes(raw).decode("utf-8", errors="replace")
        j = self.jobs[self.current_id]
        if is_err:
            j.stderr += text
        else:
            j.stdout += text
        try:
            with j.log_path.open("a", encoding="utf-8") as fh:
                fh.write(("[STDERR] " if is_err else "") + text)
        except OSError:
            pass
        parsed = parse(text)
        if parsed.stage:
            stage_state = {
                "RENDERING": JobState.RENDERING,
                "AUDIO": JobState.AUDIO,
                "MUXING": JobState.MUXING,
                "VALIDATING": JobState.VALIDATING,
                "PUBLISHED": JobState.PUBLISHED,
                "PRODUCTION-25": JobState.RENDERING,
            }.get(parsed.stage)
            if stage_state:
                self._state(stage_state, parsed.stage)
        if parsed.progress is not None:
            j.progress = parsed.progress
        self.job_output.emit(j.id, "stderr" if is_err else "stdout", text)

    def _state(self, state, stage=None):
        if not self.current_id or self.current_id not in self.jobs:
            return
        j = self.jobs[self.current_id]
        j.state = state
        j.stage = stage or state.value
        self.job_state_changed.emit(j.id, j.stage)

    def _error(self, error):
        if not self.current_id or self.current_id not in self.jobs:
            return
        message = str(error)
        self.jobs[self.current_id].errors.append(message)
        if self.process is not None and self.process.state() == QProcess.NotRunning:
            self._state(JobState.FAILED, "FAILED")

    def _finished(self, code, status):
        jid = self.current_id
        if not jid or jid not in self.jobs:
            return
        self._read(False)
        self._read(True)
        j = self.jobs[jid]
        j.exit_code = code
        j.finished_at = datetime.now().isoformat(timespec="seconds")
        if self.cancel_requested:
            j.state = JobState.CANCELLED
            j.stage = "CANCELLED"
        else:
            j.state = JobState.PASS if code == 0 else JobState.FAILED
            j.stage = j.state.value
        self._persist(j)
        self.job_state_changed.emit(jid, j.stage)
        self.job_finished.emit(jid, code)
        if self.process is not None:
            self.process.deleteLater()
        self.process = None
        self.current_id = None
        self.cancel_requested = False

    def _persist(self, j):
        try:
            (self.log_dir / (j.id + ".json")).write_text(
                json.dumps(j.serializable(), ensure_ascii=False, indent=2), encoding="utf-8"
            )
        except OSError:
            pass
