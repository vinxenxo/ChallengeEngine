@echo off
setlocal
set "C11C_PROJECT_ROOT=%~dp0..\.."
cd /d "%C11C_PROJECT_ROOT%"
python ".\tests\run_all.py" %*
set "RC=%ERRORLEVEL%"
endlocal & exit /b %RC%
