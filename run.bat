@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv" (
  echo [C11-C Studio] Creating virtual environment...
  python -m venv .venv
  if errorlevel 1 exit /b 1
)
call .venv\Scripts\activate.bat
python -c "import PySide6" >nul 2>&1
if errorlevel 1 (
  echo [C11-C Studio] Installing PySide6...
  python -m pip install -r requirements.txt
  if errorlevel 1 exit /b 1
)
python main.py %*
endlocal
