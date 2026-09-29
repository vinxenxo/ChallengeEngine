@echo off
setlocal
set "C11C_PROJECT_ROOT=%~dp0..\.."
for %%I in ("%C11C_PROJECT_ROOT%") do set "C11C_PROJECT_ROOT=%%~fI"
if "%~1"=="" (
  echo Usage: run_suite.bat ^<SuiteFile.gd^>
  endlocal & exit /b 2
)
set "GODOT_CMD=%GODOT_BIN%"
if not defined GODOT_CMD set "GODOT_CMD=godot"
cd /d "%C11C_PROJECT_ROOT%"
"%GODOT_CMD%" --headless --path "%C11C_PROJECT_ROOT%" --script "%C11C_PROJECT_ROOT%\tests\%~1"
set "EXITCODE=%ERRORLEVEL%"
endlocal & exit /b %EXITCODE%
