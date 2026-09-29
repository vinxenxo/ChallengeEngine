@echo off
setlocal
set "C11C_PROJECT_ROOT=%~dp0..\.."
cd /d "%C11C_PROJECT_ROOT%"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%C11C_PROJECT_ROOT%\c11c-suite\c11c-test\run_c11c_challenge_family_smoke.ps1" %*
set "EXITCODE=%ERRORLEVEL%"
endlocal & exit /b %EXITCODE%
