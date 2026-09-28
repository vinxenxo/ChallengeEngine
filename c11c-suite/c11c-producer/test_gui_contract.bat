@echo off
setlocal
set C11C_PROJECT_ROOT=%~dp0..\..
cd /d "%C11C_PROJECT_ROOT%"
python "%~dp0test_producer_gui_contract.py" %*
set "RC=%ERRORLEVEL%"
endlocal & exit /b %RC%
