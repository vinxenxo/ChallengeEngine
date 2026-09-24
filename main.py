import argparse
import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication, QFileDialog, QMessageBox
from c11c_studio.core.config import AppConfig
from c11c_studio.core.project_context import ProjectContext
from c11c_studio.services.environment_validator import EnvironmentValidator
from c11c_studio.ui.theme import apply_dark_theme
from c11c_studio.ui.main_window import MainWindow

APP_NAME = "C11-C Studio"
APP_VERSION = "0.2.4"


def parse_args():
    p = argparse.ArgumentParser(prog="c11c-studio")
    p.add_argument("--project", type=str, default=None)
    p.add_argument("--validate", action="store_true")
    p.add_argument("--review-5x5", action="store_true")
    p.add_argument("--production-25", action="store_true")
    return p.parse_args()


def looks_like_project(path: Path) -> bool:
    return path.exists() and sum((path / x).exists() for x in ("project.godot", "tools", "artifacts")) >= 2


def main():
    args = parse_args()
    cfg = AppConfig.load()
    root = Path(args.project).expanduser().resolve() if args.project else None
    if root is None:
        saved = cfg.get("project_root")
        if saved and Path(saved).exists():
            root = Path(saved).resolve()

    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setApplicationVersion(APP_VERSION)
    apply_dark_theme(app)

    if root is None or not looks_like_project(root):
        chosen = QFileDialog.getExistingDirectory(None, "Select ChallengeEngineV01_STATELESS project root", str(Path.home()))
        if not chosen:
            return 2
        root = Path(chosen).resolve()
        if not looks_like_project(root):
            answer = QMessageBox.question(
                None,
                APP_NAME,
                "The selected folder does not look like a ChallengeEngine project.\n\n"
                + str(root)
                + "\n\nContinue anyway?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            if answer != QMessageBox.Yes:
                return 2
        cfg.set("project_root", str(root))
        cfg.save()

    ctx = ProjectContext.discover(root, cfg)

    if args.validate:
        report = EnvironmentValidator(ctx).run_all()
        for line in report.lines():
            print(line)
        return 0 if report.ok() else 1

    win = MainWindow(ctx, cfg, app_version=APP_VERSION)
    win.show()
    if args.review_5x5:
        win.trigger_review_5x5()
    elif args.production_25:
        win.trigger_production_25()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
