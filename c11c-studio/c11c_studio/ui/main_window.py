from datetime import datetime

from PySide6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
                               QLabel, QFrame, QStackedWidget, QStatusBar,
                               QMessageBox)
from PySide6.QtCore import QTimer, QUrl
from PySide6.QtGui import QDesktopServices

from ..core.config import AppConfig
from ..services.tool_discovery import discover_all
from ..services.family_registry import FamilyRegistry
from ..services.seed_manager import SeedManager
from ..services.command_builder import CommandBuilder
from ..services.job_manager import JobManager
from ..services.artifact_registry import ArtifactRegistry

from .widgets.nav_button import NavButton
from .pages.dashboard import DashboardPage
from .pages.review import ReviewPage
from .pages.production import ProductionPage
from .pages.families import FamiliesPage
from .pages.seeds import SeedsPage
from .pages.artifacts import ArtifactsPage
from .pages.logs import LogsPage
from .pages.validation import ValidationPage
from .pages.settings import SettingsPage
from .pages.about import AboutPage


class MainWindow(QMainWindow):
    def __init__(self, ctx, app_version="0.1.0"):
        super().__init__()
        self.ctx = ctx
        self.app_version = app_version
        self.cfg = AppConfig.load()

        self.family_registry = FamilyRegistry(ctx)
        self.families = self.family_registry.load()

        self.tools = discover_all(ctx.project_root)
        if self.tools.get("powershell") and self.tools["powershell"].present:
            ctx.powershell_path = self.tools["powershell"].path
        if self.tools.get("ffmpeg") and self.tools["ffmpeg"].present:
            ctx.ffmpeg_path = self.tools["ffmpeg"].path
        if self.tools.get("ffprobe") and self.tools["ffprobe"].present:
            ctx.ffprobe_path = self.tools["ffprobe"].path
        if self.tools.get("godot") and self.tools["godot"].present:
            ctx.godot_version = self.tools["godot"].version
        ctx.python_path = self.tools["python"].path

        self.seed_manager = SeedManager(ctx.paths.scratch / "seeds")
        self.command_builder = CommandBuilder(ctx)
        self.artifact_registry = ArtifactRegistry(ctx)
        self.job_manager = JobManager(log_dir=ctx.paths.scratch / "logs")

        self.job_manager.job_output.connect(self._on_job_output)
        self.job_manager.job_finished.connect(self._on_job_finished)
        self.job_manager.job_state_changed.connect(self._on_job_state)

        self.setWindowTitle("C11-C Studio - " + ctx.project_root.name)
        self.setMinimumSize(1024, 640)
        self.resize(1360, 860)

        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)
        root.addWidget(self._build_topbar())

        body = QHBoxLayout()
        body.setContentsMargins(0, 0, 0, 0)
        body.setSpacing(0)
        body.addWidget(self._build_nav())
        self.stack = QStackedWidget()
        body.addWidget(self.stack, 1)
        body_w = QWidget()
        body_w.setLayout(body)
        root.addWidget(body_w, 1)

        self.setStatusBar(QStatusBar())
        self.statusBar().showMessage("Ready.")

        self._build_pages()
        self._wire()
        self._refresh_dashboard_counts()

        self._timer = QTimer(self)
        self._timer.setInterval(15000)
        self._timer.timeout.connect(self._refresh_env_badge)
        self._timer.start()

    def _build_topbar(self):
        bar = QFrame()
        bar.setObjectName("TopBar")
        bar.setFixedHeight(56)
        h = QHBoxLayout(bar)
        h.setContentsMargins(16, 8, 16, 8)

        title = QLabel("C11-C Studio")
        title.setObjectName("TopBarTitle")
        h.addWidget(title)

        self.env_meta = QLabel(self._env_summary())
        self.env_meta.setObjectName("TopBarMeta")
        h.addWidget(self.env_meta)
        h.addStretch(1)

        project = QLabel("Project: " + str(self.ctx.project_root))
        project.setObjectName("TopBarMeta")
        h.addWidget(project)
        return bar

    def _env_summary(self):
        g = self.tools.get("godot")
        f1 = self.tools.get("ffmpeg")
        f2 = self.tools.get("ffprobe")
        gtag = ("OK " + (g.version or "")) if g and g.present else "MISSING"
        ftag = "OK" if f1 and f1.present else "MISSING"
        ptag = "OK" if f2 and f2.present else "MISSING"
        return ("Backend: " + self.ctx.backend_version + "   |   "
                "Godot: " + gtag + "   |   "
                "FFmpeg: " + ftag + "   |   "
                "FFprobe: " + ptag)

    def _refresh_env_badge(self):
        self.env_meta.setText(self._env_summary())

    def _build_nav(self):
        rail = QFrame()
        rail.setObjectName("NavRail")
        rail.setFixedWidth(210)
        v = QVBoxLayout(rail)
        v.setContentsMargins(10, 14, 10, 14)
        v.setSpacing(4)

        self.nav_buttons = []
        items = [
            ("Dashboard", 0), ("Review", 1), ("Production", 2),
            ("Families", 3), ("Seeds", 4), ("Artifacts", 5),
            ("Logs", 6), ("Validation", 7), ("Settings", 8),
            ("About / Diagnostics", 9),
        ]
        for label, idx in items:
            b = NavButton(label)
            b.clicked.connect(lambda _=False, i=idx: self._goto(i))
            v.addWidget(b)
            self.nav_buttons.append(b)
        v.addStretch(1)
        self.nav_buttons[0].setChecked(True)
        return rail

    def _build_pages(self):
        self.dashboard = DashboardPage(self.ctx, self.tools)
        self.review = ReviewPage(self.families)
        self.production = ProductionPage(self.families)
        self.families_page = FamiliesPage(self.families)
        self.seeds_page = SeedsPage(self.seed_manager)
        self.artifacts_page = ArtifactsPage(self.artifact_registry)
        self.logs_page = LogsPage()
        self.validation_page = ValidationPage(self.ctx)
        self.settings_page = SettingsPage(self.ctx, self.cfg)
        self.about_page = AboutPage(self.ctx, self.app_version)

        for w in (self.dashboard, self.review, self.production,
                  self.families_page, self.seeds_page, self.artifacts_page,
                  self.logs_page, self.validation_page, self.settings_page,
                  self.about_page):
            self.stack.addWidget(w)

    def _wire(self):
        self.dashboard.btn_validate.clicked.connect(self._goto_validate)
        self.dashboard.btn_review.clicked.connect(lambda: self._goto(1))
        self.dashboard.btn_produce.clicked.connect(lambda: self._goto(2))
        self.dashboard.btn_single.clicked.connect(lambda: self._goto(2))

        self.review.request_run.connect(self._on_review_run)
        self.production.request_single.connect(self._on_single_run)
        self.production.request_5x5.connect(self._on_5x5_run)

        self.families_page.request_review.connect(self._on_family_review)
        self.families_page.request_open_folder.connect(
            self._on_family_open_folder)

    def _goto(self, idx):
        self.stack.setCurrentIndex(idx)
        for i, b in enumerate(self.nav_buttons):
            b.setChecked(i == idx)

    def _goto_validate(self):
        self._goto(7)
        self.validation_page.run()

    def _on_family_review(self, folder):
        self.review.preselect_families([folder])
        self._goto(1)

    def _on_family_open_folder(self, folder):
        p = self.ctx.paths.prototypes / folder
        if not p.exists():
            alt = self.ctx.paths.review_assets / folder
            if alt.exists():
                p = alt
            else:
                QMessageBox.warning(
                    self, "Folder not found",
                    "Neither prototype nor review folder exists for:\n"
                    + folder + "\n\nLooked in:\n"
                    + str(self.ctx.paths.prototypes / folder) + "\n"
                    + str(alt))
                return
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(p)))

    def trigger_review_5x5(self):
        self._goto(1)
        self._on_review_run({
            "seed_count": 5,
            "audio": True,
            "families": [f.folder for f in self.families],
        })

    def trigger_production_25(self):
        self._goto(2)
        self._on_5x5_run({
            "seed_count": 5,
            "families": [f.folder for f in self.families],
            "audio": True,
            "footer": True,
            "pre_generated_seeds": None,
            "grammar": None,
            "allow_grammar": False,
        })

    def _on_review_run(self, cfg):
        if cfg.get("cancel"):
            self.job_manager.cancel_current()
            return
        folders = cfg.get("families", [])
        if not folders:
            QMessageBox.warning(self, "No families",
                                "Select at least one family to review.")
            return
        recs = self.seed_manager.random_batch(cfg.get("seed_count", 5))
        seeds = [r.seed for r in recs]
        spec = self.command_builder.review_5x5(
            seeds, folders, audio=cfg.get("audio", True))
        self._start("review_5x5", spec, cfg, seeds)
        self.review.set_running(True)

    def _on_single_run(self, cfg):
        spec = self.command_builder.production_single(
            cfg["family"], cfg["seed"],
            audio=cfg.get("audio", True),
            grammar=cfg.get("grammar"),
            allow_grammar=cfg.get("allow_grammar", False))
        self._start("production_single", spec, cfg, [cfg["seed"]])
        self.production.set_running(True)

    def _on_5x5_run(self, cfg):
        pre = cfg.get("pre_generated_seeds")
        if pre:
            seeds = list(pre)
            self.seed_manager.manual_batch(seeds)
        else:
            recs = self.seed_manager.random_batch(cfg.get("seed_count", 5))
            seeds = [r.seed for r in recs]
        spec = self.command_builder.production_5x5(
            seeds, cfg.get("families", []),
            audio=cfg.get("audio", True),
            grammar=cfg.get("grammar"),
            allow_grammar=cfg.get("allow_grammar", False))
        self._start("production_5x5", spec, cfg, seeds)
        self.production.set_running(True)

    def _start(self, jtype, spec, cfg, seeds):
        self.logs_page.view.append_text(
            "\n=== " + jtype + " @ "
            + datetime.now().isoformat(timespec="seconds") + " ===\n"
            "$ " + spec.display_command + "\n")
        try:
            job = self.job_manager.start_job(jtype, spec)
        except RuntimeError as e:
            QMessageBox.warning(self, "Job busy", str(e))
            return
        self.statusBar().showMessage(
            "Running " + jtype + " (" + job.id + ")...")
        self.dashboard.add_job_row(
            datetime.now().strftime("%H:%M:%S"), jtype, "-",
            ",".join(map(str, seeds))[:40], "RUNNING", "-")
        self._goto(6)

    def _on_job_output(self, job_id, chunk):
        self.logs_page.view.append_text(chunk)

    def _on_job_state(self, job_id, state):
        self.statusBar().showMessage("Job " + job_id + ": " + state)

    def _on_job_finished(self, job_id, code):
        job = self.job_manager.jobs[job_id]
        self.statusBar().showMessage(
            "Job " + job_id + " finished (exit " + str(code) + ") - "
            + job.state.value, 8000)
        self.dashboard.add_job_row(
            datetime.now().strftime("%H:%M:%S"), job.job_type,
            job.family or "-", str(job.seed or "-"),
            job.state.value, "-")
        self.review.set_running(False)
        self.production.set_running(False)
        self._refresh_dashboard_counts()

        if code != 0:
            self.logs_page.view.append_text(
                "\n[FAIL] Job returned non-zero exit. See raw log at: "
                + str(job.log_path) + "\n")

    def _refresh_dashboard_counts(self):
        prod_dir = self.ctx.paths.production
        review_dir = self.ctx.paths.review_assets
        n_prod = sum(1 for _ in prod_dir.rglob("*.mp4")) if prod_dir.exists() else 0
        n_rev = sum(1 for _ in review_dir.rglob("*.mp4")) if review_dir.exists() else 0
        self.dashboard.set_counts(n_prod, n_rev, len(self.families))
