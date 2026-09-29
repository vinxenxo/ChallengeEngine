@echo off
setlocal
set "C11C_PROJECT_ROOT=%~dp0..\.."
for %%I in ("%C11C_PROJECT_ROOT%") do set "C11C_PROJECT_ROOT=%%~fI"
cd /d "%C11C_PROJECT_ROOT%"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%C11C_PROJECT_ROOT%\FULL_ACCEPTANCE_C11C_2.19.12.ps1" %*
set "EXITCODE=%ERRORLEVEL%"
endlocal & exit /b %EXITCODE%
