@echo off
setlocal
set "C11C_PROJECT_ROOT=%~dp0..\.."
cd /d "%C11C_PROJECT_ROOT%"
call "%~dp0..\c11c-maintenance\run.bat" %*
set "RC=%ERRORLEVEL%"
exit /b %RC%
