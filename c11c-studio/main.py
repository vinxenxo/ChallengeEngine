import argparse
import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication, QFileDialog, QMessageBox

from c11c_studio.core.config import AppConfig
from c11c_studio.core.project_context import ProjectContext
from c11c_studio.ui.theme import apply_dark_theme
from c11c_studio.ui.main_window import MainWindow


APP_NAME = "C11-C Studio"
APP_VERSION = "0.1.0"


def parse_args():
    p = argparse.ArgumentParser(prog="c11c-studio")
    p.add_argument("--project", type=str, default=None)
    p.add_argument("--validate", action="store_true")
    p.add_argument("--review-5x5", action="store_true")
    p.add_argument("--production-25", action="store_true")
    return p.parse_args()


def resolve_project_root(cfg, cli_path):
    if cli_path:
        return Path(cli_path).expanduser().resolve()
    saved = cfg.get("project_root")
    if saved and Path(saved).exists():
        return Path(saved)
    return None


def looks_like_project(path):
    if not path or not path.exists():
        return False
    signals = ["project.godot", "tools", "artifacts"]
    return sum((path / s).exists() for s in signals) >= 2


def main():
    args = parse_args()
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setApplicationVersion(APP_VERSION)
    apply_dark_theme(app)

    cfg = AppConfig.load()
    root = resolve_project_root(cfg, args.project)

    if root is None or not looks_like_project(root):
        chosen = QFileDialog.getExistingDirectory(
            None, "Select ChallengeEngineV01_STATELESS project root",
            str(Path.home()))
        if not chosen:
            QMessageBox.warning(None, APP_NAME,
                "No project selected. Cannot start without a project root.")
            return 2
        root = Path(chosen).resolve()
        if not looks_like_project(root):
            resp = QMessageBox.question(
                None, APP_NAME,
                "The selected folder does not look like a ChallengeEngine "
                "project:\n" + str(root) + "\n\nContinue anyway?")
            if resp != QMessageBox.Yes:
                return 2
        cfg.set("project_root", str(root))
        cfg.save()

    ctx = ProjectContext.discover(root)

    if args.validate:
        from c11c_studio.services.environment_validator import EnvironmentValidator
        report = EnvironmentValidator(ctx).run_all()
        for line in report.lines():
            print(line)
        return 0 if report.ok() else 1

    win = MainWindow(ctx, app_version=APP_VERSION)
    win.show()

    if args.review_5x5:
        win.trigger_review_5x5()
    elif args.production_25:
        win.trigger_production_25()

    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
