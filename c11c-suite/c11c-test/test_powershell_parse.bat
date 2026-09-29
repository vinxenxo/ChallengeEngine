@echo off
setlocal
set "C11C_PROJECT_ROOT=%~dp0..\.."
cd /d "%C11C_PROJECT_ROOT%"
python "%C11C_PROJECT_ROOT%\c11c-suite\c11c-test\test_powershell_parse.py"
set "EXITCODE=%ERRORLEVEL%"
endlocal & exit /b %EXITCODE%
