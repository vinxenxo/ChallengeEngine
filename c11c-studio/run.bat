@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv" (
    echo [C11-C Studio] Creating venv...
    python -m venv .venv
)
call .venv\Scripts\activate.bat
python -c "import PySide6" 2>NUL
if errorlevel 1 (
    echo [C11-C Studio] Installing deps...
    pip install -r requirements.txt
)
python main.py %*
endlocal
