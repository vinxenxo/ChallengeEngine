@echo off
setlocal
cd /d "%~dp0"
PowerShell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0resume_c11c_full_art_direction_corpus_after_longform.ps1" %*
if errorlevel 1 (
  echo.
  echo C11-C RESUME FAILED.
  exit /b 1
)
echo.
echo C11-C RESUME COMPLETE.
exit /b 0
