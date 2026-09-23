import uuid
from datetime import datetime
from pathlib import Path

from PySide6.QtCore import QObject, QProcess, Signal, QProcessEnvironment

from ..domain.job import Job, JobState


class JobManager(QObject):
    job_started = Signal(str)
    job_output = Signal(str, str)
    job_state_changed = Signal(str, str)
    job_finished = Signal(str, int)

    def __init__(self, log_dir, parent=None):
        super().__init__(parent)
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.jobs = {}
        self._current = None

    def start_job(self, job_type, spec, family=None, seed=None, batch_id=None):
        if self._current is not None:
            raise RuntimeError("A job is already running (spec 23).")

        jid = uuid.uuid4().hex[:10]
        log_path = self.log_dir / (jid + "_" + job_type + ".log")
        job = Job(id=jid, batch_id=batch_id, job_type=job_type,
                  family=family, seed=seed,
                  command=[spec.executable, *spec.arguments],
                  cwd=spec.working_directory,
                  display_command=spec.display_command,
                  log_path=log_path, state=JobState.STARTING,
                  started_at=datetime.now().isoformat(timespec="seconds"))
        self.jobs[jid] = job

        proc = QProcess(self)
        if spec.working_directory:
            proc.setWorkingDirectory(spec.working_directory)
        env = QProcessEnvironment.systemEnvironment()
        for k, v in spec.environment.items():
            env.insert(k, v)
        proc.setProcessEnvironment(env)
        proc.setProgram(spec.executable)
        proc.setArguments(spec.arguments)

        proc.readyReadStandardOutput.connect(lambda: self._on_stdout(jid))
        proc.readyReadStandardError.connect(lambda: self._on_stderr(jid))
        proc.finished.connect(lambda code, st: self._on_finished(jid, code))
        proc.errorOccurred.connect(lambda err: self._on_error(jid, err))

        self._current = (jid, proc)
        job.state = JobState.RUNNING
        self.job_started.emit(jid)
        self.job_state_changed.emit(jid, job.state.value)
        proc.start()
        return job

    def cancel_current(self):
        if not self._current:
            return
        jid, proc = self._current
        job = self.jobs[jid]
        job.state = JobState.CANCEL_REQUESTED
        self.job_state_changed.emit(jid, job.state.value)
        proc.kill()

    def _append(self, job, text):
        job.stdout += text
        if job.log_path:
            try:
                with job.log_path.open("a", encoding="utf-8") as fh:
                    fh.write(text)
            except Exception:
                pass
        self.job_output.emit(job.id, text)

    def _on_stdout(self, jid):
        cur = self._current
        if not cur or cur[0] != jid:
            return
        chunk = bytes(cur[1].readAllStandardOutput()).decode(
            "utf-8", errors="replace")
        self._append(self.jobs[jid], chunk)

    def _on_stderr(self, jid):
        cur = self._current
        if not cur or cur[0] != jid:
            return
        chunk = bytes(cur[1].readAllStandardError()).decode(
            "utf-8", errors="replace")
        job = self.jobs[jid]
        job.stderr += chunk
        self._append(job, chunk)

    def _on_finished(self, jid, code):
        job = self.jobs[jid]
        job.exit_code = code
        job.finished_at = datetime.now().isoformat(timespec="seconds")
        job.state = JobState.PASS if code == 0 else JobState.FAILED
        self.job_state_changed.emit(jid, job.state.value)
        self.job_finished.emit(jid, code)
        self._current = None

    def _on_error(self, jid, err):
        job = self.jobs[jid]
        job.errors.append(str(err))
        job.state = JobState.FAILED
        self.job_state_changed.emit(jid, job.state.value)
        self._current = None
