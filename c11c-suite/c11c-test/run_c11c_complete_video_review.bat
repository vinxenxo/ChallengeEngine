@echo off
setlocal
set "C11C_PROJECT_ROOT=%~dp0..\.."
for %%I in ("%C11C_PROJECT_ROOT%") do set "C11C_PROJECT_ROOT=%%~fI"
cd /d "%C11C_PROJECT_ROOT%"
call "%C11C_PROJECT_ROOT%\c11c-suite\c11c-test\run_c11c_complete_review.bat" %*
set "EXITCODE=%ERRORLEVEL%"
endlocal & exit /b %EXITCODE%
