@echo off
setlocal
set C11C_PROJECT_ROOT=%~dp0..\..
python "%~dp0main.py" %*
endlocal
