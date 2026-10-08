@echo off
setlocal
set "C11C_PROJECT_ROOT=%~dp0..\.."
for %%I in ("%C11C_PROJECT_ROOT%") do set "C11C_PROJECT_ROOT=%%~fI"
cd /d "%C11C_PROJECT_ROOT%"
python "%C11C_PROJECT_ROOT%\c11c-suite\c11d-control\main.py" %*
set "EXITCODE=%ERRORLEVEL%"
endlocal & exit /b %EXITCODE%
