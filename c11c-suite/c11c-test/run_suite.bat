@echo off
setlocal
if "%~1"=="" (
  echo Uso: run_suite.bat NombreTest.gd
  echo Ejemplo: run_suite.bat C11CProductionReviewCopySafetyTest.gd
  endlocal & exit /b 2
)
set "C11C_PROJECT_ROOT=%~dp0..\.."
cd /d "%C11C_PROJECT_ROOT%"
set "GODOT_CMD=%GODOT_BIN%"
if not defined GODOT_CMD set "GODOT_CMD=godot.exe"
where "%GODOT_CMD%" >nul 2>nul
if not errorlevel 1 (
  "%GODOT_CMD%" --headless --path "%C11C_PROJECT_ROOT%" --script ".\tests\%~1"
  set "RC=%ERRORLEVEL%"
) else (
  echo ERROR: godot.exe no esta en PATH. Define GODOT_BIN o anade Godot al PATH.
  set "RC=127"
)
endlocal & exit /b %RC%
